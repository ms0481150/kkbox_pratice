import requests
import time
#API文件 https://docs-zhtw.kkbox.codes/#overview

#取得token
def get_access_token():
    
    #API網址
    url = "https://account.kkbox.com/oauth2/token"

    #標頭
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "account.kkbox.com"
    }

    #資料
    data = {
        "grant_type": "client_credentials",
        "client_id": "fa84eed68d045d3c01e8acff9dc20c8f",
        "client_secret": "2021815e2d618516c4a75cfcc42505cc"
    }

    access_token = requests.post(url=url, headers=headers, data=data)
    
    #取得response中的access_token
    return access_token.json()["access_token"]

#===================各種功能===========================


#取得排行榜名稱
def get_chart():
    access_token = get_access_token()

    url = "https://api.kkbox.com/v1.1/charts"

    #標頭
    headers = {
    'accept': "application/json",
    'authorization': "Bearer " + access_token   #帶入access token
    }

    #參數
    para = {
        "territory": "TW"
    }

    response = requests.get(url=url, headers=headers, params=para)
    result = response.json()["data"]            #包含id、title、description、url、images

    for i in result:
        print(i["id"], i["title"])

#取得排行榜中的歌曲
def get_tracks_in_chart(chart_id):
    #取得access_token
    access_token = get_access_token()
    
    url = "https://api.kkbox.com/v1.1/charts/" + chart_id + "/tracks"

    #標頭
    headers = {
        "accept": "application/json",
        "authorization": "Bearer " + access_token
    }

    para = {
        "territory": "TW",
        "offset": "0",
        #"limit": "100"
    }

    response = requests.get(url=url, headers=headers, params=para)
    result = response.json()["data"]

    #print
    '''
    count=1
    for i in result:
        print(count)
        count=count+1
        print("ID: "+ i["id"])
        print("曲名: "+ i["name"])
        print("歌手: "+ i["album"]["artist"]["name"])
        print("連結: "+ i["url"])
        print("============")
    '''
    return result


