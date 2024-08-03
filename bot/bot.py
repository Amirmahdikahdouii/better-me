import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from config import BOT_TOKEN
from sqlalchemy.orm import Session
from db.db import get_db
from db.models import User, UserHabit

bot = telebot.TeleBot(BOT_TOKEN)
db: Session = next(get_db())

user_states = {}
user_habits = {}


def get_user(user_id: int):
    user = db.query(User).filter(User.user_id == user_id).first()
    return user if user else None


def set_user_state(user: User, state: str):
    user.state = state
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_state(message):
    user = get_user(message.from_user.id)
    return user.state if user else ""


def create_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, )
    markup.row(KeyboardButton("New Habit"), KeyboardButton("List Habit"))
    return markup


@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    user = get_user(user_id)
    if not user:
        user = User(
            user_id=user_id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            state="start"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        bot.reply_to(
            message, "Hello, How can I help you my friend?",
            reply_markup=create_menu()
        )
    else:
        user = set_user_state(user, "start")
        bot.reply_to(
            message,
            f"Hello {message.from_user.first_name}, Happy to see you again. How can I help you today?",
            reply_markup=create_menu()
        )


def new_habit_condition(message):
    user = get_user(message.from_user.id)
    if user:
        return message.text == "New Habit" and user.state == "start"
    return False


@bot.message_handler(func=new_habit_condition, chat_types=['private'])
def new_habit(message):
    user_id = message.from_user.id
    user = get_user(user_id)
    user = set_user_state(user, "new_habit")
    bot.reply_to(message, "Alright, Please Enter your habit name now:")


@bot.message_handler(func=lambda message: get_user_state(message) == "new_habit", chat_types=['private'])
def add_new_habit(message):
    user_id = message.from_user.id
    user = get_user(user_id)
    habit = UserHabit(user=user, name=message.text)
    db.add(habit)
    db.commit()
    db.refresh(habit)
    user = set_user_state(user, "start")
    bot.send_message(message.from_user.id, "New Habit added successfully", reply_markup=create_menu())


list_habit_condition = lambda message: get_user_state(message) == 'start' and message.text == "List Habit"


@bot.message_handler(func=list_habit_condition, chat_types=['private'])
def list_habit(message):
    user_id = message.from_user.id
    user = get_user(user_id)
    output = ""
    for i, habit in enumerate(user.habits, start=1):
        output += f"{i}. {habit.name}"
    if output == "":
        bot.send_message(user_id, "No Item founded", reply_markup=create_menu())
    else:
        bot.send_message(user_id, output, reply_markup=create_menu())
    user = set_user_state(user, 'start')


def manage_habit_condition(message):
    return get_user_state(message) == "start" and message.text == "Select Habit"


@bot.message_handler(func=manage_habit_condition, chat_types=['private'])
def manage_habit(message):
    user = get_user(message.from_user.id)
    keyboard = InlineKeyboardMarkup(row_width=1)
    for habit in user.habits:
        keyboard.add(InlineKeyboardButton(f"{habit.name}", callback_data=f"{habit.id}"))
    bot.send_message(message.chat.id, "Alright, Please select your habit now:", reply_markup=keyboard)


bot.infinity_polling()
