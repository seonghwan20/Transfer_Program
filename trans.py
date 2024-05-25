import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib import rc
import copy


font_name = fm.FontProperties(fname=r"C:\Users\Hwan\Desktop\project\nanum-gothic\NGULIM.TTF").get_name() #matplot 한글 깨짐 방지를 위해 폰트 설치
rc('font', family=font_name)


line1_time = [3.5, 1.5, 1.5, 1.5, 1.5, 1.5, 2.0, 2.0, 2.0, 2.0, 1.5, 1.5, 2.0, 1.5, 2.0, # 1호선 역간 소요시간
              1.5, 2.5, 2.0, 1.5, 2.0, 2.0, 2.0, 2.0, 1.0, 2.0, 3.0, 2.0, 2.5, 2.0, 2.0, 
              1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 2.5, 1.5, 1.0, 2.0, 2.0, 1.5, 2.0, 1.5, 
              2.0, 1.5, 1.5, 2.5, 2.0, 2.5, 2.0, 1.5, 2.0, 4.5, 3.0, 4.5, 1.5, 2.0, 2.0, 3.5, 4.5, 3.0, 7.5] 

line1_name = ['인천', '동인천', '도원', '제물포', '도화', '주안', '간석', '동암', '백운', '부평', # 1호선 역 이름
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

lines_all = [line1_name, line2_circle_name, line2_kka_name, line2_shin_name] #모든 호선 역 리스트
lines_time = [line1_time, line2_circle_time, line2_kka_time, line2_shin_time] #모든 호선 소요시간 리스트

trans_list = ['시청', '신도림', '신설동', '성수']

G = nx.Graph() #모든 역 포함 그래프
G_trans = nx.Graph() #환승역과 시점/종점 포함 그래프


#모든 역을 포함하는 그래프 G 만들기
for _ in range(len(line1_time)):
    G.add_edge(line1_name[_], line1_name[_+1], weight = line1_time[_])

for _ in range(len(line2_circle_time)):
    G.add_edge(line2_circle_name[_], line2_circle_name[_+1], weight = line2_circle_time[_])

for _ in range(len(line2_kka_time)):
    G.add_edge(line2_kka_name[_], line2_kka_name[_+1], weight = line2_kka_time[_])

for _ in range(len(line2_shin_time)):
    G.add_edge(line2_shin_name[_], line2_shin_name[_+1], weight = line2_shin_time[_])


#환승역과 시점/종점 포함 그래프 G_trans 만들기
start_point = input("출발지를 입력하세요: ")
end_point = input("목적지를 입력하세요: ")


#시점/종점도 입력받아 trans_list에 추가 -> G_trans 만들기위해
if start_point in trans_list:
    pass
else:
    trans_list.append(start_point)

if end_point in trans_list:
    pass
else:
    trans_list.append(end_point)

#아래 반복문을 위한 station list 생성
excluded_list = copy.deepcopy(trans_list)

#trans_list에 있는 station 검색하면서 두 역이 같은 line에 있다면 G_trans 그래프의 vertex로 추가
for station in trans_list:
    excluded_list.remove(station)
    for line in lines_all:
        if station in line:
            for another_station in excluded_list:
                time_travel = 0
                if another_station in line:
                    idx1 = line.index(station)
                    idx2 = line.index(another_station)
                    current_line_index = lines_all.index(line)
                    if idx2 < idx1:
                        idx1, idx2 = idx2, idx1
                    for idx in range(idx1, idx2):
                        time_travel += lines_time[current_line_index][idx] #두 station의 index 찾아 소요시간 구함 (문제점: 2호선 같은 경우는 순환형이라 문제생김.)
                     
                    G_trans.add_edge(station, another_station, weight = time_travel)
                    time_travel = 0



#G_trans 그래프 그리기
pos = nx.spring_layout(G_trans)
weight = nx.get_edge_attributes(G_trans, 'weight')
nx.draw(G_trans, pos=pos, with_labels=True, font_family=font_name)
nx.draw_networkx_edge_labels(G_trans, pos, edge_labels=weight) 
plt.show()