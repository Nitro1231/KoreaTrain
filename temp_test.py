import os
from koreatrain import *

# $ENV:SR_ID="YOUR_ID"
# sr_id = os.environ['SR_ID']
# sr_pw = os.environ['SR_PW']
ko_id = os.environ['KO_ID']
ko_pw = os.environ['KO_PW']
# print(sr_id, sr_pw)
print(ko_id, ko_pw)

# print(Parameter('a', 'b'))

k = Korail(ko_id, ko_pw, auto_login=False, feedback=True)
print(k.login())
print(k.logout())

p = Parameter(
    dep='서울',
    arr='부산',
    date='20230815',
    time='210000'
)
print(p)
print(k.search_train(p))
