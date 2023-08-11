
# Platform request parameter analysis

This document will analyze the data fields and parameters that each platform uses for its service. Those are heavily based on the website [Korail](https://www.letskorail.com/) and [SR](https://etk.srail.kr/).

## KORAIL & SR

### Search Parameters

| KORAIL |  | SR |  | Value | Description | Note |
|---|---|---|---|---|---|---|
| txtGoStart | :o: | dptRsStnCdNm | :o: | str | 출발역 | e.g. 서울 |
| txtGoEnd | :o: | arvRsStnCdNm | :o: | str | 도착역 | e.g. 부산 |
| txtGoAbrdDt | :o: | dptDt | :o: | str | 출발년월일 | e.g. 20230102 (2023년 1월 2일) |
| selGoHour | :o: | dptTm | :o: | str | 출발시 | e.g. 130500 (13시 5분) |
| radJobId | :o: | chtnDvCd | :o: | int | 여정경로 |  |
|  | :o: |  | :o: | 1 | 직통 |  |
|  | :o: |  | :o: | 2 | 환승 |  |
|  | :o: |  | :o: | 3 | 왕복 |  |


### Train Type

| KORAIL |  | SR |  | Value | Description | Note |
|---|---|---|---|---|---|---|
| selGoTrain | :o: |  | :x: | str | 열차 종류 |  |
|  | :o: |  | :x: | 05 | 전체 |  |
|  | :o: |  | :x: | 00 | KTX |  |
|  | :o: |  | :x: | 09 | ITX-청춘 |  |
|  | :o: |  | :x: | 08 | ITX-새마을 |  |
|  | :o: |  | :x: | 02 | 무궁화호/누리로 |  |
|  | :o: |  | :x: | 03 | 통근열차 |  |


### Passenger Type

| KORAIL |  | SR |  | Value | Description | Note |
|---|---|---|---|---|---|---|
| txtPsgFlg_1 | :o: | psgInfoPerPrnb1 | :o: | int, 0 ~ 9 | 어른 | 만 13세 이상 |
| txtPsgFlg_2 | :o: | psgInfoPerPrnb5 | :o: | int, 0 ~ 9 | 어린이 | 만 6세 ~ 12세 어린이 |
| txtPsgFlg_8 | :o: |  | :x: | int, 0 ~ 9 | 유아 | 만 6세 미만 유아 |
| txtPsgFlg_3 | :o: | psgInfoPerPrnb4 | :o: | int, 0 ~ 9 | 경로 | 만 65세 이상 경로 |
| txtPsgFlg_4 | :o: | psgInfoPerPrnb2 | :o: | int, 0 ~ 9 | 중증 | 장애의 정도가 심한 장애인(구1~3급) |
| txtPsgFlg_5 | :o: | psgInfoPerPrnb3 | :o: | int, 0 ~ 9 | 경증 | 장애의 정도가 심하지 않은 장애인(구4~6급) |


### Seat Type

| KORAIL |  | SR |  | Value | Description | Note |
|---|---|---|---|---|---|---|
| txtSeatAttCd_2  | :o: |  | :x: | str | 좌석 방향 |  |
|  | :o: |  | :x: | 000  | 기본  |  |
|  | :o: |  | :x: | 009 | 순방향석  |  |
|  | :o: |  | :x: | 010 | 역방향석  |  |
| txtSeatAttCd_3 | :o: | locSeatAttCd1  | :o: | str | 좌석 위치 |  |
|  | :o: |  | :o: | 000 | 기본 |  |
|  | :o: |  | :o: | 011 | 1인석 |  |
|  | :o: |  | :o: | 012 | 창측좌석 |  |
|  | :o: |  | :o: | 013 | 내측좌석 |  |
| txtSeatAttCd_4 | :o: | rqSeatAttCd1  | :o: | str | 좌석 종류 |  |
|  | :o: |  | :o: | 015 | 기본 |  |
|  | :o: |  | :x: | 019 | 유아동반/편한대화 |  |
|  | :o: |  | :x: | 031 | 노트북 |  |
|  | :o: |  | :o: | 021 | 수동휠체어석 |  |
|  | :o: |  | :o: | 028 | 전동휠체어석 |  |
|  | :o: |  | :x: | XXX | 수유실 인접 |  |
|  | :o: |  | :x: | 018 | 2층석 |  |
|  | :o: |  | :x: | 032 | 자전거거치대 |  |


## KORAIL

### Search Parameters

| Key | Value | Description | Note |
|---|---|---|---|
| txtGoStart | str | 출발역 | e.g. 서울 |
| txtGoEnd | str | 도착역 | e.g. 부산 |
| txtGoAbrdDt | str | 출발년월일 | e.g. 20230102 (2023년 1월 2일) |
| selGoHour | str | 출발시 | e.g. 130500 (13시 5분) |
| radJobId | int | 여정경로 |  |
|  | 1 | 직통 | |
|  | 2 | 환승 | |
|  | 3 | 왕복 | |


### Train Type

| Key | Value | Description | Note |
|---|---|---|---|
| selGoTrain | str | 열차 종류 |  |
|  | 05 | 전체 | |
|  | 00 | KTX |  |
|  | 09 | ITX-청춘 | |
|  | 08 | ITX-새마을 | |
|  | 02 | 무궁화호/누리로 | |
|  | 03 | 통근열차 | |


### Passenger Type

| Key | Value | Description | Note |
|---|---|---|---|
| txtPsgFlg_1 | int, 0 ~ 9 | 어른 | |
| txtPsgFlg_2 | int, 0 ~ 9 | 어린이 | 만 6세 ~ 12세 어린이 |
| txtPsgFlg_8 | int, 0 ~ 9 | 유아 | 만 6세 미만 유아 |
| txtPsgFlg_3 | int, 0 ~ 9 | 경로 | 만 65세 이상 경로 |
| txtPsgFlg_4 | int, 0 ~ 9 | 중증 | 장애의 정도가 심한 장애인(구1~3급) |
| txtPsgFlg_5 | int, 0 ~ 9 | 경증 | 장애의 정도가 심하지 않은 장애인(구4~6급) |


### Seat Type

| Key | Value | Description | Note |
|---|---|---|---|
| txtSeatAttCd_2 | str | 좌석 방향 |  |
|  | 000 | 기본 |  |
|  | 009 | 순방향석 |  |
|  | 010 | 역방향석 |  |
| txtSeatAttCd_3 | str | 창/내측/1인좌석종별 |  |
|  | 000 | 기본 |  |
|  | 011 | 1인석 |  |
|  | 012 | 창측좌석 |  |
|  | 013 | 내측좌석 |  |
| txtSeatAttCd_4 | str | 좌석 종류 |  |
|  | 015 | 기본 |  |
|  | 019 | 유아동반/편한대화 |  |
|  | 031 | 노트북 |  |
|  | 021 | 수동휠체어석 |  |
|  | 028 | 전동휠체어석 |  |
|  | XXX | 수유실 인접 |  |
|  | 018 | 2층석 |  |
|  | 032 | 자전거거치대 |  |


## SR

### Search Parameters

| Key | Value | Description | Note |
|---|---|---|---|
| dptRsStnCdNm | str | 출발지 | e.g. 수서 |
| arvRsStnCdNm | str | 도착지 | e.g. 부산 |
| dptDt | str | 출발년월일 | e.g. 20230102 (2023년 1월 2일) |
| dptTm | str | 출발시 | e.g. 130500 (13시 5분) |
| chtnDvCd | int | 여정경로 |  |
|  | 1 | 직통 | |
|  | 2 | 환승 | |
|  | 3 | 왕복 | |


### Passenger Type

| Key | Value | Description | Note |
|---|---|---|---|
| psgInfoPerPrnb1 | int, 0 ~ 9 | 어른 | 만 13세 이상 |
| psgInfoPerPrnb5 | int, 0 ~ 9 | 어린이 | 만 6세 ~ 12세 어린이 |
| psgInfoPerPrnb4 | int, 0 ~ 9 | 노인 | 만 65세 이상 경로 |
| psgInfoPerPrnb2 | int, 0 ~ 9 | 중증 | 장애의 정도가 심한 장애인(구1~3급) |
| psgInfoPerPrnb3 | int, 0 ~ 9 | 경증 | 장애의 정도가 심하지 않은 장애인(구4~6급) |


### Seat Type

| Key | Value | Description | Note |
|---|---|---|---|
| locSeatAttCd1 | str | 좌석 위치 |  |
|  | 000 | 기본 |  |
|  | 011 | 1인석 |  |
|  | 012 | 창측좌석 |  |
|  | 013 | 내측좌석 |  |
| rqSeatAttCd1 | str | 좌석 종류 |  |
|  | 015 | 기본 |  |
|  | 021 | 수동휠체어석 |  |
|  | 028 | 전동휠체어석 |  |
