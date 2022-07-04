import pymysql

db = None
try:
    db = pymysql.connect(host='localhost',user='root',password='Password123$',database='spiders',port=3306)
    # 获取游标对象
    cursor = db.cursor()
    sql = """SELECT * FROM student1"""
    cursor.execute(sql)
    # 获取查询结果
    result = cursor.fetchall()
    # 遍历查询的结果
    for row in result:
        name = row[1]
        age = row[2]
        print("姓名:%10s,年龄:%d" % (name, age))
    db.commit()
except Exception as e:
    print("数据库操作出错！", e)
else:
    print("数据库操作成功！")
finally:
    # 关闭数据库
    if db:
        db.close()