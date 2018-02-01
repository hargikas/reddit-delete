import datetime
import praw

def get_date(reddit_object):
    time = reddit_object.created
    return datetime.datetime.fromtimestamp(time)

def is_days_old(input_date, days):
    check_date = datetime.datetime.utcnow() - datetime.timedelta(days=days)
    return check_date > input_date

def get_all_queries(sublisting):
    return [sublisting.controversial, sublisting.hot,
            sublisting.new, sublisting.top]

def main():
    deleted_comments = 0
    deleted_submissions = 0
    # Create the Reddit Instance based on the configuration (praw.ini)
    reddit = praw.Reddit("deletebot")
    me_redditor = reddit.user.me()

    # Quering for comments
    for query in get_all_queries(me_redditor.comments):
        for comment in query(limit=None):
            if ((comment.subreddit == 'greece')
                    and (is_days_old(get_date(comment), 365))):
                deleted_comments += 1
    print("Comments deleted: %d" % (deleted_comments))

    # Quering for submissions
    for query in get_all_queries(me_redditor.submissions):
        for submission in query(limit=None):
            if ((submission.subreddit == 'greece')
                    and (is_days_old(get_date(submission), 365))):
                deleted_submissions += 1
    print("Submissions deleted: %d" % (deleted_submissions))



if __name__ == '__main__':
    main()
