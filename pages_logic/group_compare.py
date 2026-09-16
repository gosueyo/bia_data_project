"""
2-2단계: 그룹 비교 화면

기능:
- 범주형 변수(그룹 변수)와 숫자형 변수(비교할 값) 선택
- 그룹별 n / 평균 / 중앙값 / 표준편차 / 최소·최대값 표시
- Boxplot으로 그룹별 분포 시각화
- 정규성 검정 결과에 따라 자동으로 검정 방법 선택
    - 2개 그룹: t-test 또는 Mann-Whitney U test
    - 3개 이상 그룹: ANOVA 또는 Kruskal-Wallis test
- 선택된 검정 방법과 p-value 표시
- 표본 수가 적은 경우 주의 문구 표시
- 분석이 불가능한 경우 오류 없이 이유 안내
"""

import plotly.express as px
import streamlit as st

from utils.data_utils import classify_columns
from utils.stats_utils import compute_group_comparison


def render():
    st.header("5. 그룹 비교")

    df = st.session_state.get("df")

    if df is None:
        st.info("먼저 '데이터 업로드' 메뉴에서 파일을 업로드해주세요.")
        return

    numeric_cols, categorical_cols = classify_columns(df)

    if not numeric_cols:
        st.warning("비교할 숫자형 변수가 없습니다.")
        return

    if not categorical_cols:
        st.warning(
            "현재 데이터에 그룹을 나눌 수 있는 범주형 변수(성별, 질환군 등)가 없어 "
            "그룹 비교를 수행할 수 없습니다."
        )
        return

    col1, col2 = st.columns(2)
    with col1:
        value_col = st.selectbox("비교할 숫자형 변수", numeric_cols)
    with col2:
        group_col = st.selectbox("그룹을 나눌 범주형 변수", categorical_cols)

    result = compute_group_comparison(df, value_col, group_col)

    # 치명적 오류(비교 자체 불가)인 경우 여기서 종료
    if result["error"] and result["descriptive"] is None:
        st.error(result["error"])
        return

    # 그룹별 기술통계
    st.subheader("그룹별 기술통계")
    st.dataframe(result["descriptive"], use_container_width=True)

    # 검정에서 제외된 그룹 안내
    if result["excluded_groups"]:
        st.caption("다음 그룹은 표본 수가 부족(n<2)하여 통계 검정에서 제외되었습니다: " + ", ".join(result["excluded_groups"]))

    # 표본 수 주의 문구
    if result["small_sample_warning"]:
        st.warning("일부 그룹의 표본 수가 10개 미만으로 적어 검정 결과의 신뢰도가 낮을 수 있습니다.")

    # Boxplot
    st.subheader("그룹별 분포 (Boxplot)")
    fig = px.box(result["clean_df"], x=group_col, y=value_col, points="all")
    st.plotly_chart(fig, use_container_width=True)

    # 검정 자체가 불가능한 경우
    if result["test_method"] is None:
        if result["error"]:
            st.warning(f"통계 검정을 수행하지 못했습니다: {result['error']}")
        return

    # 정규성 검정 결과 표시
    st.subheader("정규성 검정 결과 (그룹별, Shapiro-Wilk)")
    normality_rows = []
    for group_name, info in result["normality_info"].items():
        if info["testable"]:
            normality_rows.append(
                {
                    "그룹": group_name,
                    "정규성 만족 여부": "만족" if info["is_normal"] else "불만족",
                    "p-value": round(info["p_value"], 4),
                }
            )
        else:
            normality_rows.append(
                {
                    "그룹": group_name,
                    "정규성 만족 여부": f"검정 불가 ({info['reason']})",
                    "p-value": None,
                }
            )
    st.dataframe(normality_rows, use_container_width=True)

    # 검정 결과
    st.subheader("검정 결과 (탐색적 분석 결과)")
    st.write(f"**선택된 검정 방법: {result['test_method']}**")
    st.write(f"검정 통계량: {result['test_stat']}")
    st.write(f"p-value: {result['test_p']:.4f}" if result["test_p"] is not None else "p-value: 계산되지 않음")

    if result["test_p"] is not None:
        if result["test_p"] < 0.05:
            st.info("그룹 간 통계적으로 유의한 차이가 관찰되었습니다. (p < 0.05)")
        else:
            st.info("그룹 간 통계적으로 유의한 차이가 관찰되지 않았습니다. (p >= 0.05)")

    st.caption(
        "위 결과는 탐색적 분석 결과입니다. "
        "통계적으로 유의한 차이가 있더라도 이는 질병 진단이나 인과관계를 의미하지 않습니다."
    )
