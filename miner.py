import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from textblob import TextBlob
import re as regex
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os
# from io import BytesIO
# import base64
# import plotly.plotly as py
# import plotly.graph_objs as go
# import json

class Init_Connection():
    def Init_Connection(self):
        api = None
        auth = None
        consumer_key = '4N18JRcCs4a6XsqBybCuBQjcI'
        consumer_secret = 'W1vbhCYjVSYbuFaaFvpp4Qsg5JLndROn62aONu2VzvoT6tzYVA'
        access_token = '973754658840875008-nBhYaqxNips6HTkXNgIKC0HkMiyicnV'
        access_secret = 'MV1BxlnasCel8jrgz5SPMlSgkUGyyONimxc2qZDRgDJiq'
        try:
            auth = OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_secret)

            api = tweepy.API(auth)
        except:
            print("Authentication Failed!!")
        return api, auth


def cleanTweet(tweet):
        return ' '.join(regex.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


# class dataCleanup():
#     @staticmethod
#     def removeByRegex(t, regExp):
#         t.replace(regExp, "")
#         return t
#
#     def removeUrls(self, t):
#         return dataCleanup.removeByRegex(t, regex.compile(r"http.?://[^\s]+[\s]?"))
#
#     def removeUserNames(self, t):
#         return dataCleanup.removeByRegex(t, regex.compile(r"@[^\s]+[\s]?"))
#
#     def removeSpecialCharacters(self, t):
#         for remove in map(lambda r: regex.compile(regex.escape(r)), [",", ":", "\"", "=", "&", ";", "%", "$", "@", "%", "^", "*", "(", ")", "{", "}", "[", "]", "|", "/", "\\", ">", "<", "-", "!", "?", ".", "'", "--", "---", "#"]):
#             t.replace(remove, "", inplace=True)
#         return t
#
#     def removeNumbers(self, t):
#         return dataCleanup.removeByRegex(t, regex.compile(r"\s?[0-9]+\.?[0-9]*"))
#
#     def cleanData(self, t):
#         # t = self.processedData
#         t = self.removeUrls(t)
#         t = self.removeUserNames(t)
#         # t = self.removeNotAvailable(t)
#         t = self.removeSpecialCharacters(t)
#         t = self.removeNumbers(t)
#         return t

def getTweetSentiment(tweet):
        # cd = dataCleanup()
        # tweet = cd.cleanData(tweet)
        # tweet = cleanTweet(tweet)
        analysis = TextBlob(tweet)
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

# class Stream_Listener(StreamListener):
#     def on_data(self, data):
#         try:
#             f = open('Output.json', 'a')
#             f.write(data)
#             print(data)
#             return True
#         except BaseException as e:
#             print("Error = " + str(e))
#         return True
#     def on_error(self, status):
#         print "Error"
#         print(status)
#         return True

def getTweets(api, topic, number):
    processedTweets = []
    try:
        # tweets = api.search(q=topic, count=number)
        max_tweets = 1000
        if number < max_tweets:
            max_tweets = number
        tweets = [status for status in tweepy.Cursor(api.search, q=topic).items(max_tweets)]
        print("len tweets= " + str(len(tweets)))
        for tweet in tweets:
            tw = {}
            tw['text'] = tweet.text
            tw['sentiment'] = getTweetSentiment(tweet.text)
            if tweet.retweet_count > 0:
                if tw not in processedTweets:
                    processedTweets.append(tw)
            else:
                processedTweets.append(tw)
    except tweepy.TweepError as e:
        print("Error : " + str(e))
    return processedTweets

def performSentimentAnalysis(topic, number):
    processedTweets = []
    init =  Init_Connection()
    api, auth = init.Init_Connection()
    if api is not None and auth is not None:
        print(topic)
        print(number)
        processedTweets = getTweets(api, topic, number)
    else: return False
    print("len = " + str(len(processedTweets)))
    sentiments = ('positive', 'neutral', 'negative')
    sentimentsCount = []
    for s in sentiments:
        counter = 0
        for t in processedTweets:
            if s == t['sentiment']:
                counter += 1
        sentimentsCount.append(counter)
    # data = [go.Histogram()]
    # print(processedTweets)
    print(sentimentsCount)

    plt.bar(range(3), sentimentsCount, align='center')
    plt.title("Sentiments Count")
    plt.xticks(range(3),sentiments, size='small')
    plt.xlabel("Sentiments")
    plt.ylabel("Frequency")
    if os.path.isfile('/home/shivgpt/mysite/static/plot.png'):
        os.remove('/home/shivgpt/mysite/static/plot.png')
    plt.savefig('/home/shivgpt/mysite/static/plot.png')
    plt.clf()
    plt.cla()
    plt.close()
    return True

# if __name__ == '__main__':
#     performSentimentAnalysis('Trump', 100)

