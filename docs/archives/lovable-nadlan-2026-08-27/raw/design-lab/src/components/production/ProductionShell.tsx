import { Link } from "@tanstack/react-router";
import { useEffect, useRef, useState, type ReactNode } from "react";
import { cn } from "@/lib/utils";
import { Action } from "./ui";

export const prodNav: { label: string; to?: string; href?: string }[] = [
  { label: "פרויקטים", to: "/production/nadlan/projects" },
  { label: "נכסים", to: "/production/nadlan/properties" },
  { label: "מחירים ונתונים", href: "#prices" },
  { label: "מפה", href: "#map" },
  { label: "כלים", href: "#tools" },
  { label: "אנשי מקצוע", href: "#pros" },
  { label: "מדריכים", href: "#guides" },
];

export const prodRoutes: { label: string; to: string }[] = [
  { label: "בית המוצר", to: "/production/nadlan" },
  { label: "ארכיון פרויקטים", to: "/production/nadlan/projects" },
  { label: "פרויקט · Rainbow", to: "/production/nadlan/projects/rainbow-tel-aviv" },
  { label: "ארכיון נכסים", to: "/production/nadlan/properties" },
  { label: "נכס לדוגמה · בקעה", to: "/production/nadlan/properties/baka-demo" },
  { label: "פרסום נכס", to: "/production/nadlan/post-listing" },
  { label: "מצגת פגישה", to: "/production/nadlan/meeting" },
];

/* ---------------- internal implementation & SEO drawer ---------------- */

export type Impl = {
  intent: string;
  keywords: { primary: string; secondary: string[] };
  meta: { title: string; description: string; canonical: string };
  schema: string[];
  internalLinks: string[];
  dataPolicy: string[];
  wordpress: string[];
};

export function ImplDrawer({ impl, route }: { impl: Impl; route: string }) {
  const [open, setOpen] = useState(false);
  const panelRef = useRef<HTMLDivElement>(null);
  const buttonRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    if (!open) return;
    panelRef.current?.focus();
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        setOpen(false);
        buttonRef.current?.focus();
      }
    };
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, [open]);

  const groups: { title: string; items: ReactNode[] }[] = [
    { title: "כוונת חיפוש", items: [impl.intent] },
    {
      title: "אשכול מילות מפתח",
      items: [`ראשי: ${impl.keywords.primary}`, ...impl.keywords.secondary.map((k) => `משני: ${k}`)],
    },
    {
      title: "Title / Meta / Canonical",
      items: [
        `Title: ${impl.meta.title}`,
        `Meta: ${impl.meta.description}`,
        `Canonical: ${impl.meta.canonical}`,
      ],
    },
    { title: "Schema", items: impl.schema },
    { title: "קישור פנימי", items: impl.internalLinks },
    { title: "מדיניות מצבי נתונים", items: impl.dataPolicy },
    { title: "מיפוי בלוקים לוורדפרס", items: impl.wordpress },
  ];

  return (
    <>
      <button
        ref={buttonRef}
        type="button"
        onClick={() => setOpen(true)}
        aria-expanded={open}
        aria-controls="impl-drawer"
        className="tap fixed bottom-4 start-4 z-50 inline-flex items-center gap-2 rounded-full border border-border bg-card px-4 py-3 text-xs font-bold text-card-foreground shadow-lg"
      >
        יישום ו‑SEO
      </button>

      {open ? (
        <div className="fixed inset-0 z-50">
          <button
            type="button"
            aria-label="סגירת פאנל היישום"
            onClick={() => setOpen(false)}
            className="absolute inset-0 bg-foreground/50"
          />
          <div
            id="impl-drawer"
            ref={panelRef}
            role="dialog"
            aria-modal="true"
            aria-label="פאנל יישום ו‑SEO — פנימי"
            tabIndex={-1}
            className="absolute inset-y-0 start-0 flex w-full max-w-md flex-col border-e border-border bg-card text-card-foreground shadow-2xl"
          >
            <div className="flex items-start justify-between gap-3 border-b border-border p-4">
              <div className="min-w-0">
                <p className="text-xs font-bold uppercase tracking-wide text-muted-foreground">
                  פנימי בלבד · {route}
                </p>
                <h2 className="display mt-1 text-lg">יישום ו‑SEO</h2>
              </div>
              <button
                type="button"
                onClick={() => setOpen(false)}
                className="tap shrink-0 rounded-md border border-border px-3 py-2 text-sm font-semibold"
              >
                סגירה
              </button>
            </div>
            <div className="flex-1 space-y-5 overflow-y-auto p-4">
              {groups.map((g) => (
                <section key={g.title}>
                  <h3 className="text-sm font-bold">{g.title}</h3>
                  <ul className="mt-2 space-y-2">
                    {g.items.map((item, i) => (
                      <li
                        key={i}
                        className="break-words rounded-md bg-surface p-3 text-xs leading-relaxed text-surface-foreground"
                      >
                        {item}
                      </li>
                    ))}
                  </ul>
                </section>
              ))}
            </div>
          </div>
        </div>
      ) : null}
    </>
  );
}

/* ---------------- product header ---------------- */

export function ProdHeader({
  primaryCta = "מצאו את הצעד הבא",
  secondaryCta = "פרסמו נכס אמיתי",
}: {
  primaryCta?: string;
  secondaryCta?: string;
}) {
  const [open, setOpen] = useState(false);
  const buttonRef = useRef<HTMLButtonElement>(null);
  const panelRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!open) return;
    panelRef.current?.querySelector<HTMLElement>("a, button")?.focus();
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        setOpen(false);
        buttonRef.current?.focus();
      }
    };
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, [open]);

  const itemCls =
    "tap inline-flex items-center whitespace-nowrap rounded-md px-3 py-2 text-sm font-semibold hover:bg-secondary hover:text-secondary-foreground";

  return (
    <header className="sticky top-0 z-30 w-full border-b border-border bg-background/95 backdrop-blur">
      <div className="lab-container flex min-w-0 items-center gap-2 py-3">
        <Link
          to="/production/nadlan"
          className="tap display flex min-w-0 shrink items-center gap-2 truncate text-lg"
        >
          <span
            aria-hidden="true"
            className="inline-block h-5 w-5 shrink-0 rounded-sm bg-primary"
          />
          נדל״ן
        </Link>

        <nav aria-label="ניווט ראשי" className="hidden min-w-0 xl:block">
          <ul className="flex items-center gap-0.5">
            {prodNav.map((item) =>
              item.to ? (
                <li key={item.label}>
                  <Link to={item.to} className={itemCls}>
                    {item.label}
                  </Link>
                </li>
              ) : (
                <li key={item.label}>
                  <a href={item.href} className={itemCls}>
                    {item.label}
                  </a>
                </li>
              ),
            )}
          </ul>
        </nav>

        <div className="ms-auto flex shrink-0 items-center gap-2">
          <Link
            to="/production/nadlan/post-listing"
            className="tap hidden items-center rounded-md px-3 py-2 text-sm font-semibold underline-offset-4 hover:underline lg:inline-flex"
          >
            {secondaryCta}
          </Link>
          <a
            href="#hero-tasks"
            className="tap inline-flex items-center whitespace-nowrap rounded-md bg-primary px-3 py-2 text-sm font-bold text-primary-foreground hover:opacity-90 sm:px-4"
          >
            {primaryCta}
          </a>
          <button
            ref={buttonRef}
            type="button"
            onClick={() => setOpen((v) => !v)}
            aria-expanded={open}
            aria-controls="prod-mobile-menu"
            aria-label={open ? "סגירת תפריט" : "פתיחת תפריט"}
            className="tap inline-flex items-center justify-center rounded-md border border-border px-3 py-2 xl:hidden"
          >
            <span aria-hidden="true" className="text-lg leading-none">
              {open ? "✕" : "☰"}
            </span>
          </button>
        </div>
      </div>

      {open ? (
        <div
          id="prod-mobile-menu"
          ref={panelRef}
          className="border-t border-border bg-card text-card-foreground xl:hidden"
        >
          <nav aria-label="ניווט ראשי במובייל" className="lab-container py-3">
            <ul className="grid gap-1">
              {prodNav.map((item) => (
                <li key={item.label}>
                  {item.to ? (
                    <Link
                      to={item.to}
                      onClick={() => setOpen(false)}
                      className="tap flex items-center rounded-md px-3 py-3 text-base font-semibold hover:bg-secondary"
                    >
                      {item.label}
                    </Link>
                  ) : (
                    <a
                      href={item.href}
                      onClick={() => setOpen(false)}
                      className="tap flex items-center rounded-md px-3 py-3 text-base font-semibold hover:bg-secondary"
                    >
                      {item.label}
                    </a>
                  )}
                </li>
              ))}
              <li className="mt-1 border-t border-border pt-2">
                <Link
                  to="/production/nadlan/post-listing"
                  onClick={() => setOpen(false)}
                  className="tap flex items-center rounded-md px-3 py-3 text-base font-bold underline underline-offset-4"
                >
                  {secondaryCta}
                </Link>
              </li>
            </ul>
          </nav>
        </div>
      ) : null}
    </header>
  );
}

/* ---------------- footer ---------------- */

const footerCols: { title: string; items: string[] }[] = [
  { title: "פרויקטים", items: ["פרויקטים בתל אביב", "פרויקטים חדשים", "יזמים", "התחדשות עירונית"] },
  { title: "נכסים", items: ["דירות למכירה", "דירות להשכרה", "נכסים מסחריים", "פרסום נכס"] },
  { title: "מחירים ונתונים", items: ["מדד מחירי אזור", "עסקאות שבוצעו", "מתודולוגיה ומקורות"] },
  { title: "כלים", items: ["מחשבון מס רכישה", "סימולטור מס רכישה", "מחשבון מס שבח", "נסח טאבו"] },
];

export function ProdFooter() {
  return (
    <footer className="border-t border-border bg-surface py-12 text-surface-foreground">
      <div className="lab-container">
        <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
          {footerCols.map((c) => (
            <nav key={c.title} aria-label={c.title}>
              <h2 className="text-sm font-bold">{c.title}</h2>
              <ul className="mt-3 space-y-2 text-sm text-muted-foreground">
                {c.items.map((i) => (
                  <li key={i}>
                    <a href="#" className="underline-offset-4 hover:underline">
                      {i}
                    </a>
                  </li>
                ))}
              </ul>
            </nav>
          ))}
        </div>
        <p className="mt-10 max-w-3xl text-xs leading-relaxed text-muted-foreground">
          אב טיפוס פנימי. חלק מהמודעות והפרופילים מוצגים כדוגמה להמחשת המוצר ואינם מלאי
          פעיל, לא הצעות אמיתיות ולא נתוני שוק. שדות מקור, תאריך עדכון ואימות מוצגים ריקים
          עד למילוי אמיתי.
        </p>
        <div className="mt-6 flex flex-wrap gap-3">
          <Action variant="copper" to="/production/nadlan/post-listing">
            פרסמו נכס אמיתי חינם
          </Action>
          <Action variant="quiet" to="/production/nadlan/meeting">
            מצגת המוצר לפגישה
          </Action>
        </div>
      </div>
    </footer>
  );
}

/* ---------------- shell ---------------- */

export function ProductionShell({
  route,
  impl,
  children,
  headerPrimaryCta,
}: {
  route: string;
  impl: Impl;
  children: ReactNode;
  headerPrimaryCta?: string;
}) {
  return (
    <div className="theme-prod-nadlan">
      <div className="min-h-screen bg-background text-foreground">
        <div className="w-full border-b border-dashed border-border bg-surface text-surface-foreground">
          <div className="lab-container flex min-w-0 flex-wrap items-center gap-2 py-2">
            <Link
              to="/"
              className="tap inline-flex shrink-0 items-center rounded-md px-2 py-2 text-[0.7rem] font-bold uppercase tracking-wide"
            >
              מעבדה · פנימי
            </Link>
            <nav aria-label="מסלולי חבילת המוצר" className="w-full min-w-0 lg:w-auto lg:flex-1">
              <ul className="no-scrollbar -mx-1 flex snap-x snap-mandatory items-center gap-1 overflow-x-auto px-1 py-1 lg:flex-wrap lg:overflow-visible">
                {prodRoutes.map((r) => (
                  <li key={r.to} className="shrink-0 snap-start">
                    <Link
                      to={r.to}
                      activeOptions={{ exact: true }}
                      activeProps={{
                        className: cn(
                          "tap inline-flex items-center whitespace-nowrap rounded-md px-3 py-2 text-xs font-bold",
                          "bg-primary text-primary-foreground",
                        ),
                        "aria-current": "page",
                      }}
                      inactiveProps={{
                        className:
                          "tap inline-flex items-center whitespace-nowrap rounded-md border border-border bg-card px-3 py-2 text-xs font-semibold text-card-foreground hover:bg-secondary",
                      }}
                    >
                      {r.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </nav>
          </div>
        </div>

        <a
          href="#main"
          className="sr-only focus:not-sr-only focus:absolute focus:z-50 focus:m-2 focus:rounded-md focus:bg-primary focus:px-4 focus:py-2 focus:text-primary-foreground"
        >
          דילוג לתוכן המרכזי
        </a>

        <ProdHeader {...(headerPrimaryCta ? { primaryCta: headerPrimaryCta } : {})} />
        {children}
        <ProdFooter />
        <ImplDrawer impl={impl} route={route} />
      </div>
    </div>
  );
}

