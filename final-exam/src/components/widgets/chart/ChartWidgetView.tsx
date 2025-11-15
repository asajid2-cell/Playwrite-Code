import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, BarChart, Bar, CartesianGrid } from 'recharts';
import type { ChartWidget } from '../../../types';
import { generateSeries } from '../../../utils/data';

interface Props {
  widget: ChartWidget;
}

export function ChartWidgetView({ widget }: Props) {
  const data = generateSeries(widget.config.metric, widget.config.range);

  return (
    <div className="chart-widget">
      <ResponsiveContainer width="100%" height="100%">
        {widget.config.mode === 'line' ? (
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" hide />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="value" stroke="#8884d8" dot={false} />
          </LineChart>
        ) : (
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" hide />
            <YAxis />
            <Tooltip />
            <Bar dataKey="value" fill="#10b981" />
          </BarChart>
        )}
      </ResponsiveContainer>
    </div>
  );
}
