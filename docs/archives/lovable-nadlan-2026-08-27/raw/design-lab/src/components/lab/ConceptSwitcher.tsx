import { useEffect, useRef } from "react";
import { Link } from "@tanstack/react-router";
import { concepts, type ConceptId } from "@/lib/lab-data";

export function ConceptSwitcher({ current }: { current: ConceptId }) {
  const railRef = useRef<HTMLUListElement>(null);
  const activeRef = useRef<HTMLAnchorElement>(null);

  useEffect(() => {
    const rail = railRef.current;
    const item = activeRef.current;
    if (!rail || !item) return;
    rail.scrollLeft =
      item.offsetLeft - rail.clientWidth / 2 + item.clientWidth / 2;
  }, [current]);

  return (
    <div className="sticky top-0 z-40 w-full border-b-2 border-dashed border-ring bg-surface text-surface-foreground">
      <div className="lab-container flex min-w-0 flex-wrap items-center gap-2 py-2">
        <Link
          to="/"
          className="tap inline-flex shrink-0 items-center rounded-md px-2 py-2 text-xs font-bold uppercase tracking-wide"
        >
          מעבדת עיצוב · פנימי
        </Link>
        <nav
          aria-label="מעבר בין קונספטים"
          className="w-full min-w-0 lg:w-auto lg:flex-1"
        >
          <ul
            ref={railRef}
            className="no-scrollbar flex snap-x snap-mandatory items-center gap-1 overflow-x-auto scroll-smooth px-1 py-1 lg:flex-wrap lg:overflow-visible"
          >
            {concepts.map((c) => {
              const active = c.id === current;
              return (
                <li key={c.id} className="shrink-0 snap-center">
                  <Link
                    to={c.path}
                    ref={active ? activeRef : undefined}
                    aria-current={active ? "page" : undefined}
                    className={
                      "tap inline-flex items-center whitespace-nowrap rounded-md px-3 py-2 text-xs font-semibold " +
                      (active
                        ? "bg-primary text-primary-foreground ring-2 ring-ring ring-offset-1 ring-offset-surface"
                        : "border border-border bg-card text-card-foreground hover:bg-secondary")
                    }
                  >
                    {c.code} · {c.name}
                  </Link>
                </li>
              );
            })}
          </ul>
        </nav>
      </div>
    </div>
  );
}

