import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from config import BOT_TOKEN


bot = telebot.TeleBot(BOT_TOKEN)

user_states = {}
user_habits = {}

def create_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    markup.row(KeyboardButton("New Habit"), KeyboardButton("List Habits"))
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    user_states[user_id] = "main"
    bot.reply_to(message, "Hi I'm your habit tracker assistant. How can I help you?", reply_markup=create_menu())
    

@bot.message_handler(func=lambda message: True)
def handle_menu(message):
    user_id = message.from_user.id
    if user_states[user_id] == "main":
        main_menu(message)
    elif user_states[user_id] == "new_habit":
        add_new_habit(message)
    elif user_states[user_id] == "list_habits" or message.text == "List Habits":
        list_habits(message)
    elif user_states[user_id] == "edit_habit":
        text = message.text.strip()
        try:
            text = int(text)
            edit_habit(message, text-1)
        except ValueError:
            if text != "Main Menu":
                bot.reply_to(message, "I don't underestand!")
            user_states[user_id] = "main"
            main_menu(message)
    
def main_menu(message):
    user_id = message.from_user.id
    if message.text == "New Habit":
        user_states[user_id] = "new_habit"
        bot.reply_to(message, "Please enter the name of the habit you want to add.")
    elif message.text == "List Habits":
        user_states[user_id] = "list_habits"
        list_habits(message)
    elif message.text == "Track Habit":
        bot.reply_to(message, "Which habit would you like to track today?")
    elif message.text == "View Progress":
        bot.reply_to(message, "Here's your progress: [Your progress tracking logic here]")
    else:
        bot.reply_to(message, "I don't understand that command. Please use the menu options.")

def add_new_habit(message):
    user_id = message.from_user.id
    if user_id not in user_habits:
        user_habits[user_id] = []
    habit_name = message.text.strip()
    user_habits[user_id].append(habit_name)
    user_states[user_id] = "main"
    bot.reply_to(message, f"Habit '{habit_name}' has been added successfully!", reply_markup=create_menu())

def list_habits(message):
    user_id = message.from_user.id
    habits = user_habits.get(user_id, None)
    if habits:
        habits = "\n".join(f"{i}. {habit}" for i, habit in enumerate(habits, start=1))
        bot.reply_to(message, habits)
        markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        user_states[user_id] = "edit_habit"
        markup.row(KeyboardButton("Main Menu"))
        bot.reply_to(message, "If you want to edit habit, please enter the number of habit", reply_markup=markup)
    else:
        bot.reply_to(message, "You have no habit yet!")

def edit_habit(message, habit_id):
    user_id = message.from_user.id
    habits = user_habits.get(user_id, None)
    if not habits:
        user_states[user_id] = "main"
        return bot.reply_to("You dont have any habit")
    try:
        habit = habits[habit_id]
    except IndexError:
        user_states[user_id] = "main"
        return bot.reply_to("habit not found")
    markup = ReplyKeyboardMarkup(True, False)
    
    user_states[user_id] = "edit_habit"
    markup.row(KeyboardButton("Name"), KeyboardButton("Main Menu"))
    bot.reply_to(message, "Not select the section that you want to edit:", reply_markup=markup)
    
    
bot.infinity_polling()