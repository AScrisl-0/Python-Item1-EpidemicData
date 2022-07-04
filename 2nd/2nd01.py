import pymysql


db =None

try:
    db = pymysql.connect(host='localhost',user='root',password='Password123$',database='spiders',port=3306)
    # 创建游标对象
    cursor = db.cursor()

    # 创建全国舆情信息表
    sql = """CREATE TABLE `history` (
  `ds` datetime NOT NULL COMMENT '日期',
  `confirm` int(255) DEFAULT NULL COMMENT '累计确诊',
  `confirm_add` int(255) DEFAULT NULL COMMENT '当日新增确诊',
  `confirm_now` int(255) DEFAULT NULL COMMENT '当前确诊',
  `heal` int(255) DEFAULT NULL COMMENT '累计治愈',
  `heal_add` int(255) DEFAULT NULL COMMENT '当日新增治愈',
  `dead` int(255) DEFAULT NULL COMMENT '累计死亡',
  `dead_add` int(255) DEFAULT NULL COMMENT '当日新增死亡',
  `importedCase` int(255) DEFAULT NULL COMMENT '境外输入案例',
  `importedCase_add` int(255) DEFAULT NULL COMMENT '新增境外输入',
  PRIMARY KEY (`ds`) USING BTREE
) DEFAULT CHARSET=utf8mb4;"""
    # 执行SQL语句
    cursor.execute(sql)

except Exception as e:
    print("数据库操作失败！",e)
else:
    print("数据库操作成功！")
finally:
    if db:
        cursor.close()
        db.close()