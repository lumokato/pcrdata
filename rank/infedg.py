import requests
from Crypto.Cipher import AES
import base64
import msgpack
import time
import csv

class WebClient0:
    def __init__(self):
        self.urlroot = "https://api.infedg.xyz/"
        self.default_headers={
            "Host": "api.infedg.xyz",
            "Accept-Encoding": "gzip, deflate",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
            "Custom-Source": "Kyaru",
            "Content-Type": "application/json",
            #"Origin": "https://kyaru.infedg.xyz",
            "Sec-Ch-Ua": "Chromium",
            "Sec-Fetch-Site": "same-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            #"Referer": "https://kyaru.infedg.xyz/",
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

client = WebClient0()

def query_date(date: str):
    try:
        res = client.Callapi('/search/rank/', {"filename":"qd/1/20210"+date+"0530", "page":0, "page_limit":10})
        return res
    except:
        return False

def page_to_csv(date: str):
    detail = query_date(date)
    if detail:
        with open('./rank/qd' + date + '.csv', 'a', encoding="utf8") as csvfile:
            for line in detail:
                data = '\"""{0}\""",{1},\"""{2}\""",{3},{4}\n'.format(line['clan_name'], line['damage'], line['leader_name'], line['grade_rank'], line['rank'])
                csvfile.write(data)
        csvfile.close()

def walk_date():
    date_list = ["412", "413", "414", "415"]
    for date in date_list:
        page_to_csv(date)

def read_damage_grade_rank(date: str):
    damage = {}
    with open('./rank/qd' + date + '.csv', 'r', encoding="utf8") as csvfile:
        lines = csv.reader(csvfile)
        for line in lines:
            damage[line[3]] = line[1]
        csvfile.close()
    return damage

def read_detail(date: str):
    datail = {}
    with open('./rank/qd' + date + '.csv', 'r', encoding="utf8") as csvfile:
        lines = csv.reader(csvfile)
        for line in lines:
            datail[line[4]] = [line[3], line[0], line[2]]
        csvfile.close()
    return datail

def minus_damage():
    dam1 = read_damage_grade_rank("412")
    dam2 = read_damage_grade_rank("413")
    dam3 = read_damage_grade_rank("414")
    dam4 = read_damage_grade_rank("415")
    dam5 = read_damage_grade_rank("416")
    detail_clan = read_detail("416")
    detail_damage = {}
    for clan in dam5.keys():
        if clan in dam1.keys() and clan in dam2.keys() and clan in dam3.keys() and clan in dam4.keys():
            detail_damage[clan] = [int(dam1[clan]), int(dam2[clan])-int(dam1[clan]), int(dam3[clan])-int(dam2[clan]), int(dam4[clan])-int(dam3[clan]), int(dam5[clan])-int(dam4[clan])]
    with open('./rank/damage_qd.csv', 'a', encoding="utf8") as csvfile:
        for clan_rank in detail_clan.keys():
            if detail_clan[clan_rank][0] in detail_damage.keys():
                clan_grade_rank = detail_clan[clan_rank][0]
                csvfile.write('{0},{1},{2},{3},{4},{5},{6},{7}\n'.format(clan_rank, detail_clan[clan_rank][1], detail_clan[clan_rank][2], detail_damage[clan_grade_rank][0], detail_damage[clan_grade_rank][1], detail_damage[clan_grade_rank][2], detail_damage[clan_grade_rank][3], detail_damage[clan_grade_rank][4]))
            else:
                continue

def find_index(finder:int, lister: list):
    index = 0
    while index < 1500:
        if finder < lister[index]:
            index += 1
        else:
            break
    return index

def find_rank():
    b_day1 = []
    b_day2 = []
    b_day3 = []
    b_day4 = []
    qd_data = []
    with open('./rank/damage_byrank.csv', 'r', encoding="utf8") as csvfile:
        for line in csv.reader(csvfile):
            b_day1.append(int(line[0]))
            b_day2.append(int(line[1]))
            b_day3.append(int(line[2]))
            b_day4.append(int(line[3]))
        csvfile.close()
    with open('./rank/damage_qd.csv', 'r', encoding="utf8") as csvfile:
        for line in csv.reader(csvfile):
            qd_data.append('{0},{1},{2},{3},{4},{5},{6}\n'.format(line[0], line[1], line[2], find_index(int(line[3]), b_day1), find_index(int(line[4]), b_day2), find_index(int(line[5]), b_day3), find_index(int(line[6]), b_day4)))
        csvfile.close()
    with open('./rank/rank_qd2.csv', 'w', encoding="utf8") as csvfile:
        for line in qd_data:
            csvfile.write(line)
        csvfile.close()

if __name__ == "__main__":
    minus_damage()