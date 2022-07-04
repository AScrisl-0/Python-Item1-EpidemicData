import pymysql


db =None

try:
    db = pymysql.connect(host='localhost',user='root',password='Password123$',port=3306)
except Exception:
    print("数据库连接失败！")
else:
    print("数据库连接成功！")
finally:
    if db:
        db.close()