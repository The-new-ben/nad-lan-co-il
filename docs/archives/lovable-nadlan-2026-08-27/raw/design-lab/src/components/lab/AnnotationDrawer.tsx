import { useEffect, useRef, useState } from "react";

export type Annotation = {
  seoIntent: string[];
  keywordOwner: string[];
  menuLogic: string[];
  conversionLogic: string[];
};

export function AnnotationDrawer({ annotation }: { annotation: Annotation }) {
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

  const groups: { title: string; items: string[] }[] = [
    { title: "כוונת SEO", items: annotation.seoIntent },
    { title: "בעלות על מילות מפתח", items: annotation.keywordOwner },
    { title: "היגיון התפריט", items: annotation.menuLogic },
    { title: "היגיון ההמרה", items: annotation.conversionLogic },
  ];

  return (
    <>
      <button
        ref={buttonRef}
        type="button"
        onClick={() => setOpen(true)}
        aria-expanded={open}
        aria-controls="annotation-drawer"
        className="tap fixed bottom-4 start-4 z-50 inline-flex items-center gap-2 rounded-full border-2 border-dashed border-ring bg-card px-4 py-3 text-sm font-bold text-card-foreground shadow-lg"
      >
        הערות פנימיות
      </button>

      {open ? (
        <div className="fixed inset-0 z-50">
          <button
            type="button"
            aria-label="סגירת חלונית ההערות"
            onClick={() => setOpen(false)}
            className="absolute inset-0 bg-foreground/50"
          />
          <div
            id="annotation-drawer"
            ref={panelRef}
            role="dialog"
            aria-modal="true"
            aria-label="הערות פנימיות — לא לפרסום"
            tabIndex={-1}
            className="absolute inset-y-0 start-0 flex w-full max-w-md flex-col border-e-4 border-dashed border-ring bg-card text-card-foreground shadow-2xl"
          >
            <div className="flex items-start justify-between gap-3 border-b border-border p-4">
              <div>
                <p className="text-xs font-bold uppercase tracking-wide text-muted-foreground">
                  פנימי בלבד · לא מוצג למשתמשי הקצה
                </p>
                <h2 className="display mt-1 text-lg">הערות תכנון ואסטרטגיה</h2>
              </div>
              <button
                type="button"
                onClick={() => setOpen(false)}
                className="tap rounded-lg border border-border px-3 py-2 text-sm font-semibold"
              >
                סגירה
              </button>
            </div>
            <div className="flex-1 space-y-6 overflow-y-auto p-4">
              {groups
                .filter((g) => g.title)
                .map((g) => (
                  <section key={g.title}>
                    <h3 className="text-sm font-bold text-foreground">{g.title}</h3>
                    <ul className="mt-2 space-y-2">
                      {g.items.map((item) => (
                        <li
                          key={item}
                          className="rounded-md bg-surface p-3 text-sm leading-relaxed text-surface-foreground"
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

