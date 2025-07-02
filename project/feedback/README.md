
# 과제 1 - Map Matching 및 경로 이탈 판단

## ✅ 개요
GPS 로그 데이터를 기반으로 차량이 실제 도로 위를 주행하고 있는지, 또는 경로를 이탈했는지를 판단하는 시스템입니다.

## 📁 폴더 구조
```
map-matching-task-1/
├── data/              # GPS CSV 로그 및 roads.osm 파일 위치
├── feedback/          # 평가자 피드백 문서 위치
├── src/               # 소스 코드 (main.py, utils.py 등)
```

## ⚙️ 실행 방법
1. Python 3.x 환경에서 아래 라이브러리를 설치하세요.
```
pip install pandas geopy
```

2. `src/main.py` 파일을 실행하면 각 GPS 로그에 대한 경로 매칭 결과가 출력됩니다.

## 🔍 주요 기능
- OSM(XML) 도로망 파싱
- 선분-점 거리 기반 GPS → 도로 매칭
- HDOP 기준 오차 필터링
- 지정된 Way ID 기반 경로 이탈 여부 판단
- Way 인접성 기반 경로 확장 판단
