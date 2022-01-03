# 必要なライブラリ，.pyファイルのインポート
import urllib.request, urllib.error
import pandas as pd
import config
import tweepy
from collections import Counter
import numpy as np
import time
import geocoder # 位置情報APIモジュール，緯度軽度を返させる



class SearchTweetsAPI:
    #twitter object
    api_key             = config.API_KEY
    api_key_secret      = config.API_KEY_SECRET
    bearer_token        = config.BEARER_TOKEN
    access_token        = config.ACCESS_TOKEN
    access_token_secret = config.ACCESS_TOKEN_SECRET

    # 天気リスト，雨雪は状態動詞の寄与を除くために「降」の字を付けている
    WEATHER_LIST = {'晴れ':0,
                'くもり':0,
                '雨降':0,
                '雪降':0}

    def __init__(self):
        """
        イニシャライザ，
        呼び出しの段階でAPI認証ならびに地名の入力をさせる
        """
        self.location = input('地名を入力してください：')
        self.lat, self.lng = self.f_getting_geo() 
        self.api = self.f_authenticating_twitter_api()


    def f_authenticating_twitter_api(self) -> tweepy.api.API:
        """
        API認証関数
        return:
            api:認証済のAPI情報(tweepy.api.API)
        """
        auth = tweepy.OAuthHandler(self.api_key, self.api_key_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        api = tweepy.API(auth)
        print(type(api))
        return api


    def f_getting_geo(self) -> list: 
        """
        return:
            地名の緯度軽度（list）
        """
        ret = geocoder.osm(self.location, timeout=5.0)
        return ret.latlng


    def f_identifying_weather_from_tweets(self) -> str:
    
        q = f'晴れ OR くもり OR 雨降 OR 雪降 geocode:{self.lat},{self.lng},10km -replies'
        item_num = 15

        tweets = tweepy.Cursor(
                                self.api.search_tweets, 
                                q=q, 
                                lang='ja'
                            ).items(item_num)
        
        for tweet in tweets:
            for weather in self.WEATHER_LIST.keys():
                if weather in tweet.text: self.WEATHER_LIST[weather]+=1

        weather_answer = f'現在の{self.location}の天気は{max(self.WEATHER_LIST,key=self.WEATHER_LIST.get)}であると見込まれます．'
        return weather_answer


def main():
    weather_the_location = SearchTweetsAPI()
    ans = weather_the_location.f_identifying_weather_from_tweets()
    print(ans)

if __name__ == '__main__':
    main()

