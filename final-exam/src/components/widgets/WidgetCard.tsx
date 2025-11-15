import { useState } from 'react';
import type { Widget } from '../../types';
import { useWorkspaceStore } from '../../state/useWorkspaceStore';
import { ChartWidgetView } from './chart/ChartWidgetView';
import { TableWidgetView } from './table/TableWidgetView';
import { NotesWidgetView } from './notes/NotesWidgetView';
import { WidgetSettingsModal } from './WidgetSettingsModal';

interface Props {
  widget: Widget;
}

export function WidgetCard({ widget }: Props) {
  const deleteWidget = useWorkspaceStore((s) => s.deleteWidget);
  const updateTitle = useWorkspaceStore((s) => s.updateWidgetTitle);
  const [settingsOpen, setSettingsOpen] = useState(false);

  const handleDelete = () => {
    if (window.confirm(`Delete widget "${widget.title}"?`)) {
      deleteWidget(widget.id);
    }
  };

  const renderWidget = () => {
    switch (widget.type) {
      case 'chart':
        return <ChartWidgetView widget={widget} />;
      case 'table':
        return <TableWidgetView widget={widget} />;
      case 'notes':
        return <NotesWidgetView widget={widget} />;
      default:
        return <div>Unknown widget</div>;
    }
  };

  return (
    <div className="widget-card">
      <div className="widget-header">
        <input
          value={widget.title}
          onChange={(e) => updateTitle(widget.id, e.target.value)}
          className="widget-title-input"
          aria-label={`Widget title ${widget.title}`}
        />
        <div className="widget-actions">
          <button
            className="icon-button"
            aria-label={`Configure ${widget.title}`}
            onClick={() => setSettingsOpen(true)}
          >
            ⚙
          </button>
          <button
            className="icon-button"
            aria-label={`Delete ${widget.title}`}
            onClick={handleDelete}
          >
            🗑
          </button>
        </div>
      </div>
      <div className="widget-body">{renderWidget()}</div>
      {settingsOpen && <WidgetSettingsModal widget={widget} onClose={() => setSettingsOpen(false)} />}
    </div>
  );
}
