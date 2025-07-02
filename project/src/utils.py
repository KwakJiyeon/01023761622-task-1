import xml.etree.ElementTree as ET
from collections import defaultdict, deque
from geopy.distance import geodesic
import numpy as np
import math

def parse_osm(osm_path):
    tree = ET.parse(osm_path)
    root = tree.getroot()
    nodes = {}
    ways = []
    for node in root.findall('node'):
        node_id = node.attrib['id']
        lat = float(node.attrib['lat'])
        lon = float(node.attrib['lon'])
        nodes[node_id] = (lat, lon)
    for way in root.findall('way'):
        way_id = None
        nds = [nd.attrib['ref'] for nd in way.findall('nd')]
        for tag in way.findall('tag'):
            if tag.attrib.get('k') == 'highway':
                way_id = int(way.attrib['id']) if 'id' in way.attrib else None
        if way_id:
            ways.append({'id': way_id, 'nodes': nds})
    return ways, nodes

def haversine(coord1, coord2):
    return geodesic(coord1, coord2).meters

def distance_point_to_segment(p, a, b):
    p, a, b = np.array(p), np.array(a), np.array(b)
    ab = b - a
    ap = p - a
    t = np.dot(ap, ab) / np.dot(ab, ab)
    t = max(0, min(1, t))
    closest = a + t * ab
    return np.linalg.norm(p - closest)

def build_way_adjacency(ways):
    node_to_ways = defaultdict(set)
    for way in ways:
        for node in way['nodes']:
            node_to_ways[node].add(way['id'])
    way_graph = defaultdict(set)
    for node, connected_ways in node_to_ways.items():
        for w1 in connected_ways:
            for w2 in connected_ways:
                if w1 != w2:
                    way_graph[w1].add(w2)
    return way_graph

def expand_expected_ways(expected_ids, way_graph, depth=2):
    visited = set(expected_ids)
    queue = deque([(wid, 0) for wid in expected_ids])
    while queue:
        current, d = queue.popleft()
        if d >= depth:
            continue
        for neighbor in way_graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, d + 1))
    return visited

def calculate_bearing(coord1, coord2):
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])
    dlon = lon2 - lon1
    x = math.sin(dlon) * math.cos(lat2)
    y = math.cos(lat1)*math.sin(lat2) - math.sin(lat1)*math.cos(lat2)*math.cos(dlon)
    bearing = math.atan2(x, y)
    bearing = math.degrees(bearing)
    return (bearing + 360) % 360

def angle_difference(a1, a2):
    diff = abs(a1 - a2) % 360
    return diff if diff <= 180 else 360 - diff

def is_valid_gps_point(row, max_distance, hdop_threshold, speed_threshold, angle_diff, distance):
    if row['HDOP'] > hdop_threshold:
        return False
    if row['Speed (km/h)'] < speed_threshold:
        return False
    if distance > max_distance:
        return False
    if angle_diff > 90:
        return False
    return True

def match_gps_with_strict_filter(gps_df, ways, nodes, expanded_way_ids, max_distance=20, hdop_threshold=3, speed_threshold=5):
    matched_way_ids = []
    deviation_flags = []

    for idx, row in gps_df.iterrows():
        gps_point = (row['Latitude'], row['Longitude'])
        gps_angle = row['Angle']
        min_dist = float('inf')
        matched_way_id = None
        matched_angle_diff = None

        for way in ways:
            node_ids = way['nodes']
            for i in range(len(node_ids) - 1):
                n1, n2 = nodes.get(node_ids[i]), nodes.get(node_ids[i+1])
                if not n1 or not n2:
                    continue
                dist = distance_point_to_segment(gps_point, n1, n2)
                if dist < min_dist:
                    road_angle = calculate_bearing(n1, n2)
                    angle_diff = angle_difference(gps_angle, road_angle)
                    min_dist = dist
                    matched_way_id = way['id']
                    matched_angle_diff = angle_diff

        is_valid = is_valid_gps_point(
            row, max_distance, hdop_threshold, speed_threshold, matched_angle_diff, min_dist
        )

        if is_valid and matched_way_id is not None:
            matched_way_ids.append(matched_way_id)
            deviation_flags.append(matched_way_id not in expanded_way_ids)
        else:
            matched_way_ids.append(None)
            deviation_flags.append(True)

    return matched_way_ids, deviation_flags