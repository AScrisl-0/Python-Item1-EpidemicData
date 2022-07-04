import pymysql


db =None

try:
    db = pymysql.connect(host='localhost',user='root',password='Password123$',database='spiders',port=3306)
    # 创建游标对象
    cursor = db.cursor()

    # 创建表
    sql = """create table if not exists student1(s_id int auto_increment  primary key,s_name varchar(10),s_age int);"""
    # 执行SQL语句
    cursor.execute(sql)

except Exception as e:
    print("数据库操作失败！",e)
else:
    print("数据库操作成功！")
finally:
    if db:
        db.close()