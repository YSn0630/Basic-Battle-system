# 공격은 3 ~ 9의 randint
# 방어는 3 ~ 9의 randint

# 매 턴 양측은 공격 혹은 방어 중 한 가지를 선택하여 행동.
# 값이 더 높은 쪽의 승자 독식 구조
# 양측의 체력은 30. 체력이 0 이하로 떨어지면 패배.

# 상태이상
# 원본 값이 최댓값: 다음 턴 동안 고조(최종 공격 위력 +1, 최종 수비 위력 -1) 얻음
# 원본 값이 최솟값: 다음 턴 동안 위축(최종 공격 위력 -1, 최종 수비 위력 +1) 얻음

# 공>공: 공격 값만큼 일방 피해
# 공>방: (공격-방어) 값만큼 일방 피해 
# 방>공: 다음 턴 동안 상대에게 마비(최종 공격 위력 감소 -2) 부여
# 방>방: 다음 턴 동안 상대에게 무장 해제(최종 방어 위력 감소 -2) 부여
# 값이 동일할 경우, 격전. 양측 피해 무산

# 특수 상황
# 역린: 공>방 시, 기본 공격 위력이 7이면, 방어를 무시한 고정 피해 10
# 기선 제압: 방>방 시, 기본 위력이 7이면, 다음 턴에 취약 5 부여

# 특수 상태이상
# 회광반조(1회성): 턴 시작 시 자신의 체력이 절반 이하일 경우, 이번 턴과 다음 턴 동안 보유한 모든 상태이상을 제거하고,
#               제거한만큼 공격&방어의 최종 위력 증가.
#               (한 게임 동안 각각 한 번씩만 발동함.)


import random

# 적용 중인 상태이상 갯수 세기용 함수
def count_value_one(d):
    return sum(1 for v in d.values() if v == 1)

# 공격/방어 기본 위력 결정
def attack_value():
    return random.randint(3, 9)
def defense_value():
    return random.randint(3, 9)

# 원본 값 판별 (고조, 위축, 역린, 만전)
def origin_value_buff(p, action, special, val, state, delay_state):
    special = 0
    i = 0
    if delay_state['raiseOn'] or delay_state['tensionOn']:          # 이전 턴에 고조, 위축을 얻었는지 검사 및 효과 적용
        if delay_state['raiseOn'] and action=='attack':
            i += 1
        elif delay_state['raiseOn'] and action=='defense':
            i -= 1
        elif delay_state['tensionOn'] and action=='attack':
            i -= 1
        else:
            i += 1
    if val == 9:
        state['raise'] = 1
        delay_state['raiseOn'] = True
    elif val == 3:
        state['tension'] = 1
        delay_state['tensionOn'] = True
    elif val == 7:
        special = 1            # 역린, 만전 확인용 변수
    else:
        delay_state['raiseOn'] = False
        delay_state['tensionOn'] = False                # 이전 턴에 상태이상을 얻지 않았을 경우, 상태이상 초기화
    p += i
    return p, special

# 위력 조정 (마비, 무장 해제)
def value_debuffs(action, state):
    if action == 'attack':
        return state['paralysis'] * 2
    else:
        return state['broken'] * 2
    
# 버스트 체크 및 실행
def burst_check(hp, burst, p, state, delay_state):    
    if hp <= 15 and burst < 2:
        burst += 1
        p = count_value_one(state)
        for v in delay_state.values():
            if v:
                v = False
    elif burst == 2:
        burst += 1
    return p, burst

# 역린
def critDMG(hp, special, state):
    if special == 1:
        hp -= (10 + state['vuln'] * 5)
    special = 0
    return hp, special

# 기선 제압(취약)
def vuln(special, state, delay_state):
    if delay_state['vulnOn']:                       # 이전 턴 검사 및 적용
        state['vuln'] = 1
    if special == 1:                                # 이번 턴 적용 및 초기화
        delay_state['vulnOn'] = True
    else:
        delay_state['vulnOn'] = False

def printstate(state, dstate):
    R = []
    if dstate['raiseOn']:
        R.append('고조')
    if dstate['tensionOn']:
        R.append('위축')
    if dstate['vulnOn']:
        R.append('취약')
    if state['paralysis'] == 1:
        R.append('마비')
    if state['broken'] == 1:
        R.append('무장해제')
    return R

def printbattleui(type1, type2, val1, val2, dmg):
    if type1 == 'attack':
        texttype1 = '공격'
    else:
        texttype1 = '방어'
    if type2 == 'attack':
        texttype2 = '공격'
    else:
        texttype2 = '방어'
    print(f"\n\n 플레이어 행동: {texttype1} ({val1})\t적 행동: {texttype2} ({val2})")
    if val1 == val2:
        print(f"\n 격전 !\n {val1} >>> <<< {val2}\n")
    elif val1 > val2:
        print(f"\n 합 승리 !\n {val1} >>> >>> {val2}\n")
        if type1 == 'attack':
            print(f" 적에게 체력 피해 {dmg} 가함 ")
    elif val1 < val2:
        print(f"\n 합 패배...\n {val1} <<< <<< {val2}\n")
        if type2 == 'attack':
            print(f" 플레이어 체력 피해 {dmg} 받음 ")


def simulate_game():

    # 기본 변수 초기화
    state1, state2 = { 'raise': 0, 'tension': 0, 'vuln': 0, 'paralysis': 0, 'broken': 0 }, \
        { 'raise': 0, 'tension': 0, 'vuln': 0, 'paralysis': 0, 'broken': 0 }
    hp1, hp2 = 30, 30
    turn = 0
    special1, special2 = 0, 0       # 특수 효과 판별용 변수 - 역린, 기선제압
    delay_state1, delay_state2 = { 'raiseOn': False, 'tensionOn': False, 'vulnOn': False }, \
        { 'raiseOn': False, 'tensionOn': False, 'vulnOn': False }      # 고조, 위축, 취약 판별용 딕셔너리
    burst1, burst2 = 0, 0           # 회광반조 발동 판정용 변수

    while hp1 > 0 and hp2 > 0:
        turn += 1
        p1, p2 = 0, 0                   # 위력 증감 변수 초기화

        print(f"\n\n--- 제 {turn}턴 ---\n\n 플레이어 HP: {hp1}\t 적 HP: {hp2}\n")
        R1 = printstate(state1, delay_state1); print(" 플레이어 상태 이상: ", *R1)
        if hp1 <= 15 and burst1 < 2:
            print("\n !! 현재 플레이어 회광반조 적용 중 !!\n")
        R2 = printstate(state2, delay_state2); print(" 적 상태이상: ", *R2)
        if hp2 <= 15 and burst2 < 2:
            print("\n !! 현재 적 회광반조 적용 중 !!\n")

        try:
            userAct = input("\n 행동 입력 < 공격: A ( 3 ~ 9 ) / 수비: D ( 3 ~ 9 ) > ")

            if userAct == 'a' or userAct == 'A':
                action1 = 'attack'
            elif userAct == 'd' or userAct == 'D':
                action1 = 'defense'
        except Exception as e:
            print('error', e)
            turn -= 1
            continue

        action2 = random.choice(['attack','defense'])
        val1 = attack_value() if action1=='attack' else defense_value()
        val2 = attack_value() if action2=='attack' else defense_value()

        # 버스트 체크 및 실행
        p1, burst1 = burst_check(hp1, burst1, p1, state1, delay_state1)
        p2, burst2 = burst_check(hp2, burst2, p2, state2, delay_state2)

        # 위력 증감 적용(버스트가 아닐 경우 위력 계열 상태이상 적용)
        if burst1 == 0 or burst1 == 3:
            p1 -= value_debuffs(action1, state1)
            
        if burst2 == 0 or burst2 == 3:
            p2 -= value_debuffs(action2, state2)

        # 상태이상 초기화 및 턴 시작 시 상태이상(고조, 위축, 취약, 역린, 기선 제압) 산출 및 적용
        state1, state2 = { 'raise': 0, 'tension': 0, 'vuln': 0, 'paralysis': 0, 'broken': 0 }, \
        { 'raise': 0, 'tension': 0, 'vuln': 0, 'paralysis': 0, 'broken': 0 }

        p1, special1 = origin_value_buff(p1, action1, special1, val1, state1, delay_state1)
        p2, special2 = origin_value_buff(p2, action2, special2, val2, state2, delay_state2)

        # 턴 시작, 최종 위력 산출 및 음수 방지 조정
        val1 += p1
        val2 += p2
        if val1 < 0: val1 = 0
        if val2 < 0: val2 = 0

        # 합 진행
        if action1=='attack' and action2=='attack':             # 공격 - 공격
            if val1 > val2:
                hp2 -= (val1 + state2['vuln'] * 5)
                printbattleui(action1, action2, val1, val2, (val1 + state2['vuln'] * 5))
            elif val1 < val2:
                hp1 -= (val2 + state1['vuln'] * 5)
                printbattleui(action1, action2, val1, val2, (val2 + state1['vuln'] * 5))
            else:
                printbattleui(action1, action2, val1, val2, 0)
                continue
        elif action1=='attack' and action2=='defense':         # 공격 - 방어
            if val1 > val2 and special1 == 1:
                hp2, special1 = critDMG(hp2, special1, state2)
                print("\n\n !!! !!! 역린 !!! !!!")
                printbattleui(action1, action2, val1, val2, (10 + state2['vuln'] * 5))
            elif val1 > val2:
                dmg = val1 - val2 + state2['vuln'] * 5
                if dmg <= 0: dmg = 0
                hp2 -= dmg
                printbattleui(action1, action2, val1, val2, dmg)
            elif val1 < val2:
                state1['paralysis'] = 1
                printbattleui(action1, action2, val1, val2, 0)
                print("\n 반동 !\n 다음 턴 동안 플레이어에게 마비 발생.")
            else:
                printbattleui(action1, action2, val1, val2, 0)
                continue
        elif action1=='defense' and action2=='attack':         # 방어 - 공격
            if val1 < val2 and special2 == 1:
                hp1, special2 = critDMG(hp1, special2, state1)
                print("\n\n !!! !!! 역린 !!! !!!")
                printbattleui(action1, action2, val1, val2, (10 + state1['vuln'] * 5))
            elif val1 < val2:
                dmg = val2 - val1 + state1['vuln'] * 5
                if dmg <= 0: dmg = 0
                hp1 -= dmg
                printbattleui(action1, action2, val1, val2, dmg)
            elif val1 > val2:
                state2['paralysis'] = 1
                printbattleui(action1, action2, val1, val2, 0)
                print("\n 반동 !\n 다음 턴 동안 적에게 마비 발생.")
            else:
                printbattleui(action1, action2, val1, val2, 0)
                continue
        else:                                                   # 방어 - 방어
            if val1 < val2:
                state1['broken'] = 1
                vuln(special2, state1, delay_state1)
                printbattleui(action1, action2, val1, val2, 0)
                print("\n 반동 !\n 다음 턴 동안 플레이어에게 무장 해제 발생.")
                if special2 == 1:
                    print("\n\n !! !! 기선 제압 !! !!\n 다음 턴 동안 플레이어가 추가적으로 취약 5 얻음\n")
            elif val1 > val2:
                state2['broken'] = 1
                vuln(special1, state2, delay_state2)
                printbattleui(action1, action2, val1, val2, 0)
                print("\n 반동 !\n 다음 턴 동안 적에게 무장 해제 발생.")
                if special1 == 1:
                    print("\n\n !! !! 기선 제압 !! !!\n 다음 턴 동안 적이 추가적으로 취약 5 얻음\n")
            else:
                printbattleui(action1, action2, val1, val2, 0)
                continue

    return turn, hp1, hp2

final_turn, final_hp1, final_hp2 = simulate_game()

print(f'\n\n\n --- 게임 종료 ---\n\n 누적 턴: {final_turn}\n')

if final_hp1 <= 0:
    print(f" 패배 ...\n 적 남은 체력: {final_hp2}\n")
elif final_hp2 <= 0:
    print(f" 승리 !\n 남은 체력: {final_hp1}\n")