"""🌍 Переводы сайта Fintra: азербайджанский, русский, английский.

Ключ — английский текст. Если перевода нет, показывается английский,
поэтому сайт никогда не «ломается» из-за пропущенной строки.
"""

LANGS = ("az", "ru", "en")
DEFAULT_LANG = "az"
LANG_COOKIE = "fintra_lang"

T = {
    # ---------- Общее: меню, шапка ----------
    "Count · Plan · Protect": {"az": "Sayır · Planlayır · Qoruyur", "ru": "Считает · Планирует · Защищает"},
    "Plans": {"az": "Planlayır", "ru": "Планирует"},
    "Protects": {"az": "Qoruyur", "ru": "Защищает"},
    "Overview": {"az": "Ümumi baxış", "ru": "Обзор"},
    "Expenses": {"az": "Xərclər", "ru": "Расходы"},
    "Plan & Limits": {"az": "Plan və limitlər", "ru": "План и лимиты"},
    "Chat": {"az": "Söhbət", "ru": "Чат"},
    "Security": {"az": "Təhlükəsizlik", "ru": "Безопасность"},
    "Telegram user": {"az": "Telegram istifadəçisi", "ru": "Пользователь Telegram"},
    "Log out": {"az": "Çıxış", "ru": "Выйти"},
    "Menu": {"az": "Menyu", "ru": "Меню"},
    "Telegram Synced": {"az": "Telegram ilə sinxron", "ru": "Синхронизировано с Telegram"},
    "Open @myfintra_bot": {"az": "@myfintra_bot-u aç", "ru": "Открыть @myfintra_bot"},
    "Cancel": {"az": "Ləğv et", "ru": "Отмена"},
    "Save": {"az": "Yadda saxla", "ru": "Сохранить"},
    "All": {"az": "Hamısı", "ru": "Все"},
    "Total": {"az": "Cəmi", "ru": "Итого"},
    "Category": {"az": "Kateqoriya", "ru": "Категория"},
    "Card": {"az": "Kart", "ru": "Карта"},
    "Description": {"az": "Təsvir", "ru": "Описание"},
    "Date": {"az": "Tarix", "ru": "Дата"},
    "Source": {"az": "Mənbə", "ru": "Источник"},
    "Amount": {"az": "Məbləğ", "ru": "Сумма"},
    "Delete": {"az": "Sil", "ru": "Удалить"},
    "This month": {"az": "Bu ay", "ru": "Этот месяц"},
    "Add expense": {"az": "Xərc əlavə et", "ru": "Добавить расход"},
    "Your limits": {"az": "Limitləriniz", "ru": "Ваши лимиты"},
    "No plan yet": {"az": "Hələ plan yoxdur", "ru": "Плана пока нет"},
    "No limits yet.": {"az": "Hələ limit yoxdur.", "ru": "Лимитов пока нет."},
    "You can spend today:": {"az": "Bu gün xərcləyə bilərsiniz:", "ru": "Сегодня можно потратить:"},
    "Spent: {spent} ₼ of {amount} ₼": {"az": "Xərclənib: {spent} ₼ / {amount} ₼", "ru": "Потрачено: {spent} ₼ из {amount} ₼"},

    # ---------- Категории ----------
    "Food": {"az": "Yemək", "ru": "Еда"},
    "Groceries": {"az": "Ərzaq", "ru": "Продукты"},
    "Cafe": {"az": "Kafe", "ru": "Кафе"},
    "Transport": {"az": "Nəqliyyat", "ru": "Транспорт"},
    "Education": {"az": "Təhsil", "ru": "Образование"},
    "Entertainment": {"az": "Əyləncə", "ru": "Развлечения"},
    "Clothes": {"az": "Geyim", "ru": "Одежда"},
    "Health": {"az": "Sağlamlıq", "ru": "Здоровье"},
    "Communication": {"az": "Rabitə", "ru": "Связь"},
    "Other": {"az": "Digər", "ru": "Другое"},

    # ---------- Статусы лимитов ----------
    "On track": {"az": "Qaydasındadır", "ru": "В норме"},
    "Close to limit": {"az": "Limitə yaxındır", "ru": "Близко к лимиту"},
    "Over limit": {"az": "Limit keçilib", "ru": "Лимит превышен"},

    # ---------- Периоды и источники ----------
    "Today": {"az": "Bu gün", "ru": "Сегодня"},
    "This week": {"az": "Bu həftə", "ru": "Эта неделя"},
    "All time": {"az": "Bütün dövr", "ru": "За всё время"},
    "Text": {"az": "Mətn", "ru": "Текст"},
    "Receipt photo": {"az": "Çek şəkli", "ru": "Фото чека"},
    "Voice": {"az": "Səs", "ru": "Голос"},

    # ---------- Вход (welcome) ----------
    "Welcome": {"az": "Xoş gəlmisiniz", "ru": "Добро пожаловать"},
    "The link is invalid, already used or expired.": {
        "az": "Link etibarsızdır, artıq istifadə olunub və ya vaxtı bitib.",
        "ru": "Ссылка недействительна, уже использована или устарела."},
    "Each link works only once and for 10 minutes. Please request a new one.": {
        "az": "Hər link yalnız bir dəfə və 10 dəqiqə işləyir. Zəhmət olmasa yenisini istəyin.",
        "ru": "Каждая ссылка работает один раз и 10 минут. Запросите новую."},
    "How to sign in:": {"az": "Necə daxil olmaq olar:", "ru": "Как войти:"},
    "1. Open the bot in Telegram:": {"az": "1. Telegram-da botu açın:", "ru": "1. Откройте бота в Telegram:"},
    "2. Send the command": {"az": "2. Bu əmri göndərin:", "ru": "2. Отправьте команду"},
    "3. Open the personal link from the bot": {"az": "3. Botun göndərdiyi şəxsi linki açın", "ru": "3. Откройте личную ссылку от бота"},
    "No passwords. The link is single-use and expires in 10 minutes. Never share it with anyone.": {
        "az": "Parol yoxdur. Link birdəfəlikdir və 10 dəqiqəyə etibarsız olur. Onu heç kimlə paylaşmayın.",
        "ru": "Без паролей. Ссылка одноразовая и действует 10 минут. Никому её не пересылайте."},
    "You have been logged out.": {"az": "Hesabdan çıxdınız.", "ru": "Вы вышли из аккаунта."},
    "All your data has been deleted.": {"az": "Bütün məlumatlarınız silindi.", "ru": "Все ваши данные удалены."},

    # ---------- Overview ----------
    "Expense saved": {"az": "Xərc yadda saxlanıldı", "ru": "Расход сохранён"},
    "{days} days until payday ({date})": {"az": "Maaşa {days} gün qalıb ({date})", "ru": "До зарплаты {days} дн. ({date})"},
    "Daily allowance": {"az": "Gündəlik limit", "ru": "Дневной бюджет"},
    "Based on your plan: {amount} ₼ to live on this month.": {
        "az": "Planınıza görə: bu ay yaşamaq üçün {amount} ₼.",
        "ru": "По вашему плану: {amount} ₼ на жизнь в этом месяце."},
    "{amount} ₼ spent today": {"az": "bu gün {amount} ₼ xərclənib", "ru": "сегодня потрачено {amount} ₼"},
    "Create your plan to see how much you can spend today": {
        "az": "Bu gün nə qədər xərcləyə biləcəyinizi görmək üçün plan yaradın",
        "ru": "Создайте план, чтобы видеть, сколько можно потратить сегодня"},
    "Tell Fintra your income, payday and fixed payments, for example:": {
        "az": "Fintra-ya gəlirinizi, maaş gününü və sabit ödənişləri yazın, məsələn:",
        "ru": "Напишите Fintra доход, день зарплаты и обязательные платежи, например:"},
    "\"My salary is 1000, it comes on the 5th, rent 350\"": {
        "az": "\"Maaşım 1000-dir, ayın 5-də gəlir, kirayə 350\"",
        "ru": "\"Моя зарплата 1000, приходит 5-го числа, аренда 350\""},
    "Ask Fintra": {"az": "Fintra-dan soruş", "ru": "Спросить Fintra"},
    "Spent this month": {"az": "Bu ay xərclənib", "ru": "Потрачено за месяц"},
    "expenses since {date}": {"az": "xərc ({date} tarixindən)", "ru": "расходов с {date}"},
    "Planned savings": {"az": "Planlaşdırılan qənaət", "ru": "Запланированные сбережения"},
    "{percent}% of free money, chosen by you": {
        "az": "Sərbəst pulun {percent}%-i, sizin seçiminiz",
        "ru": "{percent}% свободных денег, ваш выбор"},
    "Remaining until payday": {"az": "Maaşa qədər qalan", "ru": "Осталось до зарплаты"},
    "Spent since payday:": {"az": "Maaşdan bəri xərclənib:", "ru": "Потрачено с зарплаты:"},
    "{days}d left": {"az": "{days} gün qalıb", "ru": "осталось {days} дн."},
    "Spending breakdown": {"az": "Xərclərin bölgüsü", "ru": "Структура расходов"},
    "No expenses this month yet.": {"az": "Bu ay hələ xərc yoxdur.", "ru": "В этом месяце расходов пока нет."},
    "Latest": {"az": "Sonuncular", "ru": "Последние"},
    "5 latest expenses": {"az": "Son 5 xərc", "ru": "5 последних расходов"},
    "View all": {"az": "Hamısına bax", "ru": "Смотреть все"},
    "No expenses yet. Send one to the bot, for example \"coffee 3 manat\", or press \"Add expense\".": {
        "az": "Hələ xərc yoxdur. Bota yazın, məsələn \"qəhvə 3 manat\", və ya \"Xərc əlavə et\" düyməsini basın.",
        "ru": "Расходов пока нет. Напишите боту, например «кофе 3 маната», или нажмите «Добавить расход»."},
    "No limits yet. Ask Fintra, for example: \"Set a limit of 60 manat for cafes\".": {
        "az": "Hələ limit yoxdur. Fintra-ya yazın, məsələn: \"Kafeyə 60 manat limit qoy\".",
        "ru": "Лимитов пока нет. Напишите Fintra, например: «Поставь лимит 60 манат на кафе»."},
    "It will also be visible in the Telegram bot. Never type card numbers here.": {
        "az": "Bu, Telegram botunda da görünəcək. Burada heç vaxt kart nömrəsi yazmayın.",
        "ru": "Это будет видно и в Telegram-боте. Никогда не вводите здесь номера карт."},
    "Amount (₼)": {"az": "Məbləğ (₼)", "ru": "Сумма (₼)"},
    "e.g. coffee, Bravo, Bolt": {"az": "məs. qəhvə, Bravo, Bolt", "ru": "напр. кофе, Bravo, Bolt"},

    # ---------- Expenses ----------
    "Expense deleted": {"az": "Xərc silindi", "ru": "Расход удалён"},
    "Your expenses": {"az": "Xərcləriniz", "ru": "Ваши расходы"},
    "Everything you sent to Fintra: texts, receipt photos and voice notes.": {
        "az": "Fintra-ya göndərdiyiniz hər şey: mətnlər, çek şəkilləri və səsli mesajlar.",
        "ru": "Всё, что вы отправили Fintra: тексты, фото чеков и голосовые."},
    "Average expense": {"az": "Orta xərc", "ru": "Средний расход"},
    "per expense": {"az": "bir xərc üzrə", "ru": "на один расход"},
    "Period": {"az": "Dövr", "ru": "Период"},
    "Apply": {"az": "Tətbiq et", "ru": "Применить"},
    "Delete this expense?": {"az": "Bu xərc silinsin?", "ru": "Удалить этот расход?"},
    "No expenses for these filters.": {"az": "Bu filtrlər üzrə xərc yoxdur.", "ru": "По этим фильтрам расходов нет."},
    "Showing the latest {limit} expenses. Use the filters to narrow the list.": {
        "az": "Son {limit} xərc göstərilir. Siyahını daraltmaq üçün filtrlərdən istifadə edin.",
        "ru": "Показаны последние {limit} расходов. Сузьте список фильтрами."},

    # ---------- Plan & Limits ----------
    "Your monthly plan and spending limits. The same data as in the Telegram bot.": {
        "az": "Aylıq planınız və xərc limitləriniz. Telegram botundakı məlumatların eynisi.",
        "ru": "Ваш месячный план и лимиты расходов. Те же данные, что в Telegram-боте."},
    "Your monthly plan": {"az": "Aylıq planınız", "ru": "Ваш месячный план"},
    "Payday: day {day}": {"az": "Maaş günü: ayın {day}-i", "ru": "Зарплата: {day}-го числа"},
    "Income": {"az": "Gəlir", "ru": "Доход"},
    "Fixed payments": {"az": "Sabit ödənişlər", "ru": "Обязательные платежи"},
    "Savings": {"az": "Qənaət", "ru": "Сбережения"},
    "To live on": {"az": "Yaşamaq üçün", "ru": "На жизнь"},
    "{days} days until payday": {"az": "maaşa {days} gün qalıb", "ru": "до зарплаты {days} дн."},
    "Change your plan": {"az": "Planı dəyiş", "ru": "Изменить план"},
    "Create your plan": {"az": "Plan yarat", "ru": "Создать план"},
    "You decide how much to save. 20% is a common choice, 0 is fine too.": {
        "az": "Nə qədər qənaət edəcəyinizi siz qərar verirsiniz. 20% geniş yayılmış seçimdir, 0 da olar.",
        "ru": "Сколько откладывать, решаете вы. 20% — частый выбор, 0 тоже можно."},
    "Monthly income (₼)": {"az": "Aylıq gəlir (₼)", "ru": "Доход в месяц (₼)"},
    "Payday (day of month)": {"az": "Maaş günü (ayın günü)", "ru": "День зарплаты (число)"},
    "Savings (%)": {"az": "Qənaət (%)", "ru": "Сбережения (%)"},
    "Fixed payments (rent, loans, utilities)": {
        "az": "Sabit ödənişlər (kirayə, kreditlər, kommunal)",
        "ru": "Обязательные платежи (аренда, кредиты, коммуналка)"},
    "e.g. rent": {"az": "məs. kirayə", "ru": "напр. аренда"},
    "Save plan": {"az": "Planı yadda saxla", "ru": "Сохранить план"},
    "Monthly limits. Fintra warns you at 80% and 100%.": {
        "az": "Aylıq limitlər. Fintra 80% və 100%-də xəbərdarlıq edir.",
        "ru": "Месячные лимиты. Fintra предупредит на 80% и 100%."},
    "Remove this limit?": {"az": "Bu limit silinsin?", "ru": "Удалить этот лимит?"},
    "Remove limit": {"az": "Limiti sil", "ru": "Удалить лимит"},
    "Add a limit": {"az": "Limit əlavə et", "ru": "Добавить лимит"},
    "For": {"az": "Nə üçün", "ru": "Для"},
    "Monthly limit (₼)": {"az": "Aylıq limit (₼)", "ru": "Лимит в месяц (₼)"},
    "Card name": {"az": "Kartın adı", "ru": "Название карты"},
    "e.g. Birbank": {"az": "məs. Birbank", "ru": "напр. Birbank"},
    "🔐 Only a name, never the card number.": {
        "az": "🔐 Yalnız ad, heç vaxt kart nömrəsi yox.",
        "ru": "🔐 Только название, никогда не номер карты."},
    "Add limit": {"az": "Limit əlavə et", "ru": "Добавить лимит"},
    "Plan saved": {"az": "Plan yadda saxlanıldı", "ru": "План сохранён"},
    "Limit saved": {"az": "Limit yadda saxlanıldı", "ru": "Лимит сохранён"},
    "Limit removed": {"az": "Limit silindi", "ru": "Лимит удалён"},
    "Limit not found": {"az": "Limit tapılmadı", "ru": "Лимит не найден"},
    "Please fill income, payday and savings with numbers": {
        "az": "Gəlir, maaş günü və qənaəti rəqəmlə doldurun",
        "ru": "Заполните доход, день зарплаты и сбережения числами"},

    # ---------- Chat ----------
    "The same AI agent as in Telegram": {"az": "Telegram-dakı eyni AI agent", "ru": "Тот же AI-агент, что в Telegram"},
    "Type an expense, ask about your spending or paste a suspicious SMS. Everything you save here is also visible in the Telegram bot.": {
        "az": "Xərc yazın, xərcləriniz barədə soruşun və ya şübhəli SMS-i yapışdırın. Burada saxladığınız hər şey Telegram botunda da görünür.",
        "ru": "Напишите расход, спросите о тратах или вставьте подозрительное SMS. Всё сохранённое здесь видно и в Telegram-боте."},
    "Try asking": {"az": "Bunu yoxlayın", "ru": "Попробуйте спросить"},
    "📸 🎙 Photos and voice notes": {"az": "📸 🎙 Şəkillər və səsli mesajlar", "ru": "📸 🎙 Фото и голосовые"},
    "Send receipt photos and voice messages in Telegram. The website chat supports text.": {
        "az": "Çek şəkillərini və səsli mesajları Telegram-da göndərin. Saytdakı söhbət mətni dəstəkləyir.",
        "ru": "Фото чеков и голосовые отправляйте в Telegram. Чат на сайте поддерживает текст."},
    "Chat with Fintra": {"az": "Fintra ilə söhbət", "ru": "Чат с Fintra"},
    "Salam! Привет! Hi! 👋 I am Fintra. How can I help with your money today?": {
        "az": "Salam! 👋 Mən Fintra-yam. Bu gün pulunuzla bağlı necə kömək edə bilərəm?",
        "ru": "Привет! 👋 Я Fintra. Чем помочь с деньгами сегодня?",
        "en": "Hi! 👋 I am Fintra. How can I help with your money today?"},
    "Type a message… e.g. coffee 3 manat": {"az": "Mesaj yazın… məs. qəhvə 3 manat", "ru": "Напишите сообщение… напр. кофе 3 маната"},
    "Processed by Google Gemini. Messages with card numbers are blocked automatically.": {
        "az": "Google Gemini tərəfindən emal olunur. Kart nömrəsi olan mesajlar avtomatik bloklanır.",
        "ru": "Обрабатывается Google Gemini. Сообщения с номерами карт блокируются автоматически."},
    "✅ Yes": {"az": "✅ Bəli", "ru": "✅ Да"},
    "❌ No": {"az": "❌ Xeyr", "ru": "❌ Нет"},
    "⚠️ Something went wrong. Please try again.": {
        "az": "⚠️ Nəsə alınmadı. Yenidən cəhd edin.",
        "ru": "⚠️ Что-то пошло не так. Попробуйте ещё раз."},
    "Chart": {"az": "Diaqram", "ru": "Диаграмма"},
    "🚫 Your message contained a card number, so it was not sent. Never share card numbers, CVV or PIN — not even with me.": {
        "az": "🚫 Mesajınızda kart nömrəsi var idi, ona görə göndərilmədi. Kart nömrəsini, CVV və PIN-i heç kimə, hətta mənə də verməyin.",
        "ru": "🚫 В сообщении был номер карты, поэтому оно не отправлено. Никогда не сообщайте номер карты, CVV или PIN — даже мне."},
    "🔐 Remove limit? {scope}: {target} — {amount} ₼": {
        "az": "🔐 Limit silinsin? {scope}: {target} — {amount} ₼",
        "ru": "🔐 Удалить лимит? {scope}: {target} — {amount} ₼"},
    "⚠️ Request not found": {"az": "⚠️ Sorğu tapılmadı", "ru": "⚠️ Запрос не найден"},
    "⌛ Request expired": {"az": "⌛ Sorğunun vaxtı bitib", "ru": "⌛ Время запроса истекло"},
    "❌ Cancelled": {"az": "❌ Ləğv edildi", "ru": "❌ Отменено"},
    "✅ Limit removed": {"az": "✅ Limit silindi", "ru": "✅ Лимит удалён"},
    "⚠️ Limit not found": {"az": "⚠️ Limit tapılmadı", "ru": "⚠️ Лимит не найден"},
    "⚠️ Unknown action": {"az": "⚠️ Naməlum əməliyyat", "ru": "⚠️ Неизвестное действие"},

    # ---------- Security ----------
    "Security & Privacy": {"az": "Təhlükəsizlik və məxfilik", "ru": "Безопасность и приватность"},
    "Exactly what Fintra stores, what it never stores, and how your messages are processed. You stay in control of your data.": {
        "az": "Fintra nəyi saxlayır, nəyi heç vaxt saxlamır və mesajlarınız necə emal olunur. Məlumatlarınız sizin nəzarətinizdədir.",
        "ru": "Что именно хранит Fintra, что никогда не хранит и как обрабатываются ваши сообщения. Ваши данные под вашим контролем."},
    "Fintra never stores or asks for": {"az": "Fintra heç vaxt saxlamır və istəmir", "ru": "Fintra никогда не хранит и не спрашивает"},
    "🚫 Card numbers, CVV, PIN, SMS codes or passwords. Messages with a card number are deleted automatically.": {
        "az": "🚫 Kart nömrəsi, CVV, PIN, SMS kodları və parollar. Kart nömrəsi olan mesajlar avtomatik silinir.",
        "ru": "🚫 Номера карт, CVV, PIN, SMS-коды и пароли. Сообщения с номером карты удаляются автоматически."},
    "🚫 Bank logins. Fintra has no access to your bank and cannot make payments.": {
        "az": "🚫 Bank girişləri. Fintra-nın bankınıza çıxışı yoxdur və ödəniş edə bilməz.",
        "ru": "🚫 Логины от банка. У Fintra нет доступа к вашему банку, она не может проводить платежи."},
    "🚫 Your receipt photos and voice notes: they are only read once and not saved.": {
        "az": "🚫 Çek şəkilləri və səsli mesajlar: yalnız bir dəfə oxunur və saxlanılmır.",
        "ru": "🚫 Фото чеков и голосовые: читаются один раз и не сохраняются."},
    "What Fintra stores": {"az": "Fintra nəyi saxlayır", "ru": "Что хранит Fintra"},
    "Separated by your Telegram ID: only you see your data.": {
        "az": "Telegram ID-nizə görə ayrılır: məlumatlarınızı yalnız siz görürsünüz.",
        "ru": "Разделено по вашему Telegram ID: ваши данные видите только вы."},
    "✅ Expenses: amount, category, short description, date, card name (e.g. \"Birbank\")": {
        "az": "✅ Xərclər: məbləğ, kateqoriya, qısa təsvir, tarix, kartın adı (məs. \"Birbank\")",
        "ru": "✅ Расходы: сумма, категория, короткое описание, дата, название карты (напр. «Birbank»)"},
    "✅ Your budget plan and spending limits": {"az": "✅ Büdcə planınız və xərc limitləriniz", "ru": "✅ Ваш план бюджета и лимиты"},
    "✅ Website sessions (only as a SHA-256 hash, they expire after 24 hours)": {
        "az": "✅ Sayt sessiyaları (yalnız SHA-256 heş kimi, 24 saatdan sonra bitir)",
        "ru": "✅ Сессии сайта (только в виде SHA-256 хеша, истекают через 24 часа)"},
    "Your data right now": {"az": "Hazırda məlumatlarınız", "ru": "Ваши данные сейчас"},
    "Limits": {"az": "Limitlər", "ru": "Лимиты"},
    "Budget plan": {"az": "Büdcə planı", "ru": "План бюджета"},
    "Yes": {"az": "Bəli", "ru": "Да"},
    "No": {"az": "Xeyr", "ru": "Нет"},
    "Active web sessions": {"az": "Aktiv sayt sessiyaları", "ru": "Активные сессии сайта"},
    "How your messages are processed": {"az": "Mesajlarınız necə emal olunur", "ru": "Как обрабатываются ваши сообщения"},
    "🤖 Texts, receipt photos and voice notes are sent to Google Gemini to understand them.": {
        "az": "🤖 Mətnlər, çek şəkilləri və səsli mesajlar başa düşülmək üçün Google Gemini-yə göndərilir.",
        "ru": "🤖 Тексты, фото чеков и голосовые отправляются в Google Gemini, чтобы их понять."},
    "💳 Card numbers are detected with the Luhn algorithm and blocked before anything reaches the AI.": {
        "az": "💳 Kart nömrələri Luhn alqoritmi ilə aşkarlanır və AI-yə çatmazdan əvvəl bloklanır.",
        "ru": "💳 Номера карт распознаются алгоритмом Луна и блокируются до того, как что-то попадёт в AI."},
    "🔐 Removing a limit or deleting your data needs your confirmation. The AI can only ask.": {
        "az": "🔐 Limitin silinməsi və ya məlumatların silinməsi sizin təsdiqinizi tələb edir. AI yalnız soruşa bilər.",
        "ru": "🔐 Удаление лимита или данных требует вашего подтверждения. AI может только спросить."},
    "🛡 Text inside photos, voice notes and forwarded messages is treated as data, never as commands for the AI.": {
        "az": "🛡 Şəkillərdəki, səsli və yönləndirilmiş mesajlardakı mətn AI üçün əmr deyil, məlumat kimi qəbul edilir.",
        "ru": "🛡 Текст на фото, в голосовых и пересланных сообщениях считается данными, а не командами для AI."},
    "🔗 Website login uses one-time links from the bot: no passwords, each link works once for 10 minutes.": {
        "az": "🔗 Sayta giriş botdan gələn birdəfəlik linklərlə olur: parol yoxdur, hər link bir dəfə 10 dəqiqə işləyir.",
        "ru": "🔗 Вход на сайт по одноразовым ссылкам от бота: без паролей, каждая ссылка работает один раз 10 минут."},
    "🚨 Suspicious SMS are checked by rules in code first; the AI only explains the risk and cannot lower it.": {
        "az": "🚨 Şübhəli SMS-lər əvvəlcə koddakı qaydalarla yoxlanılır; AI yalnız riski izah edir və onu azalda bilməz.",
        "ru": "🚨 Подозрительные SMS сначала проверяются правилами в коде; AI только объясняет риск и не может его понизить."},
    "🛟 If Google Gemini is unavailable, a backup model answers (OpenRouter, or Ollama running locally on this computer).": {
        "az": "🛟 Google Gemini əlçatan olmasa, ehtiyat model cavab verir (OpenRouter və ya bu kompüterdə işləyən Ollama).",
        "ru": "🛟 Если Google Gemini недоступен, отвечает резервная модель (OpenRouter или Ollama прямо на этом компьютере)."},
    "Log out on all devices": {"az": "Bütün cihazlardan çıxış", "ru": "Выйти на всех устройствах"},
    "Ends every website session, including this one. Your data stays.": {
        "az": "Bu daxil olmaqla bütün sayt sessiyalarını bitirir. Məlumatlarınız qalır.",
        "ru": "Завершает все сессии сайта, включая эту. Данные остаются."},
    "Log out everywhere": {"az": "Hər yerdən çıx", "ru": "Выйти везде"},
    "⚠️ Irreversible action": {"az": "⚠️ Geri qaytarılmayan əməliyyat", "ru": "⚠️ Необратимое действие"},
    "Delete all my data": {"az": "Bütün məlumatlarımı sil", "ru": "Удалить все мои данные"},
    "Permanently deletes your expenses, budget plan, limits, charts and website sessions. This cannot be undone. The same as the /delete_my_data command in Telegram.": {
        "az": "Xərclərinizi, büdcə planınızı, limitlərinizi, diaqramlarınızı və sayt sessiyalarınızı həmişəlik silir. Bunu geri qaytarmaq olmaz. Telegram-dakı /delete_my_data əmri ilə eynidir.",
        "ru": "Навсегда удаляет расходы, план, лимиты, графики и сессии сайта. Отменить нельзя. То же самое, что команда /delete_my_data в Telegram."},
    "Type DELETE to confirm": {"az": "Təsdiq üçün DELETE yazın", "ru": "Для подтверждения введите DELETE"},
    "Delete ALL your data? This cannot be undone.": {
        "az": "BÜTÜN məlumatlarınız silinsin? Bunu geri qaytarmaq olmaz.",
        "ru": "Удалить ВСЕ ваши данные? Это нельзя отменить."},
    "You have been logged out on all devices.": {
        "az": "Bütün cihazlardan çıxış etdiniz.",
        "ru": "Вы вышли на всех устройствах."},
    "Data was NOT deleted: type DELETE exactly to confirm.": {
        "az": "Məlumatlar SİLİNMƏDİ: təsdiq üçün dəqiq DELETE yazın.",
        "ru": "Данные НЕ удалены: для подтверждения введите ровно DELETE."},
}


def translate(lang, text, **kwargs):
    """Перевод строки. Нет перевода → английский оригинал."""
    variants = T.get(text, {})
    result = variants.get(lang) or variants.get("en") or text
    return result.format(**kwargs) if kwargs else result


def pick_lang(query_lang, cookie_lang, accept_language):
    """🔐 Язык выбираем только из нашего списка: ?lang= → cookie → язык браузера → az."""
    for candidate in (query_lang, cookie_lang):
        if candidate in LANGS:
            return candidate
    for part in (accept_language or "").lower().split(","):
        code = part.strip()[:2]
        if code in LANGS:
            return code
    return DEFAULT_LANG
