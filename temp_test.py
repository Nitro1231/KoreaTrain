import os
from koreatrain import *

# $ENV:SR_ID="YOUR_ID"
sr_id = os.getenv('SR_ID', None)
sr_pw = os.getenv('SR_PW', None)
ko_id = os.getenv('KO_ID', None)
ko_pw = os.getenv('KO_PW', None)
print('[SR_LOGIN_INFO]', sr_id, sr_pw)
print('[KO_LOGIN_INFO]', ko_id, ko_pw)

# print(Parameter('a', 'b'))

# print(search_station('김천 구미', 3))

s = SR(sr_id, sr_pw, auto_login=False, feedback=True)
# print(s.login())
# print(s.logout())

k = Korail(ko_id, ko_pw, auto_login=False, feedback=True)
# print(k.login())
# print(k.logout())


ps = Parameter(
    dep='수서',
    arr='부산',
    passengers=[Passenger(PassengerType.ADULT), Passenger(PassengerType.CHILD, 2)]
)
pk = Parameter(
    dep='서울',
    arr='부산',
    passengers=[Passenger(PassengerType.ADULT), Passenger(PassengerType.CHILD, 2)]
)

print(s.search_train(ps))
print('=' * 30)
print(k.search_train(pk))