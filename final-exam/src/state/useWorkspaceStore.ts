import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { Dashboard, Widget, WidgetType, ChartWidget, TableWidget, NotesWidget, SaveStatus } from '../types';
import type { Layout } from 'react-grid-layout';

type WorkspaceState = {
  dashboards: Dashboard[];
  currentDashboardId?: string;
  saveStatus: SaveStatus;
  saveError?: string;
  createDashboard: () => void;
  selectDashboard: (id: string) => void;
  deleteDashboard: (id: string) => void;
  renameDashboard: (name: string) => void;
  addWidget: (type: WidgetType) => void;
  deleteWidget: (id: string) => void;
  updateWidgetTitle: (id: string, title: string) => void;
  updateWidgetConfig: (id: string, config: Record<string, unknown>) => void;
  updateLayout: (layout: Layout[]) => void;
  updateNotesContent: (id: string, content: string) => void;
  retrySave: () => void;
};

const randomId = () => crypto.randomUUID();

const createChart = (overrides: Partial<ChartWidget> = {}): ChartWidget => ({
  id: randomId(),
  type: 'chart',
  title: 'Metric overview',
  x: 0,
  y: 0,
  w: 4,
  h: 4,
  config: {
    metric: 'users',
    range: '30d',
    mode: 'line',
  },
  ...overrides,
});

const createTable = (overrides: Partial<TableWidget> = {}): TableWidget => ({
  id: randomId(),
  type: 'table',
  title: 'Events table',
  x: 4,
  y: 0,
  w: 6,
  h: 6,
  config: {
    filter: '',
    sortBy: 'name',
    sortDir: 'asc',
    page: 0,
    pageSize: 25,
  },
  ...overrides,
});

const createNotes = (overrides: Partial<NotesWidget> = {}): NotesWidget => ({
  id: randomId(),
  type: 'notes',
  title: 'Notes',
  x: 0,
  y: 4,
  w: 3,
  h: 4,
  config: {
    content: 'Capture insights, action items, and runbooks here.',
  },
  ...overrides,
});

const buildDefaultDashboards = (): Dashboard[] => [
  {
    id: randomId(),
    name: 'Product Pulse',
    updatedAt: new Date().toISOString(),
    widgets: [createChart(), createTable(), createNotes()],
  },
  {
    id: randomId(),
    name: 'Marketing Overview',
    updatedAt: new Date().toISOString(),
    widgets: [
      createChart({
        config: { metric: 'revenue', range: '90d', mode: 'bar' },
        x: 0,
        y: 0,
        w: 5,
      }),
      createNotes({
        title: 'Campaign notes',
        x: 5,
        y: 0,
        w: 4,
        h: 3,
      }),
    ],
  },
];

let saveTimer: ReturnType<typeof setTimeout> | null = null;

const triggerSave = (set: any, get: any) => {
  if (saveTimer) clearTimeout(saveTimer);
  set({ saveStatus: 'saving', saveError: undefined });
  saveTimer = setTimeout(() => {
    const fail = Math.random() < 0.1;
    if (fail) {
      set({ saveStatus: 'error', saveError: 'Failed to sync. Retry?' });
      return;
    }
    const now = new Date().toISOString();
    const currentId = get().currentDashboardId;
    if (!currentId) {
      set({ saveStatus: 'saved', saveError: undefined });
      return;
    }
    set((state: WorkspaceState) => ({
      dashboards: state.dashboards.map((d) =>
        d.id === currentId ? { ...d, updatedAt: now } : d,
      ),
      saveStatus: 'saved',
      saveError: undefined,
    }));
  }, 800 + Math.random() * 300);
};

export const useWorkspaceStore = create<WorkspaceState>()(
  persist(
    (set, get) => ({
      dashboards: buildDefaultDashboards(),
      currentDashboardId: undefined,
      saveStatus: 'idle',
      saveError: undefined,
      createDashboard: () => {
        const newDash: Dashboard = {
          id: randomId(),
          name: 'Untitled dashboard',
          updatedAt: new Date().toISOString(),
          widgets: [],
        };
        set((state) => ({
          dashboards: [...state.dashboards, newDash],
          currentDashboardId: newDash.id,
        }));
        triggerSave(set, get);
      },
      selectDashboard: (id) => {
        set({ currentDashboardId: id });
      },
      deleteDashboard: (id) => {
        set((state) => {
          const dashboards = state.dashboards.filter((d) => d.id !== id);
          const currentDashboardId =
            state.currentDashboardId === id ? dashboards[0]?.id : state.currentDashboardId;
          return { dashboards, currentDashboardId };
        });
        triggerSave(set, get);
      },
      renameDashboard: (name) => {
        const currentId = get().currentDashboardId;
        if (!currentId) return;
        set((state) => ({
          dashboards: state.dashboards.map((d) =>
            d.id === currentId ? { ...d, name } : d,
          ),
        }));
        triggerSave(set, get);
      },
      addWidget: (type) => {
        const currentId = get().currentDashboardId;
        if (!currentId) return;
        const builderMap: Record<WidgetType, () => Widget> = {
          chart: () => createChart({ x: 0, y: Infinity }),
          table: () => createTable({ x: 0, y: Infinity }),
          notes: () => createNotes({ x: 0, y: Infinity }),
        };
        const widget = builderMap[type]();
        set((state) => ({
          dashboards: state.dashboards.map((d) =>
            d.id === currentId ? { ...d, widgets: [...d.widgets, widget] } : d,
          ),
        }));
        triggerSave(set, get);
      },
      deleteWidget: (id) => {
        const currentId = get().currentDashboardId;
        if (!currentId) return;
        set((state) => ({
          dashboards: state.dashboards.map((d) =>
            d.id === currentId ? { ...d, widgets: d.widgets.filter((w) => w.id !== id) } : d,
          ),
        }));
        triggerSave(set, get);
      },
      updateWidgetTitle: (id, title) => {
        const currentId = get().currentDashboardId;
        if (!currentId) return;
        set((state) => ({
          dashboards: state.dashboards.map((d) =>
            d.id === currentId
              ? {
                  ...d,
                  widgets: d.widgets.map((w) => (w.id === id ? { ...w, title } : w)),
                }
              : d,
          ),
        }));
        triggerSave(set, get);
      },
      updateWidgetConfig: (id, config) => {
        const currentId = get().currentDashboardId;
        if (!currentId) return;
        set((state) => ({
          dashboards: state.dashboards.map((d) =>
            d.id === currentId
              ? {
                  ...d,
                  widgets: d.widgets.map((w) =>
                    w.id === id ? { ...w, config: { ...w.config, ...config } as any } : w,
                  ),
                }
              : d,
          ),
        }));
        triggerSave(set, get);
      },
      updateNotesContent: (id, content) => {
        get().updateWidgetConfig(id, { content });
      },
      updateLayout: (layout) => {
        const currentId = get().currentDashboardId;
        if (!currentId) return;
        set((state) => ({
          dashboards: state.dashboards.map((d) =>
            d.id === currentId
              ? {
                  ...d,
                  widgets: d.widgets.map((w) => {
                    const entry = layout.find((l) => l.i === w.id);
                    if (!entry) return w;
                    return { ...w, x: entry.x, y: entry.y, w: entry.w, h: entry.h };
                  }),
                }
              : d,
          ),
        }));
        triggerSave(set, get);
      },
      retrySave: () => {
        triggerSave(set, get);
      },
    }),
    {
      name: 'custom-analytics-workspace',
      partialize: (state) => ({
        dashboards: state.dashboards,
        currentDashboardId: state.currentDashboardId ?? state.dashboards[0]?.id,
      }),
      onRehydrateStorage: () => (state) => {
        if (!state?.currentDashboardId && state?.dashboards.length) {
          state.currentDashboardId = state.dashboards[0].id;
        }
      },
    },
  ),
);

export const useCurrentDashboard = () =>
  useWorkspaceStore((state) =>
    state.dashboards.find((d) => d.id === state.currentDashboardId),
  );
