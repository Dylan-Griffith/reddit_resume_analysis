import config
import praw
from psaw import PushshiftAPI
from collections import defaultdict
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import string


def authenticate():
    print('Authenticating User....')
    reddit = praw.Reddit(client_id=config.client_id,
                         client_secret=config.client_secret,
                         user_agent=config.user_agent,
                         username=config.username,
                         password=config.password)
    print("User '{user}' Authenticated".format(user=reddit.user.me()))
    return reddit


discard = ['Meta', 'Other', 'Discussion']
reddit = authenticate()
api = PushshiftAPI(reddit)

resumes = reddit.subreddit('resumes')

resume_results = defaultdict(int)

bi_list = []
a = 0
for submission in resumes.hot(limit=None):
    a += 1
    # if submission.link_flair_text and submission.link_flair_text not in discard:
    #     bi_list.append(submission.title.lower())
    #     a += 1
    #     # print(submission.title)
    #     # print(submission.link_flair_text)
    #     resume_results[submission.link_flair_text] += 1
    #     # print('---' * 10)

#  makes Bi gram
# print(bi_list)
# formatted_bi_list = [x.split() for x in bi_list]
# print(formatted_bi_list)
# formatted_bi_list = [y for x in formatted_bi_list for y in x]
#
#
# bi = list(nltk.bigrams(formatted_bi_list))
# print(bi)
# bi_freq = nltk.FreqDist(bi)
# bi_most_common = dict(bi_freq.most_common(25))
# print(bi_most_common.keys())
# print(bi_most_common.values())
# print(bi_most_common.items())
# print(bi_most_common)
# print(a)

# print('___________________________________')
# print(resume_results)
# for w in sorted(resume_results, key=resume_results.get, reverse=True):
#     print(w, resume_results[w])

# https://api.pushshift.io/reddit/search/submission/?subreddit=resumes

#https://api.pushshift.io/reddit/search/submission/?subreddit=resumes&size=1000&fields=link_flair_text&fields=title&fields=selftext

# selftext