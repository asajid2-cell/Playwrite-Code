/* eslint-disable no-console */
export type LogLevel = 'info' | 'warn' | 'error' | 'debug';

const LEVEL_COLORS: Record<LogLevel, string> = {
  info: '\x1b[32m',
  warn: '\x1b[33m',
  error: '\x1b[31m',
  debug: '\x1b[36m',
};

export interface LoggerOptions {
  level?: LogLevel;
  json?: boolean;
}

export class Logger {
  #levelOrder: Record<LogLevel, number> = {
    error: 0,
    warn: 1,
    info: 2,
    debug: 3,
  };

  #current: LogLevel;
  #json: boolean;

  constructor(opts: LoggerOptions = {}) {
    this.#current = opts.level ?? 'info';
    this.#json = opts.json ?? false;
  }

  info(message: string, extra: Record<string, unknown> = {}) {
    this.#log('info', message, extra);
  }

  warn(message: string, extra: Record<string, unknown> = {}) {
    this.#log('warn', message, extra);
  }

  error(message: string, extra: Record<string, unknown> = {}) {
    this.#log('error', message, extra);
  }

  debug(message: string, extra: Record<string, unknown> = {}) {
    this.#log('debug', message, extra);
  }

  #log(level: LogLevel, message: string, extra: Record<string, unknown>) {
    if (this.#levelOrder[level] > this.#levelOrder[this.#current]) return;
    const payload = { level, message, timestamp: new Date().toISOString(), ...extra };
    if (this.#json) {
      console.log(JSON.stringify(payload));
      return;
    }
    const color = LEVEL_COLORS[level];
    const reset = '\x1b[0m';
    console.log(`${color}[${payload.timestamp}] [${level.toUpperCase()}] ${message}${reset}`);
    if (Object.keys(extra).length) console.log(extra);
  }
}
