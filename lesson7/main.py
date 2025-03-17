import ptbot
from dotenv import load_dotenv
import os
from pytimeparse import parse


def wait(chat_id, time, bot):
    secs_time = parse(time)
    message_id = bot.send_message(chat_id, "Запускаю таймер...")
    bot.create_countdown(secs_time, notify_progress,
                         chat_id=chat_id, message_id=message_id,
                         time=secs_time, bot=bot)
    bot.create_timer(secs_time, answer, chat_id=chat_id, bot=bot)


def render_progressbar(total, iteration, prefix='', suffix='',
                       length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def notify_progress(secs_left, chat_id, message_id, time, bot):
    timer_message = (
        f"Осталось секунд: {secs_left}\n"
        f"{render_progressbar(time, time - secs_left)}"
    )
    bot.update_message(chat_id, message_id, timer_message)


def answer(chat_id, bot):
    message = "Время вышло!"
    bot.send_message(chat_id, message)


def main():
    load_dotenv()
    tg_token = os.environ['tg_token']
    
    bot = ptbot.Bot(tg_token)
    bot.reply_on_message(wait, bot=bot)
    bot.run_bot()


if __name__ == '__main__':
    main()
