import { createFileRoute, Link } from "@tanstack/react-router";
import { useSuspenseQuery, queryOptions } from "@tanstack/react-query";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { readHandoffFile } from "@/lib/handoff.functions";

export const Route = createFileRoute("/handoff/doc/$slug")({
  loader: ({ context, params }) => {
    const path = decodeURIComponent(params.slug);
    return context.queryClient.ensureQueryData(fileQuery(path));
  },
  notFoundComponent: () => (
    <div className="rounded-lg border border-red-300 bg-red-50 p-4 text-sm text-red-800">
      File not found.{" "}
      <Link to="/handoff" className="underline">Back to index</Link>
    </div>
  ),
  errorComponent: ({ error, reset }) => (
    <div className="rounded-lg border border-red-300 bg-red-50 p-4 text-sm text-red-800">
      <p>Couldn't load file.</p>
      <pre className="mt-2 text-xs">{error.message}</pre>
      <button onClick={reset} className="mt-3 rounded-sm border border-red-400 px-3 py-1">Retry</button>
    </div>
  ),
  component: DocPage,
});

function fileQuery(path: string) {
  return queryOptions({
    queryKey: ["handoff", "file", path],
    queryFn: () => readHandoffFile({ data: { path } }),
  });
}

function DocPage() {
  const { slug } = Route.useParams();
  const path = decodeURIComponent(slug);
  const { data } = useSuspenseQuery(fileQuery(path));
  const isMarkdown = path.endsWith(".md");
  const isJson = path.endsWith(".json");

  return (
    <article className="space-y-4">
      <header className="flex items-center justify-between rounded-lg border border-neutral-200 bg-white p-4">
        <div>
          <h1 className="text-lg font-semibold">{path.split("/").pop()}</h1>
          <p className="font-mono text-xs text-neutral-500">{path}</p>
        </div>
        <Link to="/handoff" className="text-xs underline">← Index</Link>
      </header>

      <div className="rounded-lg border border-neutral-200 bg-white p-6">
        {isMarkdown ? (
          <div className="prose prose-sm max-w-none prose-headings:font-semibold prose-pre:bg-neutral-900 prose-pre:text-neutral-100">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>{data.content}</ReactMarkdown>
          </div>
        ) : isJson ? (
          <pre className="overflow-auto rounded-sm bg-neutral-900 p-4 text-xs text-neutral-100">
            {JSON.stringify(JSON.parse(data.content), null, 2)}
          </pre>
        ) : (
          <pre className="overflow-auto rounded-sm bg-neutral-900 p-4 text-xs text-neutral-100">
            {data.content}
          </pre>
        )}
      </div>
    </article>
  );
}

