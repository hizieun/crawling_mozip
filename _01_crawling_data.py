"""
@ author : Jenna
@ description : 모집요강 전형명 크롤링
@ date : 2023.04.28
"""
from tqdm.auto import tqdm
import requests
import pandas as pd
import re
import os
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# from selenium.webdriver.chrome.options import Options
# options = Options()
# options.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"


def run():
    # selenium 버전 3인 경우 (X)
    # setup Driver|Chrome : 크롬드라이버를 사용하는 driver 생성
    # driver = webdriver.Chrome(
    #     "/home/jinhakdl1/chrome-driver/chromedriver", chrome_options=options
    # )
    # driver = webdriver.Chrome("/home/jinhakdl1/chrome-driver/chromedriver")
    # driver.implicitly_wait(3)  # 암묵적으로 웹 자원을 (최대) 3초 기다리기

    # selenium 버전 4인 경우 (O)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(5)  # 암묵적으로 웹 자원을 (최대) 3초 기다리기

    # 일반대학 & 전문대학
    # url_univ = "https://www.adiga.kr/PageLinkAll.do?link=/kcue/ast/eip/eis/inf/selctninf/EipSelctnInfGnrl.do&p_menu_id=PG-EIP-06001"
    url_college = "https://www.adiga.kr/PageLinkAll.do?link=/kcue/ast/eip/eis/inf/selctninfjncll/EipSelctnInfJncll.do&p_menu_id=PG-EIP-06601&main_tab=2"

    # 페이지 접근
    driver.get(url_college)

    # "검색" 버튼 클릭
    # print(driver.find_elements(By.CLASS_NAME, "btn_searchAll"))
    # driver.find_elements(By.CLASS_NAME, "btn_searchAll")[0].click()
    # driver.find_element(By.CSS_SELECTOR, "#frm > div.search_box_btn > a").click()
    # button = driver.find_elements(By.XPATH, "//*[@id='frm']/div[3]/a")
    # button = driver.find_elements(
    #     By.XPATH, "/html/body/div[2]/div[2]/div[2]/div[1]/div[2]/form/div[1]/div[5]/a"
    # )
    button = driver.find_elements(By.LINK_TEXT, "검색")

    if button[0].is_enabled():
        print("검색 버튼 클릭")
        button[0].click()
        # button[0].send_keys(Keys.ENTER)
        # button[0].send_keys(Keys.RETURN)
        # button[0].send_keys("\n")
        # driver.execute_script("arguments[0].click();", button[0])

    # 2초간 대기(반드시 필요)
    time.sleep(2)
    # driver.implicitly_wait(5)

    # print(driver.window_handles[0])
    # driver.switch_to.window(driver.window_handles[0])
    # print(driver.current_url)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    # notices = soup.select("div.tbl_list > table > tbody > tr > td")
    # full XPath : /html/body/div[2]/div[2]/div[2]/div[1]/div[2]/form/div[10]/table/tbody/tr[15]/td[4]/a

    # for n in notices:
    #     print(n.text.strip())

    # 다음 페이지로 이동
    # end_page = 4267  # 일반대학
    end_page = 4248  # 전문대학

    # TODO : 텍스트 파일로 저장
    save_path = os.path.join(os.getcwd(), "result.csv")
    df = pd.DataFrame()
    univ_list = []
    department_list = []
    mozip_list = []

    values = range(end_page)
    with tqdm(total=len(values), position=0, leave=True) as pbar:
        # for i in tqdm(range(10), position=1, leave=True):
        for i in values:
            next_button = driver.find_elements(
                By.CSS_SELECTOR,
                "#pagination > li.next > a",
            )

            if next_button[0].is_enabled():
                print(f"{i} 페이지")
                next_button[0].click()

                time.sleep(0.4)
                try:
                    alert = driver.switch_to.alert
                    alert.dismiss()
                except:
                    "There is no alert"

                html = driver.page_source
                soup = BeautifulSoup(html, "html.parser")

                univs = soup.select(
                    "div.tbl_list > table > tbody > tr > td:nth-child(1)"
                )
                departs = soup.select(
                    "div.tbl_list > table > tbody > tr > td:nth-child(3)"
                )
                mozips = soup.select(
                    "div.tbl_list > table > tbody > tr > td:nth-child(4) > a"
                )
                # notices = soup.select("div.tbl_list > table > tbody > tr > td")
                # print(notices)

                # for i, n in enumerate(univ):
                #     print(n.text.strip())

                for i, n in enumerate(mozips):
                    # f.write(f"{i} : {n.text.strip()}\n")
                    # print(univ_list[i].text.strip(), n.text.strip())
                    # df["univ"] = univs[i].text.strip()
                    # df["mozip"] = n.text.strip()
                    # TODO : univ_list, mozip_list 에 append하기
                    univ_list.append(univs[i].text.strip())
                    department_list.append(departs[i].text.strip())
                    mozip_list.append(n.text.strip())

            pbar.update(1)
        pbar.close()

    df["university"] = univ_list
    df["department"] = department_list
    df["unit"] = mozip_list

    print("=====================================")
    print(df.head())
    print("=====================================")
    print(f"모집요강 갯수 = {len(mozip_list)}")
    print("=====================================")

    with open(save_path, "a", encoding="utf-8-sig") as f:
        df.to_csv(f, header=True, index=False)

    return


if __name__ == "__main__":
    run()
