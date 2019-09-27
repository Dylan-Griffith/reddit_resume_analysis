import csv
from psaw import PushshiftAPI
import praw
import config
import datetime as dt
from collections import defaultdict
from nltk.corpus import stopwords
import nltk
import pandas as pd
import os

stop_words = set(stopwords.words('english'))


def clean_words(lst):
    filtered_sentence = []
    for w in lst:
        if w not in stop_words:
            filtered_sentence.append(w)

    return filtered_sentence


def save_raw_data(data_frame):
    if os.path.exists('./raw_data.csv'):
        with open('raw_data.csv', 'a') as fout:
            data_frame.to_csv(fout, index=False, header=False)
    else:
        print('Creating File...')
        data_frame.to_csv('raw_data.csv', index=False)
        print('File Created')


def authenticate():
    print('Authenticating User....')
    reddit = praw.Reddit(client_id=config.client_id,
                         client_secret=config.client_secret,
                         user_agent=config.user_agent,
                         username=config.username,
                         password=config.password)
    print("User '{user}' Authenticated".format(user=reddit.user.me()))
    return reddit


def get_date(created):
    return dt.datetime.fromtimestamp(created)


reddit = authenticate()
api = PushshiftAPI(reddit)

discard = ['Meta', 'Other', 'Discussion']
industry_freq = defaultdict(int)

# Dictionary: list of words from each post
industry_words = defaultdict(list)

# searches through subreddit for all submissions AFTER start epoch time. Returns submission object similar to praw
start_epoch = int(dt.datetime(2017, 1, 1).timestamp()) # 2017 1, 1
submission_ids = list(api.search_submissions(after=start_epoch,
                                             subreddit='resumes',
                                             filter=['url', 'author', 'title', 'subreddit']))
# to save to csv
post_dct = {
        "link flair": [],
        "username": [],
        "title": [],
        "text": [],
        "url": [],
        "created_at": [],
    }

all_words = []

uni_all_words = defaultdict(int)

for sub_id in submission_ids:
    if sub_id.link_flair_text and sub_id.link_flair_text not in discard:
        post_dct['link flair'].append(sub_id.link_flair_text)
        post_dct['username'].append(sub_id.author)
        post_dct['title'].append(sub_id.title.lower())
        all_words.append(sub_id.title.lower())
        post_dct['text'].append(sub_id.selftext.lower())
        all_words.append(sub_id.selftext.lower())
        post_dct['url'].append('https://www.reddit.com' + str(sub_id.permalink))
        post_dct['created_at'].append(get_date(sub_id.created_utc))

        # populates defined dictionaries
        industry_freq[sub_id.link_flair_text] += 1
        industry_words[sub_id.link_flair_text].append(sub_id.title.lower())
        if sub_id.selftext:
            industry_words[sub_id.link_flair_text].append(sub_id.selftext.lower())


w = csv.writer(open("Industry Frequency.csv", "w"))
for key, val in industry_freq.items():
    w.writerow([key, val])

industries = list(industry_words)

for key in industries:
    uni_gram_words = defaultdict(int)

    words = [x for x in industry_words[key] if x != '[deleted]']
    words = [y for x in words for y in x.split()]
    words = clean_words(words)

    for word in words:
        uni_gram_words[word] += 1

    bi = list(nltk.bigrams(words))
    bi_freq = nltk.FreqDist(bi)
    bi_most_common = dict(bi_freq.most_common(50))

    tri = list(nltk.trigrams(words))
    tri_freq = nltk.FreqDist(tri)
    tri_dct = dict(tri_freq.most_common(50))

    w = csv.writer(open("{} uni_gram.csv".format(key), "w"))
    for a, b in uni_gram_words.items():
        w.writerow([a, b])

    w = csv.writer(open("{} Bigram.csv".format(key), "w"))
    for k, v in bi_most_common.items():
        w.writerow([k, v])

    w = csv.writer(open("{} TriGram.csv".format(key), "w"))
    for key, val in tri_dct.items():
        w.writerow([key, val])


# master unigram bigram and trigram

freq_all_words = defaultdict(int)

all_words = [y for x in all_words for y in x.split()]
all_words = [x for x in all_words if x != '[deleted]']
all_words = clean_words(all_words)

for word in all_words:
    freq_all_words[word] += 1

bi = list(nltk.bigrams(all_words))
bi_freq = nltk.FreqDist(bi)
bi_most_common = dict(bi_freq.most_common(100))

tri = list(nltk.trigrams(all_words))
tri_freq = nltk.FreqDist(tri)
tri_dct = dict(tri_freq.most_common(100))


w = csv.writer(open("Master Unigram.csv", "w"))
for a, b in freq_all_words.items():
    w.writerow([a, b])

w = csv.writer(open("Master Bigram.csv", "w"))
for k, v in bi_most_common.items():
    w.writerow([k, v])

w = csv.writer(open("Master TriGram.csv", "w"))
for key, val in tri_dct.items():
    w.writerow([key, val])


data_frame = pd.DataFrame(post_dct, columns=['link flair',
                                             'username',
                                             'title',
                                             'text',
                                             'url',
                                             'created_at'])
save_raw_data(data_frame)
#
