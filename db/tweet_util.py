NAME=1

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

def util_screen_tweet(conn, db_controller, tweet_data, user_data):
    backlist_result = db_controller.get_blacklist(conn)
    print("blackList retreived")
    blacklist = {(row["screen_name"]) for row in backlist_result}
    print(str(blacklist))
    print(user_data)
    if user_data[NAME] in blacklist:
        print("returning false")
        return False
    print("returning true")    
    return True