import { useEffect } from 'react';
import { Sidebar } from './components/Sidebar';
import { DashboardHeader } from './components/DashboardHeader';
import { Workspace } from './components/Workspace';
import { useWorkspaceStore, useCurrentDashboard } from './state/useWorkspaceStore';
import './index.css';

export function App() {
  const dashboard = useCurrentDashboard();
  const dashboards = useWorkspaceStore((s) => s.dashboards);
  const selectDashboard = useWorkspaceStore((s) => s.selectDashboard);

  useEffect(() => {
    if (!dashboard && dashboards.length > 0) {
      selectDashboard(dashboards[0].id);
    }
  }, [dashboard, dashboards, selectDashboard]);

  return (
    <div className="app-shell">
      <Sidebar />
      <main className="main-area">
        {dashboard ? (
          <>
            <DashboardHeader dashboard={dashboard} />
            <Workspace dashboard={dashboard} />
          </>
        ) : (
          <div className="empty-state">
            <h2>No dashboards yet</h2>
            <p>Create a dashboard from the sidebar to get started.</p>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
