import pymysql

db = None
try:
    db = pymysql.connect(host='localhost',user='root',password='Password123$',database='spiders',port=3306)
    # 获取游标对象
    cursor = db.cursor()
    name=input("请输入需要修改的姓名:")
    age=int(input("请输入修改后的年龄值:"))
    sqlParam=(age,name)
    sql="""UPDATE student1 SET s_age=%s WHERE s_name=%s;"""
    ret=cursor.execute(sql,sqlParam)
    print("实际更新了%d条记录" % ret)
    db.commit()
except Exception as e:
    print("数据库操作出错！", e)
else:
    print("数据库操作成功！")
finally:
    # 关闭数据库
    if db:
        db.close()
