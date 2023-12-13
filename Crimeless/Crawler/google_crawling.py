
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from openpyxl import Workbook

service = Service(executable_path=r'C:\Users\c\Desktop\chromedriver.exe')
options = webdriver.ChromeOptions()
options.add_argument("headless")
options.add_argument("disable-gpu")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
driver = webdriver.Chrome(service = service, options = options)




def google():
    workbook = Workbook()
    sheet = workbook.active
    sheet['A1'] = '순서'
    sheet['B1'] = '날짜'
    sheet['C1'] = '기사제목'
    sheet['D1'] = '링크'
    sheet['E1'] = '미리보기'

    msg = input('검색어 : ')
    year = 2021     #년도
    start_month = 1 #시작 월
    end_month = 3   #끝 월
    
    for month in range(start_month, end_month+1, 1):
        #1회당 10개의 기사
        for i in range(0, 10, 1):   
            driver.get('https://www.google.com/search?q='+ str(msg) +
                    '&sca_esv=580030856&tbs=cdr:1,cd_' + 'min:'+str(month) + '/1/'+str(year)+',cd_max:' + str(month) + '/31/'+ str(year) +
                    '&tbm=nws&sxsrf=AM9HkKn7-NwibOtLfMFR7UATdJz4nzB9aA:1699334622176&ei=3slJZdCmCvbq1e8Pjuq_qAM&start='+ str(10*i) +
                    '&sa=N&ved=2ahUKEwjQjYnkkrGCAxV2dfUHHQ71DzUQ8tMDegQIAxAE&biw=1707&bih=948&dpr=1.5')
            
            time = []
            time = driver.find_elements(By.CLASS_NAME, 'OSrXXb.rbYSKb.LfVVr')
            title = []
            title = driver.find_elements(By.CLASS_NAME, 'n0jPhd.ynAwRc.MBeuO.nDgy9d')
            link = []
            link = driver.find_elements(By.CSS_SELECTOR, '.WlydOe')
            priview = []
            priview = driver.find_elements(By.CLASS_NAME, 'GI74Re.nDgy9d')
        
            for j in range(len(title)):
                time_text = time[j].text.strip()
                title_text = title[j].text.strip()
                link_text = link[j].get_attribute('href')
                priview_text = priview[j].text.strip()

                sheet.append([100*(month-1)+10*i+j+1, time_text, title_text, link_text, priview_text])
                print(str(100*(month-1)+10*i+j+1) + '번 기사 >' + time_text + title_text + '\n' + str(link_text) + '\n' + priview_text)

            workbook.save(str(year) +'년 '+ str(start_month) + '월 ' + '- ' + str(year) +'년 '+ str(end_month) + '월' +'.xlsx')
        
google()