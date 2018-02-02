"""This module deletes submissions and comments that are old enough"""
from collections import Counter
import datetime
import random
# Third-party libraries
import praw
import fire
from tendo import singleton

def get_date(reddit_object):
    """Transform a PRAW timstamp into datetime"""
    time = reddit_object.created
    return datetime.datetime.fromtimestamp(time)

def is_days_old(input_date, days):
    """Checks whether the [input] datetime object is at least [days] old"""
    check_date = datetime.datetime.utcnow() - datetime.timedelta(days=days)
    return check_date > input_date

def get_all_queries(sublisting):
    """A helper funtction that return all 4 functions that you can query
    a PRAW Sublisting object"""
    result = [sublisting.controversial, sublisting.hot,
              sublisting.new, sublisting.top]
    random.shuffle(result)
    return result

def sane_arguments(fire_input):
    """Transform the fire argument into a list of strings"""
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

    result = [i.lower() if type(i).__name__ == 'str' else str(i)
                for i in result]
    return result

def delete_content(subreddits, days_old):
    """The main function of this module, which deletes any submission or
    comment that resides in the [subreddits] and is at least [days_old]"""
    deleted = Counter()
    sub_cnt = Counter()
    subreddits_permitted = sane_arguments(subreddits)

    # Create the Reddit Instance based on the configuration (praw.ini)
    reddit = praw.Reddit("deletebot")
    me_redditor = reddit.user.me()

    # Quering for comments
    for query in get_all_queries(me_redditor.comments):
        for comment in query(limit=None):
            if ((str(comment.subreddit).lower() in subreddits_permitted)
                    and (is_days_old(get_date(comment), days_old))):
                comment.delete()
                deleted['comments'] += 1
                sub_cnt[str(comment.subreddit)] += 1
    print("Comments deleted: %d" % (deleted['comments']))

    # Quering for submissions
    for query in get_all_queries(me_redditor.submissions):
        for submission in query(limit=None):
            if ((str(submission.subreddit).lower() in subreddits_permitted)
                    and (is_days_old(get_date(submission), days_old))):
                submission.delete()
                deleted['submissions'] += 1
                sub_cnt[str(submission.subreddit)] += 1
    print("Submissions deleted: %d" % (deleted['submissions']))
    print("---")
    for i in sorted(sub_cnt):
        print("Total deleted content in /r/%s: %d" % (i, sub_cnt[i]))

def main():
    """The main function of the script. It prohibits to run in parallel
       and also make the argument parsing"""
    _ = singleton.SingleInstance()
    fire.Fire(delete_content)

if __name__ == '__main__':
    main()
