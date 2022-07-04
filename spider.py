import pandas as pd
import pymysql

conn = pymysql.connect(host='localhost',user='root',password='Password123$',database='spiders',port=3306)

df = pd.read_sql(
    "select confirm_now from details where update_time=(select update_time from details order by update_time desc limit 1)",
    con=conn)
data = df['confirm_now']
# print(df)
# print(data)
# print(type(data))
bins = [[0,100],[100,200],[200,300000],[300000,4000000]]
# data = df.value_counts() /df.value_counts().sum()
# etmpy = []
# for i in data:
#     print(i)
test = pd.cut(data,bins,right=False)
print(test)

# print(data)
# data1 = df.groupby('confirm_now')(lambda x : [0<x<100])
# print(type(data))

# date1=df.groupby('confirm').count()
