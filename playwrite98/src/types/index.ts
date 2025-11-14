export * from './plan.js';

export interface StepContext {
  runId: string;
  snapshotHash?: string;
  storedValues: Record<string, unknown>;
}

export interface ActionResult {
  stepId: string;
  status: 'success' | 'skipped' | 'error';
  startedAt: string;
  finishedAt: string;
  message?: string;
  artifacts?: string[];
  snapshotHash?: string;
}
