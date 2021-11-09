import time
import requests
import kkbox
from db_connection import mydb, mycursor

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
    
    #實行功能
    type_chart_id_want_to_insert()


if __name__ == '__main__':
    main()




    








