from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from tasks import TASK_PICK, IRREGULAR_VERBS
from data import irregular_verbs
from keyboards import to_menu_keyboard, main_menu_keyboard


async def start_irregular_verbs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    action = query.data

    if action == 'start':

        await context.bot.send_message(chat_id=update.callback_query.message.chat_id,
                                       text=f'Введіть дієслово:',
                                       parse_mode='HTML')

        return IRREGULAR_VERBS
    elif action == 'back':
        await context.bot.send_message(chat_id=update.callback_query.message.chat_id,
                                       text=f'<b>Головне меню</b>\n\n'
                                            f'Телеграм бот по вивченню англійських дієслів.\n\n'
                                            f'Обирай, що хочеш попрактикувати: ',
                                       parse_mode='HTML', reply_markup=InlineKeyboardMarkup(main_menu_keyboard))
        return TASK_PICK


async def irregular_verbs_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text: str = update.message.text.lower().strip()

    if text in irregular_verbs.keys():
        base, past_simple, past_participle = irregular_verbs[text].split(',')
        text = f'Форми дієслова {base}: \n\nBase - {base}\nPart Simple - {past_simple}\nPast Participle - {past_participle} \n\nПросто введи інше дієслово далі, щоб отримати його форми:'
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(to_menu_keyboard))
    else:
        await update.message.reply_text(f'Введене значення НЕ є неправильним дієсловом у початковій формі.\n\nЯкщо це правильне дієслово, то його інші форми створюються простим додаванням -ed в кінці.\n\nНаприклад:\nplay -> played або watch -> watched.\n\nВведи наступне дієслово:', reply_markup=InlineKeyboardMarkup(to_menu_keyboard))

    return IRREGULAR_VERBS
