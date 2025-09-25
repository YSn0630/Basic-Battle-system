# 공격은 3 ~ 8의 randint
# 방어는 3 ~ 8의 randint

# 매 턴 양측은 공격 혹은 방어 중 한 가지를 선택하여 행동.
# 값이 더 높은 쪽의 승자 독식 구조
# 양측의 체력은 20. 체력이 음수로 떨어지면 패배.

# 상태이상
# 원본 값이 최댓값: 다음 턴 동안 고조(최종 공격 위력 +1, 최종 수비 위력 -1) 얻음
# 원본 값이 최솟값: 다음 턴 동안 위축(최종 공격 위력 -1, 최종 수비 위력 +1) 얻음

# 공>공: 공격 값만큼 일방 피해
# 공>방: (공격-방어) 값만큼 일방 피해 
# 방>공: 다음 턴 동안 상대에게 마비(최종 공격 위력 감소 -2) 부여
# 방>방: 다음 턴 동안 상대에게 무장 해제(최종 방어 위력 감소 -2) 부여
# 값이 동일할 경우, 격전(양측 피해 무산. 값이 최대/최소일 경우에도 다음 턴에 고조/위축이 적용되지 않음) 발생

# 특수 상황
# 역린: 공>방 시, 기본 공격 위력이 7이면, 출혈을 부여하는 대신 방어를 무시한 고정 피해 10
# 기선 제압: 방>방 시, 기본 위력이 7이면, 다음 턴에 취약 5 부여

# 특수 상태이상
# 회광반조(1회성): 턴 시작 시 자신의 체력이 절반 이하일 경우, 이번 턴과 다음 턴 동안 보유한 모든 상태이상을 제거하고 제거한만큼 공격&방어의 최종 위력 증가.
#               (이는 한 게임 동안 각각 한 번씩만 발동함.)

# 1. 매 턴마다, 해당 게임의 승산이 높은 쪽으로 고려될 공격/방어 선택 비율이 50:50이 되게끔 밸런스 패치할 것.
# 2. 한 게임의 평균 소요 턴이 10턴 내외가 되도록 밸런스 패치할 것.


#공격: 3~8 v
#방어: 3~8 v

# 다음 턴 지속 적용 상태이상
#고조: 공격 4~9 / 방어 2~7 v
#위축: 공격 2~7 / 방어 4~9 v
#취약: +5 피해 

# 다음 턴 즉시 적용 상태이상
#마비: -2 공격 v
#무장 해제: -2 방어 v

#역린: 10 고정 피해 v
#기선 제압: 취약 부여

#회광반조: 일회성 발동 제한 v


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
    if val == 8:
        state['raise'] += 1
        delay_state['raiseOn'] = True
    elif val == 3:
        state['tension'] += 1
        delay_state['tensionOn'] = True
    elif val == 7:
        special += 1            # 역린, 만전 확인용 변수
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
    if hp <= 50 and burst < 2:
        burst += 1
        p = count_value_one(state)
        for v in delay_state.values():
            if v:
                v = False
    elif burst == 2:
        burst += 1
    return p, burst

# 역린
def critDMG(hp, special):
    if special == 1:
        hp -= 10
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


def simulate_game():

    # 기본 변수 초기화
    state1, state2 = { 'raise': 0, 'tension': 0, 'vuln': 0, 'paralysis': 0, 'broken': 0 }, \
        { 'raise': 0, 'tension': 0, 'vuln': 0, 'paralysis': 0, 'broken': 0 }
    hp1, hp2 = 20, 20
    turn = 0
    special1, special2 = 0, 0       # 특수 효과 판별용 변수 - 역린, 기선제압
    delay_state1, delay_state2 = { 'raiseOn': False, 'tensionOn': False, 'vulnOn': False }, \
        { 'raiseOn': False, 'tensionOn': False, 'vulnOn': False }      # 고조, 위축, 취약 판별용 딕셔너리
    burst1, burst2 = 0, 0           # 회광반조 발동 판정용 변수

    while hp1 > 0 and hp2 > 0:
        turn += 1
        p1, p2 = 0, 0                   # 위력 증감 변수

        action1 = random.choice(['attack','defense'])
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
        state1, state2 = { 'raise': 0, 'tension': 0, 'vuln': 0, 'paralysis': 0, 'broken': 0, 'struggle': 0 }, \
        { 'raise': 0, 'tension': 0, 'vuln': 0, 'paralysis': 0, 'broken': 0, 'struggle': 0 }

        p1, special1 = origin_value_buff(p1, action1, special1, val1, state1, delay_state1)
        p1, special2 = origin_value_buff(p2, action2, special2, val2, state2, delay_state2)

        # 턴 시작, 최종 위력 산출 및 음수 방지 조정
        val1 += p1
        val2 += p2
        if val1 < 0: val1 = 0
        if val2 < 0: val2 = 0

        # 합 진행
        if action1=='attack' and action2=='attack':             # 공격 - 공격
            if val1 > val2:
                hp2 -= (val1 + state2['vuln'] * 5)
            elif val1 < val2:
                hp1 -= (val2 + state1['vuln'] * 5)
            else:
                continue
        elif action1=='attack' and action2=='defense':         # 공격 - 방어
            if val1 > val2 and special1 == 1:
                hp2, special1 = critDMG(hp2, special1)
            elif val1 > val2:
                dmg = val1 - val2 + state2['vuln'] * 5
                if dmg <= 0: dmg = 0
                hp2 -= dmg
            elif val1 < val2:
                state1['paralysis'] += 1
            else:
                continue
        elif action1=='defense' and action2=='attack':         # 방어 - 공격
            if val1 < val2 and special2 == 1:
                hp1, special2 = critDMG(hp1, special2)
            elif val1 < val2:
                dmg = val2 - val1 + state1['vuln'] * 5
                if dmg <= 0: dmg = 0
                hp1 -= dmg
            elif val1 > val2:
                state2['paralysis'] += 1
            else:
                continue
        else:                                                   # 방어 - 방어
            if val1 < val2:
                state1['broken'] = 1
                vuln(special2, state1, delay_state1)
            elif val1 > val2:
                state2['broken'] = 1
                vuln(special1, state1, delay_state1)
            else:
                continue

    return turn

# 시뮬레이션 10,000판
total_turns = 0
for i in range(10000):
    total_turns += simulate_game()
avg_turn = total_turns/10000
print("평균 게임 턴:", avg_turn)