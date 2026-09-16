"""
상관분석, 그룹 비교 등 통계 계산에 사용되는 공통 함수 모음.
"""

import pandas as pd
from scipy import stats


def compute_correlation(df: pd.DataFrame, col_x: str, col_y: str) -> dict:
    """
    두 숫자형 변수 사이의 Pearson, Spearman 상관계수를 계산한다.

    - 두 변수 중 하나라도 결측치인 행은 제외하고 계산한다 (pairwise complete).
    - 표본 수가 3개 미만이면 계산하지 않고 안내 메시지를 반환한다.

    반환값 (dict):
        n, pearson_r, pearson_p, spearman_r, spearman_p, clean_df, error
    """
    paired = df[[col_x, col_y]].dropna()
    n = len(paired)

    result = {
        "n": n,
        "pearson_r": None,
        "pearson_p": None,
        "spearman_r": None,
        "spearman_p": None,
        "clean_df": paired,
        "error": None,
    }

    if n < 3:
        result["error"] = "유효한 값이 3개 미만이어서 상관계수를 계산할 수 없습니다."
        return result

    if paired[col_x].std() == 0 or paired[col_y].std() == 0:
        result["error"] = "선택한 변수 중 값이 모두 동일한 변수가 있어 상관계수를 계산할 수 없습니다."
        return result

    try:
        pearson_r, pearson_p = stats.pearsonr(paired[col_x], paired[col_y])
        result["pearson_r"] = round(pearson_r, 3)
        result["pearson_p"] = pearson_p
    except Exception as e:
        result["error"] = f"Pearson 상관계수 계산 중 오류가 발생했습니다: {e}"

    try:
        spearman_r, spearman_p = stats.spearmanr(paired[col_x], paired[col_y])
        result["spearman_r"] = round(spearman_r, 3)
        result["spearman_p"] = spearman_p
    except Exception as e:
        # Pearson은 성공했는데 Spearman만 실패한 경우, 기존 오류를 덮어쓰지 않고 이어붙임
        msg = f"Spearman 상관계수 계산 중 오류가 발생했습니다: {e}"
        result["error"] = (result["error"] + " / " + msg) if result["error"] else msg

    return result


def check_normality(series: pd.Series) -> dict:
    """
    한 그룹의 값들에 대해 Shapiro-Wilk 정규성 검정을 수행한다.

    - 표본 수가 3개 미만이면 검정 자체가 불가능하므로 testable=False로 반환한다.
    - 그 외 오류가 발생해도 앱이 멈추지 않도록 예외 처리한다.

    반환값 (dict): testable, is_normal, p_value, reason
    """
    values = series.dropna()
    n = len(values)

    if n < 3:
        return {
            "testable": False,
            "is_normal": False,
            "p_value": None,
            "reason": f"표본 수가 {n}개로 너무 적어 정규성 검정을 수행할 수 없습니다.",
        }

    try:
        stat, p_value = stats.shapiro(values)
        return {
            "testable": True,
            "is_normal": p_value > 0.05,
            "p_value": p_value,
            "reason": None,
        }
    except Exception as e:
        return {
            "testable": False,
            "is_normal": False,
            "p_value": None,
            "reason": f"정규성 검정 중 오류가 발생했습니다: {e}",
        }


def get_group_descriptive_stats(paired: pd.DataFrame, value_col: str, group_col: str) -> pd.DataFrame:
    """
    그룹별 n, 평균, 중앙값, 표준편차, 최소/최대값을 정리한 표를 반환한다.
    """
    rows = []
    for group_name, group_df in paired.groupby(group_col):
        values = group_df[value_col]
        rows.append(
            {
                "그룹": group_name,
                "n": len(values),
                "평균": round(values.mean(), 2),
                "중앙값": round(values.median(), 2),
                "표준편차": round(values.std(), 2) if len(values) > 1 else None,
                "최소값": values.min(),
                "최대값": values.max(),
            }
        )
    return pd.DataFrame(rows)


def compute_group_comparison(df: pd.DataFrame, value_col: str, group_col: str) -> dict:
    """
    범주형 변수(group_col)로 나눈 그룹 사이에 숫자형 변수(value_col)의 차이를 비교한다.

    자동 검정 선택 규칙:
    - 검정에 사용 가능한 그룹(n>=2)이 2개인 경우:
        모든 그룹이 정규성을 만족하면 independent t-test, 아니면 Mann-Whitney U test
    - 검정에 사용 가능한 그룹이 3개 이상인 경우:
        모든 그룹이 정규성을 만족하면 One-way ANOVA, 아니면 Kruskal-Wallis test
    - 검정 가능한 그룹이 2개 미만이면 검정을 수행하지 않고 이유를 반환한다.

    반환값 (dict):
        clean_df, descriptive, excluded_groups, normality_info,
        test_method, test_stat, test_p, small_sample_warning, error
    """
    paired = df[[value_col, group_col]].dropna()

    result = {
        "clean_df": paired,
        "descriptive": None,
        "excluded_groups": [],
        "normality_info": {},
        "test_method": None,
        "test_stat": None,
        "test_p": None,
        "small_sample_warning": False,
        "error": None,
    }

    if paired.empty:
        result["error"] = "비교할 수 있는 유효한 데이터가 없습니다."
        return result

    unique_groups = paired[group_col].unique().tolist()

    if len(unique_groups) < 2:
        result["error"] = "그룹이 2개 이상 있어야 비교할 수 있습니다. 현재 그룹이 1개뿐입니다."
        result["descriptive"] = get_group_descriptive_stats(paired, value_col, group_col)
        return result

    result["descriptive"] = get_group_descriptive_stats(paired, value_col, group_col)

    # 통계 검정에 사용할 그룹(n>=2)과 제외할 그룹(n<2) 구분
    group_arrays = {}
    for group_name, group_df in paired.groupby(group_col):
        values = group_df[value_col]
        if len(values) < 2:
            result["excluded_groups"].append(
                f"'{group_name}' (n={len(values)}, 표본 수 부족으로 검정에서 제외)"
            )
        else:
            group_arrays[group_name] = values

    # 표본 수가 적은 그룹이 있으면 주의 문구 플래그
    if any(len(v) < 10 for v in group_arrays.values()):
        result["small_sample_warning"] = True

    if len(group_arrays) < 2:
        result["error"] = "검정을 수행할 수 있는(표본 수 2개 이상) 그룹이 2개 미만입니다."
        return result

    # 각 그룹의 정규성 검정
    normal_flags = []
    for group_name, values in group_arrays.items():
        normality = check_normality(values)
        result["normality_info"][group_name] = normality
        normal_flags.append(normality["is_normal"])

    all_normal = all(normal_flags)
    group_values_list = list(group_arrays.values())

    try:
        if len(group_arrays) == 2:
            if all_normal:
                stat, p = stats.ttest_ind(group_values_list[0], group_values_list[1])
                result["test_method"] = "Independent t-test"
            else:
                stat, p = stats.mannwhitneyu(group_values_list[0], group_values_list[1])
                result["test_method"] = "Mann-Whitney U test"
        else:
            if all_normal:
                stat, p = stats.f_oneway(*group_values_list)
                result["test_method"] = "One-way ANOVA"
            else:
                stat, p = stats.kruskal(*group_values_list)
                result["test_method"] = "Kruskal-Wallis test"

        result["test_stat"] = round(stat, 3)
        result["test_p"] = p
    except Exception as e:
        result["error"] = f"통계 검정 중 오류가 발생했습니다: {e}"

    return result
