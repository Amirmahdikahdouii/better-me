# Better Me

Better Me is a Telegram bot designed to help you track and manage your habits. With Better Me, you can easily create new
habits, add notes to your habits, and keep track of your progress. This bot leverages the power of Telegram for easy
accessibility and interaction, providing a seamless experience to help you become a better version of yourself.

## Features

- **Create New Habits**: Easily create new habits that you want to track.
- **List Habits**: View a list of all your habits.
- **Select Habit**: Select a specific habit to interact with.
- **Add Notes**: Add notes to your habits to keep detailed records of your progress.
- **View Notes**: View all notes associated with a specific habit.

## Usage

1. **Start the Bot**: Use the `/start` command to begin interacting with the bot. This will register you as a user and
   display the main menu.
2. **Main Menu**: From the main menu, you can choose to:
    - **New Habit**: Create a new habit.
    - **List Habits**: View all your habits.
    - **Select Habit**: Choose a specific habit to add notes or view details.

### Commands

- `/start`: Initialize the bot and register the user.

### Main Menu Options

- **New Habit**: Prompts you to enter the name of a new habit you wish to track.
- **List Habits**: Displays a list of all your habits.
- **Select Habit**: Allows you to select a specific habit to interact with.

### Habit Menu Options

Once a habit is selected, you can:

- **Add Note**: Add a new note to the selected habit.
- **View Notes**: View all notes associated with the selected habit.
- **Main Menu**: Return to the main menu.

## Installation

To run your own instance of the Better Me bot, follow these steps:

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/better-me.git
    cd better-me
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Set up your configuration:
    - Create a `.env` file in the root directory of the project.
    - Add your Telegram bot token to the `.env` file:
        ```env
        BOT_TOKEN=your-telegram-bot-token
        DB_NAME=DATABASE_NAME
        DB_USER=DATABASE_USER
        DB_PASSWORD=DATABASE_PASSWORD
        DB_HOST=DATABASE_HOST
        DB_PORT=DATABASE_PORT
        ```

4. Initialize the database:
    - Ensure your database is set up correctly and update the connection string in the configuration if necessary.
    - Run the database migrations (if any).

5. Start the bot:
    ```sh
    python main.py
    ```

## Contributing

Contributions are welcome! If you have any suggestions or improvements, feel free to open an issue or submit a pull
request.

## Contact

If you have any questions or feedback, feel free to contact us
at [amirmahdikahdooi@gmail.com](mailto:amirmahdikahdooi@gmail.com).

## Improving Your Efficiency with Better Me

Better Me is designed to help you keep track of your habits and improve your productivity. By consistently logging your
habits and adding detailed notes, you can:

- **Monitor Progress**: Keep a detailed record of your habit formation journey.
- **Identify Patterns**: Understand what works for you and what doesn't by reviewing your notes.
- **Stay Motivated**: Seeing your progress and the notes you've made can help you stay motivated and committed to your
  goals.
- **Accountability**: Having a record of your habits and notes helps you stay accountable to yourself.

Start using Better Me today to take control of your habits and become a better version of yourself!
