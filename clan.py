from PCRClient import PCRClient, ApiException
from os.path import dirname, join, exists
import time, random
import binascii
import pandas
import csv

# client = PCRClient(1314202001949) //佑树
# client.login("2020081016480401600000", "204ea6141f2eed91eb4a3df3d2c1b6e7")
client = PCRClient(1223950737906)
client.login("2020061221263800100000", "d145b29050641dac2f8b19df0afe0e59")
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

# 查询公会信息，并保存到指定文件中
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
    except binascii.Error:
        return False

# 获取从start_id开始的公会信息
def walk_clan(start_id: int):
    walk_id = start_id
    while walk_id < 44000:
        if query_clan(walk_id, 'clan.csv'):
            if walk_id % 20 == 0:
                time.sleep(random.randint(8,12))
                print('Clan working on ' + str(walk_id))
            walk_id += 1
            time.sleep(0.2)
        else:
            time.sleep(20)

# 拼接不同文件内的公会信息
def add_walk_data():
    rows = {}
    for i in range(1,5):
        with open('clan'+str(i)+'.csv', 'r', encoding="utf8") as f:
            reader = csv.reader(f)
            for row in reader:
                rows[int(row[1])] = ['"%s"'%row[0], row[1], '"%s"'%row[2], row[3], row[4], row[5], row[6], row[7]]
    with open('full.csv','w', newline='', encoding="utf8") as csvfile:
        writer  = csv.writer(csvfile)
        for row in sorted(rows):
             writer.writerow(rows[row])

if __name__ == "__main__":
    #walk_clan(43216)
    query_clan(14495, 'members.csv')
    #add_walk_data()