from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os

TOKEN = '7291732021:AAFhKuOkHHLrWp99cfRN6pnIQ4mwg22iEec'
WEBHOOK_URL = 'https://telegrambot-patrem39.amvera.io'

REVIEWS_LINK = 'https://t.me/remizov_otziv'

PRODUCTS = {
    'tgpn': ("Терапевтическая группа по изучению потребностей", 
             "Запущена, можно присоединиться до 15 августа 2024. "
             "Терапевтическая группа по изучению потребностей - группа, где участники в небольшом кругу изучают свои потребности, "
             "прорабатывают блоки к их реализации, получают инструменты для самостоятельной работы и помогают друг другу в поиске потребностей и интеграции в жизнь полученных знаний. "
             "Стоимость 30 000 рублей.", "https://t.me/m/DknxCycKMzFi"),
    'ss': ("Стратегическая сессия", 
           "Анализ состояния вашей психики, вытаскиваем ваши глубинные желания и смотрим, что мешает вам их реализовать. "
           "С получившимся списком отправляю либо в личную работу, либо к другому специалисту, который поможет (врач, тренер, психиатр, другой психолог или кто-то ещё). "
           "Стоимость - 7000 рублей.", "https://t.me/m/wj50gp_vOTFi"),
    'lw': ("Личная работа", 
           "Глубинная работа над вашей психикой в течение 3-6 месяцев, проработка глубинных травм и неврозов. Фундаментальное решение самых волнующих и важных вопросов в вашей жизни. "
           "От 60 до 120 минут каждая сессия, раз в неделю на протяжении нескольких месяцев. Стратегическая сессия бесплатно. Стоимость - От 40 до 200 тысяч рублей.", 
           "https://t.me/m/HGjDH0znYzdi"),
    'wd': ("Воркшоп \"Истинные желания\"", 
           "Воркшоп о том, как найти свои истинные желания. Всё, что нужно от А до Я. Готовый план со всеми данными. "
           "Стоимость - 3000 рублей.", "https://t.me/m/4s936WzOZDRi"),
    'ps': ("Личная сессия поиска потребностей", 
           "Во время работы заметил, что большая часть людей понимает, что такое потребности тогда, когда могут за ручку дойти до них вместе со мной. "
           "Вот тогда-то паззл и складывается и наступает пора \"инсайтов\". Некоторые называют этот момент разделяющим на \"до\" и \"после\". "
           "Формат: 90 минут. 30 минут теории + 60 минут поиска разных потребностей + дальнейшие рекомендации. Стоимость - 7000 рублей.", 
           "https://t.me/m/8e4Do0ZjNTFi")
}

UPCOMING_PRODUCTS = {
    'npr': ("Воркшоп \"Потребности и отношения\"", 
            "Июль. Как сделать отношения глубоко гармоничными, полными понимания, благодарности и любви через работу с потребностями. "
            "(Воркшоп для пар и одиночек, которые хотят понять, как персонально им быть счастливыми в отношениях). "
            "Стоимость - 4000 рублей пара, 3000 рублей соло.", "https://t.me/+AJHfJgS03LxlOWNi"),
    'npd': ("Воркшоп \"Потребности и деньги\"", 
            "Август. Как увеличить свой доход через понимание потребностей себя и других людей. Как именно связаны потребности и деньги. "
            "Как потребности заставляют нас больше тратить и как могут помочь больше зарабатывать. Стоимость - 3000 рублей.", 
            "https://t.me/+M-R3xxeNrtE2OTYy"),
    'npc': ("Воркшоп \"Потребности и цели\"", 
            "Август. Как ставить цели, которые 100% сбудутся, а твоё тело и бессознательное будут тебе помогать в их реализации. "
            "Стоимость - 3000 рублей.", "https://t.me/+ljvOFnQOEVgzYTUy"),
    'rw': ("Воркшоп \"Как правильно отдыхать\"", 
           "Сентябрь. Как через призму понимания потребностей научиться грамотно расслабляться, эффективно восстанавливаться и отдыхать. "
           "Стоимость - 3000 рублей.", "https://t.me/+Ut6wiTMlbsgwZGYy"),
    'pt': ("Профессиональное 2-х месячное обучение", 
           "По набору группы. Групповое обучение, где я рассказываю обо всех самых передовых инструментах, которые есть у меня, и обучаю как работать этими инструментами с собой и другими. "
           "Стоимость - 70 000 рублей.", "https://t.me/+t3J4szFd4_kyODIy"),
    'ck': ("Закрытый клуб по подписке с базой знаний", 
           "По набору 50 заявок. Большая часть проведенных мной тренингов и воркшопов за 8 лет в доступе, регулярные контентные эфиры, уникальный контент с особенной глубиной - которую могут понять те, кто разбирается в вопросе не на уровне обывателя. "
           "Стоимость: 1500 рублей.", "https://t.me/+onfbgGd-aK0xMDNi"),
    'gnp': ("Второй поток группы по изучению своих потребностей", 
            "По набору группы. Четырехмесячное глубокое погружение в тему своих потребностей. Фундаментальное понимание себя и других через призму потребностей. "
            "Теория, практика, применение в жизнь. Один созвон в неделю, домашние задания, работа в парах. "
            "Стоимость - 40 000 рублей.", "https://t.me/+zGIETstU0V5lYzYy"),
    'msp': ("Записи медитаций для самостоятельной психологической проработки", 
            "По набору группы. Набор медитаций, которые я обычно делаю клиентам, адаптированные для самостоятельной работы. "
            "Многоразовые. Разбиты по темам: проработка обид, конфликтных ситуаций, самоценности и т.п. Медитации добавляются со временем. При покупке - вечный доступ. "
            "Стоимость - 7000 рублей.", "https://t.me/+oqPUqnNDinZlOTky"),
    'ppb': ("Психологический практикум \"База\"", 
            "По набору группы. Фундаментальная теория о том, как работает психика человека, как устроены травмы, как они лечатся и через какие инструменты. "
            "Стоимость 2000 рублей.", "https://t.me/+LDNsYAd0W7ExOTYy"),
    'vcc': ("Большой курс по ценностям", 
            "По набору группы. Бывший легендарный \"БДТ\". Стоимость 7000 рублей.", "https://t.me/+qhTi_PpWbWwwNmMy")
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Инфа о доступных сейчас проектах", callback_data='projects')],
        [InlineKeyboardButton("Инфа о готовящихся продуктах", callback_data='upcoming')],
        [InlineKeyboardButton("Лучшие статьи (в разработке)", callback_data='best_articles')],
        [InlineKeyboardButton("Бесплатные продукты (в разработке)", callback_data='free_products')],
        [InlineKeyboardButton("Отзывы", url=REVIEWS_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.message:
        await update.message.reply_text('Добро пожаловать! Выберите один из разделов:', reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.edit_message_text('Добро пожаловать! Выберите один из разделов:', reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == 'projects':
        keyboard = [[InlineKeyboardButton(PRODUCTS[code][0], callback_data=f'product_{code}')] for code in PRODUCTS.keys()]
        keyboard.append([InlineKeyboardButton("Назад", callback_data='back_to_main')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Информация о доступных сейчас проектах:", reply_markup=reply_markup)
    
    elif data == 'upcoming':
        keyboard = [[InlineKeyboardButton(UPCOMING_PRODUCTS[code][0], callback_data=f'upcoming_{code}')] for code in UPCOMING_PRODUCTS.keys()]
        keyboard.append([InlineKeyboardButton("Назад", callback_data='back_to_main')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Информация о готовящихся продуктах:", reply_markup=reply_markup)
    
    elif data == 'best_articles' or data == 'free_products':
        await query.edit_message_text(text="Эй, пирожок, не всё сразу, мне нужно немного времени, чтобы доделать это. Я тут всё делаю пока своими ручками 🤚🤚 (обе левые)", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data='back_to_main')]]))
    
    elif data == 'reviews':
        await query.edit_message_text(text="Отзывы:")  # Здесь можно добавить информацию о отзывах и кнопки
    
    elif data.startswith('product_'):
        code = data[len('product_'):]
        product_name, product_info, sign_up_link = PRODUCTS[code]
        keyboard = [
            [InlineKeyboardButton("Назад", callback_data='projects')],
            [InlineKeyboardButton("Записаться", url=sign_up_link)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=f"{product_name}\n\n{product_info}", reply_markup=reply_markup)

    elif data.startswith('upcoming_'):
        code = data[len('upcoming_'):]
        product_name, product_info, sign_up_link = UPCOMING_PRODUCTS[code]
        keyboard = [
            [InlineKeyboardButton("Назад", callback_data='upcoming')],
            [InlineKeyboardButton("Записаться в предсписок", url=sign_up_link)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=f"{product_name}\n\n{product_info}", reply_markup=reply_markup)

    elif data == 'back_to_main':
        await start(update, context)

def main() -> None:
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(button))

    # Устанавливаем вебхук
    app.run_webhook(listen="0.0.0.0",
                    port=int(os.environ.get('PORT', '8443')),
                    url_path=TOKEN,
                    webhook_url=f"{WEBHOOK_URL}/{TOKEN}")

if __name__ == '__main__':
    main()
