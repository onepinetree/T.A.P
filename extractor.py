# 패키지 설치 및 설정
!pip install selenium
!apt-get update
!apt install -y chromium-chromedriver
!sudo apt-get install -y fonts-nanum
!sudo fc-cache -fv
!rm ~/.cache/matplotlib -rf


import sys
from selenium import webdriver
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 폰트 문제 해결
plt.rcParams['font.family'] = 'NanumBarunGothic'
plt.rcParams['axes.unicode_minus'] = False
sns.set(font="NanumBarunGothic", style="whitegrid")  # seaborn에도 폰트 설정

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

def extract_integers(s):
    return list(map(int, re.findall(r'\b\d+\b', s)))

def tanagement_link_to_distance_list(link) -> list:

      # 웹 드라이버 실행 및 웹 페이지 접근
      wd = webdriver.Chrome(options=chrome_options)
      wd.get(link) #input<---------------- Tanagement 링크 붙여넣기 input으로 받음.

      # 원하는 요소가 나타날 때까지 대기 및 요소 찾기
      wait = WebDriverWait(wd, 5000)

      #반응형프로그램을 생각해서 중심의 위치도 계속 가지고 와야함.즉, 중심이 고정이 아님(1이 욕구, 2가 행동판단)
      element_1_vertex = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#__next > div > section > div.sc-ivTmOn.bpCyiU.MuiBox-root > div > div.sc-ivTmOn.gfZTiV.MuiBox-root > div > div.sc-ivTmOn.jmJWWx.MuiBox-root > div.sc-ivTmOn.btHYOz.MuiBox-root > div > svg > g:nth-child(3)")))
      element_2_vertex = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#__next > div > section > div.sc-ivTmOn.bpCyiU.MuiBox-root > div > div.sc-ivTmOn.gfZTiV.MuiBox-root > div > div.sc-ivTmOn.jmJWWx.MuiBox-root > div.sc-ivTmOn.btHYOz.MuiBox-root > div > svg > g:nth-child(4) > g > path")))
      element_center = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#__next > div > section > div.sc-ivTmOn.bpCyiU.MuiBox-root > div > div.sc-ivTmOn.gfZTiV.MuiBox-root > div > div.sc-ivTmOn.jmJWWx.MuiBox-root > div.sc-ivTmOn.btHYOz.MuiBox-root > div > svg")))

      # JavaScript가 완전히 로드될 때까지 추가로 2초 대기(그 이하는 값 오류)
      import time
      time.sleep(2)

      # 결과 출력 (원래 코드)

      if element_center:
        #중심 좌표자료 처리
        element_center_html = element_center.get_attribute('outerHTML')
        center_data = element_center_html[8:22]
        center_coordinate_list = extract_integers(center_data)


        #꼭짓점(욕구) 좌표자료 처리
        element_1_vertex_html = element_1_vertex.get_attribute('outerHTML').split('d="M')
        vertex_1_data = element_1_vertex_html[1].split('Z"></path>')[0]
        vertex_1_coordinate_info_list = vertex_1_data.split('L')[:8]

        vertex_1_coordinate_list = []
        for object in vertex_1_coordinate_info_list:
          coordinate = object.split(',')
          vertex_1_coordinate_list.append(coordinate)


        #꼭짓점(행동판단) 좌표자료 처리
        element_2_vertex_html = element_2_vertex.get_attribute('outerHTML').split('d="M')
        vertex_2_data = element_2_vertex_html[1].split('Z"></path>')[0]
        vertex_2_coordinate_info_list = vertex_2_data.split('L')[:8]

        vertex_2_coordinate_list = []
        for object in vertex_2_coordinate_info_list:
          coordinate = object.split(',')
          vertex_2_coordinate_list.append(coordinate)

        #세개의 리스트의 정보를 통해서 중심과 꼭짓점평균 사이에 거리 구하기
        tanagement_value_list_desire = []
        tanagement_value_list_action = []

        center_x = center_coordinate_list[0]
        center_y = center_coordinate_list[1]

        for i in range(8):
          user_x = round(float(vertex_1_coordinate_list[i][0]),2)
          user_y = round(float(vertex_1_coordinate_list[i][1]),2)
          distance = math.sqrt((user_x - center_x)**2 + (user_y - center_y)**2)
          tanagement_value_list_desire.append(round(distance,1))

        for i in range(8):
          user_x = round(float(vertex_2_coordinate_list[i][0]),2)
          user_y = round(float(vertex_2_coordinate_list[i][1]),2)
          distance = math.sqrt((user_x - center_x)**2 + (user_y - center_y)**2)
          tanagement_value_list_action.append(round(distance,1))

      return [tanagement_value_list_desire, tanagement_value_list_action]







data_dict = {
    "홍시" : "https://tanagement.co.kr/bivwxbxuus",
    "쏠": "https://tanagement.co.kr/mvowvvdisw",
    "테이": "https://tanagement.co.kr/rqformephb",
    "콜라": "https://tanagement.co.kr/mlijzqelht",
    "플레이": "https://tanagement.co.kr/pclugjivyf",
    "소나무": "https://tanagement.co.kr/jjlbgpghec",
    "토니": "https://tanagement.co.kr/eluvtftgvj",
    "마에브": "https://tanagement.co.kr/axvphkocmo",
    "송": "https://tanagement.co.kr/tmdfagcnfi",
    "진": "https://tanagement.co.kr/zdqalmejjs",
    "에밀리": "https://tanagement.co.kr/yodiqzrvzr",
    "쥬디": "https://tanagement.co.kr/qodrmwrfuo",
    "에드": "https://tanagement.co.kr/hhtxzvrzoy",
    "앤드류": "https://tanagement.co.kr/pkfkuiduop",
    "용": "https://tanagement.co.kr/lzdbijdrfq",
    "에런": "https://tanagement.co.kr/hlwtkdtjsv",
    "세라": "https://tanagement.co.kr/bzxyzebehb",
    "조이" : "https://tanagement.co.kr/esphngtqzt",
    "엘라" : "https://tanagement.co.kr/hlrhluikon",
    "광덕" : "https://tanagement.co.kr/uqvsxwzqyb",
    "아키" : "https://tanagement.co.kr/eltyegysbs",
    "만보" : "https://tanagement.co.kr/vvyjacevng",
    "지구" : "https://tanagement.co.kr/vihfhkfmqp",
    "헤이" : "https://tanagement.co.kr/qtscnxkfjx",
    "코진" : "https://tanagement.co.kr/wgfseammir",
    "리니" : "https://tanagement.co.kr/hhrwygrjvl",
    "홍시" : "https://tanagement.co.kr/",
    "토드" : "https://tanagement.co.kr/",
    "이제" : "https://tanagement.co.kr/kmzbnqhulv"
    }

nickname_result_list = {}
for nickname, link in data_dict.items():
  nickname_result_list[nickname] = tanagement_link_to_distance_list(link)
print(nickname_result_list)
