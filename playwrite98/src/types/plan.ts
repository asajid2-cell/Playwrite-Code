import { z } from 'zod';

export const capabilitySchema = z.enum(['pdf', 'testing', 'tracing', 'media', 'none']);

const baseStepSchema = z.object({
  id: z.string().min(1),
  description: z.string().optional(),
  continueOnError: z.boolean().default(false),
});

const navigateStepSchema = baseStepSchema.extend({
  kind: z.literal('navigate'),
  url: z.string().url(),
  waitUntil: z.enum(['load', 'domcontentloaded', 'networkidle']).default('load'),
});

const waitStepSchema = baseStepSchema.extend({
  kind: z.literal('waitFor'),
  role: z.string().optional(),
  name: z.string().optional(),
  selector: z.string().optional(),
  timeoutMs: z.number().int().positive().default(10000),
});

const clickStepSchema = baseStepSchema.extend({
  kind: z.literal('click'),
  selector: z.string().optional(),
  role: z.string().optional(),
  name: z.string().optional(),
  clickCount: z.number().int().positive().default(1),
  delayMs: z.number().int().nonnegative().default(0),
});

const fillStepSchema = baseStepSchema.extend({
  kind: z.literal('fill'),
  selector: z.string(),
  value: z.string(),
  submit: z.boolean().default(false),
});

const evaluateStepSchema = baseStepSchema.extend({
  kind: z.literal('evaluate'),
  expression: z.string().min(1),
  args: z.record(z.unknown()).optional(),
  storeAs: z.string().optional(),
});

const assertTextStepSchema = baseStepSchema.extend({
  kind: z.literal('assertText'),
  target: z.string(),
  includes: z.string(),
});

const snapshotStepSchema = baseStepSchema.extend({
  kind: z.literal('snapshot'),
  label: z.string().min(1),
  includeDOM: z.boolean().default(false),
});

export const stepSchema = z.discriminatedUnion('kind', [
  navigateStepSchema,
  waitStepSchema,
  clickStepSchema,
  fillStepSchema,
  evaluateStepSchema,
  assertTextStepSchema,
  snapshotStepSchema,
]);

export const planSchema = z.object({
  name: z.string(),
  description: z.string().optional(),
  startUrl: z.string().url(),
  capabilities: z.array(capabilitySchema).default(['none']),
  env: z.record(z.string()).default({}),
  outputDir: z.string().optional(),
  steps: z.array(stepSchema).min(1),
});

export type Capability = z.infer<typeof capabilitySchema>;
export type PlanDefinition = z.infer<typeof planSchema>;
export type PlanStep = z.infer<typeof stepSchema>;
