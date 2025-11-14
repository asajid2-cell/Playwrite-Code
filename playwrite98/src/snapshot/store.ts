import { createHash } from 'crypto';
import { mkdir, writeFile } from 'fs/promises';
import path from 'path';
import type { AccessibilitySnapshot, Page } from 'playwright';
import { Logger } from '../utils/logger.js';

export interface SnapshotArtifact {
  label: string;
  hash: string;
  filePath: string;
  domPath?: string;
}

export class SnapshotStore {
  #dir: string;
  #logger: Logger;

  constructor(dir: string, logger: Logger) {
    this.#dir = dir;
    this.#logger = logger;
  }

  async init() {
    await mkdir(this.#dir, { recursive: true });
  }

  async capture(page: Page, label: string, includeDOM = false): Promise<SnapshotArtifact> {
    const snapshot = await page.accessibility.snapshot({ interestingOnly: false });
    const dom = includeDOM ? await page.content() : undefined;
    const hash = this.#hashSnapshot(snapshot, dom);
    const filePath = path.join(this.#dir, `${label}-${hash}.json`);
    await writeFile(filePath, JSON.stringify(snapshot, null, 2), 'utf-8');
    let domPath: string | undefined;
    if (dom) {
      domPath = path.join(this.#dir, `${label}-${hash}.html`);
      await writeFile(domPath, dom, 'utf-8');
    }
    this.#logger.info(`Captured snapshot ${label}`, { hash, filePath });
    return { label, hash, filePath, domPath };
  }

  #hashSnapshot(snapshot: AccessibilitySnapshot, dom?: string) {
    const hash = createHash('sha256');
    hash.update(JSON.stringify(snapshot));
    if (dom) hash.update(dom);
    return hash.digest('hex').slice(0, 16);
  }
}
