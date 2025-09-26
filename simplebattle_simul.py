import random

def battle_value(s, type, burst):           # 위력 산출
    if s == 0:
        s = 1
    i = 0; a = 0; d = 0
    if burst == 1:
        i = random.randint(1,2)
        if i == 1:
            a += s
        else:
            d += s

    if type == 'A' or type == 'a':
        p = random.randint(1, 10)
        p += p + a
        return p
    elif type == 'D' or type == 'd':
        p = random.randint(3,7)
        power = p + d
        return power
    
def battle_result(user_type, enemy_type, up, ep):            # 전투 결과 산출
    if user_type == enemy_type:

    else:
        if user_type == "attack":

        else:

    return r

def special_buffs(s):               # 상태이상

    return s


userHP = 100; enemyHP = 100   # 체력
us = 0; es = 0              # 상태이상
ub = 0; eb = 0              # 버스트 돌입 여부

t = 1                       # 경과 턴


print(' --룰북--\n 공격( 1 ~ 10 ) : 값이 더 클 경우, 공격 값만큼 피해.\n 수비( 3 ~ 7 ) : 값이 더 클 경우, 값의 절반만큼 반동 피해.' \
' 상태이상 : 공격-수비에서 공격이 더 클 경우, \"출혈\" 부여.\n  수비가 더 클 경우, \"마비\" 부여.' \
'   유형에 관계없이 본인의 값이 최댓값이 나올 경우, \"고조\" 획득. 최솟값일 경우, \"위축\" 획득.' \
'   수비-수비의 경우, 값이 적은 측에게 \"취약\" 부여.' \
'   모든 상태이상은 부여된 그 다음 턴 동안만 유효함.\n 유형에 관계없이 양측 값이 같을 경우, 상태이상 및 피해 무산.' \
' 체력이 절반 이하일 경우, 2턴 동안 \"버스트\" 돌입.' \
' 버스트 : 모든 상태이상을 제거하고, 그 수치만큼 \"회광반조\"를 획득(최솟값 1). 공격과 수비의 최종 위력 + \"회광반조 수치\"' \
'\n 버스트 외의 다른 모든 상태이상을 자세히 보려면 \'상태이상 룰\' 또는 \'S\' 입력.')

while(userHP > 0 and enemyHP > 0):



    p = input('{}턴, 플레이어 HP: {} / 적 HP: {}\n행동 선택\n\n공격(\'A\' 입력, 1 ~ 10)\n수비(\'D\' 입력, 3 ~ 7)\n'.format(t,userHP,enemyHP))
    if p == "상태이상 룰" or p == 'S' or p == 's':
        print('\n ---룰북(상태이상)---\n 출혈: [ 공격>수비 로 부여 ] 다음 턴 동안 받는 피해량 \'+2\'' \
              ' 마비: [ 공격<수비 로 부여 ] 다음 턴 동안 최종 공격 위력 \'-2\'' \
              ' 취약: [ 수비>수비 로 부여 ] 다음 턴 동안 최종 수비 위력 \'-2\'' \
              ' 고조: [ 최댓값일 경우 ] 다음 턴 동안 자신의 최종 공격 위력 \'+1\', 최종 수비 위력 \'-1\'' \
              ' 위축: [ 최솟값일 경우 ] 다음 턴 동안 자신의 최종 공격 위력 \'-1\', 최종 수비 위력 \'+1\'' \
              ' 격전: [ 양측의 값이 동일 ] 최대/최소로 인한 상태이상 무시, 양측 피해 무산.' \
              '\n 특수 상태이상(3)\n 역린: [ 공격>수비에서 공격 값이 7인 경우 ] 출혈을 부여하지 않는 대신, ')

    ep = random.randint(1,2)                                    # 적 행동 결정 (1: 공격 / 2: 수비 )
    if ep == 1:
        ep = '공격'
    else:
        ep = '수비'

    if p == 'A' or p == 'a':
        up = final_value(us, p, ub); p = '공격'
        if ep == 1:                                             # 공격 - 공격
            epp = int(random.randint(1, 10)); ep = '공격'
            if up > epp:
                enemyHP -= up
                r = '승. {} 만큼 피해!'.format(up)
            elif up < epp:
                userHP -= epp
                r = '패. {} 만큼 피해 받음!'.format(epp)
            else:
                r = '격전, 양측 피해 무산'
        else:                                                   # 공격 - 수비
            epp = int(random.randint(3, 7)); ep = '수비'
            if up > epp:
                enemyHP -= (up - epp)
                r = '적 방어 파괴. 초과 피해 {} 발생!'.format(up-epp)
            elif up < epp:
                userHP -= epp//2
                r = '공격 실패. 반동 피해 {} 받음.'.format(epp//2)
            else:
                r = '피해 상쇄'

    elif p == 'D' or p == 'd':
        up = int(random.randint(3, 7)); p = '수비'
        if ep == 1:                                              # 수비 - 공격
            epp = int(random.randint(1, 10)); ep = '공격'
            if up > epp:
                enemyHP -= up//2
                r = '방어 성공. {} 만큼 반동 피해!'.format(up//2)
            elif up < epp:
                userHP -= (epp - up)
                r = '방어 파괴됨. 초과 피해 {} 받음'.format(epp-up)
            else:
                r = '피해 상쇄'
        else:                                                    # 수비 - 수비
            epp = int(random.randint(3, 7)); ep = '수비'
            r = '상쇄'


    if error != 1:
        print('\n {}턴 결과\n 플레이어 행동 : {}[{}]\n 적 행동 : {}[{}]\n {}\n\n'.format(t, p, up, ep, epp, r))
        t += 1


class Endgame:
    def __init__(self, userHP, enemyHP):
        Endgame.userHP = userHP
        Endgame.enemyHP = enemyHP
        

if userHP <= 0:
    print('\n 패배 !\n 경과한 턴: {}\n 적 남은 체력: {}'.format(t-1, enemyHP))
elif enemyHP <= 0:
    print('\n 승리 !\n 경과한 턴: {}\n 플레이어 남은 체력: {}'.format(t-1, userHP))
elif userHP <= 0 and enemyHP <= 0:
    print('\n 공멸 !\n 경과한 턴: {}'.format(t-1))



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
    
    return