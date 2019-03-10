import logging
from db_config import *

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', filename='db-service.log',level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

def get_tweet_data(request):
    return (
        int(request.values["id"]),
        request.values["url"],
        request.values["date"],
        int(request.values["user_id"])
    )

def get_user_data(request):
    return (
        int(request.values["user_id"]),
        request.values["name"],
        int(request.values["count"])
    )

def util_screen_tweet(conn, db_controller, request):
    backlist_result = db_controller.get_blacklist(conn)

    blacklist = {(row["screen_name"]) for row in backlist_result}

    if request.values["name"] in blacklist:
        logger.info("restricted user @%s" % request.values["name"])
        return False

    for word in RESTRICTED_WORDS:
        if word in request.values["text"]:
            logger.info('restricted word "%s"' % word)
            return False
        
    print("returning true")    
    return True