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

sr = SR(sr_id, sr_pw, auto_login=False, feedback=True)
print(sr.login())
# print(sr.logout())

ko = Korail(ko_id, ko_pw, auto_login=False, feedback=True)
# print(ko.login())
# print(ko.logout())


param = Parameter(
    dep='수서',
    arr='부산',
    date='20230920',
    time='200000',
    #time_limit='182500',
    passengers=[Passenger(PassengerType.ADULT), Passenger(PassengerType.CHILD, 2)],
    reserve_option=ReserveOption.SPECIAL_FIRST
)
sr_trains = sr.search_train(param)
print(sr_trains[0])
# sr.reserve(param, sr_trains[0])
print(sr.get_reservations())

# print('=' * 30)

# param.dep = '서울'
# print(k.search_train(param))