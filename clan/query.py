import PCRClient as cli
import time, random
import binascii
import csv, os
import account as ac
import pandas as pd
import json

client = cli.PCRClient(ac.viewer_id)
client.login(ac.uid, ac.access_key)

#查询指定id的用户信息
def query_id(viewer_id: int):
    try:
        res = client.Callapi('/profile/get_profile', {
            'target_viewer_id': viewer_id
        })#['user_info']
        return res
    except KeyError:
        return False

# 查询公会内成员信息，并保存到指定文件中
def query_clan_members(clan_id: int, clan_name:str, outpath):
    try:
        members = client.Callapi('/clan/others_info', {
                    'clan_id': clan_id
                })#['clan']['members']
        for mem in members:
            res0 = client.Callapi('/profile/get_profile', {
                'target_viewer_id': int(mem['viewer_id'])
            })['user_info']
            data0 = '\"""{0}\""",{1},{2},{3},{4},{5},{6},{7},\"""{8}\""",{9}\n'.format(res0['user_name'], res0['viewer_id'], res0['team_level'], res0['total_power'], res0['arena_group'], res0['arena_rank'], res0['grand_arena_group'], res0['grand_arena_rank'], clan_name, clan_id)
            f = open('./clan/' + outpath,'a')
            f.write(data0)
            f.close()
        return True
    except KeyError:
        return False

# 查询公会信息，并保存到指定文件中
def query_clan(clan_id: int, outpath):
    try:
        msg = client.Callapi('/clan/others_info', {
                'clan_id': clan_id
            })
        if 'clan' in msg:
            detail = msg['clan']['detail']
            data = '\"""{0}\""",{1},\"""{2}\""",{3},{4},{5},{6},{7}\n'.format(detail['clan_name'], detail['clan_id'], detail['leader_name'], detail['join_condition'], detail['member_num'], detail['activity'], detail['grade_rank'], detail['current_period_ranking'])
            f = open('./clan/' + outpath, 'a', encoding='utf8')
            f.write(data)
            f.close()
            return True
        elif 'message' in msg['server_error']:
            if msg['server_error']['message'] == '此行会已解散。\\n返回标题界面。':
                return True
    except binascii.Error:
        return False

# 获取从start_id开始的公会信息
def walk_clan(start_id: int):
    walk_id = start_id
    while walk_id < 46000:
        if query_clan(walk_id, 'clan_full.csv'):
            if walk_id % 20 == 0:
                time.sleep(random.randint(8,12))
                print('Clan working on ' + str(walk_id))
            walk_id += 1
            time.sleep(0.2)
        else:
            time.sleep(20)

#更新公会信息
def refresh_clan(filename):
    os.rename('./clan/' + filename, './clan/' + filename + '.bak')
    walk_order = 1
    with open('./clan/' + filename + '.bak', 'r', encoding="utf8") as csvfile:
        lines = csv.reader(csvfile)
        for line in lines:
            if query_clan(int(line[1]), filename):
                if walk_order % 20 == 0:
                    time.sleep(random.randint(8,12))
                    print('Clan working on ' + str(walk_order))
                walk_order += 1
                time.sleep(0.2)
            else:
                print("false")
                time.sleep(1)

#查询会战排名页数
def get_page_status(page: int):
    temp = client.Callapi('clan_battle/period_ranking', {'clan_id': ac.clan_id, 'clan_battle_id': -1, 'period': -1, 'month': 0, 'page': page, 'is_my_clan': 0, 'is_first': 1})
    if 'period_ranking' not in temp:
        client.login(ac.uid, ac.access_key)
        temp = client.Callapi('clan_battle/period_ranking', {'clan_id': ac.clan_id, 'clan_battle_id': -1, 'period': -1, 'month': 0, 'page': page, 'is_my_clan': 0, 'is_first': 1})
    return temp['period_ranking']

#查询当前会战前排工会排名
def query_clan_top(endrank: int):
    for page in range(int(endrank/10)):
        pagedata = get_page_status(page)
        with open('./clan/clan_top' + str(endrank) + '.csv', 'a', encoding="utf8") as csvfile:
            for detail in pagedata:
                csvfile.write('\"""{0}\""",{1},{2}\n'.format(detail['clan_name'], detail['rank'], detail['grade_rank']))
    return False

def query_top_members():
    dict_id = {}
    with open('./clan/clan_top.csv', 'r', encoding="utf8") as csvfile:
        lines = csv.reader(csvfile)
        for line in lines:
            if int(line[7]) < 151 and int(line[7]) > 0:
                dict_id[int(line[7])] = [line[0], int(line[1])]
    for rank in range(1,151):
        try:
            query_clan_members(dict_id[rank][1], dict_id[rank][0], 'members_top.csv')
            time.sleep(2)
        except:
            time.sleep(10)

def query_top_members_extra():
    dict_id = {}
    list_clanid = []
    with open('./clan/clan_top.csv', 'r', encoding="utf8") as csvfile:
        lines = csv.reader(csvfile)
        for line in lines:
            if int(line[7]) < 151 and int(line[7]) > 0:
                dict_id[int(line[7])] = [line[0], int(line[1])]
        csvfile.close()
    with open('./clan/members_top.csv', 'r') as csvfile:
        lines = csv.reader(csvfile)
        for line in lines:
            if int(line[9]) not in list_clanid:
                list_clanid.append(int(line[9]))
    for rank in range(1,151):
        try:
            if dict_id[rank][1] not in list_clanid:
                    query_clan_members(dict_id[rank][1], dict_id[rank][0], 'members_top.csv')
                    time.sleep(2)
        except KeyError:
            print(rank)

def search_members():
    data = pd.read_csv("./clan/search.csv",encoding = "utf8")
    for i in range(data['viewer_id'].size):
        try:
            res = client.Callapi('/profile/get_profile', {'target_viewer_id': int(data['viewer_id'][i])})
        except:
            time.sleep(10)
            client.login(ac.uid, ac.access_key)
            res = client.Callapi('/profile/get_profile', {'target_viewer_id': int(data['viewer_id'][i])})
        uinfo = res['user_info']
        data.loc[i] = [uinfo['user_name'],uinfo['viewer_id'],uinfo['team_level'],uinfo['total_power'],uinfo['arena_group'],uinfo['arena_rank'],uinfo['grand_arena_group'],uinfo['grand_arena_rank'],res['clan_name']]
        time.sleep(1)
    data.to_csv('./clan/search_new.csv', index=False, encoding="utf8")

def read_json():
    data = json.load('./unpack/arena.json')
    print('a')

def query_test():
    res = client.Callapi('/clan/chat_info_list', {'clan_id': 43746, 'start_message_id': 0, 'search_date': '2099-12-31', 'direction': 1, 'count': 10, 'wait_interval': 3, 'update_message_ids': []})
    print(res)

if __name__ == "__main__":
    #walk_clan(43598)
    #refresh_clan('clan_top.csv')
    #query_clan_members(3, "a", 'members.csv')
    #query_clan_top(200)
    #query_top_members_extra()
    query_id(1262611243590)
    #get_page_status(1)
    #read_json()
    #search_members()
    #query_test()
