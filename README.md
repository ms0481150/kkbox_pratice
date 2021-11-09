使用API獲取資料-以KKBOX Open API為例
===


[![hackmd-github-sync-badge](https://hackmd.io/KYOdu-jyRFWFVlqGaHzh2Q/badge)](https://hackmd.io/KYOdu-jyRFWFVlqGaHzh2Q)
[TOC]

前言
---

為了練習資料寫入MySQL，先練習從API來獲取資料，以利後續操作  
雖然官方有提供`kkbox-developer-sdk`來簡化操作，不過還是希望用基礎的方式來練習

[KKBOX Open API](https://docs-zhtw.kkbox.codes/#overview--%E4%BB%8B%E7%B4%B9)

有關在Conda中使用pip：  
[Using pip in an environment](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#using-pip-in-an-environment)  
[How to install PyPi packages using anaconda conda command-stackoverflow](https://stackoverflow.com/questions/29286624/how-to-install-pypi-packages-using-anaconda-conda-command)  

> 最後更新：[time=Tue, Nov 9, 2021 5:01 PM][name=Jacky Chuang]


環境
---
`Python`：3.6.13(為配合`mysql-connector-python`而使用3.6)  
`requests`：2.26.0  
`mysql-connector-python`：8.0.18



前置作業
---

### 建立App獲取 ID & Secret
前往KKBOX開發者頁面，註冊帳號後建立App，取得ID與Secret
![](https://i.imgur.com/l2ZUja6.png)


### 獲取Access_Token
需要使用KKBOX OAuth 2.0 Token API來獲取Access_Token使用API  
使用requests package來發送request請求
```python=
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
        "client_id": "自己的ID",
        "client_secret": "自己的SECRET"
    }

    access_token = requests.post(url=url, headers=headers, data=data)
    
    #取得response中的access_token
    return access_token.json()["access_token"]
```
而response的JSON檔範例如下:
```json=
{
  "access_token": "fCVTwABPlcO6Qxc7Ll23rsdfsf",
  "expires_in": 1492982700,
  "token_type": "Bearer"
}
```

使用 KKBOX APIs 獲取資料
---
獲取access_token後，就可以有權限呼叫API了  
以獲取音樂排行榜為例，根據API文件帶入Header要的內容與參數
![](https://i.imgur.com/zqUCjX1.png)


```python=
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
```
這時根據response回來的JSON取用需要的內容，我以取用 ID 與 標題 為例會如下所示:
```
LZPhK2EyYzN15dU-PT 綜合新歌即時榜
8n2tN-nbFBkcmf7148 華語單曲日榜
5ayRdCxgnNDC77-W2v 西洋單曲日榜
HZ0Ha-izzAH65Ef1Wo 韓語單曲日榜
0rC1QejCzZ7WGo4ZeB 日語單曲日榜
0mHoeJQfTW0auM3zqb 台語單曲日榜
Ha9qR37M_aVO3xko99 粵語單曲日榜
9Xy755NiUFThOCHopG 華語新歌日榜
DYOevsoFw4Kz5SZoHF 西洋新歌日榜
LXaTI8WGqyA6QX9Qig 韓語新歌日榜
Ks2mru5whgbL7zxq1t 日語新歌日榜
Okx30A--JB8-QzjvXc 台語新歌日榜
Gre9tFT6iNRIT4lYxr 粵語新歌日榜
KmZLKejDu5MxGy6KjP 原聲帶單曲週榜
CkHGdUN2fJZPFwQC6B 電子單曲週榜
OrnGS58Q_b3P1D1PwX 嘻哈單曲週榜
Da6OlToa6hWuNVGZ-0 R＆B單曲週榜
X-ST0z_4wzDxno6gX1 爵士單曲週榜
1ZpbnANePcQzNY8D3b 搖滾單曲週榜
GlZFWPqQJoxtrKKAtX 獨立/另類單曲週榜
5-IRVllW5_mo8GO5Hp 靈魂樂單曲週榜
9ZMCs6ghQ1a9ywvHbP 鄉村單曲週榜
5YVNtRm93dAIP_G7_L 雷鬼單曲週榜
DX-GMF-EHhl4uZPWTS 有聲書 / 相聲單曲週榜
Ot9b9neLPHGat4LYK- 英美金曲榜
__u6jEV61Qgdt4Tci1 錢櫃國語點播榜
4r3AnG_o9kvNjwSvIr 錢櫃台語點播榜
GnherLVRBEMYgp_iSG 錢櫃國語新歌榜
9Y0bAhEBuyYIc1HFIc 錢櫃台語新歌榜
```
同理，可以根據API文件裡回傳的JSON文件的其他內容來取用不同的列表或歌曲資訊。

將獲取的資料寫入MySQL
---
有關連線MySQL的方法之前有寫過筆記：https://hackmd.io/eQBW_HzkRaiCRD_3opxEYg  

下一步希望取得指定排行榜中的內容，所以根據API文件所需要的headers與parameter來撰寫函式獲得：  
```python=
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
```
而我從回傳資料中取用幾個想寫入的內容，在MySQL中先建立好columns：  
![](https://i.imgur.com/gKQzaCB.png)


透過`get_chart()`獲取排行榜ID後，傳入`get_tracks_in_chart()`指定任一個排行榜內容寫入資料庫：  
```python=
 #新增SQL
    command = "INSERT INTO charts(id, name, artist, url)VALUES(%s, %s, %s, %s)"

    #取得欲新增的排行榜內容
    charts = kkbox.get_tracks_in_chart(chart_id)

    #寫入table
    for i in charts:
        mycursor.execute(command, (i["id"], i["name"], i["album"]["artist"]["name"], i["url"]))

    #確定寫入
    mydb.commit()
    
    return print("寫入完成")
```
這時候就會發現MySQL中建立好的table已經被寫入剛剛指定排行榜的內容了!  
![](https://i.imgur.com/2Iv4JcC.png)

所以綜上所述整體獲取資料寫入資料庫的流程如下：  
1. 透過`KKBOX OAuth 2.0 Token API`來獲取Access_Token。
2. 以獲取排行榜為例，根據API文件所需要的內容發送必要之標頭與參數，獲得回傳的JSON。
3. 根據回傳的JSON取用需要的內容，擷取後利用`mysql-connect-python`串接預先建立好的資料庫與表單，寫入對應的資料。

結語
---
過程中遇到幾個之後可能需要修正的點：  
* 一個帳號獲取的Access Token會有過期問題，需要再加上自動更新的功能。
* `mysql-connector-python`能支援的`python`版本目前似乎只到3.6，所以可以改用其他的package看看，例如`pymysql`。

接下來應該會想練習結合flask來建立前端介面實作功能應用。



###### tags: `MySQL`, `GitHub`