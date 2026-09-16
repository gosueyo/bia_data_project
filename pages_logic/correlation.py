"""
2-1단계: 상관분석 화면

기능:
- 숫자형 변수 2개 선택
- Pearson correlation, Spearman correlation 계산 (r, p-value, n)
- Scatter plot 표시
- 결과는 "탐색적 분석 결과" 수준으로만 표현 (인과관계 표현 금지)
"""

import plotly.express as px
import streamlit as st

from utils.data_utils import classify_columns
from utils.stats_utils import compute_correlation


def render():
    st.header("4. 상관분석")

    df = st.session_state.get("df")

    if df is None:
        st.info("먼저 '데이터 업로드' 메뉴에서 파일을 업로드해주세요.")
        return

    numeric_cols, _ = classify_columns(df)

    if len(numeric_cols) < 2:
        st.warning("상관분석을 하려면 숫자형 변수가 2개 이상 필요합니다.")
        return

    col1, col2 = st.columns(2)
    with col1:
        var_x = st.selectbox("변수 1 (X축)", numeric_cols, index=0)
    with col2:
        # 변수 2 기본값은 변수 1과 겹치지 않도록 설정
        default_index = 1 if len(numeric_cols) > 1 else 0
        var_y = st.selectbox("변수 2 (Y축)", numeric_cols, index=default_index)

    if var_x == var_y:
        st.warning("서로 다른 두 변수를 선택해주세요.")
        return

    result = compute_correlation(df, var_x, var_y)

    st.caption(f"결측치를 제외하고 두 변수 모두 값이 있는 {result['n']}개 데이터로 계산했습니다.")

    if result["error"]:
        st.error(result["error"])
        return

    # 결과 표
    st.subheader("상관계수 결과 (탐색적 분석 결과)")
    result_table = {
        "구분": ["Pearson", "Spearman"],
        "상관계수(r)": [result["pearson_r"], result["spearman_r"]],
        "p-value": [result["pearson_p"], result["spearman_p"]],
        "표본 수(n)": [result["n"], result["n"]],
    }
    st.dataframe(result_table, use_container_width=True)

    # 표본 수 주의 문구
    if result["n"] < 30:
        st.warning("표본 수가 적어 상관계수 결과의 신뢰도가 낮을 수 있습니다. 참고용으로만 활용해주세요.")

    # Scatter plot
    st.subheader("Scatter Plot")
    fig = px.scatter(result["clean_df"], x=var_x, y=var_y)
    st.plotly_chart(fig, use_container_width=True)

    st.caption(
        "위 결과는 두 변수 사이의 통계적 상관관계를 탐색한 것으로, "
        "인과관계나 질병 여부를 의미하지 않습니다."
    )
