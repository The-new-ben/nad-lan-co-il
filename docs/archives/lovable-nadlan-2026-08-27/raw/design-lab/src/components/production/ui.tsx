import { Link } from "@tanstack/react-router";
import { useState, type ReactNode } from "react";
import { cn } from "@/lib/utils";

/* ---------- layout primitives ---------- */

export function Band({
  id,
  children,
  tone = "base",
  className,
  labelledBy,
}: {
  id?: string;
  children: ReactNode;
  tone?: "base" | "surface" | "card" | "ink";
  className?: string;
  labelledBy?: string;
}) {
  return (
    <section
      id={id}
      aria-labelledby={labelledBy}
      className={cn(
        "py-12 md:py-16",
        tone === "surface" && "bg-surface text-surface-foreground",
        tone === "card" && "bg-card text-card-foreground",
        tone === "ink" && "bg-foreground text-background",
        className,
      )}
    >
      <div className="lab-container min-w-0">{children}</div>
    </section>
  );
}

export function BandHead({
  eyebrow,
  title,
  lead,
  id,
  as: As = "h2",
}: {
  eyebrow?: string;
  title: string;
  lead?: string;
  id?: string;
  as?: "h2" | "h3";
}) {
  return (
    <header className="mb-7 max-w-3xl">
      {eyebrow ? (
        <p className="mb-2 text-xs font-bold uppercase tracking-[0.14em] text-muted-foreground">
          {eyebrow}
        </p>
      ) : null}
      <As id={id} className="display text-2xl leading-tight md:text-[2rem]">
        {title}
      </As>
      {lead ? (
        <p className="mt-3 text-base leading-relaxed text-muted-foreground">{lead}</p>
      ) : null}
    </header>
  );
}

export function Panel({
  children,
  className,
  as: As = "div",
}: {
  children: ReactNode;
  className?: string;
  as?: "div" | "article" | "li" | "form";
}) {
  return (
    <As
      className={cn(
        "rounded-lg border border-border bg-card p-5 text-card-foreground",
        className,
      )}
    >
      {children}
    </As>
  );
}

export function Action({
  children,
  variant = "primary",
  href = "#",
  to,
  className,
}: {
  children: ReactNode;
  variant?: "primary" | "secondary" | "copper" | "quiet";
  href?: string | undefined;
  to?: string | undefined;
  className?: string | undefined;
}) {
  const cls = cn(
    "tap inline-flex items-center justify-center gap-2 rounded-md px-5 py-3 text-sm font-bold transition-colors md:text-base",
    variant === "primary" && "bg-primary text-primary-foreground hover:opacity-90",
    variant === "copper" &&
      "bg-highlight text-highlight-foreground hover:opacity-90",
    variant === "secondary" &&
      "border-2 border-primary text-primary hover:bg-secondary",
    variant === "quiet" &&
      "border border-border bg-card text-card-foreground hover:bg-secondary",
    className,
  );
  if (to) {
    return (
      <Link to={to} className={cls}>
        {children}
      </Link>
    );
  }
  return (
    <a href={href} className={cls}>
      {children}
    </a>
  );
}

export function InlineLink({
  children,
  href = "#",
  to,
}: {
  children: ReactNode;
  href?: string | undefined;
  to?: string | undefined;
}) {
  const cls =
    "tap inline-flex items-center gap-1 text-sm font-bold text-primary underline underline-offset-4 hover:text-highlight";
  if (to)
    return (
      <Link to={to} className={cls}>
        {children}
        <span aria-hidden="true">←</span>
      </Link>
    );
  return (
    <a href={href} className={cls}>
      {children}
      <span aria-hidden="true">←</span>
    </a>
  );
}

export function Chip({ children, tone = "neutral" }: { children: ReactNode; tone?: "neutral" | "copper" | "ink" }) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full px-2.5 py-1 text-xs font-semibold",
        tone === "neutral" && "border border-border bg-secondary text-secondary-foreground",
        tone === "copper" && "bg-accent text-accent-foreground",
        tone === "ink" && "bg-foreground text-background",
      )}
    >
      {children}
    </span>
  );
}

/* ---------- data honesty ---------- */

export function DemoBadge({ label = "דוגמה להמחשת המוצר" }: { label?: string }) {
  return (
    <span className="inline-flex items-center gap-1.5 rounded-md border border-accent bg-accent px-2 py-1 text-xs font-semibold text-accent-foreground">
      <span aria-hidden="true">◐</span>
      {label}
    </span>
  );
}

export function SourceStamp({
  source = "מקור: מיקום לשיבוץ — טרם מולא",
  updated = "עודכן: מיקום לשיבוץ — טרם מולא",
  verification = "אימות: ממתין לבדיקה",
}: {
  source?: string;
  updated?: string;
  verification?: string;
}) {
  return (
    <dl className="mt-3 grid gap-1 text-xs text-muted-foreground sm:grid-cols-3">
      <div>
        <dt className="sr-only">מקור</dt>
        <dd>{source}</dd>
      </div>
      <div>
        <dt className="sr-only">תאריך עדכון</dt>
        <dd>{updated}</dd>
      </div>
      <div>
        <dt className="sr-only">סטטוס אימות</dt>
        <dd>{verification}</dd>
      </div>
    </dl>
  );
}

export type DataState = "demo" | "empty" | "live";

export const dataStateLabels: Record<DataState, string> = {
  demo: "דמו",
  empty: "אין עדיין נתונים",
  live: "נתונים אמיתיים",
};

export function DataStateSwitch({
  value,
  onChange,
  label = "מצב נתונים לתצוגה",
}: {
  value: DataState;
  onChange: (v: DataState) => void;
  label?: string;
}) {
  const states: DataState[] = ["demo", "empty", "live"];
  return (
    <div className="flex min-w-0 flex-wrap items-center gap-2">
      <span className="text-xs font-bold uppercase tracking-wide text-muted-foreground">
        {label}
      </span>
      <div role="group" aria-label={label} className="flex flex-wrap gap-1">
        {states.map((s) => (
          <button
            key={s}
            type="button"
            onClick={() => onChange(s)}
            aria-pressed={value === s}
            className={cn(
              "tap rounded-md px-3 py-2 text-xs font-bold",
              value === s
                ? "bg-primary text-primary-foreground"
                : "border border-border bg-card text-card-foreground hover:bg-secondary",
            )}
          >
            {dataStateLabels[s]}
          </button>
        ))}
      </div>
    </div>
  );
}

export function EmptyState({
  title,
  body,
  ctaLabel,
}: {
  title: string;
  body: string;
  ctaLabel: string;
}) {
  return (
    <Panel className="border-dashed text-center">
      <h3 className="display text-lg">{title}</h3>
      <p className="mx-auto mt-2 max-w-xl text-sm text-muted-foreground">{body}</p>
      <div className="mt-5 flex justify-center">
        <Action variant="copper" to="/production/nadlan/post-listing">
          {ctaLabel}
        </Action>
      </div>
    </Panel>
  );
}

export function LiveState({ title, body }: { title: string; body: string }) {
  return (
    <Panel className="border-dashed">
      <h3 className="display text-lg">{title}</h3>
      <p className="mt-2 text-sm text-muted-foreground">{body}</p>
      <SourceStamp />
    </Panel>
  );
}

/* ---------- misc display ---------- */

export function Crumbs({
  trail,
}: {
  trail: { label: string; to?: string | undefined }[];
}) {
  return (
    <nav aria-label="מסלול ניווט" className="text-xs text-muted-foreground">
      <ol className="flex flex-wrap items-center gap-2">
        {trail.map((item, i) => (
          <li key={item.label} className="flex items-center gap-2">
            {i > 0 ? <span aria-hidden="true">‹</span> : null}
            {i === trail.length - 1 || !item.to ? (
              <span aria-current="page" className="font-semibold text-foreground">
                {item.label}
              </span>
            ) : (
              <Link to={item.to} className="underline-offset-4 hover:underline">
                {item.label}
              </Link>
            )}
          </li>
        ))}
      </ol>
    </nav>
  );
}

export function FaqList({ items }: { items: { q: string; a: string }[] }) {
  return (
    <div className="grid gap-3">
      {items.map((f) => (
        <details
          key={f.q}
          className="rounded-lg border border-border bg-card p-4 text-card-foreground"
        >
          <summary className="tap flex cursor-pointer list-none items-center justify-between gap-3 text-base font-bold">
            {f.q}
            <span aria-hidden="true" className="text-primary">
              +
            </span>
          </summary>
          <p className="mt-3 text-sm leading-relaxed text-muted-foreground">{f.a}</p>
        </details>
      ))}
    </div>
  );
}

export function KeyValueGrid({ rows }: { rows: { k: string; v: string }[] }) {
  return (
    <dl className="grid gap-x-6 gap-y-3 sm:grid-cols-2">
      {rows.map((r) => (
        <div key={r.k} className="border-b border-border pb-2">
          <dt className="text-xs font-semibold uppercase tracking-wide text-muted-foreground">
            {r.k}
          </dt>
          <dd className="mt-1 text-sm font-semibold">{r.v}</dd>
        </div>
      ))}
    </dl>
  );
}

export function MediaFrame({
  label,
  ratio = "16 / 9",
  note,
}: {
  label: string;
  ratio?: string;
  note?: string | undefined;
}) {
  return (
    <figure className="min-w-0">
      <div
        style={{ aspectRatio: ratio }}
        className="flex w-full items-center justify-center rounded-lg border border-dashed border-border bg-secondary text-center"
      >
        <span className="px-4 text-sm font-semibold text-muted-foreground">{label}</span>
      </div>
      {note ? (
        <figcaption className="mt-2 text-xs text-muted-foreground">{note}</figcaption>
      ) : null}
    </figure>
  );
}

export function Tabs({
  items,
  ariaLabel,
}: {
  items: { id: string; label: string; content: ReactNode }[];
  ariaLabel: string;
}) {
  const [active, setActive] = useState(items[0]!.id);
  const current = items.find((i) => i.id === active)!;
  return (
    <div className="min-w-0">
      <div
        role="tablist"
        aria-label={ariaLabel}
        className="no-scrollbar -mx-1 flex snap-x snap-mandatory gap-2 overflow-x-auto px-1 pb-1"
      >
        {items.map((i) => (
          <button
            key={i.id}
            type="button"
            role="tab"
            id={`tab-${i.id}`}
            aria-selected={active === i.id}
            aria-controls={`panel-${i.id}`}
            onClick={() => setActive(i.id)}
            className={cn(
              "tap shrink-0 snap-start whitespace-nowrap rounded-md px-4 py-2.5 text-sm font-bold",
              active === i.id
                ? "bg-primary text-primary-foreground"
                : "border border-border bg-card text-card-foreground hover:bg-secondary",
            )}
          >
            {i.label}
          </button>
        ))}
      </div>
      <div
        id={`panel-${current.id}`}
        role="tabpanel"
        aria-labelledby={`tab-${current.id}`}
        className="mt-5 min-w-0"
      >
        {current.content}
      </div>
    </div>
  );
}

