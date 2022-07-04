from flask import Flask, render_template, jsonify
import pandas as pd
import pymysql
import re
import traceback
from calendar import monthrange
from dateutil import relativedelta
from datetime import datetime

app = Flask(__name__)


def get_conn():
    """数据库连接"""
    conn = pymysql.connect(host="localhost", user="root", password="Password123$", db="spiders", charset='utf8')
    # 创建游标
    cursor = conn.cursor()
    return conn, cursor


def close_conn(conn, cursor):
    """用于关闭数据库"""
    conn.close()
    cursor.close()


def query(sql, *args):
    '''一个通用的查询函数'''
    conn, cursor = get_conn()
    cursor.execute(sql, args)
    res = cursor.fetchall()
    close_conn(conn, cursor)
    return res


@app.route('/')
def index():  # 首页页面
    conn, cursor = get_conn()
    # 获取日期最新的记录
    sql = "SELECT confirm_add,heal_add,confirm_now,confirm from history ORDER BY ds desc LIMIT 1"
    res = query(sql)[0]
    data = {
        'confirm_add': res[0],
        'heal_add': res[1],
        'confirm_now': res[2],
        'confirm': res[3]}
    close_conn(conn, cursor)
    return render_template('index.html', today_data=data)


@app.route('/get_risk_info')
def get_risk_info():
    '''获取中高风险地区'''
    sql1 = """
           select * from risk_area 
           where end_update_time=(
               select end_update_time 
               from risk_area 
               order by end_update_time desc limit 1)
       """
    sql2 = """
           select hnum, mnum from risknum 
           where update_time=(
               select update_time from risknum 
               order by update_time desc limit 1);
       """

    res1 = query(sql1)
    res2 = query(sql2)
    updata_time = res1[0][1]
    risk = []
    detail = []
    # 中高风险的数量
    risk_num = {
        'high_num': res2[0][0],
        'medium_num': res2[0][1],
    }
    for a, b, c, d, e, f, g in res1:  # 中高风险地区信息
        risk.append(g)  # 风险类型
        detail.append(f"{c}\t{d}\t{e}\t{f}")

    return jsonify({"update_time": updata_time, "risk_num": risk_num,
                    "detail": detail, "risk": risk})


@app.route('/get_province_confirm')
def get_province_confirm():
    '''省份的现存确诊TOP5'''
    sql = '''
            select province, confirm_now from details 
            where update_time = (
                select update_time from details 
                order by update_time desc limit 1) 
            order by confirm_now desc limit 5;
        '''
    res = query(sql)
    cityList = []
    cityData = []
    for i in range(5):
        cityList.append(res[i][0])
        cityData.append(res[i][1])

    return jsonify({"cityList": cityList, "cityData": cityData})


def parse_date(df, columns):
    '''如果DataFrame中有datetime对象，就启用这个方法'''
    # 隔离出年月日
    df_tmp = df.copy()
    df_tmp[columns] = pd.to_datetime(df[columns])
    df_tmp['year'] = df_tmp[columns].apply(lambda x: x.year)
    df_tmp['month'] = df_tmp[columns].apply(lambda x: x.month)
    df_tmp['day'] = df_tmp[columns].apply(lambda x: x.day)
    return df_tmp


@app.route('/get_heal_dead')
def get_heal_dead():
    '''死亡和治愈折线图'''
    conn = get_conn()[0]
    df = pd.read_sql('select ds,dead,heal,dead_add,heal_add from history', con=conn)
    df = df.dropna()  # 去除无效值
    df_date = parse_date(df, 'ds')
    # 统计各年和各月的死亡、治愈、新增死亡、新增治愈
    g = df_date.groupby(['year', 'month'])
    # 新增的数据进行累加
    deadAddList = g['dead_add'].sum()
    healAddList = g['heal_add'].sum()
    # 累加的数据本来就是一个最终的数据，所以需要取每个月最后一天的数据
    dateList = list(deadAddList.keys())
    dateList = list(map(lambda x: f"{x[0]}-{x[1]}", dateList))
    # 每个数据整理成列表
    deadAddList = deadAddList.tolist()
    healAddList = healAddList.tolist()
    deadList = []
    healList = []
    for date in dateList:
        year, month = date.split("-")
        # 获取当月的range值
        _, end = monthrange(int(year), int(month))
        for i in range(end, 0, -1):  # 倒着回去获取月份数据，直到到当月最后一条记录位置
            try:
                # print(f'当前月份为{month} | 日期为：{i}')
                ds = '-'.join([year, month, str(i)])
                res = df[df['ds'] == ds]
                if res.empty:  # 如果是空数据集，那就证明还没找到当月最后一条记录
                    continue
                deadList.append(res['dead'].tolist()[0])
                healList.append(res['heal'].tolist()[0])
            except:
                traceback.print_exc()
                continue
            else:
                break
    return jsonify({'dateList': dateList,
                    'addData': {'deadAdd': deadAddList, 'healAdd': healAddList},
                    'sumData': {'dead': deadList, 'heal': healList}})


@app.route('/get_two_month')
def get_two_month():
    '''近两个月新增趋势（本土和境外）'''
    conn = get_conn()[0]
    now = datetime.now()
    # 计算两个月之间的天数
    pre_date = now - relativedelta.relativedelta(months=2)
    # 计算两个月之间天数差距
    res_date = datetime(pre_date.year, pre_date.month, 1)
    # 最终需要获取的天数信息
    df = pd.read_sql('select ds,confirm_add,importedCase_add from history', con=conn)
    df = df.dropna()  # 去除无效值
    df_date = parse_date(df, 'ds')
    df_tmp = df_date[df_date['ds'] >= res_date]
    dateList = df_tmp.ds.astype("str").tolist()
    confirmAddList = df_tmp.confirm_add.tolist()
    importedCaseList = df_tmp.importedCase_add.tolist()
    return jsonify({
        'dateList': dateList,
        'confirmAddList': confirmAddList,
        'importedCaseList': importedCaseList})


@app.route('/get_map_data')
def get_map_data():
    '''各个省份每个月新增确诊总量/新增死亡总量/新增治愈总量'''
    conn = get_conn()[0]
    df = pd.read_sql("select update_time, confirm_add, province from details", con=conn)
    df.update_time = df.update_time.dt.to_period('M')
    # 透视表：获取数据库中根据月份总结的新增确诊数据
    df_tmp = pd.pivot_table(df, index='province',
                            columns='update_time',
                            values='confirm_add', aggfunc='sum')
    # 港澳台没有历史数据，所以只能做横向的na值填充了
    df_tmp = df_tmp.fillna(axis=1, method='bfill')
    year_month = [str(x) for x in df_tmp.columns]
    # 列表中的字列表就是每个月份的columns代表的数据
    confirm_add = [df_tmp[col].values.tolist() for col in year_month]
    return jsonify({
        'year_month': year_month,
        'province': df_tmp.index.to_list(),
        'confirm_add': confirm_add
    })


@app.route('/get_death_rate')
def get_death_rate():
    print("work normal")
    conn = get_conn()[0]
    df = pd.read_sql("select ds,dead,confirm from history where ds=(select ds from history order by ds desc limit 1)",
                     con=conn)
    dead_num = int(df.iloc[:,1])
    confirm_num = int(df.iloc[:,2])
    dead_rate = (dead_num / confirm_num)*100
    dead_rate = round(dead_rate, 3)
    print(dead_num, confirm_num, dead_rate)
    return jsonify({
        'dead': str(dead_num),
        'confirm': str(confirm_num),
        'dead_rate': str(dead_rate)
    })

@app.route('/get_now_confirm')
def get_now_confirm():
    conn = get_conn()[0]
    df = pd.read_sql(
        "select confirm_now from details where update_time=(select update_time from details order by update_time desc limit 1);",
        con=conn)
    bins = [0, 100, 200, 300000, 4000000]
    labels = ['[0,100)', '[100,200)', '[200,300000)', '[300000,4000000)']
    df['group'] = pd.cut(df['confirm_now'], bins=bins, labels=labels, right=False)
    df1 = df.groupby(by='group').count().values.tolist()
    values = []
    for i in range(len(df1)):
        values.append(df1[i][0])

    return jsonify([{'value': values[i], 'name': labels[i]} for i in range(len(values))])



if __name__ == '__main__':
    app.run()
