import pymysql

db = None
try:
    db = pymysql.connect(host='localhost',user='root',password='Password123$',database='spiders',port=3306)
    cursor = db.cursor()
    sqlParam = input("请输入需要删除的姓名:")
    sql = """DELETE FROM student1 WHERE s_name=%s;"""
    ret = cursor.execute(sql, sqlParam)
    print("实际删除了%d条记录" % ret)
    db.commit()
except Exception as e:
    print("数据库操作出错！", e)
else:
    print("数据库操作成功！")
finally:
    # 关闭数据库
    if db:
        db.close()