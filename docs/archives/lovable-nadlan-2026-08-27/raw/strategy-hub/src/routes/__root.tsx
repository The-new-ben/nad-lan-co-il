import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import {
  Outlet,
  Link,
  createRootRouteWithContext,
  useRouter,
  HeadContent,
  Scripts,
} from "@tanstack/react-router";
import { DirectionProvider } from "@radix-ui/react-direction";
import { useEffect, type ReactNode } from "react";

import appCss from "../styles.css?url";
import { reportLovableError } from "../lib/lovable-error-reporting";
import { LangProvider, useLang } from "@/lib/lang-context";
import { SiteHeader } from "@/components/shell/SiteHeader";
import { SiteFooter } from "@/components/shell/SiteFooter";

function NotFoundComponent() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-paper px-4">
      <div className="max-w-md text-center">
        <p className="kicker">404</p>
        <h1 className="mt-3">הדף לא נמצא</h1>
        <div className="mt-6">
          <Link to="/" className="btn-terracotta hover:btn-terracotta-hover inline-block">
            חזרה לעמוד הבית
          </Link>
        </div>
      </div>
    </div>
  );
}

function ErrorComponent({ error, reset }: { error: Error; reset: () => void }) {
  console.error(error);
  const router = useRouter();
  useEffect(() => {
    reportLovableError(error, { boundary: "tanstack_root_error_component" });
  }, [error]);

  return (
    <div className="flex min-h-screen items-center justify-center bg-paper px-4">
      <div className="max-w-md text-center">
        <h1>הדף הזה לא נטען</h1>
        <div className="mt-6 flex justify-center gap-2">
          <button
            onClick={() => { router.invalidate(); reset(); }}
            className="btn-terracotta hover:btn-terracotta-hover"
          >
            ניסיון נוסף
          </button>
          <a href="/" className="btn-gold-outline">חזרה לעמוד הבית</a>
        </div>
      </div>
    </div>
  );
}

export const Route = createRootRouteWithContext<{ queryClient: QueryClient }>()({
  head: () => ({
    meta: [
      { charSet: "utf-8" },
      { name: "viewport", content: "width=device-width, initial-scale=1" },
      { title: "נדל״ן — מוצאים דירה, בודקים מחיר, מכירים את הסביבה" },
      { name: "description", content: "פלטפורמת הנדל״ן הישראלית שבה כל פרויקט הוא מודל תלת־ממדי חי: קומות, דירות, שמש ונוף מהחלון — לפני שחותמים." },
      { name: "author", content: "NadLan" },
      { property: "og:site_name", content: "NadLan" },
      { property: "og:title", content: "נדל״ן — מוצאים דירה, בודקים מחיר, מכירים את הסביבה" },
      { property: "og:description", content: "כל פרויקט הוא מודל תלת־ממדי חי. קונים דירה בעיניים פקוחות." },
      { property: "og:type", content: "website" },
      { property: "og:locale", content: "he_IL" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
    links: [
      { rel: "stylesheet", href: appCss },
      { rel: "preconnect", href: "https://fonts.googleapis.com" },
      { rel: "preconnect", href: "https://fonts.gstatic.com", crossOrigin: "anonymous" },
      {
        rel: "stylesheet",
        href: "https://fonts.googleapis.com/css2?family=Frank+Ruhl+Libre:wght@500;600;700;800&family=Heebo:wght@400;500;600;700&display=swap",
      },
    ],
    scripts: [
      {
        type: "application/ld+json",
        children: JSON.stringify({
          "@context": "https://schema.org",
          "@type": "Organization",
          name: "NadLan",
          url: "/",
        }),
      },
    ],
  }),
  shellComponent: RootShell,
  component: RootComponent,
  notFoundComponent: NotFoundComponent,
  errorComponent: ErrorComponent,
});

function RootShell({ children }: { children: ReactNode }) {
  return (
    <html lang="he" dir="rtl">
      <head>
        <HeadContent />
      </head>
      <body>
        {children}
        <Scripts />
      </body>
    </html>
  );
}

function RootComponent() {
  const { queryClient } = Route.useRouteContext();

  return (
    <QueryClientProvider client={queryClient}>
      <LangProvider>
        <DirectedLayout />
      </LangProvider>
    </QueryClientProvider>
  );
}

function DirectedLayout() {
  const { dir } = useLang();
  return (
    <DirectionProvider dir={dir}>
      <div className="flex min-h-screen flex-col">
        <SiteHeader />
        <main className="flex-1">
          <Outlet />
        </main>
        <SiteFooter />
      </div>
    </DirectionProvider>
  );
}

