from telegram.ext import Updater, CommandHandler, Filters, MessageHandler
from stats_extractor import get_stats
from tele_ch_send import send_review
from tokens import *
import logging
import sched, time
import threading

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', filename='bot2.log',level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
schedule = sched.scheduler(time.time, time.sleep)

def screen_tweets(bot, msg_id, chat_id, url):
    logging.info("checking {}".format(url))
    stats = get_stats(url)
    retweets = int(stats[0])
    likes = int(stats[1])

    if retweets < 1 or likes < 2:
        logging.info("{} did not fulfil requirement: {}/{}".format(url, retweets, likes))
        try:
            send_review("{}/{} : \n{}".format(retweets, likes, url))
            response = bot.delete_message(chat_id=chat_id, message_id=msg_id)
        except Exception as e:
            print("response: {}".format(e))
    


def all_message(bot, update):
    chat_id = update.channel_post.chat.id
    if chat_id == -1001272004845:    # only process message from main channel
        logging.info("scheduling check for {}".format(update.channel_post.text))
        schedule.enter(     # schedule check 10 mins later
            600, 0, 
            screen_tweets, 
            argument=(
                bot, 
                update.channel_post.message_id, 
                update.channel_post.chat.id, 
                update.channel_post.text,
            )
        )
        t = threading.Thread(target=schedule.run)
        t.start()


def main():
    updater = Updater(BOT2_TOKEN)
    dp = updater.dispatcher


    command_handler = MessageHandler(Filters.command, all_message)
    text_handler = MessageHandler(Filters.text, all_message)

    dp.add_handler(command_handler)
    dp.add_handler(text_handler)

    logging.info("start polling")
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print("something went wrong: %s" % str(e))

# channel id: update.channel_post.chat.id
# channel name: update.channel_post.chat.title
# message id : update.channel_post.message_id
# message: update.channel_post.text