#!/usr/bin/env node
import { readFile } from 'fs/promises';
import path from 'path';
import { Command } from 'commander';
import { planSchema, type PlanDefinition } from './types/plan.js';
import { Logger } from './utils/logger.js';
import { PlanExecutor } from './orchestrator/executor.js';

async function loadPlan(filePath: string): Promise<PlanDefinition> {
  const data = await readFile(filePath, 'utf-8');
  const parsed = JSON.parse(data);
  return planSchema.parse(parsed);
}

export async function main(argv: string[] = process.argv) {
  const program = new Command();
  program.name('playwrite98').description('Token-efficient UI automation harness');

  program
    .command('run')
    .argument('<planFile>', 'Path to a plan JSON file')
    .option('--out <dir>', 'Override output directory')
    .option('--log-level <level>', 'info | warn | error | debug', 'info')
    .action(async (planFile: string, options: { out?: string; logLevel: string }) => {
      const logger = new Logger({ level: options.logLevel as any });
      const resolved = path.resolve(planFile);
      logger.info('Loading plan', { file: resolved });
      const plan = await loadPlan(resolved);
      if (options.out) plan.outputDir = path.resolve(options.out);
      const executor = new PlanExecutor(plan, logger);
      const summary = await executor.run();
      logger.info('Run completed', summary);
    });

  await program.parseAsync(argv);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
