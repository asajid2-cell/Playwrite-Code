import { mkdir } from 'fs/promises';
import path from 'path';
import { chromium, type Browser, type BrowserContext, type Page } from 'playwright';
import type { Capability } from '../types/index.js';
import { Logger } from '../utils/logger.js';

export interface SessionOptions {
  headless?: boolean;
  outputDir: string;
  capabilities: Capability[];
  env: Record<string, string>;
}

export class BrowserSession {
  #browser?: Browser;
  #context?: BrowserContext;
  #page?: Page;
  #logger: Logger;
  #opts: SessionOptions;

  constructor(opts: SessionOptions, logger: Logger) {
    this.#opts = opts;
    this.#logger = logger;
  }

  get page() {
    if (!this.#page) throw new Error('Session not started');
    return this.#page;
  }

  async start(startUrl: string) {
    await mkdir(this.#opts.outputDir, { recursive: true });
    this.#browser = await chromium.launch({
      headless: this.#opts.headless ?? true,
      env: this.#opts.env,
    });
    this.#context = await this.#browser.newContext({
      recordVideo: this.#opts.capabilities.includes('media')
        ? { dir: path.join(this.#opts.outputDir, 'video') }
        : undefined,
    });
    this.#page = await this.#context.newPage();
    this.#logger.info('Browser session started', { startUrl });
    await this.#page.goto(startUrl);
  }

  async dispose() {
    await this.#page?.close();
    await this.#context?.close();
    await this.#browser?.close();
    this.#logger.info('Browser session closed');
  }
}
