import mysql.connector
from mysql.connector import Error


#連線DB

print("type the password of DB: ")
pwd = input()

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