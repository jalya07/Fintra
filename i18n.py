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
    "✅ Website sessions (only as a SHA-256 hash; they end after 30 days without visits)": {
        "az": "✅ Sayt sessiyaları (yalnız SHA-256 heş kimi; 30 gün daxil olmasanız bitir)",
        "ru": "✅ Сессии сайта (только в виде SHA-256 хеша; заканчиваются через 30 дней без визитов)"},
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
    # ---------- Privacy Policy ----------
    "Privacy Policy": {"az": "Məxfilik siyasəti", "ru": "Политика конфиденциальности"},
    "Last updated: {date}": {"az": "Son yenilənmə: {date}", "ru": "Обновлено: {date}"},
    "Open Fintra": {"az": "Fintra-nı aç", "ru": "Открыть Fintra"},
    "privacy_intro": {
        "en": "Fintra is an AI finance assistant in Telegram and on the web. Your financial data is personal, so here we explain in plain words what we store, why, who processes it and how you can delete it.",
        "az": "Fintra Telegram-da və saytda işləyən AI maliyyə köməkçisidir. Maliyyə məlumatlarınız şəxsidir, ona görə burada sadə sözlərlə izah edirik: nəyi saxlayırıq, nə üçün, kim emal edir və onu necə silə bilərsiniz.",
        "ru": "Fintra — AI-помощник по финансам в Telegram и на сайте. Финансовые данные — это личное, поэтому здесь простыми словами объясняем, что мы храним, зачем, кто это обрабатывает и как всё удалить."},
    "privacy_h1": {"en": "Who we are", "az": "Biz kimik", "ru": "Кто мы"},
    "privacy_p1": {
        "en": "Fintra is a student project created for the \"Agentic AI: From Models to Systems\" workshop (IMechE ASOIU Student Chapter, UFAZ). It is not a bank and not a commercial service. We do not show ads and do not sell or share your data for marketing.",
        "az": "Fintra \"Agentic AI: From Models to Systems\" vorkşopu (IMechE ASOIU Student Chapter, UFAZ) üçün hazırlanmış tələbə layihəsidir. Bu, bank və ya kommersiya xidməti deyil. Reklam göstərmirik, məlumatlarınızı satmırıq və marketinq üçün paylaşmırıq.",
        "ru": "Fintra — студенческий проект, созданный для воркшопа «Agentic AI: From Models to Systems» (IMechE ASOIU Student Chapter, UFAZ). Это не банк и не коммерческий сервис. Мы не показываем рекламу, не продаём ваши данные и не передаём их для маркетинга."},
    "privacy_h2": {"en": "What we store", "az": "Nəyi saxlayırıq", "ru": "Что мы храним"},
    "privacy_p2": {
        "en": "• Your Telegram ID, to keep your data separate from other users.\n• Expenses: amount, currency, category, short description, date, card name (for example \"Birbank\") and how it was added (text, photo or voice).\n• Your budget plan: income, payday, savings percent and fixed payments.\n• Your spending limits.\n• Chart images that Fintra draws for you.\n• Website login links and sessions, stored only as SHA-256 hashes.",
        "az": "• Telegram ID-niz, məlumatlarınızı digər istifadəçilərdən ayırmaq üçün.\n• Xərclər: məbləğ, valyuta, kateqoriya, qısa təsvir, tarix, kartın adı (məsələn \"Birbank\") və necə əlavə edildiyi (mətn, şəkil və ya səs).\n• Büdcə planınız: gəlir, maaş günü, qənaət faizi və sabit ödənişlər.\n• Xərc limitləriniz.\n• Fintra-nın sizin üçün çəkdiyi diaqramlar.\n• Sayta giriş linkləri və sessiyalar, yalnız SHA-256 heş kimi.",
        "ru": "• Ваш Telegram ID, чтобы отделять ваши данные от других пользователей.\n• Расходы: сумма, валюта, категория, короткое описание, дата, название карты (например «Birbank») и способ добавления (текст, фото или голос).\n• План бюджета: доход, день зарплаты, процент сбережений и обязательные платежи.\n• Лимиты расходов.\n• Графики, которые Fintra рисует для вас.\n• Ссылки для входа на сайт и сессии — только в виде SHA-256 хешей."},
    "privacy_h3": {"en": "What we never collect", "az": "Heç vaxt nəyi toplamırıq", "ru": "Что мы никогда не собираем"},
    "privacy_p3": {
        "en": "Card numbers, CVV, PIN, SMS codes, passwords or bank logins. A message with a card number is blocked before it reaches the AI, and in Telegram it is deleted from the chat. Fintra has no access to your bank account and cannot make payments. We do not save your chat history, receipt photos or voice messages.",
        "az": "Kart nömrələri, CVV, PIN, SMS kodları, parollar və ya bank girişləri. Kart nömrəsi olan mesaj AI-yə çatmazdan əvvəl bloklanır, Telegram-da isə söhbətdən silinir. Fintra-nın bank hesabınıza çıxışı yoxdur və ödəniş edə bilməz. Söhbət tarixçənizi, çek şəkillərini və səsli mesajları saxlamırıq.",
        "ru": "Номера карт, CVV, PIN, SMS-коды, пароли и логины от банка. Сообщение с номером карты блокируется до того, как попадёт в AI, а в Telegram удаляется из чата. У Fintra нет доступа к вашему банковскому счёту, она не может проводить платежи. Мы не сохраняем историю переписки, фото чеков и голосовые сообщения."},
    "privacy_h4": {"en": "Who processes your messages", "az": "Mesajlarınızı kim emal edir", "ru": "Кто обрабатывает ваши сообщения"},
    "privacy_p4": {
        "en": "• Telegram delivers messages between you and the bot.\n• Google Gemini reads your message, receipt photo or voice note to understand it and returns an answer.\n• If Gemini is unavailable, the text message goes to a backup model through OpenRouter. We turned off providers that may train on user data.\n• As the last backup, a model runs locally with Ollama on the computer where Fintra works: the data does not leave that computer.\nThese services process data under their own privacy policies.",
        "az": "• Telegram sizinlə bot arasında mesajları çatdırır.\n• Google Gemini mesajınızı, çek şəklini və ya səsli mesajı başa düşmək üçün oxuyur və cavab qaytarır.\n• Gemini əlçatan olmadıqda mətn mesajı OpenRouter vasitəsilə ehtiyat modelə gedir. İstifadəçi məlumatları ilə model öyrədə bilən provayderləri söndürmüşük.\n• Son ehtiyat kimi Fintra-nın işlədiyi kompüterdə Ollama ilə yerli model işləyir: məlumat həmin kompüterdən çıxmır.\nBu xidmətlər məlumatları öz məxfilik siyasətlərinə uyğun emal edir.",
        "ru": "• Telegram доставляет сообщения между вами и ботом.\n• Google Gemini читает сообщение, фото чека или голосовое, чтобы понять его, и возвращает ответ.\n• Если Gemini недоступен, текстовое сообщение уходит резервной модели через OpenRouter. Провайдеров, которые могут обучаться на данных пользователей, мы отключили.\n• Последний резерв — модель, которая работает локально через Ollama на компьютере, где запущена Fintra: данные не покидают этот компьютер.\nЭти сервисы обрабатывают данные по своим политикам конфиденциальности."},
    "privacy_h5": {"en": "How long we keep data", "az": "Məlumatları nə qədər saxlayırıq", "ru": "Сколько мы храним данные"},
    "privacy_p5": {
        "en": "Expenses, plan, limits and charts are kept until you delete them. A website session ends after 30 days without visits, a login link expires after 10 minutes and works only once. Technical server logs may briefly contain the actions the agent performed (for example, \"add expense 3 AZN, cafe\") to find errors.",
        "az": "Xərclər, plan, limitlər və diaqramlar siz silənə qədər saxlanılır. Sayt sessiyası 30 gün daxil olmasanız bitir, giriş linki 10 dəqiqədən sonra etibarsız olur və yalnız bir dəfə işləyir. Xətaları tapmaq üçün serverin texniki loqlarında agentin etdiyi əməliyyatlar (məsələn, \"xərc əlavə et 3 AZN, kafe\") qısa müddət qala bilər.",
        "ru": "Расходы, план, лимиты и графики хранятся, пока вы их не удалите. Сессия сайта заканчивается через 30 дней без визитов, ссылка для входа истекает через 10 минут и работает один раз. В технических логах сервера могут ненадолго оставаться действия агента (например, «добавить расход 3 AZN, кафе»), чтобы находить ошибки."},
    "privacy_h6": {"en": "You are in control", "az": "Nəzarət sizdədir", "ru": "Всё под вашим контролем"},
    "privacy_p6": {
        "en": "• See all your expenses, plan and limits on the website.\n• Delete a single expense on the Expenses page.\n• Delete all your data with the /delete_my_data command in Telegram or on the Security page. It is permanent and needs your confirmation.\n• Log out on all devices on the Security page.",
        "az": "• Bütün xərclərinizi, planınızı və limitlərinizi saytda görün.\n• Ayrı bir xərci Xərclər səhifəsində silin.\n• Bütün məlumatlarınızı Telegram-da /delete_my_data əmri ilə və ya Təhlükəsizlik səhifəsində silin. Bu, həmişəlikdir və təsdiqinizi tələb edir.\n• Təhlükəsizlik səhifəsində bütün cihazlardan çıxın.",
        "ru": "• Смотрите все расходы, план и лимиты на сайте.\n• Удаляйте отдельный расход на странице «Расходы».\n• Удалите все данные командой /delete_my_data в Telegram или на странице «Безопасность». Это навсегда и требует вашего подтверждения.\n• Выйдите на всех устройствах на странице «Безопасность»."},
    "privacy_h7": {"en": "How we protect data", "az": "Məlumatları necə qoruyuruq", "ru": "Как мы защищаем данные"},
    "privacy_p7": {
        "en": "Each request works only with the data of the signed-in user. Login links and sessions are stored as hashes, cookies are HttpOnly. Important actions (removing a limit, deleting data) happen only after your confirmation, the AI can only ask. Text inside photos and forwarded messages is treated as data, never as commands. Suspicious SMS are checked by rules in code, and the AI cannot lower the risk level. API keys are never stored in the code.",
        "az": "Hər sorğu yalnız daxil olmuş istifadəçinin məlumatları ilə işləyir. Giriş linkləri və sessiyalar heş kimi saxlanılır, cookie-lər HttpOnly-dir. Vacib əməliyyatlar (limitin silinməsi, məlumatların silinməsi) yalnız təsdiqinizdən sonra baş verir, AI yalnız soruşa bilər. Şəkillərdəki və yönləndirilmiş mesajlardakı mətn əmr deyil, məlumat kimi qəbul edilir. Şübhəli SMS-lər koddakı qaydalarla yoxlanılır və AI risk səviyyəsini azalda bilməz. API açarları heç vaxt kodda saxlanılmır.",
        "ru": "Каждый запрос работает только с данными вошедшего пользователя. Ссылки для входа и сессии хранятся в виде хешей, cookie — HttpOnly. Важные действия (удаление лимита, удаление данных) выполняются только после вашего подтверждения, AI может только спросить. Текст на фото и в пересланных сообщениях считается данными, а не командами. Подозрительные SMS проверяются правилами в коде, и AI не может понизить уровень риска. API-ключи никогда не хранятся в коде."},
    "privacy_h8": {"en": "Important", "az": "Vacibdir", "ru": "Важно"},
    "privacy_p8": {
        "en": "Fintra helps you track and plan your money, but it does not give investment, legal or tax advice. Always check important financial decisions yourself. If this policy changes, we will update the date at the top of this page.",
        "az": "Fintra pulunuzu izləməyə və planlaşdırmağa kömək edir, lakin investisiya, hüquqi və ya vergi məsləhəti vermir. Vacib maliyyə qərarlarını həmişə özünüz yoxlayın. Bu siyasət dəyişsə, səhifənin yuxarısındakı tarixi yeniləyəcəyik.",
        "ru": "Fintra помогает учитывать и планировать деньги, но не даёт инвестиционных, юридических и налоговых советов. Важные финансовые решения всегда проверяйте сами. Если политика изменится, мы обновим дату вверху страницы."},
    "privacy_h9": {"en": "Contact", "az": "Əlaqə", "ru": "Связь"},
    "privacy_p9": {
        "en": "Questions or found a problem? Write to us on GitHub:",
        "az": "Sualınız var və ya problem tapdınız? GitHub-da bizə yazın:",
        "ru": "Есть вопросы или нашли проблему? Напишите нам на GitHub:"},
    # ---------- PWA: установка и вход ----------
    "Install Fintra on your phone": {"az": "Fintra-nı telefonunuza quraşdırın", "ru": "Установите Fintra на телефон"},
    "Install": {"az": "Quraşdır", "ru": "Установить"},
    "iPhone: tap Share, then \u201cAdd to Home Screen\u201d.": {
        "az": "iPhone: \u201cPaylaş\u201d, sonra \u201cƏsas ekrana əlavə et\u201d düyməsinə toxunun.",
        "ru": "iPhone: нажмите \u201cПоделиться\u201d, затем \u201cНа экран Домой\u201d."},
    "Close": {"az": "Bağla", "ru": "Закрыть"},
    "Have a link from the bot? Paste it here:": {"az": "Botdan link var? Buraya yapışdırın:", "ru": "Есть ссылка от бота? Вставьте её сюда:"},
    "Paste the link": {"az": "Linki yapışdırın", "ru": "Вставьте ссылку"},
    "Sign in": {"az": "Daxil ol", "ru": "Войти"},
    "This does not look like a Fintra login link.": {"az": "Bu, Fintra giriş linkinə oxşamır.", "ru": "Это не похоже на ссылку для входа в Fintra."},
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
