import pymysql


db =None

try:
    db = pymysql.connect(host='localhost',user='root',password='Password123$',database='spiders',port=3306)
    # 创建游标对象
    cursor = db.cursor()

    # 创建表
    sql = """insert into student1(s_name,s_age) values
    ("zhangsan",22),
    ("lisi",23),
    ("wnagwu",25);
    """
    # 执行SQL语句
    cursor.execute(sql)
    db.commit()
except Exception as e:
    print("数据库操作失败！",e)
else:
    print("数据库操作成功！")
finally:
    if db:
        db.close()