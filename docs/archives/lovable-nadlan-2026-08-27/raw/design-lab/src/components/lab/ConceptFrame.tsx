import type { ReactNode } from "react";
import { ConceptSwitcher } from "./ConceptSwitcher";
import { AnnotationDrawer, type Annotation } from "./AnnotationDrawer";
import { HandoffPanel, type Handoff } from "./HandoffPanel";
import { concepts, type ConceptId } from "@/lib/lab-data";

export function ConceptFrame({
  id,
  annotation,
  handoff,
  children,
}: {
  id: ConceptId;
  annotation: Annotation;
  handoff: Handoff;
  children: ReactNode;
}) {
  const concept = concepts.find((c) => c.id === id)!;
  return (
    <div className={concept.theme}>
      <div className="min-h-screen bg-background text-foreground">
        <ConceptSwitcher current={id} />
        <a
          href="#main"
          className="sr-only focus:not-sr-only focus:absolute focus:z-50 focus:m-2 focus:rounded-md focus:bg-primary focus:px-4 focus:py-2 focus:text-primary-foreground"
        >
          דילוג לתוכן המרכזי
        </a>
        {children}
        <HandoffPanel handoff={handoff} />
        <AnnotationDrawer annotation={annotation} />
      </div>
    </div>
  );
}

