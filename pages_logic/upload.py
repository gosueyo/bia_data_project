"""
1-2단계: 데이터 업로드 화면

기능:
- xlsx / xls / csv 파일 업로드
- Excel 파일일 경우 sheet 목록을 보여주고 사용자가 선택
- 불러온 데이터를 st.session_state에 저장 (다른 메뉴에서도 재사용)
- 업로드 직후 데이터 미리보기(상위 5행)만 표시
"""

import pandas as pd
import streamlit as st


def render():
    st.header("1. 데이터 업로드")

    st.write(
        """
        BIA/BIS 데이터가 담긴 파일을 업로드해주세요.
        지원 형식: .xlsx, .xls, .csv
        """
    )

    uploaded_file = st.file_uploader(
        "파일을 선택하세요",
        type=["xlsx", "xls", "csv"],
    )

    # 아직 파일이 없으면 여기서 종료
    if uploaded_file is None:
        st.info("파일을 업로드하면 미리보기가 표시됩니다.")
        return

    file_name = uploaded_file.name

    # 파일 확장자에 따라 읽는 방식이 다름
    if file_name.endswith(".csv"):
        df = _read_csv(uploaded_file)
    else:
        df = _read_excel(uploaded_file)

    # 읽기에 실패한 경우 (오류 메시지는 각 함수에서 이미 표시함)
    if df is None:
        return

    # 세션에 저장 -> 다른 메뉴(구조 확인, 변수 탐색 등)에서도 사용 가능
    st.session_state["df"] = df
    st.session_state["file_name"] = file_name

    st.success(f"'{file_name}' 파일을 정상적으로 불러왔습니다.")

    st.subheader("데이터 미리보기 (상위 5행)")
    st.dataframe(df.head())

    st.caption(f"전체 {df.shape[0]}행 × {df.shape[1]}열")


def _read_csv(uploaded_file):
    """CSV 파일을 읽어서 DataFrame으로 반환. 실패 시 None 반환."""
    try:
        df = pd.read_csv(uploaded_file)
        return df
    except Exception as e:
        st.error(f"CSV 파일을 읽는 중 오류가 발생했습니다: {e}")
        return None


def _read_excel(uploaded_file):
    """Excel 파일을 읽어서 DataFrame으로 반환. sheet가 여러 개면 선택 UI 제공."""
    try:
        excel_file = pd.ExcelFile(uploaded_file)
    except Exception as e:
        st.error(f"Excel 파일을 읽는 중 오류가 발생했습니다: {e}")
        return None

    sheet_names = excel_file.sheet_names

    if len(sheet_names) == 1:
        selected_sheet = sheet_names[0]
    else:
        st.write(f"이 파일에는 {len(sheet_names)}개의 sheet가 있습니다.")
        selected_sheet = st.selectbox("분석할 sheet를 선택하세요", sheet_names)

    try:
        df = excel_file.parse(selected_sheet)
        return df
    except Exception as e:
        st.error(f"'{selected_sheet}' sheet를 읽는 중 오류가 발생했습니다: {e}")
        return None
