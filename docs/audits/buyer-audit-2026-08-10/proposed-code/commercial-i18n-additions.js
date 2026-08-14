/**
 * PROPOSAL ONLY — NOT APPLIED.
 * Complete commercial-decision vocabulary for HE/EN/FR/RU/AR.
 *
 * Every locale owns the same complete key set. `get()` never merges a partial
 * locale with English, so a missing translation fails during initialization
 * instead of leaking mixed-language buyer copy into the decision surface.
 */
(function commercialI18nModule(window) {
  "use strict";

  var SUPPORTED = ["he", "en", "fr", "ru", "ar"];

  var dictionaries = {
    en: {
      locale: "en", dir: "ltr",
      chooseFloor: "Choose a floor to explore",
      modelSelectionUnavailable: "Explore with the floor list while model selection is unavailable.",
      noFloorAtPoint: "There is no selectable floor at this point.",
      nonSelectableFloor: "This level is shown for context but is not offered for selection.",
      selected: "Selected",
      verified: "verified", effective: "effective", sources: "sources",
      askThis: "Ask for this answer", owner: "Answer owner", ownerUnknown: "No accountable answer owner is assigned",
      conflictingObservations: "The sources conflict — open the evidence before relying on this item",
      beamUnknown: "The orientation scene is waiting for a verified anchor and facade calibration",
      beamScene: "Where this facade looks", projectHere: "Project",
      exposureUnknown: "The facade direction is not verified yet",
      beamUnknownBody: "The map stays neutral until the project anchor and facade azimuth are evidenced. No cone or landmark is guessed.",
      beamIllustrativeCaveat: "Illustrative orientation aid; request the signed orientation and view pack before relying on it.",
      directionUnknown: "Direction not verified", viewContradictory: "the view evidence conflicts", viewUnknown: "the view context is not verified",
      exposures: "Facade exposures", requestEvidence: "See what must be verified",
      rentableArea: "Rentable area", planningCapacity: "Planning capacity", people: "people", allInCost: "Monthly all-in cost",
      backToBuilding: "Back to the building", selectedOffice: "The office space you selected", unidentifiedAsset: "Selected space",
      evidenceTools: "Ways to understand this space", floorPack: "Open the floor pack", floorPackBody: "See the plan, measured area, core and source documents",
      fitOut: "Explore fit-out and infrastructure", fitOutBody: "See capacity, MEP, telecoms and delivery conditions",
      context: "See the commute and area", contextBody: "Explore sourced routes, daily needs, market context and risks",
      cost: "Understand the full occupancy cost", costBody: "See rent, charges, comparisons and supporting records",
      actions: "Space actions", save: "Save this space", compare: "Compare spaces", share: "Share this space",
      askAbout: "Ask us about", thisSpace: "this space", inquiry: "Build a question pack", back: "Back",
      noFloorPack: "A verified floor pack is not attached yet.", requestFloorPack: "Ask for the verified floor pack",
      notVerified: "Not verified yet — add this question", contextAdapterRequired: "The verified location layer needs its approved map adapter before it can be shown.",
      requestContextPack: "Ask for the verified location and commute pack", costUnknown: "The complete commercial schedule has not been verified for this space.",
      requestTerms: "Ask for the full commercial schedule", compareHelp: "Choose another sourced space to compare facts side by side.",
      inquiryHelp: "Choose the questions and documents you want; the responsible commercial route will answer them.",
      modelRegion: "Interactive building and floor selection", decisionRegion: "Selected space facts and decision tools",
      network: "by route", straightLine: "straight line", noRoute: "Route not calculated", openSource: "Open supporting source",
      notCalculated: "Not calculated", modeLabel: "Explore the area by topic", mapLabel: "Sourced project context map",
      caveat: "Travel times are ranges. Operating and planned transport are shown separately.", mapUnavailable: "Interactive map unavailable",
      mapFallback: "The sourced place and route cards remain available.", noEvidence: "No current sourced evidence is available in this view",
      askForLayer: "Ask for this context layer", results: "Results", page: "Page", pagination: "Context result pages", previous: "Previous", next: "Next",
      selectedContext: "Selected space", questionsTitle: "What would help you decide?", questions: "Questions to answer", documents: "Documents to receive",
      otherQuestion: "What else should the team answer?", continue: "Continue to contact details", contactTitle: "Where should the complete answer reach you?",
      companyName: "Company", contactName: "Contact name", email: "Email", internationalPhone: "International phone",
      headcount: "Planned headcount", moveIn: "Target move-in (YYYY-MM)", privacyConsent: "I agree to the privacy notice for handling this request",
      termsConsent: "I agree to the request terms", marketingConsent: "Send useful project updates (optional)", send: "Send my question and document pack",
      chooseOne: "Choose a question, document, or write your own request.", contactRequired: "Add an email or international phone number.",
      secureRetryUnavailable: "Secure submission is unavailable. Please keep this window open and try again.", sending: "Sending your selected questions…",
      retryPreserved: "Nothing was cleared. Review and retry; the same request key prevents a second case.", received: "Your request reached the responsible commercial route",
      caseId: "Case", recipient: "Responsible route", commercialTeam: "Commercial response team", sla: "Response target", hours: "hours",
      safeConfirmation: "For privacy, this confirmation does not expose a private mailbox or staff identity.",
      fitOutTopics: { capacity: "Capacity", hvac: "HVAC", power_backup: "Power and backup", fiber: "Fiber connectivity", lifts_loading: "Lifts and loading", accessibility: "Accessible route" },
      status: {
        unknown: "Availability not verified", verified_available: "Verified available", soft_hold: "Soft hold", under_offer: "Under offer",
        under_loi: "Under LOI", leased: "Leased", delivered: "Delivered", unavailable: "Unavailable", not_marketed: "Not marketed"
      },
      evidenceStates: { unknown: "Unknown", source_estimate: "Sourced estimate", verified: "Verified", contradictory: "Conflicting sources" },
      states: { unknown: "Unknown", source_estimate: "Sourced estimate", verified: "Verified", contradictory: "Conflicting sources" },
      modes: { commute: "Commute", daily_life: "Daily life", business: "Business services", market: "Market", risk: "Risks" },
      routeKinds: { project_team: "Accountable project team", commercial_desk: "Accountable commercial desk" },
      rfpQuestions: {
        live_availability: "Which floors and suites are genuinely available now?", asking_rent: "What is the current asking rent and charge schedule?",
        net_to_gross: "How is net-to-gross measured?", power_capacity: "What electrical, backup and cooling capacity is committed?",
        commute_and_transport: "What are the sourced commute and transport options?", nearby_facilities: "Which everyday facilities are operating nearby?"
      },
      rfpDocuments: {
        availability_schedule: "Dated availability schedule", floor_plan_pdf: "Floor plan PDF", measurement_report: "Measurement report",
        tenant_technical_manual: "Tenant technical manual", orientation_plan: "Signed orientation plan", lease_draft: "Lease draft or heads of terms"
      }
    },

    he: {
      locale: "he", dir: "rtl",
      chooseFloor: "בחרו קומה כדי להכיר אותה",
      modelSelectionUnavailable: "אפשר להמשיך דרך רשימת הקומות בזמן שהבחירה על המודל אינה זמינה.",
      noFloorAtPoint: "אין בנקודה הזאת קומה שאפשר לבחור.",
      nonSelectableFloor: "המפלס מוצג להקשר, אך אינו מוצע לבחירה.",
      selected: "נבחרה",
      verified: "אומת", effective: "בתוקף", sources: "מקורות",
      askThis: "בקשו תשובה לשאלה הזאת", owner: "אחראי לתשובה", ownerUnknown: "עדיין לא הוגדר גורם אחראי לתשובה",
      conflictingObservations: "המקורות סותרים זה את זה — פתחו את הראיות לפני שמסתמכים על הנתון",
      beamUnknown: "סצנת הכיוון ממתינה לעוגן פרויקט ולאזימוט חזית מאומתים",
      beamScene: "לאן החזית הזאת פונה", projectHere: "הפרויקט",
      exposureUnknown: "כיוון החזית עדיין לא אומת",
      beamUnknownBody: "המפה נשארת ניטרלית עד שעוגן הפרויקט וכיוון החזית מגובים בראיות. לא מציירים אלומה או נקודת ציון בניחוש.",
      beamIllustrativeCaveat: "המחשת התמצאות בלבד; לפני הסתמכות בקשו תוכנית כיוונים וחבילת נוף חתומות.",
      directionUnknown: "הכיוון לא אומת", viewContradictory: "ראיות הנוף סותרות", viewUnknown: "הקשר הנוף לא אומת",
      exposures: "כיווני החזית", requestEvidence: "ראו מה צריך לאמת",
      rentableArea: "שטח להשכרה", planningCapacity: "קיבולת תכנון", people: "אנשים", allInCost: "עלות חודשית כוללת",
      backToBuilding: "חזרה לבניין", selectedOffice: "שטח המשרד שבחרתם", unidentifiedAsset: "השטח הנבחר",
      evidenceTools: "דרכים להכיר את השטח", floorPack: "פתחו את חבילת הקומה", floorPackBody: "ראו תוכנית, שטח מדוד, גרעין ומסמכי מקור",
      fitOut: "גלו את התכנון והתשתיות", fitOutBody: "ראו קיבולת, מערכות, תקשורת ותנאי מסירה",
      context: "גלו את ההגעה והסביבה", contextBody: "בדקו מסלולים, צרכים יומיומיים, שוק וסיכונים עם מקורות",
      cost: "הבינו את עלות האכלוס המלאה", costBody: "ראו שכירות, חיובים, השוואות ומסמכים תומכים",
      actions: "פעולות לשטח", save: "שמרו את השטח", compare: "השוו שטחים", share: "שתפו את השטח",
      askAbout: "שאלו אותנו על", thisSpace: "השטח הזה", inquiry: "בנו סל שאלות", back: "חזרה",
      noFloorPack: "עדיין לא צורפה חבילת קומה מאומתת.", requestFloorPack: "בקשו את חבילת הקומה המאומתת",
      notVerified: "עדיין לא אומת — הוסיפו לסל השאלות", contextAdapterRequired: "שכבת המיקום המאומתת תוצג רק אחרי חיבור למתאם המפה המאושר.",
      requestContextPack: "בקשו את חבילת המיקום וההגעה המאומתת", costUnknown: "לשטח הזה עדיין אין לוח תנאים מסחריים מלא ומאומת.",
      requestTerms: "בקשו את לוח התנאים המסחרי המלא", compareHelp: "בחרו שטח נוסף עם מקורות והשוו את העובדות זו לצד זו.",
      inquiryHelp: "בחרו את השאלות והמסמכים שחשובים לכם; הגורם המסחרי האחראי יחזור עם תשובה.",
      modelRegion: "בניין אינטראקטיבי ובחירת קומה", decisionRegion: "עובדות וכלי החלטה לשטח הנבחר",
      network: "במסלול", straightLine: "בקו אווירי", noRoute: "המסלול לא חושב", openSource: "פתחו את המקור התומך",
      notCalculated: "לא חושב", modeLabel: "גלו את הסביבה לפי נושא", mapLabel: "מפת הקשר לפרויקט עם מקורות",
      caveat: "זמני הנסיעה מוצגים כטווחים. תחבורה פעילה ומתוכננת מוצגות בנפרד.", mapUnavailable: "המפה האינטראקטיבית אינה זמינה",
      mapFallback: "כרטיסי המקומות והמסלולים עם המקורות עדיין זמינים.", noEvidence: "אין בתצוגה הזאת ראיות עדכניות עם מקור",
      askForLayer: "בקשו את שכבת המידע הזאת", results: "תוצאות", page: "עמוד", pagination: "עמודי תוצאות הסביבה", previous: "הקודם", next: "הבא",
      selectedContext: "השטח הנבחר", questionsTitle: "מה יעזור לכם להחליט?", questions: "שאלות לקבל עליהן תשובה", documents: "מסמכים לקבלה",
      otherQuestion: "מה עוד תרצו שהצוות יבדוק?", continue: "המשיכו לפרטי הקשר", contactTitle: "לאן לשלוח את התשובה המלאה?",
      companyName: "שם החברה", contactName: "שם איש הקשר", email: "דוא״ל", internationalPhone: "טלפון בינלאומי",
      headcount: "מספר עובדים מתוכנן", moveIn: "מועד כניסה רצוי (YYYY-MM)", privacyConsent: "אני מסכים/ה להודעת הפרטיות לצורך הטיפול בבקשה",
      termsConsent: "אני מסכים/ה לתנאי הבקשה", marketingConsent: "שלחו עדכוני פרויקט שימושיים (רשות)", send: "שלחו את סל השאלות והמסמכים שלי",
      chooseOne: "בחרו שאלה, מסמך או כתבו בקשה משלכם.", contactRequired: "הוסיפו דוא״ל או מספר טלפון בינלאומי.",
      secureRetryUnavailable: "השליחה המאובטחת אינה זמינה. השאירו את החלון פתוח ונסו שוב.", sending: "שולחים את השאלות שבחרתם…",
      retryPreserved: "דבר לא נמחק. בדקו ונסו שוב; אותו מפתח בקשה מונע פתיחת פנייה כפולה.", received: "הבקשה הגיעה למסלול המסחרי האחראי",
      caseId: "מספר פנייה", recipient: "מסלול אחראי", commercialTeam: "צוות המענה המסחרי", sla: "יעד למענה", hours: "שעות",
      safeConfirmation: "לשמירת הפרטיות, האישור אינו חושף תיבה פרטית או זהות של עובד.",
      fitOutTopics: { capacity: "קיבולת", hvac: "מיזוג ואוורור", power_backup: "חשמל וגיבוי", fiber: "קישוריות סיבים", lifts_loading: "מעליות ופריקה", accessibility: "מסלול נגיש" },
      status: {
        unknown: "הזמינות לא אומתה", verified_available: "זמין ומאומת", soft_hold: "שמירה זמנית", under_offer: "בתהליך הצעה",
        under_loi: "בתהליך מסמך כוונות", leased: "הושכר", delivered: "נמסר", unavailable: "לא זמין", not_marketed: "אינו משווק"
      },
      evidenceStates: { unknown: "לא ידוע", source_estimate: "הערכה עם מקור", verified: "מאומת", contradictory: "מקורות סותרים" },
      states: { unknown: "לא ידוע", source_estimate: "הערכה עם מקור", verified: "מאומת", contradictory: "מקורות סותרים" },
      modes: { commute: "הגעה", daily_life: "חיי יום־יום", business: "שירותים לעסקים", market: "שוק", risk: "סיכונים" },
      routeKinds: { project_team: "צוות הפרויקט האחראי", commercial_desk: "הדסק המסחרי האחראי" },
      rfpQuestions: {
        live_availability: "אילו קומות ויחידות באמת זמינות עכשיו?", asking_rent: "מהם דמי השכירות והחיובים המבוקשים כעת?",
        net_to_gross: "איך נמדד היחס בין נטו לברוטו?", power_capacity: "איזו קיבולת חשמל, גיבוי וקירור מובטחת?",
        commute_and_transport: "מהן אפשרויות ההגעה והתחבורה עם מקורות?", nearby_facilities: "אילו שירותים יומיומיים פועלים בסביבה?"
      },
      rfpDocuments: {
        availability_schedule: "טבלת זמינות מתוארכת", floor_plan_pdf: "תוכנית קומה PDF", measurement_report: "דוח מדידה",
        tenant_technical_manual: "מדריך טכני לשוכר", orientation_plan: "תוכנית כיוונים חתומה", lease_draft: "טיוטת שכירות או עיקרי תנאים"
      }
    },

    fr: {
      locale: "fr", dir: "ltr",
      chooseFloor: "Choisissez un étage à explorer",
      modelSelectionUnavailable: "Explorez avec la liste des étages pendant que la sélection sur le modèle est indisponible.",
      noFloorAtPoint: "Aucun étage sélectionnable à cet endroit.", nonSelectableFloor: "Ce niveau donne du contexte mais n’est pas proposé à la sélection.", selected: "Sélectionné",
      verified: "vérifié", effective: "en vigueur", sources: "sources", askThis: "Demander cette réponse", owner: "Responsable de la réponse", ownerUnknown: "Aucun responsable n’est encore attribué",
      conflictingObservations: "Les sources se contredisent — ouvrez les preuves avant de vous fier à cette donnée",
      beamUnknown: "La scène d’orientation attend un point projet et un azimut de façade vérifiés", beamScene: "Vers quoi regarde cette façade", projectHere: "Projet",
      exposureUnknown: "L’orientation de la façade n’est pas encore vérifiée", beamUnknownBody: "La carte reste neutre tant que le point projet et l’azimut ne sont pas étayés. Aucun cône ni repère n’est deviné.",
      beamIllustrativeCaveat: "Aide d’orientation illustrative ; demandez le plan signé et le dossier de vues avant de vous y fier.", directionUnknown: "Direction non vérifiée",
      viewContradictory: "les preuves de vue se contredisent", viewUnknown: "le contexte de vue n’est pas vérifié", exposures: "Orientations de façade", requestEvidence: "Voir ce qui doit être vérifié",
      rentableArea: "Surface locative", planningCapacity: "Capacité d’aménagement", people: "personnes", allInCost: "Coût mensuel tout compris",
      backToBuilding: "Retour au bâtiment", selectedOffice: "L’espace de bureau sélectionné", unidentifiedAsset: "Espace sélectionné", evidenceTools: "Mieux comprendre cet espace",
      floorPack: "Ouvrir le dossier d’étage", floorPackBody: "Voir plan, surface mesurée, noyau et pièces sources", fitOut: "Explorer l’aménagement et les infrastructures",
      fitOutBody: "Voir capacité, équipements techniques, télécoms et conditions de livraison", context: "Voir les trajets et le quartier", contextBody: "Explorer trajets sourcés, quotidien, marché et risques",
      cost: "Comprendre le coût d’occupation complet", costBody: "Voir loyer, charges, comparaisons et justificatifs", actions: "Actions sur l’espace", save: "Enregistrer cet espace",
      compare: "Comparer les espaces", share: "Partager cet espace", askAbout: "Nous interroger sur", thisSpace: "cet espace", inquiry: "Composer vos questions", back: "Retour",
      noFloorPack: "Aucun dossier d’étage vérifié n’est encore joint.", requestFloorPack: "Demander le dossier d’étage vérifié", notVerified: "Pas encore vérifié — ajouter la question",
      contextAdapterRequired: "La couche de localisation vérifiée nécessite son adaptateur cartographique approuvé.", requestContextPack: "Demander le dossier vérifié de localisation et de trajet",
      costUnknown: "La grille commerciale complète n’est pas vérifiée pour cet espace.", requestTerms: "Demander la grille commerciale complète",
      compareHelp: "Choisissez un autre espace sourcé pour comparer les faits côte à côte.", inquiryHelp: "Choisissez les questions et documents souhaités ; le circuit commercial responsable répondra.",
      modelRegion: "Bâtiment interactif et choix d’étage", decisionRegion: "Faits et outils de décision de l’espace sélectionné",
      network: "par itinéraire", straightLine: "à vol d’oiseau", noRoute: "Itinéraire non calculé", openSource: "Ouvrir la source", notCalculated: "Non calculé",
      modeLabel: "Explorer le quartier par thème", mapLabel: "Carte contextuelle sourcée du projet", caveat: "Les temps de trajet sont des fourchettes. Les transports en service et projetés sont séparés.",
      mapUnavailable: "Carte interactive indisponible", mapFallback: "Les fiches de lieux et d’itinéraires sourcées restent disponibles.", noEvidence: "Aucune preuve sourcée actuelle dans cette vue",
      askForLayer: "Demander cette couche de contexte", results: "Résultats", page: "Page", pagination: "Pages des résultats contextuels", previous: "Précédent", next: "Suivant",
      selectedContext: "Espace sélectionné", questionsTitle: "Qu’est-ce qui vous aiderait à décider ?", questions: "Questions à faire répondre", documents: "Documents à recevoir",
      otherQuestion: "Que doit encore vérifier l’équipe ?", continue: "Continuer vers vos coordonnées", contactTitle: "Où envoyer la réponse complète ?", companyName: "Entreprise",
      contactName: "Nom du contact", email: "E-mail", internationalPhone: "Téléphone international", headcount: "Effectif prévu", moveIn: "Emménagement visé (AAAA-MM)",
      privacyConsent: "J’accepte la notice de confidentialité pour traiter cette demande", termsConsent: "J’accepte les conditions de la demande", marketingConsent: "Recevoir des nouvelles utiles du projet (facultatif)",
      send: "Envoyer mon lot de questions et documents", chooseOne: "Choisissez une question, un document ou rédigez votre demande.", contactRequired: "Ajoutez un e-mail ou un téléphone international.",
      secureRetryUnavailable: "L’envoi sécurisé est indisponible. Gardez cette fenêtre ouverte et réessayez.", sending: "Envoi de vos questions sélectionnées…",
      retryPreserved: "Rien n’a été effacé. Vérifiez puis réessayez ; la même clé empêche un second dossier.", received: "Votre demande a atteint le circuit commercial responsable",
      caseId: "Dossier", recipient: "Circuit responsable", commercialTeam: "Équipe de réponse commerciale", sla: "Délai cible", hours: "heures",
      safeConfirmation: "Pour votre confidentialité, cette confirmation n’expose ni boîte privée ni identité d’employé.",
      fitOutTopics: { capacity: "Capacité", hvac: "CVC", power_backup: "Électricité et secours", fiber: "Connectivité fibre", lifts_loading: "Ascenseurs et livraisons", accessibility: "Parcours accessible" },
      status: { unknown: "Disponibilité non vérifiée", verified_available: "Disponible et vérifié", soft_hold: "Réservation souple", under_offer: "Sous offre", under_loi: "Sous lettre d’intention", leased: "Loué", delivered: "Livré", unavailable: "Indisponible", not_marketed: "Non commercialisé" },
      evidenceStates: { unknown: "Inconnu", source_estimate: "Estimation sourcée", verified: "Vérifié", contradictory: "Sources contradictoires" },
      states: { unknown: "Inconnu", source_estimate: "Estimation sourcée", verified: "Vérifié", contradictory: "Sources contradictoires" },
      modes: { commute: "Trajets", daily_life: "Vie quotidienne", business: "Services aux entreprises", market: "Marché", risk: "Risques" },
      routeKinds: { project_team: "Équipe projet responsable", commercial_desk: "Cellule commerciale responsable" },
      rfpQuestions: { live_availability: "Quels étages et lots sont réellement disponibles aujourd’hui ?", asking_rent: "Quel est le loyer demandé et la grille de charges actuelle ?", net_to_gross: "Comment le ratio net/brut est-il mesuré ?", power_capacity: "Quelles capacités électriques, de secours et de refroidissement sont garanties ?", commute_and_transport: "Quelles options de trajet et de transport sont sourcées ?", nearby_facilities: "Quels services quotidiens fonctionnent à proximité ?" },
      rfpDocuments: { availability_schedule: "État daté des disponibilités", floor_plan_pdf: "Plan d’étage PDF", measurement_report: "Rapport de mesure", tenant_technical_manual: "Manuel technique preneur", orientation_plan: "Plan d’orientation signé", lease_draft: "Projet de bail ou principaux termes" }
    },

    ru: {
      locale: "ru", dir: "ltr",
      chooseFloor: "Выберите этаж для просмотра", modelSelectionUnavailable: "Пока выбор на модели недоступен, используйте список этажей.", noFloorAtPoint: "В этой точке нет доступного для выбора этажа.", nonSelectableFloor: "Уровень показан для ориентира, но не предлагается для выбора.", selected: "Выбрано",
      verified: "проверено", effective: "действует", sources: "источников", askThis: "Запросить ответ", owner: "Ответственный за ответ", ownerUnknown: "Ответственный пока не назначен", conflictingObservations: "Источники противоречат друг другу — откройте доказательства, прежде чем полагаться на данные",
      beamUnknown: "Сцена ориентации ожидает проверенные координаты проекта и азимут фасада", beamScene: "Куда обращён этот фасад", projectHere: "Проект", exposureUnknown: "Направление фасада ещё не проверено", beamUnknownBody: "Карта остаётся нейтральной, пока координаты проекта и азимут фасада не подтверждены. Конус и ориентиры не угадываются.", beamIllustrativeCaveat: "Иллюстрация для ориентации; запросите подписанный план и пакет видов до принятия решения.", directionUnknown: "Направление не проверено", viewContradictory: "данные о виде противоречат", viewUnknown: "контекст вида не проверен", exposures: "Ориентация фасада", requestEvidence: "Узнать, что нужно проверить",
      rentableArea: "Арендуемая площадь", planningCapacity: "Расчётная вместимость", people: "человек", allInCost: "Полная месячная стоимость", backToBuilding: "Вернуться к зданию", selectedOffice: "Выбранное офисное пространство", unidentifiedAsset: "Выбранное пространство", evidenceTools: "Как изучить это пространство", floorPack: "Открыть пакет этажа", floorPackBody: "План, измеренная площадь, ядро и исходные документы", fitOut: "Изучить отделку и инфраструктуру", fitOutBody: "Вместимость, инженерия, связь и условия передачи", context: "Изучить дорогу и район", contextBody: "Маршруты с источниками, повседневные услуги, рынок и риски", cost: "Понять полную стоимость размещения", costBody: "Аренда, сборы, сравнения и подтверждающие записи", actions: "Действия с пространством", save: "Сохранить пространство", compare: "Сравнить пространства", share: "Поделиться пространством", askAbout: "Спросить нас о", thisSpace: "этом пространстве", inquiry: "Собрать пакет вопросов", back: "Назад",
      noFloorPack: "Проверенный пакет этажа пока не приложен.", requestFloorPack: "Запросить проверенный пакет этажа", notVerified: "Ещё не проверено — добавить вопрос", contextAdapterRequired: "Для проверенного слоя местоположения нужен одобренный картографический адаптер.", requestContextPack: "Запросить проверенный пакет локации и маршрутов", costUnknown: "Полная коммерческая таблица для этого пространства не проверена.", requestTerms: "Запросить полную коммерческую таблицу", compareHelp: "Выберите другое пространство с источниками и сравните факты рядом.", inquiryHelp: "Выберите вопросы и документы; ответит ответственный коммерческий маршрут.", modelRegion: "Интерактивное здание и выбор этажа", decisionRegion: "Факты и инструменты решения по выбранному пространству",
      network: "по маршруту", straightLine: "по прямой", noRoute: "Маршрут не рассчитан", openSource: "Открыть источник", notCalculated: "Не рассчитано", modeLabel: "Изучить район по теме", mapLabel: "Карта контекста проекта с источниками", caveat: "Время в пути дано диапазоном. Действующий и планируемый транспорт разделены.", mapUnavailable: "Интерактивная карта недоступна", mapFallback: "Карточки мест и маршрутов с источниками остаются доступны.", noEvidence: "В этом виде нет актуальных данных с источниками", askForLayer: "Запросить этот слой контекста", results: "Результаты", page: "Страница", pagination: "Страницы результатов по району", previous: "Предыдущая", next: "Следующая",
      selectedContext: "Выбранное пространство", questionsTitle: "Что поможет вам принять решение?", questions: "Вопросы для ответа", documents: "Документы для получения", otherQuestion: "Что ещё должна проверить команда?", continue: "Перейти к контактам", contactTitle: "Куда направить полный ответ?", companyName: "Компания", contactName: "Контактное лицо", email: "Электронная почта", internationalPhone: "Международный телефон", headcount: "Планируемое число сотрудников", moveIn: "Желаемый въезд (ГГГГ-ММ)", privacyConsent: "Я согласен с уведомлением о конфиденциальности для обработки запроса", termsConsent: "Я согласен с условиями запроса", marketingConsent: "Присылать полезные новости проекта (необязательно)", send: "Отправить мой пакет вопросов и документов", chooseOne: "Выберите вопрос, документ или напишите свой запрос.", contactRequired: "Добавьте электронную почту или международный телефон.", secureRetryUnavailable: "Безопасная отправка недоступна. Оставьте окно открытым и попробуйте ещё раз.", sending: "Отправляем выбранные вопросы…", retryPreserved: "Ничего не удалено. Проверьте и повторите; тот же ключ не позволит создать второе обращение.", received: "Запрос поступил ответственному коммерческому маршруту", caseId: "Обращение", recipient: "Ответственный маршрут", commercialTeam: "Команда коммерческого ответа", sla: "Целевой срок ответа", hours: "часов", safeConfirmation: "Для защиты данных подтверждение не раскрывает личный ящик или сотрудника.",
      fitOutTopics: { capacity: "Вместимость", hvac: "Вентиляция и кондиционирование", power_backup: "Электроснабжение и резерв", fiber: "Оптоволоконная связь", lifts_loading: "Лифты и погрузка", accessibility: "Доступный маршрут" },
      status: { unknown: "Доступность не проверена", verified_available: "Проверено: доступно", soft_hold: "Мягкая бронь", under_offer: "На стадии предложения", under_loi: "На стадии письма о намерениях", leased: "Сдано", delivered: "Передано", unavailable: "Недоступно", not_marketed: "Не предлагается" },
      evidenceStates: { unknown: "Неизвестно", source_estimate: "Оценка с источником", verified: "Проверено", contradictory: "Источники противоречат" },
      states: { unknown: "Неизвестно", source_estimate: "Оценка с источником", verified: "Проверено", contradictory: "Источники противоречат" },
      modes: { commute: "Дорога", daily_life: "Повседневная жизнь", business: "Деловые услуги", market: "Рынок", risk: "Риски" },
      routeKinds: { project_team: "Ответственная команда проекта", commercial_desk: "Ответственный коммерческий центр" },
      rfpQuestions: { live_availability: "Какие этажи и блоки действительно доступны сейчас?", asking_rent: "Какова текущая запрашиваемая аренда и таблица сборов?", net_to_gross: "Как измеряется соотношение полезной и арендуемой площади?", power_capacity: "Какая мощность электроснабжения, резерва и охлаждения гарантируется?", commute_and_transport: "Какие маршруты и транспорт подтверждены источниками?", nearby_facilities: "Какие повседневные услуги уже работают рядом?" },
      rfpDocuments: { availability_schedule: "Датированная ведомость доступности", floor_plan_pdf: "План этажа PDF", measurement_report: "Отчёт об измерениях", tenant_technical_manual: "Техническое руководство арендатора", orientation_plan: "Подписанный план ориентации", lease_draft: "Проект договора или основные условия" }
    },

    ar: {
      locale: "ar", dir: "rtl",
      chooseFloor: "اختاروا طابقًا لاستكشافه", modelSelectionUnavailable: "يمكن الاستكشاف من قائمة الطوابق أثناء تعذّر الاختيار على المجسّم.", noFloorAtPoint: "لا يوجد طابق قابل للاختيار في هذه النقطة.", nonSelectableFloor: "يظهر هذا المستوى للسياق لكنه غير معروض للاختيار.", selected: "تم الاختيار",
      verified: "تم التحقق", effective: "ساري", sources: "مصادر", askThis: "اطلبوا إجابة عن هذا السؤال", owner: "المسؤول عن الإجابة", ownerUnknown: "لم يُعيّن مسؤول عن الإجابة بعد", conflictingObservations: "تتعارض المصادر — افتحوا الأدلة قبل الاعتماد على المعلومة",
      beamUnknown: "ينتظر مشهد الاتجاه موقعًا موثّقًا للمشروع وسمتًا موثّقًا للواجهة", beamScene: "إلى أين تتجه هذه الواجهة", projectHere: "المشروع", exposureUnknown: "اتجاه الواجهة غير موثّق بعد", beamUnknownBody: "تبقى الخريطة حيادية إلى أن يُوثّق موقع المشروع وسمت الواجهة. لا نرسم مخروطًا أو معلمًا بالتخمين.", beamIllustrativeCaveat: "وسيلة توضيحية للاتجاه؛ اطلبوا مخطط الاتجاه وحزمة المشاهد الموقّعة قبل الاعتماد عليها.", directionUnknown: "الاتجاه غير موثّق", viewContradictory: "أدلة المشهد متعارضة", viewUnknown: "سياق المشهد غير موثّق", exposures: "اتجاهات الواجهة", requestEvidence: "اعرفوا ما الذي يجب توثيقه",
      rentableArea: "المساحة القابلة للتأجير", planningCapacity: "السعة التخطيطية", people: "أشخاص", allInCost: "التكلفة الشهرية الشاملة", backToBuilding: "العودة إلى المبنى", selectedOffice: "مساحة المكتب التي اخترتموها", unidentifiedAsset: "المساحة المختارة", evidenceTools: "طرق لفهم هذه المساحة", floorPack: "افتحوا حزمة الطابق", floorPackBody: "شاهدوا المخطط والمساحة المقاسة والنواة ووثائق المصدر", fitOut: "استكشفوا التجهيز والبنية التحتية", fitOutBody: "شاهدوا السعة والأنظمة والاتصالات وشروط التسليم", context: "استكشفوا الوصول والمنطقة", contextBody: "افحصوا المسارات والحياة اليومية والسوق والمخاطر مع المصادر", cost: "افهموا تكلفة الإشغال الكاملة", costBody: "شاهدوا الإيجار والرسوم والمقارنات والسجلات الداعمة", actions: "إجراءات المساحة", save: "احفظوا المساحة", compare: "قارنوا المساحات", share: "شاركوا المساحة", askAbout: "اسألونا عن", thisSpace: "هذه المساحة", inquiry: "كوّنوا حزمة أسئلة", back: "عودة",
      noFloorPack: "لم تُرفق حزمة طابق موثّقة بعد.", requestFloorPack: "اطلبوا حزمة الطابق الموثّقة", notVerified: "غير موثّق بعد — أضيفوه إلى الأسئلة", contextAdapterRequired: "تحتاج طبقة الموقع الموثّقة إلى موصّل الخريطة المعتمد قبل عرضها.", requestContextPack: "اطلبوا حزمة الموقع والوصول الموثّقة", costUnknown: "لم يُتحقق من الجدول التجاري الكامل لهذه المساحة.", requestTerms: "اطلبوا الجدول التجاري الكامل", compareHelp: "اختاروا مساحة أخرى موثقة بالمصادر لمقارنة الحقائق جنبًا إلى جنب.", inquiryHelp: "اختاروا الأسئلة والوثائق؛ وسيرد المسار التجاري المسؤول.", modelRegion: "مبنى تفاعلي واختيار الطابق", decisionRegion: "حقائق وأدوات قرار للمساحة المختارة",
      network: "عبر المسار", straightLine: "بخط مستقيم", noRoute: "لم يُحسب المسار", openSource: "افتحوا المصدر الداعم", notCalculated: "لم يُحسب", modeLabel: "استكشفوا المنطقة حسب الموضوع", mapLabel: "خريطة سياق المشروع مع المصادر", caveat: "أزمنة الرحلة نطاقات. تُعرض وسائل النقل العاملة والمخططة منفصلة.", mapUnavailable: "الخريطة التفاعلية غير متاحة", mapFallback: "تبقى بطاقات الأماكن والمسارات الموثقة بالمصادر متاحة.", noEvidence: "لا توجد أدلة حديثة موثقة بالمصادر في هذا العرض", askForLayer: "اطلبوا طبقة السياق هذه", results: "النتائج", page: "الصفحة", pagination: "صفحات نتائج المنطقة", previous: "السابق", next: "التالي",
      selectedContext: "المساحة المختارة", questionsTitle: "ما الذي يساعدكم على اتخاذ القرار؟", questions: "أسئلة للحصول على إجابات", documents: "وثائق لاستلامها", otherQuestion: "ما الذي تريدون من الفريق التحقق منه أيضًا؟", continue: "تابعوا إلى بيانات الاتصال", contactTitle: "إلى أين نرسل الإجابة الكاملة؟", companyName: "الشركة", contactName: "اسم جهة الاتصال", email: "البريد الإلكتروني", internationalPhone: "هاتف دولي", headcount: "عدد الموظفين المخطط", moveIn: "موعد الانتقال المستهدف (YYYY-MM)", privacyConsent: "أوافق على إشعار الخصوصية لمعالجة هذا الطلب", termsConsent: "أوافق على شروط الطلب", marketingConsent: "أرسلوا تحديثات مفيدة عن المشروع (اختياري)", send: "أرسلوا حزمة أسئلتي ووثائقي", chooseOne: "اختاروا سؤالًا أو وثيقة أو اكتبوا طلبكم.", contactRequired: "أضيفوا بريدًا إلكترونيًا أو رقم هاتف دوليًا.", secureRetryUnavailable: "الإرسال الآمن غير متاح. أبقوا النافذة مفتوحة وحاولوا ثانية.", sending: "نرسل أسئلتكم المختارة…", retryPreserved: "لم يُحذف شيء. راجعوا وحاولوا ثانية؛ مفتاح الطلب نفسه يمنع إنشاء حالة ثانية.", received: "وصل طلبكم إلى المسار التجاري المسؤول", caseId: "رقم الحالة", recipient: "المسار المسؤول", commercialTeam: "فريق الرد التجاري", sla: "الوقت المستهدف للرد", hours: "ساعات", safeConfirmation: "لحماية الخصوصية، لا يكشف هذا التأكيد صندوق بريد خاصًا أو هوية موظف.",
      fitOutTopics: { capacity: "السعة", hvac: "التكييف والتهوية", power_backup: "الكهرباء والاحتياط", fiber: "اتصال الألياف", lifts_loading: "المصاعد والتحميل", accessibility: "مسار مهيأ" },
      status: { unknown: "التوافر غير موثّق", verified_available: "متاح وموثّق", soft_hold: "حجز مبدئي", under_offer: "قيد العرض", under_loi: "قيد خطاب النوايا", leased: "مؤجّر", delivered: "تم التسليم", unavailable: "غير متاح", not_marketed: "غير مطروح" },
      evidenceStates: { unknown: "غير معروف", source_estimate: "تقدير بمصدر", verified: "موثّق", contradictory: "مصادر متعارضة" },
      states: { unknown: "غير معروف", source_estimate: "تقدير بمصدر", verified: "موثّق", contradictory: "مصادر متعارضة" },
      modes: { commute: "الوصول", daily_life: "الحياة اليومية", business: "خدمات الأعمال", market: "السوق", risk: "المخاطر" },
      routeKinds: { project_team: "فريق المشروع المسؤول", commercial_desk: "المكتب التجاري المسؤول" },
      rfpQuestions: { live_availability: "ما الطوابق والوحدات المتاحة فعلًا الآن؟", asking_rent: "ما الإيجار المطلوب وجدول الرسوم الحالي؟", net_to_gross: "كيف تُقاس نسبة الصافي إلى الإجمالي؟", power_capacity: "ما قدرة الكهرباء والاحتياط والتبريد الملتزم بها؟", commute_and_transport: "ما خيارات الوصول والنقل الموثقة بالمصادر؟", nearby_facilities: "ما المرافق اليومية العاملة بالقرب من المشروع؟" },
      rfpDocuments: { availability_schedule: "جدول توافر مؤرخ", floor_plan_pdf: "مخطط الطابق PDF", measurement_report: "تقرير القياس", tenant_technical_manual: "الدليل الفني للمستأجر", orientation_plan: "مخطط اتجاه موقّع", lease_draft: "مسودة عقد أو رؤوس شروط" }
    }
  };

  var rfpAdditions = {
    en: {
      stepProgress: "Step {current} of {total}",
      questionsStepTitle: "Choose the questions the team must answer",
      documentsStepTitle: "Choose the documents you want to receive",
      requirementsTitle: "Timing and team size",
      reviewTitle: "Review consent and send",
      projectLabel: "Project", buildingLabel: "Building", towerLabel: "Tower", floorLabel: "Floor", suiteLabel: "Suite",
      sandboxTestSink: "Sandbox test sink - no message delivered",
      intentChanged: "Your edits are preserved. Confirm them as a new request before sending.",
      useChangesAsNewIntent: "Use my edits as a new request",
      newIntentReady: "Your fields are preserved. The next send will use a new request key.",
      consentUpdated: "The consent text was updated. Review and accept it before sending.",
      questionTextLimit: "Up to {max} characters; the complete text stays visible.",
      questionsPagination: "Question pages", questionPageStatus: "Questions {start}-{end} of {total}",
      writeOtherQuestion: "Write another question", backToQuestionChoices: "Back to the question choices",
      documentsPagination: "Document pages", documentPageStatus: "Documents {start}-{end} of {total}",
      rfpQuestionShort: {
        live_availability: "Availability", asking_rent: "Rent & charges", net_to_gross: "Area method",
        power_capacity: "Power & cooling", commute_and_transport: "Commute", nearby_facilities: "Nearby services"
      },
      rfpDocumentShort: {
        availability_schedule: "Availability list", floor_plan_pdf: "Floor plan", measurement_report: "Measurement",
        tenant_technical_manual: "Technical manual", orientation_plan: "Orientation plan", lease_draft: "Lease terms"
      },
      rfpErrors: {
        consent_expired: "The consent text changed while this request was open. Your fields are preserved.",
        invalid_field: "One field needs review. Nothing else was cleared.",
        rate_limited: "Too many requests reached the service. Your unchanged request is preserved.",
        rate_limited_wait: "Too many requests reached the service. Retry the unchanged request after about {seconds} seconds.",
        route_unavailable: "The responsible route is temporarily unavailable. Your unchanged request is preserved.",
        conflict: "This request key conflicts with a previous payload. Check whether a case exists, then explicitly start a new request intent.",
        network: "The connection did not confirm delivery. Nothing was cleared; retry sends the exact same request and key.",
        consent_refresh_unavailable: "The updated consent could not be loaded. Your entered fields remain here."
      },
      rfpRecoveryActions: {
        review_consent: "Review updated consent", fix_field: "Review this field",
        new_intent: "Start a new request intent", retry: "Retry the unchanged request"
      }
    },
    he: {
      stepProgress: "שלב {current} מתוך {total}",
      questionsStepTitle: "בחרו את השאלות שעליהן הצוות חייב לענות",
      documentsStepTitle: "בחרו את המסמכים שתרצו לקבל",
      requirementsTitle: "לוח זמנים וגודל הצוות",
      reviewTitle: "בדקו את ההסכמות ושלחו",
      projectLabel: "פרויקט", buildingLabel: "בניין", towerLabel: "מגדל", floorLabel: "קומה", suiteLabel: "שטח",
      sandboxTestSink: "יעד בדיקה בארגז החול - לא נשלחה הודעה",
      intentChanged: "השינויים נשמרו. אשרו אותם כבקשה חדשה לפני השליחה.",
      useChangesAsNewIntent: "השתמשו בשינויים כבקשה חדשה",
      newIntentReady: "כל השדות נשמרו. השליחה הבאה תשתמש במפתח בקשה חדש.",
      consentUpdated: "נוסח ההסכמה עודכן. בדקו ואשרו אותו לפני השליחה.",
      questionTextLimit: "עד {max} תווים; כל הטקסט נשאר גלוי.",
      questionsPagination: "עמודי שאלות", questionPageStatus: "שאלות {start}–{end} מתוך {total}",
      writeOtherQuestion: "כתבו שאלה נוספת", backToQuestionChoices: "חזרה לבחירת השאלות",
      documentsPagination: "עמודי מסמכים", documentPageStatus: "מסמכים {start}–{end} מתוך {total}",
      rfpQuestionShort: {
        live_availability: "זמינות", asking_rent: "שכירות וחיובים", net_to_gross: "שיטת שטח",
        power_capacity: "חשמל וקירור", commute_and_transport: "הגעה", nearby_facilities: "שירותים קרובים"
      },
      rfpDocumentShort: {
        availability_schedule: "רשימת זמינות", floor_plan_pdf: "תוכנית קומה", measurement_report: "מדידה",
        tenant_technical_manual: "מדריך טכני", orientation_plan: "תוכנית כיוונים", lease_draft: "תנאי שכירות"
      },
      rfpErrors: {
        consent_expired: "נוסח ההסכמה השתנה בזמן שהבקשה הייתה פתוחה. כל השדות נשמרו.",
        invalid_field: "צריך לבדוק שדה אחד. שום דבר אחר לא נמחק.",
        rate_limited: "השירות קיבל יותר מדי בקשות. הבקשה שלא השתנתה נשמרה.",
        rate_limited_wait: "השירות קיבל יותר מדי בקשות. נסו שוב את אותה בקשה בעוד כ-{seconds} שניות.",
        route_unavailable: "מסלול המענה האחראי אינו זמין כרגע. הבקשה שלא השתנתה נשמרה.",
        conflict: "מפתח הבקשה מתנגש עם תוכן קודם. בדקו אם כבר נפתחה פנייה ואז פתחו במפורש כוונת בקשה חדשה.",
        network: "החיבור לא אישר שהבקשה נמסרה. דבר לא נמחק; ניסיון חוזר שולח בדיוק את אותה בקשה ואותו מפתח.",
        consent_refresh_unavailable: "לא ניתן לטעון את נוסח ההסכמה המעודכן. כל השדות שהוזנו נשארו כאן."
      },
      rfpRecoveryActions: {
        review_consent: "בדקו את ההסכמה המעודכנת", fix_field: "בדקו את השדה",
        new_intent: "פתחו כוונת בקשה חדשה", retry: "נסו שוב את אותה בקשה"
      }
    },
    fr: {
      stepProgress: "Étape {current} sur {total}",
      questionsStepTitle: "Choisissez les questions auxquelles l’équipe doit répondre",
      documentsStepTitle: "Choisissez les documents à recevoir",
      requirementsTitle: "Calendrier et taille de l’équipe",
      reviewTitle: "Vérifier les consentements et envoyer",
      projectLabel: "Projet", buildingLabel: "Bâtiment", towerLabel: "Tour", floorLabel: "Étage", suiteLabel: "Lot",
      sandboxTestSink: "Destination de test sandbox - aucun message envoyé",
      intentChanged: "Vos modifications sont conservées. Confirmez-les comme nouvelle demande avant l’envoi.",
      useChangesAsNewIntent: "Utiliser mes modifications comme nouvelle demande",
      newIntentReady: "Vos champs sont conservés. Le prochain envoi utilisera une nouvelle clé de demande.",
      consentUpdated: "Le texte de consentement a été mis à jour. Vérifiez-le et acceptez-le avant l’envoi.",
      questionTextLimit: "{max} caractères maximum ; tout le texte reste visible.",
      questionsPagination: "Pages de questions", questionPageStatus: "Questions {start}–{end} sur {total}",
      writeOtherQuestion: "Écrire une autre question", backToQuestionChoices: "Retour au choix des questions",
      documentsPagination: "Pages de documents", documentPageStatus: "Documents {start}–{end} sur {total}",
      rfpQuestionShort: {
        live_availability: "Disponibilité", asking_rent: "Loyer et charges", net_to_gross: "Méthode de surface",
        power_capacity: "Énergie et froid", commute_and_transport: "Trajets", nearby_facilities: "Services proches"
      },
      rfpDocumentShort: {
        availability_schedule: "Liste disponible", floor_plan_pdf: "Plan d’étage", measurement_report: "Mesurage",
        tenant_technical_manual: "Manuel technique", orientation_plan: "Plan d’orientation", lease_draft: "Conditions du bail"
      },
      rfpErrors: {
        consent_expired: "Le texte de consentement a changé pendant l’ouverture de la demande. Vos champs sont conservés.",
        invalid_field: "Un champ doit être vérifié. Rien d’autre n’a été effacé.",
        rate_limited: "Le service a reçu trop de demandes. Votre demande inchangée est conservée.",
        rate_limited_wait: "Le service a reçu trop de demandes. Réessayez la demande inchangée dans environ {seconds} secondes.",
        route_unavailable: "Le circuit responsable est temporairement indisponible. Votre demande inchangée est conservée.",
        conflict: "Cette clé entre en conflit avec un contenu antérieur. Vérifiez si un dossier existe, puis démarrez explicitement une nouvelle intention.",
        network: "La connexion n’a pas confirmé la livraison. Rien n’a été effacé ; un nouvel essai renvoie exactement la même demande et la même clé.",
        consent_refresh_unavailable: "Le consentement actualisé n’a pas pu être chargé. Les champs saisis restent ici."
      },
      rfpRecoveryActions: {
        review_consent: "Vérifier le consentement actualisé", fix_field: "Vérifier ce champ",
        new_intent: "Démarrer une nouvelle intention", retry: "Réessayer la demande inchangée"
      }
    },
    ru: {
      stepProgress: "Шаг {current} из {total}",
      questionsStepTitle: "Выберите вопросы, на которые должна ответить команда",
      documentsStepTitle: "Выберите документы, которые хотите получить",
      requirementsTitle: "Сроки и размер команды",
      reviewTitle: "Проверьте согласия и отправьте",
      projectLabel: "Проект", buildingLabel: "Здание", towerLabel: "Башня", floorLabel: "Этаж", suiteLabel: "Блок",
      sandboxTestSink: "Тестовый приёмник песочницы - сообщение не отправлено",
      intentChanged: "Изменения сохранены. Перед отправкой подтвердите их как новый запрос.",
      useChangesAsNewIntent: "Использовать изменения как новый запрос",
      newIntentReady: "Все поля сохранены. При следующей отправке будет создан новый ключ запроса.",
      consentUpdated: "Текст согласия обновлён. Проверьте и примите его перед отправкой.",
      questionTextLimit: "До {max} знаков; весь текст остаётся видимым.",
      questionsPagination: "Страницы вопросов", questionPageStatus: "Вопросы {start}–{end} из {total}",
      writeOtherQuestion: "Написать другой вопрос", backToQuestionChoices: "Вернуться к выбору вопросов",
      documentsPagination: "Страницы документов", documentPageStatus: "Документы {start}–{end} из {total}",
      rfpQuestionShort: {
        live_availability: "Доступность", asking_rent: "Аренда и сборы", net_to_gross: "Метод площади",
        power_capacity: "Энергия и холод", commute_and_transport: "Маршруты", nearby_facilities: "Услуги рядом"
      },
      rfpDocumentShort: {
        availability_schedule: "Список площадей", floor_plan_pdf: "План этажа", measurement_report: "Обмеры",
        tenant_technical_manual: "Техруководство", orientation_plan: "План ориентации", lease_draft: "Условия аренды"
      },
      rfpErrors: {
        consent_expired: "Текст согласия изменился, пока запрос был открыт. Все поля сохранены.",
        invalid_field: "Нужно проверить одно поле. Остальные данные не удалены.",
        rate_limited: "Сервис получил слишком много запросов. Неизменённый запрос сохранён.",
        rate_limited_wait: "Сервис получил слишком много запросов. Повторите неизменённый запрос примерно через {seconds} секунд.",
        route_unavailable: "Ответственный маршрут временно недоступен. Неизменённый запрос сохранён.",
        conflict: "Ключ запроса конфликтует с прежним содержимым. Проверьте, создано ли обращение, затем явно начните новый запрос.",
        network: "Соединение не подтвердило доставку. Данные не удалены; повтор отправит точно тот же запрос с тем же ключом.",
        consent_refresh_unavailable: "Не удалось загрузить обновлённое согласие. Введённые поля остаются на месте."
      },
      rfpRecoveryActions: {
        review_consent: "Проверить обновлённое согласие", fix_field: "Проверить это поле",
        new_intent: "Начать новый запрос", retry: "Повторить неизменённый запрос"
      }
    },
    ar: {
      stepProgress: "الخطوة {current} من {total}",
      questionsStepTitle: "اختاروا الأسئلة التي يجب على الفريق الإجابة عنها",
      documentsStepTitle: "اختاروا الوثائق التي تريدون استلامها",
      requirementsTitle: "الجدول الزمني وحجم الفريق",
      reviewTitle: "راجعوا الموافقات ثم أرسلوا",
      projectLabel: "المشروع", buildingLabel: "المبنى", towerLabel: "البرج", floorLabel: "الطابق", suiteLabel: "المساحة",
      sandboxTestSink: "وجهة اختبار في صندوق الرمل - لم تُرسل أي رسالة",
      intentChanged: "تم حفظ التعديلات. أكدوها كطلب جديد قبل الإرسال.",
      useChangesAsNewIntent: "استخدام تعديلاتي كطلب جديد",
      newIntentReady: "تم حفظ جميع الحقول. سيستخدم الإرسال التالي مفتاح طلب جديدًا.",
      consentUpdated: "تم تحديث نص الموافقة. راجعوه ووافقوا عليه قبل الإرسال.",
      questionTextLimit: "حتى {max} حرفًا؛ يبقى النص كاملًا ظاهرًا.",
      questionsPagination: "صفحات الأسئلة", questionPageStatus: "الأسئلة {start}–{end} من {total}",
      writeOtherQuestion: "اكتبوا سؤالًا آخر", backToQuestionChoices: "العودة إلى خيارات الأسئلة",
      documentsPagination: "صفحات الوثائق", documentPageStatus: "الوثائق {start}–{end} من {total}",
      rfpQuestionShort: {
        live_availability: "التوافر", asking_rent: "الإيجار والرسوم", net_to_gross: "طريقة المساحة",
        power_capacity: "الطاقة والتبريد", commute_and_transport: "الوصول", nearby_facilities: "خدمات قريبة"
      },
      rfpDocumentShort: {
        availability_schedule: "قائمة التوافر", floor_plan_pdf: "مخطط الطابق", measurement_report: "القياس",
        tenant_technical_manual: "الدليل الفني", orientation_plan: "مخطط الاتجاه", lease_draft: "شروط الإيجار"
      },
      rfpErrors: {
        consent_expired: "تغيّر نص الموافقة أثناء فتح الطلب. تم حفظ جميع الحقول.",
        invalid_field: "يحتاج حقل واحد إلى المراجعة. لم يُحذف أي شيء آخر.",
        rate_limited: "تلقى النظام عددًا كبيرًا من الطلبات. تم حفظ الطلب دون تغيير.",
        rate_limited_wait: "تلقى النظام عددًا كبيرًا من الطلبات. أعيدوا إرسال الطلب نفسه بعد نحو {seconds} ثانية.",
        route_unavailable: "مسار الرد المسؤول غير متاح مؤقتًا. تم حفظ الطلب دون تغيير.",
        conflict: "يتعارض مفتاح الطلب مع محتوى سابق. تحققوا من وجود حالة ثم ابدؤوا طلبًا جديدًا بشكل صريح.",
        network: "لم يؤكد الاتصال التسليم. لم يُحذف شيء؛ تعيد المحاولة إرسال الطلب نفسه تمامًا وبالمفتاح نفسه.",
        consent_refresh_unavailable: "تعذر تحميل الموافقة المحدثة. تبقى جميع الحقول المدخلة هنا."
      },
      rfpRecoveryActions: {
        review_consent: "مراجعة الموافقة المحدثة", fix_field: "مراجعة هذا الحقل",
        new_intent: "بدء طلب جديد", retry: "إعادة إرسال الطلب نفسه"
      }
    }
  };

  /*
   * Context-map strings are a separate complete shape so every render-time
   * fallback is resolved by the active locale; no normalization step freezes
   * English copy into a record before rendering.
   */
  var contextMapAdditions = {
    en: {
      operatingState: "Operating state", stage: "Stage", expected: "Expected",
      expectedUnknown: "Expected timing not supplied", projectedTravel: "Projected travel",
      closedServiceTravel: "Reference travel while service is closed",
      historicalTravel: "Historical/reference travel", unknownStateTravel: "Travel applicability not verified",
      mapFocusUnavailable: "Map focus unavailable", openSourceRecord: "Open source record",
      sourceNotLinked: "Source reference is not linked", transfers: "transfers", minutesShort: "min", metresShort: "m",
      estimateCaveat: "Source estimate only; confirm current conditions before relying on it.",
      evidenceCaveat: "Evidence applies to the stated scope and date; confirm current conditions before relying on it.",
      operatingStates: {
        operating: "Operating", under_construction: "Under construction", planned: "Planned",
        temporarily_closed: "Temporarily closed", closed: "Closed", unknown: "Not verified"
      },
      travelModes: { walk: "Walk", transit: "Public transport", bike: "Bicycle", drive: "Drive" },
      categories: {
        rail: "Rail", bus: "Bus", metro: "Metro", light_rail: "Light rail", food: "Food",
        pharmacy: "Pharmacy", medical: "Medical", gym: "Gym", parking: "Parking", hotel: "Hotel",
        airport: "Airport", office: "Business service", market: "Market evidence", risk: "Local risk"
      }
    },
    he: {
      operatingState: "מצב תפעולי", stage: "שלב", expected: "צפוי",
      expectedUnknown: "מועד צפוי לא נמסר", projectedTravel: "זמן נסיעה חזוי",
      closedServiceTravel: "זמן נסיעה לייחוס בזמן שהשירות סגור",
      historicalTravel: "זמן נסיעה היסטורי או לייחוס", unknownStateTravel: "תחולת זמן הנסיעה לא אומתה",
      mapFocusUnavailable: "לא ניתן למקד את המפה", openSourceRecord: "פתחו את רשומת המקור",
      sourceNotLinked: "ההפניה למקור אינה מקושרת", transfers: "החלפות", minutesShort: "דק׳", metresShort: "מ׳",
      estimateCaveat: "זו הערכה ממקור בלבד; יש לאמת את התנאים העדכניים לפני הסתמכות.",
      evidenceCaveat: "הראיות חלות על ההיקף והתאריך המוצגים; יש לאמת תנאים עדכניים לפני הסתמכות.",
      operatingStates: {
        operating: "פעיל", under_construction: "בביצוע", planned: "מתוכנן",
        temporarily_closed: "סגור זמנית", closed: "סגור", unknown: "לא אומת"
      },
      travelModes: { walk: "הליכה", transit: "תחבורה ציבורית", bike: "אופניים", drive: "נהיגה" },
      categories: {
        rail: "רכבת", bus: "אוטובוס", metro: "מטרו", light_rail: "רכבת קלה", food: "מזון",
        pharmacy: "בית מרקחת", medical: "רפואה", gym: "חדר כושר", parking: "חניה", hotel: "מלון",
        airport: "נמל תעופה", office: "שירות עסקי", market: "נתוני שוק", risk: "סיכון מקומי"
      }
    },
    fr: {
      operatingState: "État de fonctionnement", stage: "Étape", expected: "Prévu",
      expectedUnknown: "Calendrier prévisionnel non fourni", projectedTravel: "Trajet prévisionnel",
      closedServiceTravel: "Trajet de référence pendant la fermeture du service",
      historicalTravel: "Trajet historique ou de référence", unknownStateTravel: "Applicabilité du trajet non vérifiée",
      mapFocusUnavailable: "Centrage de la carte indisponible", openSourceRecord: "Ouvrir la fiche source",
      sourceNotLinked: "La référence source n’est pas liée", transfers: "correspondances", minutesShort: "min", metresShort: "m",
      estimateCaveat: "Estimation issue d’une source uniquement ; confirmez les conditions actuelles avant de vous y fier.",
      evidenceCaveat: "La preuve vaut pour le périmètre et la date indiqués ; confirmez les conditions actuelles avant de vous y fier.",
      operatingStates: {
        operating: "En service", under_construction: "En construction", planned: "Planifié",
        temporarily_closed: "Fermé temporairement", closed: "Fermé", unknown: "Non vérifié"
      },
      travelModes: { walk: "À pied", transit: "Transports publics", bike: "Vélo", drive: "Voiture" },
      categories: {
        rail: "Train", bus: "Bus", metro: "Métro", light_rail: "Tramway", food: "Restauration",
        pharmacy: "Pharmacie", medical: "Santé", gym: "Salle de sport", parking: "Stationnement", hotel: "Hôtel",
        airport: "Aéroport", office: "Service aux entreprises", market: "Donnée de marché", risk: "Risque local"
      }
    },
    ru: {
      operatingState: "Статус работы", stage: "Этап", expected: "Ожидаемый срок",
      expectedUnknown: "Ожидаемый срок не указан", projectedTravel: "Расчётное время в пути",
      closedServiceTravel: "Справочное время в пути при закрытом сервисе",
      historicalTravel: "Историческое или справочное время", unknownStateTravel: "Применимость маршрута не подтверждена",
      mapFocusUnavailable: "Фокусировка карты недоступна", openSourceRecord: "Открыть запись источника",
      sourceNotLinked: "Ссылка на источник не подключена", transfers: "пересадки", minutesShort: "мин", metresShort: "м",
      estimateCaveat: "Это только оценка по источнику; перед решением подтвердите текущие условия.",
      evidenceCaveat: "Данные относятся к указанным охвату и дате; перед решением подтвердите текущие условия.",
      operatingStates: {
        operating: "Работает", under_construction: "Строится", planned: "Запланировано",
        temporarily_closed: "Временно закрыто", closed: "Закрыто", unknown: "Не подтверждено"
      },
      travelModes: { walk: "Пешком", transit: "Общественный транспорт", bike: "Велосипед", drive: "Автомобиль" },
      categories: {
        rail: "Железная дорога", bus: "Автобус", metro: "Метро", light_rail: "Легкорельсовый транспорт", food: "Питание",
        pharmacy: "Аптека", medical: "Медицина", gym: "Спортзал", parking: "Парковка", hotel: "Гостиница",
        airport: "Аэропорт", office: "Деловой сервис", market: "Рыночные данные", risk: "Локальный риск"
      }
    },
    ar: {
      operatingState: "حالة التشغيل", stage: "المرحلة", expected: "الموعد المتوقع",
      expectedUnknown: "لم يُذكر التوقيت المتوقع", projectedTravel: "زمن رحلة متوقع",
      closedServiceTravel: "زمن رحلة مرجعي أثناء إغلاق الخدمة",
      historicalTravel: "زمن رحلة تاريخي أو مرجعي", unknownStateTravel: "لم يتم التحقق من انطباق زمن الرحلة",
      mapFocusUnavailable: "تعذر تركيز الخريطة", openSourceRecord: "افتحوا سجل المصدر",
      sourceNotLinked: "مرجع المصدر غير مرتبط", transfers: "تبديلات", minutesShort: "د", metresShort: "م",
      estimateCaveat: "هذا تقدير من مصدر فقط؛ تحققوا من الظروف الحالية قبل الاعتماد عليه.",
      evidenceCaveat: "تنطبق الأدلة على النطاق والتاريخ المعروضين؛ تحققوا من الظروف الحالية قبل الاعتماد عليها.",
      operatingStates: {
        operating: "قيد التشغيل", under_construction: "قيد الإنشاء", planned: "مخطط",
        temporarily_closed: "مغلق مؤقتًا", closed: "مغلق", unknown: "غير متحقق"
      },
      travelModes: { walk: "مشي", transit: "نقل عام", bike: "دراجة", drive: "سيارة" },
      categories: {
        rail: "قطار", bus: "حافلة", metro: "مترو", light_rail: "قطار خفيف", food: "طعام",
        pharmacy: "صيدلية", medical: "رعاية صحية", gym: "نادي رياضي", parking: "موقف سيارات", hotel: "فندق",
        airport: "مطار", office: "خدمة أعمال", market: "بيانات السوق", risk: "مخاطر محلية"
      }
    }
  };

  var beamAdditions = {
    en: {
      exposureCone: "Evidenced facade sector",
      northUpSchematic: "North-up schematic from evidenced project and landmark coordinates",
      beamEvidenceTitle: "Orientation sources",
      projectAnchor: "Project anchor",
      source: "Source",
      allSources: "All sources",
      documentId: "Document",
      requestSource: "Request this source record",
      illustrativeBadge: "Illustrative",
      methodsCount: "{count} methods",
      distanceMethodsShort: {
        straight_line_geodesic: "Geodesic",
        routed_walking: "Walking route",
        routed_cycling: "Cycling route",
        routed_driving: "Driving route",
        routed_transit: "Transit route"
      },
      distanceMethods: {
        straight_line_geodesic: "Straight-line geodesic distance",
        routed_walking: "Sourced walking-route distance",
        routed_cycling: "Sourced cycling-route distance",
        routed_driving: "Sourced driving-route distance",
        routed_transit: "Sourced public-transport route distance"
      }
    },
    he: {
      exposureCone: "גזרת חזית מגובה בראיות",
      northUpSchematic: "תרשים מוצפן לצפון לפי קואורדינטות הפרויקט ונקודות הציון שבמקורות",
      beamEvidenceTitle: "מקורות הכיוון",
      projectAnchor: "עוגן הפרויקט",
      source: "מקור",
      allSources: "כל המקורות",
      documentId: "מסמך",
      requestSource: "בקשו את רשומת המקור הזאת",
      illustrativeBadge: "להמחשה",
      methodsCount: "{count} שיטות",
      distanceMethodsShort: {
        straight_line_geodesic: "גאודטי",
        routed_walking: "מסלול הליכה",
        routed_cycling: "מסלול אופניים",
        routed_driving: "מסלול נסיעה",
        routed_transit: "מסלול תחבורה"
      },
      distanceMethods: {
        straight_line_geodesic: "מרחק גאודטי בקו ישר",
        routed_walking: "מרחק במסלול הליכה עם מקור",
        routed_cycling: "מרחק במסלול אופניים עם מקור",
        routed_driving: "מרחק במסלול נסיעה עם מקור",
        routed_transit: "מרחק במסלול תחבורה ציבורית עם מקור"
      }
    },
    fr: {
      exposureCone: "Secteur de façade étayé",
      northUpSchematic: "Schéma orienté nord fondé sur les coordonnées sourcées du projet et des repères",
      beamEvidenceTitle: "Sources d’orientation",
      projectAnchor: "Point du projet",
      source: "Source",
      allSources: "Toutes les sources",
      documentId: "Document",
      requestSource: "Demander cette source",
      illustrativeBadge: "Indicatif",
      methodsCount: "{count} méthodes",
      distanceMethodsShort: {
        straight_line_geodesic: "Géodésique",
        routed_walking: "Trajet à pied",
        routed_cycling: "Trajet à vélo",
        routed_driving: "Trajet voiture",
        routed_transit: "Trajet transport"
      },
      distanceMethods: {
        straight_line_geodesic: "Distance géodésique en ligne droite",
        routed_walking: "Distance d’itinéraire à pied sourcée",
        routed_cycling: "Distance d’itinéraire à vélo sourcée",
        routed_driving: "Distance d’itinéraire en voiture sourcée",
        routed_transit: "Distance d’itinéraire en transports publics sourcée"
      }
    },
    ru: {
      exposureCone: "Подтверждённый сектор фасада",
      northUpSchematic: "Схема с севером вверху по подтверждённым координатам проекта и ориентиров",
      beamEvidenceTitle: "Источники ориентации",
      projectAnchor: "Точка проекта",
      source: "Источник",
      allSources: "Все источники",
      documentId: "Документ",
      requestSource: "Запросить эту запись источника",
      illustrativeBadge: "Схема",
      methodsCount: "Методов: {count}",
      distanceMethodsShort: {
        straight_line_geodesic: "Геодезическое",
        routed_walking: "Пеший маршрут",
        routed_cycling: "Веломаршрут",
        routed_driving: "Автомаршрут",
        routed_transit: "Общественный транспорт"
      },
      distanceMethods: {
        straight_line_geodesic: "Геодезическое расстояние по прямой",
        routed_walking: "Расстояние подтверждённого пешего маршрута",
        routed_cycling: "Расстояние подтверждённого веломаршрута",
        routed_driving: "Расстояние подтверждённого автомобильного маршрута",
        routed_transit: "Расстояние подтверждённого маршрута на общественном транспорте"
      }
    },
    ar: {
      exposureCone: "قطاع واجهة مدعوم بالأدلة",
      northUpSchematic: "مخطط شمالي مبني على إحداثيات موثقة للمشروع والمعالم",
      beamEvidenceTitle: "مصادر الاتجاه",
      projectAnchor: "مرساة المشروع",
      source: "مصدر",
      allSources: "كل المصادر",
      documentId: "مستند",
      requestSource: "اطلبوا سجل المصدر هذا",
      illustrativeBadge: "توضيحي",
      methodsCount: "{count} طرق",
      distanceMethodsShort: {
        straight_line_geodesic: "جيوديسية",
        routed_walking: "مسار مشي",
        routed_cycling: "مسار دراجات",
        routed_driving: "مسار قيادة",
        routed_transit: "مسار نقل عام"
      },
      distanceMethods: {
        straight_line_geodesic: "مسافة جيوديسية بخط مستقيم",
        routed_walking: "مسافة مسار مشي موثّق",
        routed_cycling: "مسافة مسار دراجات موثّق",
        routed_driving: "مسافة مسار قيادة موثّق",
        routed_transit: "مسافة مسار نقل عام موثّق"
      }
    }
  };

  /*
   * Short-landscape labels remain intentional localized copy, never CSS
   * truncation. The full curiosity-led door name remains the button's
   * accessible name; these compact variants are visible only when height is
   * constrained and are kept to a single concise buyer-recognizable concept.
   */
  var compactDoorAdditions = {
    en: { floorPackShort: "Floor pack", fitOutShort: "Fit-out", contextShort: "Area", costShort: "Full cost" },
    he: { floorPackShort: "חבילת קומה", fitOutShort: "תכנון", contextShort: "סביבה", costShort: "עלות מלאה" },
    fr: { floorPackShort: "Dossier étage", fitOutShort: "Aménagement", contextShort: "Quartier", costShort: "Coût complet" },
    ru: { floorPackShort: "Пакет этажа", fitOutShort: "Оснащение", contextShort: "Район", costShort: "Полная цена" },
    ar: { floorPackShort: "حزمة الطابق", fitOutShort: "التجهيز", contextShort: "المنطقة", costShort: "التكلفة الكاملة" }
  };

  SUPPORTED.forEach(function (locale) {
    Object.keys(rfpAdditions[locale]).forEach(function (key) {
      dictionaries[locale][key] = rfpAdditions[locale][key];
    });
    Object.keys(contextMapAdditions[locale]).forEach(function (key) {
      dictionaries[locale][key] = contextMapAdditions[locale][key];
    });
    Object.keys(beamAdditions[locale]).forEach(function (key) {
      dictionaries[locale][key] = beamAdditions[locale][key];
    });
    Object.keys(compactDoorAdditions[locale]).forEach(function (key) {
      dictionaries[locale][key] = compactDoorAdditions[locale][key];
    });
  });

  function isPlainObject(value) {
    return Boolean(value) && Object.prototype.toString.call(value) === "[object Object]";
  }

  function collectShape(value, prefix, output) {
    Object.keys(value).sort().forEach(function (key) {
      var path = prefix ? prefix + "." + key : key;
      if (isPlainObject(value[key])) collectShape(value[key], path, output);
      else output.push(path);
    });
    return output;
  }

  function validateDictionaries() {
    var canonicalShape = collectShape(dictionaries.en, "", []);
    SUPPORTED.forEach(function (locale) {
      var dictionary = dictionaries[locale];
      if (!dictionary || dictionary.locale !== locale) {
        throw new Error("Missing commercial dictionary: " + locale);
      }
      if (dictionary.dir !== (locale === "he" || locale === "ar" ? "rtl" : "ltr")) {
        throw new Error("Invalid commercial dictionary direction: " + locale);
      }
      var shape = collectShape(dictionary, "", []);
      if (shape.join("\n") !== canonicalShape.join("\n")) {
        throw new Error("Incomplete commercial dictionary: " + locale);
      }
      shape.forEach(function (path) {
        var cursor = dictionary;
        path.split(".").forEach(function (part) { cursor = cursor[part]; });
        if (typeof cursor !== "string" || !cursor.trim()) {
          throw new Error("Empty commercial translation: " + locale + "." + path);
        }
      });
    });
    return canonicalShape.slice();
  }

  function deepFreeze(value) {
    if (!isPlainObject(value)) return value;
    Object.keys(value).forEach(function (key) { deepFreeze(value[key]); });
    return Object.freeze(value);
  }

  function normalizeLocale(value) {
    var base = String(value || "en").toLowerCase().split(/[-_]/)[0];
    return SUPPORTED.indexOf(base) >= 0 ? base : "en";
  }

  var requiredKeys = validateDictionaries();
  SUPPORTED.forEach(function (locale) { deepFreeze(dictionaries[locale]); });

  window.NadlanCommercialI18n = Object.freeze({
    supported: SUPPORTED.slice(),
    requiredKeys: requiredKeys,
    get: function get(locale) {
      return dictionaries[normalizeLocale(locale)];
    },
    direction: function direction(locale) {
      return dictionaries[normalizeLocale(locale)].dir;
    },
    validate: validateDictionaries
  });
})(window);
