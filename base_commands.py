from config import botExcursions, user_state, user_text, get_cursor
from telebot import types

storage_tags = {
    'mountains': 'горы',
    'sea': 'морские прогулки',
    'bus_excursions': 'автобусные экскурсии'
}

class BotService:
    def __init__(self, bot):
        self.bot = bot

    def send_message(self, chat_id, text, reply_markup=None):
        self.bot.send_message(chat_id, text, reply_markup=reply_markup)

    def send_menu(self, chat_id, buttons, text="Выберите действие:"):
        markup = types.InlineKeyboardMarkup()
        for row in buttons:
            markup.add(*row) 
             
        self.send_message(chat_id, text, reply_markup=markup)
        
    def edit_message_text(self, chat_id, message_id, text, reply_markup=None):
        self.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=reply_markup)
            
bot_service = BotService(botExcursions)

@botExcursions.message_handler(commands=['start'])
def startBot(message):
    first_mess = (
        f"<b>{message.from_user.first_name}</b>, "
        f"привет!\nДанный бот способен рассказать о экскурсиях в городе Геленджик, "
        f"показать актуальные цены. "
        f"Желаете протестировать бота?"
    )
    
    buttons = [
        [types.InlineKeyboardButton(text='Да', callback_data='yes')],
        [types.InlineKeyboardButton(text='Нет', callback_data='no')]
    ]
    
    markup = types.InlineKeyboardMarkup()
    for row in buttons:
        markup.add(*row)
    
    botExcursions.send_message(
        message.chat.id, 
        first_mess, 
        parse_mode='html', 
        reply_markup=markup
    )
    
@botExcursions.message_handler(commands=['pay'])
def startBot(message):
    first_mess = (
        f"<b>{message.from_user.first_name}</b>, "
        f"хотите оплатить экскурсию?"
    )
    
    buttons = [
        [types.InlineKeyboardButton(text='Да', callback_data='yes')],
        [types.InlineKeyboardButton(text='Нет', callback_data='no')]
    ]
    
    markup = types.InlineKeyboardMarkup()
    for row in buttons:
        markup.add(*row)
    
    botExcursions.send_message(
        message.chat.id, 
        first_mess, 
        parse_mode='html', 
        reply_markup=markup
    )
    
def start_from_callback(bot_service, chat_id, message_id):
    text = (
        "Привет!\n"
        "Данный бот способен рассказать о экскурсиях в городе Геленджик.\n"
        "Желаете протестировать бота?"
    )

    buttons = [
        [types.InlineKeyboardButton(text='Да', callback_data='yes')],
        [types.InlineKeyboardButton(text='Нет', callback_data='no')]
    ]

    markup = types.InlineKeyboardMarkup()
    for row in buttons:
        markup.add(*row)

    bot_service.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text,
        reply_markup=markup
    )

def handle_yes(bot_service, chat_id, message_id):
    buttons = [
        [types.InlineKeyboardButton(text='Узнать цены на экскурсии', callback_data='price')],
        [types.InlineKeyboardButton(text='Прочитать информацию об экскурсиях', callback_data='info')],
        [types.InlineKeyboardButton(text='Проверить время начала эскурсий', callback_data='time')]
    ]
    markup = types.InlineKeyboardMarkup()
    for row in buttons:
        markup.add(*row)
        
    bot_service.edit_message_text(chat_id, message_id, "Отлично, давайте изучать меню", reply_markup=markup)
   
def handle_no (bot_service, chat_id, message_id):
    
   buttons = [
        [types.InlineKeyboardButton(text='Вернуться в начало', callback_data='begin_text')]
    ]
   
   markup = types.InlineKeyboardMarkup()
   for row in buttons:
        markup.add(*row)
    
   bot_service.edit_message_text(
        chat_id, 
        message_id,
        "Ничего страшного, можете вернуться когда захотите",
        reply_markup=markup
    )
  
def handle_info (bot_service, chat_id, message_id): 
    conn, cursor = get_cursor()
    cursor.execute('SELECT * FROM public."Excursions" WHERE id=1')
    row = cursor.fetchone()
    if row is None:
        bot_service.send_message(chat_id, "Запись не найдена!")
        return
    text = f"Название: {row[1]}\nОписание: {row[2]}\nЦена: {row[3]}"
    
    bot_service.edit_message_text(
        chat_id, 
        message_id,
        text
    )

    cursor.close()
    conn.close()
  
def handle_time (bot_service, chat_id): 
    user_state[chat_id] = "wait_answer_number"
    
    buttons = [
        [types.InlineKeyboardButton(text='Вернуться в меню', callback_data='menu')]
    ]
    
    answer_text = user_text.get(chat_id, "Пока нет сохранённых заметок")
    bot_service.send_menu(
        chat_id, 
        buttons,
        f"{answer_text}"
    )
  
def handle_price (bot_service, chat_id, message_id): 
    
    buttons = [
        [types.InlineKeyboardButton(text='Горы', callback_data='mountains')],
        [types.InlineKeyboardButton(text='Море', callback_data='sea')],
        [types.InlineKeyboardButton(text='Автобусные экскурсии', callback_data='bus_excursions')]
    ]
   
    markup = types.InlineKeyboardMarkup()
    for row in buttons:
        markup.add(*row)
    
    bot_service.edit_message_text(
        chat_id, 
        message_id,
        "Выберите вид экскурсии",
        reply_markup=markup
    )
   
    """conn, cursor = get_cursor()
    cursor.execute('SELECT * FROM public."Excursions" WHERE id=1')
    row = cursor.fetchone()
    if row is None:
        bot_service.send_message(chat_id, "Запись не найдена!")
        return
    text = f"Цена за экскурсию: {row[2]}"
    
    bot_service.edit_message_text(
        chat_id, 
        message_id,
        text
    )

    cursor.close()
    conn.close()"""
    
def handle_tags (bot_service, chat_id, message_id): 
    state = user_state.get(chat_id)
    tag = storage_tags.get(state)
    
    if not tag:
        bot_service.send_message(chat_id, "Неизвестная категория")
        return

    conn, cursor = get_cursor()
    cursor.execute(
        'SELECT * FROM public."Excursions" WHERE tag = %s',
        (tag,)
    )

    rows = cursor.fetchall()

    if not rows:
        bot_service.send_message(chat_id, "Запись не найдена!")
        cursor.close()
        conn.close()
        return

    row = rows[0]
    text = f"Цена за экскурсию: {row[2]}"

    bot_service.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=text
    )

    cursor.close()
    conn.close()

    
handles = {
    "yes": handle_yes,
    "no": handle_no,
    "info": handle_info,
    "time": handle_time,
    "price": handle_price,
    "menu": handle_yes,
    "begin_text": start_from_callback,
    "repeat": handle_price,
    "mountains": handle_tags,
    "sea": handle_tags,
    "bus_excursions": handle_tags,
}

@botExcursions.callback_query_handler(func=lambda call: True)
def callback(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    if call.data in handles:
        handles[call.data](bot_service, chat_id, message_id)
        
@botExcursions.callback_query_handler(func=lambda call: call.data in storage_tags)
def callback(call):
    user_state[call.message.chat.id] = call.data
    handle_tags(bot_service, call.message.chat.id, call.message.message_id)

@botExcursions.message_handler(
    func=lambda message: (
        user_state.get(message.chat.id) == "wait_writting_number"
    )
)

def write_number_chapter(message):
  chat_id = message.chat.id
  
  if user_state.get(chat_id) == "wait_writting_number":
      save_text = message.text
      user_text[chat_id] = save_text
      user_state[chat_id] = None
      
      botExcursions.send_message(
          chat_id, 
          "Отлично, я записал ваши заметки"
      )
  else:
      botExcursions.send_message(
          chat_id, 
          "Пожалуйста, введите текст."
      )

