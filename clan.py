from PCRClient import PCRClient, ApiException
from os.path import dirname, join, exists
import time, random

client = PCRClient(1314202001949)
client.login("2020081016480401600000", "204ea6141f2eed91eb4a3df3d2c1b6e7")

def query_id(viewer_id: int):
    try:
        res = client.Callapi('/profile/get_profile', {
            'target_viewer_id': viewer_id
        })['user_info']
        return res
    except ApiException as e:
        return '查询出错，{e}'

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
    except ApiException as e:
        f = open(outpath,'a')
        f.write('查询到公会' + clan_id + '时出错，错误信息为' + '{e}')
        f.close()
        return False

def query_clan(clan_id: int, outpath):
    try:
        msg = client.Callapi('/clan/others_info', {
                'clan_id': clan_id
            })
        if 'clan' in msg:
            detail = msg['clan']['detail']
            data = '{0},{1},{2},{3},{4},{5},{6},{7}\n'.format(detail['clan_name'], detail['clan_id'], detail['leader_name'], detail['join_condition'], detail['member_num'], detail['activity'], detail['grade_rank'], detail['current_period_ranking'])
            f = open(outpath,'a')
            f.write(data)
            f.close()
            return True
        elif 'message' in msg['server_error']:
            if msg['server_error']['message'] == '此行会已解散。\\n返回标题界面。':
                return True
    except KeyError:
        f = open(outpath,'a')
        f.write('查询到公会' + str(clan_id) + '时出错\n')
        f.close()
        return False

def walk_clan(start_id: int):
    walk_id = start_id
    while query_clan(walk_id, 'clanx.csv'):
        if walk_id % 20 == 0:
            time.sleep(random.randint(8,12))
        walk_id += 1
        time.sleep(0.2)
    f = open(str(walk_id) + '.a', 'w')
    f.write(' ')
    f.close

if __name__ == "__main__":
    walk_clan(50)
