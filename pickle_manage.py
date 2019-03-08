import pickle
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', filename='bot.log',level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

def get_pickle(name):
    try:
        with open(name, "rb") as pickle_file:
            content = pickle.load(pickle_file)
        return content
    except (OSError, IOError) as e:
        logger.error(e)

def get_save():
    saved_pickle = get_pickle("media.pk")
    if saved_pickle is None:
        return set()
    else:
        logger.info(saved_pickle)
        return saved_pickle

def save_pickle(date_set):
    saved_pickle = open("media.pk", "wb")
    pickle.dump(date_set, saved_pickle)
    saved_pickle.close()
