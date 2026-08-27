import { createFileRoute, Outlet, Link } from "@tanstack/react-router";

export const Route = createFileRoute("/handoff")({
  head: () => ({
    meta: [
      { title: "NadLan3D Handoff Viewer" },
      { name: "robots", content: "noindex,nofollow" },
    ],
  }),
  component: HandoffLayout,
});

function HandoffLayout() {
  return (
    <div dir="ltr" className="min-h-screen bg-neutral-50 text-neutral-900">
      <header className="sticky top-0 z-20 border-b border-neutral-200 bg-white">
        <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-3">
          <Link to="/handoff" className="text-sm font-semibold tracking-tight">
            NadLan3D · Handoff Viewer
          </Link>
          <nav className="flex flex-wrap gap-1 text-xs">
            <NavLink to="/handoff">Overview</NavLink>
            <NavLink to="/handoff/compare">Before / After</NavLink>
            <NavLink to="/handoff/showroom">Showroom</NavLink>
            <NavLink to="/handoff/homepage">Homepage</NavLink>
            <NavLink to="/handoff/projects">Projects</NavLink>
          </nav>
        </div>
      </header>
      <main className="mx-auto max-w-7xl px-4 py-6">
        <Outlet />
      </main>
      <footer className="mx-auto max-w-7xl px-4 py-10 text-xs text-neutral-500">
        Files live at <code>handoff/lovable/2026-06-24-premium-pattern/</code> in this repo.
        This viewer is read-only and does not affect nadlan3d.co.il.
      </footer>
    </div>
  );
}

function NavLink({ to, children }: { to: string; children: React.ReactNode }) {
  return (
    <Link
      to={to}
      className="rounded-sm border border-transparent px-3 py-1.5 hover:border-neutral-300 hover:bg-neutral-50"
      activeProps={{ className: "rounded-sm border border-neutral-900 bg-neutral-900 px-3 py-1.5 text-white" }}
      activeOptions={{ exact: to === "/handoff" }}
    >
      {children}
    </Link>
  );
}

