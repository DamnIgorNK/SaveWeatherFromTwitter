# 必要なライブラリ，.pyファイルのインポート
import urllib.request, urllib.error
import pandas as pd
import config
import tweepy
from collections import Counter
import numpy as np
import time

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

WEATHER_LIST = {'晴':0,
                '曇':0,
                'くもり':0,
                '雨降':0,
                '雷':0,
                '雪降':0}

def main():
    # 対象の地名
    search_keyword = input('地名を入力してください：')
    
    # 検索条件
    q = f'{search_keyword} 晴 OR くもり OR 曇 OR 雨降 OR 雪降 OR 雷'
    item_num = 10

    # 計算開始時間
    start_time = time.time()

    tweets = tweepy.Cursor(api.search_tweets, q=q, lang='ja').items(item_num)

    for tweet in tweets:
        for weather in WEATHER_LIST.keys():
            if weather in tweet.text: WEATHER_LIST[weather]+=1
    
    # 総計算時間
    elapsed_time=time.time()-start_time
    print(f'計算時間：{elapsed_time}sec')

    print(f'{time.time()}時点での{search_keyword}の天気は{max(WEATHER_LIST,key=WEATHER_LIST.get)}であると見込まれます．')

if __name__=='__main__':
    main()




