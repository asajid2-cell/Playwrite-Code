import { useMemo } from 'react';
import type { TableWidget } from '../../../types';
import { generateTableRows } from '../../../utils/data';
import { useWorkspaceStore } from '../../../state/useWorkspaceStore';

// Lazy initialization - only generate once when first needed
let masterRows: ReturnType<typeof generateTableRows> | null = null;
const getMasterRows = () => {
  if (!masterRows) {
    masterRows = generateTableRows(750);
  }
  return masterRows;
};

interface Props {
  widget: TableWidget;
}

export function TableWidgetView({ widget }: Props) {
  const updateConfig = useWorkspaceStore((s) => s.updateWidgetConfig);
  const { filter, sortBy, sortDir, page, pageSize } = widget.config;

  const filtered = useMemo(() => {
    const keyword = filter.toLowerCase();
    const allRows = getMasterRows();
    const rows = allRows.filter(
      (row) =>
        row.name.toLowerCase().includes(keyword) ||
        row.event.toLowerCase().includes(keyword) ||
        row.city.toLowerCase().includes(keyword),
    );
    // Create a copy before sorting to avoid mutation
    return [...rows].sort((a, b) => {
      const dir = sortDir === 'asc' ? 1 : -1;
      if (sortBy === 'value') {
        return (a.value - b.value) * dir;
      }
      return a[sortBy].localeCompare(b[sortBy]) * dir;
    });
  }, [filter, sortBy, sortDir]);

  const totalPages = Math.ceil(filtered.length / pageSize);
  const currentPage = Math.min(page, totalPages - 1);
  const pagedRows = filtered.slice(currentPage * pageSize, currentPage * pageSize + pageSize);

  const updateSort = (column: TableWidget['config']['sortBy']) => {
    const nextDir = sortBy === column && sortDir === 'asc' ? 'desc' : 'asc';
    updateConfig(widget.id, { sortBy: column, sortDir: nextDir, page: 0 });
  };

  return (
    <div className="table-widget">
      <div className="table-controls">
        <input
          value={filter}
          placeholder="Search users or events"
          onChange={(e) => updateConfig(widget.id, { filter: e.target.value, page: 0 })}
        />
        <div className="table-sorts">
          <button onClick={() => updateSort('name')}>Name</button>
          <button onClick={() => updateSort('event')}>Event</button>
          <button onClick={() => updateSort('value')}>Value</button>
        </div>
      </div>
      <div className="table-head">
        <span>Name</span>
        <span>Event</span>
        <span>City</span>
        <span>Value</span>
      </div>
      <div className="table-body">
        {pagedRows.map((row) => (
          <div className="table-row" key={row.id}>
            <span>{row.name}</span>
            <span>{row.event}</span>
            <span>{row.city}</span>
            <span>{row.value}</span>
          </div>
        ))}
        {pagedRows.length === 0 && <p className="muted">No matching records.</p>}
      </div>
      <div className="table-pagination">
        <button
          disabled={currentPage === 0}
          onClick={() => updateConfig(widget.id, { page: Math.max(0, currentPage - 1) })}
        >
          Prev
        </button>
        <span>
          Page {currentPage + 1} / {Math.max(totalPages, 1)}
        </span>
        <button
          disabled={currentPage >= totalPages - 1}
          onClick={() =>
            updateConfig(widget.id, { page: Math.min(totalPages - 1, currentPage + 1) })
          }
        >
          Next
        </button>
      </div>
    </div>
  );
}
