/* TogetherRoom, the shared viewing room (design system TogetherRoom, version 77, 28.9.2026; inc/together.php).
 *
 * Loaded only on a project page with ?room=<id> (or ?room=new). The room takes the page's own parts full screen: the stage
 * (assets/project-stage/<dir>/stage.js, window.__nlpsStage), the 360 viewer (tour.js, window.__nlTour) and the view from
 * the floor (bridge.js, window.__nlpsView), and lays the room over them: the top bar with the mode switch, the dock with
 * the video tiles, the notes and the apartment's file, numbered pins in the writer's role colour, the representative's
 * named pointer, and the small plan "איפה אתם בדירה" (an example apartment, labelled so).
 *
 * Two transports with one interface: LiveKit (video, and the leader's view over the data channel about ten times a second:
 * lossy topic 'view', reliable topics 'mode' and 'notes'), loaded from the CDN only after the join click; and, without a
 * LiveKit key, the site's REST API (the leader posts the state, the others poll every 1.5 s, like inc/cotour.php). The
 * notes are always stored by the server (/room/notes) and make the file (/room/file, the page ?room=<id>&file=1).
 *
 * Words: five languages (he, en, fr, ru, ar; the direction by the language). The consent line is the design's, as is.
 * NadLan is never presented as a broker or as the developer; every apartment here is an example apartment.
 */

const CFG_EL = document.getElementById('nltg-root');
let CFG = {};
try { CFG = JSON.parse((CFG_EL && CFG_EL.dataset.cfg) || '{}'); } catch (e) { CFG = {}; }
const QS = new URLSearchParams(location.search);
const LANGS = ['he', 'en', 'fr', 'ru', 'ar'];
const MODES = ['building', 'plan', 'inside', 'view'];
const ROLE_CLASS = { rep: 'rep', buyer: 'buyer', partner: 'family', friend: 'family', designer: 'pro', engineer: 'pro', lawyer: 'pro' };
const ROLE_COLOR = { rep: '#1F4B5C', buyer: '#8A6A2E', family: '#2E7D5B', pro: '#6A4C93' };
const JOIN_ROLES = ['buyer', 'partner', 'friend', 'designer', 'engineer', 'lawyer'];
const ga = (name, params) => { try { if (window.nadlanGA) window.nadlanGA(name, params || {}); } catch (e) { /* none */ } };
const reduced = () => !!(window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches);
const phoneMQ = window.matchMedia ? matchMedia('(max-width: 760px)') : { matches: false, addEventListener() {} };

/* ------------------------------------------------------------------ words */

const STR = {
  he: {
    kicker: 'חדר צפייה משותף', sample: 'דירה לדוגמה', floor: 'קומה {n}',
    live: 'בשידור חי · {n} משתתפים', live1: 'בשידור חי · משתתף אחד', sync: 'מחוברים · {n} משתתפים', sync1: 'מחוברים · משתתף אחד', liveShort: 'חי',
    invite: 'הזמנת משתתף', leave: 'יציאה',
    m_building: 'הבניין', m_plan: 'התוכנית והחתכים', m_inside: 'בתוך הדירה', m_view: 'הנוף',
    ms_building: 'הבניין', ms_plan: 'התוכנית', ms_inside: 'בתוך הדירה', ms_view: 'הנוף', modesLbl: 'מה רואים',
    mic: 'מיקרופון', cam: 'מצלמה', follow: 'עקבו אחריי', followStop: 'הפסקת ההובלה',
    notes: 'הערות', people: 'משתתפים',
    addNote: 'הוספת הערה', addNoteSub: 'לוחצים על נקודה בדירה, וההערה נצמדת אליה',
    pickHint: 'לחצו על נקודה בדירה, וההערה תיצמד אליה', cancel: 'ביטול',
    change: 'כפוף לאישור היזם', changeAsk: 'בקשה לשינוי בדירה (כפוף לאישור היזם)',
    newNote: 'הערה חדשה', notePh: 'מה חשוב לזכור כאן? נקודת חשמל, מידה, שינוי', whereLbl: 'איפה בדירה', save: 'שמירת ההערה', del: 'מחיקה',
    noNotes: 'עוד אין הערות. לוחצים על "הוספת הערה", ואחר כך על נקודה בדירה.',
    file: 'תיק הדירה', notesN: '{n} הערות', notes1: 'הערה אחת',
    sendFile: 'שליחת התיק לנציג ולמשתתפים בוואטסאפ', sendFileRep: 'שליחת התיק למשתתפים בוואטסאפ', sendFileShort: 'שליחת תיק הדירה', copy: 'העתקה', copied: 'הועתק',
    consent: 'השיחה אינה מוקלטת. ההערות נשמרות בתיק הדירה. השיחה היא עם צוות נדל״ן, פלטפורמה עצמאית, ואינה מטעם היזם. שינויים בדירה כפופים לאישור היזם.',
    followPill: 'כולם רואים את מה ש{name} מראה', followBack: 'חזרה למה ש{name} מראה', rep: 'הנציג',
    me: 'אני', leading: 'מוביל את המבט', inRoom: 'בחדר', away: 'לא בחדר עכשיו',
    waRep: 'שיחה עם הנציג בוואטסאפ', waitRep: 'הנציג עוד לא בחדר. אפשר לשלוח לו הודעה בוואטסאפ עם הקישור לחדר.',
    waCall: 'שלום, אני בחדר הצפייה המשותף של {project} ואשמח לשיחה עם נציג: {url}',
    joinP: 'נכנסים יחד לדירה לדוגמה: כולם רואים את אותו מבט, והנציג מוביל. כל משתתף יכול להצמיד הערה לנקודה בדירה, וההערות נשמרות בתיק הדירה.',
    nameLbl: 'השם שלכם', namePh: 'השם שיופיע לכולם', roleLbl: 'מי אתם בחדר', withCam: 'להצטרף עם מצלמה', withMic: 'עם מיקרופון',
    enter: 'כניסה לחדר', enterBack: 'כניסה חזרה לחדר', needName: 'כתבו שם, בבקשה.', langLbl: 'שפה',
    e_closed: 'החדר הזה נסגר. אפשר לתאם שיחה חדשה.', e_room: 'לא מצאנו את החדר. בדקו את הקישור.', e_full: 'החדר מלא כרגע.',
    e_rate: 'יותר מדי ניסיונות. נסו שוב בעוד כמה דקות.', e_net: 'אין חיבור לשרת. נסו שוב.', e_role: 'התפקיד הזה שמור לנציגי נדל״ן.',
    e_no_rep: 'אין כרגע נציג זמין לחדר משותף. אפשר לתאם מועד, והנציג ישלח קישור לחדר לפני השיחה.',
    book: 'לתאם מועד', backToPage: 'לעמוד הפרויקט',
    camDenied: 'המצלמה או המיקרופון לא אושרו. אפשר להמשיך בלי.', lkFail: 'הווידאו לא התחבר. ממשיכים בלי וידאו: המבט וההערות מסתנכרנים.',
    audio: 'הפעלת השמע', reconnecting: 'החיבור נקטע. מתחברים שוב…',
    inviteH: 'הזמנת משתתף', inviteP: 'כל מי שמקבל את הקישור נכנס עם שם ותפקיד. בלי הרשמה ובלי סיסמה.', copyLink: 'העתקת הקישור', waShare: 'שליחה בוואטסאפ', share: 'שיתוף',
    inviteText: 'הצטרפו אליי לחדר הצפייה המשותף ב{project}: {url}', close: 'סגירה',
    left: 'יצאתם מהחדר. תיק הדירה נשמר.', openFile: 'לתיק הדירה',
    fileK: 'תיק הדירה · חדר צפייה משותף', fileNone: 'אין הערות בתיק.', joinRoom: 'כניסה לחדר', print: 'הדפסה', fileOpened: 'נפתח ב־{date}',
    miniH: 'איפה אתם בדירה', miniTop: 'למעלה {words}',
    planH: 'התוכנית', cutH: 'החתך', planNote: 'תוכנית סכמטית של דירה לדוגמה, להמחשה בלבד, ואינה תוכנית מכר. בחתך: {n} הקומות של המגדל והקומה שנבחרה.',
    living: 'סלון ומטבח', roomW: 'חדר', windowW: 'חלון',
    spotLiving: 'סלון', spotBalcony: 'מרפסת', wall: 'קיר {dir}', floorW: 'רצפה', ceiling: 'תקרה',
    towerW: 'המגדל · קומה {n}', groundW: 'המגרש', buildingW: 'הבניין', viewW: 'הנוף', planW: 'התוכנית · {room}',
    waFileHead: 'תיק הדירה · חדר צפייה משותף', waFileMore: 'ועוד {n} הערות בתיק המלא', waFileLink: 'התיק המלא: {url}',
    tourCap: 'הדמיית פנים להמחשה בלבד: החלוקה, הגמרים והנוף משוערים ואינם לפי תוכנית מכר.',
  },
  en: {
    kicker: 'Shared viewing room', sample: 'Example apartment', floor: 'Floor {n}',
    live: 'Live · {n} people', live1: 'Live · 1 person', sync: 'Connected · {n} people', sync1: 'Connected · 1 person', liveShort: 'Live',
    invite: 'Invite someone', leave: 'Leave',
    m_building: 'The building', m_plan: 'Plan and section', m_inside: 'Inside the apartment', m_view: 'The view',
    ms_building: 'Building', ms_plan: 'Plan', ms_inside: 'Inside', ms_view: 'View', modesLbl: 'What we see',
    mic: 'Microphone', cam: 'Camera', follow: 'Follow me', followStop: 'Stop leading',
    notes: 'Notes', people: 'People',
    addNote: 'Add a note', addNoteSub: 'Tap a point in the apartment and the note sticks to it',
    pickHint: 'Tap a point in the apartment to pin the note', cancel: 'Cancel',
    change: 'Subject to the developer’s approval', changeAsk: 'A change to the apartment (subject to the developer’s approval)',
    newNote: 'New note', notePh: 'What should we remember here? A socket, a measurement, a change', whereLbl: 'Where', save: 'Save the note', del: 'Delete',
    noNotes: 'No notes yet. Tap “Add a note”, then a point in the apartment.',
    file: 'Apartment file', notesN: '{n} notes', notes1: '1 note',
    sendFile: 'Send the file to the representative and everyone on WhatsApp', sendFileRep: 'Send the file to everyone on WhatsApp', sendFileShort: 'Send the file', copy: 'Copy', copied: 'Copied',
    consent: 'The call is not recorded. The notes are kept in the apartment’s file. The call is with the NadLan team, an independent platform, and is not on behalf of the developer. Changes to the apartment are subject to the developer’s approval.',
    followPill: 'Everyone sees what {name} shows', followBack: 'Back to what {name} shows', rep: 'the representative',
    me: 'Me', leading: 'Leading the view', inRoom: 'In the room', away: 'Not in the room now',
    waRep: 'Call the representative on WhatsApp', waitRep: 'The representative is not in the room yet. You can send a WhatsApp message with the room link.',
    waCall: 'Hello, I am in the shared viewing room of {project} and would like to talk with a representative: {url}',
    joinP: 'Walk through the example apartment together: everyone sees the same view, and the representative leads. Anyone can pin a note to a point in the apartment; the notes are kept in the apartment’s file.',
    nameLbl: 'Your name', namePh: 'The name everyone will see', roleLbl: 'Who are you in the room', withCam: 'Join with camera', withMic: 'with microphone',
    enter: 'Enter the room', enterBack: 'Back into the room', needName: 'Please write a name.', langLbl: 'Language',
    e_closed: 'This room has closed. You can book a new call.', e_room: 'We could not find this room. Please check the link.', e_full: 'The room is full right now.',
    e_rate: 'Too many attempts. Please try again in a few minutes.', e_net: 'No connection to the server. Please try again.', e_role: 'This role is for NadLan representatives.',
    e_no_rep: 'No representative is available for a shared room right now. Book a time, and the representative will send you the room link before the call.',
    book: 'Book a time', backToPage: 'Back to the project page',
    camDenied: 'The camera or microphone was not allowed. You can continue without them.', lkFail: 'Video did not connect. Continuing without video: the view and the notes stay in sync.',
    audio: 'Turn on sound', reconnecting: 'Connection lost. Reconnecting…',
    inviteH: 'Invite someone', inviteP: 'Anyone with the link joins with a name and a role. No sign-up, no password.', copyLink: 'Copy the link', waShare: 'Send on WhatsApp', share: 'Share',
    inviteText: 'Join me in the shared viewing room of {project}: {url}', close: 'Close',
    left: 'You left the room. The apartment file is saved.', openFile: 'Open the file',
    fileK: 'Apartment file · Shared viewing room', fileNone: 'No notes in the file.', joinRoom: 'Enter the room', print: 'Print', fileOpened: 'Opened {date}',
    miniH: 'Where you are', miniTop: 'Top: {words}',
    planH: 'The plan', cutH: 'The section', planNote: 'A schematic plan of an example apartment, for illustration only; not a sales plan. The section shows the tower’s {n} floors and the chosen floor.',
    living: 'Living and kitchen', roomW: 'Room', windowW: 'Window',
    spotLiving: 'Living room', spotBalcony: 'Balcony', wall: '{dir} wall', floorW: 'Floor', ceiling: 'Ceiling',
    towerW: 'Tower · floor {n}', groundW: 'The lot', buildingW: 'The building', viewW: 'The view', planW: 'Plan · {room}',
    waFileHead: 'Apartment file · Shared viewing room', waFileMore: 'and {n} more notes in the full file', waFileLink: 'The full file: {url}',
    tourCap: 'Interior visualisation for illustration only: layout, finishes and view are estimated, not a sales plan.',
  },
  fr: {
    kicker: 'Salle de visite partagée', sample: 'Appartement type', floor: 'Étage {n}',
    live: 'En direct · {n} participants', live1: 'En direct · 1 participant', sync: 'Connectés · {n} participants', sync1: 'Connecté · 1 participant', liveShort: 'Direct',
    invite: 'Inviter', leave: 'Quitter',
    m_building: 'L’immeuble', m_plan: 'Plan et coupe', m_inside: 'Dans l’appartement', m_view: 'La vue',
    ms_building: 'Immeuble', ms_plan: 'Plan', ms_inside: 'Intérieur', ms_view: 'Vue', modesLbl: 'Ce que l’on voit',
    mic: 'Micro', cam: 'Caméra', follow: 'Suivez-moi', followStop: 'Arrêter de guider',
    notes: 'Notes', people: 'Participants',
    addNote: 'Ajouter une note', addNoteSub: 'Touchez un point de l’appartement, la note s’y attache',
    pickHint: 'Touchez un point de l’appartement pour y attacher la note', cancel: 'Annuler',
    change: 'Soumis à l’accord du promoteur', changeAsk: 'Une modification de l’appartement (soumise à l’accord du promoteur)',
    newNote: 'Nouvelle note', notePh: 'À retenir ici : une prise, une mesure, une modification', whereLbl: 'Où', save: 'Enregistrer la note', del: 'Supprimer',
    noNotes: 'Pas encore de notes. Touchez « Ajouter une note », puis un point de l’appartement.',
    file: 'Dossier de l’appartement', notesN: '{n} notes', notes1: '1 note',
    sendFile: 'Envoyer le dossier au conseiller et aux participants sur WhatsApp', sendFileRep: 'Envoyer le dossier aux participants sur WhatsApp', sendFileShort: 'Envoyer le dossier', copy: 'Copier', copied: 'Copié',
    consent: 'L’appel n’est pas enregistré. Les notes sont conservées dans le dossier de l’appartement. L’appel est avec l’équipe NadLan, une plateforme indépendante, et non au nom du promoteur. Toute modification de l’appartement est soumise à l’accord du promoteur.',
    followPill: 'Tout le monde voit ce que montre {name}', followBack: 'Revenir à ce que montre {name}', rep: 'le conseiller',
    me: 'Moi', leading: 'Guide la visite', inRoom: 'Dans la salle', away: 'Absent pour l’instant',
    waRep: 'Appeler le conseiller sur WhatsApp', waitRep: 'Le conseiller n’est pas encore dans la salle. Vous pouvez lui envoyer le lien sur WhatsApp.',
    waCall: 'Bonjour, je suis dans la salle de visite partagée de {project} et j’aimerais parler à un conseiller : {url}',
    joinP: 'Visitez ensemble l’appartement type : tout le monde voit la même vue, et le conseiller guide. Chacun peut attacher une note à un point de l’appartement ; les notes sont gardées dans le dossier.',
    nameLbl: 'Votre nom', namePh: 'Le nom visible par tous', roleLbl: 'Qui êtes-vous', withCam: 'Avec caméra', withMic: 'avec micro',
    enter: 'Entrer dans la salle', enterBack: 'Revenir dans la salle', needName: 'Indiquez un nom, s’il vous plaît.', langLbl: 'Langue',
    e_closed: 'Cette salle est fermée. Vous pouvez prendre un nouveau rendez-vous.', e_room: 'Salle introuvable. Vérifiez le lien.', e_full: 'La salle est pleine pour le moment.',
    e_rate: 'Trop de tentatives. Réessayez dans quelques minutes.', e_net: 'Pas de connexion au serveur. Réessayez.', e_role: 'Ce rôle est réservé aux conseillers NadLan.',
    e_no_rep: 'Aucun conseiller n’est disponible pour le moment. Prenez rendez-vous ; le conseiller vous enverra le lien de la salle avant l’appel.',
    book: 'Prendre rendez-vous', backToPage: 'Retour à la page du projet',
    camDenied: 'Caméra ou micro non autorisés. Vous pouvez continuer sans.', lkFail: 'La vidéo ne s’est pas connectée. On continue sans vidéo : la vue et les notes restent synchronisées.',
    audio: 'Activer le son', reconnecting: 'Connexion perdue. Reconnexion…',
    inviteH: 'Inviter', inviteP: 'Toute personne ayant le lien entre avec un nom et un rôle. Sans inscription ni mot de passe.', copyLink: 'Copier le lien', waShare: 'Envoyer sur WhatsApp', share: 'Partager',
    inviteText: 'Rejoignez-moi dans la salle de visite partagée de {project} : {url}', close: 'Fermer',
    left: 'Vous avez quitté la salle. Le dossier est enregistré.', openFile: 'Ouvrir le dossier',
    fileK: 'Dossier de l’appartement · Salle de visite partagée', fileNone: 'Aucune note dans le dossier.', joinRoom: 'Entrer dans la salle', print: 'Imprimer', fileOpened: 'Ouvert le {date}',
    miniH: 'Où vous êtes', miniTop: 'En haut : {words}',
    planH: 'Le plan', cutH: 'La coupe', planNote: 'Plan schématique d’un appartement type, à titre d’illustration ; ce n’est pas un plan de vente. La coupe montre les {n} étages de la tour et l’étage choisi.',
    living: 'Séjour et cuisine', roomW: 'Chambre', windowW: 'Fenêtre',
    spotLiving: 'Séjour', spotBalcony: 'Balcon', wall: 'Mur {dir}', floorW: 'Sol', ceiling: 'Plafond',
    towerW: 'Tour · étage {n}', groundW: 'Le terrain', buildingW: 'L’immeuble', viewW: 'La vue', planW: 'Plan · {room}',
    waFileHead: 'Dossier de l’appartement · Salle de visite partagée', waFileMore: 'et {n} autres notes dans le dossier complet', waFileLink: 'Le dossier complet : {url}',
    tourCap: 'Visualisation intérieure à titre d’illustration : agencement, finitions et vue estimés, pas un plan de vente.',
  },
  ru: {
    kicker: 'Общий просмотр', sample: 'Пример квартиры', floor: 'Этаж {n}',
    live: 'В эфире · участников: {n}', live1: 'В эфире · 1 участник', sync: 'На связи · участников: {n}', sync1: 'На связи · 1 участник', liveShort: 'Эфир',
    invite: 'Пригласить', leave: 'Выйти',
    m_building: 'Здание', m_plan: 'План и разрез', m_inside: 'В квартире', m_view: 'Вид',
    ms_building: 'Здание', ms_plan: 'План', ms_inside: 'Внутри', ms_view: 'Вид', modesLbl: 'Что смотрим',
    mic: 'Микрофон', cam: 'Камера', follow: 'Следуйте за мной', followStop: 'Перестать вести',
    notes: 'Заметки', people: 'Участники',
    addNote: 'Добавить заметку', addNoteSub: 'Нажмите на точку в квартире, и заметка прикрепится к ней',
    pickHint: 'Нажмите на точку в квартире, чтобы прикрепить заметку', cancel: 'Отмена',
    change: 'Требует согласия застройщика', changeAsk: 'Изменение в квартире (требует согласия застройщика)',
    newNote: 'Новая заметка', notePh: 'Что запомнить здесь: розетка, размер, изменение', whereLbl: 'Где', save: 'Сохранить заметку', del: 'Удалить',
    noNotes: 'Заметок пока нет. Нажмите «Добавить заметку», затем точку в квартире.',
    file: 'Папка квартиры', notesN: 'Заметок: {n}', notes1: '1 заметка',
    sendFile: 'Отправить папку представителю и участникам в WhatsApp', sendFileRep: 'Отправить папку участникам в WhatsApp', sendFileShort: 'Отправить папку', copy: 'Копировать', copied: 'Скопировано',
    consent: 'Звонок не записывается. Заметки сохраняются в папке квартиры. Звонок проводит команда NadLan, независимая платформа, не от имени застройщика. Изменения в квартире требуют согласия застройщика.',
    followPill: 'Все видят то, что показывает {name}', followBack: 'Вернуться к показу {name}', rep: 'представитель',
    me: 'Я', leading: 'Ведёт показ', inRoom: 'В комнате', away: 'Сейчас не в комнате',
    waRep: 'Позвонить представителю в WhatsApp', waitRep: 'Представитель ещё не в комнате. Можно отправить ему ссылку в WhatsApp.',
    waCall: 'Здравствуйте, я в комнате общего просмотра {project} и хочу поговорить с представителем: {url}',
    joinP: 'Смотрим пример квартиры вместе: все видят одно и то же, ведёт представитель. Каждый может прикрепить заметку к точке в квартире; заметки хранятся в папке квартиры.',
    nameLbl: 'Ваше имя', namePh: 'Имя, которое увидят все', roleLbl: 'Кто вы в комнате', withCam: 'С камерой', withMic: 'с микрофоном',
    enter: 'Войти в комнату', enterBack: 'Вернуться в комнату', needName: 'Пожалуйста, укажите имя.', langLbl: 'Язык',
    e_closed: 'Комната закрыта. Можно назначить новый звонок.', e_room: 'Комната не найдена. Проверьте ссылку.', e_full: 'Комната сейчас заполнена.',
    e_rate: 'Слишком много попыток. Попробуйте через несколько минут.', e_net: 'Нет связи с сервером. Попробуйте ещё раз.', e_role: 'Эта роль только для представителей NadLan.',
    e_no_rep: 'Сейчас нет свободного представителя. Назначьте время, и представитель пришлёт ссылку на комнату перед звонком.',
    book: 'Назначить время', backToPage: 'К странице проекта',
    camDenied: 'Камера или микрофон не разрешены. Можно продолжить без них.', lkFail: 'Видео не подключилось. Продолжаем без видео: вид и заметки синхронизируются.',
    audio: 'Включить звук', reconnecting: 'Связь прервалась. Подключаемся…',
    inviteH: 'Пригласить', inviteP: 'Любой, у кого есть ссылка, входит с именем и ролью. Без регистрации и пароля.', copyLink: 'Копировать ссылку', waShare: 'Отправить в WhatsApp', share: 'Поделиться',
    inviteText: 'Присоединяйтесь к общему просмотру {project}: {url}', close: 'Закрыть',
    left: 'Вы вышли из комнаты. Папка квартиры сохранена.', openFile: 'Открыть папку',
    fileK: 'Папка квартиры · Общий просмотр', fileNone: 'В папке нет заметок.', joinRoom: 'Войти в комнату', print: 'Печать', fileOpened: 'Открыта {date}',
    miniH: 'Где вы в квартире', miniTop: 'Сверху: {words}',
    planH: 'План', cutH: 'Разрез', planNote: 'Схематический план примерной квартиры, только для иллюстрации; не план продажи. На разрезе {n} этажей башни и выбранный этаж.',
    living: 'Гостиная и кухня', roomW: 'Комната', windowW: 'Окно',
    spotLiving: 'Гостиная', spotBalcony: 'Балкон', wall: '{dir} стена', floorW: 'Пол', ceiling: 'Потолок',
    towerW: 'Башня · этаж {n}', groundW: 'Участок', buildingW: 'Здание', viewW: 'Вид', planW: 'План · {room}',
    waFileHead: 'Папка квартиры · Общий просмотр', waFileMore: 'и ещё {n} заметок в полной папке', waFileLink: 'Полная папка: {url}',
    tourCap: 'Визуализация интерьера только для иллюстрации: планировка, отделка и вид приблизительны, это не план продажи.',
  },
  ar: {
    kicker: 'غرفة مشاهدة مشتركة', sample: 'شقة نموذجية', floor: 'الطابق {n}',
    live: 'بث مباشر · {n} مشاركين', live1: 'بث مباشر · مشارك واحد', sync: 'متصلون · {n} مشاركين', sync1: 'متصل · مشارك واحد', liveShort: 'مباشر',
    invite: 'دعوة مشارك', leave: 'خروج',
    m_building: 'المبنى', m_plan: 'المخطط والمقاطع', m_inside: 'داخل الشقة', m_view: 'الإطلالة',
    ms_building: 'المبنى', ms_plan: 'المخطط', ms_inside: 'داخل الشقة', ms_view: 'الإطلالة', modesLbl: 'ماذا نرى',
    mic: 'ميكروفون', cam: 'كاميرا', follow: 'اتبعوني', followStop: 'إيقاف القيادة',
    notes: 'ملاحظات', people: 'المشاركون',
    addNote: 'إضافة ملاحظة', addNoteSub: 'اضغطوا على نقطة في الشقة فتلتصق الملاحظة بها',
    pickHint: 'اضغطوا على نقطة في الشقة لتثبيت الملاحظة', cancel: 'إلغاء',
    change: 'خاضع لموافقة المطوّر', changeAsk: 'طلب تغيير في الشقة (خاضع لموافقة المطوّر)',
    newNote: 'ملاحظة جديدة', notePh: 'ما الذي يجب تذكره هنا؟ مقبس كهرباء، قياس، تغيير', whereLbl: 'أين', save: 'حفظ الملاحظة', del: 'حذف',
    noNotes: 'لا توجد ملاحظات بعد. اضغطوا "إضافة ملاحظة" ثم نقطة في الشقة.',
    file: 'ملف الشقة', notesN: '{n} ملاحظات', notes1: 'ملاحظة واحدة',
    sendFile: 'إرسال الملف إلى الممثل والمشاركين عبر واتساب', sendFileRep: 'إرسال الملف إلى المشاركين عبر واتساب', sendFileShort: 'إرسال ملف الشقة', copy: 'نسخ', copied: 'تم النسخ',
    consent: 'المكالمة لا تُسجَّل. تُحفظ الملاحظات في ملف الشقة. المكالمة مع فريق NadLan، منصة مستقلة، وليست باسم المطوّر. أي تغيير في الشقة يخضع لموافقة المطوّر.',
    followPill: 'الجميع يرى ما يعرضه {name}', followBack: 'العودة إلى ما يعرضه {name}', rep: 'الممثل',
    me: 'أنا', leading: 'يقود العرض', inRoom: 'في الغرفة', away: 'ليس في الغرفة الآن',
    waRep: 'مكالمة الممثل عبر واتساب', waitRep: 'الممثل ليس في الغرفة بعد. يمكن إرسال رابط الغرفة إليه عبر واتساب.',
    waCall: 'مرحبًا، أنا في غرفة المشاهدة المشتركة لـ{project} وأرغب بالتحدث مع ممثل: {url}',
    joinP: 'ندخل معًا إلى الشقة النموذجية: الجميع يرى المشهد نفسه، والممثل يقود. يمكن لكل مشارك تثبيت ملاحظة على نقطة في الشقة، وتُحفظ الملاحظات في ملف الشقة.',
    nameLbl: 'اسمكم', namePh: 'الاسم الذي سيظهر للجميع', roleLbl: 'من أنتم في الغرفة', withCam: 'الانضمام بالكاميرا', withMic: 'بالميكروفون',
    enter: 'دخول الغرفة', enterBack: 'العودة إلى الغرفة', needName: 'اكتبوا اسمًا من فضلكم.', langLbl: 'اللغة',
    e_closed: 'أُغلقت هذه الغرفة. يمكن تحديد مكالمة جديدة.', e_room: 'لم نجد الغرفة. تحققوا من الرابط.', e_full: 'الغرفة ممتلئة حاليًا.',
    e_rate: 'محاولات كثيرة. حاولوا بعد بضع دقائق.', e_net: 'لا اتصال بالخادم. حاولوا مرة أخرى.', e_role: 'هذا الدور مخصص لممثلي NadLan.',
    e_no_rep: 'لا يوجد ممثل متاح الآن لغرفة مشتركة. حددوا موعدًا، وسيرسل الممثل رابط الغرفة قبل المكالمة.',
    book: 'تحديد موعد', backToPage: 'إلى صفحة المشروع',
    camDenied: 'لم يُسمح بالكاميرا أو الميكروفون. يمكن المتابعة بدونهما.', lkFail: 'لم يتصل الفيديو. نتابع بدون فيديو: المشهد والملاحظات متزامنة.',
    audio: 'تشغيل الصوت', reconnecting: 'انقطع الاتصال. نعيد الاتصال…',
    inviteH: 'دعوة مشارك', inviteP: 'كل من يتلقى الرابط يدخل باسم ودور. بلا تسجيل وبلا كلمة مرور.', copyLink: 'نسخ الرابط', waShare: 'إرسال عبر واتساب', share: 'مشاركة',
    inviteText: 'انضموا إليّ في غرفة المشاهدة المشتركة لـ{project}: {url}', close: 'إغلاق',
    left: 'خرجتم من الغرفة. ملف الشقة محفوظ.', openFile: 'إلى ملف الشقة',
    fileK: 'ملف الشقة · غرفة مشاهدة مشتركة', fileNone: 'لا ملاحظات في الملف.', joinRoom: 'دخول الغرفة', print: 'طباعة', fileOpened: 'فُتح في {date}',
    miniH: 'أين أنتم في الشقة', miniTop: 'في الأعلى: {words}',
    planH: 'المخطط', cutH: 'المقطع', planNote: 'مخطط تخطيطي لشقة نموذجية للتوضيح فقط، وليس مخطط بيع. في المقطع: طوابق البرج الـ{n} والطابق المختار.',
    living: 'صالون ومطبخ', roomW: 'غرفة', windowW: 'نافذة',
    spotLiving: 'الصالون', spotBalcony: 'الشرفة', wall: 'الجدار {dir}', floorW: 'الأرضية', ceiling: 'السقف',
    towerW: 'البرج · الطابق {n}', groundW: 'القطعة', buildingW: 'المبنى', viewW: 'الإطلالة', planW: 'المخطط · {room}',
    waFileHead: 'ملف الشقة · غرفة مشاهدة مشتركة', waFileMore: 'و{n} ملاحظات أخرى في الملف الكامل', waFileLink: 'الملف الكامل: {url}',
    tourCap: 'تصور داخلي للتوضيح فقط: التقسيم والتشطيبات والإطلالة تقديرية وليست وفق مخطط البيع.',
  },
};
const ROLES = {
  he: { long: { rep: 'נציג או נציגת נדל״ן', buyer: 'קונה', partner: 'בן או בת זוג', friend: 'חבר או חברה', designer: 'מעצב או מעצבת פנים', engineer: 'מהנדס או מהנדסת', lawyer: 'עורך או עורכת דין' },
    short: { rep: 'נציג נדל״ן', buyer: 'קונה', partner: 'בן/בת זוג', friend: 'חבר/ה', designer: 'מעצב/ת פנים', engineer: 'מהנדס/ת', lawyer: 'עו״ד' } },
  en: { long: { rep: 'NadLan representative', buyer: 'Buyer', partner: 'Partner', friend: 'Friend', designer: 'Interior designer', engineer: 'Engineer', lawyer: 'Lawyer' },
    short: { rep: 'NadLan rep', buyer: 'Buyer', partner: 'Partner', friend: 'Friend', designer: 'Designer', engineer: 'Engineer', lawyer: 'Lawyer' } },
  fr: { long: { rep: 'Conseiller NadLan', buyer: 'Acheteur', partner: 'Conjoint', friend: 'Ami', designer: 'Architecte d’intérieur', engineer: 'Ingénieur', lawyer: 'Avocat' },
    short: { rep: 'Conseiller', buyer: 'Acheteur', partner: 'Conjoint', friend: 'Ami', designer: 'Designer', engineer: 'Ingénieur', lawyer: 'Avocat' } },
  ru: { long: { rep: 'Представитель NadLan', buyer: 'Покупатель', partner: 'Супруг(а)', friend: 'Друг', designer: 'Дизайнер интерьера', engineer: 'Инженер', lawyer: 'Юрист' },
    short: { rep: 'Представитель', buyer: 'Покупатель', partner: 'Супруг(а)', friend: 'Друг', designer: 'Дизайнер', engineer: 'Инженер', lawyer: 'Юрист' } },
  ar: { long: { rep: 'ممثل NadLan', buyer: 'مشترٍ', partner: 'شريك أو شريكة', friend: 'صديق', designer: 'مصمم داخلي', engineer: 'مهندس', lawyer: 'محامٍ' },
    short: { rep: 'ممثل NadLan', buyer: 'مشترٍ', partner: 'شريك/ة', friend: 'صديق', designer: 'مصمم', engineer: 'مهندس', lawyer: 'محامٍ' } },
};
const COMPASS = {
  he: { n: 'צפוני', e: 'מזרחי', s: 'דרומי', w: 'מערבי' }, en: { n: 'North', e: 'East', s: 'South', w: 'West' },
  fr: { n: 'nord', e: 'est', s: 'sud', w: 'ouest' }, ru: { n: 'Северная', e: 'Восточная', s: 'Южная', w: 'Западная' },
  ar: { n: 'الشمالي', e: 'الشرقي', s: 'الجنوبي', w: 'الغربي' },
};
const FACING = {
  en: { n: 'facing north', e: 'facing east', s: 'facing south', w: 'facing west' }, fr: { n: 'côté nord', e: 'côté est', s: 'côté sud', w: 'côté ouest' },
  ru: { n: 'на север', e: 'на восток', s: 'на юг', w: 'на запад' }, ar: { n: 'نحو الشمال', e: 'نحو الشرق', s: 'نحو الجنوب', w: 'نحو الغرب' },
};

let LANG = (() => {
  const q = QS.get('lang');
  let s = null;
  try { s = sessionStorage.getItem('nltg:lang'); } catch (e) { s = null; }
  return LANGS.includes(q) ? q : (LANGS.includes(s) ? s : (LANGS.includes(CFG.lang) ? CFG.lang : 'he'));
})();
const RTL = () => LANG === 'he' || LANG === 'ar';
function t(key, vars) {
  let s = (STR[LANG] && STR[LANG][key]) || STR.he[key] || key;
  if (vars) for (const k in vars) s = s.split('{' + k + '}').join(String(vars[k]));
  return s;
}
/* the project's name in the room's language: the page's English name for the other languages, when it has one */
const PN = () => (LANG !== 'he' && LANG !== 'ar' && CFG.nameEn ? CFG.nameEn : CFG.name) || '';
const roleLong = (r) => (ROLES[LANG] || ROLES.he).long[r] || r;
const roleShort = (r) => (ROLES[LANG] || ROLES.he).short[r] || r;
const rc = (r) => ROLE_CLASS[r] || 'buyer';
const initial = (name) => (String(name || '?').trim()[0] || '?').toUpperCase();
const hhmm = (sec) => { try { return new Date(sec * 1000).toLocaleTimeString(LANG === 'he' ? 'he-IL' : LANG, { hour: '2-digit', minute: '2-digit' }); } catch (e) { return ''; } };

/* ------------------------------------------------------------------ the page's parts */

const PS = (() => { try { return JSON.parse(document.getElementById('nlps').dataset.cfg || '{}'); } catch (e) { return {}; } })();
const UNITS = Array.isArray(PS.units) ? PS.units.map((u) => ({ id: String(u[0]), bearing: Number(u[1]) })) : [];
const SEA = (UNITS.find((u) => u.id === 'w') || UNITS[0] || { id: 'w' }).id;
const norm = (b) => ((Number(b) % 360) + 360) % 360;
const sideBearing = (side) => { const u = UNITS.find((x) => x.id === side); return u ? u.bearing : ({ n: 0, e: 90, s: 180, w: 270 }[side] || 270); };
const compassOf = (b) => ['n', 'e', 's', 'w'][Math.round(norm(b) / 90) % 4];
function facingWords(side) {
  if (!side) return '';
  if (LANG !== 'he') return (FACING[LANG] || FACING.en)[compassOf(sideBearing(side))] || '';
  const x = norm(sideBearing(side));
  for (const s of (Array.isArray(PS.sectors) ? PS.sectors : [])) {
    const from = norm(s[0]), to = norm(s[1]);
    if (from <= to ? (x >= from && x < to) : (x >= from || x < to)) return String(s[2]);
  }
  return '';
}
const stage = () => window.__nlpsStage || null;
const tour = () => window.__nlTour || null;
const view = () => window.__nlpsView || null;
function currentSel() {
  let sel = null;
  try { sel = stage() && stage().getSelection ? stage().getSelection() : null; } catch (e) { sel = null; }
  if (sel && sel.floor) return { floor: sel.floor, side: sel.unit ? String(sel.unit).split('-')[1] : (ST.sel.side || SEA), unit: sel.unit || null };
  return { floor: ST.sel.floor || null, side: ST.sel.side || null, unit: ST.sel.unit || null };
}
const tourScenes = (() => {
  const b = document.querySelector('[data-nlps-tour]');
  try { return JSON.parse((b && b.getAttribute('data-nlps-tour-scenes')) || '[]') || []; } catch (e) { return []; }
})();
const tourFloors = [...new Set(tourScenes.map((x) => Number(x.floor) || 25))].sort((a, b) => a - b);
const nearestTourFloor = (f) => (tourFloors.length ? tourFloors.reduce((b, x) => (Math.abs(x - f) < Math.abs(b - f) ? x : b), tourFloors[0]) : 25);
const tourModuleUrl = () => {
  const s = document.getElementById('nadlan-ps-bridge');
  return s && s.src ? s.src.replace(/bridge\.js(\?|$)/, 'tour.js$1') : null;
};
function towerFloors() {
  const s = stage();
  if (!s || typeof s.floorHeight !== 'function') return 0;
  let n = 0;
  while (n < 150 && s.floorHeight(n + 1) != null) n++;
  return n;
}

/* ------------------------------------------------------------------ state */

const ST = {
  room: '', me: null, joined: false, mode: 'building', tab: 'notes', notes: [], rev: -1, people: [],
  leader: '', leaderName: '', following: true, lastState: null, lastSent: '', lastSentAt: 0,
  sel: { floor: null, side: null, unit: null }, focus: null, armed: false, temp: null,
  applying: false, modeBusy: false, openingTour: false, closingTour: false,
  mouse: null, myPointer: null, speaking: new Set(), created: false, wantMic: true, wantCam: true,
};
let T = null; // the transport
const amLeader = () => !!(ST.me && ST.leader && ST.leader === ST.me.pid);
const following = () => !!(ST.me && ST.leader && ST.leader !== ST.me.pid && ST.following);

/* ------------------------------------------------------------------ REST */

async function api(method, path, body) {
  const url = new URL(path, CFG.rest || '/wp-json/nadlan/v1/');
  const o = { method, headers: { Accept: 'application/json' }, credentials: 'same-origin' };
  if (CFG.nonce) o.headers['X-WP-Nonce'] = CFG.nonce;
  if (body && body.__keepalive) { o.keepalive = true; body = Object.assign({}, body); delete body.__keepalive; } // survives the page closing
  if (method === 'GET' && body) for (const k in body) if (body[k] != null) url.searchParams.set(k, body[k]);
  if (method !== 'GET') { o.headers['Content-Type'] = 'application/json'; o.body = JSON.stringify(body || {}); }
  let r;
  try { r = await fetch(url.toString(), o); } catch (e) { return { ok: false, error: 'net', status: 0 }; }
  let j = null;
  try { j = await r.json(); } catch (e) { j = null; }
  if (!j || typeof j !== 'object') return { ok: false, error: 'net', status: r.status };
  if (!r.ok && j.ok !== false) j.ok = false;
  j.status = r.status;
  if (!r.ok && !j.error) j.error = j.code || 'net';
  return j;
}
const credsKey = () => 'nltg:' + ST.room;
function saveCreds() { try { sessionStorage.setItem(credsKey(), JSON.stringify(ST.me)); } catch (e) { /* private mode */ } }
function loadCreds() { try { return JSON.parse(sessionStorage.getItem(credsKey()) || 'null'); } catch (e) { return null; } }

/* ------------------------------------------------------------------ DOM helpers */

function h(tag, attrs, ...kids) {
  const el = document.createElement(tag);
  if (attrs) for (const k in attrs) {
    const v = attrs[k];
    if (v == null || v === false) continue;
    if (k === 'class') el.className = v;
    else if (k === 'text') el.textContent = v;
    else if (k.startsWith('on') && typeof v === 'function') el.addEventListener(k.slice(2), v);
    else if (k === 'style' && typeof v === 'object') Object.assign(el.style, v);
    else el.setAttribute(k, v === true ? '' : String(v));
  }
  for (const c of kids.flat()) if (c != null && c !== false) el.append(c instanceof Node ? c : document.createTextNode(String(c)));
  return el;
}
const ICONS = {
  link: '<path d="M10 14a5 5 0 0 0 7 0l3-3a5 5 0 0 0-7-7l-1 1M14 10a5 5 0 0 0-7 0l-3 3a5 5 0 0 0 7 7l1-1" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/>',
  mic: '<rect x="9" y="3" width="6" height="11" rx="3" fill="none" stroke="currentColor" stroke-width="2"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
  micOff: '<path d="M3 3l18 18M9 9v3a3 3 0 0 0 5 2M15 10V5a3 3 0 0 0-6 0M5 11a7 7 0 0 0 11 5.7M19 11a7 7 0 0 1-.6 2.8M12 18v3" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
  cam: '<rect x="3" y="6" width="13" height="12" rx="2.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M16 10l5-3v10l-5-3z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>',
  camOff: '<path d="M3 3l18 18M16 16v0a2 2 0 0 1-2 2H5.5A2.5 2.5 0 0 1 3 15.5v-7A2.5 2.5 0 0 1 5.5 6H6M10 6h3.5A2.5 2.5 0 0 1 16 8.5v2l5-3v10" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
  wa: '<path d="M12 3a9 9 0 0 0-7.8 13.5L3 21l4.6-1.2A9 9 0 1 0 12 3z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M8.8 8.6c.2-.5.5-.5.8-.5h.5c.2 0 .4 0 .6.5l.7 1.7c.1.2 0 .5-.1.6l-.5.6c-.1.2-.2.3 0 .6.5.9 1.3 1.7 2.3 2.2.3.1.4.1.6-.1l.6-.7c.2-.2.4-.2.6-.1l1.6.8c.3.1.4.3.3.6-.1.8-.9 1.5-1.7 1.6-1.9.2-5.6-1.7-6.4-5-.2-.9 0-1.8.1-2.2z" fill="currentColor"/>',
  copy: '<rect x="8" y="8" width="12" height="12" rx="2.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M16 8V6a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h2" fill="none" stroke="currentColor" stroke-width="2"/>',
  eye: '<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="3" fill="none" stroke="currentColor" stroke-width="2"/>',
  x: '<path d="M6 6l12 12M18 6L6 18" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/>',
  down: '<path d="M6 9l6 6 6-6" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>',
};
function icon(name, size) {
  const s = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  s.setAttribute('viewBox', '0 0 24 24'); s.setAttribute('class', 'nltg-ico'); s.setAttribute('aria-hidden', 'true');
  if (size) { s.setAttribute('width', size); s.setAttribute('height', size); s.style.width = size + 'px'; s.style.height = size + 'px'; }
  s.innerHTML = ICONS[name] || '';
  return s;
}
function roleChip(role, short) { return h('span', { class: 'nltg-role nltg-r-' + rc(role), text: short === false ? roleLong(role) : roleShort(role) }); }
async function copyText(s) {
  try { await navigator.clipboard.writeText(s); return true; } catch (e) {
    try { const ta = h('textarea', { style: { position: 'fixed', opacity: '0' } }); ta.value = s; document.body.append(ta); ta.select(); const ok = document.execCommand('copy'); ta.remove(); return ok; } catch (e2) { return false; }
  }
}
function waHref(text, toSite) { return 'https://wa.me/' + (toSite && CFG.wa ? CFG.wa : '') + '?text=' + encodeURIComponent(text); }
const joinUrl = () => { const u = new URL(CFG.url || location.href); u.search = ''; u.hash = ''; u.searchParams.set('room', ST.room); return u.toString(); };
const fileUrl = () => { const u = new URL(joinUrl()); u.searchParams.set('file', '1'); return u.toString(); };

/* ------------------------------------------------------------------ the frame: the view layer and the room */

const VP = h('div', { class: 'nltg-vp', 'aria-hidden': 'false' });
const LAYER = { building: h('div', { class: 'nltg-layer' }), view: h('div', { class: 'nltg-layer is-off' }), plan: h('div', { class: 'nltg-layer is-off' }) };
VP.append(LAYER.building, LAYER.view, LAYER.plan);
const R = h('div', { class: 'nltg', id: 'nltg' });
const moved = [];
function adopt(el, into) {
  if (!el || !el.parentNode) return;
  const ph = document.createComment('nltg');
  el.parentNode.insertBefore(ph, el);
  into.append(el);
  moved.push([el, ph]);
}
function restore() {
  for (const [el, ph] of moved.splice(0)) { if (ph.parentNode) { ph.parentNode.insertBefore(el, ph); ph.remove(); } }
}

let UI = {};
function applyDir() {
  R.dir = RTL() ? 'rtl' : 'ltr';
  R.lang = LANG;
}

/* ------------------------------------------------------------------ boot */

async function boot() {
  if (!CFG_EL) return;
  ST.room = String(QS.get('room') || '').toLowerCase();
  document.documentElement.classList.add('nltg-on', 'nltg-m-building');
  applyDir();
  document.body.append(VP, R);
  adopt(document.getElementById('nlps'), LAYER.building);
  adopt(document.querySelector('.nlps-viewwrap'), LAYER.view);
  reframe();
  if (QS.get('file') === '1' && /^[a-z2-7]{12}$/.test(ST.room)) { showFile(); return; }
  if (ST.room === 'new') {
    const ok = await createRoom();
    if (!ok) return;
  }
  if (!/^[a-z2-7]{12}$/.test(ST.room)) { showNotice(t('e_room')); return; }
  showJoin();
}

async function createRoom() {
  const r = await api('POST', 'room', { post: CFG.post });
  if (!r.ok) {
    showNotice(t(r.error === 'no_rep' ? 'e_no_rep' : (r.error === 'rate' ? 'e_rate' : 'e_net')), r.error === 'no_rep');
    return false;
  }
  ST.room = r.room;
  ST.created = true;
  try { const u = new URL(location.href); u.searchParams.set('room', r.room); history.replaceState(history.state, '', u.pathname + u.search + u.hash); } catch (e) { /* keep */ }
  ga('room_create', { project: CFG.name, by: CFG.canRep ? 'rep' : 'buyer' });
  return true;
}

/* the stage changed its box (the page's column, the full screen): once its size is taken, the opening view for that size */
function reframe() {
  waitFor(() => stage(), 20000).then((s) => {
    if (!s) return;
    Promise.resolve(s.ready).then(() => requestAnimationFrame(() => requestAnimationFrame(() => { try { if (s.home) s.home(0); } catch (e) { /* none */ } })));
  });
}

/* a message instead of the room (closed, not found, no representative): back to the page, or the booking band */
function showNotice(msg, withBook) {
  R.textContent = '';
  const card = h('div', { class: 'nltg-card', role: 'dialog', 'aria-modal': 'true', 'aria-label': t('kicker') },
    h('div', { class: 'k', text: t('kicker') + ' · ' + t('sample') }),
    h('div', { class: 'h', text: PN() || '' }),
    h('div', { class: 'p', text: msg }),
    h('div', { class: 'row' },
      withBook || document.getElementById('nlsch') ? h('button', { type: 'button', class: 'nltg-btn teal', text: t('book'), onclick: () => leave(true, '#nlsch') }) : null,
      CFG.wa ? h('a', { class: 'nltg-btn wa', href: waHref(t('waCall', { project: PN(), url: CFG.url }), true), target: '_blank', rel: 'noopener' }, icon('wa'), t('waRep')) : null,
      h('button', { type: 'button', class: 'nltg-btn', text: t('backToPage'), onclick: () => leave(true) })));
  R.append(h('div', { class: 'nltg-scrim' }, card));
  const f = card.querySelector('button, a'); if (f) f.focus();
}

/* ------------------------------------------------------------------ joining */

function showJoin(err) {
  R.textContent = '';
  applyDir();
  const saved = loadCreds();
  let role = (saved && saved.role) || (CFG.canRep && ST.created ? 'rep' : 'buyer');
  if (role === 'rep' && !CFG.canRep) role = 'buyer';
  const name = h('input', { class: 'nltg-in', id: 'nltg-name', type: 'text', maxlength: '40', autocomplete: 'given-name', placeholder: t('namePh') });
  name.value = (saved && saved.name) || (CFG.canRep ? (CFG.user || '') : '');
  const roles = h('div', { class: 'nltg-roles', role: 'radiogroup', 'aria-label': t('roleLbl') });
  const list = (CFG.canRep ? ['rep'] : []).concat(JOIN_ROLES);
  const mark = () => roles.querySelectorAll('button').forEach((b) => b.setAttribute('aria-checked', b.dataset.role === role ? 'true' : 'false'));
  for (const r of list) {
    roles.append(h('button', { type: 'button', role: 'radio', 'data-role': r, onclick: () => { role = r; mark(); } }, h('i', { style: { background: ROLE_COLOR[rc(r)] } }), roleLong(r)));
  }
  mark();
  const cam = h('input', { type: 'checkbox' }); cam.checked = ST.wantCam;
  const mic = h('input', { type: 'checkbox' }); mic.checked = ST.wantMic;
  const errEl = h('div', { class: 'nltg-err', role: 'alert', text: err || '' });
  if (!err) errEl.hidden = true;
  const go = h('button', { type: 'submit', class: 'nltg-btn teal go', text: saved ? t('enterBack') : t('enter') });
  const langs = h('div', { class: 'nltg-langs', role: 'group', 'aria-label': t('langLbl') });
  for (const l of LANGS) {
    langs.append(h('button', { type: 'button', lang: l, 'aria-current': l === LANG ? 'true' : 'false', text: { he: 'עב', en: 'EN', fr: 'FR', ru: 'RU', ar: 'ع' }[l],
      onclick: () => { LANG = l; try { sessionStorage.setItem('nltg:lang', l); } catch (e) { /* none */ } ST.me = null; const keepName = name.value; showJoin(); const n2 = document.getElementById('nltg-name'); if (n2) n2.value = keepName; } }));
  }
  const title = PN() + (currentSel().floor ? ' · ' + t('floor', { n: currentSel().floor }) : '');
  const form = h('form', { class: 'nltg-card', role: 'dialog', 'aria-modal': 'true', 'aria-labelledby': 'nltg-jt', novalidate: true },
    h('div', { class: 'k', text: t('kicker') + ' · ' + t('sample') }),
    h('div', { class: 'h', id: 'nltg-jt', text: title }),
    h('div', { class: 'p', text: t('joinP') }),
    h('div', null, h('label', { class: 'nltg-lbl', for: 'nltg-name', text: t('nameLbl') }), name),
    h('div', null, h('span', { class: 'nltg-lbl', text: t('roleLbl') }), roles),
    CFG.lk ? h('div', { class: 'nltg-checks' }, h('label', { class: 'nltg-check' }, cam, t('withCam')), h('label', { class: 'nltg-check' }, mic, t('withMic'))) : null,
    h('div', { class: 'consent', text: t('consent') }),
    errEl, go, langs);
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const nm = name.value.trim().slice(0, 40);
    if (!nm) { errEl.textContent = t('needName'); errEl.hidden = false; name.focus(); return; }
    ST.wantCam = cam.checked; ST.wantMic = mic.checked;
    go.disabled = true;
    const r = await api('POST', 'room/token', { room: ST.room, name: nm, role, pid: saved && saved.pid, key: saved && saved.key });
    go.disabled = false;
    if (!r.ok) {
      if (r.error === 'closed') { showNotice(t('e_closed'), true); return; }
      errEl.textContent = t('e_' + r.error) !== 'e_' + r.error ? t('e_' + r.error) : t('e_net');
      errEl.hidden = false;
      return;
    }
    await enter(r);
  });
  R.append(h('div', { class: 'nltg-scrim' }, form));
  setTimeout(() => (name.value ? go : name).focus(), 30);
}

async function enter(r) {
  ST.me = { pid: r.pid, key: r.key, name: r.name, role: r.role };
  saveCreds();
  ST.people = r.participants || [];
  ST.leader = r.leader || '';
  ST.leaderName = nameOf(ST.leader);
  ST.joined = true;
  document.documentElement.classList.add('nltg-in');
  buildRoom();
  ga('room_join', { role: r.role, transport: r.mode, project: CFG.name });
  // the stage: no idle orbit in a room (the camera moves only when someone moves it)
  waitFor(() => stage(), 20000).then((s) => { if (s) Promise.resolve(s.ready).then(() => { try { s.setAutoOrbit(false); } catch (e) { /* none */ } }); });
  await loadNotes();
  if (r.mode === 'livekit' && r.token && CFG.lkLib) {
    T = new LiveKitTransport(r);
    const ok = await T.start().then(() => true, (e) => { console.warn('[together] livekit', e); return false; });
    if (!ok) { toast(t('lkFail')); T = new FallbackTransport(r); T.start(); }
  } else {
    T = new FallbackTransport(r);
    T.start();
  }
  if (r.state && ST.leader && ST.leader !== ST.me.pid) applyState(r.state, 0);
  renderAll();
  if (ST.created && ST.me.role === 'rep') openInvite(); // the representative's console: the join link ready to share
  requestAnimationFrame(frame);
}

function nameOf(pid) {
  if (!pid) return '';
  if (ST.me && pid === ST.me.pid) return ST.me.name;
  const p = ST.people.find((x) => x.pid === pid);
  return p ? p.name : '';
}
function setLeader(pid, name) {
  const was = ST.leader;
  ST.leader = pid || '';
  ST.leaderName = name || nameOf(pid);
  if (ST.leader !== was) {
    ST.following = true; // a new leader: everyone follows again
    if (ST.leader && ST.me && ST.leader !== ST.me.pid && ST.lastState) applyState(ST.lastState, 0.6);
  }
  renderTop(); renderCtl(); renderTiles(); renderList();
}

/* ------------------------------------------------------------------ the room's UI */

function buildRoom() {
  R.textContent = '';
  applyDir();
  UI = {};
  // pins first: the dock and the bars cover them
  UI.pins = h('div', { class: 'nltg-pins', 'aria-hidden': 'true' });
  UI.pointer = h('div', { class: 'nltg-pointer', hidden: true });
  UI.pointer.innerHTML = '<svg width="22" height="22" viewBox="0 0 24 24"><path d="M4 3l16 7-7 2-2 7z" fill="#1F4B5C" stroke="#fff" stroke-width="1.6" stroke-linejoin="round"/></svg>';
  UI.pointerName = h('span');
  UI.pointer.append(UI.pointerName);
  UI.label = h('div', { class: 'nltg-pin-label', hidden: true });
  UI.pins.append(UI.pointer, UI.label);
  R.append(UI.pins);

  // the plan and the section (drawn into the view layer)
  UI.plan = h('div', { class: 'nltg-plan' });
  LAYER.plan.textContent = '';
  LAYER.plan.append(UI.plan);

  UI.mini = h('div', { class: 'nltg-mini', hidden: true });
  R.append(UI.mini);

  // the top bar
  UI.kicker = h('span', { class: 'nltg-k' });
  UI.title = h('span', { class: 'nltg-n' });
  UI.tbox = h('div', { class: 'nltg-t' }, UI.kicker, UI.title);
  UI.live = h('span', { class: 'nltg-live', role: 'status' }, h('i'), h('span'));
  UI.inviteBtn = h('button', { type: 'button', class: 'nltg-btn ghost nltg-invite', onclick: () => openInvite() }, icon('link', 18), t('invite'));
  UI.modes = h('div', { class: 'nltg-modes', role: 'group', 'aria-label': t('modesLbl') });
  for (const m of MODES) UI.modes.append(h('button', { type: 'button', 'data-mode': m, text: t('m_' + m), onclick: () => setMode(m, 'local') }));
  UI.modeSel = h('div', { class: 'nltg-modesel' });
  UI.modeSelBtn = h('button', { type: 'button', 'aria-haspopup': 'true', 'aria-expanded': 'false', onclick: () => toggleModeMenu() });
  UI.modeMenu = h('div', { class: 'menu', role: 'menu', hidden: true });
  for (const m of MODES) UI.modeMenu.append(h('button', { type: 'button', role: 'menuitemradio', 'data-mode': m, text: t('m_' + m), onclick: () => { toggleModeMenu(false); setMode(m, 'local'); } }));
  UI.modeSel.append(UI.modeSelBtn, UI.modeMenu);
  UI.leaveBtn = h('button', { type: 'button', class: 'nltg-btn leave nltg-leave-top', text: t('leave'), onclick: () => leave() });
  UI.top = h('div', { class: 'nltg-top' }, UI.tbox, UI.live, h('span', { class: 'nltg-sp' }), UI.inviteBtn, UI.modes, UI.modeSel, UI.leaveBtn);
  R.append(UI.top);

  // the follow pill
  UI.followWrap = h('div', { class: 'nltg-followwrap' });
  R.append(UI.followWrap);

  // the dock
  UI.tiles = h('div', { class: 'nltg-tiles' });
  UI.peopleBox = h('div', { class: 'nltg-people' });
  UI.ctl = h('div', { class: 'nltg-ctl' });
  UI.tabs = h('div', { class: 'nltg-tabs', role: 'tablist' });
  UI.tabNotes = h('button', { type: 'button', role: 'tab', id: 'nltg-tab-n', 'aria-controls': 'nltg-list', onclick: () => { ST.tab = 'notes'; renderList(); } });
  UI.tabPeople = h('button', { type: 'button', role: 'tab', id: 'nltg-tab-p', 'aria-controls': 'nltg-list', onclick: () => { ST.tab = 'people'; renderList(); } });
  UI.tabs.append(UI.tabNotes, UI.tabPeople);
  UI.list = h('div', { class: 'nltg-list', id: 'nltg-list', role: 'tabpanel' });
  UI.file = h('div', { class: 'nltg-file' });
  UI.consent = h('div', { class: 'nltg-consent', text: t('consent') });
  UI.ctlrow = h('div', { class: 'nltg-ctlrow' });
  UI.dock = h('aside', { class: 'nltg-dock', 'aria-label': t('kicker') }, h('div', { class: 'nltg-grab', 'aria-hidden': 'true' }), UI.tiles, UI.peopleBox, UI.ctl, UI.tabs, UI.list, UI.file, UI.consent, UI.ctlrow);
  R.append(UI.dock);

  // phones: the strip of tiles, the floating "הוספת הערה"
  UI.strip = h('div', { class: 'nltg-strip' });
  UI.fab = h('button', { type: 'button', class: 'nltg-fab', onclick: () => armPick() }, '＋ ', t('addNote'));
  R.append(UI.strip, UI.fab);

  UI.toast = h('div', { class: 'nltg-toast', role: 'status', 'aria-live': 'polite', hidden: true });
  R.append(UI.toast);
}

function renderAll() {
  if (!ST.joined) return;
  renderTop(); renderTiles(); renderCtl(); renderList(); renderFile(); renderPlan(); renderMini();
}

function countOn() {
  if (T && T.kind === 'livekit' && T.room) return 1 + T.room.remoteParticipants.size;
  return Math.max(1, ST.people.filter((p) => p.on).length);
}
function titleLine() {
  let floor = null, side = null, extra = '';
  if (ST.mode === 'inside' && tour()) {
    const v = tour().getView();
    floor = v.floor || null; side = v.dir || null;
    if (v.spot === 'balcony') extra = t('spotBalcony');
  } else {
    const s = currentSel(); floor = s.floor; side = s.unit ? s.side : null;
  }
  return [PN(), floor ? t('floor', { n: floor }) : '', side ? facingWords(side) : '', extra].filter(Boolean).join(' · ');
}
let topKey = '';
function renderTop() {
  if (!UI.top) return;
  const phone = phoneMQ.matches;
  const key = [phone, LANG, ST.mode, ST.leader, ST.leaderName, ST.following, titleLine(), countOn(), T && T.kind, !!tour()].join('|');
  if (key === topKey) return;
  topKey = key;
  // the kicker; on a phone it also says who leads (the pill has no room there), and is the way back when one looked away
  const ld = ST.leader && ST.me && ST.leader !== ST.me.pid ? (ST.leaderName || t('rep')) : (amLeader() ? ST.me.name : '');
  const k = t('kicker') + (phone ? '' : ' · ' + t('sample'));
  if (phone && ld) {
    const back = ST.leader !== ST.me.pid && !ST.following;
    const el = back ? h('button', { type: 'button', class: 'nltg-k', text: t('followBack', { name: ld }), onclick: () => refollow() }) : h('span', { class: 'nltg-k is-follow', text: t('followPill', { name: ld }) });
    UI.kicker.replaceWith(el); UI.kicker = el;
  } else {
    if (UI.kicker.tagName !== 'SPAN' || UI.kicker.classList.contains('is-follow')) { const el = h('span', { class: 'nltg-k' }); UI.kicker.replaceWith(el); UI.kicker = el; }
    UI.kicker.textContent = k;
  }
  UI.title.textContent = phone ? titleLine().split(' · ').slice(0, 2).join(' · ') : titleLine();
  const n = countOn(), lk = T && T.kind === 'livekit';
  UI.live.classList.toggle('is-sync', !lk);
  UI.live.lastChild.textContent = phone ? t('liveShort') : (lk ? (n === 1 ? t('live1') : t('live', { n })) : (n === 1 ? t('sync1') : t('sync', { n })));
  UI.live.setAttribute('aria-label', lk ? (n === 1 ? t('live1') : t('live', { n })) : (n === 1 ? t('sync1') : t('sync', { n })));
  UI.modes.querySelectorAll('button').forEach((b) => b.setAttribute('aria-pressed', b.dataset.mode === ST.mode ? 'true' : 'false'));
  UI.modeMenu.querySelectorAll('button').forEach((b) => b.setAttribute('aria-pressed', b.dataset.mode === ST.mode ? 'true' : 'false'));
  UI.modeSelBtn.textContent = '';
  UI.modeSelBtn.append(t('ms_' + ST.mode), icon('down', 16));
  UI.modeSelBtn.setAttribute('aria-label', t('modesLbl') + ': ' + t('m_' + ST.mode));
  // the pill over the view
  UI.followWrap.textContent = '';
  if (ld && !phone) {
    const back = ST.leader !== ST.me.pid && !ST.following;
    const pill = back
      ? h('button', { type: 'button', class: 'nltg-follow', onclick: () => refollow() }, h('span', { class: 'dot', text: initial(ld) }), t('followBack', { name: ld }))
      : h('div', { class: 'nltg-follow', role: 'status' }, h('span', { class: 'dot', text: initial(ld) }), t('followPill', { name: ld }));
    UI.followWrap.append(pill);
  }
}
function toggleModeMenu(on) {
  const open = on == null ? UI.modeMenu.hidden : on;
  UI.modeMenu.hidden = !open;
  UI.modeSelBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
}

/* the video tiles (LiveKit) or the participants' chips (without video) */
function renderTiles() {
  if (!UI.tiles) return;
  const phone = phoneMQ.matches;
  const lk = T && T.kind === 'livekit';
  R.classList.toggle('is-chips', !lk);
  UI.strip.classList.toggle('is-chips', !lk);
  if (lk) {
    UI.peopleBox.hidden = true;
    const host = phone ? UI.strip : UI.tiles;
    (phone ? UI.tiles : UI.strip).textContent = '';
    UI.tiles.hidden = phone;
    const list = T.peopleList();
    const repIdx = list.findIndex((p) => p.role === 'rep');
    if (repIdx > 0) list.unshift(list.splice(repIdx, 1)[0]);
    const keep = new Map([...host.querySelectorAll('.nltg-tile')].map((el) => [el.dataset.pid, el]));
    host.textContent = '';
    list.forEach((p, i) => {
      let el = keep.get(p.pid);
      if (!el) {
        el = h('div', { class: 'nltg-tile', 'data-pid': p.pid }, h('div', { class: 'av' }), h('div', { class: 'spk' }), h('div', { class: 'nm' }), h('div', { class: 'mute' }));
        el.querySelector('.mute').append(icon('micOff', 12));
        el.querySelector('.mute svg').style.color = '#fff';
      }
      el.classList.toggle('big', !phone && i === 0 && p.role === 'rep');
      el.classList.toggle('is-me', !!p.me);
      el.querySelector('.av').textContent = initial(p.name);
      const nm = el.querySelector('.nm'); nm.textContent = ''; nm.append(roleChip(p.role), phone ? '' : p.name + (p.me ? ' (' + t('me') + ')' : ''));
      el.setAttribute('aria-label', p.name + ', ' + roleLong(p.role));
      host.append(el);
      T.attachVideo(p, el);
    });
    renderTilesState();
  } else {
    UI.tiles.hidden = true;
    UI.tiles.textContent = '';
    // chips: who is in the room; and for a visitor, a WhatsApp call to the representative
    const chips = h('div', { class: 'nltg-chips' });
    const people = ST.people.slice().sort((a, b) => (b.role === 'rep') - (a.role === 'rep'));
    for (const p of people) {
      chips.append(h('span', { class: 'nltg-chip' + (p.on ? ' on' : ''), title: p.on ? t('inRoom') : t('away') }, h('i', { class: 'd' }), roleChip(p.role), p.name + (ST.me && p.pid === ST.me.pid ? ' (' + t('me') + ')' : '')));
    }
    UI.peopleBox.textContent = '';
    UI.peopleBox.hidden = false;
    UI.peopleBox.append(chips);
    const repIn = ST.people.some((p) => p.role === 'rep' && p.on);
    if (ST.me && ST.me.role !== 'rep' && CFG.wa) {
      if (!repIn) UI.peopleBox.append(h('div', { class: 'nltg-wait', text: t('waitRep') }));
      UI.peopleBox.append(h('a', { class: 'nltg-btn wa', href: waHref(t('waCall', { project: PN(), url: joinUrl() }), true), target: '_blank', rel: 'noopener', onclick: () => ga('whatsapp_click', { source: 'together-call' }) }, icon('wa'), t('waRep')));
    }
    UI.strip.textContent = '';
    for (const p of people.filter((x) => x.on)) UI.strip.append(h('span', { class: 'nltg-chip on' }, h('i', { class: 'd' }), roleChip(p.role), p.name));
  }
}
function renderTilesState() {
  if (!(T && T.kind === 'livekit')) return;
  const host = phoneMQ.matches ? UI.strip : UI.tiles;
  const byId = new Map(T.peopleList().map((p) => [p.pid, p]));
  host.querySelectorAll('.nltg-tile').forEach((el) => {
    const p = byId.get(el.dataset.pid);
    el.classList.toggle('is-speaking', ST.speaking.has(el.dataset.pid));
    el.classList.toggle('is-muted', !!(p && p.muted));
  });
}

/* the controls: microphone, camera, "עקבו אחריי" (the representative only); on a phone the bottom row */
function renderCtl() {
  if (!UI.ctl) return;
  const lk = T && T.kind === 'livekit';
  const isRep = ST.me && ST.me.role === 'rep';
  UI.ctl.textContent = '';
  UI.ctlrow.textContent = '';
  const micOn = lk && T.micOn(), camOn = lk && T.camOn();
  const follow = (round) => h('button', { type: 'button', class: 'nltg-btn teal' + (round ? ' round' : ''), 'aria-pressed': amLeader() ? 'true' : 'false', 'aria-label': round ? (amLeader() ? t('followStop') : t('follow')) : null, onclick: () => toggleLead() }, round ? icon('eye') : (amLeader() ? t('followStop') : t('follow')));
  if (lk) {
    UI.ctl.append(
      h('button', { type: 'button', class: 'nltg-btn tog' + (micOn ? '' : ' off'), 'aria-pressed': micOn ? 'true' : 'false', onclick: () => T.toggleMic() }, icon(micOn ? 'mic' : 'micOff'), t('mic')),
      h('button', { type: 'button', class: 'nltg-btn tog' + (camOn ? '' : ' off'), 'aria-pressed': camOn ? 'true' : 'false', onclick: () => T.toggleCam() }, icon(camOn ? 'cam' : 'camOff'), t('cam')));
  }
  if (isRep) UI.ctl.append(follow(false));
  UI.ctl.hidden = !UI.ctl.childNodes.length;
  // the phone's row: mic, camera (or the WhatsApp call), follow (the representative), the file, leave; all 48px
  if (lk) {
    UI.ctlrow.append(
      h('button', { type: 'button', class: 'nltg-btn round tog' + (micOn ? '' : ' off'), 'aria-pressed': micOn ? 'true' : 'false', 'aria-label': t('mic'), onclick: () => T.toggleMic() }, icon(micOn ? 'mic' : 'micOff')),
      h('button', { type: 'button', class: 'nltg-btn round tog' + (camOn ? '' : ' off'), 'aria-pressed': camOn ? 'true' : 'false', 'aria-label': t('cam'), onclick: () => T.toggleCam() }, icon(camOn ? 'cam' : 'camOff')));
  } else if (!isRep && CFG.wa) {
    UI.ctlrow.append(h('a', { class: 'nltg-btn round', href: waHref(t('waCall', { project: PN(), url: joinUrl() }), true), target: '_blank', rel: 'noopener', 'aria-label': t('waRep') }, icon('wa')));
  }
  if (isRep) UI.ctlrow.append(follow(true));
  UI.ctlrow.append(fileLink('nltg-btn wa', t('sendFileShort')));
  UI.ctlrow.append(h('button', { type: 'button', class: 'nltg-btn leave round', 'aria-label': t('leave'), onclick: () => leave() }, icon('x')));
}

/* the tabs: הערות (n) / משתתפים (n) */
function renderList() {
  if (!UI.list) return;
  const nNotes = ST.notes.length, nPeople = T && T.kind === 'livekit' ? T.peopleList().length : ST.people.filter((p) => p.on).length || 1;
  UI.tabNotes.textContent = ''; UI.tabNotes.append(t('notes'), ' ', h('i', { text: nNotes }));
  UI.tabPeople.textContent = ''; UI.tabPeople.append(t('people'), ' ', h('i', { text: nPeople }));
  UI.tabNotes.setAttribute('aria-selected', ST.tab === 'notes' ? 'true' : 'false');
  UI.tabPeople.setAttribute('aria-selected', ST.tab === 'people' ? 'true' : 'false');
  UI.list.setAttribute('aria-labelledby', ST.tab === 'notes' ? 'nltg-tab-n' : 'nltg-tab-p');
  const keepScroll = UI.list.scrollTop;
  UI.list.textContent = '';
  if (ST.tab === 'notes') {
    for (const n of ST.notes) UI.list.append(noteEl(n, true));
    if (!ST.notes.length) UI.list.append(h('div', { class: 'nltg-empty', text: t('noNotes') }));
    UI.list.append(h('button', { type: 'button', class: 'nltg-add', onclick: () => armPick() },
      h('span', { class: 'num', 'aria-hidden': 'true', text: '+' }), h('span', null, h('span', { class: 'tx', text: t('addNote') }), h('span', { class: 'meta', text: t('addNoteSub') }))));
  } else {
    UI.list.append(h('button', { type: 'button', class: 'nltg-btn', style: { width: '100%' }, onclick: () => openInvite() }, icon('link', 18), t('invite')));
    const list = T && T.kind === 'livekit' ? T.peopleList() : ST.people.map((p) => Object.assign({}, p, { me: ST.me && p.pid === ST.me.pid }));
    for (const p of list) {
      const st = p.pid === ST.leader ? t('leading') : (p.on === false ? t('away') : t('inRoom'));
      UI.list.append(h('div', { class: 'nltg-person' },
        h('span', { class: 'av nltg-r-' + rc(p.role), text: initial(p.name), 'aria-hidden': 'true' }),
        h('span', null, p.name + (p.me ? ' (' + t('me') + ')' : ''), h('span', { class: 'sub', text: roleLong(p.role) })),
        h('span', { class: 'st' + (p.on === false ? '' : ' on'), text: st })));
    }
  }
  if (phoneMQ.matches) {
    // on a phone the view has no room for its caption: the mode's own words go here, under the notes, with the consent
    const cap = modeCaption();
    if (cap) UI.list.append(h('div', { class: 'nltg-cap', text: cap }));
    UI.list.append(h('div', { class: 'nltg-consent', text: t('consent') }));
  }
  UI.list.scrollTop = keepScroll;
}
function modeCaption() {
  const txt = (sel) => { const el = document.querySelector(sel); return el ? (el.textContent || '').trim() : ''; };
  if (ST.mode === 'building') return txt('#nlps .rbs-caption');
  if (ST.mode === 'inside') return t('tourCap');
  if (ST.mode === 'view') return txt('#nlps-view-cap');
  return t('planNote', { n: towerFloors() || '' });
}
function noteEl(n, interactive) {
  const mine = ST.me && (n.pid === ST.me.pid || ST.me.role === 'rep');
  const tx = h('div', { class: 'tx' }, n.text);
  if (n.change) tx.append(' ', h('span', { class: 'chg', text: t('change') }));
  const meta = h('div', { class: 'meta' });
  if (n.where) meta.append(h('span', { class: 'where', text: n.where }));
  meta.append([n.author, roleShort(n.role), hhmm(n.t)].filter(Boolean).join(' · '));
  if (interactive && mine) meta.append(h('button', { type: 'button', class: 'del', text: t('del'), onclick: (e) => { e.stopPropagation(); deleteNote(n); } }));
  const el = h(interactive ? 'div' : 'div', { class: 'nltg-note' + (ST.focus === n.id ? ' is-focus' : ''), 'data-id': n.id },
    h('span', { class: 'num nltg-r-' + rc(n.role), text: n.n, 'aria-hidden': 'true' }), h('div', null, h('span', { class: 'nltg-srt', text: n.n + '. ' }), tx, meta));
  el.querySelector('.nltg-srt').style.cssText = 'position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)';
  if (interactive) {
    el.tabIndex = 0;
    el.setAttribute('role', 'button');
    el.addEventListener('click', () => focusNote(n));
    el.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); focusNote(n); } });
  }
  return el;
}

/* the apartment's file: floor, direction, notes; sent on WhatsApp, and copied */
function fileText() {
  const s = currentSel();
  const lines = [t('waFileHead'), [PN(), s.floor ? t('floor', { n: s.floor }) : '', s.unit ? facingWords(s.side) : '', '(' + t('sample') + ')'].filter(Boolean).join(' · '), ''];
  let used = lines.join('\n').length, shown = 0;
  for (const n of ST.notes) {
    const line = n.n + '. ' + n.text + (n.change ? ' (' + t('change') + ')' : '') + (n.where ? ' · ' + n.where : '') + ' · ' + n.author + ', ' + roleShort(n.role);
    if (used + line.length > 1500) break;
    lines.push(line); used += line.length + 1; shown++;
  }
  if (shown < ST.notes.length) lines.push(t('waFileMore', { n: ST.notes.length - shown }));
  lines.push('', t('waFileLink', { url: fileUrl() }));
  return lines.join('\n');
}
function fileLink(cls, label) {
  const toSite = !(ST.me && ST.me.role === 'rep'); // the representative sends it on to the participants (a share)
  return h('a', { class: cls + ' nltg-filelink', href: waHref(fileText(), toSite), target: '_blank', rel: 'noopener',
    onclick: () => ga('room_file_send', { notes: ST.notes.length, to: toSite ? 'site' : 'share' }) }, icon('wa'), label);
}
function refreshFileLinks() {
  const toSite = !(ST.me && ST.me.role === 'rep');
  const href = waHref(fileText(), toSite);
  R.querySelectorAll('a.nltg-filelink').forEach((a) => { a.href = href; });
}
function renderFile() {
  if (!UI.file) return;
  const s = currentSel();
  UI.file.textContent = '';
  const sub = [s.floor ? t('floor', { n: s.floor }) : '', s.unit ? facingWords(s.side) : '', ST.notes.length === 1 ? t('notes1') : t('notesN', { n: ST.notes.length })].filter(Boolean).join(' · ');
  const copyBtn = h('button', { type: 'button', class: 'copy', 'aria-label': t('copy'), title: t('copy'), onclick: async () => { const ok = await copyText(fileText()); toast(ok ? t('copied') : fileUrl()); } }, icon('copy', 16));
  // the design's box: the title and the line, the one WhatsApp button across; the copy button small, beside the line
  UI.file.append(h('div', { class: 'h' }, h('span', { text: t('file') }), h('span', { class: 'meta' }, h('small', { text: sub }), copyBtn)),
    h('div', { class: 'row' }, fileLink('nltg-btn wa', ST.me && ST.me.role === 'rep' ? t('sendFileRep') : t('sendFile'))));
  refreshFileLinks();
}

/* ------------------------------------------------------------------ modes */

function setLayers(m) {
  LAYER.building.classList.toggle('is-off', m !== 'building');
  LAYER.view.classList.toggle('is-off', m !== 'view');
  LAYER.plan.classList.toggle('is-off', m !== 'plan');
  const H = document.documentElement.classList;
  for (const x of MODES) H.toggle('nltg-m-' + x, x === m);
}
async function setMode(m, why) {
  if (!MODES.includes(m)) return;
  if (why === 'local' && following()) breakFollow();
  if (m === ST.mode && (m !== 'inside' || tour())) { renderTop(); return; }
  ST.mode = m;
  setLayers(m);
  if (m !== 'inside' && tour()) { ST.closingTour = true; try { tour().close(); } catch (e) { /* none */ } ST.closingTour = false; }
  if (m === 'inside') await openInside();
  else if (m === 'view') await ensureView();
  else if (m === 'plan') renderPlan();
  cancelPick();
  renderTop(); renderMini();
  if (phoneMQ.matches) renderList();
  if (why === 'local') { ga('room_mode', { mode: m }); if (amLeader() && T) T.sendMode(m); }
}
async function openInside() {
  if (tour()) return;
  const s = currentSel();
  const fl = nearestTourFloor(Number(s.floor) || 25);
  const scenes = tourScenes.filter((x) => (Number(x.floor) || 25) === fl);
  const want = (ST.lastState && following() && ST.lastState.v && ST.lastState.v.s) || s.side || SEA;
  const start = scenes.some((x) => x.id === want) ? want : (scenes.some((x) => x.id === (s.side || SEA)) ? (s.side || SEA) : (scenes[0] && scenes[0].id));
  const url = tourModuleUrl();
  if (!url || !scenes.length) return;
  ST.openingTour = true;
  try {
    const mod = await import(url);
    if (ST.mode !== 'inside') return;
    const first = scenes.find((x) => x.id === start) || scenes[0];
    mod.openTour({ src: first.src, srcSmall: first.small, title: first.title, scenes, start, caption: t('tourCap'), opener: null,
      onScene: (id) => ga('tour_direction', { side: id, project: CFG.name, floor: fl, source: 'together' }) });
  } catch (e) {
    console.warn('[together] tour', e);
  } finally { ST.openingTour = false; }
}
async function ensureView() {
  const v = view();
  if (v && v.getView()) { setTimeout(() => window.dispatchEvent(new Event('resize')), 60); return; }
  const s = stage();
  if (!s) return;
  await Promise.resolve(s.ready).catch(() => {});
  const cur = currentSel();
  if (!cur.unit) {
    ST.applying = true;
    try { s.selectUnit((cur.floor || 25) + '-' + (cur.side || SEA), 'user'); } catch (e) { /* none */ }
    ST.applying = false;
  }
  await waitFor(() => view() && view().getView(), 8000);
  setTimeout(() => window.dispatchEvent(new Event('resize')), 60);
}
/* the 360 viewer opened or closed by itself (the page's own buttons, Esc): the room's mode follows */
window.addEventListener('nl:tour', (e) => {
  if (!ST.joined) return;
  const d = e.detail || {};
  if (d.open && ST.mode !== 'inside' && !ST.openingTour) { ST.mode = 'inside'; setLayers('inside'); if (following()) breakFollow(); if (amLeader() && T) T.sendMode('inside'); renderTop(); renderMini(); }
  else if (!d.open && ST.mode === 'inside' && !ST.closingTour) { ST.mode = 'building'; setLayers('building'); if (amLeader() && T) T.sendMode('building'); renderTop(); renderMini(); }
});
/* the stage card's "הנוף והמפה" inside a room: the mode "הנוף" */
window.addEventListener('nl:floor-action', (e) => {
  if (!ST.joined) return;
  const d = e.detail || {};
  if (d.action === 'view') setTimeout(() => setMode('view', 'local'), 0);
});
/* a floor or an apartment picked on the stage */
function onPick(e) {
  const d = e.detail || {};
  if (d.floor != null) ST.sel.floor = d.floor;
  if (d.unit) { ST.sel.unit = d.unit; ST.sel.side = String(d.unit).split('-')[1]; }
  if (!ST.joined) return;
  if (!ST.applying && following()) breakFollow();
  renderTop(); renderFile(); renderMini();
  if (ST.mode === 'plan') renderPlan();
}
window.addEventListener('nl:floor', onPick);
window.addEventListener('nl:facing', onPick);
/* the visitor moved the camera himself: a follower looks on his own until he taps back */
window.addEventListener('nl:view', (e) => {
  if (!ST.joined || !e.detail || e.detail.source !== 'user') return;
  if (following()) breakFollow();
});
function breakFollow() { ST.following = false; renderTop(); }
function refollow() { ST.following = true; renderTop(); if (ST.lastState) applyState(ST.lastState, 0.6); }

/* ------------------------------------------------------------------ the leader's state, out and in */

function snapshot() {
  const s = { m: ST.mode };
  let sel = null;
  try { sel = stage() && stage().getSelection ? stage().getSelection() : null; } catch (e) { sel = null; }
  if (sel) { s.f = sel.floor; if (sel.unit) s.u = sel.unit; }
  try {
    if (ST.mode === 'building') { const v = stage() && stage().getView ? stage().getView() : null; if (v) s.v = { t: v.target, r: v.r, p: v.phi, th: v.theta, hf: v.hf }; }
    else if (ST.mode === 'inside') { const v = tour() ? tour().getView() : null; if (v) { s.v = { s: v.scene, y: v.yaw, p: v.pitch, f: v.fov }; if (!s.f && v.floor) s.f = v.floor; } }
    else if (ST.mode === 'view') { const v = view() ? view().getView() : null; if (v) s.v = { b: v.bearing, v: v.vert }; }
  } catch (e) { /* the part is not ready yet */ }
  if (ST.myPointer && ST.myPointer.mode === ST.mode) s.pt = ST.myPointer;
  return s;
}
async function applyState(st, dur) {
  if (!st || typeof st !== 'object') return;
  ST.lastState = st;
  if (!following()) { renderTop(); return; }
  const s = stage();
  if (s) {
    ST.applying = true;
    try {
      const cur = s.getSelection ? s.getSelection() : null;
      if (st.u && (!cur || cur.unit !== st.u)) s.selectUnit(st.u, 'user');
      else if (!st.u && st.f && (!cur || cur.floor !== st.f)) s.selectFloor(st.f);
    } catch (e) { /* the stage is not ready yet */ }
    ST.applying = false;
  }
  if (st.m && st.m !== ST.mode) {
    if (ST.modeBusy) return;
    ST.modeBusy = true;
    try { await setMode(st.m, 'remote'); } finally { ST.modeBusy = false; }
    st = ST.lastState;
    if (!following()) return;
  }
  const v = st.v || {};
  try {
    if (st.m === 'building' && Array.isArray(v.t) && s && s.setView) {
      // the same width of the scene on a screen of another shape (a phone following a desktop): the distance scales
      let r = Number(v.r);
      const mine = s.getView ? s.getView() : null;
      if (mine && v.hf > 0 && mine.hf > 0) r *= Math.max(0.5, Math.min(3, Math.tan(v.hf / 2) / Math.tan(mine.hf / 2)));
      s.setView({ target: v.t, r, phi: v.p, theta: v.th }, reduced() ? 0 : dur);
    }
    else if (st.m === 'inside' && tour()) tour().setView({ scene: v.s, yaw: v.y, pitch: v.p, fov: v.f }, reduced() ? 0 : dur);
    else if (st.m === 'view' && view()) view().setView({ bearing: v.b, vert: v.v });
  } catch (e) { /* not ready */ }
  renderTop();
}
function toggleLead() {
  if (!T || !ST.me || ST.me.role !== 'rep') return;
  const on = !amLeader();
  T.setLead(on);
  ga('room_lead', { on });
}

/* the leader's loop: the snapshot, sent when it changes (LiveKit: up to ten a second; without it, the transport throttles) */
setInterval(() => {
  if (!ST.joined || !T) return;
  if (ST.me && ST.me.role === 'rep') updateMyPointer();
  if (!amLeader()) return;
  const snap = snapshot();
  const js = JSON.stringify(snap);
  const now = performance.now();
  const beat = T.kind === 'livekit' ? 2000 : 8000;
  if (js !== ST.lastSent || now - ST.lastSentAt > beat) {
    if (T.sendState(snap)) { ST.lastSent = js; ST.lastSentAt = now; }
  }
}, 100);

/* ------------------------------------------------------------------ points: a tap to an anchor, an anchor to the screen */

function planRect() { const svg = UI.plan && UI.plan.querySelector('svg.big'); return svg ? svg.getBoundingClientRect() : null; }
const PLAN = { x0: 6 / 200, y0: 6 / 120, x1: 194 / 200, y1: 114 / 120 };
function viewGeom() {
  const host = document.getElementById('nlps-view-map');
  if (!host) return null;
  const r = host.getBoundingClientRect();
  if (!r.width || !r.height) return null;
  const vf = 36.87 * Math.PI / 180; // Mapbox's field of view
  const hf = 2 * Math.atan(Math.tan(vf / 2) * (r.width / r.height));
  return { r, vf, hf };
}
function pickAnchor(mode, x, y) {
  const sel = currentSel();
  const base = { mode, floor: sel.floor || undefined, side: sel.side || undefined };
  if (mode === 'building') {
    const s = stage();
    const p = s && s.pickPoint ? s.pickPoint(x, y) : null;
    // the note keeps the apartment's floor (the file's); the floor that was tapped on the tower goes into its "where"
    if (p) return Object.assign(base, { x: p.x, y: p.y, z: p.z, floor: base.floor || p.floor || undefined, hit: p.floor || undefined, on: p.on });
    const r = VP.getBoundingClientRect();
    return Object.assign(base, { sx: +((x - r.left) / r.width).toFixed(4), sy: +((y - r.top) / r.height).toFixed(4) });
  }
  if (mode === 'inside') {
    const tv = tour();
    if (!tv) return null;
    const d = tv.pick(x, y);
    if (!d) return null;
    const v = tv.getView();
    return { mode, floor: base.floor || v.floor || undefined, side: v.dir || base.side, scene: v.scene, yaw: d.yaw, pitch: d.pitch };
  }
  if (mode === 'view') {
    const g = viewGeom(), v = view() && view().getView();
    if (!g || !v) return null;
    const dx = ((x - g.r.left) / g.r.width) * 2 - 1, dy = ((y - g.r.top) / g.r.height) * 2 - 1;
    const ha = Math.atan(dx * Math.tan(g.hf / 2)) * 180 / Math.PI, va = Math.atan(dy * Math.tan(g.vf / 2)) * 180 / Math.PI;
    return Object.assign(base, { yaw: +norm(v.bearing + ha).toFixed(2), pitch: +(v.vert - va).toFixed(2) });
  }
  if (mode === 'plan') {
    const r = planRect();
    if (!r) return null;
    const px = (x - r.left) / r.width, py = (y - r.top) / r.height;
    if (px < PLAN.x0 || px > PLAN.x1 || py < PLAN.y0 || py > PLAN.y1) return null;
    return Object.assign(base, { sx: +((px - PLAN.x0) / (PLAN.x1 - PLAN.x0)).toFixed(4), sy: +((py - PLAN.y0) / (PLAN.y1 - PLAN.y0)).toFixed(4) });
  }
  return null;
}
function projectAnchor(a) {
  if (!a || a.mode !== ST.mode) return null;
  if (a.mode === 'building') {
    if (a.x != null) {
      const s = stage();
      const p = s && s.project ? s.project({ x: a.x, y: a.y, z: a.z }) : null;
      return p && !p.behind ? p : null;
    }
    if (a.sx != null) { const r = VP.getBoundingClientRect(); return { x: r.left + a.sx * r.width, y: r.top + a.sy * r.height }; }
    return null;
  }
  if (a.mode === 'inside') {
    const tv = tour();
    if (!tv) return null;
    const v = tv.getView();
    if (a.scene && a.scene !== v.scene) return null;
    const p = tv.project({ yaw: a.yaw, pitch: a.pitch });
    return p && !p.behind ? p : null;
  }
  if (a.mode === 'view') {
    const g = viewGeom(), v = view() && view().getView();
    if (!g || !v || a.yaw == null) return null;
    let ha = norm(a.yaw) - norm(v.bearing); ha = ((ha + 540) % 360) - 180;
    const va = v.vert - Number(a.pitch || 0);
    if (Math.abs(ha) > 80 || Math.abs(va) > 60) return null;
    const x = g.r.left + (Math.tan(ha * Math.PI / 180) / Math.tan(g.hf / 2) + 1) / 2 * g.r.width;
    const y = g.r.top + (Math.tan(va * Math.PI / 180) / Math.tan(g.vf / 2) + 1) / 2 * g.r.height;
    return x < g.r.left - 20 || x > g.r.right + 20 ? null : { x, y };
  }
  if (a.mode === 'plan') {
    const r = planRect();
    if (!r || a.sx == null) return null;
    return { x: r.left + (PLAN.x0 + a.sx * (PLAN.x1 - PLAN.x0)) * r.width, y: r.top + (PLAN.y0 + a.sy * (PLAN.y1 - PLAN.y0)) * r.height };
  }
  return null;
}
function whereFor(a) {
  if (!a) return '';
  if (a.mode === 'inside') {
    const spot = /balcony/.test(a.scene || '') ? t('spotBalcony') : t('spotLiving');
    if (a.pitch < -0.62) return spot + ' · ' + t('floorW');
    if (a.pitch > 0.62) return spot + ' · ' + t('ceiling');
    const b = sideBearing(a.side || (a.scene || 'w').split('-')[0]) - a.yaw * 180 / Math.PI; // yaw grows to the left
    return spot + ' · ' + t('wall', { dir: (COMPASS[LANG] || COMPASS.he)[compassOf(b)] });
  }
  if (a.mode === 'building') return a.on === 'tower' && (a.hit || a.floor) ? t('towerW', { n: a.hit || a.floor }) : (a.on === 'ground' ? t('groundW') : t('buildingW'));
  if (a.mode === 'view') return t('viewW') + (a.side ? ' · ' + facingWords(a.side) : '');
  if (a.mode === 'plan') return t('planW', { room: a.sx < 0.6 ? t('living') : t('roomW') });
  return '';
}

/* the representative's own pointer over the view, as an anchor (sent with the state) */
document.addEventListener('pointermove', (e) => {
  const over = e.target && e.target.closest ? e.target.closest('.nltg-vp, .nlat-viewer__stage, .nltg-pins') : null; // a pin is a point of the view: pointing at a note keeps the pointer
  ST.mouse = over && e.pointerType !== 'touch' ? { x: e.clientX, y: e.clientY, at: performance.now() } : null;
}, { passive: true });
// the pointer stays while the hand rests on a point (one talks about it); it goes when the mouse leaves the view or the window
document.documentElement.addEventListener('mouseleave', () => { ST.mouse = null; });
function updateMyPointer() {
  const m = ST.mouse;
  if (!m || performance.now() - m.at > 30000 || ST.armed) { ST.myPointer = null; return; }
  const a = pickAnchor(ST.mode, m.x, m.y);
  ST.myPointer = a ? Object.assign({}, a, { on: undefined, hit: undefined }) : null;
}

/* ------------------------------------------------------------------ notes */

async function loadNotes() {
  const r = await api('GET', 'room/notes', { room: ST.room });
  if (!r.ok) return;
  ST.notes = Array.isArray(r.notes) ? r.notes : [];
  if (typeof r.rev === 'number') ST.rev = r.rev;
  renderList(); renderFile(); renderMini(); renderPlan();
}
function upsertNote(n) {
  if (!n || !n.id) return;
  const i = ST.notes.findIndex((x) => x.id === n.id);
  if (i >= 0) ST.notes[i] = n; else ST.notes.push(n);
  ST.notes.sort((a, b) => a.n - b.n || a.t - b.t);
  renderList(); renderFile(); renderMini(); renderPlan();
}
function removeNote(id) {
  ST.notes = ST.notes.filter((x) => x.id !== id);
  if (ST.focus === id) ST.focus = null;
  renderList(); renderFile(); renderMini(); renderPlan();
}
async function deleteNote(n) {
  const r = await api('POST', 'room/notes', { room: ST.room, pid: ST.me.pid, key: ST.me.key, delete: n.id });
  if (!r.ok) { toast(t('e_net')); return; }
  removeNote(n.id);
  if (T) T.noteDeleted(n.id, r.rev);
}
function focusNote(n) {
  ST.focus = n.id;
  renderList();
  const a = n.anchor || {};
  const go = () => {
    try {
      if (a.mode === 'inside' && tour()) tour().setView({ scene: a.scene, yaw: a.yaw, pitch: Math.max(-0.5, Math.min(0.5, a.pitch || 0)) }, 0.8);
      else if (a.mode === 'building' && a.x != null && stage() && stage().getView) {
        const v = stage().getView();
        if (v) stage().setView({ target: [a.x, a.y, a.z], r: Math.min(v.r, 320), phi: v.phi, theta: v.theta }, 0.9);
      } else if (a.mode === 'view' && view()) view().setView({ bearing: a.yaw, vert: Math.max(-45, Math.min(10, Number(a.pitch) || 0)) });
    } catch (e) { /* not ready */ }
  };
  if (a.mode && a.mode !== ST.mode) setMode(a.mode, 'local').then(() => setTimeout(go, 400));
  else { if (following()) breakFollow(); go(); }
}

/* "הוספת הערה": the next tap on the view is the note's point */
function armPick() {
  if (!ST.joined) return;
  cancelCompose();
  ST.armed = true;
  document.documentElement.classList.add('nltg-pick');
  UI.pick = h('div', { class: 'nltg-pick', role: 'application', 'aria-label': t('pickHint') });
  UI.pickHint = h('div', { class: 'nltg-pickhint', role: 'status' }, t('pickHint'), h('button', { type: 'button', text: t('cancel'), onclick: (e) => { e.stopPropagation(); cancelPick(); } }));
  UI.pick.addEventListener('click', (e) => {
    const a = pickAnchor(ST.mode, e.clientX, e.clientY);
    if (!a) return;
    cancelPick();
    compose(a, e.clientX, e.clientY);
  });
  // the pick area is the view: under the dock and the bars (they stay usable)
  R.insertBefore(UI.pick, UI.top);
  R.append(UI.pickHint);
}
function cancelPick() {
  ST.armed = false;
  document.documentElement.classList.remove('nltg-pick');
  if (UI.pick) UI.pick.remove();
  if (UI.pickHint) UI.pickHint.remove();
  UI.pick = UI.pickHint = null;
}
function compose(anchor, x, y) {
  cancelCompose();
  const next = ST.notes.reduce((m, n) => Math.max(m, n.n), 0) + 1;
  ST.temp = { anchor, n: next, role: ST.me.role };
  const ta = h('textarea', { class: 'nltg-ta', maxlength: '400', placeholder: t('notePh'), 'aria-label': t('newNote') });
  const where = h('input', { class: 'nltg-in', type: 'text', maxlength: '60', 'aria-label': t('whereLbl') });
  where.value = whereFor(anchor).slice(0, 60);
  const chg = h('input', { type: 'checkbox' });
  const err = h('div', { class: 'nltg-err', hidden: true });
  const save = h('button', { type: 'submit', class: 'nltg-btn teal', text: t('save') });
  const form = h('form', { class: 'nltg-compose', role: 'dialog', 'aria-label': t('newNote') },
    h('div', { class: 'h' }, h('span', { class: 'num nltg-r-' + rc(ST.me.role), text: next }), t('newNote')),
    ta, h('div', null, h('label', { class: 'nltg-lbl', text: t('whereLbl') }), where),
    h('label', { class: 'nltg-check' }, chg, t('changeAsk')), err,
    h('div', { class: 'row' }, save, h('button', { type: 'button', class: 'nltg-btn', text: t('cancel'), onclick: () => cancelCompose() })));
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const text = ta.value.trim().slice(0, 400);
    if (!text) { ta.focus(); return; }
    save.disabled = true;
    const r = await api('POST', 'room/notes', { room: ST.room, pid: ST.me.pid, key: ST.me.key, text, where: where.value.trim().slice(0, 60), anchor, change: chg.checked });
    save.disabled = false;
    if (!r.ok || !r.note) { err.textContent = t(r.error === 'rate' ? 'e_rate' : (r.error === 'closed' ? 'e_closed' : 'e_net')); err.hidden = false; return; }
    cancelCompose();
    ST.focus = r.note.id;
    if (typeof r.rev === 'number') ST.rev = r.rev;
    upsertNote(r.note);
    if (T) T.noteAdded(r.note);
    ga('room_note', { mode: anchor.mode, change: !!chg.checked });
  });
  form.addEventListener('keydown', (e) => { if (e.key === 'Escape') { e.preventDefault(); cancelCompose(); } });
  UI.compose = form;
  R.append(form);
  if (!phoneMQ.matches) {
    const W = innerWidth, H = innerHeight, fw = 340, fh = form.offsetHeight || 330, dock = 372 + 32;
    const rtl = RTL();
    const minX = rtl ? dock : 16, maxX = rtl ? W - fw - 16 : W - dock - fw;
    let left = x + 28; if (left > maxX) left = x - fw - 28;
    left = Math.max(minX, Math.min(maxX, left));
    const top = Math.max(92, Math.min(H - fh - 16, y - fh / 2));
    form.style.left = left + 'px'; form.style.top = top + 'px';
  }
  setTimeout(() => ta.focus(), 20);
}
function cancelCompose() {
  if (UI.compose) UI.compose.remove();
  UI.compose = null;
  ST.temp = null;
}

/* ------------------------------------------------------------------ the frame loop: pins, the label, the pointer */

const pinEls = new Map();
let tempPin = null;
function frame() {
  if (!ST.joined) return;
  requestAnimationFrame(frame);
  const seen = new Set();
  for (const n of ST.notes) {
    const p = projectAnchor(n.anchor);
    let el = pinEls.get(n.id);
    if (!p) { if (el) el.hidden = true; continue; }
    if (!el) {
      el = h('button', { type: 'button', class: 'nltg-pin', 'aria-label': n.n + '. ' + n.text, onclick: () => focusNote(n) });
      UI.pins.append(el); pinEls.set(n.id, el);
    }
    el.className = 'nltg-pin nltg-r-' + rc(n.role);
    el.textContent = n.n;
    el.hidden = false;
    el.style.transform = 'translate3d(' + Math.round(p.x) + 'px,' + Math.round(p.y - 22) + 'px,0)';
    seen.add(n.id);
    if (ST.focus === n.id) placeLabel(n.text + (n.change ? ' · ' + t('change') : ''), p);
  }
  for (const [id, el] of pinEls) if (!seen.has(id) && !ST.notes.some((n) => n.id === id)) { el.remove(); pinEls.delete(id); }
  if (!ST.focus || !seen.has(ST.focus)) { if (!ST.temp) UI.label.hidden = true; }
  // the note being written
  if (ST.temp) {
    const p = projectAnchor(ST.temp.anchor);
    if (!tempPin) { tempPin = h('div', { class: 'nltg-pin is-temp' }); UI.pins.append(tempPin); }
    tempPin.className = 'nltg-pin is-temp nltg-r-' + rc(ST.temp.role);
    tempPin.textContent = ST.temp.n;
    tempPin.hidden = !p;
    if (p) tempPin.style.transform = 'translate3d(' + Math.round(p.x) + 'px,' + Math.round(p.y - 22) + 'px,0)';
  } else if (tempPin) { tempPin.remove(); tempPin = null; }
  // the representative's pointer, with the name (followers only)
  const st = ST.lastState;
  const pt = following() && st && st.pt && st.pt.mode === ST.mode ? projectAnchor(st.pt) : null;
  UI.pointer.hidden = !pt;
  if (pt) {
    UI.pointerName.textContent = ST.leaderName || t('rep');
    UI.pointer.style.transform = 'translate3d(' + Math.round(pt.x - 3) + 'px,' + Math.round(pt.y - 3) + 'px,0)';
  }
  if (++frameN % 6 === 0) renderMiniDyn();
}
let frameN = 0;
function placeLabel(text, p) {
  const el = UI.label;
  if (el.textContent !== text) el.textContent = text;
  el.hidden = false;
  const w = el.offsetWidth || 200, hgt = el.offsetHeight || 30;
  const x = RTL() ? p.x - w - 26 : p.x + 26;
  el.style.transform = 'translate3d(' + Math.round(Math.max(8, Math.min(innerWidth - w - 8, x))) + 'px,' + Math.round(p.y - 22 - hgt / 2) + 'px,0)';
}

/* ------------------------------------------------------------------ the plan: small ("איפה אתם בדירה") and large */

function planSvg(cls, W) {
  const s = currentSel();
  const words = s.side ? facingWords(s.side).replace(/^לכיוון /, '') : '';
  const big = cls === 'big', f1 = big ? 7.5 : 11, f2 = big ? 7 : 10;
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('viewBox', '0 0 200 120');
  svg.setAttribute('class', cls);
  if (W) { svg.setAttribute('width', W); svg.setAttribute('height', Math.round(W * 0.6)); }
  svg.setAttribute('role', 'img');
  svg.setAttribute('aria-label', t('sample'));
  const esc = (x) => String(x).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  // the design's example apartment: the window along the top, the living room and kitchen, two rooms
  svg.innerHTML = '<rect x="6" y="6" width="188" height="108" rx="6" fill="#fff" stroke="#CFC6B6" stroke-width="2"/>'
    + '<path d="M6 18 Q100 -2 194 18" fill="none" stroke="#2F6F86" stroke-width="4"/>'
    + '<line x1="120" y1="18" x2="120" y2="114" stroke="#CFC6B6" stroke-width="2"/>'
    + '<line x1="120" y1="66" x2="194" y2="66" stroke="#CFC6B6" stroke-width="2"/>'
    + '<text x="60" y="80" font-size="' + f1 + '" font-family="Assistant, sans-serif" fill="#6B6558" text-anchor="middle">' + esc(t('living')) + '</text>'
    + '<text x="157" y="48" font-size="' + f2 + '" font-family="Assistant, sans-serif" fill="#6B6558" text-anchor="middle">' + esc(t('roomW')) + '</text>'
    + '<text x="157" y="96" font-size="' + f2 + '" font-family="Assistant, sans-serif" fill="#6B6558" text-anchor="middle">' + esc(t('roomW')) + '</text>'
    + (big && words ? '<text x="100" y="30" font-size="5.5" font-weight="700" font-family="Assistant, sans-serif" fill="#2F6F86" text-anchor="middle">' + esc(t('windowW') + ' · ' + words) + '</text>' : '')
    + '<g class="cone"></g><g class="pins"></g>';
  return svg;
}
/* the viewer's place in the example apartment, and the pins: where the living-room point is, what the camera faces */
const EYE = () => ({ x: 64, y: 62 });
function renderMini() {
  if (!UI.mini) return;
  const show = (ST.mode === 'inside' && tour()) || (ST.mode === 'view' && view() && view().getView());
  UI.mini.hidden = !show;
  if (!show) return;
  const s = currentSel();
  const words = s.side ? facingWords(s.side).replace(/^לכיוון /, '') : '';
  UI.mini.textContent = '';
  UI.mini.append(h('div', { class: 'mh' }, h('span', { text: t('miniH') }), h('small', { text: t('sample') + (words ? ' · ' + t('miniTop', { words }) : '') })), planSvg('mini', 200));
  renderMiniDyn();
}
function renderMiniDyn() {
  if (!UI.mini || UI.mini.hidden) return;
  const svg = UI.mini.querySelector('svg');
  if (!svg) return;
  const e = EYE();
  let rot = 0;
  let scene = null;
  if (ST.mode === 'inside' && tour()) { const v = tour().getView(); rot = -v.yaw * 180 / Math.PI; scene = v.scene; }
  else if (ST.mode === 'view' && view() && view().getView()) { const v = view().getView(); rot = v.bearing - sideBearing(currentSel().side || SEA); }
  const cone = svg.querySelector('g.cone');
  const want = '<g transform="rotate(' + rot.toFixed(1) + ' ' + e.x + ' ' + e.y + ')"><path d="M' + e.x + ' ' + e.y + ' L' + (e.x - 34) + ' 22 L' + (e.x + 34) + ' 22 Z" fill="rgba(31,75,92,.16)"/></g><circle cx="' + e.x + '" cy="' + e.y + '" r="6" fill="#1F4B5C" stroke="#fff" stroke-width="2"/>';
  if (cone.getAttribute('data-k') !== want) { cone.innerHTML = want; cone.setAttribute('data-k', want); }
  // the pins of this apartment's living room (their direction from the viewer) and of the plan (their place)
  const pins = svg.querySelector('g.pins');
  let html = '';
  for (const n of ST.notes) {
    const a = n.anchor || {};
    let x = null, y = null;
    if (a.mode === 'inside' && (!scene || a.scene === scene) && a.yaw != null) {
      const ang = (-a.yaw) ; // 0 = up (the window), positive = clockwise
      x = e.x + Math.sin(ang) * 34; y = e.y - Math.cos(ang) * 34;
    } else if (a.mode === 'plan' && a.sx != null) {
      x = 6 + a.sx * 188; y = 6 + a.sy * 108;
    }
    if (x == null) continue;
    x = Math.max(12, Math.min(188, x)); y = Math.max(12, Math.min(108, y));
    html += '<circle cx="' + x.toFixed(1) + '" cy="' + y.toFixed(1) + '" r="7" fill="' + ROLE_COLOR[rc(n.role)] + '"/><text x="' + x.toFixed(1) + '" y="' + (y + 3.5).toFixed(1) + '" font-size="9" fill="#fff" text-anchor="middle" font-family="Assistant, sans-serif" font-weight="800">' + Number(n.n) + '</text>';
  }
  if (pins.getAttribute('data-k') !== html) { pins.innerHTML = html; pins.setAttribute('data-k', html); }
}
function renderPlan() {
  if (!UI.plan) return;
  UI.plan.textContent = '';
  const s = currentSel();
  const floors = towerFloors() || 0;
  const big = planSvg('big');
  const cut = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  if (floors) {
    const fh = 7, H = floors * fh + 24;
    cut.setAttribute('viewBox', '0 0 80 ' + H);
    cut.setAttribute('class', 'cut');
    cut.setAttribute('role', 'img');
    cut.setAttribute('aria-label', t('cutH'));
    let g = '<rect x="4" y="' + (H - 14) + '" width="72" height="2" fill="#6B6558"/>';
    for (let f = 1; f <= floors; f++) {
      const y = H - 14 - f * fh;
      const on = s.floor === f;
      g += '<rect x="' + (on ? 14 : 18) + '" y="' + (y + 1) + '" width="' + (on ? 52 : 44) + '" height="' + (fh - 2) + '" rx="1.5" fill="' + (on ? '#1F4B5C' : '#E2DCD0') + '"/>';
    }
    if (s.floor) {
      const y = H - 14 - s.floor * fh + fh / 2 + 3;
      g += '<text x="40" y="' + (y - fh - 2) + '" font-size="8" font-weight="700" font-family="Assistant, sans-serif" fill="#1F4B5C" text-anchor="middle">' + t('floor', { n: s.floor }).replace(/[<>&]/g, '') + '</text>';
    }
    cut.innerHTML = g;
  }
  const inner = h('div', { class: 'in' },
    h('figure', null, h('figcaption', null, t('planH'), h('span', { class: 'sample', text: t('sample') })), big),
    floors ? h('figure', null, h('figcaption', null, t('cutH')), cut) : null);
  UI.plan.append(inner, h('div', { class: 'note', text: t('planNote', { n: floors || '' }) }));
}

/* ------------------------------------------------------------------ the invitation */

function openInvite() {
  closePop();
  const url = joinUrl();
  const input = h('input', { class: 'nltg-in', type: 'text', readonly: true, value: url, 'aria-label': t('inviteH'), onfocus: (e) => e.target.select() });
  const pop = h('div', { class: 'nltg-pop', role: 'dialog', 'aria-label': t('inviteH') },
    h('div', { class: 'h', text: t('inviteH') }), h('div', { class: 'p', text: t('inviteP') }), input,
    h('div', { class: 'row' },
      h('button', { type: 'button', class: 'nltg-btn teal', onclick: async () => { const ok = await copyText(url); toast(ok ? t('copied') : url); ga('room_invite', { how: 'copy' }); } }, icon('copy', 18), t('copyLink')),
      h('a', { class: 'nltg-btn wa', href: waHref(t('inviteText', { project: PN(), url }), false), target: '_blank', rel: 'noopener', onclick: () => ga('room_invite', { how: 'whatsapp' }) }, icon('wa', 18), t('waShare')),
      navigator.share ? h('button', { type: 'button', class: 'nltg-btn', text: t('share'), onclick: () => { navigator.share({ title: PN(), text: t('inviteText', { project: PN(), url: '' }).trim(), url }).catch(() => {}); } }) : null,
      h('button', { type: 'button', class: 'nltg-btn ghost', text: t('close'), onclick: () => closePop() })));
  // under the invite button (desktop), at the bottom over the sheet (phone)
  if (!phoneMQ.matches && UI.inviteBtn) {
    const r = UI.inviteBtn.getBoundingClientRect();
    const w = 360;
    pop.style.left = Math.max(16, Math.min(innerWidth - w - 16, RTL() ? r.right - w : r.left)) + 'px';
  }
  UI.pop = pop;
  R.append(pop);
  setTimeout(() => input.select(), 20);
}
function closePop() { if (UI.pop) UI.pop.remove(); UI.pop = null; }
document.addEventListener('keydown', (e) => {
  if (e.key !== 'Escape' || !ST.joined) return;
  if (UI.pop) { closePop(); return; }
  if (ST.armed) { cancelPick(); return; }
  if (UI.modeMenu && !UI.modeMenu.hidden) toggleModeMenu(false);
}, true);
document.addEventListener('click', (e) => {
  if (UI.pop && !UI.pop.contains(e.target) && !(e.target.closest && e.target.closest('.nltg-invite, .nltg-list .nltg-btn'))) closePop();
  if (UI.modeMenu && !UI.modeMenu.hidden && UI.modeSel && !UI.modeSel.contains(e.target)) toggleModeMenu(false);
});

/* ------------------------------------------------------------------ messages */

let toastT = 0;
function toast(msg) {
  if (!UI.toast) { const o = h('div', { class: 'nltg-out', role: 'status', text: msg }); document.body.append(o); setTimeout(() => o.remove(), 6000); return; }
  UI.toast.textContent = msg;
  UI.toast.hidden = false;
  clearTimeout(toastT);
  toastT = setTimeout(() => { UI.toast.hidden = true; }, 4200);
}

/* ------------------------------------------------------------------ leaving */

async function leave(quiet, hash) {
  const wasIn = ST.joined;
  ST.joined = false;
  cancelPick(); cancelCompose(); closePop();
  if (tour()) { ST.closingTour = true; try { tour().close(); } catch (e) { /* none */ } ST.closingTour = false; }
  if (T) { try { await T.leave(); } catch (e) { /* none */ } T = null; }
  if (wasIn) ga('room_leave', { notes: ST.notes.length });
  restore();
  VP.remove(); R.remove();
  const H = document.documentElement.classList;
  H.remove('nltg-on', 'nltg-in', 'nltg-pick', 'nltg-file'); for (const m of MODES) H.remove('nltg-m-' + m);
  try { const s = stage(); if (s) s.setAutoOrbit(true); } catch (e) { /* none */ }
  reframe();
  const room = ST.room;
  try { const u = new URL(location.href); u.searchParams.delete('room'); u.searchParams.delete('file'); history.replaceState(history.state, '', u.pathname + u.search + (hash || '')); } catch (e) { /* keep */ }
  window.dispatchEvent(new Event('resize'));
  if (hash) { const el = document.querySelector(hash); if (el) el.scrollIntoView({ behavior: reduced() ? 'auto' : 'smooth' }); }
  if (wasIn && !quiet && /^[a-z2-7]{12}$/.test(room)) {
    const o = h('div', { class: 'nltg-out', role: 'status' }, t('left') + ' ', h('a', { href: fileUrl(), text: t('openFile') }));
    o.dir = RTL() ? 'rtl' : 'ltr';
    document.body.append(o);
    setTimeout(() => o.remove(), 9000);
  }
}
window.addEventListener('pagehide', () => { if (T && ST.joined) T.leave(true); });

/* ------------------------------------------------------------------ the file page (?room=<id>&file=1) */

async function showFile() {
  document.documentElement.classList.add('nltg-file');
  R.textContent = '';
  const page = h('div', { class: 'nltg-filepage' });
  R.append(page);
  const r = await api('GET', 'room/file', { room: ST.room });
  const inner = h('div', { class: 'in' });
  page.append(inner);
  if (!r.ok) { inner.append(h('div', { class: 'h', text: t('e_room') }), h('div', { class: 'row' }, h('button', { type: 'button', class: 'nltg-btn', text: t('backToPage'), onclick: () => leave(true) }))); return; }
  ST.notes = Array.isArray(r.notes) ? r.notes : [];
  ST.sel = { floor: r.floor || null, side: r.side || null, unit: r.floor && r.side ? r.floor + '-' + r.side : null };
  const facing = LANG === 'he' ? (r.facing || facingWords(r.side)) : facingWords(r.side);
  const date = r.created ? new Date(r.created * 1000).toLocaleDateString(LANG === 'he' ? 'he-IL' : LANG) : '';
  const list = h('div', { class: 'notes' });
  for (const n of ST.notes) list.append(noteEl(n, false));
  if (!ST.notes.length) list.append(h('div', { class: 'nltg-empty', text: t('fileNone') }));
  const txt = () => {
    const lines = [t('waFileHead'), [Number(r.project.id) === Number(CFG.post) ? PN() : r.project.name, r.floor ? t('floor', { n: r.floor }) : '', facing, '(' + t('sample') + ')'].filter(Boolean).join(' · '), ''];
    for (const n of ST.notes) lines.push(n.n + '. ' + n.text + (n.change ? ' (' + t('change') + ')' : '') + (n.where ? ' · ' + n.where : '') + ' · ' + n.author + ', ' + roleShort(n.role));
    lines.push('', t('waFileLink', { url: location.href }));
    return lines.join('\n').slice(0, 1900);
  };
  inner.append(
    h('div', { class: 'k', text: t('fileK') }),
    h('div', { class: 'h', text: Number(r.project.id) === Number(CFG.post) ? PN() : r.project.name }),
    h('div', { class: 'sub' }, [r.floor ? t('floor', { n: r.floor }) : '', facing].filter(Boolean).join(' · '), h('span', { class: 'sample', text: t('sample') }), date ? h('span', { text: '· ' + t('fileOpened', { date }) }) : null),
    list,
    h('div', { class: 'consent', text: t('consent') }),
    h('div', { class: 'row' },
      CFG.wa ? h('a', { class: 'nltg-btn wa', href: waHref(txt(), true), target: '_blank', rel: 'noopener', onclick: () => ga('room_file_send', { from: 'file' }) }, icon('wa'), t('sendFile')) : null,
      h('button', { type: 'button', class: 'nltg-btn', onclick: async () => { const ok = await copyText(txt()); toast(ok ? t('copied') : ''); } }, icon('copy', 18), t('copy')),
      h('button', { type: 'button', class: 'nltg-btn', text: t('print'), onclick: () => window.print() }),
      r.open ? h('a', { class: 'nltg-btn teal', href: joinUrl(), text: t('joinRoom') }) : null,
      h('button', { type: 'button', class: 'nltg-btn ghost', text: t('backToPage'), onclick: () => leave(true) })));
}

/* ------------------------------------------------------------------ transports */

/* without LiveKit: the site's REST API, polled every 1.5 s; the leader posts the state (at most every 0.8 s) */
class FallbackTransport {
  constructor(join) { this.kind = 'fallback'; this.t = Number(join.t) || 0; this.postAt = 0; this.posting = false; this.alive = true; this.timer = 0; this.fails = 0; }
  start() { this.poll(); }
  async poll() {
    if (!this.alive) return;
    const r = await api('GET', 'room/state', { room: ST.room, pid: ST.me.pid, key: ST.me.key, since: this.t });
    if (!this.alive) return;
    try { await this.take(r); } catch (e) { console.warn('[together] poll', e); } // one bad answer never stops the polling
    if (this.alive) this.timer = setTimeout(() => this.poll(), document.hidden ? 4000 : 1500);
  }
  async take(r) {
    if (r.ok) {
      this.fails = 0;
      if (r.rejoin) await api('POST', 'room/token', { room: ST.room, name: ST.me.name, role: ST.me.role, pid: ST.me.pid, key: ST.me.key });
      ST.people = Array.isArray(r.participants) ? r.participants : ST.people;
      if ((r.leader || '') !== ST.leader) setLeader(r.leader || '', nameOf(r.leader));
      else ST.leaderName = nameOf(ST.leader) || ST.leaderName;
      if (r.state && Number(r.t) > this.t) {
        this.t = Number(r.t);
        if (ST.leader && ST.leader !== ST.me.pid) applyState(r.state, 0.9);
      }
      if (typeof r.rev === 'number' && r.rev !== ST.rev) { ST.rev = r.rev; loadNotes(); }
      const sig = JSON.stringify(ST.people.map((p) => [p.pid, p.name, p.role, p.on]));
      if (sig !== this.sig) { this.sig = sig; renderTiles(); renderList(); }
      renderTop();
    } else if (r.status === 410) {
      this.alive = false;
      ST.joined = false;
      document.documentElement.classList.remove('nltg-in');
      showNotice(t('e_closed'), true);
    } else if (++this.fails === 3) toast(t('reconnecting'));
  }
  sendState(snap) {
    const now = performance.now();
    if (this.posting || now - this.postAt < 800) return false;
    this.posting = true; this.postAt = now;
    api('POST', 'room/state', { room: ST.room, pid: ST.me.pid, key: ST.me.key, state: snap }).then((r) => {
      this.posting = false;
      if (!r.ok && r.error === 'not_leader') setLeader(r.leader || '', '');
    });
    return true;
  }
  sendMode() { ST.lastSent = ''; } // the next tick posts the new mode
  async setLead(on) {
    const r = await api('POST', 'room/state', { room: ST.room, pid: ST.me.pid, key: ST.me.key, lead: !!on });
    if (r.ok) { setLeader(r.leader || '', r.leader === ST.me.pid ? ST.me.name : ''); ST.lastSent = ''; }
    else toast(t('e_net'));
  }
  noteAdded() { /* the others see the new revision on their next poll */ }
  noteDeleted() { /* same */ }
  micOn() { return false; }
  camOn() { return false; }
  peopleList() { return ST.people; }
  attachVideo() { /* no video */ }
  leave(beacon) {
    this.alive = false;
    clearTimeout(this.timer);
    const body = { room: ST.room, pid: ST.me.pid, key: ST.me.key, leave: true };
    if (beacon) { body.__keepalive = true; api('POST', 'room/state', body); return Promise.resolve(); }
    return api('POST', 'room/state', body);
  }
}

/* LiveKit: video, and the data channel (lossy 'view' ~10 Hz; reliable 'mode' and 'notes') */
class LiveKitTransport {
  constructor(join) { this.kind = 'livekit'; this.join = join; this.room = null; this.LK = null; this.videos = new Map(); this.audioBox = h('div', { hidden: true }); }
  async start() {
    const LK = await import(CFG.lkLib);
    this.LK = LK;
    const E = LK.RoomEvent;
    const room = new LK.Room({ adaptiveStream: true, dynacast: true });
    this.room = room;
    document.body.append(this.audioBox);
    const people = () => { renderTiles(); renderTop(); renderList(); };
    room
      .on(E.ParticipantConnected, (p) => { people(); if (amLeader()) this.hello(p.identity); })
      .on(E.ParticipantDisconnected, (p) => { if (ST.leader === p.identity) setLeader('', ''); people(); })
      .on(E.TrackSubscribed, (track, pub, p) => {
        if (track.kind === 'audio') { const el = track.attach(); this.audioBox.append(el); }
        else if (track.kind === 'video') { this.videos.set(p.identity, track); renderTiles(); }
      })
      .on(E.TrackUnsubscribed, (track, pub, p) => {
        track.detach().forEach((el) => el.remove());
        if (track.kind === 'video' && this.videos.get(p.identity) === track) { this.videos.delete(p.identity); renderTiles(); }
      })
      .on(E.LocalTrackPublished, (pub) => { if (pub.track && pub.track.kind === 'video') this.videos.set(room.localParticipant.identity, pub.track); renderTiles(); renderCtl(); })
      .on(E.LocalTrackUnpublished, (pub) => { if (pub.track && pub.track.kind === 'video') this.videos.delete(room.localParticipant.identity); renderTiles(); renderCtl(); })
      .on(E.TrackMuted, () => { renderTilesState(); renderCtl(); })
      .on(E.TrackUnmuted, () => { renderTilesState(); renderCtl(); })
      .on(E.ActiveSpeakersChanged, (sp) => { ST.speaking = new Set(sp.map((p) => p.identity)); renderTilesState(); })
      .on(E.DataReceived, (payload, p, kind, topic) => this.onData(payload, p, topic))
      .on(E.Reconnecting, () => toast(t('reconnecting')))
      .on(E.AudioPlaybackStatusChanged, () => { if (!room.canPlaybackAudio) this.audioPrompt(); })
      .on(E.Disconnected, () => { if (ST.joined && T === this) { toast(t('lkFail')); T = new FallbackTransport(this.join); T.start(); renderAll(); } });
    await room.connect(this.join.url, this.join.token);
    if (ST.wantMic || ST.wantCam) {
      try {
        if (ST.wantMic) await room.localParticipant.setMicrophoneEnabled(true);
        if (ST.wantCam) await room.localParticipant.setCameraEnabled(true);
      } catch (e) { toast(t('camDenied')); }
    }
    if (!room.canPlaybackAudio) this.audioPrompt();
    // a newcomer asks who leads; the leader answers
    this.send('mode', { type: 'hello' }, true);
    renderCtl();
  }
  audioPrompt() {
    toast(t('audio'));
    const b = h('button', { type: 'button', class: 'nltg-btn teal', text: t('audio'), style: { position: 'absolute', insetBlockStart: '96px', left: '50%', transform: 'translateX(-50%)' }, onclick: () => { this.room.startAudio().catch(() => {}); b.remove(); } });
    R.append(b);
  }
  roleOf(p) { try { return (JSON.parse((p && p.metadata) || '{}').role) || 'buyer'; } catch (e) { return 'buyer'; } }
  peopleList() {
    if (!this.room) return [];
    const lp = this.room.localParticipant;
    const out = [{ pid: lp.identity, name: ST.me.name, role: ST.me.role, me: true, on: true, muted: !lp.isMicrophoneEnabled, p: lp }];
    for (const p of this.room.remoteParticipants.values()) out.push({ pid: p.identity, name: p.name || '', role: this.roleOf(p), on: true, muted: !p.isMicrophoneEnabled, p });
    return out;
  }
  attachVideo(person, el) {
    const track = this.videos.get(person.pid);
    let v = el.querySelector('video');
    if (track && !track.isMuted) {
      if (!v) { v = h('video', { autoplay: true, playsinline: true, muted: true }); v.muted = true; el.prepend(v); }
      if (v.dataset.sid !== track.sid) { track.attach(v); v.dataset.sid = track.sid || '1'; }
      el.classList.add('has-video');
    } else {
      if (v) { if (track) track.detach(v); v.remove(); }
      el.classList.remove('has-video');
    }
  }
  micOn() { return !!(this.room && this.room.localParticipant.isMicrophoneEnabled); }
  camOn() { return !!(this.room && this.room.localParticipant.isCameraEnabled); }
  async toggleMic() { try { await this.room.localParticipant.setMicrophoneEnabled(!this.micOn()); } catch (e) { toast(t('camDenied')); } renderCtl(); renderTilesState(); }
  async toggleCam() { try { await this.room.localParticipant.setCameraEnabled(!this.camOn()); } catch (e) { toast(t('camDenied')); } renderCtl(); renderTiles(); }
  send(topic, obj, reliable, to) {
    if (!this.room) return false;
    try {
      const o = { reliable: !!reliable, topic };
      if (to) o.destinationIdentities = to;
      this.room.localParticipant.publishData(new TextEncoder().encode(JSON.stringify(obj)), o);
      return true;
    } catch (e) { return false; }
  }
  sendState(snap) { return this.send('view', { type: 'state', s: snap }, false); }
  sendMode(m) { this.send('mode', { type: 'mode', m }, true); ST.lastSent = ''; }
  hello(identity) { if (amLeader()) { this.send('mode', { type: 'lead', on: true, name: ST.me.name }, true, [identity]); ST.lastSent = ''; } }
  setLead(on) {
    setLeader(on ? ST.me.pid : '', on ? ST.me.name : '');
    this.send('mode', { type: 'lead', on: !!on, name: ST.me.name }, true);
    ST.lastSent = '';
    api('POST', 'room/state', { room: ST.room, pid: ST.me.pid, key: ST.me.key, lead: !!on }); // the server knows too (the file, the admin list)
  }
  noteAdded(note) { this.send('notes', { type: 'add', note }, true); }
  noteDeleted(id) { this.send('notes', { type: 'del', id }, true); }
  onData(payload, p, topic) {
    let msg = null;
    try { msg = JSON.parse(new TextDecoder().decode(payload)); } catch (e) { return; }
    if (!msg || !p) return;
    if (topic === 'view' && msg.type === 'state') { if (p.identity === ST.leader) applyState(msg.s, 0.12); return; }
    if (topic === 'mode') {
      if (msg.type === 'hello') { this.hello(p.identity); return; }
      if (this.roleOf(p) !== 'rep') return; // only a representative leads (the role is in the server-signed token)
      if (msg.type === 'lead') setLeader(msg.on ? p.identity : (ST.leader === p.identity ? '' : ST.leader), msg.on ? (p.name || msg.name || '') : ST.leaderName);
      return;
    }
    if (topic === 'notes') { if (msg.type === 'add') upsertNote(msg.note); else if (msg.type === 'del') removeNote(msg.id); }
  }
  async leave() {
    try { await this.room.disconnect(); } catch (e) { /* none */ }
    this.audioBox.remove();
    if (ST.me) api('POST', 'room/state', { room: ST.room, pid: ST.me.pid, key: ST.me.key, leave: true, __keepalive: true });
  }
}

/* ------------------------------------------------------------------ helpers, start */

function waitFor(fn, ms) {
  return new Promise((res) => {
    const t0 = performance.now();
    const tick = () => { let v = null; try { v = fn(); } catch (e) { v = null; } if (v) res(v); else if (performance.now() - t0 > ms) res(null); else setTimeout(tick, 120); };
    tick();
  });
}
phoneMQ.addEventListener && phoneMQ.addEventListener('change', () => { if (ST.joined) renderAll(); });
window.addEventListener('resize', () => { if (ST.joined && ST.mode === 'plan') renderPlan(); });

window.__nlTogether = { state: ST, snapshot, applyState, setMode, pickAnchor, projectAnchor, leave }; // for the page's checks
boot();
