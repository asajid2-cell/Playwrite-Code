import { useWorkspaceStore } from '../state/useWorkspaceStore';
import type { Dashboard } from '../types';

export function Sidebar() {
  const dashboards = useWorkspaceStore((s) => s.dashboards);
  const currentId = useWorkspaceStore((s) => s.currentDashboardId);
  const select = useWorkspaceStore((s) => s.selectDashboard);
  const createDashboard = useWorkspaceStore((s) => s.createDashboard);
  const deleteDashboard = useWorkspaceStore((s) => s.deleteDashboard);

  const handleDelete = (dashboard: Dashboard) => {
    if (window.confirm(`Delete dashboard "${dashboard.name}"?`)) {
      deleteDashboard(dashboard.id);
    }
  };

  return (
    <aside className="sidebar" aria-label="Dashboards">
      <div className="sidebar-header">
        <h1>Workspaces</h1>
        <button className="primary" onClick={createDashboard}>
          + New dashboard
        </button>
      </div>
      <ul className="dashboard-list">
        {dashboards.map((dash) => (
          <li key={dash.id}>
            <button
              className={`dashboard-item ${dash.id === currentId ? 'active' : ''}`}
              onClick={() => select(dash.id)}
            >
              <div>
                <strong>{dash.name}</strong>
                <small>Updated {new Date(dash.updatedAt).toLocaleString()}</small>
              </div>
              <span className="sr-only">Select dashboard {dash.name}</span>
            </button>
            <button
              className="icon-button"
              aria-label={`Delete dashboard ${dash.name}`}
              onClick={() => handleDelete(dash)}
            >
              ×
            </button>
          </li>
        ))}
      </ul>
      {dashboards.length === 0 && (
        <p className="muted">No dashboards yet. Create your first dashboard.</p>
      )}
    </aside>
  );
}
