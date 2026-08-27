import { createFileRoute, Link } from "@tanstack/react-router";
import { useSuspenseQuery } from "@tanstack/react-query";
import { queryOptions } from "@tanstack/react-query";
import { listHandoffFiles } from "@/lib/handoff.functions";

const filesQuery = queryOptions({
  queryKey: ["handoff", "files"],
  queryFn: () => listHandoffFiles(),
});

export const Route = createFileRoute("/handoff/")({
  loader: ({ context }) => context.queryClient.ensureQueryData(filesQuery),
  component: HandoffIndex,
});

function HandoffIndex() {
  const { data } = useSuspenseQuery(filesQuery);

  return (
    <div className="space-y-8">
      <section className="rounded-lg border border-neutral-200 bg-white p-6">
        <h1 className="text-2xl font-semibold">Premium pattern packet</h1>
        <p className="mt-2 max-w-2xl text-sm text-neutral-600">
          Reference files for the NadLan3D WordPress rebuild. The packet contains
          design specs, HTML/CSS reference renders, copy in HE+EN, JSON contracts,
          and a Codex build plan. The viewer below shows the same files, live.
        </p>
        <div className="mt-5 flex flex-wrap gap-2">
          <Link to="/handoff/compare" className="rounded-sm bg-neutral-900 px-4 py-2 text-sm text-white hover:bg-neutral-800">
            Open Before / After
          </Link>
          <Link to="/handoff/showroom" className="rounded-sm border border-neutral-300 px-4 py-2 text-sm hover:bg-neutral-50">
            Open Showroom reference
          </Link>
        </div>
      </section>

      <Section title="Documents">
        <ul className="grid gap-2 sm:grid-cols-2">
          {data.docs.map((path) => (
            <li key={path}>
              <Link
                to="/handoff/doc/$slug"
                params={{ slug: encodeURIComponent(path) }}
                className="block rounded-sm border border-neutral-200 bg-white px-3 py-2 text-sm hover:border-neutral-400"
              >
                <span className="font-mono text-xs text-neutral-500">md</span>{" "}
                {path}
              </Link>
            </li>
          ))}
        </ul>
      </Section>

      <Section title="Reference renders">
        <ul className="grid gap-2 sm:grid-cols-3">
          {[
            { to: "/handoff/showroom", label: "Showroom" },
            { to: "/handoff/homepage", label: "Homepage" },
            { to: "/handoff/projects", label: "Projects archive" },
          ].map((it) => (
            <li key={it.to}>
              <Link to={it.to} className="block rounded-sm border border-neutral-200 bg-white px-3 py-2 text-sm hover:border-neutral-400">
                {it.label}
              </Link>
            </li>
          ))}
        </ul>
      </Section>

      <Section title="JSON contracts">
        <ul className="grid gap-2 sm:grid-cols-2">
          {data.data.map((path) => (
            <li key={path}>
              <Link
                to="/handoff/doc/$slug"
                params={{ slug: encodeURIComponent(path) }}
                className="block rounded-sm border border-neutral-200 bg-white px-3 py-2 text-sm hover:border-neutral-400"
              >
                <span className="font-mono text-xs text-neutral-500">json</span> {path}
              </Link>
            </li>
          ))}
        </ul>
      </Section>

      <Section title="Concept screenshots">
        <p className="mb-3 text-xs text-neutral-500">
          These are renders of the static reference HTML, not screenshots of nadlan3d.co.il.
        </p>
        <ul className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-5">
          {data.screenshots.map((path) => (
            <li key={path} className="overflow-hidden rounded-sm border border-neutral-200 bg-white">
              <img
                src={`/handoff-file/${encodeURIComponent(path)}`}
                alt={path}
                loading="lazy"
                className="block h-32 w-full object-cover"
              />
              <div className="border-t border-neutral-200 px-2 py-1 font-mono text-[10px] text-neutral-500">
                {path.replace("screenshots/", "")}
              </div>
            </li>
          ))}
        </ul>
      </Section>
    </div>
  );
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section>
      <h2 className="mb-3 text-xs font-semibold uppercase tracking-wider text-neutral-500">{title}</h2>
      {children}
    </section>
  );
}

