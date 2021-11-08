import time
import mysql.connector
import requests
from mysql.connector import Error
import kkbox
print("type the password of DB: ")
pwd = input()

#連線DB
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=pwd,
    database="kkbox_chart_data"
    )
mycursor = mydb.cursor()

try:
    if mydb.is_connected():

        #顯示資料庫版本
        db_info = mydb.get_server_info()
        print("DB版本： "+ db_info)
                
        #顯示當前連接的資料庫
        mycursor.execute("SELECT DATABASE()")
        for i in mycursor:
            print("當前使用DB：", i[0])

except:
    print("DB連接錯誤： ", Error)  


#排行榜寫入table
def insert_chart_data_into_table(chart_id):

    #新增SQL
    command = "INSERT INTO charts(id, name, artist, url)VALUES(%s, %s, %s, %s)"

    #取得欲新增的排行榜內容
    charts = kkbox.get_tracks_in_chart(chart_id)

    #寫入table
    for i in charts:
        mycursor.execute(command, (i["id"], i["name"], i["album"]["artist"]["name"], i["url"]))

    #確定寫入
    mydb.commit()

    #測試有無資料
    '''
    mycursor.execute("SELECT * FROM charts")
    t = mycursor.fetchone()
    print(t)
    '''
    return print("寫入完成")

#確認帶入的id有無錯誤
def type_chart_id_want_to_insert():
    try:
        print("type a chart id you want: ")
        id = input()

        #LOADING效果
        print("Loading",end = "")
        for i in range(10):
            print(".",end = '',flush = True)
            time.sleep(0.5)
        print("")

        #帶入chart_id
        insert_chart_data_into_table(id)
    except:
        print("Error, please type a correct id")

#主程式
def main():
    #取得排行榜id
    kkbox.get_chart()
    
    type_chart_id_want_to_insert()

    #測試用
    #insert_chart_data_into_table("LZPhK2EyYzN15dU-PT")

if __name__ == '__main__':
    main()




    








