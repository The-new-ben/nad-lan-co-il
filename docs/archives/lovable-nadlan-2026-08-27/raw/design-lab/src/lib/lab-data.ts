export type ConceptId =
  | "j1"
  | "j2"
  | "j3"
  | "n1"
  | "n2"
  | "n3"
  | "fj"
  | "fn";

export type Concept = {
  id: ConceptId;
  path: string;
  brand: "justice" | "nadlan";
  code: string;
  name: string;
  tagline: string;
  theme: string;
  final?: boolean;
};

export const concepts: Concept[] = [
  {
    id: "j1",
    path: "/justice/product-first",
    brand: "justice",
    code: "J1",
    name: "Justice · מוצר תחילה",
    tagline: "בורר תרחישים ותצוגת סימולציה מעל הקיפול",
    theme: "theme-j1",
  },
  {
    id: "j2",
    path: "/justice/authority-first",
    brand: "justice",
    code: "J2",
    name: "Justice · סמכות תוכן",
    tagline: "עורך ראשי, E-E-A-T גלוי, מוביל לכלים",
    theme: "theme-j2",
  },
  {
    id: "j3",
    path: "/justice/dual-audience",
    brand: "justice",
    code: "J3",
    name: "Justice · שני קהלים",
    tagline: "כניסה מפוצלת לפרטיים ולעורכי דין וחברות",
    theme: "theme-j3",
  },
  {
    id: "n1",
    path: "/nadlan/tools-first",
    brand: "nadlan",
    code: "N1",
    name: "נדל״ן · כלים תחילה",
    tagline: "משגר מחשבונים, חותמת עדכון חוק, תוצאה לשיתוף",
    theme: "theme-n1",
  },
  {
    id: "n2",
    path: "/nadlan/map-first",
    brand: "nadlan",
    code: "N2",
    name: "נדל״ן · מפה והחלטה",
    tagline: "מסע ״איפה אתם בתהליך?״ עם בדיקת נכס",
    theme: "theme-n2",
  },
  {
    id: "n3",
    path: "/nadlan/authority-first",
    brand: "nadlan",
    code: "N3",
    name: "נדל״ן · סמכות תוכן",
    tagline: "עמודי תוכן ומילון שמזינים את המחשבונים",
    theme: "theme-n3",
  },
  {
    id: "fj",
    path: "/final/justice",
    brand: "justice",
    code: "F-J",
    name: "Justice · כיוון סופי",
    tagline: "J1 מוצר תחילה + שכבת סמכות מ‑J2 + פיצול קהלים מרוסן",
    theme: "theme-j1",
    final: true,
  },
  {
    id: "fn",
    path: "/final/nadlan",
    brand: "nadlan",
    code: "F-N",
    name: "נדל״ן · כיוון סופי",
    tagline: "N1 כלים תחילה + מנוע קישור פנימי מ‑N3 + צ׳ק־ליסט שלב מ‑N2",
    theme: "theme-n1",
    final: true,
  },
];

export const justiceMenu = [
  "תחומי משפט",
  "כלים וסימולציות",
  "איך זה עובד",
  "לעורכי דין",
  "ידע משפטי",
];

export const nadlanMenu = [
  "כלים ומחשבונים",
  "קנייה ומכירה",
  "משכנתאות",
  "בדיקות נכס",
  "מדריכים",
  "מילון נדל״ן",
];

export type ContentCard = {
  title: string;
  intent: string;
  href: string;
  linkLabel: string;
};

export const justiceCards: ContentCard[] = [
  {
    title: "חקירת עדים",
    intent: "מה מותר לשאול, איך נבנית שורת שאלות ואיך מתכוננים להפתעות",
    href: "/justice/tools/witness-cross-examination",
    linkLabel: "תרגלו חקירת עדים בסימולציה",
  },
  {
    title: "הכנה לדיון",
    intent: "מה קורה באולם, מה להביא ואיך מנסחים תשובה קצרה ומדויקת",
    href: "/justice/tools/hearing-preparation",
    linkLabel: "הריצו סימולציית דיון",
  },
  {
    title: "עלות גירושין",
    intent: "מרכיבי העלות בהליך, מה משפיע עליהם ואיפה נוצרים פערים",
    href: "/justice/guides/divorce-cost",
    linkLabel: "בדקו את מרכיבי העלות בתרחיש שלכם",
  },
  {
    title: "מחיקת רישום פלילי",
    intent: "תנאי סף, מסלולים אפשריים ומה נדרש להוכיח",
    href: "/justice/guides/criminal-record-erasure",
    linkLabel: "בדקו התאמה למסלול בסימולציה",
  },
  {
    title: "הסכם גירושין",
    intent: "סעיפים מרכזיים, נקודות מחלוקת נפוצות ואיך מגיעים מוכנים",
    href: "/justice/guides/divorce-agreement",
    linkLabel: "עברו לסימולציית משא ומתן",
  },
];

export type NadlanTool = {
  title: string;
  owns: string;
  href: string;
  linkLabel: string;
  note: string;
};

export const nadlanTools: NadlanTool[] = [
  {
    title: "נסח טאבו",
    owns: "כוונת חיפוש: הפקה, קריאה והבנה של נסח רישום מקרקעין",
    href: "/nadlan/tools/tabu-extract",
    linkLabel: "פתחו את מדריך נסח טאבו",
    note: "עמוד כלי עצמאי. לא ממוזג לתוך מחשבון מס.",
  },
  {
    title: "מחשבון מס רכישה",
    owns: "כוונת חיפוש: כמה מס רכישה אשלם על דירה",
    href: "/nadlan/tools/purchase-tax-calculator",
    linkLabel: "חשבו מס רכישה",
    note: "עמוד מחשבון ייעודי עם מדרגות ותאריך עדכון.",
  },
  {
    title: "סימולטור מס רכישה",
    owns: "כוונת חיפוש: השוואת תרחישים — דירה יחידה, נוספת, שינוי מועד",
    href: "/nadlan/tools/purchase-tax-simulator",
    linkLabel: "השוו תרחישי מס רכישה",
    note: "נפרד מהמחשבון: השוואה בין מצבים, לא חישוב בודד.",
  },
  {
    title: "מחשבון מס שבח",
    owns: "כוונת חיפוש: מס שבח במכירת דירה, פטורים וחישוב ליניארי",
    href: "/nadlan/tools/capital-gains-calculator",
    linkLabel: "חשבו מס שבח",
    note: "עמוד נפרד לחלוטין מכלי מס הרכישה.",
  },
];

export const nadlanPillars = [
  {
    title: "קנייה ומכירה של דירה",
    desc: "סדר הפעולות מהחלטה ועד מסירה, ומה נבדק בכל שלב",
    href: "/nadlan/guides/buying-selling",
  },
  {
    title: "משכנתאות",
    desc: "מבנה תמהיל, מסמכים נדרשים ומה משפיע על אישור עקרוני",
    href: "/nadlan/guides/mortgages",
  },
  {
    title: "בדיקות נכס לפני חתימה",
    desc: "רישום, תכנון ובנייה, מצב פיזי וחובות — מה מאתרים ואיך",
    href: "/nadlan/guides/due-diligence",
  },
  {
    title: "מילון נדל״ן",
    desc: "מונחים בשפה פשוטה, כל ערך מקשר לכלי הרלוונטי",
    href: "/nadlan/glossary",
  },
];

