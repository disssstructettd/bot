import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from pytube import YouTube

# Замените YOUR_BOT_TOKEN на ваш токен, который вы получили от @BotFather
BOT_TOKEN = '6389921681:AAEhXbj7fAa9ynrNNQWT2f8auMDTkSV1Esk'

# Функция для скачивания видео с YouTube
def download_youtube_video(update, context):
    message = update.message
    video_url = message.text

    try:
        # Проверяем, что это действительно URL YouTube
        if 'youtube.com' not in video_url:
            raise ValueError("Неправильный URL YouTube.")

            # Создаем объект YouTube и получаем видео с наивысшим разрешением
        yt = YouTube(video_url)
        video = yt.streams.get_highest_resolution()

        # Скачиваем видео
        video_path = f'{yt.video_id}.mp4'
        video.download(output_path=video_path)

        # Отправляем видео пользователю
        message.reply_video(open(video_path, 'rb'))

    except Exception as e:
        message.reply_text(f"Ошибка при скачивании видео: {e}")

        # Функция для обработки команды /start
def start(update, context):
    message = update.message
    message.reply_text("Привет! Отправьте мне ссылку на видео с YouTube, и я скачаю его для вас.")

def main():
    # Включаем логирование, чтобы видеть ошибки и информацию о работе бота
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Обработчики команд и сообщений
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, download_youtube_video))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()