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


def get_habit(user_id: int) -> None | UserHabit:
    """
        Return User habit by habit ID stored in user.state
    """

    user: User = get_user(user_id)
    state = user.state.split("-")
    try:
        habit_id = int(state[1])
        return db.query(UserHabit).filter(UserHabit.user == user, UserHabit.id == habit_id).first()
    except (IndexError, ValueError):
        ...
    return None


def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    markup.row(KeyboardButton("New Habit"), KeyboardButton("List Habit"))
    markup.row(KeyboardButton("Select Habit"))
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
            reply_markup=main_menu()
        )
    else:
        user = set_user_state(user, "start")
        bot.reply_to(
            message,
            f"Hello {message.from_user.first_name}, Happy to see you again. How can I help you today?",
            reply_markup=main_menu()
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
    bot.send_message(message.from_user.id, "New Habit added successfully", reply_markup=main_menu())


list_habit_condition = lambda message: get_user_state(message) == 'start' and message.text == "List Habit"


@bot.message_handler(func=list_habit_condition, chat_types=['private'])
def list_habit(message):
    user_id = message.from_user.id
    user = get_user(user_id)
    output = ""
    for i, habit in enumerate(user.habits, start=1):
        output += f"{i}. {habit.name}"
    if output == "":
        bot.send_message(user_id, "No Item founded", reply_markup=main_menu())
    else:
        bot.send_message(user_id, output, reply_markup=main_menu())
    user = set_user_state(user, 'start')


def manage_habit_condition(message):
    return get_user_state(message) == "start" and message.text == "Select Habit"


@bot.message_handler(func=manage_habit_condition, chat_types=['private'])
def manage_habit(message):
    user = get_user(message.from_user.id)
    keyboard = InlineKeyboardMarkup(row_width=1)
    if user.habits:
        for habit in user.habits:
            keyboard.add(InlineKeyboardButton(f"{habit.name}", callback_data=f"{habit.id}"))
        bot.send_message(message.chat.id, "Alright, Please select your habit now:", reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "No Item founded", reply_markup=main_menu())


def get_user_habit(callback):
    try:
        habit_id = int(callback.data)
        habit = db.query(UserHabit).filter(UserHabit.id == habit_id).first()
    except ValueError:
        habit = None
        ...
    return habit if habit else False


def select_habit_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    keyboard.row(KeyboardButton("Edit Name"), KeyboardButton("Delete Habit"))
    keyboard.row(KeyboardButton("Main Menu"))
    return keyboard


@bot.callback_query_handler(func=get_user_habit)
def select_user_habit(callback):
    habit = get_user_habit(callback)
    bot.delete_message(callback.message.chat.id, callback.json['message']['message_id'])
    keyboard = select_habit_keyboard()
    bot.send_message(
        callback.from_user.id, f"Ok, {habit} selected!\n What do you want to do now?", reply_markup=keyboard
    )
    user = get_user(callback.from_user.id)
    set_user_state(user, f"habit-{habit.id}")


def edit_habit_name_condition(message):
    user_state = get_user_state(message).split("-")
    user = get_user(message.from_user.id)
    if user_state[0] == "habit" and len(user_state) == 2 and message.text == "Edit Name":
        habit_id = int(user_state[-1])
        habit = db.query(UserHabit).filter(UserHabit.id == habit_id, UserHabit.user == user).first()
        if habit:
            return habit
    return False


@bot.message_handler(func=edit_habit_name_condition, chat_types=['private'])
def get_new_habit_name(message):
    user_id = message.from_user.id
    user = get_user(user_id)
    bot.send_message(user_id, "Ok now Enter new habit name:")
    set_user_state(user, f"habit-edit_name-{user.state[-1]}")


def set_new_habit_name_condition(message):
    user_state = get_user_state(message).split("-")
    user = get_user(message.from_user.id)
    if "-".join(x for x in user_state[:2]) == "habit-edit_name":
        habit_id = int(user_state[-1])
        habit = db.query(UserHabit).filter(UserHabit.id == habit_id, UserHabit.user == user).first()
        if habit:
            return habit
    return False


@bot.message_handler(func=set_new_habit_name_condition, chat_types=['private'])
def set_new_habit_name(message):
    habit = set_new_habit_name_condition(message)
    habit.name = message.text
    db.add(habit)
    db.commit()
    db.refresh(habit)
    bot.send_message(message.from_user.id, "Habit Name Changed!", reply_markup=select_habit_keyboard())
    set_user_state(habit.user, f"habit-{habit.id}")


def delete_habit_condition(message):
    user_state = get_user_state(message).split("-")
    user = get_user(message.from_user.id)
    if user_state[0] == "habit" and message.text == "Delete Habit":
        habit_id = int(user_state[-1])
        habit = db.query(UserHabit).filter(UserHabit.id == habit_id, UserHabit.user == user).first()
        if habit:
            return habit
    return False


@bot.message_handler(func=delete_habit_condition, chat_types=['private'])
def delete_habit(message):
    user_id = message.from_user.id
    habit = get_habit(user_id)
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.row(InlineKeyboardButton("Yes", callback_data=f"delete_habit-{habit.id}"))
    keyboard.row(InlineKeyboardButton("No", callback_data=f"cancel_delete_habit"))
    bot.send_message(user_id, "Are You sure you want to delete your habit?", reply_markup=keyboard)


def delete_user_habit_condition(callback):
    data = callback.data.split("-")
    if data[0] == "delete_habit":
        try:
            habit_id = int(data[-1])
            habit = get_habit(callback.from_user.id)
            return habit.id == habit_id
        except ValueError:
            ...
    return False


@bot.callback_query_handler(func=delete_user_habit_condition)
def delete_user_habit(callback):
    user_id = callback.from_user.id
    habit = get_habit(user_id)
    db.delete(habit)
    db.commit()
    bot.delete_message(callback.message.chat.id, callback.json['message']['message_id'])
    bot.send_message(user_id, "Habit Deleted Successfully!", reply_markup=main_menu())
    user = get_user(user_id)
    user = set_user_state(user, "start")


def cancel_delete_suer_habit_condition(callback):
    if callback.data == "cancel_delete_habit":
        return True
    return False


@bot.callback_query_handler(func=cancel_delete_suer_habit_condition)
def cancel_delete_suer_habit(callback):
    bot.delete_message(callback.message.chat.id, callback.json["message"]['message_id'])
    bot.send_message(callback.from_user.id, "Delete Habit canceled!", reply_markup=select_habit_keyboard())


bot.infinity_polling()
