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
