import telebot, db, creds
from telebot import types

token = creds.token
bot = telebot.TeleBot(token)

expenses_list = []
categories = db.selecting_categories()
def is_number(str):
    try:
        float(str)
        return True
    except ValueError:
        return False


def user_list_without_category(expenses_list):
    list = []
    for i in range(0, len(expenses_list)):
        list.append(expenses_list[i][0])
    return list

def usual_keyboard():
    markup=types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton(text="Баланс", callback_data="Баланс")
    item2 = types.InlineKeyboardButton(text="Список расходов", callback_data="Список расходов")
    item3 = types.InlineKeyboardButton(text="Очистить список", callback_data="Очистить список")
    markup.row(item1, item2)
    markup.row(item3)
    return markup
   
            
@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.from_user.id
    username = message.from_user.username
    db.save_new_user(user_id, username)
    markup = usual_keyboard()
    bot.send_message(message.chat.id,'Добро пожаловать в бот учета расходов', reply_markup=markup)



@bot.message_handler(content_types=['text'])
def message_reply(message):
    global expenses_list
    if is_number(message.text):
        select_category(message)
    else:
        bot.send_message(message.chat.id,"Попробуй еще раз, пёс")

def select_category(message):
    keyboard = types.InlineKeyboardMarkup() #наша клавиатура
    value = abs(float(message.text))
    for category in categories:
        key = types.InlineKeyboardButton(text=category, callback_data=str(value) + " " + category)
        keyboard.add(key) #добавляем кнопку в клавиатуру
    question = 'Какую категорию ты выберешь?'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
    
    
@bot.callback_query_handler(func=lambda call: True)
def adding_expense(call):
    global expenses_list
    user_id = call.from_user.id
    username = call.message.from_user.username
    db.save_new_user(user_id, username)
    markup = usual_keyboard()
    summa = db.balance(user_id) #Получение баланса из БД
    if call.data == "Баланс":
        if summa == 0:
            bot.send_message(call.message.chat.id,"Вы пока ничего не занесли", reply_markup=markup)
        elif summa > 0:
            bot.send_message(call.message.chat.id, f"Ваши расходы: {summa}", reply_markup=markup)
    elif call.data == "Список расходов":
        if summa == 0:
            bot.send_message(call.message.chat.id,"Вы пока ничего не занесли", reply_markup=markup)
        elif summa > 0:
            for expense in db.user_expenses_list(user_id):
                bot.send_message(call.message.chat.id, f"{expense[0]} в категории {expense[1]}" )
            bot.send_message(call.message.chat.id, f"Ваши расходы: {summa}", reply_markup=markup)
    elif call.data == "Очистить список":
        db.clear_expenses(user_id)
        bot.send_message(call.message.chat.id,"Список очищен", reply_markup=markup)
    elif ' '.join(call.data.split()[1:]) in categories:
        data = call.data.split()
        text = abs(float(data[0]))
        category = ' '.join(data[1:])
        db.new_expese(text, category, user_id)
        bot.send_message(call.message.chat.id, f"Добавлен расход {text} рублей в категорию {category}", reply_markup=markup)

bot.infinity_polling()
