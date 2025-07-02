# 01023761622-task-1
# GPS 주행 판별 시스템

이 프로젝트는 GPS 데이터를 도로 망(OpenStreetMap) 기반으로 분석하여 주행 형태(직진, 좌회전, 우회전, 역주행)와 경로 이탈 여부를 판별하는 시스템입니다.

## 📁 폴더 구조
```
project_root/
│
├── data/
│   ├── roads.osm
│   ├── gps_left_turn.csv
│   ├── gps_straight01.csv
│   └── ... (총 10개 CSV)
│
├── utils.py              # 주요 기능 모듈
├── main_real_analysis.py # 실제 분석 결과 생성 코드
└── 실제_분석_결과표.csv    # 실행 후 생성되는 결과 요약 파일
```

## ⚙️ 실행 방법

1. `data/` 폴더에 `roads.osm` 및 모든 GPS CSV 파일들을 넣습니다.
2. `main_real_analysis.py` 파일을 실행합니다.
3. 실행 후, `실제_분석_결과표.csv` 파일이 생성됩니다.

```bash
python main_real_analysis.py
```

## 🧪 출력 예시 (`실제_분석_결과표.csv`)

| 파일명                  | 주행형태 | 판정결과 |
|------------------------|-----------|-----------|
| gps_left_turn.csv       | 좌회전    | 경로이탈  |
| gps_straight01.csv      | 직진      | 정상      |

## 🧠 주요 기능

- **OSM 기반 도로 매칭**: OpenStreetMap 도로와 GPS 좌표를 정밀하게 매칭
- **오차 필터링**: HDOP, 속도, 방향 각도 등을 기준으로 신뢰도 낮은 GPS 제거
- **경로 이탈 판정**: 예상 도로에서 벗어난 구간 여부 탐지

## 🛠 요구사항
- Python 3.7+
- pandas, numpy, geopy

## 🙋‍♂️ 문의
코드 및 결과 관련 질문은 언제든지 환영입니다!
