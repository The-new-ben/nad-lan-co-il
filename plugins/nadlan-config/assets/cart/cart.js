/* "הסל שלי" (HAD-796, package 4 of HAD-788; board https://claude.ai/artifact/CWRiuCvoeyxqS1ymeJAhkg).
 * One basket for every project and every language (he, en, fr, ru, ar), kept in this browser (localStorage 'nl-cart:v1').
 * Ways in, one store: the stage (nl:floor, nl:facing, nl:view), package 3's shell (nadlan:unit-picked, slot [data-nl-slot=basket]),
 * the showroom engine's "build me an offer" buttons ([data-act=rfp][data-id]), the Kikar showroom (window.__nlBasket), the designer
 * (package 2: nl:design and 'nl-cart-design:<project>:<unit>'), the rental plan (package 6: nadlan:rent-plan and 'nl-rent-plan:v1').
 * Steps like an order: the basket, 1 the summary, 2 the request for proposal (POST nadlan/v1/lead, then nadlan/v1/cart/order),
 * 3 the reservation (the order document, inc/cart.php: draft conditions, a lawyer gate, a SIMULATED deposit; no money moves).
 * Honesty: an example apartment is called one; prices are only what the buyer types; services carry no price; professionals are
 * real directory entries (Hebrew pages) or "we will recommend". Events for package 5: window.nlTrack (no personal data). */
(function () {
  'use strict';
  if (window.NLCart) return;
  const cfgEl = document.getElementById('nadlan-cart-cfg');
  if (!cfgEl) return;
  let C;
  try { C = JSON.parse(cfgEl.textContent); } catch (e) { return; }
  const P = C.project || null; // the project this page is about (null on any other page)
  const L = ['he', 'en', 'fr', 'ru', 'ar'].indexOf(C.lang) >= 0 ? C.lang : 'he';
  const RTL = L === 'he' || L === 'ar';

  /* ---------------------------------------------------------------- words */
  const D = {
    he: {
      name: 'הסל שלי', add: 'הוספת הדירה לסל', add_proj: 'הוספת הפרויקט לסל', in_cart: 'בסל', open: 'לסל שלי', count: 'פרויקטים בסל',
      kept: 'נשמר בדפדפן הזה. אפשר לאסוף דירות מכמה פרויקטים.', empty: 'הסל ריק. בחרו דירה במגדל, או הוסיפו את הפרויקט, והכל יחכה כאן.',
      unit: 'הדירה', example: 'דירה לדוגמה', unit_open: 'הדירה תיבחר עם היזם', floor: 'קומה', tower: 'מגדל', facing: 'פונה ל', rooms: 'חדרים', sqm: 'מ״ר',
      pick_hint: 'בחרו קומה במגדל שבדף, והדירה תתעדכן כאן.', change: 'שינוי', remove: 'הסרה מהסל', edit: 'עריכה',
      design: 'התכנון שלי', design_none: 'עוד לא תכננת. במעצב מזיזים קירות, בוחרים גימורים ומשאירים הערות לקבלן.', to_designer: 'למעצב הדירה',
      design_sum: '${rooms} חדרים · ${fin} גימורים · ${chg} שינויים · ${notes} הערות לקבלן', design_saved: 'תכנון שמור במעצב', style: 'סגנון בדירה לדוגמה',
      services: 'שירותים', services_sub: 'מה לצרף לבקשה. בלי מחיר ובלי התחייבות.',
      svc_mortgage: 'ייעוץ משכנתא', svc_mortgage_d: 'מסגרת מימון ואישור עקרוני', svc_lawyer: 'עורך דין מקרקעין', svc_lawyer_d: 'בדיקת חוזה המכר והבטוחות',
      svc_design: 'עיצוב פנים', svc_design_d: 'קונספט ותקציב לדירה הזו', svc_inspection: 'בדק בית ופיקוח', svc_inspection_d: 'בדיקת הדירה לפני המסירה',
      svc_moving: 'הובלה', svc_moving_d: 'הצעה להובלה ליום הכניסה', svc_rent: 'ניהול השכרה', svc_rent_d: 'כמה הדירה תכניס עד שתעברו',
      pro_pick: 'אנשי מקצוע מהמאגר (לא חובה)', pro_none: 'נבקש המלצה מהצוות', pro_chosen: 'נבחר', rent_calc: 'לחישוב ההכנסה מהשכרה',
      call: 'שיחה', call_sub: 'מתי נוח שהיזם והצוות יחזרו אליך? זו בקשה, לא פגישה שנקבעה.', call_none: 'עוד לא נבחר מועד', between: 'בין', and: 'ל־',
      ch_phone: 'טלפון', ch_video: 'וידאו', ch_wa: 'וואטסאפ', days: ['ראשון', 'שני', 'שלישי', 'רביעי', 'חמישי', 'שישי', 'שבת'],
      price: 'מחיר ומס רכישה', price_l: 'המחיר שקיבלת מהנציג (לא חובה)', b_single: 'דירה יחידה', b_additional: 'דירה נוספת', b_foreign: 'תושב/ת חוץ',
      tax: 'מס רכישה משוער', tax_note: 'לפי המדרגות בתוקף. אומדן, לא ייעוץ מס.', foreign_note: 'תושב חוץ משלם לפי מדרגות דירה נוספת מהשקל הראשון.', hint: 'מחיר שפורסם',
      to_summary: 'לסיכום ההזמנה', s1: 'סיכום', s2: 'בקשה להצעה', s3: 'שריון', summary: 'סיכום ההזמנה',
      not_incl: 'המחיר, המפרט והחוזה נקבעים מול היזם. נדל״ן מפרסמת את הפרויקט ומעבירה את הבקשה ליזם ולאנשי המקצוע שבחרת; היא אינה צד לעסקה ואינה גובה מהקונה דבר.',
      to_request: 'המשך לבקשה להצעה', f_name: 'שם מלא', f_phone: 'נייד או וואטסאפ', f_email: 'אימייל (לא חובה)',
      privacy: 'מסירת הפרטים היא לבחירתך; בלעדיהם לא נוכל להעביר את הבקשה. הפרטים יועברו אל היזם של ${project} ואל אנשי המקצוע שבחרת, כדי לענות לבקשה הזו בלבד. המפעיל: נדל״ן, nad-lan.co.il. זכותך לעיין בפרטים, לתקן אותם ולבקש מחיקה.',
      privacy_link: 'מדיניות הפרטיות', consent: 'אני מסכים/ה שהבקשה תועבר ליזם של ${project} ולאנשי המקצוע שבחרתי',
      send: 'שליחת הבקשה להצעה', sending: 'שולחים...', need: 'נא למלא שם ונייד, ולסמן את ההסכמה.', err: 'משהו לא עבר. נסו שוב בעוד רגע.',
      sent: 'הבקשה נשלחה', st_rfp: 'הבקשה נקלטה', st_next: 'היזם והצוות חוזרים אליך', st_offer: 'הצעה מסודרת לדירה הזו',
      doc: 'מסמך הבקשה (להדפסה ולשמירה)', to_reserve: 'להמשך: שריון הדירה', reserve_note: 'בשריון יש תנאים בטיוטה לעורך דין, עצירה לבדיקת עורך דין, ופיקדון לדוגמה בלבד. לא יחויב כסף.',
      ordered: 'נשלחה בקשה ${ref}', open_order: 'פתיחת ההזמנה',
      wa: 'שליחת הסל בוואטסאפ', room: 'לחדר צפייה משותף עם נציג', clear: 'ריקון הסל', close: 'סגירה', back: 'חזרה לסל',
      legal: 'הסל אינו רכישה והדירה לא נמכרת באתר. כל תשלום על הדירה, כשיהיה, רק ליזם לחשבון הליווי של הפרויקט.',
      wa_intro: 'שלום, בניתי סל ב${project} באתר nad-lan.co.il:', wa_close: 'אשמח לתוכניות, למחירים ולזמינות. זו בקשה למידע, לא הזמנה.', other: 'עוד בסל',
    },
    en: {
      name: 'My basket', add: 'Add this apartment', add_proj: 'Add the project', in_cart: 'In basket', open: 'My basket', count: 'projects in basket',
      kept: 'Kept in this browser. You can collect apartments from several projects.', empty: 'Your basket is empty. Pick an apartment on the tower, or add the project, and it waits here.',
      unit: 'The apartment', example: 'Example apartment', unit_open: 'Chosen with the developer', floor: 'Floor', tower: 'Tower', facing: 'Facing', rooms: 'rooms', sqm: 'sqm',
      pick_hint: 'Pick a floor on the tower on this page and the apartment updates here.', change: 'Change', remove: 'Remove', edit: 'Edit',
      design: 'My design', design_none: 'No design yet. In the designer you move walls, choose finishes and leave notes for the builder.', to_designer: 'Open the designer',
      design_sum: '${rooms} rooms · ${fin} finishes · ${chg} changes · ${notes} notes to the builder', design_saved: 'A design is saved in the designer', style: 'Style in the example apartment',
      services: 'Services', services_sub: 'What to add to the request. No price, no commitment.',
      svc_mortgage: 'Mortgage advice', svc_mortgage_d: 'Financing limit and approval in principle', svc_lawyer: 'Real estate lawyer', svc_lawyer_d: 'Sale contract and guarantees checked',
      svc_design: 'Interior design', svc_design_d: 'Concept and budget for this apartment', svc_inspection: 'Inspection and supervision', svc_inspection_d: 'The apartment checked before handover',
      svc_moving: 'Moving', svc_moving_d: 'A moving quote for the day you move in', svc_rent: 'Rental management', svc_rent_d: 'What it earns until you move in',
      pro_pick: 'Professionals from the directory (optional)', pro_none: 'We will recommend one', pro_chosen: 'Chosen', rent_calc: 'Work out the rental income',
      call: 'Call', call_sub: 'When should the developer and the team call you back? A request, not a booked meeting.', call_none: 'No time chosen yet', between: 'between', and: 'and',
      ch_phone: 'Phone', ch_video: 'Video', ch_wa: 'WhatsApp', days: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
      price: 'Price and purchase tax', price_l: 'The price the sales team gave you (optional)', b_single: 'Only home', b_additional: 'Additional home', b_foreign: 'Foreign resident',
      tax: 'Estimated purchase tax', tax_note: 'By the brackets in force. An estimate, not tax advice.', foreign_note: 'A foreign resident pays the additional-home brackets from the first shekel.', hint: 'Published price',
      to_summary: 'Order summary', s1: 'Summary', s2: 'Request', s3: 'Reserve', summary: 'Order summary',
      not_incl: 'Price, specification and contract are set with the developer. NadLan publishes the project and passes your request to the developer and the professionals you chose; it is not a party to the sale and charges the buyer nothing.',
      to_request: 'Continue to the request', f_name: 'Full name', f_phone: 'Mobile or WhatsApp', f_email: 'Email (optional)',
      privacy: 'Giving your details is your choice; without them we cannot pass the request on. They go to the developer of ${project} and to the professionals you chose, only to answer this request. Operator: NadLan, nad-lan.co.il. You may see, correct and ask to delete your details.',
      privacy_link: 'Privacy policy', consent: 'I agree that the request goes to the developer of ${project} and to the professionals I chose',
      send: 'Send request for proposal', sending: 'Sending...', need: 'Please fill in your name and mobile, and tick the consent.', err: 'Something did not go through. Please try again in a moment.',
      sent: 'Request sent', st_rfp: 'Request received', st_next: 'The developer and the team get back to you', st_offer: 'A proper offer for this apartment',
      doc: 'The request document (print or save)', to_reserve: 'Next: reserve the apartment', reserve_note: 'Reserving has draft conditions for a lawyer, a stop for a lawyer\'s review, and an example deposit only. No money is charged.',
      ordered: 'Request ${ref} sent', open_order: 'Open the order',
      wa: 'Send the basket on WhatsApp', room: 'Shared viewing room with a representative', clear: 'Empty the basket', close: 'Close', back: 'Back to basket',
      legal: 'The basket is not a purchase and the apartment is not sold on this site. Any payment for the apartment, when there is one, goes only to the developer\'s project escrow.',
      wa_intro: 'Hello, I built a basket for ${project} on nad-lan.co.il:', wa_close: 'I would like plans, prices and availability. This is a request for information, not an order.', other: 'Also in the basket',
    },
    fr: {
      name: 'Mon panier', add: 'Ajouter cet appartement', add_proj: 'Ajouter le projet', in_cart: 'Dans le panier', open: 'Mon panier', count: 'projets dans le panier',
      kept: 'Conservé dans ce navigateur. Vous pouvez réunir des appartements de plusieurs projets.', empty: 'Votre panier est vide. Choisissez un appartement sur la tour, ou ajoutez le projet.',
      unit: 'L’appartement', example: 'Appartement exemple', unit_open: 'Choisi avec le promoteur', floor: 'Étage', tower: 'Tour', facing: 'Orienté', rooms: 'pièces', sqm: 'm²',
      pick_hint: 'Choisissez un étage sur la tour de la page, l’appartement se met à jour ici.', change: 'Modifier', remove: 'Retirer', edit: 'Modifier',
      design: 'Mon aménagement', design_none: 'Pas encore d’aménagement. Dans l’outil, on déplace les murs, on choisit les finitions et on laisse des notes au constructeur.', to_designer: 'Ouvrir l’outil d’aménagement',
      design_sum: '${rooms} pièces · ${fin} finitions · ${chg} modifications · ${notes} notes au constructeur', design_saved: 'Un aménagement est enregistré', style: 'Style de l’appartement exemple',
      services: 'Services', services_sub: 'À joindre à la demande. Sans prix, sans engagement.',
      svc_mortgage: 'Conseil en crédit', svc_mortgage_d: 'Capacité de financement et accord de principe', svc_lawyer: 'Avocat immobilier', svc_lawyer_d: 'Contrat de vente et garanties vérifiés',
      svc_design: 'Architecture intérieure', svc_design_d: 'Concept et budget pour cet appartement', svc_inspection: 'Inspection et suivi', svc_inspection_d: 'Vérification avant la livraison',
      svc_moving: 'Déménagement', svc_moving_d: 'Un devis pour le jour de l’emménagement', svc_rent: 'Gestion locative', svc_rent_d: 'Ce qu’il rapporte en attendant',
      pro_pick: 'Professionnels de l’annuaire (facultatif)', pro_none: 'Nous en recommanderons un', pro_chosen: 'Choisi', rent_calc: 'Calculer le revenu locatif',
      call: 'Appel', call_sub: 'Quand le promoteur et l’équipe peuvent-ils vous rappeler ? Une demande, pas un rendez-vous fixé.', call_none: 'Aucun créneau choisi', between: 'entre', and: 'et',
      ch_phone: 'Téléphone', ch_video: 'Vidéo', ch_wa: 'WhatsApp', days: ['dim.', 'lun.', 'mar.', 'mer.', 'jeu.', 'ven.', 'sam.'],
      price: 'Prix et droits d’achat', price_l: 'Le prix communiqué par le vendeur (facultatif)', b_single: 'Logement unique', b_additional: 'Logement supplémentaire', b_foreign: 'Non-résident',
      tax: 'Droits d’achat estimés', tax_note: 'Selon les tranches en vigueur. Une estimation, pas un conseil fiscal.', foreign_note: 'Un non-résident paie les tranches du logement supplémentaire dès le premier shekel.', hint: 'Prix publié',
      to_summary: 'Récapitulatif', s1: 'Résumé', s2: 'Demande', s3: 'Réservation', summary: 'Récapitulatif de la commande',
      not_incl: 'Prix, descriptif et contrat sont fixés avec le promoteur. NadLan publie le projet et transmet votre demande au promoteur et aux professionnels choisis ; elle n’est pas partie à la vente et ne facture rien à l’acheteur.',
      to_request: 'Continuer vers la demande', f_name: 'Nom complet', f_phone: 'Mobile ou WhatsApp', f_email: 'E-mail (facultatif)',
      privacy: 'Donner vos coordonnées est un choix ; sans elles, nous ne pouvons pas transmettre la demande. Elles vont au promoteur de ${project} et aux professionnels choisis, uniquement pour répondre à cette demande. Opérateur : NadLan, nad-lan.co.il. Vous pouvez les consulter, les corriger et demander leur suppression.',
      privacy_link: 'Politique de confidentialité', consent: 'J’accepte que la demande soit transmise au promoteur de ${project} et aux professionnels choisis',
      send: 'Envoyer la demande', sending: 'Envoi...', need: 'Indiquez votre nom et votre mobile, et cochez l’accord.', err: 'Cela n’a pas abouti. Réessayez dans un instant.',
      sent: 'Demande envoyée', st_rfp: 'Demande reçue', st_next: 'Le promoteur et l’équipe vous recontactent', st_offer: 'Une offre en bonne forme pour cet appartement',
      doc: 'Le document de la demande (imprimer ou enregistrer)', to_reserve: 'Étape suivante : réserver', reserve_note: 'La réservation comporte des conditions provisoires pour avocat, un arrêt pour l’avocat et un dépôt exemple uniquement. Aucun débit.',
      ordered: 'Demande ${ref} envoyée', open_order: 'Ouvrir la commande',
      wa: 'Envoyer le panier sur WhatsApp', room: 'Salle de visite partagée avec un conseiller', clear: 'Vider le panier', close: 'Fermer', back: 'Retour au panier',
      legal: 'Le panier n’est pas un achat et l’appartement n’est pas vendu sur ce site. Tout paiement pour l’appartement ira uniquement sur le compte séquestre du projet.',
      wa_intro: 'Bonjour, j’ai composé un panier pour ${project} sur nad-lan.co.il :', wa_close: 'Je souhaite les plans, les prix et les disponibilités. C’est une demande d’information, pas une commande.', other: 'Aussi dans le panier',
    },
    ru: {
      name: 'Моя корзина', add: 'Добавить квартиру', add_proj: 'Добавить проект', in_cart: 'В корзине', open: 'Моя корзина', count: 'проектов в корзине',
      kept: 'Хранится в этом браузере. Можно собрать квартиры из нескольких проектов.', empty: 'Корзина пуста. Выберите квартиру на башне или добавьте проект.',
      unit: 'Квартира', example: 'Пример квартиры', unit_open: 'Выбирается с застройщиком', floor: 'Этаж', tower: 'Башня', facing: 'Окна на', rooms: 'комн.', sqm: 'м²',
      pick_hint: 'Выберите этаж на башне на этой странице, и квартира обновится здесь.', change: 'Изменить', remove: 'Убрать', edit: 'Изменить',
      design: 'Мой проект', design_none: 'Проекта пока нет. В дизайнере можно двигать стены, выбирать отделку и оставлять заметки строителю.', to_designer: 'Открыть дизайнер',
      design_sum: '${rooms} комн. · ${fin} отделок · ${chg} изменений · ${notes} заметок строителю', design_saved: 'Проект сохранён в дизайнере', style: 'Стиль в примере квартиры',
      services: 'Услуги', services_sub: 'Что приложить к запросу. Без цены и обязательств.',
      svc_mortgage: 'Ипотечный консультант', svc_mortgage_d: 'Лимит финансирования и предварительное одобрение', svc_lawyer: 'Юрист по недвижимости', svc_lawyer_d: 'Проверка договора и гарантий',
      svc_design: 'Дизайн интерьера', svc_design_d: 'Концепция и бюджет для этой квартиры', svc_inspection: 'Технический надзор', svc_inspection_d: 'Проверка квартиры перед сдачей',
      svc_moving: 'Переезд', svc_moving_d: 'Предложение на день переезда', svc_rent: 'Управление арендой', svc_rent_d: 'Сколько она принесёт до вашего переезда',
      pro_pick: 'Специалисты из каталога (необязательно)', pro_none: 'Мы порекомендуем', pro_chosen: 'Выбран', rent_calc: 'Рассчитать доход от аренды',
      call: 'Звонок', call_sub: 'Когда застройщику и команде перезвонить вам? Это просьба, а не назначенная встреча.', call_none: 'Время не выбрано', between: 'с', and: 'до',
      ch_phone: 'Телефон', ch_video: 'Видео', ch_wa: 'WhatsApp', days: ['вс', 'пн', 'вт', 'ср', 'чт', 'пт', 'сб'],
      price: 'Цена и налог на покупку', price_l: 'Цена от отдела продаж (необязательно)', b_single: 'Единственное жильё', b_additional: 'Дополнительное жильё', b_foreign: 'Нерезидент',
      tax: 'Налог на покупку (оценка)', tax_note: 'По действующим ставкам. Оценка, не налоговая консультация.', foreign_note: 'Нерезидент платит по ставкам дополнительного жилья с первого шекеля.', hint: 'Опубликованная цена',
      to_summary: 'Итог заказа', s1: 'Итог', s2: 'Запрос', s3: 'Бронь', summary: 'Итог заказа',
      not_incl: 'Цена, спецификация и договор согласуются с застройщиком. NadLan публикует проект и передаёт ваш запрос застройщику и выбранным специалистам; сайт не является стороной сделки и ничего не берёт с покупателя.',
      to_request: 'Перейти к запросу', f_name: 'Полное имя', f_phone: 'Мобильный или WhatsApp', f_email: 'E-mail (необязательно)',
      privacy: 'Вы указываете данные добровольно; без них мы не сможем передать запрос. Они передаются застройщику проекта ${project} и выбранным специалистам, только для ответа на этот запрос. Оператор: NadLan, nad-lan.co.il. Вы вправе просмотреть, исправить и удалить свои данные.',
      privacy_link: 'Политика конфиденциальности', consent: 'Я согласен(на) на передачу запроса застройщику проекта ${project} и выбранным специалистам',
      send: 'Отправить запрос', sending: 'Отправляем...', need: 'Укажите имя и мобильный и отметьте согласие.', err: 'Не получилось. Попробуйте ещё раз через минуту.',
      sent: 'Запрос отправлен', st_rfp: 'Запрос получен', st_next: 'Застройщик и команда свяжутся с вами', st_offer: 'Оформленное предложение по этой квартире',
      doc: 'Документ запроса (печать или сохранение)', to_reserve: 'Далее: бронирование', reserve_note: 'В бронировании: черновик условий для юриста, остановка на проверку юристом и только пробный депозит. Деньги не списываются.',
      ordered: 'Запрос ${ref} отправлен', open_order: 'Открыть заказ',
      wa: 'Отправить корзину в WhatsApp', room: 'Общая комната просмотра с представителем', clear: 'Очистить корзину', close: 'Закрыть', back: 'Назад в корзину',
      legal: 'Корзина не является покупкой, и квартира не продаётся на сайте. Любой платёж за квартиру поступает только на эскроу-счёт проекта.',
      wa_intro: 'Здравствуйте, я собрал(а) корзину по проекту ${project} на nad-lan.co.il:', wa_close: 'Прошу планы, цены и наличие. Это запрос информации, а не заказ.', other: 'Ещё в корзине',
    },
    ar: {
      name: 'سلتي', add: 'إضافة الشقة إلى السلة', add_proj: 'إضافة المشروع إلى السلة', in_cart: 'في السلة', open: 'سلتي', count: 'مشاريع في السلة',
      kept: 'تُحفظ في هذا المتصفح. يمكنك جمع شقق من عدة مشاريع.', empty: 'السلة فارغة. اختر شقة على البرج أو أضف المشروع، وستنتظرك هنا.',
      unit: 'الشقة', example: 'شقة نموذجية', unit_open: 'تُختار مع المطوّر', floor: 'الطابق', tower: 'البرج', facing: 'باتجاه', rooms: 'غرف', sqm: 'م²',
      pick_hint: 'اختر طابقًا على البرج في هذه الصفحة وستتحدّث الشقة هنا.', change: 'تغيير', remove: 'إزالة', edit: 'تعديل',
      design: 'تصميمي', design_none: 'لا يوجد تصميم بعد. في المصمم تحرّك الجدران وتختار التشطيبات وتترك ملاحظات للمقاول.', to_designer: 'فتح مصمم الشقة',
      design_sum: '${rooms} غرف · ${fin} تشطيبات · ${chg} تغييرات · ${notes} ملاحظات للمقاول', design_saved: 'تصميم محفوظ في المصمم', style: 'النمط في الشقة النموذجية',
      services: 'الخدمات', services_sub: 'ما يُرفق بالطلب. بلا سعر وبلا التزام.',
      svc_mortgage: 'استشارة رهن عقاري', svc_mortgage_d: 'سقف التمويل وموافقة مبدئية', svc_lawyer: 'محامي عقارات', svc_lawyer_d: 'فحص عقد البيع والضمانات',
      svc_design: 'تصميم داخلي', svc_design_d: 'فكرة وميزانية لهذه الشقة', svc_inspection: 'فحص وإشراف', svc_inspection_d: 'فحص الشقة قبل التسليم',
      svc_moving: 'نقل', svc_moving_d: 'عرض نقل ليوم الانتقال', svc_rent: 'إدارة التأجير', svc_rent_d: 'كم تدرّ الشقة حتى انتقالك',
      pro_pick: 'مختصون من الدليل (اختياري)', pro_none: 'سنوصي بمختص', pro_chosen: 'تم الاختيار', rent_calc: 'احسب دخل الإيجار',
      call: 'مكالمة', call_sub: 'متى يناسبك أن يتصل بك المطوّر والفريق؟ هذا طلب وليس موعدًا محجوزًا.', call_none: 'لم يُختر موعد بعد', between: 'بين', and: 'و',
      ch_phone: 'هاتف', ch_video: 'فيديو', ch_wa: 'واتساب', days: ['الأحد', 'الاثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت'],
      price: 'السعر وضريبة الشراء', price_l: 'السعر الذي أعطاك إياه فريق المبيعات (اختياري)', b_single: 'شقة وحيدة', b_additional: 'شقة إضافية', b_foreign: 'مقيم في الخارج',
      tax: 'ضريبة الشراء التقديرية', tax_note: 'وفق الشرائح السارية. تقدير وليس استشارة ضريبية.', foreign_note: 'المقيم في الخارج يدفع وفق شرائح الشقة الإضافية من الشيكل الأول.', hint: 'سعر منشور',
      to_summary: 'ملخص الطلب', s1: 'الملخص', s2: 'طلب عرض', s3: 'الحجز', summary: 'ملخص الطلب',
      not_incl: 'السعر والمواصفات والعقد تُحدَّد مع المطوّر. ينشر NadLan المشروع وينقل طلبك إلى المطوّر والمختصين الذين اخترتهم؛ وليس طرفًا في الصفقة ولا يتقاضى من المشتري شيئًا.',
      to_request: 'متابعة إلى طلب العرض', f_name: 'الاسم الكامل', f_phone: 'الجوال أو واتساب', f_email: 'البريد الإلكتروني (اختياري)',
      privacy: 'تقديم بياناتك اختياري؛ ومن دونها لا يمكننا نقل الطلب. تُنقل إلى مطوّر ${project} وإلى المختصين الذين اخترتهم، للرد على هذا الطلب فقط. المشغّل: NadLan، nad-lan.co.il. يحق لك الاطلاع على بياناتك وتصحيحها وطلب حذفها.',
      privacy_link: 'سياسة الخصوصية', consent: 'أوافق على نقل الطلب إلى مطوّر ${project} وإلى المختصين الذين اخترتهم',
      send: 'إرسال طلب العرض', sending: 'جارٍ الإرسال...', need: 'يرجى إدخال الاسم والجوال وتحديد الموافقة.', err: 'لم ينجح الأمر. حاول مجددًا بعد قليل.',
      sent: 'تم إرسال الطلب', st_rfp: 'تم استلام الطلب', st_next: 'يتواصل معك المطوّر والفريق', st_offer: 'عرض منظّم لهذه الشقة',
      doc: 'مستند الطلب (للطباعة والحفظ)', to_reserve: 'التالي: حجز الشقة', reserve_note: 'في الحجز: مسودة شروط للمحامي، وتوقف لمراجعة المحامي، وعربون تجريبي فقط. لن يُخصم أي مبلغ.',
      ordered: 'تم إرسال الطلب ${ref}', open_order: 'فتح الطلب',
      wa: 'إرسال السلة عبر واتساب', room: 'غرفة مشاهدة مشتركة مع ممثل', clear: 'إفراغ السلة', close: 'إغلاق', back: 'العودة إلى السلة',
      legal: 'السلة ليست شراءً، والشقة لا تُباع على الموقع. أي دفعة عن الشقة، حين تكون، تذهب فقط إلى حساب الضمان الخاص بالمشروع.',
      wa_intro: 'مرحبًا، جهّزت سلة لمشروع ${project} على nad-lan.co.il:', wa_close: 'أرغب في المخططات والأسعار والتوفر. هذا طلب معلومات وليس طلب شراء.', other: 'أيضًا في السلة',
    },
  };
  const fill = (s, v) => (v ? String(s).replace(/\$\{(\w+)\}/g, (m, k) => (v[k] == null ? '' : String(v[k]))) : String(s));
  const t = (k, v) => fill((D[L] && D[L][k] != null) ? D[L][k] : (D.en[k] != null ? D.en[k] : k), v);
  const esc = (s) => String(s == null ? '' : s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const NFL = { he: 'he-IL', en: 'en-GB', fr: 'fr-FR', ru: 'ru-RU', ar: 'en-GB' }[L];
  const nf = new Intl.NumberFormat(NFL, { maximumFractionDigits: 0 });
  const ils = (n) => '<span class="nlc-n">₪ ' + esc(nf.format(Math.round(n))) + '</span>';
  const track = (n, d) => { try { if (window.nlTrack) window.nlTrack(n, d || {}); } catch (e) { /* none */ } };
  const SVC = ['mortgage', 'lawyer', 'design', 'inspection', 'moving', 'rent'];
  const PROF = { mortgage: 'mashkanta', lawyer: 'lawyer', design: 'interior_designer', inspection: 'engineer' };
  const DIRS = { he: ['צפון', 'צפון מזרח', 'מזרח', 'דרום מזרח', 'דרום', 'דרום מערב', 'מערב', 'צפון מערב'], en: ['north', 'north-east', 'east', 'south-east', 'south', 'south-west', 'west', 'north-west'],
    fr: ['nord', 'nord-est', 'est', 'sud-est', 'sud', 'sud-ouest', 'ouest', 'nord-ouest'], ru: ['север', 'северо-восток', 'восток', 'юго-восток', 'юг', 'юго-запад', 'запад', 'северо-запад'],
    ar: ['الشمال', 'الشمال الشرقي', 'الشرق', 'الجنوب الشرقي', 'الجنوب', 'الجنوب الغربي', 'الغرب', 'الشمال الغربي'] };

  /* ---------------------------------------------------------------- the store */
  const KEY = 'nl-cart:v1';
  const fresh = () => ({ v: 1, projects: {}, order: [] });
  function load() { try { const s = JSON.parse(localStorage.getItem(KEY) || 'null'); if (s && s.v === 1 && s.projects && typeof s.projects === 'object') { s.order = Array.isArray(s.order) ? s.order : Object.keys(s.projects); return s; } } catch (e) { /* private window */ } return fresh(); }
  let S = load();
  let dirty = false;
  function save() { S.updated = Date.now(); try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) { /* storage blocked: the basket lasts for this page */ } dirty = true; schedulePaint(); }
  const inCart = () => S.order.filter((s) => S.projects[s] && S.projects[s].in);
  function proj(slug, create) {
    let p = S.projects[slug];
    if (!p && create && P && slug === P.slug) {
      p = S.projects[slug] = { slug, name: P.name, city: P.city, url: P.url, img: P.img, lang: L, in: false, added: 0, unit: null, style: null, services: {}, call: null, price: { amount: '', buyer: 'single' }, design: null, rent: null, order: null };
      S.order = [slug].concat(S.order.filter((x) => x !== slug));
    }
    if (p && P && slug === P.slug && p.lang === L) { p.name = P.name; p.url = P.url; p.city = P.city; if (P.img) p.img = P.img; } // the page's own words win in its language
    return p || null;
  }
  // the old per-project basket (nl-basket:<slug>, until 19.11.2026): what the buyer collected there is carried over once
  if (P) {
    try {
      const old = JSON.parse(localStorage.getItem('nl-basket:' + P.slug) || localStorage.getItem('nl-basket:' + P.slug + '-' + L) || 'null');
      if (old && !(S.projects[P.slug] && S.projects[P.slug].migrated)) {
        const p = proj(P.slug, true);
        if (old.unit && old.unit.floor) p.unit = { floor: Number(old.unit.floor), tower: old.unit.tower || '', bearing: old.unit.bearing != null ? Number(old.unit.bearing) : null, label: old.unit.label || '' };
        if (old.style) p.style = old.style;
        if (old.team) for (const k of Object.keys(old.team)) { const m = { mashkanta: 'mortgage', lawyer: 'lawyer', interior_designer: 'design', engineer: 'inspection' }[k]; if (m && old.team[k]) p.services[m] = { pro: old.team[k].id ? { id: old.team[k].id, name: old.team[k].name } : null }; }
        if (old.price && old.price.amount) p.price = { amount: String(old.price.amount), buyer: old.price.buyer || 'single' };
        if (p.unit || p.style || Object.keys(p.services).length || p.price.amount) p.in = true;
        p.migrated = 1;
        save();
      }
    } catch (e) { /* none */ }
  }

  /* ---------------------------------------------------------------- what the page tells us */
  function setUnit(u, source) {
    if (!P) return;
    const p = proj(P.slug, true);
    const cur = p.unit || {};
    const next = { floor: u.floor != null && isFinite(u.floor) ? Number(u.floor) : (cur.floor != null ? cur.floor : null), tower: u.tower != null ? String(u.tower).slice(0, 4) : (u.floor === cur.floor ? cur.tower || '' : ''),
      bearing: u.bearing != null && isFinite(u.bearing) ? Math.round(Number(u.bearing)) : (u.floor === cur.floor ? cur.bearing : null), label: u.label ? String(u.label).slice(0, 60) : '', id: u.id ? String(u.id).slice(0, 60) : '' };
    if (next.floor == null && !next.id) return;
    p.unit = next; p.unitSource = source || '';
    save();
  }
  window.addEventListener('nl:floor', (e) => { const f = e.detail && Number(e.detail.floor); if (f > 0) setUnit({ floor: f }, 'stage'); });
  window.addEventListener('nl:facing', (e) => { const d = e.detail || {}; if (Number(d.floor) > 0) setUnit({ floor: Number(d.floor), bearing: d.bearing, tower: d.tower || null, label: !d.tower && d.label ? d.label : '' }, 'stage'); });
  window.addEventListener('nadlan:unit-picked', (e) => { const d = e.detail || {}; if (!P || (d.project && d.project !== P.slug)) return; setUnit({ floor: d.floor, tower: d.tower || null, bearing: d.bearing, id: d.unit || '' }, 'shell'); });
  window.addEventListener('nl:view', (e) => { const d = e.detail || {}; if (P && d.mode === 'inside' && d.style) { const p = proj(P.slug, true); if (p.style !== d.style) { p.style = String(d.style).slice(0, 20); save(); } } });
  // the designer (package 2): an explicit add, or the saved design for this project
  function takeDesign(d, add) {
    if (!d || d.schema !== 'nadlan-cart-design' || !d.project) return;
    const p = S.projects[d.project] || (P && d.project === P.slug ? proj(P.slug, true) : null);
    if (!p) { if (add) { S.projects[d.project] = { slug: d.project, name: d.project_name || d.project, city: '', url: '', img: '', lang: d.lang || L, in: true, added: Date.now(), unit: null, services: {}, call: null, price: { amount: '', buyer: 'single' }, design: d, rent: null, order: null }; S.order.unshift(d.project); save(); } return; }
    p.design = d;
    if (add && !p.in) { p.in = true; p.added = Date.now(); track('basket_add', { project: p.slug, unit: d.unit_id || '', v: inCart().length }); }
    save();
  }
  window.addEventListener('nl:design', (e) => takeDesign(e.detail, false));
  // package 2's design order (schema nadlan-design-order v1, localStorage 'nl-design-order:v1', events nadlan:design-order[-updated]):
  // read as it is, never written; mapped to the basket's design shape (labels already in the buyer's language, unknown numbers omitted)
  function fromOrder(o) {
    if (!o || o.schema !== 'nadlan-design-order' || !o.project || !o.project.slug) return null;
    const abs = (u) => { try { return u ? new URL(u, location.origin).href : null; } catch (e) { return null; } };
    const fin = (o.finishes || []).map((f) => ({ label: (f.roomName ? f.roomName + ': ' : '') + (f.label || '') })).filter((f) => f.label);
    const chg = (o.changes || []).map((c) => ({ kind: c.kind || 'other', label: (c.label || '') + (c.qty > 1 ? ' ×' + c.qty : '') })).filter((c) => c.label);
    const items = (o.items || []).map((i) => ({ label: (i.label || '') + (i.count > 1 ? ' ×' + i.count : '') + (i.roomName ? ' (' + i.roomName + ')' : '') })).filter((i) => i.label);
    const extras = (o.services || []).map((s) => s.label).filter(Boolean);
    return { schema: 'nadlan-cart-design', v: 1, from: 'design-order', id: o.id, rev: o.rev, project: o.project.slug, project_name: o.project.title || '', unit_id: (o.unit && o.unit.id) || '', lang: o.lang || L,
      updated_at: o.updated || o.created || '', rooms: (o.rooms || []).map((r) => ({ key: r.id, name: r.name, area_m2: r.area_m2 != null ? r.area_m2 : null })), finishes: fin, changes: chg, items, extras,
      notes: (o.notes || []).map((n) => ({ text: (n.roomName ? n.roomName + ': ' : '') + (n.text || ''), room_key: n.room || null, at: n.at || '', by: 'buyer' })).filter((n) => n.text),
      budget: o.budget && o.budget.min != null ? { min: o.budget.min, max: o.budget.max != null ? o.budget.max : null } : null, share_url: abs(o.link), services: (o.services || []).map((s) => s.id), unit: o.unit || null };
  }
  function takeOrder(o, add) {
    const d = fromOrder(o);
    if (!d) return;
    const p = S.projects[d.project];
    if (!add && !(p && p.in)) { if (p) { p.design = d; save(); } return; } // an autosave refreshes only an order already in the basket
    takeDesign(d, add);
    const q = S.projects[d.project];
    if (q) {
      if (d.services.indexOf('designer') >= 0 && !q.services.design) q.services.design = { pro: null };
      if (d.services.indexOf('tenant') >= 0 && !q.services.rent) q.services.rent = { pro: null };
      if (d.services.indexOf('call') >= 0 && !q.call) V.open[q.slug + ':call'] = 1;
      if (!q.unit && d.unit && d.unit.label) q.unit = { floor: null, tower: '', bearing: null, label: String(d.unit.label).slice(0, 60), id: '' };
      save();
    }
  }
  window.addEventListener('nadlan:design-order', (e) => { takeOrder(e.detail, true); open('basket', e.detail && e.detail.project && e.detail.project.slug); });
  window.addEventListener('nadlan:design-order-updated', (e) => takeOrder(e.detail, false));
  function scanOrders() {
    try {
      const r = JSON.parse(localStorage.getItem('nl-design-order:v1') || 'null');
      if (!r || !r.orders) return;
      for (const k of Object.keys(r.orders)) {
        const d = fromOrder(r.orders[k]);
        const p = d && S.projects[d.project];
        if (p && (!p.design || String(d.updated_at || '') > String(p.design.updated_at || ''))) p.design = d;
      }
    } catch (e) { /* none */ }
  }
  function scanDesigns() {
    try {
      for (let i = 0; i < localStorage.length; i++) {
        const k = localStorage.key(i);
        if (!k || k.indexOf('nl-cart-design:') !== 0) continue;
        const d = JSON.parse(localStorage.getItem(k) || 'null');
        if (!d || !d.project) continue;
        const p = S.projects[d.project];
        if (p && (!p.design || String(d.updated_at || '') > String(p.design.updated_at || ''))) p.design = d;
      }
    } catch (e) { /* none */ }
  }
  // the rental plan (package 6)
  function takeRent(plan, add) {
    if (!plan || plan.schema !== 'nadlan-rent-plan' || !plan.project) return;
    const slug = plan.project.slug;
    const p = S.projects[slug] || (P && slug === P.slug ? proj(P.slug, true) : null);
    if (!p) return;
    p.rent = plan; p.services.rent = p.services.rent || { pro: null };
    if (add && !p.in) { p.in = true; p.added = Date.now(); }
    save();
  }
  window.addEventListener('nadlan:rent-plan', (e) => takeRent(e.detail, true));
  function scanRent() {
    try { const r = JSON.parse(localStorage.getItem('nl-rent-plan:v1') || 'null'); if (r && r.plans) for (const k of Object.keys(r.plans)) { const pl = r.plans[k]; const s = pl && pl.project && pl.project.slug; if (s && S.projects[s] && !S.projects[s].rent) S.projects[s].rent = pl; } } catch (e) { /* none */ }
  }
  window.addEventListener('storage', (e) => {
    if (e.key === KEY) { S = load(); schedulePaint(); }
    else if (e.key && e.key.indexOf('nl-cart-design:') === 0) { try { takeDesign(JSON.parse(e.newValue || 'null'), false); } catch (x) { /* none */ } }
    else if (e.key === 'nl-rent-plan:v1') { scanRent(); save(); }
    else if (e.key === 'nl-design-order:v1') { scanOrders(); save(); }
  });
  // the showroom engine (DUO, Rainbow and the other engine pages): its units and its "build me an offer" buttons
  function engineUnit(id) {
    const SR = window.NADLAN_SHOWROOM;
    if (!SR || !SR.projects) return null;
    for (const k of Object.keys(SR.projects)) { const us = (SR.projects[k] && SR.projects[k].units) || []; for (const u of us) if (String(u.id) === String(id)) return u; }
    return null;
  }
  if (P && P.engine) {
    document.addEventListener('click', (e) => {
      const b = e.target && e.target.closest && e.target.closest('[data-act="rfp"][data-id],[data-act="select"][data-id]');
      if (!b) return;
      const u = engineUnit(b.getAttribute('data-id'));
      if (u) setUnit({ floor: u.floor, id: u.id, label: u.label || '' }, 'engine');
      if (b.getAttribute('data-act') === 'rfp') { e.preventDefault(); e.stopImmediatePropagation(); add(true, b); go('summary', P.slug); }
    }, true);
  }

  /* ---------------------------------------------------------------- the words for a line */
  const unitLine = (u) => {
    if (!u || (u.floor == null && !u.label)) return '';
    const a = [];
    if (u.label) a.push(u.label);
    if (u.floor != null) a.push(t('floor') + ' ' + u.floor);
    if (u.tower) a.push(t('tower') + ' ' + u.tower);
    if (u.bearing != null) a.push(t('facing') + (L === 'he' ? '' : ' ') + DIRS[L][Math.round((((u.bearing % 360) + 360) % 360) / 45) % 8]);
    return a.join(' · ');
  };
  const designLine = (d) => d ? t('design_sum', { rooms: (d.rooms || []).length, fin: (d.finishes || []).length, chg: (d.changes || []).length, notes: (d.notes || []).length }) : '';
  function tax(amount, buyer) {
    const br = (C.tax && C.tax[buyer === 'single' ? 'single' : 'additional']) || [];
    let x = 0, prev = 0;
    for (const [ceil, rate] of br) { const top = ceil == null ? Infinity : Number(ceil); if (amount > prev) x += (Math.min(amount, top) - prev) * Number(rate); prev = top; if (amount <= top) break; }
    return Math.round(x);
  }
  const amountOf = (p) => { const n = Number(String((p.price && p.price.amount) || '').replace(/[^\d]/g, '')); return n >= 100000 ? n : 0; };
  const svcOn = (p) => SVC.filter((k) => p.services && p.services[k]);
  const callLine = (c) => {
    if (!c) return '';
    const d = new Date(c.day + 'T12:00:00');
    const day = (D[L].days || D.en.days)[d.getDay()] + ' ' + String(d.getDate()).padStart(2, '0') + '.' + String(d.getMonth() + 1).padStart(2, '0');
    return day + ' · ' + t('between') + ' ' + c.win + ':00 ' + t('and') + (Number(c.win) + 3) + ':00 · ' + t('ch_' + c.ch);
  };

  /* ---------------------------------------------------------------- the sheet */
  let root = null, body = null, foot = null, opener = null, V = { view: 'basket', slug: null, open: {} };
  function build() {
    root = document.createElement('div');
    root.className = 'nlc'; root.hidden = true; root.setAttribute('dir', RTL ? 'rtl' : 'ltr'); root.setAttribute('lang', L);
    root.innerHTML = '<div class="nlc__scrim" data-x></div><section class="nlc__sheet" role="dialog" aria-modal="true" aria-labelledby="nlc-title">'
      + '<header class="nlc__head"><div class="nlc__hgrp"><p class="nlc__kick"></p><h2 class="nlc__title" id="nlc-title"></h2></div><button type="button" class="nlc__x" data-x aria-label="' + esc(t('close')) + '">×</button></header>'
      + '<div class="nlc__body"></div><footer class="nlc__foot"></footer></section>';
    document.body.appendChild(root);
    body = root.querySelector('.nlc__body'); foot = root.querySelector('.nlc__foot');
    root.addEventListener('click', onClick);
    root.addEventListener('change', onChange);
    root.addEventListener('input', onInput);
    root.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') { close(); return; }
      if (e.key !== 'Tab') return;
      const f = [...root.querySelectorAll('button:not([disabled]),a[href],input:not([disabled]),select,textarea,[tabindex="0"]')].filter((x) => x.offsetParent !== null);
      if (!f.length) return;
      if (e.shiftKey && document.activeElement === f[0]) { e.preventDefault(); f[f.length - 1].focus(); } else if (!e.shiftKey && document.activeElement === f[f.length - 1]) { e.preventDefault(); f[0].focus(); }
    });
    if (!document.querySelector('link[data-nlc-fonts]')) {
      const l = document.createElement('link'); l.rel = 'stylesheet'; l.setAttribute('data-nlc-fonts', '');
      l.href = 'https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@500&family=IBM+Plex+Sans+Arabic:wght@400;600;700&family=IBM+Plex+Sans+Hebrew:wght@400;600;700&family=IBM+Plex+Sans:wght@400;600;700&display=swap';
      document.head.appendChild(l);
    }
  }
  // the Kikar showroom keeps the apartment on screen in its own link (#dira=B24-262); it announces it before this script listens
  function fromHash() {
    const m = /^#dira=([A-Z])(\d{1,3})-(\d{1,3})/.exec(location.hash || '');
    if (!m || !P) return;
    const p = S.projects[P.slug], u = p && p.unit;
    if (u && u.tower === m[1] && u.floor === Number(m[2]) && u.bearing === Number(m[3])) return;
    setUnit({ floor: Number(m[2]), tower: m[1], bearing: Number(m[3]) }, 'link');
  }
  window.addEventListener('hashchange', fromHash);
  function open(view, slug, from) {
    fromHash();
    if (!root) build();
    scanDesigns(); scanOrders(); scanRent();
    opener = from || document.activeElement;
    V.view = view || 'basket'; V.slug = slug || (P && S.projects[P.slug] && S.projects[P.slug].in ? P.slug : inCart()[0]) || null;
    render();
    root.hidden = false;
    document.documentElement.classList.add('nlc-open');
    requestAnimationFrame(() => root.classList.add('is-on'));
    const x = root.querySelector('.nlc__x'); if (x) x.focus({ preventScroll: true });
    track('basket_open', { project: V.slug || (P && P.slug) || '', v: inCart().length });
  }
  function close() {
    if (!root || root.hidden) return;
    root.classList.remove('is-on'); root.hidden = true;
    document.documentElement.classList.remove('nlc-open');
    if (opener && opener.focus) try { opener.focus({ preventScroll: true }); } catch (e) { /* none */ }
  }
  function go(view, slug) { if (!root || root.hidden) { open(view, slug); return; } V.view = view; if (slug) V.slug = slug; render(); body.scrollTop = 0; }
  function add(openIt, from) {
    if (!P) { if (openIt) open('basket', null, from); return; }
    fromHash();
    const p = proj(P.slug, true);
    if (!p.in) { p.in = true; p.added = Date.now(); track('basket_add', { project: P.slug, unit: (p.unit && (p.unit.id || p.unit.floor)) || '', v: inCart().length }); }
    S.order = [P.slug].concat(S.order.filter((x) => x !== P.slug));
    save();
    if (openIt) open('basket', P.slug, from);
  }

  const steps = (n) => '<ol class="nlc-steps" aria-label="' + esc(t('summary')) + '">' + ['s1', 's2', 's3'].map((k, i) => '<li class="' + (i + 1 < n ? 'is-done' : i + 1 === n ? 'is-on' : '') + '"' + (i + 1 === n ? ' aria-current="step"' : '') + '><b>' + (i + 1) + '</b> ' + esc(t(k)) + '</li>').join('') + '</ol>';
  const row = (k, v, act) => '<div class="nlc-ln"><span class="nlc-k">' + esc(k) + '</span><span class="nlc-v">' + v + '</span>' + (act || '<span></span>') + '</div>';

  function render() {
    if (!root) return;
    const y = body.scrollTop;
    root.querySelector('.nlc__kick').textContent = V.view === 'basket' ? t('kept') : ((S.projects[V.slug] || {}).name || '');
    root.querySelector('.nlc__title').textContent = V.view === 'basket' ? t('name') : V.view === 'sent' ? t('sent') : V.view === 'request' ? t('s2') : t('summary');
    if (V.view === 'summary' && V.slug && S.projects[V.slug]) { body.innerHTML = vSummary(S.projects[V.slug]); }
    else if (V.view === 'request' && V.slug && S.projects[V.slug]) { body.innerHTML = vRequest(S.projects[V.slug]); }
    else if (V.view === 'sent' && V.slug && S.projects[V.slug]) { body.innerHTML = vSent(S.projects[V.slug]); }
    else { V.view = 'basket'; body.innerHTML = vBasket(); }
    foot.innerHTML = vFoot();
    body.scrollTop = V.view === 'basket' ? y : 0;
    dirty = false;
  }
  let paintTimer = 0;
  function schedulePaint() { if (paintTimer) return; paintTimer = requestAnimationFrame(() => { paintTimer = 0; paint(); }); }
  function paint() {
    const n = inCart().length;
    document.querySelectorAll('.nlc-badge').forEach((b) => { b.textContent = String(n); b.hidden = n === 0; });
    const p = P ? S.projects[P.slug] : null;
    document.querySelectorAll('.nlc-addbtn').forEach((b) => { const on = !!(p && p.in); b.classList.toggle('is-in', on); b.querySelector('span').textContent = on ? t('in_cart') + ' · ' + t('open') : (p && p.unit ? t('add') : t('add_proj')); });
    if (chip) chip.hidden = n === 0 && !P;
    const ae = document.activeElement;
    if (root && !root.hidden && dirty && !(ae && root.contains(ae) && ae.matches('input,textarea,select'))) render();
  }

  /* views */
  function card(p) {
    const cur = V.open || {};
    const u = p.unit;
    let h = '<article class="nlc-proj" data-slug="' + esc(p.slug) + '"><header class="nlc-proj__h"><b>' + esc(p.name) + '</b><span>' + esc(p.city || '') + '</span></header>';
    // the apartment
    const ul = unitLine(u);
    h += row(t('unit'), ul ? esc(ul) + (u && !u.id ? ' <span class="nlc-tag">' + esc(t('example')) + '</span>' : '') : '<span class="nlc-mute">' + esc(t('unit_open')) + '</span>' + (P && P.slug === p.slug ? '<br><span class="nlc-mute nlc-s">' + esc(t('pick_hint')) + '</span>' : ''),
      P && P.slug === p.slug ? '' : (p.url ? '<a class="nlc-ed" href="' + esc(p.url) + '">' + esc(t('change')) + '</a>' : ''));
    // the design
    const dl = p.design ? designLine(p.design) : '';
    const dsg = C.designer ? C.designer + '?project=' + encodeURIComponent(p.slug) + '&lang=' + L : '';
    h += row(t('design'), dl ? esc(dl) : (p.style ? esc(t('style')) : '<span class="nlc-mute nlc-s">' + esc(t('design_none')) + '</span>'), dsg ? '<a class="nlc-ed" href="' + esc(p.design && p.design.share_url ? p.design.share_url : dsg) + '">' + esc(t('to_designer')) + '</a>' : '');
    // services
    let sv = '<div class="nlc-chips" role="group" aria-label="' + esc(t('services')) + '">';
    for (const k of SVC) sv += '<button type="button" class="nlc-chip' + (p.services[k] ? ' is-on' : '') + '" data-svc="' + k + '" aria-pressed="' + (p.services[k] ? 'true' : 'false') + '" title="' + esc(t('svc_' + k + '_d')) + '">' + esc(t('svc_' + k)) + '</button>';
    sv += '</div>';
    const on = svcOn(p);
    if (on.length) {
      sv += '<ul class="nlc-svcl">';
      for (const k of on) {
        const pro = p.services[k] && p.services[k].pro;
        sv += '<li><b>' + esc(t('svc_' + k)) + '</b> <span class="nlc-mute">' + esc(t('svc_' + k + '_d')) + '</span>';
        if (k === 'rent') sv += p.rent && p.rent.estimate ? '<br>' + ils(p.rent.estimate.low) + ' - ' + ils(p.rent.estimate.high) + ' <span class="nlc-mute nlc-s">' + esc((p.rent.estimate.source_label || '') + ' ' + (p.rent.estimate.as_of || '')) + '</span>' : ' <a class="nlc-ed" href="' + esc((p.rent && p.rent.link) || (C.rentals + '?project=' + encodeURIComponent(p.slug) + '#earn')) + '">' + esc(t('rent_calc')) + '</a>';
        else if (PROF[k] && L === 'he') sv += '<br><span class="nlc-pros" data-pros="' + k + '">' + (pro ? esc(t('pro_chosen')) + ': ' + esc(pro.name) : '<button type="button" class="nlc-link" data-loadpros="' + k + '">' + esc(t('pro_pick')) + '</button>') + '</span>';
        else sv += '<br><span class="nlc-mute nlc-s">' + esc(t('pro_none')) + '</span>';
        sv += '</li>';
      }
      sv += '</ul>';
    }
    h += '<div class="nlc-blk"><div class="nlc-k">' + esc(t('services')) + '</div><p class="nlc-mute nlc-s">' + esc(t('services_sub')) + '</p>' + sv + '</div>';
    // the call
    const cOpen = cur[p.slug + ':call'];
    h += row(t('call'), p.call ? esc(callLine(p.call)) : '<span class="nlc-mute">' + esc(t('call_none')) + '</span>', '<button type="button" class="nlc-ed nlc-link" data-toggle="' + esc(p.slug) + ':call" aria-expanded="' + (cOpen ? 'true' : 'false') + '">' + esc(t(p.call ? 'change' : 'edit')) + '</button>');
    if (cOpen) h += callPicker(p);
    // the price
    const pOpen = cur[p.slug + ':price'];
    const amt = amountOf(p);
    h += row(t('price'), amt ? ils(amt) + ' · ' + esc(t('tax')) + ' ' + ils(tax(amt, p.price.buyer)) : '<span class="nlc-mute">-</span>', '<button type="button" class="nlc-ed nlc-link" data-toggle="' + esc(p.slug) + ':price" aria-expanded="' + (pOpen ? 'true' : 'false') + '">' + esc(t('edit')) + '</button>');
    if (pOpen) h += pricePicker(p);
    // the order already sent, or the next step
    if (p.order) h += '<div class="nlc-sent"><span class="nlc-ref">' + esc(p.order.ref) + '</span> ' + esc(t('ordered', { ref: '' })) + ' <a class="nlc-ed" href="' + esc(p.order.url) + '" target="_blank" rel="noopener">' + esc(t('open_order')) + '</a></div>';
    h += '<div class="nlc-acts"><button type="button" class="nlc-btn" data-go="summary" data-slug="' + esc(p.slug) + '">' + esc(t('to_summary')) + '</button><button type="button" class="nlc-link nlc-rm" data-remove="' + esc(p.slug) + '">' + esc(t('remove')) + '</button></div>';
    return h + '</article>';
  }
  function callPicker(p) {
    const c = p.call || {};
    let days = '';
    const d0 = new Date();
    for (let i = 1, n = 0; n < 6 && i < 12; i++) {
      const d = new Date(d0.getFullYear(), d0.getMonth(), d0.getDate() + i);
      if (d.getDay() === 6) continue;
      const iso = d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
      days += '<button type="button" class="nlc-chip' + (c.day === iso ? ' is-on' : '') + '" data-day="' + iso + '" aria-pressed="' + (c.day === iso) + '">' + esc((D[L].days || D.en.days)[d.getDay()]) + ' <span class="nlc-n">' + String(d.getDate()).padStart(2, '0') + '.' + String(d.getMonth() + 1).padStart(2, '0') + '</span></button>';
      n++;
    }
    const fri = c.day && new Date(c.day + 'T12:00:00').getDay() === 5;
    const wins = (fri ? ['09'] : ['09', '12', '15', '18']).map((w) => '<button type="button" class="nlc-chip' + (c.win === w ? ' is-on' : '') + '" data-win="' + w + '" aria-pressed="' + (c.win === w) + '"><span class="nlc-n">' + w + ':00-' + (Number(w) + 3) + ':00</span></button>').join('');
    const chs = ['phone', 'video', 'wa'].map((k) => '<button type="button" class="nlc-chip' + ((c.ch || 'phone') === k ? ' is-on' : '') + '" data-ch="' + k + '" aria-pressed="' + ((c.ch || 'phone') === k) + '">' + esc(t('ch_' + k)) + '</button>').join('');
    return '<div class="nlc-pick" data-slug="' + esc(p.slug) + '"><p class="nlc-mute nlc-s">' + esc(t('call_sub')) + '</p><div class="nlc-chips">' + days + '</div><div class="nlc-chips">' + wins + '</div><div class="nlc-chips">' + chs + '</div></div>';
  }
  function pricePicker(p) {
    const amt = amountOf(p), b = p.price.buyer || 'single';
    const hint = P && P.slug === p.slug && P.hint ? '<p class="nlc-mute nlc-s">' + esc(t('hint')) + ': ' + esc(P.hint) + '</p>' : '';
    return '<div class="nlc-pick" data-slug="' + esc(p.slug) + '"><label class="nlc-f"><span>' + esc(t('price_l')) + '</span><input type="text" inputmode="numeric" autocomplete="off" id="nlc-amt-' + esc(p.slug) + '" data-amt value="' + esc(amt ? nf.format(amt) : '') + '" dir="ltr"></label>'
      + '<div class="nlc-chips">' + ['single', 'additional', 'foreign'].map((k) => '<button type="button" class="nlc-chip' + (b === k ? ' is-on' : '') + '" data-buyer="' + k + '" aria-pressed="' + (b === k) + '">' + esc(t('b_' + k)) + '</button>').join('') + '</div>'
      + '<p class="nlc-tax" data-taxline>' + (amt ? esc(t('tax')) + ': ' + ils(tax(amt, b)) : '') + '</p><p class="nlc-mute nlc-s">' + esc(t('tax_note')) + (b === 'foreign' ? ' ' + esc(t('foreign_note')) : '') + '</p>' + hint + '</div>';
  }
  function vBasket() {
    const list = inCart();
    if (!list.length) return '<p class="nlc-empty">' + esc(t('empty')) + '</p>';
    const first = P && list.indexOf(P.slug) >= 0 ? [P.slug].concat(list.filter((x) => x !== P.slug)) : list;
    return first.map((s, i) => (i === 1 ? '<p class="nlc-other">' + esc(t('other')) + '</p>' : '') + card(S.projects[s])).join('') + '<p class="nlc-legal">' + esc(t('legal')) + '</p>';
  }
  function vSummary(p) {
    const amt = amountOf(p);
    const ed = (k) => '<button type="button" class="nlc-ed nlc-link" data-go="basket" data-open="' + esc(p.slug) + ':' + k + '">' + esc(t('edit')) + '</button>';
    let h = steps(1) + '<div class="nlc-sum">';
    h += row(t('unit'), unitLine(p.unit) ? esc(unitLine(p.unit)) + (p.unit && !p.unit.id ? ' <span class="nlc-tag">' + esc(t('example')) + '</span>' : '') : '<span class="nlc-mute">' + esc(t('unit_open')) + '</span>', '');
    h += row(t('design'), p.design ? esc(designLine(p.design)) : '<span class="nlc-mute">-</span>', '');
    if (p.design && p.design.notes && p.design.notes.length) h += '<ul class="nlc-notes">' + p.design.notes.slice(0, 6).map((n) => '<li>' + esc(n.text || n) + '</li>').join('') + '</ul>';
    h += row(t('services'), svcOn(p).length ? esc(svcOn(p).map((k) => t('svc_' + k) + (p.services[k].pro ? ' (' + p.services[k].pro.name + ')' : '')).join(' · ')) : '<span class="nlc-mute">-</span>', ed('svc'));
    h += row(t('call'), p.call ? esc(callLine(p.call)) : '<span class="nlc-mute">' + esc(t('call_none')) + '</span>', ed('call'));
    if (amt) { h += row(t('price'), ils(amt) + ' <span class="nlc-mute nlc-s">' + esc(t('b_' + p.price.buyer)) + '</span>', ed('price')); h += row(t('tax'), ils(tax(amt, p.price.buyer)), ''); }
    h += '</div><p class="nlc-note">' + esc(t('not_incl')) + '</p>';
    if (p.order) h += '<div class="nlc-sent"><span class="nlc-ref">' + esc(p.order.ref) + '</span> <a class="nlc-ed" href="' + esc(p.order.url) + '#reserve" target="_blank" rel="noopener">' + esc(t('open_order')) + '</a></div>';
    return h;
  }
  function vRequest(p) {
    const f = V.form || {};
    return steps(2) + '<form class="nlc-form" novalidate data-slug="' + esc(p.slug) + '">'
      + '<label class="nlc-f"><span>' + esc(t('f_name')) + '</span><input id="nlc-name" name="name" autocomplete="name" required value="' + esc(f.name || '') + '"></label>'
      + '<label class="nlc-f"><span>' + esc(t('f_phone')) + '</span><input id="nlc-phone" name="phone" type="tel" inputmode="tel" autocomplete="tel" dir="ltr" required value="' + esc(f.phone || '') + '"></label>'
      + '<label class="nlc-f"><span>' + esc(t('f_email')) + '</span><input id="nlc-email" name="email" type="email" autocomplete="email" dir="ltr" value="' + esc(f.email || '') + '"></label>'
      + '<input type="text" name="company" tabindex="-1" autocomplete="off" class="nlc-hp" aria-hidden="true">'
      + '<p class="nlc-priv">' + esc(t('privacy', { project: p.name })) + ' <a href="' + esc(C.privacy) + '" target="_blank" rel="noopener">' + esc(t('privacy_link')) + '</a></p>'
      + '<label class="nlc-ck"><input type="checkbox" id="nlc-consent" name="consent"' + (f.consent ? ' checked' : '') + '><span>' + esc(t('consent', { project: p.name })) + '</span></label>'
      + '<p class="nlc-err" role="alert" aria-live="assertive"></p></form>';
  }
  function vSent(p) {
    const o = p.order || {};
    const when = o.at ? new Date(o.at).toLocaleString(NFL, { day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit' }) : '';
    return steps(3) + '<div class="nlc-ok"><span class="nlc-ref nlc-ref--big">' + esc(o.ref || '') + '</span>'
      + '<div class="nlc-tl"><div><i class="is-ok"></i><span>' + esc(t('st_rfp')) + ' <span class="nlc-mute nlc-s nlc-n">' + esc(when) + '</span></span></div><div><i class="is-wait"></i><span>' + esc(t('st_next')) + (p.call ? ' · ' + esc(callLine(p.call)) : '') + '</span></div><div><i></i><span>' + esc(t('st_offer')) + '</span></div></div>'
      + '<a class="nlc-btn nlc-btn--2" href="' + esc(o.url || '#') + '" target="_blank" rel="noopener">' + esc(t('doc')) + '</a>'
      + '<p class="nlc-note">' + esc(t('reserve_note')) + '</p></div>';
  }
  function vFoot() {
    if (V.view === 'summary') return '<button type="button" class="nlc-btn" data-go="request">' + esc(t('to_request')) + '</button><button type="button" class="nlc-link" data-go="basket">' + esc(t('back')) + '</button>';
    if (V.view === 'request') return '<button type="button" class="nlc-btn" data-send>' + esc(t('send')) + '</button><button type="button" class="nlc-link" data-go="summary">' + esc(t('s1')) + '</button>';
    if (V.view === 'sent') { const o = (S.projects[V.slug] || {}).order || {}; return '<a class="nlc-btn" data-reserve href="' + esc((o.url || '#') + '#reserve') + '" target="_blank" rel="noopener">' + esc(t('to_reserve')) + '</a><button type="button" class="nlc-link" data-go="basket">' + esc(t('back')) + '</button>'; }
    let h = '';
    const p = P ? S.projects[P.slug] : null;
    if (P && !(p && p.in)) h += '<button type="button" class="nlc-btn" data-add>' + esc(p && p.unit ? t('add') : t('add_proj')) + '</button>';
    const sub = [];
    if (C.wa && inCart().length) sub.push('<a class="nlc-link" data-wa href="#" target="_blank" rel="noopener">' + esc(t('wa')) + '</a>');
    if (document.querySelector('a[data-nlps-ev="hero-video"]')) sub.push('<button type="button" class="nlc-link" data-room>' + esc(t('room')) + '</button>');
    if (inCart().length) sub.push('<button type="button" class="nlc-link" data-clear>' + esc(t('clear')) + '</button>');
    return h + (sub.length ? '<div class="nlc-sub">' + sub.join('') + '</div>' : '');
  }

  /* ---------------------------------------------------------------- actions */
  const projOf = (el) => { const a = el.closest('[data-slug]'); return a ? S.projects[a.getAttribute('data-slug')] : (V.slug ? S.projects[V.slug] : null); };
  function waText() {
    const out = [];
    for (const s of inCart()) {
      const p = S.projects[s];
      out.push(t('wa_intro', { project: p.name }));
      if (unitLine(p.unit)) out.push('• ' + t('unit') + ': ' + unitLine(p.unit));
      if (p.design) out.push('• ' + t('design') + ': ' + designLine(p.design));
      if (svcOn(p).length) out.push('• ' + t('services') + ': ' + svcOn(p).map((k) => t('svc_' + k)).join(', '));
      if (p.call) out.push('• ' + t('call') + ': ' + callLine(p.call));
      if (p.order) out.push('• ' + p.order.ref);
    }
    out.push(t('wa_close'));
    return out.join('\n');
  }
  function onClick(e) {
    const el = e.target.closest('button,a');
    if (!el) { if (e.target.hasAttribute && e.target.hasAttribute('data-x')) close(); return; }
    if (el.hasAttribute('data-x')) { close(); return; }
    if (el.hasAttribute('data-add')) { add(false); render(); return; }
    if (el.hasAttribute('data-go')) {
      const to = el.getAttribute('data-go'), s = el.getAttribute('data-slug');
      if (el.getAttribute('data-open')) { V.open = {}; V.open[el.getAttribute('data-open')] = 1; }
      if (to === 'request') { track('rfp_open', { project: V.slug, v: inCart().length }); }
      if (to === 'summary' && s) V.slug = s;
      go(to, s || V.slug);
      return;
    }
    if (el.hasAttribute('data-remove')) { const s = el.getAttribute('data-remove'); if (S.projects[s]) { S.projects[s].in = false; track('basket_remove', { project: s, v: inCart().length }); save(); render(); } return; }
    if (el.hasAttribute('data-clear')) { for (const s of Object.keys(S.projects)) S.projects[s].in = false; save(); render(); return; }
    if (el.hasAttribute('data-wa')) { el.href = 'https://wa.me/' + C.wa + '?text=' + encodeURIComponent(waText()); return; }
    if (el.hasAttribute('data-room')) { close(); const v = document.querySelector('a[data-nlps-ev="hero-video"]'); if (v) v.click(); return; }
    if (el.hasAttribute('data-toggle')) { const k = el.getAttribute('data-toggle'); V.open[k] = !V.open[k]; render(); return; }
    if (el.hasAttribute('data-send')) { send(el); return; }
    if (el.hasAttribute('data-reserve')) { track('reserve_start', { project: V.slug, unit: '' }); return; }
    const p = projOf(el);
    if (!p) return;
    if (el.hasAttribute('data-svc')) { const k = el.getAttribute('data-svc'); if (p.services[k]) delete p.services[k]; else p.services[k] = { pro: null }; save(); render(); return; }
    if (el.hasAttribute('data-loadpros')) { loadPros(p, el.getAttribute('data-loadpros'), el.parentNode); return; }
    if (el.hasAttribute('data-pro')) { const k = el.getAttribute('data-k'); p.services[k] = { pro: el.getAttribute('data-pro') === '0' ? null : { id: Number(el.getAttribute('data-pro')), name: el.getAttribute('data-name') } }; save(); render(); return; }
    if (el.hasAttribute('data-day')) { p.call = Object.assign({ win: '18', ch: 'phone' }, p.call || {}, { day: el.getAttribute('data-day') }); if (new Date(p.call.day + 'T12:00:00').getDay() === 5) p.call.win = '09'; track('call_book', { project: p.slug, k: p.call.ch === 'video' ? 'video' : 'meeting' }); save(); render(); return; }
    if (el.hasAttribute('data-win')) { if (p.call) { p.call.win = el.getAttribute('data-win'); save(); render(); } return; }
    if (el.hasAttribute('data-ch')) { if (p.call) { p.call.ch = el.getAttribute('data-ch'); save(); render(); } return; }
    if (el.hasAttribute('data-buyer')) { p.price.buyer = el.getAttribute('data-buyer'); save(); render(); return; }
  }
  function onInput(e) {
    const a = e.target;
    if (a.hasAttribute('data-amt')) {
      const p = projOf(a); if (!p) return;
      p.price.amount = a.value.replace(/[^\d]/g, '');
      try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (x) { /* none */ }
      const n = amountOf(p), tl = a.closest('.nlc-pick').querySelector('[data-taxline]');
      if (tl) tl.innerHTML = n ? esc(t('tax')) + ': ' + ils(tax(n, p.price.buyer)) : '';
    }
    if (a.form && a.form.classList.contains('nlc-form')) { V.form = V.form || {}; V.form[a.name] = a.type === 'checkbox' ? a.checked : a.value; const er = a.form.querySelector('.nlc-err'); if (er) er.textContent = ''; }
  }
  function onChange(e) {
    const a = e.target;
    if (a.hasAttribute('data-amt')) { const p = projOf(a); if (p) { const n = amountOf(p); a.value = n ? nf.format(n) : ''; save(); } }
    if (a.form && a.form.classList.contains('nlc-form')) { V.form = V.form || {}; V.form[a.name] = a.type === 'checkbox' ? a.checked : a.value; }
  }
  const proCache = {};
  function loadPros(p, k, box) {
    const go2 = (list) => {
      box.innerHTML = (list.length ? list.map((x) => '<button type="button" class="nlc-chip" data-k="' + k + '" data-pro="' + x.id + '" data-name="' + esc(x.name) + '">' + esc(x.name) + (x.city ? ' · ' + esc(x.city) : '') + '</button>').join('') : '')
        + '<button type="button" class="nlc-chip" data-k="' + k + '" data-pro="0">' + esc(t('pro_none')) + '</button>';
      box.classList.add('nlc-chips');
    };
    const ck = k + '|' + (p.city || '');
    if (proCache[ck]) { go2(proCache[ck]); return; }
    box.textContent = '…';
    fetch(C.rest + 'basket/pros?profession=' + encodeURIComponent(PROF[k]) + '&city=' + encodeURIComponent(p.city || ''), { credentials: 'same-origin' })
      .then((r) => r.json()).then((j) => { proCache[ck] = (j && j.pros) || []; go2(proCache[ck]); }).catch(() => go2([]));
  }
  async function send(btn) {
    const p = S.projects[V.slug];
    const form = body.querySelector('.nlc-form');
    const err = body.querySelector('.nlc-err');
    if (!p || !form) return;
    const fN = form.querySelector('#nlc-name'), fP = form.querySelector('#nlc-phone'), fE = form.querySelector('#nlc-email'), fC = form.querySelector('#nlc-consent'), fH = form.querySelector('.nlc-hp');
    const name = fN.value.trim(), phone = fP.value.trim(), email = fE.value.trim(), ok = fC.checked;
    if (name.length < 2 || phone.replace(/\D/g, '').length < 9 || !ok) { err.textContent = t('need'); (name.length < 2 ? fN : phone.replace(/\D/g, '').length < 9 ? fP : fC).focus(); return; }
    btn.disabled = true; const label = btn.textContent; btn.textContent = t('sending'); err.textContent = '';
    const u = p.unit || {};
    const ukey = u.id || [u.floor != null ? 'f' + u.floor : '', u.tower || '', u.bearing != null ? 'b' + u.bearing : ''].filter(Boolean).join('-') || 'open';
    const lines = [t('summary') + ': ' + p.name, t('unit') + ': ' + (unitLine(u) || t('unit_open'))];
    if (p.design) lines.push(t('design') + ': ' + designLine(p.design));
    if (svcOn(p).length) lines.push(t('services') + ': ' + svcOn(p).map((k) => t('svc_' + k)).join(', '));
    if (p.call) lines.push(t('call') + ': ' + callLine(p.call));
    try {
      const r1 = await fetch(C.rest + 'lead', { method: 'POST', headers: { 'Content-Type': 'application/json' }, credentials: 'same-origin', body: JSON.stringify({
        name, phone, email, goal: 'rfp', source: 'cart-rfp-v1', message: lines.join('\n'), project_slug: p.slug, project_title: p.name, unit: ukey,
        floor: u.floor != null ? u.floor : undefined, purchase_intent: 1, consent: 1, consent_text: t('privacy', { project: p.name }) + ' | ' + t('consent', { project: p.name }), company: fH ? fH.value : '',
      }) });
      const j1 = await r1.json();
      if (!r1.ok || !j1 || !j1.lead_id) throw new Error('lead');
      const services = {};
      for (const k of svcOn(p)) services[k] = { pro: p.services[k].pro ? p.services[k].pro.id : 0 };
      const r2 = await fetch(C.rest + 'cart/order', { method: 'POST', headers: { 'Content-Type': 'application/json' }, credentials: 'same-origin', body: JSON.stringify({
        lang: L, project: p.slug, lead_id: j1.lead_id, name: name.split(/\s+/)[0], unit: { floor: u.floor, tower: u.tower, bearing: u.bearing, id: u.id },
        design: p.design || null, services, rent: p.rent || null, call: p.call || null, price: amountOf(p) ? { amount: amountOf(p), buyer: p.price.buyer } : null,
      }) });
      const j2 = await r2.json();
      if (!r2.ok || !j2 || !j2.token) throw new Error('order');
      p.order = { token: j2.token, ref: j2.ref, url: j2.url, status: j2.status, at: Date.now() };
      V.form = {};
      save();
      track('rfp_send', { project: p.slug, v: inCart().length });
      go('sent', p.slug);
    } catch (x) {
      btn.disabled = false; btn.textContent = label; err.textContent = t('err');
    }
  }

  /* ---------------------------------------------------------------- the ways in */
  let chip = null;
  function entryBtn(cls, label, onTap) {
    const b = document.createElement('button');
    b.type = 'button'; b.className = cls; b.setAttribute('aria-haspopup', 'dialog');
    b.innerHTML = '<svg viewBox="0 0 20 20" aria-hidden="true" width="18" height="18"><path d="M3 6h14l-1.4 9.2a1.5 1.5 0 0 1-1.5 1.3H5.9a1.5 1.5 0 0 1-1.5-1.3L3 6Zm4 0V5a3 3 0 0 1 6 0v1" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg><span></span><b class="nlc-badge" hidden>0</b>';
    b.querySelector('span').textContent = label;
    b.querySelector('.nlc-badge').setAttribute('aria-label', t('count'));
    b.addEventListener('click', () => onTap(b));
    return b;
  }
  function mountSlots() {
    document.querySelectorAll('[data-nl-slot="basket"]').forEach((s) => {
      if (s.querySelector('.nlc-slotbtn')) return;
      s.appendChild(entryBtn('nlc-slotbtn', t('name'), (b) => { if (P && !(S.projects[P.slug] && S.projects[P.slug].in)) add(true, b); else open('basket', null, b); }));
    });
  }
  function mount() {
    mountSlots();
    if (P) {
      const stl = document.querySelector('.nlps-steps');
      if (stl && !stl.querySelector('.nlc-stepbtn')) { const li = document.createElement('li'); li.appendChild(entryBtn('nlps-step nlc-stepbtn', t('name'), (b) => open('basket', null, b))); stl.appendChild(li); }
      const cta = document.getElementById('nlps-view-cta');
      if (cta && !cta.querySelector('.nlc-addbtn')) cta.appendChild(entryBtn('nlds-btn nlds-btn--secondary nlc-addbtn', t('add'), (b) => add(true, b)));
    }
    // a small chip where no other way in exists (pages outside the project shell, and every other page once the basket holds something)
    setTimeout(() => {
      if (document.querySelector('.nlc-slotbtn,.nlc-stepbtn')) return;
      chip = entryBtn('nlc-chip-fixed', t('name'), (b) => { if (P && !(S.projects[P.slug] && S.projects[P.slug].in)) add(true, b); else open('basket', null, b); });
      chip.setAttribute('dir', RTL ? 'rtl' : 'ltr');
      document.body.appendChild(chip);
      paint();
    }, P ? 4200 : 0);
    paint();
  }
  window.addEventListener('nadlan:shell-ready', () => { mountSlots(); paint(); });
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount); else mount();

  // the earlier basket's callers (Kikar showroom, cockpit, slice, world): the same doors open this basket
  if (!window.__nlBasket) {
    window.__nlBasket = {
      open: (from) => { if (P && !(S.projects[P.slug] && S.projects[P.slug].in)) add(true, from && from.nodeType ? from : null); else open('basket', null, from && from.nodeType ? from : null); },
      close,
      get state() { const p = P ? S.projects[P.slug] : null; return { unit: p && p.unit ? p.unit : null, style: p ? p.style : null, team: {}, price: p ? p.price : {} }; },
    };
  }
  window.NLCart = {
    add: (item) => { if (item && item.type === 'design') takeDesign(item, true); else if (item && item.type === 'rent') takeRent(item.plan, true); else add(false); open('basket', item && item.project ? item.project : null); },
    open: (view, slug) => open(view || 'basket', slug || null),
    get: () => JSON.parse(JSON.stringify(S)),
    count: () => inCart().length,
  };
  window.dispatchEvent(new CustomEvent('nl:cart', { detail: { ready: true, count: inCart().length } }));
})();
