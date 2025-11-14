export type WidgetType = 'chart' | 'table' | 'notes';

export type ChartMetric = 'users' | 'revenue' | 'sessions';
export type ChartRange = '7d' | '30d' | '90d';
export type ChartMode = 'line' | 'bar';

export interface ChartConfig {
  metric: ChartMetric;
  range: ChartRange;
  mode: ChartMode;
}

export interface TableConfig {
  filter: string;
  sortBy: 'name' | 'event' | 'value';
  sortDir: 'asc' | 'desc';
  page: number;
  pageSize: number;
}

export interface NotesConfig {
  content: string;
}

export type WidgetConfig = ChartConfig | TableConfig | NotesConfig;

export interface WidgetBase {
  id: string;
  type: WidgetType;
  title: string;
  x: number;
  y: number;
  w: number;
  h: number;
}

export interface ChartWidget extends WidgetBase {
  type: 'chart';
  config: ChartConfig;
}

export interface TableWidget extends WidgetBase {
  type: 'table';
  config: TableConfig;
}

export interface NotesWidget extends WidgetBase {
  type: 'notes';
  config: NotesConfig;
}

export type Widget = ChartWidget | TableWidget | NotesWidget;

export interface Dashboard {
  id: string;
  name: string;
  widgets: Widget[];
  updatedAt: string;
}

export type SaveStatus = 'idle' | 'saving' | 'saved' | 'error';
