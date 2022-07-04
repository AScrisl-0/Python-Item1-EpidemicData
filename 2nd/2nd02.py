import pymysql


db =None

try:
    db = pymysql.connect(host='localhost',user='root',password='Password123$',database='spiders',port=3306)
    # 创建游标对象
    cursor = db.cursor()

    # 创建各省份日期与舆情的相关表
    sql = """CREATE TABLE `details` (
  `id` int(255) NOT NULL AUTO_INCREMENT,
  `update_time` datetime DEFAULT NULL COMMENT '数据最后更新时间',
  `province` varchar(255) DEFAULT NULL COMMENT '省',
  `confirm` int(255) DEFAULT NULL COMMENT '累计确诊',
  `confirm_add` int(255) DEFAULT NULL COMMENT '新增确诊',
  `confirm_now` int(255) DEFAULT NULL COMMENT '现有确诊',
  `heal` int(255) DEFAULT NULL COMMENT '累计治愈',
  `dead` int(255) DEFAULT NULL COMMENT '累计死亡',
  `dead_add` int(255) DEFAULT NULL COMMENT '新增死亡',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """
    # 执行SQL语句
    cursor.execute(sql)

except Exception as e:
    print("数据库操作失败！",e)
else:
    print("数据库操作成功！")
finally:
    if db:
        db.close()