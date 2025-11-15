import { useState } from 'react';
import { useWorkspaceStore } from '../state/useWorkspaceStore';
import type { Dashboard } from '../types';

interface Props {
  dashboard: Dashboard;
}

const statusCopy: Record<string, string> = {
  idle: '',
  saving: 'Saving…',
  saved: 'Saved',
  error: 'Save failed',
};

export function DashboardHeader({ dashboard }: Props) {
  const rename = useWorkspaceStore((s) => s.renameDashboard);
  const saveStatus = useWorkspaceStore((s) => s.saveStatus);
  const saveError = useWorkspaceStore((s) => s.saveError);
  const retry = useWorkspaceStore((s) => s.retrySave);
  const [name, setName] = useState(dashboard.name);

  const handleBlur = () => {
    if (name.trim().length === 0) {
      setName(dashboard.name);
      return;
    }
    rename(name.trim());
  };

  return (
    <header className="dash-header">
      <div className="dash-title">
        <input
          value={name}
          onChange={(e) => setName(e.target.value)}
          onBlur={handleBlur}
          className="title-input"
          aria-label="Dashboard name"
        />
        <div className={`save-status ${saveStatus}`}>
          {statusCopy[saveStatus] || `Saved ${new Date(dashboard.updatedAt).toLocaleTimeString()}`}
          {saveStatus === 'error' && saveError && (
            <button className="link-button" onClick={retry}>
              Retry
            </button>
          )}
        </div>
      </div>
      <div className="dash-meta">
        <span>Last saved {new Date(dashboard.updatedAt).toLocaleString()}</span>
      </div>
    </header>
  );
}
