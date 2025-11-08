from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import json
import os

# --- Главное меню ---
main_menu = [
    ["Клиентам", "Полезные материалы", "Клуб"],
    ["Обо мне ℹ️"]
]

# --- Меню для клиентов ---
clients_menu = [
    ["Записаться на консультацию", "Узнать цены"],
    ["Назад в меню"]
]
# --- Меню "Записаться на консультацию" ---
consult_menu = [
    ["Назад", "Главное меню"]
]
# --- Меню "Узнать цены" ---
prices_menu = [
    ["Назад", "Главное меню"]
]
# --- Меню "Полезные материалы" ---
materials_menu = [
    ["Статьи", "Видео"],
    ["Назад"]
]

# Функция для сохранения chat_id
def save_user(chat_id):
    file = "users.json"
    users = []

    # Если файл уже есть — читаем старые ID
    if os.path.exists(file):
        with open(file, "r", encoding="utf-8") as f:
            users = json.load(f)
    # Если chat_id новый — добавляем
    if chat_id not in users:
        users.append(chat_id)
        with open(file, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=2)
USERS_FILE = "users.json"
# Функция которая чистить базу данных пользователей
def reset_users():
    """Полностью очищает список пользователей."""
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)
#Функция проверки зарегистрирован пользователь или нет
def is_user_registered(chat_id):
    """Проверяет, есть ли пользователь в списке."""
    if not os.path.exists(USERS_FILE):
        return False
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        users = json.load(f)
    return chat_id in users

# --- Команда /start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    save_user(chat_id)
    reply_markup = ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
    await update.message.reply_text(
        "Привет! 👋\nЯ бот, выбери нужный раздел:",
        reply_markup=reply_markup
    )
# --- Команда /sendall ---

ADMIN_ID = 601752044  # ← сюда вставь свой chat_id

async def sendall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    if chat_id != ADMIN_ID:
        await update.message.reply_text("⛔ У тебя нет прав использовать эту команду.")
        return

    if not context.args:
        await update.message.reply_text("❗ Используй формат: /sendall <текст>")
        return

    message = " ".join(context.args)

    with open("users.json", "r", encoding="utf-8") as f:
        users = json.load(f)

    count = 0
    for user_id in users:
        try:
            await context.bot.send_message(chat_id=user_id, text=message)
            count += 1
        except Exception as e:
            print(f"Ошибка при отправке {user_id}: {e}")

    await update.message.reply_text(f"✅ Сообщение отправлено {count} пользователям.")
# Команда для использования функции очистки пользователей(доступно только админу)
async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id != ADMIN_ID:
        await update.message.reply_text("⛔ У тебя нет прав использовать эту команду.")
        return

    reset_users()
    await update.message.reply_text("✅ Все пользователи сброшены. Им нужно снова написать /start.")
# --- Обработка нажатий на кнопки ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    chat_id = update.effective_chat.id
    if not is_user_registered(chat_id):
        await update.message.reply_text("❗ Сначала напиши /start, чтобы начать заново.")
        return
    # Главное меню
    if text == "Клиентам":
        reply_markup = ReplyKeyboardMarkup(clients_menu, resize_keyboard=True)
        await update.message.reply_text("Выберите действие 👇", reply_markup=reply_markup)

    elif text == "Назад в меню":
        reply_markup = ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
        await update.message.reply_text("Главное меню 👇", reply_markup=reply_markup)


    elif text == "Записаться на консультацию":

        reply_markup = ReplyKeyboardMarkup(consult_menu, resize_keyboard=True)

        await update.message.reply_text(

            "Чтобы записаться свяжитесь по контактам \nНомер телефона: 88888888 \nТелеграмм: @ффф\n Электронная почта: skksks@mail.ru",

            reply_markup=reply_markup

        )


    elif text == "Назад":

        reply_markup = ReplyKeyboardMarkup(clients_menu, resize_keyboard=True)

        await update.message.reply_text("Меню для клиентов 👇", reply_markup=reply_markup)


    elif text == "Главное меню":

        reply_markup = ReplyKeyboardMarkup(main_menu, resize_keyboard=True)

        await update.message.reply_text("Главное меню 👇", reply_markup=reply_markup)



    elif text == "Узнать цены":

        reply_markup = ReplyKeyboardMarkup(prices_menu, resize_keyboard=True)

        await update.message.reply_text(

            "Вот прайс-лист 💰\n\n- \n-  \n- ",

            reply_markup=reply_markup

        )



    elif text == "Полезные материалы":

        reply_markup = ReplyKeyboardMarkup(materials_menu, resize_keyboard=True)

        await update.message.reply_text(

            "Вот полезные материалы 📚\nВыбери, что тебя интересует:",

            reply_markup=reply_markup

        )
    elif text == "Статьи":
        await update.message.reply_text("📰 Вот список статей: скоро добавим ссылки!")

    elif text == "Видео":
        await update.message.reply_text("🎥 Вот видео:")
        with open("video/@why4ch (2).mp4", "rb") as video:
            await update.message.reply_video(video)
            # Кнопки после видео
            keyboard = [["Назад", "Главное меню"]]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text("Выбери действие 👇", reply_markup=reply_markup)



    elif text == "Клуб":
        await update.message.reply_text("🎯 Клуб в разработке, следи за обновлениями!")

    elif text == "Обо мне ℹ️":
        await update.message.reply_text("Вот немного обо мне 😊")
        with open("photo/photo_2025-11-08_10-59-00.jpg", "rb") as photo:
            await update.message.reply_photo(photo, caption="Я такой то такой то")
            # Добавляем кнопки для возврата
            keyboard = [["Назад", "Главное меню"]]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text("Что хочешь сделать дальше?", reply_markup=reply_markup)

    else:
        await update.message.reply_text("Не понял 😅 Выбери кнопку из меню.")

# --- Основная функция ---
def main():
    app = ApplicationBuilder().token("8314097287:AAH6tXiyHYHjktN6C8nJN2xKpcboEW84twA").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("sendall", sendall))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Бот запущен. Нажми Ctrl+C, чтобы остановить.")
    app.run_polling()

# --- Запуск ---
if __name__ == "__main__":
    main()
