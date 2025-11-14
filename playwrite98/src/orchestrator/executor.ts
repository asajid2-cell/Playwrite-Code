import { mkdir, writeFile } from 'fs/promises';
import path from 'path';
import type { PlanDefinition, PlanStep, ActionResult, StepContext } from '../types/index.js';
import { Logger } from '../utils/logger.js';
import { BrowserSession } from './session.js';
import { SnapshotStore } from '../snapshot/store.js';

export interface ExecutionSummary {
  runId: string;
  outputDir: string;
  results: ActionResult[];
}

export class PlanExecutor {
  #plan: PlanDefinition;
  #logger: Logger;

  constructor(plan: PlanDefinition, logger: Logger) {
    this.#plan = plan;
    this.#logger = logger;
  }

  async run(): Promise<ExecutionSummary> {
    const runId = new Date().toISOString().replace(/[:.]/g, '-');
    const outputDir = this.#plan.outputDir ?? path.join(process.cwd(), 'artifacts', runId);
    await mkdir(outputDir, { recursive: true });
    const session = new BrowserSession(
      {
        outputDir,
        capabilities: this.#plan.capabilities,
        env: this.#plan.env,
      },
      this.#logger,
    );
    const snapshotStore = new SnapshotStore(path.join(outputDir, 'snapshots'), this.#logger);
    await snapshotStore.init();
    const results: ActionResult[] = [];
    const ctx: StepContext = { runId, storedValues: {} };
    try {
      await session.start(this.#plan.startUrl);
      for (const step of this.#plan.steps) {
        const startedAt = new Date().toISOString();
        try {
          const artifacts = await this.#executeStep(session, snapshotStore, ctx, step);
          const finishedAt = new Date().toISOString();
          results.push({
            stepId: step.id,
            status: 'success',
            startedAt,
            finishedAt,
            artifacts,
            snapshotHash: ctx.snapshotHash,
          });
        } catch (error) {
          const finishedAt = new Date().toISOString();
          const message = error instanceof Error ? error.message : String(error);
          this.#logger.error(`Step ${step.id} failed`, { message });
          results.push({
            stepId: step.id,
            status: 'error',
            startedAt,
            finishedAt,
            message,
          });
          if (!step.continueOnError) break;
        }
      }
    } finally {
      await session.dispose();
      const summaryPath = path.join(outputDir, 'run.json');
      await writeFile(summaryPath, JSON.stringify({ runId, results }, null, 2));
      this.#logger.info('Execution summary written', { summaryPath });
    }
    return { runId, outputDir, results };
  }

  async #executeStep(
    session: BrowserSession,
    snapshotStore: SnapshotStore,
    ctx: StepContext,
    step: PlanStep,
  ) {
    const page = session.page;
    switch (step.kind) {
      case 'navigate': {
        this.#logger.info(`Navigating to ${step.url}`);
        await page.goto(step.url, { waitUntil: step.waitUntil });
        return [];
      }
      case 'waitFor': {
        this.#logger.info('Waiting for condition', step);
        if (step.selector) {
          await page.waitForSelector(step.selector, { timeout: step.timeoutMs });
        } else if (step.role || step.name) {
          await page.getByRole(step.role ?? 'button', { name: step.name, exact: false }).waitFor();
        } else {
          await page.waitForTimeout(step.timeoutMs);
        }
        return [];
      }
      case 'click': {
        this.#logger.info('Clicking target', step);
        if (step.selector) {
          await page.click(step.selector, {
            clickCount: step.clickCount,
            delay: step.delayMs,
          });
        } else {
          await page
            .getByRole(step.role ?? 'button', { name: step.name, exact: false })
            .click({ clickCount: step.clickCount, delay: step.delayMs });
        }
        return [];
      }
      case 'fill': {
        this.#logger.info(`Filling ${step.selector}`);
        await page.fill(step.selector, step.value);
        if (step.submit) await page.keyboard.press('Enter');
        return [];
      }
      case 'evaluate': {
        this.#logger.info('Evaluating expression');
        const result = await page.evaluate(step.expression, step.args);
        if (step.storeAs) ctx.storedValues[step.storeAs] = result;
        return [];
      }
      case 'assertText': {
        this.#logger.info(`Asserting text contains ${step.includes}`);
        await page.getByText(step.includes, { exact: false }).waitFor();
        return [];
      }
      case 'snapshot': {
        this.#logger.info(`Capturing snapshot ${step.label}`);
        const artifact = await snapshotStore.capture(page, step.label, step.includeDOM);
        ctx.snapshotHash = artifact.hash;
        return [artifact.filePath, artifact.domPath].filter(Boolean) as string[];
      }
      default: {
        const _exhaustive: never = step;
        throw new Error(`Unsupported step ${(_exhaustive as { id: string }).id}`);
      }
    }
  }
}
