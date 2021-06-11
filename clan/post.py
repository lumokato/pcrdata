import PCRClient as cli
import time, random
import binascii
import csv, os
import account as ac

client = cli.PCRClient(ac.viewer_id)
client.login(ac.uid, ac.access_key)

def givegift(viewer_id: int):
    try:
        res = client.Callapi('room/give_gift', {
            'unit_id': 107801, 'item_id': 50003, 'item_num': 8, 'current_item_num': 2165
        })
        return res
    except KeyError:
        return False


def storycheck(viewer_id: int, storyid: int):
    try:
        res = client.Callapi('/story/check', {
            'story_id': storyid
        })
        time.sleep(2)
        res = client.Callapi('/story/start', {
            'story_id': storyid
        })
        return res
    except KeyError:
        return False


#a = givegift(ac.viewer_id)
aa = storycheck(ac.viewer_id, 2001005)
#aa = storycheck(ac.viewer_id, 2001004)
print(aa)
