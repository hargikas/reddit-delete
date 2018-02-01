import praw

def main():
    # Create the Reddit Instance based on the configuration (praw.ini)
    reddit = praw.Reddit("deletebot")

    active_redditor = reddit.redditor('hargikas')
    for comment in active_redditor.get_comments(limit=None):
        print(comment.body)


if __name__ == '__main__':
    main()
