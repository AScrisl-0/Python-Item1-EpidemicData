import pymysql

db =None
try:
    db = pymysql.connect(host='localhost',user='root',password='Password123$',database='spiders',port=3306)
    # 创建游标对象
    cursor = db.cursor()

    # 创建当日中高风险地区的数量表
    sql = """CREATE TABLE `risknum` (
  `id` int(255) NOT NULL AUTO_INCREMENT,
  `update_time` varchar(255) DEFAULT NULL COMMENT '数据最后更新时间',
  `hnum` INT(255) DEFAULT NULL COMMENT '高风险地区数量',
  `mnum` INT(255) DEFAULT NULL COMMENT '中风险地区数量',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"""
    # 执行SQL语句
    cursor.execute(sql)

except Exception as e:
    print("数据库操作失败！",e)
else:
    print("数据库操作成功！")
finally:
    if db:
        db.close()