# 必要なライブラリ，.pyファイルのインポート
import urllib.request, urllib.error
import pandas as pd
import config
import tweepy
import time
import datetime
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

    def __init__(self, location):
        """
        イニシャライザ，
        呼び出しの段階でAPI認証ならびに地名の入力をさせる
        """
        self.dt_today = datetime.date.today().strftime('%Y-%m-%d_')
        self.location = location
        self.lat = self.f_getting_geo()[0] # 指定した地域の緯度
        self.lng = self.f_getting_geo()[1] # 指定した地域の経度
        self.api = self.f_authenticating_twitter_api()


    def f_authenticating_twitter_api(self):
        """
        API認証関数
        return:
            api:認証済のAPI情報(tweepy.api.API)
        """
        auth = tweepy.OAuthHandler(self.api_key, self.api_key_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        api = tweepy.API(auth)

        return api


    def f_getting_geo(self) -> list: 
        """
        入力した目的地の緯度経度を返す関数
        return:
            地名の緯度軽度（list）
        """
        ret = geocoder.osm(self.location, timeout=5.0)

        return ret.latlng


    def f_identifying_weather_from_tweets(self) -> str:
        """
        ツイートを取得して天気を割り出す関数
        return:
            現地の天気
        """
        q = f'晴 OR くもり OR 雨降 OR 雪降 since:{self.dt_today}_JST geocode:{self.lat},{self.lng},10km -replies'
        item_num = 15

        tweets = tweepy.Cursor(
                                self.api.search_tweets, 
                                q=q, 
                                lang='ja'
                            ).items(item_num)
        
        for tweet in tweets:
            print(tweet.text) # ちゃんとツイートを取得できているかどうかチェックするためprint
            for weather in self.WEATHER_LIST.keys():
                if weather in tweet.text: self.WEATHER_LIST[weather]+=1


        if sum(list(self.WEATHER_LIST.values()))==0: #WEATHER_LISTのバリューが全部0なら，ツイートを取得できていないことになる
            weather_answer = 'ツイートを取得できなかったため，天気を割り出せませんでした'
        else:
            weather_answer = f'現在の{self.location}の天気は{max(self.WEATHER_LIST,key=self.WEATHER_LIST.get)}であると見込まれます．'
        return weather_answer


def main():
    location_input = input('場所を入力してください：')
    weather_the_location = SearchTweetsAPI(location_input)
    ans = weather_the_location.f_identifying_weather_from_tweets()
    print(ans)

if __name__ == '__main__':
    main()

