from json import load, dump
from PCRClient import PCRClient, ApiException
from os.path import dirname, join, exists

client = PCRClient(1314202001949)
client.login("2020081016480401600000", "204ea6141f2eed91eb4a3df3d2c1b6e7")

def query_id(id: str):
    res = client.Callapi('/profile/get_profile', {
            'target_viewer_id': int(id)
        })['user_info']
    return res

def query_clan_members(id: str, outpath):
    try:
        members = client.Callapi('/clan/others_info', {
                    'clan_id': int(id)
                })['clan']['members']
        for mem in members:
            res0 = client.Callapi('/profile/get_profile', {
                'target_viewer_id': int(mem['viewer_id'])
            })['user_info']
            data0 = '{0},{1},{2},{3},{4},{5},{6},{7}\n'.format(res0['user_name'], res0['viewer_id'], res0['team_level'], res0['total_power'], res0['arena_group'], res0['arena_rank'], res0['grand_arena_group'], res0['grand_arena_rank'])
            f = open(outpath,'a')
            f.write(data0)
            f.close()
        return 0
    except KeyError:
        return 0
def query_clan(id:str, outpath):
    try:
        detail = client.Callapi('/clan/others_info', {
                'clan_id': int(id)
            })['clan']['detail']
        data = '{0},{1},{2},{3},{4},{5},{6},{7}\n'.format(detail['clan_name'], detail['clan_id'], detail['leader_name'], detail['join_condition'], detail['member_num'], detail['activity'], detail['grade_rank'], detail['current_period_ranking'])
        f = open(outpath,'a')
        f.write(data)
        f.close()
        return 0
    except KeyError:
        return 0


if __name__ == "__main__":
    for clan in [40971]:
        query_clan(clan, 'clan.csv')
        query_clan_members(clan, 'members.csv')
