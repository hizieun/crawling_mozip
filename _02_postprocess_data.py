"""
@ author : Jenna
@ description : 크롤링 데이터 전처리 후 최종 결과 저장
@ date : 2023.05.09
"""
import os
import pandas as pd


def run():
    univ_csv = os.path.join(os.getcwd(), "result_univ.csv")
    college_csv = os.path.join(os.getcwd(), "result_college.csv")

    univ_df = pd.read_csv(univ_csv)
    college_df = pd.read_csv(college_csv)

    dup_univ_list = univ_df["unit"].tolist()
    dup_college_list = college_df["unit"].tolist()
    print(f"중복된 전체 개수 = 일반대학 : {len(dup_univ_list)} , 전문대학 : {len(dup_college_list)}")

    univ_list = list(set(dup_univ_list))
    college_list = list(set(dup_college_list))
    print(f"최종 = 일반대학 : {len(univ_list)} , 전문대학 : {len(college_list)}")

    res_univ_df = pd.DataFrame()
    res_college_df = pd.DataFrame()

    res_univ_df["전형"] = univ_list
    res_college_df["전형"] = college_list

    """
    상위전형, 하위전형으로 분리
    """
    split_char = ">"

    res_univ_df[["전형", "하위"]] = res_univ_df["전형"].str.split(split_char, expand=True)
    res_college_df[["전형", "하위"]] = res_college_df["전형"].str.split(
        split_char, expand=True
    )
    # print(res_univ_df.head())

    """
    일반대학, 전문대학 별도 csv 저장
    """
    res_univ_df.to_csv("전형명_일반대학.csv", index=False, header=False)
    res_college_df.to_csv("전형명_전문대학.csv", index=False, header=False)

    save_univ = os.path.join(os.getcwd(), "전형명_일반대학.csv")
    save_college = os.path.join(os.getcwd(), "전형명_전문대학.csv")

    with open(save_univ, "wt", encoding="utf-8-sig") as f:
        res_univ_df.to_csv(f, header=False, index=False)

    with open(save_college, "wt", encoding="utf-8-sig") as f:
        res_college_df.to_csv(f, header=False, index=False)

    """
    단어 사전용 결과 저장 
    """
    save_res = os.path.join(os.getcwd(), "전형명_전체.csv")
    res_df = pd.concat([res_univ_df, res_college_df])
    res_df = pd.concat([res_df["전형"], res_df["하위"]])

    res_df_list = res_df.tolist()
    res_df_list = list(set(res_df_list))
    print(f"최종 = {len(res_df_list)}")  # 1989

    unit_df = pd.DataFrame()
    unit_df["전형"] = res_df_list
    print(unit_df.head())

    with open(save_res, "wt", encoding="utf-8-sig") as f:
        unit_df.to_csv(f, header=False, index=False)

    """
    TODO : 세부 전형 분리 후 전처리
    """
    unit_list = unit_df["전형"].tolist()

    split_sebu1 = "("
    split_sebu2 = "{"
    split_sebu3 = "["

    replace_char1 = ")"
    replace_char2 = "}"
    replace_char3 = "]"

    dash_char = "-"
    under_char = "_"

    unit_list = [
        x.replace(split_sebu2, split_sebu1)
        .replace(split_sebu3, split_sebu1)
        .replace(replace_char2, replace_char1)
        .replace(replace_char3, replace_char1)
        .replace(under_char, dash_char)
        for x in unit_list
    ]

    # 여는 괄호로 세부전형 분리
    unit_list = [x.split(split_sebu1) for x in unit_list]

    # 2차원 리스트를 1차원 리스트로 변환
    unit_list = sum(unit_list, [])

    # 특수문자 제거
    unit_list = [
        x.replace(replace_char1, "")
        # .replace(replace_char2, "")
        # .replace(replace_char3, "")
        for x in unit_list
    ]

    # 대쉬로 분리
    unit_list = [x.split(dash_char) for x in unit_list]

    # 2차원 리스트를 1차원 리스트로 변환
    unit_list = sum(unit_list, [])

    # 중복제거
    unit_list = list(set(unit_list))

    # 공백인 값 제거
    unit_list = [x for x in unit_list if x != ""]

    # 글자 맨앞 맨뒤 공백 제거
    unit_list = [x.strip() for x in unit_list]

    # 리스트를 데이터프레임으로 변환
    final_df = pd.DataFrame()
    final_df["전형"] = unit_list
    # print(len(unit_list))

    """
    csv 형태 저장
    (최종 결과물 = 전형명_최종.csv)
    """
    save_final = os.path.join(os.getcwd(), "전형명_최종.csv")

    with open(save_final, "wt", encoding="utf-8-sig") as f:
        final_df.to_csv(f, header=False, index=False)

    return


if __name__ == "__main__":
    run()
