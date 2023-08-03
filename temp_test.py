from korea_train import *

ko = KoreaTrain(Platform.KORAIL, feedback=True)
print(ko)
# print(ko.login())
print(ko)
print(ko.logout())

# ko_search = KorailSearch('서울', '부산', train_type=TrainType.KTX)
ko_search = KorailParameter('서울', '부산', '20230805', '074000', '080000', None, TrainType.KTX)
print(ko_search)
print(ko.search_train(ko_search, False))


print('=' * 30)
sr = KoreaTrain(Platform.SR)
print(sr)
# print(sr.login('a', 'b'))
print(sr)
print(sr.logout())

sr_search = SRParameter('수서', '부산', '20230805', '053000', '061000')
print(sr_search)
print(sr.search_train(sr_search, False))
