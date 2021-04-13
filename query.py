from PCRClient import PCRClient
import time, random
import binascii
import csv, os
import account as ac

client = PCRClient(ac.viewer_id)
client.login(ac.uid, ac.access_key)

#查询指定id的用户信息
def query_id(viewer_id: int):
    try:
        res = client.Callapi('/profile/get_profile', {
            'target_viewer_id': viewer_id
        })['user_info']
        return res
    except KeyError:
        return False

# 查询公会内成员信息，并保存到指定文件中
def query_clan_members(clan_id: int, outpath):
    try:
        members = client.Callapi('/clan/others_info', {
                    'clan_id': clan_id
                })['clan']['members']
        for mem in members:
            res0 = client.Callapi('/profile/get_profile', {
                'target_viewer_id': int(mem['viewer_id'])
            })['user_info']
            data0 = '{0},{1},{2},{3},{4},{5},{6},{7}\n'.format(res0['user_name'], res0['viewer_id'], res0['team_level'], res0['total_power'], res0['arena_group'], res0['arena_rank'], res0['grand_arena_group'], res0['grand_arena_rank'])
            f = open(outpath,'a')
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
            f = open(outpath, 'a', encoding='utf8')
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
    while walk_id < 44000:
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
    os.rename(filename, filename + '.bak')
    walk_order = 1
    with open(filename + '.bak', 'r', encoding="utf8") as csvfile:
        lines = csv.reader(csvfile)
        for line in lines:
            if query_clan(int(line[1]), filename):
                if walk_order % 20 == 0:
                    time.sleep(random.randint(8,12))
                    print('Clan working on ' + str(walk_order))
                walk_order += 1
                time.sleep(0.2)
            else:
                time.sleep(20)

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
        with open("clan_top" + str(endrank) + '.csv', 'a', encoding="utf8") as csvfile:
            for detail in pagedata:
                csvfile.write('\"""{0}\""",{1},{2}\n'.format(detail['clan_name'], detail['rank'], detail['grade_rank']))
    return False


if __name__ == "__main__":
    #walk_clan(43280)
    #refresh_clan('clan_top.csv')
    #query_clan_members(5645, 'members.csv')
    query_clan_top(300)
