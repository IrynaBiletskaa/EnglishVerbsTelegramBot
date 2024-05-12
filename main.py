import json
from typing import Final
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ConversationHandler, CallbackQueryHandler, MessageHandler, \
    filters, ContextTypes
import random
from warnings import filterwarnings
from telegram.warnings import PTBUserWarning
from keyboards import main_menu_keyboard
from commands.irregular_verbs import *
from data import *
from tasks import TASK_PICK, START_IRREGULAR_VERBS, IRREGULAR_VERBS, START_TRANSLATE_UA_EN, TRANSLATE_UA_EN, \
    START_IRREGULAR_VERBS_PRACTICE, IRREGULAR_VERBS_PRACTICE, START_PHRASAL_VERBS, PHRASAL_VERBS_CATEGORY, \
    PHRASAL_VERBS, START_STATIVE_DYNAMIC_VERBS, STATIVE_DYNAMIC_VERBS

filterwarnings(action="ignore", message=r".*CallbackQueryHandler",
               category=PTBUserWarning)

TOKEN: Final = '*****'
BOT_USERNAME: Final = '@learn_english_verbs_dev_bot'


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'Привіт, {update.message.chat.first_name}!\n\n'
                                    f'Вітаємо тебе у чат-боті, з яким ти зможеш вивчати дієслова англійської мови 🥳.\n\n'
                                    f'Хутчіш обирай що саме ти хочеш практикувати в меню нижче і ходімо вчитися!', reply_markup=InlineKeyboardMarkup(main_menu_keyboard))
    return TASK_PICK


async def to_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    action = query.data

    if action == 'to_main_menu':
        await context.bot.send_message(chat_id=update.callback_query.message.chat_id,
                                       text=f'<b>Головне меню</b>\n\n'
                                            f'Телеграм бот для вивчення англійських дієслів.\n\n'
                                            f'Обирай, що хочеш попрактикувати: ',
                                       parse_mode='HTML', reply_markup=InlineKeyboardMarkup(main_menu_keyboard))
        return TASK_PICK


async def task_picker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    task = query.data

    keyboard = [
        [InlineKeyboardButton('Почати', callback_data='start')],
        [InlineKeyboardButton('Назад', callback_data='back')]
    ]

    if task == 'irregular_verbs':
        await context.bot.send_message(chat_id=update.callback_query.message.chat_id,
                                       text=f'<b>Неправильні дієслова</b>\n\n'
                                            f'У цьому завданні ти можеш пригадати форми неправильних дієслів.\n\n'
                                            f'Просто напиши мені початкову форму, а я вкажу всі інші!',
                                       parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard))
        return START_IRREGULAR_VERBS
    elif task == 'practice_irregular_verbs':
        await context.bot.send_message(chat_id=update.callback_query.message.chat_id,
                                       text=f'<b>Практика неправильних дієслів</b>\n\n'
                                            f'Тут ти зможеш перевірити свої знання неправильних дієслів.\n\n'
                                            f'Я надаватиму одну із форм і вкажу, яку форму тобі потрібно написати мені у відпровідь.\n\n'
                                            f'Якщо ти не можеш пригадати потрібну форму, просто попроси у мене допомоги і я залюбки тобі підкажу 😊',
                                       parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard))
        return START_IRREGULAR_VERBS_PRACTICE
    elif task == 'translate_verbs_ua_en':
        await context.bot.send_message(chat_id=update.callback_query.message.chat_id,
                                       text=f'<b>Переклад (UA → EN)</b>\n\n'
                                            f'У цьому завданні я пропоную тобі перекладати слова з української англійською.\n\n'
                                            f'У повідомлені я вкажу слово, а твоє завдання написати правильний переклад.\n\n'
                                            f'Якщо ти не знаєш певне дієслово, є можливість попросити моєї допомоги.\n\n'
                                            f'То що, поїхали? 🏃‍♂️ ',
                                       parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard))
        return START_TRANSLATE_UA_EN
    elif task == 'practice_phrasal_verbs':
        await context.bot.send_message(chat_id=update.callback_query.message.chat_id,
                                       text=f'<b>Фразові дієслова</b>\n\n'
                                            f'Давай повторимо фразові дієслова.\n\n'
                                            f'Я надаватиму частину фразового дієслова і його значення. Завдання - правильно його доповнити.\n\n'
                                            f'Якщо ти не знаєш правильну форму, я залюбки тобі допоможу :)',
                                       parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard))
        return START_PHRASAL_VERBS
    elif task == 'practice_stative_dynamic':
        await context.bot.send_message(chat_id=update.callback_query.message.chat_id,
                                       text=f'<b>Статичні та динамічні дієсслова</b>\n\n'
                                            f'Давай попрактикуємо переклад із використання'
                                            f'статичних та динамічних дієслів.\n\n'
                                            f'Я надаватиму речення українською. Завдання - правильно його перекласти.\n\n'
                                            f'Якщо ти не знаєш правильну форму, я залюбки тобі допоможу :)',
                                       parse_mode='HTML', reply_markup=InlineKeyboardMarkup(
                                           [
                                               [InlineKeyboardButton(
                                                   'Почати', callback_data='start')],
                                               [InlineKeyboardButton(
                                                   'Переглянути правило', callback_data='explanation')],
                                               [InlineKeyboardButton(
                                                   'Назад', callback_data='back')]
                                           ]
                                       ))
        return START_STATIVE_DYNAMIC_VERBS
    else:
        print('unknown_task')


async def start_irregular_verbs_practice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    action = query.data

    if action == 'start':
        verb = random.choice(list(irregular_verbs.keys()))
        verb_forms = irregular_verbs[verb].split(',')
        target_form = random.choice([1, 2])

        context.user_data['ir_practice_verb'] = verb
        context.user_data['ir_practice_form'] = target_form
        context.user_data['ir_practice_form_verb'] = verb_forms[target_form]

        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton('Не знаю', callback_data='dont_know')],
            [InlineKeyboardButton('Закінчити', callback_data='to_main_menu')]
        ])

        await context.bot.send_message(chat_id=update.callback_query.message.chat_id,
                                       text=f'Вкажи правильну форму:\n\n'
                                            f'Дієслово: <b>{verb}</b>\n'
                                            f'Форма: <b>{"Past Simple" if target_form == 1 else "Past Participle"}</b>',
                                       parse_mode='HTML',
                                       reply_markup=reply_markup)

        return IRREGULAR_VERBS_PRACTICE
    elif action == 'back':
        await context.bot.send_message(chat_id=update.callback_query.message.chat_id,
                                       text=f'<b>Головне меню</b>\n\n'
                                            f'Телеграм бот з вивчення англійських дієслів.\n\n'
                                            f'Обирай, що хочеш попрактикувати: ',
                                       parse_mode='HTML', reply_markup=InlineKeyboardMarkup(main_menu_keyboard))
        return TASK_PICK


async def irregular_verbs_practice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text: str = update.message.text.lower().strip()
    prev_verb: str = context.user_data['ir_practice_verb']
    prev_target_form: str = context.user_data['ir_practice_form']
    prev_target_form_value: str = context.user_data['ir_practice_form_verb']

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('Не знаю', callback_data='dont_know')],
        [InlineKeyboardButton('Закінчити', callback_data='to_main_menu')]
    ])

    if text == prev_target_form_value:
        next_verbs_options = list(
            filter(lambda v: v != prev_verb, list(irregular_verbs.keys())))
        verb = random.choice(next_verbs_options)
        verb_forms = irregular_verbs[verb].split(',')
        target_form = random.choice([1, 2])

        context.user_data['ir_practice_verb'] = verb
        context.user_data['ir_practice_form'] = target_form
        context.user_data['ir_practice_form_verb'] = verb_forms[target_form]

        await update.message.reply_text(f'✅ Правильно!\n\n'
                                        f'<b>{"Past Simple" if prev_target_form == 1 else "Past Participle"}</b> '
                                        f'дієслова <b>{prev_verb}</b> - <b>{prev_target_form_value}</b>\n\n'
                                        f'Наступне:\n\n'
                                        f'Дієслово: <b>{verb}</b>\n'
                                        f'Форма: <b>{"Past Simple" if target_form == 1 else "Past Participle"}</b>',
                                        parse_mode='HTML',
                                        reply_markup=reply_markup)
    else:
        await update.message.reply_text(f'❌ Неправильно, спробуй ще раз',
                                        parse_mode='HTML',
                                        reply_markup=reply_markup)

    return IRREGULAR_VERBS_PRACTICE


async def irregular_verbs_practice_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    action = query.data
    prev_verb: str = context.user_data['ir_practice_verb']
    prev_target_form: str = context.user_data['ir_practice_form']
    prev_target_form_value: str = context.user_data['ir_practice_form_verb']

    if action == 'dont_know':
        next_verbs_options = list(
            filter(lambda v: v != prev_verb, list(irregular_verbs.keys())))
        verb = random.choice(next_verbs_options)
        verb_forms = irregular_verbs[verb].split(',')
        target_form = random.choice([1, 2])

        context.user_data['ir_practice_verb'] = verb
        context.user_data['ir_practice_form'] = target_form
        context.user_data['ir_practice_form_verb'] = verb_forms[target_form]

        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton('Не знаю', callback_data='dont_know')],
            [InlineKeyboardButton('Закінчити', callback_data='to_main_menu')]
        ])

        await context.bot.send_message(chat_id=update.callback_query.message.chat_id,
                                       text=f'👌 Нічого страшного!\n\n'
                                       f'<b>{"Past Simple" if prev_target_form == 1 else "Past Participle"}</b> '
                                       f'дієслова <b>{prev_verb}</b> - <b>{prev_target_form_value}</b>\n\n'
                                       f'Наступне:\n\n'
                                       f'Дієслово: <b>{verb}</b>\n'
                                       f'Форма: <b>{"Past Simple" if target_form == 1 else "Past Participle"}</b>',
                                       parse_mode='HTML',
                                       reply_markup=reply_markup)

        return IRREGULAR_VERBS_PRACTICE
    elif action == 'to_main_menu':
        await context.bot.send_message(chat_id=update.callback_query.message.chat_id,
                                       text=f'<b>Головне меню</b>\n\n'
                                            f'Телеграм бот з вивчення англійських дієслів.\n\n'
                                            f'Обирай, що хочеш попрактикувати: ',
                                       parse_mode='HTML', reply_markup=InlineKeyboardMarkup(main_menu_keyboard))
        return TASK_PICK


async def start_verbs_translate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('start_verbs_translate_command')
    query = update.callback_query
    await query.answer()
    action = query.data

    if action == 'start':
        verb_to_translate = random.choice(list(verbs_translate.keys()))
        context.user_data['verb_to_translate'] = verb_to_translate

        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton('Не знаю', callback_data='dont_know')],
            [InlineKeyboardButton('Закінчити', callback_data='to_main_menu')]
        ])

        await context.bot.send_message(chat_id=update.callback_query.message.chat_id,
                                       text=f'Переклади - {verb_to_translate}',
                                       parse_mode='HTML', reply_markup=reply_markup)

        return TRANSLATE_UA_EN
    elif action == 'back':
        await context.bot.send_message(chat_id=update.callback_query.message.chat_id,
                                       text=f'<b>Головне меню</b>\n\n'
                                            f'Телеграм бот з вивчення англійських дієслів.\n\n'
                                            f'Обирай, що хочеш попрактикувати: ',
                                       parse_mode='HTML', reply_markup=InlineKeyboardMarkup(main_menu_keyboard))
        return TASK_PICK


async def verb_translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text: str = update.message.text.lower().strip()
    target: str = verbs_translate[context.user_data['verb_to_translate']]

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('Не знаю', callback_data='dont_know')],
        [InlineKeyboardButton('Закінчити', callback_data='to_main_menu')]
    ])

    if text == target:
        next_verbs_options = list(
            filter(lambda v: v != target, list(verbs_translate.keys())))
        verb_to_translate = random.choice(next_verbs_options)
        context.user_data['verb_to_translate'] = verb_to_translate
        await update.message.reply_text(f'✅ Правильно!\n\n'
                                        f'Наступне слово:\n\n'
                                        f'<b>{verb_to_translate}</b>',
                                        parse_mode='HTML',
                                        reply_markup=reply_markup)
    else:
        await update.message.reply_text(f'❌ Неправильно, спробуй ще раз',
                                        parse_mode='HTML',
                                        reply_markup=reply_markup)

    return TRANSLATE_UA_EN


async def verb_translate_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    action = query.data

    if action == 'dont_know':
        verb = context.user_data['verb_to_translate']
        target: str = verbs_translate[verb]

        next_verbs_options = list(
            filter(lambda v: v != target, list(verbs_translate.keys())))
        verb_to_translate = random.choice(next_verbs_options)
        context.user_data['verb_to_translate'] = verb_to_translate
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton('Не знаю', callback_data='dont_know')],
            [InlineKeyboardButton('Закінчити', callback_data='to_main_menu')]
        ])

        await context.bot.send_message(chat_id=update.callback_query.message.chat_id,
                                       text=f'👌 Нічого страшного!\n\n'
                                            f'{verb} - <b>{target}</b>.\n\nНаступне слово - {verb_to_translate}',
                                       parse_mode='HTML',
                                       reply_markup=reply_markup)

        return TRANSLATE_UA_EN
    elif action == 'to_main_menu':
        await context.bot.send_message(chat_id=update.callback_query.message.chat_id,
                                       text=f'<b>Головне меню</b>\n\n'
                                            f'Телеграм бот з вивчення англійських дієслів.\n\n'
                                            f'Обирай, що хочеш попрактикувати: ',
                                       parse_mode='HTML', reply_markup=InlineKeyboardMarkup(main_menu_keyboard))
        return TASK_PICK


async def start_phrasal_verbs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('start_phrasal_verbs')
    query = update.callback_query
    await query.answer()
    action = query.data

    print(action)

    if action == 'start':
        await context.bot.send_message(chat_id=update.callback_query.message.chat_id,
                                       text=f'Практика фразових дієслів.\n\n'
                                            f'Будь-ласка, обери категорію:',
                                       parse_mode='HTML', reply_markup=InlineKeyboardMarkup(
                                           [
                                               [InlineKeyboardButton(
                                                   'Довільна', callback_data='any')],
                                               [InlineKeyboardButton(
                                                   'TAKE', callback_data='take')],
                                               [InlineKeyboardButton(
                                                   'GET', callback_data='get')],
                                               [InlineKeyboardButton(
                                                   'LOOK', callback_data='look')],
                                           ]
                                       ))

        return PHRASAL_VERBS_CATEGORY
    elif action == 'back':
        await context.bot.send_message(chat_id=update.callback_query.message.chat_id,
                                       text=f'<b>Головне меню</b>\n\n'
                                            f'Телеграм бот з вивчення англійських дієслів.\n\n'
                                            f'Обирай, що хочеш попрактикувати: ',
                                       parse_mode='HTML', reply_markup=InlineKeyboardMarkup(main_menu_keyboard))
        return TASK_PICK


async def phrasal_verbs_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('phrasal_verbs_category')
    query = update.callback_query
    await query.answer()
    category = query.data
    if category == 'any':
        phrasal_verbs_to_pick = phrasal_verbs
    else:
        phrasal_verbs_to_pick = list(
            filter(lambda v: v['category'] == category, phrasal_verbs))

    context.user_data['phrasal_verbs_category'] = category
    target_phrasal_verb = random.choice(phrasal_verbs_to_pick)
    context.user_data['target_phrasal_verb'] = json.dumps(target_phrasal_verb)

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('Не знаю', callback_data='dont_know')],
        [InlineKeyboardButton('Закінчити', callback_data='to_main_menu')]
    ])

    await context.bot.send_message(chat_id=update.callback_query.message.chat_id,
                                   text=f'Починаємо!\n\n'
                                        f'Значення: <b>{target_phrasal_verb["translation"]}</b>\n\n'
                                        f'<b>{target_phrasal_verb["practice"]}</b>',
                                   parse_mode='HTML',
                                   reply_markup=reply_markup)

    return PHRASAL_VERBS


async def phrasal_verb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('phrasal_verb')
    text: str = update.message.text.lower().strip()
    target = json.loads(context.user_data['target_phrasal_verb'])
    users_phrasal_verb = target['practice'].replace("___", text)

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('Не знаю', callback_data='dont_know')],
        [InlineKeyboardButton('Закінчити', callback_data='to_main_menu')]
    ])

    if users_phrasal_verb == target["verb"]:

        category = context.user_data['phrasal_verbs_category']

        if category == 'any':
            phrasal_verbs_to_pick = phrasal_verbs
        else:
            phrasal_verbs_to_pick = list(filter(
                lambda v: v['category'] == category and v['verb'] != target['verb'], phrasal_verbs))

        target_phrasal_verb = random.choice(phrasal_verbs_to_pick)
        context.user_data['target_phrasal_verb'] = json.dumps(
            target_phrasal_verb)

        await update.message.reply_text(f'✅ Правильно!\n\n'
                                        f'Наступне значення: <b>{target_phrasal_verb["translation"]}</b>\n\n'
                                        f'<b>{target_phrasal_verb["practice"]}</b>',
                                        parse_mode='HTML',
                                        reply_markup=reply_markup)
    else:
        await update.message.reply_text(f'❌ Неправильно, спробуй ще раз',
                                        parse_mode='HTML',
                                        reply_markup=reply_markup)

    return PHRASAL_VERBS


async def phrasal_verbs_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    action = query.data
    old_phrasal_verb = json.loads(context.user_data['target_phrasal_verb'])

    if action == 'dont_know':
        category = context.user_data['phrasal_verbs_category']

        if category == 'any':
            phrasal_verbs_to_pick = phrasal_verbs
        else:
            phrasal_verbs_to_pick = list(filter(
                lambda v: v['category'] == category and v['verb'] != old_phrasal_verb['verb'], phrasal_verbs))

        target_phrasal_verb = random.choice(phrasal_verbs_to_pick)
        context.user_data['target_phrasal_verb'] = json.dumps(
            target_phrasal_verb)

        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton('Не знаю', callback_data='dont_know')],
            [InlineKeyboardButton('Закінчити', callback_data='to_main_menu')]
        ])

        await context.bot.send_message(chat_id=update.callback_query.message.chat_id,
                                       text=f'👌 Нічого страшного!\n\nПравильнв відповідь:\n\n'
                                       f'<b>{old_phrasal_verb["verb"]}</b> ({old_phrasal_verb["translation"]})\n\n'
                                       f'Наступне значення: <b>{target_phrasal_verb["translation"]}</b>\n\n'
                                       f'<b>{target_phrasal_verb["practice"]}</b>',
                                       parse_mode='HTML',
                                       reply_markup=reply_markup)

        return PHRASAL_VERBS
    elif action == 'to_main_menu':
        await context.bot.send_message(chat_id=update.callback_query.message.chat_id,
                                       text=f'<b>Головне меню</b>\n\n'
                                            f'Телеграм бот з вивчення англійських дієслів.\n\n'
                                            f'Обирай, що хочеш попрактикувати: ',
                                       parse_mode='HTML', reply_markup=InlineKeyboardMarkup(main_menu_keyboard))
        return TASK_PICK


async def unknown_message_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.callback_query.message.chat_id,
                                   text=f'🙆‍ Упс... Щось пішло не так \n\n'
                                   f'Давай почнемо спочатку.\n\nВведи команду /start , щоб розпочати навчання з ботом',
                                   parse_mode='HTML')


async def start_stative_dynamic_verbs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('start_stative_dynamic_verbs')
    query = update.callback_query
    await query.answer()
    action = query.data

    if action == 'start':

        target_stative_dynamic = random.choice(stative_dynamic_verbs)
        context.user_data['target_stative_dynamic_task'] = json.dumps(
            target_stative_dynamic)

        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton('Не знаю', callback_data='dont_know')],
            [InlineKeyboardButton('Закінчити', callback_data='to_main_menu')]
        ])

        await context.bot.send_message(chat_id=update.callback_query.message.chat_id,
                                       text=f'<b>Пояснення завдання: </b> \n\n'
                                            f'В одній ситуації (прикладі) дієслово буде вжито двічі: як stative '
                                            f'та як dynamic verb. \n'
                                            f'Твоє завдання: врахувати контекст речення, визначити яке дієслово '
                                            f'потрібно вжити stative або dynamic та запоовнити пропуски. Успіхів! \n\n\n'
                                            f'<b>Переклади речення:</b>\n'
                                            f'{target_stative_dynamic["translation"]}\n\n'
                                            f'<b>{target_stative_dynamic["task"]} </b>\n\n'
                                            f'<em>Напиши лише пропущенні значення через кому</em>',
                                       parse_mode='HTML', reply_markup=reply_markup)

        return STATIVE_DYNAMIC_VERBS
    elif action == 'explanation':
        await context.bot.send_message(chat_id=update.callback_query.message.chat_id,
                                       text=f'<b>Статичні (stative) і Динамічні (dynamic) дієслова</b>\n\n'
                                            f'Статичні та динамічні дієслова – це однакові дієслова, '
                                            f'але залежно від контексту  їх значення та форми змінюються. \n\n'
                                            f'Динамічні (активні) – дієслова, які виражають активну дію, '
                                            f'яка може тривати певний проміжок часу та за цією дією можна '
                                            f'спостерігати або ж візуалізувати її. \n\n'
                                            f'Статичні (пасивні)  – дієслова, які вказують на певний стан, '
                                            f'ментальні процеси або неактивні дії, за якими ми не можемо '
                                            f'спостерігати наочно. \n\n'
                                            f'Статичні дієслова зазвичай <b>не</b> використовуються в категоріях часів '
                                            f'Continuous. Здебільшого вони використовуються у <b>Simple</b> '
                                            f'та <b>Perfect Tenses</b>.\n\n'
                                            f'Динамічні дієслова можуть вживатися у всіх категоріях часів: '
                                            f'<b>Simple, Continuous, Perfect, Perfect Continuous</b> \n\n'
                                            f'Проте, існують виключення. Важливо навчитися розрізняти контекст, '
                                            f'у якому вживається дієслово. Від цього контексту і буде залежати форма '
                                            f'та значення певного дієслова. \n\n'
                                            f'Наприклад: \n\n'
                                            f'<em>I <b>think</b> that it is a good idea.</em> – я думаю, в загальному '
                                            f'значенні цього слова. \n '
                                            f'<em>I <b>am thinking</b> about you.</em> – «я думаю» прямо зараз, '
                                            f'ця дія зараз у прогресі. Хоча за правилом, дієслово <b>think</b> '
                                            f'є статичним дієсловом, оскільки ми не бачимо, не можемо спостерігати як '
                                            f'людина думає. У цьому ж випадку, дієслово <b>think</b> означає '
                                            f'динамічну дію. \n\n'
                                            f'<em>I <b>am tasting</b> this cake. </em> – Я смакую, куштую цей пиріг '
                                            f'прямо зараз. Динамічна дія, дія в прогресі – ми можемо спостерігати '
                                            f'як хтось куштує пиріг.\n'
                                            f'<em>This cake <b>tastes</b> well.</em> – Цей пиріг смакує добре, '
                                            f'він смачний на смак. Статична дія, яка не може тривати, не може бути '
                                            f'візуалізованою. \n\n'
                                            f'Для того, щоб ти навчився розрізняти контекст та вживати відповідну '
                                            f'форму дієслова, я підготував для тебе вправи. Натисни "почати вправи", щоб розпочати вправи на '
                                            f'<b>stative</b> та <b>dynamic verbs.</b> Успіхів 😉',
                                       parse_mode='HTML', reply_markup=InlineKeyboardMarkup(
                                           [
                                               [InlineKeyboardButton(
                                                   'Почати вправи', callback_data='start')],
                                               [InlineKeyboardButton(
                                                   'Головне меню', callback_data='back')]
                                           ]
                                       ))
        return START_STATIVE_DYNAMIC_VERBS
    elif action == 'back':
        await context.bot.send_message(chat_id=update.callback_query.message.chat_id,
                                       text=f'<b>Головне меню</b>\n\n'
                                            f'Телеграм бот з вивчення англійських дієслів.\n\n'
                                            f'Обирай, що хочеш попрактикувати: ',
                                       parse_mode='HTML', reply_markup=InlineKeyboardMarkup(main_menu_keyboard))
        return TASK_PICK


async def stative_dynamic_verbs_practice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('stative_dynamic_verbs_practice')
    text: str = update.message.text.lower().strip().replace(", ", ",")
    target = json.loads(context.user_data['target_stative_dynamic_task'])

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('Не знаю', callback_data='dont_know')],
        [InlineKeyboardButton('Закінчити', callback_data='to_main_menu')]
    ])

    if text == target["user_answer"]:

        stative_dynamic_to_pick = list(
            filter(lambda v: v['task'] != target['task'], stative_dynamic_verbs))
        target_stative_dynamic = random.choice(stative_dynamic_to_pick)
        context.user_data['target_stative_dynamic_task'] = json.dumps(
            target_stative_dynamic)

        await update.message.reply_text(f'✅ Правильно!\n\n'
                                        f'{target["full_answer"]}\n\n'
                                        f'<b>Наступне речення:</b>\n'
                                        f'{target_stative_dynamic["translation"]}\n\n'
                                        f'<b>{target_stative_dynamic["task"]} </b>\n\n',
                                        parse_mode='HTML',
                                        reply_markup=reply_markup)
    else:
        await update.message.reply_text(f'❌ Неправильно, спробуй ще раз',
                                        parse_mode='HTML',
                                        reply_markup=reply_markup)

    return STATIVE_DYNAMIC_VERBS


async def stative_dynamic_verbs_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    action = query.data

    if action == 'dont_know':
        old_target = json.loads(
            context.user_data['target_stative_dynamic_task'])
        stative_dynamic_to_pick = list(
            filter(lambda v: v['task'] != old_target['task'], stative_dynamic_verbs))
        target_stative_dynamic = random.choice(stative_dynamic_to_pick)
        context.user_data['target_stative_dynamic_task'] = json.dumps(
            target_stative_dynamic)

        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton('Не знаю', callback_data='dont_know')],
            [InlineKeyboardButton('Закінчити', callback_data='to_main_menu')]
        ])

        await context.bot.send_message(chat_id=update.callback_query.message.chat_id,
                                       text=f'👌 Нічого страшного!\n\n'
                                       f'Правильна відповідь: <em>{old_target["user_answer"]}</em>\n\n'
                                       f'<b>{old_target["full_answer"]}</b>\n\n'
                                       f'<em>{old_target["explanation"]}</em>\n\n\n'
                                       f'<b>Наступне речення:</b>\n'
                                       f'{target_stative_dynamic["translation"]}\n\n'
                                       f'<b>{target_stative_dynamic["task"]} </b>\n\n',
                                       parse_mode='HTML',
                                       reply_markup=reply_markup)

        return STATIVE_DYNAMIC_VERBS
    elif action == 'to_main_menu':
        await context.bot.send_message(chat_id=update.callback_query.message.chat_id,
                                       text=f'<b>Головне меню</b>\n\n'
                                            f'Телеграм бот з вивчення англійських дієслів.\n\n'
                                            f'Обирай, що хочеш попрактикувати: ',
                                       parse_mode='HTML', reply_markup=InlineKeyboardMarkup(main_menu_keyboard))
        return TASK_PICK


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


if __name__ == '__main__':
    print('Starting Bot')
    app = Application.builder().token(TOKEN).build()

    app.add_handler(ConversationHandler(
        entry_points=[CommandHandler('start', start_command)],
        states={
            TASK_PICK: [CallbackQueryHandler(task_picker)],
            START_IRREGULAR_VERBS: [CallbackQueryHandler(start_irregular_verbs)],
            IRREGULAR_VERBS: [MessageHandler(filters.TEXT & ~filters.COMMAND, irregular_verbs_command)],
            START_IRREGULAR_VERBS_PRACTICE: [CallbackQueryHandler(start_irregular_verbs_practice)],
            IRREGULAR_VERBS_PRACTICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, irregular_verbs_practice),
                                       CallbackQueryHandler(irregular_verbs_practice_callback)],
            START_TRANSLATE_UA_EN: [CallbackQueryHandler(start_verbs_translate_command)],
            TRANSLATE_UA_EN: [MessageHandler(filters.TEXT & ~filters.COMMAND, verb_translate),
                              CallbackQueryHandler(verb_translate_callback)],

            START_PHRASAL_VERBS: [CallbackQueryHandler(start_phrasal_verbs)],
            PHRASAL_VERBS_CATEGORY: [CallbackQueryHandler(phrasal_verbs_category)],
            PHRASAL_VERBS: [MessageHandler(filters.TEXT & ~filters.COMMAND, phrasal_verb),
                            CallbackQueryHandler(phrasal_verbs_callback)],

            START_STATIVE_DYNAMIC_VERBS: [CallbackQueryHandler(start_stative_dynamic_verbs)],
            STATIVE_DYNAMIC_VERBS: [MessageHandler(filters.TEXT & ~filters.COMMAND, stative_dynamic_verbs_practice),
                                    CallbackQueryHandler(stative_dynamic_verbs_callback)],
        },
        fallbacks=[CallbackQueryHandler(to_main_menu)]
    ))

    app.add_handler(CallbackQueryHandler(unknown_message_callback_handler))

    app.add_error_handler(error)

    print('Polling...')
    app.run_polling(poll_interval=1)
