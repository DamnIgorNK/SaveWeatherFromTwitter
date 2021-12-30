# 必要なライブラリ，.pyファイルのインポート
import urllib.request, urllib.error
import pandas as pd
import config
import tweepy
from collections import Counter
import numpy as np

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


def main():
    #入力する地名
    search_keyword = input('地名を入力してください：')
    item_num = 6 # 6個くらい拾ってくれりゃいける

    tweets = tweepy.Cursor(api.search_tweets, q=f'{search_keyword} 晴 OR くもり OR 曇 OR 雨 OR 雪 OR 雷', lang='ja').items(item_num)
    for tweet in tweets:
        print(tweet.text)
        print(tweet.id)

if __name__=='__main__':
    main()





