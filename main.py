# 必要なライブラリ，.pyファイルのインポート
import urllib.request, urllib.error
import pandas as pd
import config
import tweepy
import os
from collections import Counter

# 保存ディレクトリ
data_dir = '../data/'

#twitter object
api_key             = config.API_KEY
api_key_secret      = config.API_KEY_SECRET
bearer_token        = config.BEARER_TOKEN
access_token        = config.ACCESS_TOKEN
access_token_secret = config.ACCESS_TOKEN_SECRET


# OAuth
auth = tweepy.OAuthHandler(api_key,api_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


#天気情報
WEATHER_DICT = {'晴':'Sunny',
                '曇':'Cloudy',
                'くもり':'Cloudy',
                '雨':'Rainy',
                '雷':'Thunder',
                '雪':'Snowy'}


def main():
    #入力する地名
    search_keyword = input('地名を入力してください：')
    item_num = 4 # 4個くらい拾ってくれりゃいける

    tweets = tweepy.Cursor(api.search_tweets, q=[search_keyword], lang='ja').items(item_num)
    for tweet in tweets:
        print(tweet.text)

if __name__=='__main__':
    main()





