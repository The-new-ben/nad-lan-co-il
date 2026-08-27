// Real Hebrew + English copy for NadLan sections.
// Every string here is the final production text. No lorem, no placeholders.

export const HE = {
  brand: "נדל״ן",
  tagline: "מוצאים דירה. בודקים מחיר. מכירים את הסביבה.",

  nav: {
    projects: "פרויקטים חדשים",
    listings: "דירות",
    professionals: "אנשי מקצוע",
    urbanRenewal: "התחדשות עירונית",
    rentals: "ניהול השכרות",
    guides: "מדריכים",
  },

  footer: {
    product: "מוצר",
    solutions: "פתרונות",
    tools: "כלים",
    company: "חברה",
    calculators: "מחשבונים",
    glossary: "מילון מונחים",
    about: "אודות",
    contact: "צור קשר",
    myRenewal: "חדר התחדשות",
    myRentals: "ניהול השכרות",
    guides: "מדריכים",
    disclaim: "המידע באתר אינו מהווה ייעוץ משפטי, מימוני או מקצועי. תכניות והדמיות מסומנות בבירור.",
    rights: "© 2026 נדל״ן",
  },

  hero: {
    kicker: "נדל״ן / ישראל / 2026",
    title: "מוצאים דירה, בודקים מחיר, מכירים את הסביבה — לפני שחותמים",
    sub: "כל פרויקט באתר הוא מודל תלת־ממדי חי: קומות, דירות, שמש ונוף מהחלון.",
    tabs: ["קנייה", "השכרה", "פרויקטים", "אנשי מקצוע"],
    placeholder: "עיר, שכונה או פרויקט",
    search: "חיפוש",
    trust: "197 פרויקטים · 938 מתחמי התחדשות · 5 מחשבונים",
  },

  theater: {
    kicker: "הבמה המרכזית",
    title: "בחרו דירה מתוך הבניין, בתלת־ממד",
    stageLabel: "המודל התלת־ממדי האמיתי של הפרויקט",
    honest:
      "פרויקטים אמיתיים שהפכנו למודלים חיים כהדגמת יכולת — היזמים המוצגים אינם לקוחות שלנו.",
    developerCta: "יזמים: רוצים את הבניין שלכם על הבמה?",
    projects: [
      {
        id: "keshet-holon",
        name: "קשת חולון",
        detail: "118 דירות · 12 קומות",
        city: "חולון",
      },
      {
        id: "duo-ramat-gan",
        name: "DUO רמת גן",
        detail: "2 מגדלים · 340 דירות",
        city: "רמת גן",
      },
      {
        id: "rainbow-beer-yaakov",
        name: "רינבו באר יעקב",
        detail: "240 דירות · פארק פרטי",
        city: "באר יעקב",
      },
      {
        id: "sde-dov",
        name: "שדה דב תל אביב",
        detail: "שכונה חדשה · חזית לים",
        city: "תל אביב",
      },
    ],
  },

  map: {
    kicker: "מפה חיה",
    title: "מפת הפרויקטים החיה",
    sub: "התקרבו לעיר ובחרו פרויקט",
    cities: [
      { name: "תל אביב", count: 43 },
      { name: "רמת גן", count: 22 },
      { name: "ירושלים", count: 28 },
      { name: "חיפה", count: 19 },
      { name: "באר שבע", count: 14 },
      { name: "נתניה", count: 17 },
      { name: "ראשון לציון", count: 21 },
      { name: "חולון", count: 12 },
    ],
  },

  rentals: {
    kicker: "ניהול השכרות · חינם",
    title: "כל הדירות המושכרות שלכם: על המפה ובתוך הבניין",
    sub: "פורטפוליו אחד, שלוש נקודות מבט — מפה, בניין, דירה.",
    steps: [
      { n: "01", title: "מוסיפים נכס", body: "כתובת, קומה, שכר דירה, חוזה." },
      { n: "02", title: "מסמנים דירות על המודל", body: "הבניין נטען אוטומטית. אתם מסמנים איזו דירה שלכם." },
      { n: "03", title: "רואים הכל בצבע אחד", body: "חוזה, בטוחות, תיקונים ותזכורות בלוח אחד." },
    ],
    cta: "מתחילים לנהל, חינם",
    note: "מעקב ותזכורות, לא סליקה.",
  },

  renewal: {
    kicker: "התחדשות עירונית",
    title: "חדר הפרויקט של הבניין שלכם",
    sub: "מודל תלת־ממדי של הבניין, מעקב הסכמות דיירים ותיק מסמכים אחד.",
    steps: [
      { n: "01", title: "בודקים את הבניין", body: "כדאיות ראשונית בחינם — לפי גוש/חלקה." },
      { n: "02", title: "פותחים חדר", body: "מודל תלת־ממדי, טבלת דיירים, מסמכים." },
      { n: "03", title: "מזמינים את השכנים", body: "כל דייר רואה את הדירה שלו, מסמן הסכמה." },
    ],
    ctaCheck: "בדיקת כדאיות חינם",
    ctaDemo: "הדגמה חיה",
  },

  listings: {
    kicker: "דירות למכירה",
    title: "דירות נבחרות מהשבוע",
    sub: "לחצו על דירה כדי להיכנס לבניין.",
    items: [
      {
        id: "tlv-lev",
        title: "דירת 3 חדרים משופצת, לב תל אביב",
        price: "₪3,690,000",
        area: "78 מ״ר · קומה 2",
        city: "תל אביב",
      },
      {
        id: "jlm-rehavia",
        title: "דירת 4 חדרים עם מרפסת, רחביה",
        price: "₪4,250,000",
        area: "104 מ״ר · קומה 3",
        city: "ירושלים",
      },
      {
        id: "haifa-carmel",
        title: "דירת 3 חדרים עם נוף לים, כרמל",
        price: "₪1,980,000",
        area: "88 מ״ר · קומה 4",
        city: "חיפה",
      },
      {
        id: "rg-bavli",
        title: "דירת 5 חדרים חדשה, בבלי רמת גן",
        price: "₪5,120,000",
        area: "126 מ״ר · קומה 12",
        city: "רמת גן",
      },
    ],
    viewAll: "לכל הדירות",
  },

  tools: {
    kicker: "כלים",
    title: "החישובים שאתם צריכים לפני שאתם חותמים",
    lead: {
      title: "מחשבון משכנתא",
      body: "החזר חודשי, מסלולים והצמדות — בשלוש שאלות.",
    },
    rest: [
      { title: "מס רכישה", body: "מדרגות מס לפי סוג הרוכש." },
      { title: "שווי נכס", body: "אומדן שוק לפי אזור וגודל." },
      { title: "קנייה מול שכירות", body: "מה משתלם לכם ב־10 שנים." },
      { title: "בדיקת התחדשות", body: "האם הבניין שלכם עומד בקריטריונים." },
    ],
  },

  magazine: {
    kicker: "מדריכים",
    title: "המדריכים שכל קונה חייב לקרוא",
    items: [
      {
        id: "post-tama",
        eyebrow: "התחדשות",
        title: "מה במקום תמ״א 38?",
        excerpt: "המסלולים שהחליפו את תמ״א 38, מה עובד היום ומי מרוויח.",
      },
      {
        id: "buy-guide",
        eyebrow: "מדריך",
        title: "מדריך קניית דירה: מהראשונה ועד המפתח",
        excerpt: "כל השלבים, המסמכים והבדיקות — בסדר הנכון.",
      },
      {
        id: "pinuy-binuy",
        eyebrow: "התחדשות",
        title: "פינוי־בינוי: המדריך המלא לדיירים",
        excerpt: "רוב דרוש, זכויות בנייה, מיסוי ולוחות זמנים.",
      },
    ],
  },

  project: {
    kicker: "פרויקט חדש",
    facts: {
      units: "דירות",
      floors: "קומות",
      rooms: "חדרים",
      price: "מחיר מ־",
      status: "סטטוס",
    },
    tabs: {
      apartments: "דירות",
      floors: "קומות",
      sun: "שמש ונוף",
      docs: "מסמכים",
    },
    offerCta: "בקשת שיחה עם היזם",
    tourCta: "כניסה לסיור התלת־ממדי",
    illustrative: "הדמיה בלבד — נבנה על מודל אמיתי לאחר קבלת חומרי היזם.",
  },

  myRentals: {
    kicker: "ניהול השכרות",
    title: "כל הדירות שלכם. בבניין, על המפה, ובתיק אחד.",
    sub: "פורטפוליו נחיתה למשכירים פרטיים — חינם, בעברית, בלי סליקה.",
    healthCards: [
      { key: "contract", title: "חוזה", status: "בתוקף · 8 חודשים" },
      { key: "rent", title: "שכ״ד", status: "שולם · הבא ב־01/07" },
      { key: "security", title: "בטוחות", status: "ערבות בנקאית · ₪18,000" },
      { key: "repairs", title: "תיקונים", status: "פתוח · 20 יום" },
      { key: "tax", title: "מס", status: "פטור · מתחת לתקרה" },
      { key: "renewal", title: "חידוש", status: "רלוונטי בעוד 4 חודשים" },
    ],
    ledgerTitle: "לוח תשלומים · 12 חודשים",
    demoNote: "נתוני דוגמה — מוצגים לצורך המחשה בלבד.",
  },

  myRenewal: {
    kicker: "חדר הפרויקט",
    title: "בניין אחד, כל הדיירים, מודל אחד.",
    sub: "צבע הדירה על המודל משתנה כשמסמנים הסכמה — 6 שלבים גלויים בכל רגע.",
    consent: [
      { name: "הסכימו", color: "success", count: 12 },
      { name: "עדיין בודקים", color: "warning", count: 5 },
      { name: "מתנגדים", color: "danger", count: 2 },
    ],
    stepper: [
      "בדיקת זכויות",
      "התארגנות דיירים",
      "בחירת יזם",
      "חתימת הסכם",
      "היתר בנייה",
      "פינוי דירות",
      "הריסה",
      "בנייה",
      "אכלוס",
      "מסירת מפתח",
    ],
  },
} as const;

export const EN = {
  brand: "NadLan",
  tagline: "Find an apartment. Check the price. Know the area.",

  nav: {
    projects: "New projects",
    listings: "Homes",
    professionals: "Professionals",
    urbanRenewal: "Urban renewal",
    rentals: "Rental manager",
    guides: "Guides",
  },

  footer: {
    product: "Product",
    solutions: "Solutions",
    tools: "Tools",
    company: "Company",
    calculators: "Calculators",
    glossary: "Glossary",
    about: "About",
    contact: "Contact",
    myRenewal: "Renewal room",
    myRentals: "Rental manager",
    guides: "Guides",
    disclaim: "This site is not legal, financial or professional advice. Renderings and illustrative plans are clearly labelled.",
    rights: "© 2026 NadLan",
  },

  hero: {
    kicker: "Real estate / Israel / 2026",
    title: "Find an apartment, check the price, know the area — before you sign",
    sub: "Every project on this site is a living 3D model: floors, apartments, sunlight and the view from the window.",
    tabs: ["Buy", "Rent", "Projects", "Professionals"],
    placeholder: "City, neighborhood or project",
    search: "Search",
    trust: "197 projects · 938 renewal sites · 5 calculators",
  },
} as const;

