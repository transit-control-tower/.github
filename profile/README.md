<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/transit-control-tower/.github/main/assets/banners/banner-dark.png">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/transit-control-tower/.github/main/assets/banners/banner-light.png">
  <img src="https://raw.githubusercontent.com/transit-control-tower/.github/main/assets/banners/banner-light.png" alt="잠실 교통 혼잡 예측 — 현재, 60분 후, 120분 후 버스·지하철 혼잡 전망" width="100%">
</picture>

<div align="center">

# Transit Control Tower

**교통 데이터로 도시의 흐름을 읽고, 운영 판단을 돕습니다.**

잠실종합운동장 권역의 교통·행사·기상 데이터를 연결하는 관제탑5팀입니다.

[프로젝트 살펴보기](https://github.com/transit-control-tower/jamsil-transit-congestion-forecast) · [서비스·데이터 기준](https://github.com/transit-control-tower/jamsil-transit-congestion-forecast/blob/main/docs/JAMSIL_MVP_BASELINE.md)

</div>

---

## 🚦 잠실 교통 혼잡 예측

버스·지하철 승하차 관측과 행사·기상 정보를 결합하여 **현재·60분 후·120분 후의 상대 혼잡 위험**을 살펴보고, 공공 교통 운영 담당자의 대응 판단을 지원하는 프로젝트입니다.

| 📡 교통 현황 | 📈 혼잡 전망 | 🗺️ 통합 대시보드 |
| :--- | :--- | :--- |
| 권역 승하차 범위와 관측 시각 확인 | 교통수단별 위험 단계와 시간대 변화 확인 | 교통·행사·지도·참고 근거를 한 화면에 구성 |

## 🛠️ 우리가 만드는 것

- **데이터 파이프라인** — 원천 수집부터 정규화·품질 검사·저장까지 이어지는 처리 흐름
- **예측 모델** — 시간순 평가와 기준 모델 비교를 통한 재현 가능한 검증
- **운영 웹** — 현황과 예측 추이, 행사 정보를 연결하는 대시보드
- **근거 검색** — 공식 운영 문서와 대응 사례를 찾아 의사결정에 참고할 정보 제공

## ⚙️ 기술 스택

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/SQL-4169E1?style=flat-square&logo=postgresql&logoColor=white" alt="SQL">
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white" alt="TypeScript">
  <img src="https://img.shields.io/badge/Next.js-000000?style=flat-square&logo=nextdotjs&logoColor=white" alt="Next.js">
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Microsoft_Azure-0078D4?style=flat-square" alt="Microsoft Azure">
</p>

**Cloud & Data** · Azure Functions · Event Hubs · Stream Analytics  
**ML & Search** · Azure Machine Learning · Azure AI Search

## 📂 프로젝트 저장소

### [jamsil-transit-congestion-forecast ↗](https://github.com/transit-control-tower/jamsil-transit-congestion-forecast)

수집·전처리, ML 실험, 추론 파이프라인, 대시보드와 기술 문서를 함께 관리합니다.

[데이터 안내](https://github.com/transit-control-tower/jamsil-transit-congestion-forecast/blob/main/data/README.md) · [ML 검증 현황](https://github.com/transit-control-tower/jamsil-transit-congestion-forecast/blob/main/docs/ml/OFFLINE_MILESTONE.md)

---

**검증 가능한 데이터와 예측으로, 사람 중심의 교통 운영을 지원합니다.**
