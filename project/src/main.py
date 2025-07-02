import pandas as pd
from utils import parse_osm, build_way_adjacency, expand_expected_ways, match_gps_with_strict_filter
import os

# 분석 대상 파일들과 그에 맞는 주행 형태 정의
file_info = {
    "gps_left_turn.csv": "좌회전",
    "gps_left02_turn.csv": "좌회전",
    "gps_reverse_direction.csv": "역주행",
    "gps_right_turn_01.csv": "우회전",
    "gps_right02_turn..csv": "우회전",
    "gps_straight01.csv": "직진",
    "gps_straight02.csv": "직진",
    "gps_straight03.csv": "직진",
    "gps_straight04.csv": "직진",
    "gps_multipath.csv": "직진",
}

# 예상 도로 ID (문제에서 주어진)
expected_ids = {521766182, 990628459, 472042763, 218864485, 520307304}

# OSM 파일 및 도로 정보 파싱
osm_path = "data/roads.osm"
ways, nodes = parse_osm(osm_path)
way_graph = build_way_adjacency(ways)
expanded_way_ids = expand_expected_ways(expected_ids, way_graph, depth=2)

# 결과 저장용 리스트
results = []

# 모든 파일 분석
for filename, drive_type in file_info.items():
    csv_path = os.path.join("data", filename)
    gps_df = pd.read_csv(csv_path)
    matched_ids, deviations = match_gps_with_strict_filter(gps_df, ways, nodes, expanded_way_ids)
    gps_df['Matched_Way_ID'] = matched_ids
    gps_df['Deviation'] = deviations

    # 판정 결과
    is_deviated = any(deviations)
    result = "경로이탈" if is_deviated else "정상"
    results.append({
        "파일명": filename,
        "주행형태": drive_type,
        "판정결과": result
    })

# 최종 결과 저장
final_df = pd.DataFrame(results)
final_df.to_csv("최종_판정_결과_테이블.csv", index=False)
print("✅ 최종 판정 결과가 '최종_판정_결과_테이블.csv'에 저장되었습니다.")