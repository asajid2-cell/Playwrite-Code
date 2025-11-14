import type { ChartMetric, ChartRange } from '../types';

const metricSeeds: Record<ChartMetric, number> = {
  users: 1200,
  revenue: 45000,
  sessions: 3200,
};

const rangeDays: Record<ChartRange, number> = {
  '7d': 7,
  '30d': 30,
  '90d': 90,
};

export interface SeriesPoint {
  date: string;
  value: number;
}

export function generateSeries(metric: ChartMetric, range: ChartRange): SeriesPoint[] {
  const days = rangeDays[range];
  const base = metricSeeds[metric];
  const now = new Date();
  const points: SeriesPoint[] = [];

  for (let i = days - 1; i >= 0; i--) {
    const d = new Date(now);
    d.setDate(now.getDate() - i);
    const noise = Math.sin(i / 3) * 0.1 + Math.random() * 0.05;
    const value = Math.round(base * (1 + noise));
    points.push({
      date: d.toISOString().slice(0, 10),
      value,
    });
  }

  return points;
}

export interface TableRow {
  id: string;
  name: string;
  event: string;
  value: number;
  city: string;
}

const sampleEvents = ['Signup', 'Purchase', 'Logout', 'Upgrade', 'Churn', 'Invite'];
const sampleCities = ['Seattle', 'London', 'Berlin', 'NYC', 'Paris', 'Tokyo', 'Sydney'];

export function generateTableRows(count = 750): TableRow[] {
  const rows: TableRow[] = [];
  for (let i = 0; i < count; i++) {
    rows.push({
      id: `row-${i}`,
      name: `User ${i + 1}`,
      event: sampleEvents[i % sampleEvents.length],
      value: Math.floor(Math.random() * 1000),
      city: sampleCities[i % sampleCities.length],
    });
  }
  return rows;
}
