# Korea-Train
A Python wrapper for [korail2](https://github.com/carpedm20/korail2) and [SRT](https://github.com/ryanking13/SRT).


# Data Classes

## class `Parameter`

| Key | Value Type | Description | KORAIL | SR | Default Value |
|---|---|---|---|---|---|
| dep | str | Departing Station Name | :o: | :o: | USER INPUT REQUIRED |
| arr | str | Destination Station Name | :o: | :o: | USER INPUT REQUIRED |
| date | str | Departing Date (yyyymmdd) | :o: | :o: | Current Date |
| time | str | Departing Time (HHMMSS) | :o: | :o: | Current Time |
| time_limit | str | Departing Time Upper Limit (HHMMSS) | :o: | :o: | '240000' |
| train_type | TrainType | Train Type | :o: | :x: | TrainType.ALL |
| passengers | list[Passenger] | List of Passengers | :o: | :o: | [Passenger()] |
| heading | Heading | Heading of Seat | :o: | :x: | Heading.DEFAULT |
| seat_location | SeatLocation | Location of Seat | :o: | :o: | SeatLocation.DEFAULT |
| seat_type | SeatType | Seat Type | :o: | :o: | SeatType.DEFAULT |
| reserve_option | ReserveOption | Reservation Options | :o: | :o: | ReserveOption.GENERAL_FIRST |


## class `Passenger`

| Key | Value Type | Description | KORAIL | SR | Default Value |
|---|---|---|---|---|---|
| type_code | PassengerType | Passenger Type | :o: | :o: | PassengerType.ADULT |
| count | int | Number of Passengers | :o: | :o: | 1 |


# Enums

## `Platform`

| Name | Value |
|---|---|
| SR | 0 |
| KORAIL | 1 |


## `TrainType`

| Name | Value | Description | KORAIL | SR |
|---|---|---|---|---|
| KTX | '100' | KTX | :o: | :x: |
| SAEMAEUL | '101' | 새마을호 | :o: | :x: |
| MUGUNGHWA | '102' | 무궁화호 | :o: | :x: |
| TONGGUEN | '103' | 통근열차 | :o: | :x: |
| NURIRO | '102' | 누리로 | :o: | :x: |
| ALL | '109' | 전체 | :o: | :x: |
| AIRPORT | '105' | 공항직통 | :o: | :x: |
| KTX_SANCHEON | '100' | KTX-산천 | :o: | :x: |
| ITX_SAEMAEUL | '101' | ITX-새마을 | :o: | :x: |
| ITX_CHEONGCHUN | '104' | ITX-청춘 | :o: | :x: |


## `PassengerType`

| Name | Value | Description | KORAIL | SR |
|---|---|---|---|---|
| ADULT | 0 | 어른 - 만 13세 이상 | :o: | :o: |
| CHILD | 1 | 어린이 - 만 6세 ~ 12세 어린이 | :o: | :o: |
| CHILD_UNDER_6 | 2 | 유아 - 만 6세 미만 유아 | :o: | :x: |
| SENIOR | 3 | 경로 - 만 65세 이상 경로 | :o: | :o: |
| DISABILITY_1_TO_3 | 4 | 중증 - 장애의 정도가 심한 장애인(구1~3급) | :o: | :o: |
| DISABILITY_4_TO_6 | 5 | 경증 - 장애의 정도가 심한 장애인(구1~3급) | :o: | :o: |


## `Heading`

좌석 방향

| Name | Value | Description | KORAIL | SR |
|---|---|---|---|---|
| DEFAULT | '000' | 기본 | :o: | :x: |
| FORWARD | '009' | 순방향석 | :o: | :x: |
| BACKWARD | '010' | 역방향석 | :o: | :x: |


## `SeatLocation`

좌석 위치

| Name | Value | Description | KORAIL | SR |
|---|---|---|---|---|
| DEFAULT | '000' | 기본 | :o: | :o: |
| SINGLE | '011' | 1인석 | :o: | :o: |
| WINDOW | '012' | 창측좌석 | :o: | :o: |
| AISLE | '013' | 내측좌석 | :o: | :o: |


## `SeatType`

좌석 종류

| Name | Value | Description | KORAIL | SR |
|---|---|---|---|---|
| DEFAULT | '015'  | 기본  | :o: | :o: |
| CHILD | '019'  | 유아동반 / 편한대화  | :o: | :x: |
| LAPTOP | '031'  | 노트북  | :o: | :x: |
| MANUAL_WHEELCHAIR | '021'  | 수동휠체어석  | :o: | :o: |
| ELECTRIC_WHEELCHAIR | '028'  | 전동휠체어석  | :o: | :o: |
| NURSING_ROOM | 'XXX'  | 수유실 인접  | :o: | :x: |
| SECOND_FLOOR | '018'  | 2층석  | :o: | :x: |
| BIKE_RACK | '032' | 자전거거치대 | :o: | :x: |


## `ReserveOption`

예약 옵션

| Name | Value | Description | KORAIL | SR |
|---|---|---|---|---|
| GENERAL_FIRST | 'GENERAL_FIRST' | 일반실 우선  | :o: | :o: |
| GENERAL_ONLY | 'GENERAL_ONLY' | 일반실  | :o: | :o: |
| SPECIAL_FIRST | 'SPECIAL_FIRST' | 특실 우선  | :o: | :o: |
| SPECIAL_ONLY | 'SPECIAL_ONLY' | 특실 | :o: | :o: |
