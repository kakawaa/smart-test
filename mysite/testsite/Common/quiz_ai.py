import random
import requests
import time
import threading

# 百人场 = 18
# 2人一题 = 2
# 2人多题 = 5
# 6人一题 = 3
# 6人多题 = 4
# 新手场 = 暂时先不做
base_url = 'http://47.74.180.115:8001/api/game-quiz'
ai_all_win = 0

def join(battle_id,uid):
    # 百人场chip不为fee
    if battle_id == '18':
        chip = 'chip2'
    else:
        chip = 'fee'
    url = base_url + "/battle/join?" \
                     "sign=n_e_m_o" \
                     "&uid={}" \
                     "&debug=fatmore" \
                     "&anm=vgame" \
                     "&subanm=quizboss" \
                     "&battle_id={}" \
                     "&chip={}&nickname=fatmore&avatar=i%20dont%20known" \
                     "&s_time={}".format(uid,battle_id,chip,int(time.time()))
    response = requests.request("GET", url).json()
    match_id = response['origin']['match_id']
    print('加入比赛,比赛id为：',match_id)
    return match_id

def perform(battle_id,uid,match_id):
    print(match_id)
    url = base_url + '/battle/perform?sign=n_e_m_o&' \
                     'uid={}&debug=fatmore&anm=vgame' \
                     '&battle_id={}' \
                     '&subanm=quizboss&' \
                     's_time={}' \
                     '&match_id={}'.format(uid,battle_id,int(time.time()),match_id)
    try:
        response = requests.request("GET", url).json()
        status = response['origin']['perform_data']['status']
        response_match_id = response['origin']['perform_data']['match_id']
        print(response_match_id)
        question_id = response['origin']['perform_data']['question_id']
        if response_match_id != match_id:
            status = 'waiting next match'
        print('比赛id', match_id, '的状态为：', status, '问题id是:', question_id)
    except:
        status = '请求失败'
        question_id = ''
        print('比赛id', match_id, '的状态为：', status, '问题id是:', question_id)
    return status,question_id

def answer(uid,match_id,question_id):
    answer = random.randint(1,4)
    print('比赛id', match_id, '问题id是:', question_id, '随机的答案为：',answer)
    url = base_url + '/battle/answer?sign=n_e_m_o' \
                     '&uid={}' \
                     '&debug=fatmore&anm=vgame' \
                     '&question_id={}' \
                     '&subanm=quizboss' \
                     '&match_id={}' \
                     '&answer={}&' \
                     's_time={}'.format(uid,question_id,match_id,answer,int(time.time()))
    response = requests.request("GET", url).json()
    status = response['status']
    if status == 1:
        return True
    else:
        return False

def get_bingo(uid,match_id,question_id):
    url = base_url + '/battle/get_answer_result?sign=n_e_m_o' \
          '&uid={}' \
          '&debug=fatmore' \
          '&subanm=quizboss' \
          '&match_id={}' \
          '&question_id={}' \
          '&anm=vgame&s_time={}'.format(uid,match_id,question_id,int(time.time()))
    response = requests.request("GET", url).json()
    print(response)
    answer = response['origin']['answer']
    print('正确答案是：',answer)
    uids_opt = 'uids_opt' + str(answer)
    win_uid_list = response['origin']
    if uids_opt in win_uid_list:
        print('bingo的用户有：',win_uid_list[uids_opt])
        if len(win_uid_list[uids_opt]) != 0:
            for win_uid in win_uid_list[uids_opt]:
                if win_uid['uid'] != uid:
                    bingo = True
                    break
                else:
                    bingo = False
        else:
            bingo = False
    else:
        bingo = False
    print('ai答题结果为',bingo)
    return bingo


def get_win(uid,match_id):
    url = base_url + "/battle/get_result?sign=n_e_m_o&" \
                     "uid={}" \
                     "&debug=fatmore&subanm=quizboss" \
                     "&match_id={}" \
                     "&anm=vgame" \
                     "&s_time={}".format(uid,match_id,int(time.time()))
    response = requests.request("GET", url).json()
    player_list = response['origin']['player_list']
    for player in player_list:
        if player['uid'] == uid:
            prize = player["prize"]
            if prize > 0:
                ai_win = False
                print("AI输了")
            else:
                ai_win = True
                print("AI胜出")
    return ai_win

def one_run(battle_id,uid,question_num):
    # 单题的模式，只看bingo数
    global ai_all_win
    all_question = 1
    match_id = join(battle_id,uid)
    answered = 0
    show_answered = 0
    while True:
        if all_question <= question_num:
            print('第',all_question,"题")
            status, question_id = perform(battle_id,uid, match_id)
            if status == 'waiting next match':
                time.sleep(3)
                continue
            elif status == 'answer':
                print('状态为answer')
                if answered == 0:
                    answer(uid, match_id, question_id)
                    answered = 1
                    show_answered = 0
            elif status == 'show_answer':
                print('状态为show_answer')
                if show_answered == 0:
                    if get_bingo(uid, match_id, question_id):
                        ai_all_win += 1
                    answered = 0
                    show_answered = 1
                    all_question += 1
            elif status == 'end':
                print('end')
                match_id = join(battle_id,uid)
            time.sleep(3)
        else:
            break
    return

def more_run(battle_id,uid,match_num):
    # 多题的比赛看 输赢
    global ai_all_win
    all_match = 1
    match_id = join(battle_id,uid)
    print('第 1 场比赛')
    answered = 0
    while True:
        if all_match <= match_num:
            status, question_id = perform(battle_id,uid,match_id)
            if status == 'answer':
                print('状态为answer')
                if answered == 0:
                    answer(uid,match_id,question_id)
                    answered = 1
            elif status == 'show_result':
                if get_win(uid, match_id):
                    ai_all_win += 1
                all_match += 1
            elif status == 'end':
                print('end')
                match_id = join(battle_id,uid)
                print('第 '+all_match+' 场比赛')
            time.sleep(3)
        else:
            break

def run(battle_id,num):
    # each_num = int(num / 10)
    uid_list = ['43651716', '59241854', '32171446', '63211387', '77421480', '82811890', '85791770', '46751641',
                '98059289', '34488666']
    for uid in uid_list:
        if battle_id in ['2','3','18']:
            thread = threading.Thread(target=one_run, args=[battle_id, uid,num])
        else:
            thread = threading.Thread(target=more_run, args=[battle_id, uid, num])
        thread.start()
        time.sleep(2)
    thread.join()
    return ai_all_win

if __name__ == '__main__':
    # 百人场 = 18
    # 2人一题 = 2
    # 2人多题 = 5
    # 6人一题 = 3
    # 6人多题 = 4
    # 新手场 = 暂时先不做
    print(run('4',10))


