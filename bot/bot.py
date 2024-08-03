import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from config import BOT_TOKEN
from sqlalchemy.orm import Session
from db.db import get_db
from db.models import User

bot = telebot.TeleBot(BOT_TOKEN)
db: Session = next(get_db())

user_states = {}
user_habits = {}


def create_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row(KeyboardButton("New Habit"), KeyboardButton("List Habit"))
    return markup


@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        user = User(
            user_id=user_id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        bot.reply_to(
            message, "Hello, How can I help you my friend?",
            reply_markup=create_menu()
        )
    else:
        bot.reply_to(
            message,
            f"Hello {message.from_user.first_name}, Happy to see you again. How can I help you today?",
            reply_markup=create_menu()
        )
    user_states[user_id] = "start"


new_habit_condition = lambda message: message.text == "New Habit" and user_states[message.from_user.id] == "start"


@bot.message_handler(func=new_habit_condition, chat_types=['private'])
def new_habit(message):
    user_id = message.from_user.id
    bot.reply_to(message, "Alright, Please Enter your habit name now:")
    user_states[user_id] = "new_habit"


@bot.message_handler(func=lambda message: user_states[message.from_user.id] == "new_habit", chat_types=['private'])
def add_new_habit(message):
    user_id = message.from_user.id
    if user_habits.get(user_id) is None:
        user_habits[user_id] = []
    user_habits[user_id].append(message.text)
    user_states[user_id] = 'start'
    bot.send_message(message.from_user.id, "New Habit added successfully", reply_markup=create_menu())


list_habit_condition = lambda message: user_states[message.from_user.id] == 'start' and message.text == "List Habit"


@bot.message_handler(func=list_habit_condition, chat_types=['private'])
def list_habit(message):
    user_id = message.from_user.id
    output = ""
    for i, habit in enumerate(user_habits.get(user_id, []), start=1):
        output += f"{i}. {habit}"
    if output == "":
        bot.send_message(user_id, "No Item founded", reply_markup=create_menu())
    else:
        bot.send_message(user_id, output, reply_markup=create_menu())
    user_states[user_id] = 'start'


bot.infinity_polling()
