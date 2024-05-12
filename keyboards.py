from telegram import InlineKeyboardButton

main_menu_keyboard = [
            [InlineKeyboardButton('Неправильні дієслова', callback_data='irregular_verbs')],
            [InlineKeyboardButton('Практика неправильних дієслів', callback_data='practice_irregular_verbs')],
            [InlineKeyboardButton('Переклад (UA → EN)', callback_data='translate_verbs_ua_en')],
            [InlineKeyboardButton('Фразові дієслова', callback_data='practice_phrasal_verbs')],
            [InlineKeyboardButton('Статичні і динамічні дієслова', callback_data='practice_stative_dynamic')]
]

to_menu_keyboard = [
            [InlineKeyboardButton('Головне меню', callback_data='to_main_menu')]
]