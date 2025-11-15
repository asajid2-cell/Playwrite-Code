import { WidthProvider, Responsive as ResponsiveGridLayout, type Layout } from 'react-grid-layout';
import type { Dashboard, WidgetType } from '../types';
import { useWorkspaceStore } from '../state/useWorkspaceStore';
import { WidgetCard } from './widgets/WidgetCard';
import 'react-grid-layout/css/styles.css';
import 'react-resizable/css/styles.css';

const ResponsiveGrid = WidthProvider(ResponsiveGridLayout);

interface Props {
  dashboard: Dashboard;
}

const cols = { lg: 12, md: 8, sm: 4, xs: 2, xxs: 1 };
const breakpoints = { lg: 1200, md: 996, sm: 768, xs: 480, xxs: 0 };

export function Workspace({ dashboard }: Props) {
  const addWidget = useWorkspaceStore((s) => s.addWidget);
  const updateLayout = useWorkspaceStore((s) => s.updateLayout);

  const layout: Layout[] = dashboard.widgets.map((w) => ({
    i: w.id,
    x: w.x,
    y: w.y,
    w: w.w,
    h: w.h,
  }));

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
        <p className="muted">Drag widgets by their body and resize by the handle in the lower-right corner.</p>
      </div>
      {dashboard.widgets.length === 0 ? (
        <div className="empty-area">
          <p>No widgets yet. Use the buttons above to add your first widget.</p>
        </div>
      ) : (
        <ResponsiveGrid
          className="layout"
          layouts={{ lg: layout, md: layout, sm: layout, xs: layout, xxs: layout }}
          breakpoints={breakpoints}
          cols={cols}
          rowHeight={40}
          isDraggable
          isResizable
          onLayoutChange={(next) => updateLayout(next as Layout[])}
          draggableHandle=".widget-card"
          measureBeforeMount={false}
          compactType="vertical"
          useCSSTransforms
        >
          {dashboard.widgets.map((widget) => (
            <div key={widget.id} data-grid={{ i: widget.id }}>
              <WidgetCard widget={widget} />
            </div>
          ))}
        </ResponsiveGrid>
      )}
    </section>
  );
}
