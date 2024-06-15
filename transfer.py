import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib import rc
import copy
import heapq
import copy

font_name = fm.FontProperties(fname=r"C:\Users\Hwan\Transfer_Program\nanum-gothic\NGULIM.TTF").get_name() #matplot 한글 깨짐 방지를 위해 폰트 설치
rc('font', family=font_name)

# 데이터 초기화
line1_time = [3.5, 1.5, 1.5, 1.5, 1.5, 1.5, 2.0, 2.0, 2.0, 2.0, 1.5, 1.5, 2.0, 1.5, 2.0, 
              1.5, 2.5, 2.0, 1.5, 2.0, 2.0, 2.0, 2.0, 1.0, 2.0, 3.0, 2.0, 2.5, 2.0, 2.0, 
              1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 2.5, 1.5, 1.0, 2.0, 2.0, 1.5, 2.0, 1.5, 
              2.0, 1.5, 1.5, 2.5, 2.0, 2.5, 2.0, 1.5, 2.0, 4.5, 3.0, 4.5, 1.5, 2.0, 2.0, 3.5, 4.5, 3.0, 7.5] 

line1_name = ['인천', '동인천', '도원', '제물포', '도화', '주안', '간석', '동암', '백운', '부평', 
              '부개', '송내', '중동', '부천', '소사', '역곡', '온수', '오류동', '개봉', '구일', '구로', 
              '신도림', '영등포', '신길', '대방', '노량진', '용산', '남영', '서울역', '시청', '종각', '종로3가', 
              '종로5가', '동대문', '동묘앞', '신설동', '제기동', '청량리', '회기', '외대앞', '신이문', '석계', 
              '광운대', '월계', '녹천', '창동', '방학', '도봉', '도봉산', '망월사', '회룡', '의정부', '가능', 
              '녹양', '양주', '덕계', '덕정', '지행', '동두중', '보산', '동두천', '소요산', '청산', '전곡', '연천']

line2_circle_time = [1.5, 1.0, 1.0, 1.5, 1.5, 1.0, 1.0, 1.5, 1.5, 1.0, 1.5, 2.0, 1.0, 2.0, 1.5, 
              1.5, 1.5, 1.5, 1.5, 1.5, 1.0, 1.5, 1.0, 2.0, 2.5, 2.0, 1.5, 1.0, 1.5, 
              2.0, 1.5, 1.5, 2.5, 2.0, 1.0, 1.5, 2.5, 1.5, 2.0, 1.0, 1.0, 1.5, 1.5 
              ]

line2_circle_name = ['시청', '을지로입구', '을지로3가', '을지로4가', 
                     '동대문역사문화공원', '신당', '상왕십리', 
                     '왕십리', '한양대', '뚝섬', '성수', 
                     '건대입구', '구의', '강변', '잠실나루', '잠실',
                     '잠실새내', '종합운동장', '삼성', '선릉', 
                     '역삼', '강남', '교대', '서초', '방배', 
                     '사당', '낙성대', '서울대입구', '봉천', 
                     '신림', '신대방', '구로디지털단지', '대림', 
                     '신도림', '문래', '영등포구청', '당산', '합정', 
                     '홍대입구', '신촌', '이대', '아현', '충정로', '시청']

line2_kka_time = [1.5, 2.5, 3.0, 2.5]
line2_kka_name = ['신도림', '도림천', '양천구청', 
                  '신정네거리', '까치산']

line2_shin_time = [3.0, 1.5, 1.5, 1.5]
line2_shin_name = ['성수', '용답', '신답', '용두', '신설동']

lines_all = [line1_name, line2_circle_name, line2_kka_name, line2_shin_name]
lines_time = [line1_time, line2_circle_time, line2_kka_time, line2_shin_time]

trans_list = ['시청', '신도림', '신설동', '성수']

# 그래프 생성
graph = {}

def add_edge(graph, from_node, to_node, weight):
    if from_node not in graph:
        graph[from_node] = []
    if to_node not in graph:
        graph[to_node] = []
    graph[from_node].append((to_node, weight))
    graph[to_node].append((from_node, weight))

# 출발지와 목적지 입력
start_point = input("출발지를 입력하세요: ")
end_point = input("목적지를 입력하세요: ")

# 시점/종점도 입력받아 trans_list에 추가
if start_point not in trans_list:
    trans_list.append(start_point)
if end_point not in trans_list:
    trans_list.append(end_point)

excluded_list = copy.deepcopy(trans_list)
time_travel = 0 

# 순환노선의 경우 시계방향(index 방향), 반시계 방향(index의 역방향)의 경우를 따로 계산해 최소시간으로 설정
def select(current_line_index, idx_station, idx_another_station): 
    global time_travel
    time_clockwise = 0
    time_anticlockwise = 0
     
    if idx_another_station < idx_station:
        idx_station, idx_another_station = idx_another_station, idx_station
    for idx in range(idx_station, idx_another_station):
        time_clockwise += lines_time[current_line_index][idx] 
     
    for idx in range(0, idx_station):
        time_anticlockwise += lines_time[current_line_index][idx]
    for idx in range(idx_another_station, 43):
        time_anticlockwise += lines_time[current_line_index][idx]
    
    if time_clockwise < time_anticlockwise:
        time_travel = time_clockwise
    else:
        time_travel = time_anticlockwise
        
# 비순환노선의 경우 index 방향으로 계산       
def time(idx_station, idx_another_station):
    global time_travel
    if idx_another_station < idx_station:
        idx_station, idx_another_station = idx_another_station, idx_station
    for idx in range(idx_station, idx_another_station):
        time_travel += lines_time[current_line_index][idx] 

# trans_list에 있는 station 검색하면서 두 역이 같은 line에 있다면 그래프에 추가
for station in trans_list:
    excluded_list.remove(station)
    for line in lines_all:
        if station in line:
            for another_station in excluded_list:
                if another_station in line:
                    idx_station = line.index(station)
                    idx_another_station = line.index(another_station)
                    current_line_index = lines_all.index(line)
                    if current_line_index == 1:
                        select(current_line_index, idx_station, idx_another_station)
                    else:
                        time(idx_station, idx_another_station)
                     
                    add_edge(graph, station, another_station, time_travel)
                    time_travel = 0

# 데이크스트라 알고리즘 구현
def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    priority_queue = [(0, start)]
    shortest_path = {node: [] for node in graph}
    lines_path = {node: [] for node in graph}  # 경로에 포함된 호선 저장

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))
                shortest_path[neighbor] = shortest_path[current_node] + [current_node]

                # 호선 정보 추가
                for line_index, line in enumerate(lines_all):
                    if current_node in line and neighbor in line:
                        line_name = f"{line_index + 1}호선" if line_index < 1 else f"2호선"  # 호선 정보 수정
                        lines_path[neighbor] = lines_path[current_node] + [line_name]
                        break

    return distances, shortest_path, lines_path

# 최단 경로 찾기
distances, shortest_path, lines_path = dijkstra(graph, start_point)
shortest_route = shortest_path[end_point] + [end_point]
shortest_time = distances[end_point]
shortest_lines = lines_path[end_point]  # 경로에 포함된 호선

# 환승 정보 출력
transfer_info = []
previous_line = shortest_lines[0]
for i in range(1, len(shortest_lines)):
    current_line = shortest_lines[i]
    if current_line != previous_line:
        transfer_station = shortest_route[i]
        transfer_info.append(f"{transfer_station}에서 {previous_line}에서 {current_line}으로 환승")
        previous_line = current_line

# 최단 경로와 시간 출력
print(f"최단 경로: {' -> '.join(shortest_route)}")
print(f"소요 시간: {shortest_time}분")

if transfer_info:
    print("환승 정보:")
    for info in transfer_info:
        print(info)
else:
    print("환승 없음")


#그래프 그리기

def visualize_graph(graph, shortest_route):
    G = nx.Graph()

    # 노드와 엣지를 그래프에 추가
    for node in graph:
        G.add_node(node)
    for node, edges in graph.items():
        for edge in edges:
            G.add_edge(node, edge[0], weight=edge[1])

    pos = nx.spring_layout(G)  # 노드의 위치를 설정

    # 노드와 엣지 그리기
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500, font_size=10, font_family=font_name)

    # 최단 경로 강조
    path_edges = list(zip(shortest_route, shortest_route[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)
    
    # 최단 경로 노드 강조
    nx.draw_networkx_nodes(G, pos, nodelist=shortest_route, node_color='red')

    weight = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=weight)
    plt.show()

# 그래프 시각화 함수 호출
visualize_graph(graph, shortest_route)