"""
BIA/BIS 탐색적 분석 Tool
메인 진입점 (app.py)

이 파일은 사이드바 메뉴를 표시하고,
선택된 메뉴에 맞는 화면(pages_logic 폴더 안의 파일)을 호출하는 역할만 합니다.
실제 분석 로직은 각 pages_logic/*.py 파일에 있습니다.
"""

import streamlit as st

from pages_logic import (
    correlation,
    explore,
    group_compare,
    literature_reference,
    overview,
    repeated_measure,
    upload,
)

# 브라우저 탭 제목, 레이아웃 설정
st.set_page_config(
    page_title="BIA/BIS 탐색적 분석 Tool",
    layout="wide",
)

# 사이드바 메뉴 목록
# 아직 구현되지 않은 메뉴는 "준비 중" 안내만 표시됨
MENU_LIST = [
    "데이터 업로드",
    "데이터 구조 확인",
    "변수 탐색",
    "상관분석",
    "그룹 비교",
    "반복측정 분석",
    "문헌 기반 분석",
]

st.sidebar.title("BIA/BIS 분석 Tool")
selected_menu = st.sidebar.radio("메뉴", MENU_LIST)

st.title("BIA/BIS 탐색적 분석 Tool")
st.caption("이 Tool은 질병 진단 도구가 아니며, 탐색적 데이터 분석을 위한 프로토타입입니다.")

# 선택된 메뉴에 따라 해당 화면을 표시
if selected_menu == "데이터 업로드":
    upload.render()
elif selected_menu == "데이터 구조 확인":
    overview.render()
elif selected_menu == "변수 탐색":
    explore.render()
elif selected_menu == "상관분석":
    correlation.render()
elif selected_menu == "그룹 비교":
    group_compare.render()
elif selected_menu == "반복측정 분석":
    repeated_measure.render()
elif selected_menu == "문헌 기반 분석":
    literature_reference.render()
else:
    st.header(selected_menu)
    st.warning("이 메뉴는 다음 단계에서 구현될 예정입니다.")
