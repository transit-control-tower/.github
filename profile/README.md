<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/hero-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/hero-light.svg">
  <img src="assets/hero-light.svg" alt="Transit Control Tower — 관제탑5팀. 교통 데이터로 도시의 흐름을 읽고, 운영 판단을 돕습니다." width="100%">
</picture>

<p align="center">
  <a href="#잠실-교통-혼잡-예측">대표 프로젝트</a> &nbsp;·&nbsp;
  <a href="#시스템-노선도">시스템 노선도</a> &nbsp;·&nbsp;
  <a href="#혼잡-점수를-읽는-기준">혼잡 점수 기준</a> &nbsp;·&nbsp;
  <a href="#개발-운행-현황">개발 현황</a> &nbsp;·&nbsp;
  <a href="#기술-스택">기술 스택</a>
</p>

관제탑5팀은 잠실종합운동장 일대처럼 **행사 하나로 교통 흐름이 바뀌는 곳**에서, 운영 담당자가 조금 더 일찍 상황을 알아차릴 수 있도록 돕는 팀입니다.
버스·지하철 승하차, 공연·경기 일정, 날씨를 한 화면에 모으고, 앞으로 두 시간의 혼잡 위험과 그 판단에 참고할 공식 근거를 함께 보여줍니다.

<br>

## 잠실 교통 혼잡 예측

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.png">
  <source media="(prefers-color-scheme: light)" srcset="assets/banner-light.png">
  <img src="assets/banner-light.png" alt="잠실 교통 혼잡 예측 — 현재, 60분 후, 120분 후 버스·지하철 혼잡 전망" width="100%">
</picture>

잠실종합운동장 권역의 버스·지하철 승하차, 공연·행사, 기상 정보를 결합해 **현재·60분 후·120분 후의 상대 혼잡 위험**을 예측하고, 공공 교통 운영 담당자의 대응 판단을 지원합니다.

| 무엇을 | 어떻게 |
| --- | --- |
| **누구를 위해** | 공공 교통 운영기관의 관리·운영 담당자 (B2G) |
| **어디를** | 잠실종합운동장과 2호선 종합운동장역 주변 |
| **무엇을 예측하나** | 버스·지하철의 현재(0분)·60분 후·120분 후 혼잡 점수와 위험 단계 |
| **무엇으로 배우나** | 2025-01-01 ~ 2026-06-30 시간 단위 승하차 + 행사·공휴일·날씨 |
| **지금 무엇을 보나** | 서울시 실시간 도시데이터(OA-21285)의 권역 승하차 범위, 5분 단위 집계 |

### 담당자가 대시보드에서 하는 일

| 확인하기 | 내다보기 | 근거 찾기 |
| --- | --- | --- |
| 권역 승하차 범위와 가장 최근 관측 시각 | 교통수단별 위험 단계와 2시간 동안의 변화 | 공식 운영 매뉴얼과 비슷한 대응 사례 |

<br>

## 시스템 노선도

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/route-map-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/route-map-light.svg">
  <img src="assets/route-map-light.svg" alt="시스템 노선도. 실시간 관측 노선: 도시데이터 OA-21285, Azure Functions, Event Hubs, Stream Analytics, PostgreSQL. 혼잡 예측 노선: 날씨·행사·공휴일, Inference Function, Azure ML. 근거 검색 노선: 운영 매뉴얼·사례, Azure AI Search, RAG API. 세 노선은 운영 웹 대시보드에서 만납니다." width="100%">
</picture>

세 개의 노선이 하나의 대시보드로 모입니다.

- **실시간 관측** — 서울시 도시데이터를 5분마다 수집해 Event Hubs와 Stream Analytics로 집계하고 PostgreSQL에 저장합니다.
- **혼잡 예측** — 집계된 관측에 날씨·행사·공휴일 조건을 더해 Azure ML로 혼잡 점수를 산출하고, 결과를 다시 저장합니다.
- **근거 검색** — 공식 운영 매뉴얼과 과거 대응 사례를 Azure AI Search로 찾아, 판단에 참고할 근거로 함께 보여줍니다.

<br>

## 혼잡 점수를 읽는 기준

> [!IMPORTANT]
> **혼잡 점수(0~100)는 상대 혼잡 위험을 나타내는 내부 지표입니다.**
> 객차 탑승률, 실제 점유율(%), 확정 승하차 인원, 혼잡 발생 확률을 뜻하지 않습니다.

우리는 예측이 그럴듯해 보이는 것보다 **어디까지 믿을 수 있는지 분명한 것**을 더 중요하게 봅니다.

| 원칙 | 실제로 지키는 방식 |
| --- | --- |
| 단위가 다른 자료를 섞지 않습니다 | 과거 1시간 역·정류소 자료와 실시간 5분 권역 관측은 합산하거나 같은 실측값으로 취급하지 않습니다 |
| 범위는 범위로 보여줍니다 | 실시간 승하차는 최소·최대 **범위**로 관측되므로, 하나의 숫자로 바꾸지 않습니다 |
| 추정은 추정이라고 표시합니다 | 버스 시간대 배분량을 실측값으로 표시하지 않고, 확인되지 않은 수집 시각은 비워 둡니다 |
| 최종 판단은 사람이 합니다 | 시스템은 위험 신호와 공식 근거를 제시하고, 운영 결정은 담당자가 내립니다 |

<br>

## 개발 운행 현황

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/roadmap-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/roadmap-light.svg">
  <img src="assets/roadmap-light.svg" alt="개발 운행 현황. 구현: MVP 기준 수립, 수집·전처리(PR #7), ML 재구성(PR #2), 추론 파이프라인(PR #1). 진행 중: 운영 웹 대시보드. 예정: 통합 검증." width="100%">
</picture>

| 구간 | 한 일 | 기록 |
| --- | --- | --- |
| 수집·전처리 | 원천별 정규화, CSV/XLSX 재실행, 다중 월 스냅샷, 시간축·품질 검사 | PR #7 |
| ML 재구성 | 기준 코드 복원, Pipeline·시간순 평가, 월별 이용량 평가와 오류 진단 | PR #2 |
| 추론 파이프라인 | PostgreSQL 기반 추론 Function, DB 스키마와 알림 연동 | PR #1 |

개선 모델은 오프라인 진단용이며, 실시간 추론·배포 모델의 성능으로 해석하지 않습니다. 클라우드 상시 가동과 종단 간 연동은 통합 검증 단계에서 확인합니다.

<br>

## 데이터 출처

| 데이터 | 원천 | 쓰임 |
| --- | --- | --- |
| 과거 지하철 | 서울교통공사 종합운동장역 시간대별 승하차 | 1시간 단위 패턴 학습 |
| 과거 버스 | 서울시 OA-12913(시간대별) · OA-12912(일일 합계) | 학습 피처·총량 검증 |
| 지하철 검증 | 서울시 OA-12914(일일 합계) | 일일 총량·이상치 검증 |
| 실시간 승하차 | 서울시 OA-21285 `LIVE_SUB_PPLTN` · `LIVE_BUS_PPLTN` | 최근 구간 승하차 범위 관측 |
| 행사·공휴일 | KBO, KOPIS, 서울시 문화행사, 공휴일 자료 | 행사·달력 피처 |
| 날씨 | 기상자료개방포털, 도시데이터 날씨 영역 | 기상 조건 피처 |

<br>

## 기술 스택

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/stack-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/stack-light.svg">
  <img src="assets/stack-light.svg" alt="기술 스택. 데이터 흐름: Azure Functions, Azure Event Hubs, Azure Stream Analytics, PostgreSQL. 예측 모델: Python, Azure Machine Learning, SQL. 근거·운영 웹: Azure AI Search, Next.js, TypeScript." width="100%">
</picture>

<br>

## 저장소

| 저장소 | 내용 |
| --- | --- |
| [**jamsil-transit-congestion-forecast**](https://github.com/transit-control-tower/jamsil-transit-congestion-forecast) | 수집·전처리, ML 실험, 추론 파이프라인, 대시보드, 기술 문서 |

## 팀

| <img src="https://github.com/soniiiiij.png" width="72" alt="soniiiiij"> | <img src="https://github.com/uuhlynn-oss.png" width="72" alt="uuhlynn-oss"> |
| :---: | :---: |
| [**soniiiiij**](https://github.com/soniiiiij) | [**uuhlynn-oss**](https://github.com/uuhlynn-oss) |


<br>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/footer-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/footer-light.svg">
  <img src="assets/footer-light.svg" alt="검증 가능한 데이터와 예측으로, 사람 중심의 교통 운영을 지원합니다." width="100%">
</picture>
