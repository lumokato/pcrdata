import requests
from Crypto.Cipher import AES
import base64
import msgpack
import time
import csv

class WebClient:
    def __init__(self):
        self.urlroot = "https://service-kjcbcnmw-1254119946.gz.apigw.tencentcs.com/"
        self.default_headers={
            "Host": "service-kjcbcnmw-1254119946.gz.apigw.tencentcs.com",
            "Accept-Encoding": "gzip, deflate",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
            "Custom-Source": "KyoukaOfficial",
            "Content-Type": "application/json",
            "Origin": "https://kengxxiao.github.io",
            "Sec-Ch-Ua": "Chromium",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://kengxxiao.github.io/",
            "Accept-Language": "zh-CN,zh",
            "Accept": "application/json, text/javascript, */*",
            "Connection": "close"
            }
        self.conn = requests.session()
    def Callapi(self, apiurl, request):
        headers = self.default_headers
        resp = self.conn.post(url= self.urlroot + apiurl,
                        headers = headers, json = request)
        ret = eval(resp.content.decode())
        return ret["data"]

client = WebClient()

def query_page(page: int, history_time: int):
    try:
        res = client.Callapi('/page/' + str(page), {"history": history_time})
        return res
    except:
        return False

def time_date():
    time_dict = {"510": 1620594006, "511": 1620680406, "512": 1620766806, "513": 1620853206, "514": 0}
    return time_dict

def page_to_csv(date: str, page_start: int, page_end: int):
    history_time = time_date()[date]
    page_count = page_start
    while page_count < page_end:
        detail = query_page(page_count, history_time)
        if detail:
            with open('./rank/b' + date + '.csv', 'a', encoding="utf8") as csvfile:
                for line in detail:
                    data = '\"""{0}\""",{1},\"""{2}\""",{3},{4}\n'.format(line['clan_name'], line['damage'], line['leader_name'], line['leader_viewer_id'], line['rank'])
                    csvfile.write(data)
            csvfile.close()
            page_count += 1
            time.sleep(1)
        else:
            time.sleep(10)

def read_damage(date: str):
    damage = {}
    with open('./rank/b' + date + '.csv', 'r', encoding="utf8") as csvfile:
        lines = csv.reader(csvfile)
        for line in lines:
            damage[line[3]] = line[1]
        csvfile.close()
    return damage

def read_rank(date: str):
    rank = {}
    with open('./rank/b' + date + '.csv', 'r', encoding="utf8") as csvfile:
        lines = csv.reader(csvfile)
        for line in lines:
            rank[line[3]] = line[4]
        csvfile.close()
    return rank

def read_damage_id(date: str):
    damage = {}
    with open('./rank/b' + date + '.csv', 'r', encoding="utf8") as csvfile:
        lines = csv.reader(csvfile)
        for line in lines:
            damage[line[3]] = line[1]
        csvfile.close()
    return damage

def read_damage_rank(date: str):
    damage = {}
    with open('./rank/b' + date + '.csv', 'r', encoding="utf8") as csvfile:
        lines = csv.reader(csvfile)
        for line in lines:
            damage[line[4]] = line[1]
        csvfile.close()
    return damage

def rank_confirm(day: int):
    if day == 0: day1 = "412"; day2 ="413"
    elif day == 1: day1 = "413"; day2 ="414"
    elif day == 2: day1 = "414"; day2 ="415"
    rank1 = read_rank(day1)
    rank2 = read_rank(day2)
    for rank in rank2.keys():
        if rank not in rank1.keys():
            with open('./rank/b' + day2 +'.txt', 'a') as f:
                f.write(str(rank2[rank]) + '\n')
                f.close
    for rank in rank1.keys():
        if rank not in rank2.keys():
            with open('./rank/b' + day2 +'.txt', 'a') as f:
                f.write(str(rank1[rank]) + '\n')
                f.close

def dict_minus(dic1: dict, dic2:dict):
    minus_list = []
    for key in dic2.keys():
        if key in dic1.keys():
            minus_list.append(int(dic2[key]) - int(dic1[key]))
    return sorted(minus_list, reverse=True)


def clan_minus_id():
    dam1 = read_damage_id("412")
    dam2 = read_damage_id("413")
    dam3 = read_damage_id("414")
    dam4 = read_damage_id("415")
    dam5 = read_damage_id("416")
    dam_day1 = sorted(dam1.values(), reverse=True)
    dam_day2 = dict_minus(dam1, dam2)
    dam_day3 = dict_minus(dam2, dam3)
    dam_day4 = dict_minus(dam3, dam4)
    dam_day5 = dict_minus(dam4, dam5)
    clan_num = min([len(dam_day1), len(dam_day2), len(dam_day3), len(dam_day4), len(dam_day5)])
    with open('./rank/damage_byclan.csv','w', encoding="utf8") as csvfile:
        for i in range(clan_num):
            csvfile.write(dam_day1[i]+','+str(dam_day2[i])+','+str(dam_day3[i])+','+str(dam_day4[i])+','+str(dam_day5[i])+'\n')
    csvfile.close()

def clan_minus_rank():
    dam1 = read_damage_rank("412")
    dam2 = read_damage_rank("413")
    dam3 = read_damage_rank("414")
    dam4 = read_damage_rank("415")
    dam5 = read_damage_rank("416")
    dam_day1 = sorted(dam1.values(), reverse=True)
    dam_day2 = dict_minus(dam1, dam2)
    dam_day3 = dict_minus(dam2, dam3)
    dam_day4 = dict_minus(dam3, dam4)
    dam_day5 = dict_minus(dam4, dam5)
    clan_num = min([len(dam_day1), len(dam_day2), len(dam_day3), len(dam_day4), len(dam_day5)])
    with open('./rank/damage_byrank.csv','w', encoding="utf8") as csvfile:
        for i in range(clan_num):
            csvfile.write(dam_day1[i]+','+str(dam_day2[i])+','+str(dam_day3[i])+','+str(dam_day4[i])+','+str(dam_day5[i])+'\n')
    csvfile.close()

if __name__ == "__main__":
    page_to_csv("609",0,160)
    page_to_csv("610",0,160)
    # clan_minus_id()