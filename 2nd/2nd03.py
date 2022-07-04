import pymysql


db =None

try:
    db = pymysql.connect(host='localhost',user='root',password='Password123$',database='spiders',port=3306)
    # 创建游标对象
    cursor = db.cursor()

    # 创建中高风险地区数据表
    sql = """CREATE TABLE `risk_area` (
`id` int(10) PRIMARY KEY AUTO_INCREMENT,
`end_update_time` varchar(255) COMMENT '数据最后更新时间',
`province` varchar(255) COMMENT '省',
`city` varchar(255) COMMENT '市',
`county` varchar(255) COMMENT '县',
`address` varchar(255) COMMENT '详细地址',
`type` varchar(10) COMMENT '风险类型'
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
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