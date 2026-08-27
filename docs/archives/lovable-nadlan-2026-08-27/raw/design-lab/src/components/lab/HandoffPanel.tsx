import { Card } from "./primitives";

export type Handoff = {
  tokens: { name: string; value: string; usage: string }[];
  blocks: { name: string; desc: string }[];
  menu: { label: string; children: string[] }[];
  schema: string[];
  performance: string[];
};

export function HandoffPanel({ handoff }: { handoff: Handoff }) {
  return (
    <section
      id="wordpress-handoff"
      aria-label="פאנל מסירה לוורדפרס — פנימי"
      className="border-t-4 border-dashed border-ring bg-surface py-12 text-surface-foreground"
    >
      <div className="lab-container">
        <p className="text-xs font-bold uppercase tracking-wide text-muted-foreground">
          פנימי · אפיון מסירה, לא חלק מהאתר החי
        </p>
        <h2 className="display mt-1 text-2xl">מסירה לוורדפרס</h2>

        <div className="mt-8 grid gap-6 lg:grid-cols-2">
          <Card>
            <h3 className="text-base font-bold">טוקנים לעיצוב (theme.json)</h3>
            <div className="mt-3 overflow-x-auto">
              <table className="w-full text-start text-sm">
                <thead>
                  <tr className="border-b border-border text-muted-foreground">
                    <th scope="col" className="py-2 text-start font-semibold">
                      טוקן
                    </th>
                    <th scope="col" className="py-2 text-start font-semibold">
                      ערך
                    </th>
                    <th scope="col" className="py-2 text-start font-semibold">
                      שימוש
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {handoff.tokens.map((t) => (
                    <tr key={t.name} className="border-b border-border/60 align-top">
                      <td className="py-2 font-mono text-xs">{t.name}</td>
                      <td className="py-2 font-mono text-xs">{t.value}</td>
                      <td className="py-2 text-muted-foreground">{t.usage}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Card>

          <Card>
            <h3 className="text-base font-bold">בלוקים לשימוש חוזר</h3>
            <ul className="mt-3 space-y-2 text-sm">
              {handoff.blocks.map((b) => (
                <li key={b.name}>
                  <span className="font-semibold">{b.name}</span>
                  <span className="text-muted-foreground"> — {b.desc}</span>
                </li>
              ))}
            </ul>
          </Card>

          <Card>
            <h3 className="text-base font-bold">מבנה תפריט (WP Menus)</h3>
            <ul className="mt-3 space-y-3 text-sm">
              {handoff.menu.map((m) => (
                <li key={m.label}>
                  <span className="font-semibold">{m.label}</span>
                  <ul className="mt-1 ms-4 list-disc space-y-1 text-muted-foreground">
                    {m.children.map((c) => (
                      <li key={c}>{c}</li>
                    ))}
                  </ul>
                </li>
              ))}
            </ul>
          </Card>

          <div className="grid gap-6">
            <Card>
              <h3 className="text-base font-bold">Schema מומלץ</h3>
              <ul className="mt-3 list-disc space-y-1 ms-4 text-sm text-muted-foreground">
                {handoff.schema.map((s) => (
                  <li key={s}>{s}</li>
                ))}
              </ul>
            </Card>
            <Card>
              <h3 className="text-base font-bold">כללי ביצועים</h3>
              <ul className="mt-3 list-disc space-y-1 ms-4 text-sm text-muted-foreground">
                {handoff.performance.map((p) => (
                  <li key={p}>{p}</li>
                ))}
              </ul>
            </Card>
          </div>
        </div>
      </div>
    </section>
  );
}

