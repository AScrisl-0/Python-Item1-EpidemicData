import traceback
import requests
import time
from datetime import datetime
from dateutil import relativedelta
import hashlib
import pymysql

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko)"
                         " Chrome/102.0.0.0 Safari/537.36",
           "Host": "api.inews.qq.com",
           "Origin": "https://news.qq.com/"}

def cal_limit_days(month=3):
    """获取三个月之前的天数month可以调节"""
    now = datetime.now()
    # 计算三个月之前的日期
    pre_date = now - relativedelta.relativedelta(months=month)
    # 计算两个月之间的天数差距
    res_date = datetime(pre_date.year,pre_date.month,1)
    # 天数差
    diff_day = (now - res_date).days
    return diff_day,res_date

def turn_to_sql_date(i,min_date:datetime,year='y',format='%Y.%m.%d'):
    """日期边界判断"""
    ds = str(i[year]) + "." + i['date']
    ds_tmp = datetime.strptime(ds,format)
    if ds_tmp < min_date:
        print("日期超过边界,跳过")
        return None,None
    return ds_tmp.strftime('%Y.%m.%d'), ds_tmp

def get_tencent_data():
    '''获取腾讯网站中的疫情数据'''
    limit_num,min_date = cal_limit_days()
    print("limit应该设置为:",limit_num)
    url = 'https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=localCityNCOVDataList,diseaseh5Shelf'
    response = requests.post(url,headers=headers)
    # 获取JSON数据
    data_all = response.json()['data']
    # H5数据
    data_h5 = data_all['diseaseh5Shelf']
    # 当日本土数据
    data_DailyReport = data_all['localCityNCOVDataList']

    # 根据日期的确诊统计和新增确诊的数量
    dayListnew_url = "https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=chinaDayListNew,chinaDayAddListNew&limit={}".format(limit_num)
    day_resp = requests.post(dayListnew_url,headers=headers)
    data_daylist = day_resp.json()['data']

    # 根据日期整理全国数据
    history = {}
    # 中国疫情每日总体情况

    for i in data_daylist['chinaDayListNew']:
        ds, _ = turn_to_sql_date(i,min_date)
        if not ds:
            continue
        history[ds] = {'confirm':i['confirm'],'heal':i['heal'],'dead':i['dead'],'confirm_now':i['nowConfirm'],'importedCase':i['importedCase']}

    # 中国疫情每日新增数据
    for i in data_daylist['chinaDayAddListNew']:
        ds, _ = turn_to_sql_date(i,min_date)
        if ds not in history.keys():
           continue

        history[ds].update({'confirm_add':i['confirm'],'heal_add':i['heal'],'dead_add':i['dead'],'importedCase_add':i['importedCase']})
    # TODO数量写入数据库
    # 插入数据库
    insert_to_history(history)

    # 详细数据
    province_at = data_h5['areaTree'][0]['children']
    for pro_info in province_at:
        print(pro_info['name'])
        # 省份名称
        province = pro_info['name']
        # 获取当天的现有确诊数据
        now_confirm = pro_info['total']['nowConfirm']
        # 更新日期
        ds_str = pro_info['date'].replace("/",'-')
        ex_pro_total = pro_info['total']
        ex_pro_today = pro_info['today']

        # 对当日省份的数据进行整合
        ex_pro_info = [ds_str,province,ex_pro_total['confirm'],ex_pro_today['confirm'],now_confirm,ex_pro_total['heal'],ex_pro_total['dead'],ex_pro_today['dead_add']]
        insert_to_detail(ex_pro_info)

        # 当日之前三个月的历史数据,港澳台没有历史数据
        if pro_info['adcode'] == '':
            continue
        pro_url = f'https://api.inews.qq.com/newsqa/v1/query/pubished/daily/list?adCode={pro_info["adcode"]}&limit={limit_num}'
        pro_resp = requests.get(pro_url,headers=headers)
        pro_date_detail = pro_resp.json()['data']
        for pro_day in pro_date_detail:
            ds,ds_date = turn_to_sql_date(pro_day,year='year',min_date=min_date)
            pro_date = [ds,pro_day['province'],pro_day['confirm'],pro_day['confirm_add'],None,pro_day['heal'],pro_day['dead'],pro_day['deadAdd']]

            insert_to_detail(pro_date)

        print(f'[{province}] 三月份的数据写入成功,等待完成下一个省份的数据爬取......')
        # 爬虫的QPS最好设置为10,否则容易封IP,具体情况依网站而定
        time.sleep(3)
def load_signature():
    '''获取网站的加密参数'''
    # 时间戳
    e = str(int(time.time()))
    a = '23y0ufFl5YxIyGrI8hWRUZmKkvtSjLQA'
    i = '123456789abcdefg'
    s1 = hashlib.sha256()
    s1.update((e + a + i + e).encode())
    qu_sign = s1.hexdigest().upper()
    # header加密
    s2 = hashlib.sha256()
    s2.update((e + "fTN2pfuisxTavbTuYVSsNJHetwq5bJvCQkjjtiLM2dCratiA" + e).encode())
    x_wif_sign = s2.hexdigest().upper()
    return x_wif_sign,qu_sign,e

def get_risk_data():
    '''获取中高风险地区的数据'''
    # 获取加密的值
    x_wif_sign,qu_sign,ts = load_signature()

    # 请求头构建
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
        "Referer": "http://bmfw.www.gov.cn/yqfxdjcx/risk.html",
        "Host": "bmfw.www.gov.cn",
        "Orign": "http://bmfw.www.gov.cn",
        "x-wif-nonce": "QkjjtiLM2dCratiA",
        "x-wif-paasid": "smt-application",
        "x-wif-signature": x_wif_sign,
        "x-wif-timestamp": ts
    }
    # 构建加密参数
    query = {
        "appId": "NcApplication",
        "key": "3C502C97ABDA40D0A60FBEE50FAAD1DA",
        "nonceHeader": "123456789abcdefg",
        "paasHeader": "zdww",
        "signatureHeader": qu_sign,
        "timestampHeader": ts
    }
    gov_url = 'http://bmfw.www.gov.cn/bjww/interface/interfaceJson'
    resp = requests.post(gov_url,headers=headers,json=query)
    if resp.status_code == 200:
        risk_data = resp.json()['data']
        utime = risk_data['end_update_time']
        utime_date = datetime.strptime(utime,"%Y-%m-%d %H时")
        utime = utime.date.strftime("%Y-%m-%d")
        # 中高风险地区的数量
        m_risk_num,h_risk_num = risk_data['mcount'],risk_data['hcount']

        insert_to_riskNum([utime,h_risk_num,m_risk_num])
        # 修改数据关于中高风险的类型显示
        h_risk = risk_data['highlist']
        m_risk = risk_data['middlelist']
        # 中高风险进行压缩,0为高风险,1为低风险
        combine_risk = zip((0,1),(h_risk,m_risk))
        risk_infos = []
        for type,rlist in combine_risk:
            type = "高风险" if type == 0 else "低风险"
            for hd in rlist:
                province = hd['province']
                city = hd['city']
                county = hd['county']
                area_name = hd['area_name']
                communitys = hd['communitys']
                for x in communitys:
                    print([utime,province,city,county,x,type])
                    risk_infos.append([utime,province,city,county,x,type])
        insert_to_riskData(risk_infos)
    else:
        print("爬虫失败,数据未变动!")


def get_conn():
    '''数据库连接'''
    db = pymysql.conect(host='localhost',user='root',password='Password123$', database='spiders',port=3306,charset='utf8')
    # 创建游标
    cursor = db.cursor()
    return db,cursor

def insert_to_history(data):
    '''全国每天的历史数据'''
    # 获取数据库的连接和游标
    db,cursor = get_conn()
    print(f"{time.asctime()}:开始更新历史数据...")
    try:
        sql = 'insert into history values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        sql_query = 'select confirm from history where ds=%s'
        for k ,v in data.items():
            if not cursor.execute(sql_query,k):
                cursor.execute(sql,[k,v.get('confirm'),v.get('confirm_add'),
                                    v.get('confirm_now'),v.get('heal'),
                                    v.get('heal_add'),v.get('dead'),v.get('dead_add'),
                                    v.get('importedCase'),v.get('importedCase_add')])
                print(f'[history] | [china] | {k} 记录写入成功！')
        db.commit()  # 提交事物
        print(f'{time.asctime()}：历史数据更新完毕...')
    except:
        # 异常进行回滚
        db.rollback()
        # 打印错误的信息
        traceback.print_exc()

    finally:
        cursor.close()
        db.close()

def insert_to_detail(data):
    '''每个省份每天的数据'''
    db,cursor = get_conn()
    try:
        sql = 'insert into details(upodate_time,province,confirm,confirm_add,confirm_now,heal,dead,dead_add) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        sql_query = 'select confirm from details where province=%s and update_time=%s'
        if not cursor.execute(sql_query, [data[1],data[0]]):
            print(f'写入[{data[1]}] | [{data[0]}] 成功!')
            cursor.execute(sql,data)
        db.commit()  # 提交事物
    except:
        # 异常进行回滚
        db.rollback()
        # 打印错误的信息
        traceback.print_exc()

    finally:
        cursor.close()
        db.close()

def insert_to_riskNum(data):
    '''更新当天中高风险地区的数量'''
    conn, cursor = get_conn()
    try:
        sql = "insert into risknum(update_time,hnum,mnum) values(%s,%s,%s)"
        # 对比当前最大时间戳
        sql_query = "select hnum from risknum where update_time=%s"
        if not cursor.execute(sql_query, data[0]):
            print(f'{time.asctime()}：开始更新风险地区的数量')
            cursor.execute(sql, data)
            print(f'{time.asctime()}：完成风险地区的数量的更新')
            conn.commit()  # 记得提交事务~
        else:
            print(f'{time.asctime()}: 当前风险地区数量已是最新数据！')
    except:
        traceback.print_exc()
        conn.rollback()
    finally:
        conn.close()
        cursor.close()


def insert_to_riskData(data):
    '''更新当天中高风险地区的数量'''
    conn, cursor = get_conn()
    try:
        sql = "insert into risk_area(end_update_time,province,city,county,address,type) values(%s,%s,%s,%s,%s,%s)"
        # 对比当前最大时间戳
        sql_query = 'select %s=(select end_update_time from risk_area order by id desc limit 1)'
        cursor.execute(sql_query, data[0][0])  # 传入最新时间戳
        if not cursor.fetchone()[0]:
            for item in data:
                cursor.execute(sql, item)
                print('成功写入：', item)
            conn.commit()  # 记得提交事务
        else:
            print(f'{time.asctime()}: 当前地区信息已是最新数据！')
    except:
        traceback.print_exc()
        conn.rollback()
    finally:
        conn.close()
        cursor.close()

if __name__ =='__main__':
    get_tencent_data()
    get_risk_data()