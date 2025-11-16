import type { Dashboard, WidgetType } from '../types';
import { useWorkspaceStore } from '../state/useWorkspaceStore';
import { WidgetCard } from './widgets/WidgetCard';

interface Props {
  dashboard: Dashboard;
}

export function Workspace({ dashboard }: Props) {
  const addWidget = useWorkspaceStore((s) => s.addWidget);

  const handleAdd = (type: WidgetType) => {
    addWidget(type);
  };

  return (
    <section className="workspace">
      <div className="workspace-toolbar" data-test="workspace-toolbar">
        <div>
          <span>Add widget:</span>
          <button data-test="add-chart" onClick={() => handleAdd('chart')}>
            Chart
          </button>
          <button data-test="add-table" onClick={() => handleAdd('table')}>
            Table
          </button>
          <button data-test="add-notes" onClick={() => handleAdd('notes')}>
            Notes
          </button>
        </div>
      </div>
      {dashboard.widgets.length === 0 ? (
        <div className="empty-area">
          <p>No widgets yet. Use the buttons above to add your first widget.</p>
        </div>
      ) : (
        <div className="simple-grid">
          {dashboard.widgets.map((widget) => (
            <WidgetCard key={widget.id} widget={widget} />
          ))}
        </div>
      )}
    </section>
  );
}
