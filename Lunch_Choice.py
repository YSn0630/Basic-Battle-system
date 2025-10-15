import random
import time

ll = []

le = ''

while (le != '끝'):
    le = input("뭐.먹.싶?(그.싶.끝.입.) > ")
    if le != '끝':
        ll.append(le)

lc = []
lc = random.sample(ll,1)
print("오늘의 메뉴는...")

time.sleep(3)

if "" not in lc:
    print(*lc)
else:
    print("굶.\n공백, 괘씸.")