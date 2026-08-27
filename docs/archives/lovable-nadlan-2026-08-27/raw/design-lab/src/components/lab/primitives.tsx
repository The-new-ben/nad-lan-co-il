import { Link } from "@tanstack/react-router";
import { useEffect, useRef, useState, type ReactNode } from "react";
import { cn } from "@/lib/utils";

export function Section({
  id,
  children,
  className,
  tone = "base",
}: {
  id?: string;
  children: ReactNode;
  className?: string;
  tone?: "base" | "surface" | "card";
}) {
  return (
    <section
      id={id}
      className={cn(
        "py-14 md:py-20",
        tone === "surface" && "bg-surface text-surface-foreground",
        tone === "card" && "bg-card text-card-foreground",
        className,
      )}
    >
      <div className="lab-container">{children}</div>
    </section>
  );
}

export function SectionHead({
  eyebrow,
  title,
  lead,
  as: As = "h2",
}: {
  eyebrow?: string;
  title: string;
  lead?: string;
  as?: "h2" | "h3";
}) {
  return (
    <header className="mb-8 max-w-2xl">
      {eyebrow ? (
        <p className="mb-2 text-sm font-semibold tracking-wide text-muted-foreground">
          {eyebrow}
        </p>
      ) : null}
      <As className="display text-2xl leading-tight md:text-3xl">{title}</As>
      {lead ? (
        <p className="mt-3 text-base leading-relaxed text-muted-foreground">{lead}</p>
      ) : null}
    </header>
  );
}

export function Cta({
  children,
  variant = "primary",
  href = "#",
}: {
  children: ReactNode;
  variant?: "primary" | "secondary" | "quiet";
  href?: string;
}) {
  return (
    <a
      href={href}
      className={cn(
        "tap inline-flex items-center justify-center gap-2 rounded-lg px-6 py-3 text-base font-semibold transition-colors",
        variant === "primary" &&
          "bg-primary text-primary-foreground hover:bg-highlight hover:text-highlight-foreground",
        variant === "secondary" &&
          "border-2 border-primary text-primary hover:bg-secondary hover:text-secondary-foreground",
        variant === "quiet" &&
          "border border-border bg-card text-card-foreground hover:bg-secondary",
      )}
    >
      {children}
    </a>
  );
}

export function Breadcrumbs({ trail }: { trail: string[] }) {
  return (
    <nav aria-label="מסלול ניווט" className="text-sm text-muted-foreground">
      <ol className="flex flex-wrap items-center gap-2">
        {trail.map((item, i) => (
          <li key={item} className="flex items-center gap-2">
            {i > 0 ? <span aria-hidden="true">‹</span> : null}
            {i === trail.length - 1 ? (
              <span aria-current="page" className="font-medium text-foreground">
                {item}
              </span>
            ) : (
              <a href="#" className="underline-offset-4 hover:underline">
                {item}
              </a>
            )}
          </li>
        ))}
      </ol>
    </nav>
  );
}

export function SiteHeader({
  brand,
  menu,
  primaryCta,
  secondaryCta,
}: {
  brand: string;
  menu: string[];
  primaryCta: string;
  secondaryCta: string;
}) {
  const [open, setOpen] = useState(false);
  const buttonRef = useRef<HTMLButtonElement>(null);
  const panelRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!open) return;
    const firstLink = panelRef.current?.querySelector<HTMLElement>("a, button");
    firstLink?.focus();
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        setOpen(false);
        buttonRef.current?.focus();
      }
    };
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, [open]);

  return (
    <header className="sticky top-0 z-30 w-full border-b border-border bg-background/95 backdrop-blur">
      <div className="lab-container flex min-w-0 items-center gap-2 py-3">
        <a
          href="#"
          className="tap display flex min-w-0 shrink items-center truncate text-lg font-bold"
        >
          {brand}
        </a>

        <nav aria-label="ניווט ראשי" className="hidden min-w-0 lg:block">
          <ul className="flex flex-wrap items-center gap-1">
            {menu.map((item) => (
              <li key={item}>
                <a
                  href="#"
                  className="tap inline-flex items-center whitespace-nowrap rounded-md px-3 py-2 text-sm font-medium text-foreground hover:bg-secondary hover:text-secondary-foreground"
                >
                  {item}
                </a>
              </li>
            ))}
          </ul>
        </nav>

        <div className="ms-auto flex shrink-0 items-center gap-2">
          <a
            href="#"
            className="tap hidden items-center rounded-lg px-3 py-2 text-sm font-semibold text-foreground underline-offset-4 hover:underline lg:inline-flex"
          >
            {secondaryCta}
          </a>
          <a
            href="#"
            className="tap inline-flex items-center whitespace-nowrap rounded-lg bg-primary px-3 py-2 text-sm font-semibold text-primary-foreground hover:bg-highlight hover:text-highlight-foreground sm:px-4"
          >
            {primaryCta}
          </a>
          <button
            ref={buttonRef}
            type="button"
            onClick={() => setOpen((v) => !v)}
            aria-expanded={open}
            aria-controls="site-mobile-menu"
            aria-label={open ? "סגירת תפריט" : "פתיחת תפריט"}
            className="tap inline-flex items-center justify-center rounded-lg border border-border px-3 py-2 lg:hidden"
          >
            <span aria-hidden="true" className="text-lg leading-none">
              {open ? "✕" : "☰"}
            </span>
          </button>
        </div>
      </div>

      {open ? (
        <div
          id="site-mobile-menu"
          ref={panelRef}
          className="border-t border-border bg-card text-card-foreground lg:hidden"
        >
          <nav aria-label="ניווט ראשי במובייל" className="lab-container py-3">
            <ul className="grid gap-1">
              {menu.map((item) => (
                <li key={item}>
                  <a
                    href="#"
                    onClick={() => setOpen(false)}
                    className="tap flex items-center rounded-md px-3 py-3 text-base font-medium hover:bg-secondary hover:text-secondary-foreground"
                  >
                    {item}
                  </a>
                </li>
              ))}
              <li className="mt-1 border-t border-border pt-2">
                <a
                  href="#"
                  onClick={() => setOpen(false)}
                  className="tap flex items-center rounded-md px-3 py-3 text-base font-semibold underline underline-offset-4"
                >
                  {secondaryCta}
                </a>
              </li>
            </ul>
          </nav>
        </div>
      ) : null}
    </header>
  );
}


export function Card({
  children,
  className,
  as: As = "div",
}: {
  children: ReactNode;
  className?: string;
  as?: "div" | "article" | "li";
}) {
  return (
    <As
      className={cn(
        "rounded-xl border border-border bg-card p-5 text-card-foreground shadow-[0_1px_2px_color-mix(in_oklab,var(--foreground)_8%,transparent)]",
        className,
      )}
    >
      {children}
    </As>
  );
}

export function Tag({ children }: { children: ReactNode }) {
  return (
    <span className="inline-flex items-center rounded-full border border-border bg-secondary px-2.5 py-1 text-xs font-medium text-secondary-foreground">
      {children}
    </span>
  );
}

export function ExampleBadge() {
  return (
    <span className="inline-flex items-center rounded-md bg-accent px-2 py-0.5 text-xs font-bold text-accent-foreground">
      דוגמה
    </span>
  );
}

export function ContextLink({ href, children }: { href: string; children: ReactNode }) {
  return (
    <a
      href={href}
      className="tap inline-flex items-center gap-1 text-sm font-semibold text-primary underline underline-offset-4 hover:text-highlight"
    >
      {children}
      <span aria-hidden="true">←</span>
    </a>
  );
}

export function TrustBlocks({
  reviewer,
  method,
  privacy,
  sourceDate,
  limits,
}: {
  reviewer: string;
  method: string;
  privacy: string;
  sourceDate: string;
  limits: string;
}) {
  const items = [
    { t: "בדיקה מקצועית", d: reviewer },
    { t: "מתודולוגיה", d: method },
    { t: "פרטיות ואבטחה", d: privacy },
    { t: "עדכון מקורות", d: sourceDate },
    { t: "מגבלות ואזהרה", d: limits },
  ];
  return (
    <ul className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {items.map((i) => (
        <Card as="li" key={i.t}>
          <h3 className="text-base font-bold">{i.t}</h3>
          <p className="mt-2 text-sm leading-relaxed text-muted-foreground">{i.d}</p>
        </Card>
      ))}
    </ul>
  );
}

export function BackToLab() {
  return (
    <Link
      to="/"
      className="tap inline-flex items-center gap-2 rounded-lg border border-border px-3 py-2 text-sm font-semibold"
    >
      חזרה למעבדת ההשוואה
    </Link>
  );
}

