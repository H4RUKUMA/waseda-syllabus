import time
from selenium import webdriver
import csv
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import os
import mojimoji

semester = 2
semester_list = ['通年', '春学期', '秋学期', 'その他']
#1: 通年 2:春学期 3:秋学期 4:その他

week = 1
week_list = ['月','火','水','木','金','土','日','その他']
#1:月 2:火 3:水 4:木 5:金 6:土 7:日 8:その他

period = 2
period_list = ['1時限','2時限', '3時限', '4時限','5時限','6時限','7時限','フルオンデマンド','その他']
#1:1時限 2:2時限 3:3時限 4:4時限 5:5時限 6:6時限 7:7時限 8:フルオンデマンド #9:その他

department = 0
department_list = ['指定なし','政経','法学','教育','商学','社学','人科','スポーツ','国際教養','文構' 
,'文','人通','基幹','創造','先進']
#0: 指定なし 1:政経 2:法学 3:教育 4:商学 5:社学 6:人科 7:スポーツ 8:国際教養 9:文構 
#10:文 11:人通 12:基幹 13:創造 14:先進 e.t.c
semester_path = 'data/' + '2020/' + str(semester-2) + semester_list[semester-1] + '/'
os.makedirs(semester_path, exist_ok=True)

semesterData = [[]]


weekData = [[]]
week_path = "TEST" + semester_path + str(week-1) + week_list[week-1] + "/"
os.makedirs(week_path, exist_ok=True)

if period == 8:
    pass
else:
    csvNum = str(semester)+str(week)+str(period)+str(department)
    csvNum2 = str(semester)+str(department)
    # driver = webdriver.Chrome()
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options) 
    URL = 'https://www.wsl.waseda.jp/syllabus/JAA101.php'
    driver.get(URL)

    p_gakki = driver.find_element_by_name("p_gakki")
    semesterSelect = Select(p_gakki)
    semesterSelect.select_by_index(semester)

    p_youbi = driver.find_element_by_name("p_youbi")
    weekSelect = Select(p_youbi)
    weekSelect.select_by_index(week)

    p_jigen = driver.find_element_by_name("p_jigen")
    periodSelect = Select(p_jigen)
    periodSelect.select_by_index(period)

    p_gakubu = driver.find_element_by_name("p_gakubu")
    depSelect = Select(p_gakubu)
    depSelect.select_by_index(department)

    search = driver.find_elements_by_tag_name("BtnSubmit")
    driver.execute_script("func_search('JAA103SubCon');")

    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, "html.parser")

    try:
        btnTable = soup.findAll("table", {"class":"t-btn"})[2]
        count = len(btnTable.find('tr').findAll('td'))
        last_page = btnTable.find('tr').findAll('td')[count-1].find('a').contents[0]
    except:
        pass

    allData = [[]]

    for num in range(1,int(last_page)+2):
        html = driver.page_source.encode('utf-8')
        soup = BeautifulSoup(html, "html.parser")

        try:
            table = soup.findAll("table", {"class":"ct-vh"})[0]
            rows = table.findAll("tr")
        except: 
            pass

        for row in rows:
            csvRow = []
            for cell in row.findAll(['td', 'th']):
                csvRow.append(str(cell.get_text()))

            if csvRow[0] == "開講年度":
                pass
            elif csvRow[7] == "教室未定" or csvRow[7] == " -":
                pass
            elif "-" not in csvRow[7] == True:
                pass
            else: 
                csvRow[7] = mojimoji.zen_to_han(csvRow[7])
                allData.append(csvRow)
                weekData.append(csvRow)
                semesterData.append(csvRow)
        
        try:
            driver.execute_script("page_turning('JAA103SubCon',"+ str(num) + ");")
        except:
            pass

    with open(os.path.join(week_path, "syllabus"+csvNum+".csv"), "w", encoding='utf-8',newline="") as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerows(allData)
    driver.quit()
    print(week_path + "syllabus"+csvNum+".csv"+".....done")
    file.close()