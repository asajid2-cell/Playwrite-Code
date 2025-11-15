import type { Widget, ChartWidget, TableWidget, NotesWidget } from '../../types';
import { useWorkspaceStore } from '../../state/useWorkspaceStore';

interface Props {
  widget: Widget;
  onClose: () => void;
}

export function WidgetSettingsModal({ widget, onClose }: Props) {
  const updateConfig = useWorkspaceStore((s) => s.updateWidgetConfig);

  const renderForm = () => {
    if (widget.type === 'chart') {
      const config = widget.config as ChartWidget['config'];
      return (
        <>
          <label>
            Metric
            <select value={config.metric} onChange={(e) => updateConfig(widget.id, { metric: e.target.value })}>
              <option value="users">Users</option>
              <option value="revenue">Revenue</option>
              <option value="sessions">Sessions</option>
            </select>
          </label>
          <label>
            Range
            <select value={config.range} onChange={(e) => updateConfig(widget.id, { range: e.target.value })}>
              <option value="7d">7 days</option>
              <option value="30d">30 days</option>
              <option value="90d">90 days</option>
            </select>
          </label>
          <label>
            Mode
            <select value={config.mode} onChange={(e) => updateConfig(widget.id, { mode: e.target.value })}>
              <option value="line">Line</option>
              <option value="bar">Bar</option>
            </select>
          </label>
        </>
      );
    }
    if (widget.type === 'table') {
      const config = widget.config as TableWidget['config'];
      return (
        <>
          <label>
            Rows per page
            <input
              type="number"
              value={config.pageSize}
              min={10}
              max={100}
              onChange={(e) => updateConfig(widget.id, { pageSize: Number(e.target.value) })}
            />
          </label>
          <label>
            Sort column
            <select value={config.sortBy} onChange={(e) => updateConfig(widget.id, { sortBy: e.target.value })}>
              <option value="name">Name</option>
              <option value="event">Event</option>
              <option value="value">Value</option>
            </select>
          </label>
          <label>
            Sort direction
            <select value={config.sortDir} onChange={(e) => updateConfig(widget.id, { sortDir: e.target.value })}>
              <option value="asc">Ascending</option>
              <option value="desc">Descending</option>
            </select>
          </label>
        </>
      );
    }
    const config = widget.config as NotesWidget['config'];
    return (
      <label>
        Default text
        <textarea
          value={config.content}
          onChange={(e) => updateConfig(widget.id, { content: e.target.value })}
          rows={6}
        />
      </label>
    );
  };

  return (
    <div className="modal-backdrop" role="dialog" aria-modal="true">
      <div className="modal">
        <header>
          <h3>{widget.title} settings</h3>
        </header>
        <div className="modal-body">{renderForm()}</div>
        <footer className="modal-footer">
          <button onClick={onClose}>Close</button>
        </footer>
      </div>
    </div>
  );
}
