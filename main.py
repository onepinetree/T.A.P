# 패키지 설치 및 설정
!sudo apt-get install -y fonts-nanum
!sudo fc-cache -fv
!rm ~/.cache/matplotlib -rf
!apt -qq -y install fonts-nanum
!apt-get update -qq
!apt-get install fonts-nanum* -qq
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 폰트 경로 설정
fontpath = '/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf'
font = fm.FontProperties(fname=fontpath, size=10)

# 폰트 설정
plt.rc('font', family='NanumBarunGothic')

# 설치된 폰트 확인
system_fonts = fm.findSystemFonts(fontpaths=None, fontext='ttf')

# 'Nanum'이 들어간 폰트만 선택
nanum_fonts = [f for f in system_fonts if 'Nanum' in f]
print(f"nanum_fonts: {nanum_fonts}")

# 폰트 경로 직접 지정 (일반적으로 'NanumBarunGothic.ttf'를 많이 사용합니다. 여기서는 리스트의 첫 번째를 사용하였습니다.)
font_path = nanum_fonts[0]

# matplotlib의 폰트 관련 설정
plt.rc('font', family='NanumBarunGothic')

# ---여기서 부터는 기존 코드 ---



import pandas as pd
import numpy as np
import sys
import re
import math
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 폰트 문제 해결
plt.rcParams['font.family'] = 'NanumBarunGothic'
plt.rcParams['axes.unicode_minus'] = False
sns.set(font="NanumBarunGothic", style="whitegrid")  # seaborn에도 폰트 설정

class TAP:

    student_num = 0

    def __init__(self):
      '''학생 인스턴스가 들어있는 메소드'''
      self.students = {}

    def add_student(self, nickname, list_desire, list_action):
        self.students[nickname] = Student(nickname, list_desire, list_action)
        self.student_num += 1

    def get_student_data(self, nickname):
        return self.students[nickname].distance_data if nickname in self.students else None

    def group_analysis(self):
        labels = ["추진", "완성", "조정", "평가", "탐구", "창조", "동기부여", "외교"]
        action_df = pd.DataFrame(data = self.prepare_students_data('action'), index = labels)
        action_df = action_df.T

        desire_df = pd.DataFrame(data = self.prepare_students_data('desire'), index = labels)
        desire_df = desire_df.T
        desire_df.loc['총합', :] =  desire_df.sum(axis = 'index')
        desire_df.loc['총합', :] = desire_df.loc['총합', :]/2

        value_sum_array = list(desire_df.loc['총합', :])
        self.graph_drawer(value_sum_array)

        #장점 시너지 파악
        best_value = (desire_df.loc['총합',:].T).sort_values(ascending = False).index[0]
        print("이 팀은 {}으로 시너지를 발휘합니다".format(best_value))
        #보완 시너지 파악
        weak_values = list((desire_df.loc['총합',:].T).sort_values().index[0:3])
        i = 0
        for value in weak_values:
          front = '가장' if i == 0 else '그다음'
          desire_max_student = desire_df.drop('총합', axis=0)[value].sort_values(ascending=False).index[0]
          action_max_student = action_df[value].sort_values(ascending=False).index[:2]
          print("{} 부족한 부분은 {}, 그 특징에서 행동판단강점MAX:{}, {} 욕구강점MAX: {}, ".format(front, value, action_max_student[0],action_max_student[1], desire_max_student))
          print()
          i += 1

    def show_all_student_graph(self):
        for nickname, student_instance in self.students.items():
          self.graph_drawer(student_instance.distance_list_desire, nickname = nickname)

    @staticmethod
    def graph_drawer(distance_list, nickname = '전체 팀'):
        labels = ["추진", "완성", "조정", "평가", "탐구", "창조", "동기부여", "외교"]

        # 특정 경고 메시지 필터링
        import warnings
        warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")
        warnings.filterwarnings("ignore")

        # Seaborn을 사용한 바 그래프 그리기
        sns.barplot(x=labels, y=distance_list, palette="BuGn")

        # 각 막대에 대한 수치를 추가
        ax = plt.gca()
        for index, value in enumerate(distance_list):
          ax.text(index, value + 0.5, str(round(value, 1)), ha='center', va='center')  # 0.5는 수치의 위치를 조절하기 위한 값입니다.

        # 그래프 제목과 레이블 추가
        plt.title(f'{nickname}의 TAP 결과')
        plt.ylabel('수치')
        warnings.filterwarnings("ignore")

        # 그래프 표시
        plt.show()
        warnings.filterwarnings("ignore")

    def prepare_students_data(self, type):
      labels = ["추진", "완성", "조정", "평가", "탐구", "창조", "동기부여", "외교"]
      students_data = {}

      if type == 'desire':
        for nickname, student_instance in self.students.items():
          students_data[nickname] = student_instance.distance_list_desire
      else:
        for nickname, student_instance in self.students.items():
          students_data[nickname] = student_instance.distance_list_action

      return students_data



class Student:
    def __init__(self, nickname, list_desire, list_action):
        self.nickname = nickname
        self.distance_list_desire = list_desire
        self.distance_list_action = list_action





# 메인 함수:
def main():

    data_dict = {
    '쏠': [[53.6, 40.3, 94.3, 46.5, 70.0, 53.6, 52.7, 31.9], [63.8, 24.4, 22.1, 60.7, 56.7, 93.4, 63.3, 58.5]],
    '테이': [[68.6, 35.4, 60.2, 94.3, 89.9, 34.1, 24.4, 35.9], [56.7, 10.6, 53.1, 64.7, 86.4, 71.7, 66.0, 33.7]],
    '콜라': [[40.3, 31.0, 74.0, 52.7, 40.7, 75.3, 64.2, 64.2], [12.0, 54.0, 94.3, 70.9, 56.2, 82.4, 28.8, 44.3]],
    '플레이': [[70.0, 17.7, 45.2, 55.8, 68.6, 46.5, 50.0, 89.0], [57.6, 44.7, 40.7, 70.9, 73.1, 32.8, 68.6, 54.5]],
    '소나무': [[12.4, 64.7, 49.2, 69.1, 65.1, 73.5, 46.5, 62.4], [30.6, 79.3, 97.0, 87.2, 68.2, 62.0, 4.0, 14.2]],
    '토니': [[46.1, 44.7, 93.4, 62.0, 75.7, 83.7, 20.4, 16.4], [50.9, 78.8, 54.5, 87.7, 43.4, 16.8, 81.5, 29.2]],
    '마에브': [[60.2, 65.5, 64.2, 81.5, 49.2, 44.3, 16.4, 61.6], [27.0, 42.5, 86.4, 98.3, 79.7, 52.7, 12.0, 43.8]],
    '송': [[22.1, 71.7, 83.7, 79.3, 62.0, 33.2, 47.4, 43.4], [31.9, 79.3, 65.5, 93.0, 80.6, 17.3, 40.3, 34.5]],
    '진': [[42.5, 26.1, 67.3, 46.5, 59.8, 62.4, 53.1, 85.0], [44.7, 67.3, 68.2, 44.3, 74.0, 21.3, 36.3, 86.4]],
    '에밀리': [[93.0, 89.9, 81.9, 47.8, 67.8, 23.0, 21.7, 17.7], [85.5, 124.0, 69.5, 43.4, 55.8, 14.2, 14.6, 19.9]],
    '쥬디': [[47.8, 77.1, 46.1, 30.6, 33.2, 26.1, 124.0, 46.5], [25.7, 24.4, 27.5, 66.9, 31.0, 78.4, 114.3, 74.8]],
    '에드': [[22.6, 116.9, 62.0, 55.8, 30.6, 27.0, 63.3, 64.7], [8.4, 59.8, 57.1, 74.4, 35.0, 64.7, 74.0, 69.5]],
    '앤드류': [[87.2, 52.3, 93.4, 30.1, 40.3, 64.2, 31.4, 44.3], [75.7, 60.7, 58.5, 65.1, 73.5, 75.7, 10.6, 23.0]],
    '용': [[11.5, 52.3, 30.1, 66.4, 95.7, 26.1, 84.6, 76.6], [6.2, 48.7, 23.9, 77.9, 64.7, 65.5, 124.0, 25.2]],
    '애런': [[60.2, 10.6, 34.5, 54.9, 64.7, 83.7, 55.8, 78.8], [19.9, 58.5, 54.0, 56.7, 51.8, 73.1, 50.5, 78.4]],
    '세라': [[55.4, 44.7, 36.3, 42.5, 40.7, 60.7, 56.2, 105.8], [16.4, 26.6, 61.1, 88.1, 78.4, 84.1, 33.7, 54.0]],
    '조이': [[36.3, 35.0, 71.7, 83.7, 57.6, 29.2, 80.6, 48.7], [8.0, 50.5, 69.1, 61.6, 114.7, 65.5, 30.6, 42.5]],
    '엘라': [[58.0, 66.4, 84.1, 38.5, 35.0, 45.6, 30.1, 84.1], [56.2, 68.2, 75.7, 63.3, 65.1, 51.8, 25.2, 38.1]],
    '광덕': [[27.5, 31.4, 44.3, 62.0, 96.5, 80.2, 34.5, 66.0], [37.6, 29.7, 49.6, 64.2, 46.5, 89.9, 47.8, 78.4]],
    '아키': [[23.5, 75.3, 92.1, 46.1, 81.5, 21.7, 37.6, 64.7], [60.2, 11.5, 52.7, 56.7, 107.6, 76.2, 63.3, 14.6]],
    '만보': [[14.6, 63.8, 39.9, 88.6, 82.8, 77.9, 19.9, 55.4], [11.1, 30.6, 32.3, 28.8, 104.5, 88.1, 97.0, 49.6]],
    '지구': [[12.4, 65.5, 35.9, 33.2, 56.7, 62.9, 77.9, 98.3], [11.1, 24.4, 62.4, 40.7, 47.4, 107.6, 84.1, 65.1]],
    '헤이': [[48.3, 46.1, 35.4, 27.0, 40.7, 47.8, 77.1, 120.0], [39.0, 29.7, 67.3, 30.1, 27.0, 66.4, 70.9, 112.5]],
    '코진': [[43.4, 62.0, 53.1, 58.5, 65.5, 78.8, 33.2, 48.3], [60.7, 62.9, 31.9, 53.6, 46.1, 58.5, 76.2, 53.1]],
    '리니': [[95.7, 22.6, 64.2, 51.4, 48.3, 60.2, 40.7, 59.3], [50.0, 78.4, 62.0, 91.7, 64.7, 14.6, 32.3, 49.2]],
    '토드': [[47.8, 41.2, 36.8, 50.0, 34.1, 82.4, 99.6, 50.9], [53.6, 85.9, 94.3, 88.6, 45.2, 15.5, 17.7, 42.1]],
    '이제': [[26.1, 46.9, 37.6, 43.4, 58.5, 83.7, 82.4, 64.2], [27.5, 62.4, 36.8, 89.5, 66.0, 76.2, 66.9, 17.7]],
    '홍시': [[58.5, 73.1, 73.5, 53.1, 65.5, 54.5, 17.7, 46.9], [42.1, 54.9, 17.7, 67.3, 56.2, 57.6, 88.6, 58.0]]
      }


    tap = TAP()

    while True:
        print("\nTAP 분석 프로그램")
        print("1. 팀원 추가")
        print("2. 개별 팀원 분석 결과 보기")
        print("3. 전체 팀원 분석 결과 보기")
        print("4. 종료")
        choice = input("원하는 번호를 선택하세요: ")

        if choice == "1":
          while True:
              nickname = input("닉네임을 입력하세요: ")
              if nickname in data_dict.keys():
                break
              else:
                print("닉네임이 틀렸습니다. 다시 입력해주세요.")
                continue
          tap.add_student(nickname, data_dict[nickname][0], data_dict[nickname][1])
          print(f"{nickname} 팀원이 추가되었습니다.")

        elif choice == "2":
            tap.show_all_student_graph()

        elif choice == "3":
            print("전체 {}명의 팀원의 시너지 분석을 시작합니다.".format(tap.student_num))
            tap.group_analysis()

        elif choice == "4":
            print("프로그램을 종료합니다.")
            break

        else:
            print("올바른 번호를 선택하세요.")

if __name__ == "__main__":
  main()

