# 2nd_Project
2차 프로젝트


## 국내 유가 데이터 대시보드
----------------------

### 프로젝트 배경 및 목표
- **러-우 전쟁**, **하마스-이스라엘 전쟁** 등 국제이슈 발생으로 **유가 변동에 대한 관심 상승**
- 유가 추이, 국내 유가 변동의 파악에 대한 **시각화 정보 제공**에 대한 필요성 대두

- 기술적 목표
    - OPEN API를 활용한 데이터 파일 생성 (csv)
    - AWS의 S3 서버 관리에 대한 이해
    - Datawarehouse 구축
    - Superset을 활용한 데이터 시각화 및 대시보드 생성
### 진행과정 및 팀원 역할

| 이름 | 역할 | 깃헙 |
| :---: | :---: | :---: |
| 곽도영 | 데이터 수집 및 ETL, 대시보드 개발 | https://github.com/dooby99 |
| 손봉호 | 데이터 수집 및 ETL, 대시보드 개발 | https://github.com/bongHsss |
| 이민재 | 데이터 수집 및 ETL, 대시보드 개발 | https://github.com/snowmuffin |
| 조성민 | 데이터 수집 및 ETL, 대시보드 개발 | https://github.com/eddiddiee |

### 활용 기술 및 프레임 워크
||프레임 워크|
|:---:|:---:|
|Data|오피넷 유가정보 API, BeautifulSoup, Selenium|
|Data Preprocessing|Python, Pandas|
|Storage Server|AWS S3|
|Data Warehouse(DB)|Snowflake|
|Visualization & Dashboard|Preset|
|Team Management|Slack, Github, Notion|

### ERD
![프로그래머스 2차 프로젝트 ERD drawio](https://github.com/Programmers-2nd-Project/2nd_Project/assets/166678994/6710bcde-2a83-4e78-b993-4f897ef47a66)

### DashBoard 결과물
![2-차프로젝트-3-팀-2-조-2024-05-17T07-12-16 085Z](https://github.com/Programmers-2nd-Project/2nd_Project/assets/77647785/3bcaf899-0066-430e-9456-8e7e1ff62c26)
### 기대효과 및 보안점
### 차트별 기대효과

- **기간별 가격 추이 차트**
    - 국내 유가(휘발유, 경유) 추이를 쉽게 확인 가능 (1년 및 5년)
- **지역별 휘발유/경유 평균 가격 차트**
    - 연료별 평균 가격 확인 및 타 지역과의 색상 차이로 평균 가격 비교 가능
- **지역별 휘발유/경유 최저가 테이블 차트**
    - 각 지역별 최저가 주유소의 위치와 가격 확인 가능
- **연료별 차량 정보** **차트**
    - 국내 차량의 연료별 등록 대수 증감(2022 vs 2023) 및 파이차트를 통한 비율 확인 가능(2023.12월 기준)
- **휘발유/경유 가격 변동량 차트**
    - 연료별 변동량 확인 가능 (최근 1년)
- **주유소 브랜드 별 평균 휘발유/경유 가격 차트**
    - 주유소 브랜드 별 연료별 평균 가격 확인 가능 >> 가장 저렴한 연료별 평균 가격을 가진 브랜드 확인 가능

### 한계점

- 테이블 간 JOIN을 통한 새로운 테이블 생성하는 ELT 작업이 없음
- API를 사용하지 않고 수집한 데이터의 최신 업데이트 자동화 불가능
