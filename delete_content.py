import datetime
from tendo import singleton
import praw
import fire

def get_date(reddit_object):
    time = reddit_object.created
    return datetime.datetime.fromtimestamp(time)

def is_days_old(input_date, days):
    check_date = datetime.datetime.utcnow() - datetime.timedelta(days=days)
    return check_date > input_date

def get_all_queries(sublisting):
    return [sublisting.controversial, sublisting.hot,
            sublisting.new, sublisting.top]

def sane_arguments(fire_input):
    """Transform the argument into a list of strings"""
    type_of = type(fire_input).__name__
    result = []

    # Try to convert possible
    if ((type_of == 'str') or (type_of == 'int') or (type_of == 'float')):
        result = [fire_input]
    elif type_of == 'list':
        result = fire_input[:]
    elif type_of == 'tuple':
        result = list(fire_input)
    elif type_of == 'dict':
        result = [key for key in fire_input]

    result = [i if type(i).__name__ == 'str' else str(i) for i in result]
    return result

def delete_content(subreddits, days_old):
    deleted_comments = 0
    deleted_submissions = 0

    subreddits_permitted = sane_arguments(subreddits)

    # Create the Reddit Instance based on the configuration (praw.ini)
    reddit = praw.Reddit("deletebot")
    me_redditor = reddit.user.me()

    # Quering for comments
    for query in get_all_queries(me_redditor.comments):
        for comment in query(limit=None):
            if ((comment.subreddit in subreddits_permitted)
                    and (is_days_old(get_date(comment), days_old))):
                comment.delete()
                deleted_comments += 1
    print("Comments deleted: %d" % (deleted_comments))

    # Quering for submissions
    for query in get_all_queries(me_redditor.submissions):
        for submission in query(limit=None):
            if ((submission.subreddit in subreddits_permitted)
                    and (is_days_old(get_date(submission), days_old))):
                submission.delete()
                deleted_submissions += 1
    print("Submissions deleted: %d" % (deleted_submissions))

def main():
    """The main function of the script. It prohibits to run in parallel
       and also make the argument parsing"""
    _ = singleton.SingleInstance()
    fire.Fire(delete_content)

if __name__ == '__main__':
    main()
