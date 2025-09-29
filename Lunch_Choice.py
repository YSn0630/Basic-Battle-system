import random
import time

ll = []

le = ''

while (le != '끝'):
    le = input("뭐.먹.싶? > ")
    if le != '끝':
        ll.append(le)

lc = random.sample(ll,1)

print("오늘의 메뉴는...")

time.sleep(3)

print(lc)