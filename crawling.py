from bs4 import BeautifulSoup
from urllib.request import urlopen
import time
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
from selenium.webdriver.common.keys import Keys
from PyQt5 import QtCore, QtWidgets
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crawler.settings")
import django
django.setup()
from crawling_data.models import ReviewData
from crawling_data.models import BuildingData


def crawling(search_key, search_cnt, file_name):
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    #chrome_options.add_argument("headless") #백그라운드 실행

    review_data = []
    review_dict = []
    building_dict = []


    def scrollDown(driver, scrollDown_num=10): #스크롤 내리는 코드
        body = driver.find_element_by_css_selector('body')
        body.click()
        for i in range(50):
            time.sleep(0.01) #
            body.send_keys(Keys.PAGE_DOWN)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")


    url = "https://map.naver.com/v5/search/" + search_key #네이버 플레이스 검색
    #driverPath = "chromedriver.exe" #상대경로
    driverPath = "D:\\GitHub\\I-Review-U\\Dev\\Backend\\chromedriver.exe" #절대경로 #절대경로
    driver = webdriver.Chrome(driverPath, options=chrome_options)
    driver.implicitly_wait(5) #로딩까지 기다리기 위해 implicitly_wait와 sleep 사용
    driver.get(url) #드라이버로 받은 주소를 실행
    time.sleep(3)
    driver.switch_to.frame('searchIframe') # 네이버플레이스 맨 왼쪽 장소를 보여주는 프레임

    ad_cnt = len(driver.find_elements_by_partial_link_text('광고'))# 광고가 붙어있는 리스트는 중복되므로 건너뛰기 위해 카운트
    body = driver.find_element_by_css_selector('body')
    body.click()
    scrollDown(driver) #스크롤 내려서 모두 로드
    time.sleep(3)
    current_page = driver.page_source
    soup = BeautifulSoup(current_page, 'html.parser') #html 로드
    list_cnt = len(soup.select('#_pcmap_list_scroll_container > ul > li'))
    if search_cnt > list_cnt: #존재하는 장소 수가 검색할 수보다 더 적으면 존재하는 만큼만 검색
        search_cnt = list_cnt  
    current_place = 0 + ad_cnt
    driver.switch_to_default_content()   
    for i in range(ad_cnt, search_cnt + ad_cnt): #페이지당 장소 최대 50개
        driver.switch_to.frame('searchIframe') # 해당 장소 리뷰 크롤링이 끝나면 프레임 전환
        current_page = driver.page_source
        soup = BeautifulSoup(current_page, 'html.parser') #html 로드
        place_list = driver.find_element_by_xpath(f'/html/body/div[3]/div/div[2]/div[1]/ul/li[{i+1}]/div[1]/a')  # 해당 장소의 xpath 경로
        place_name = soup.select_one(f'li:nth-of-type({i+1}) > div._3hn9q > a > div.O9Z-o > div > span.OXiLu').text
        #place_type = soup.select_one(f'li:nth-of-type({i+1}) > div._3hn9q > a > div.O9Z-o > div > span._39UbY').text
        #place_location = soup.select_one(f'li:nth-of-type({i+1}) > div._3ZU00._1rBq3 > div > div > span > a > span._3hCbH').text
        #place_time = soup.select_one(f'li:nth-of-type({i+1}) > div._3ZU00._1rBq3 > a:nth-of-type(3) > div > span').text
        place_list.click() #클릭
        time.sleep(2) #페이지 로드를 기다림
        driver.switch_to_default_content() 
        driver.switch_to.frame('entryIframe') # 장소의 상세한 정보를 나타내는 두번째 프레임
        current_page = driver.page_source
        soup = BeautifulSoup(current_page, 'html.parser') #html 로드
        place_location = soup.select_one('span._2yqUQ').text
        call_number = soup.select_one('div > ul > li._1M_Iz._3xPmJ > div > span._3ZA0S').text 
        review_check = soup.select_one('div._3uUKd._2z4r0 > div._37n49 > span > a').text
        #방문자 리뷰가 존재하는지 체크(존재하지 않거나 블로그리뷰만 있으면 다음 장소로 넘어감)
        if '방문자리뷰' in review_check:
            review_list = driver.find_element_by_partial_link_text('리뷰') #리뷰 버튼을 찾아서 클릭
            review_list.click()
            time.sleep(5) #페이지 로드를 기다림
            review_cnt = int(driver.find_element_by_class_name('place_section_count').text.replace(',','')) #글로 된 리뷰 개수 확인
            current_page = driver.page_source
            soup = BeautifulSoup(current_page, 'html.parser') #html 로드
            h2_tag = soup.select('h2.place_section_header') 
            text_review_exists = 0
            for n in range(len(h2_tag)): #글 리뷰가 있는지 확인
                if ('리뷰' in h2_tag[n]): #사진리뷰만 존재하면 다음 장소로 넘어감
                    text_review_exists = 1
                    break   
            if text_review_exists == 1:

                building_obj = {
                            'place' : place_name,
                            'location' : place_location,
                            'call' : call_number,
                            #'time' : place_time
                        }

                building_dict.append(building_obj)
                if review_cnt % 10 == 0: #더보기당 리뷰 10개
                    more_cnt =  review_cnt//10 - 1
                else:
                    more_cnt =  review_cnt//10
                body = driver.find_element_by_css_selector('body')
                body.click()    
                for j in range(more_cnt):  #더보기 개수 만큼 스크롤 내리고 클릭 
                    #print(more_cnt)       
                    #wscrollDown(driver)
                    #more_review = driver.find_element_by_class_name('_3iTUo') #버튼 경로
                    more_review = driver.find_element_by_css_selector("a._3iTUo")
                
                    driver.execute_script("arguments[0].click();", more_review)
                    #print(more_review.text) #디버깅
                    #more_wwreview.click()
                    # #more_review.send_keys('\n')                   
                scrollDown(driver)    
                current_page = driver.page_source
                soup = BeautifulSoup(current_page, 'html.parser') #모든 리뷰를 로드                  
                for j in range(review_cnt):                    
                    if soup.select_one(f'li:nth-of-type({j+1}) > div._3vfQ6 > a > span') != None: #긴 리뷰는 펼치기 버튼이 있으므로 찾아서 누르기
                        '''
                        if(len(soup.select(f'li:nth-of-type({j+1}) > div._3vfQ6 > a > span'))) == 2:                            
                            driver.find_element_by_css_selector(f'li:nth-of-type({j+1}) > > div._3vfQ6 > a').click() #클릭 함수가 안될 경우 엔터 키를 보냄
                            driver.find_element_by_class_name('M_704').click()   
                            current_page = driver.page_source
                            soup = BeautifulSoup(current_page, 'html.parser')  #리뷰를 펼치고 다시 로드                      
                            time.sleep(1)  
                        '''                                       
                        review_text = soup.select_one(f'li:nth-of-type({j+1}) > div._3vfQ6 > a > span').text.strip() #텍스트 추출
                        #star_rate = ''
                        #if  soup.select_one(f'li:nth-of-type({j+1}) > div._3-LAD > span._1fvo3.Sv1wj > em') == None:
                           #continue

                        #star_rate = soup.select_one(f'li:nth-of-type({j+1}) > div._3-LAD > span._1fvo3.Sv1wj > em').text #별점 추출
                        review_data.append((place_name, review_text)) #리스트로 저장

                        review_obj = {
                            'place' : place_name,
                            'review' : review_text,
                            #'rate' : star_rate
                        }                        
                        review_dict.append(review_obj)                      
                        time.sleep(0.1)           
        text_review_exists = 0  #다음 장소를 위해 글 리뷰 여부 초기화
        current_place += 1
        print(current_place)               
        driver.switch_to_default_content() #프레임 초기화
        time.sleep(2)
    '''
    df = pd.DataFrame(review_data, columns = ['장소명', '리뷰']) #데이터 프레임으로 만들어 엑셀에 저장
    df.to_csv(file_name + '.csv', encoding='utf-8-sig', index=False)
    '''
    if __name__=='__main__':
        for item in building_dict:
            BuildingData(building_name = item['place'], building_loc = item['location'], building_call = item['call']).save()
            #BuildingData(building_name = item['place'], building_loc = item['location'], building_call = item['call'], building_time = item['time']).save()
        for item in review_dict:
            ReviewData(building_name = item['place'], review_content = item['review']).save()
    
    driver.close()


                         


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(140, 60, 201, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(140, 100, 201, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_3.setGeometry(QtCore.QRect(140, 140, 201, 20))
        self.lineEdit_3.setObjectName("lineEdit_2")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(160, 200, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.button_clicked)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(50, 60, 56, 20))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(50, 100, 56, 20))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(50, 140, 56, 20))
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_2")


        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "크롤링 시작"))
        self.label.setText(_translate("Dialog", "장소명"))
        self.label_2.setText(_translate("Dialog", "장소 수"))
        self.label_3.setText(_translate("Dialog", "파일명"))
        self.lineEdit_3.setText(_translate("Dialog", "확장자 제외"))
   

    def button_clicked(self):
        search_key = self.lineEdit.text()
        search_cnt = int(self.lineEdit_2.text())
        file_name = self.lineEdit_3.text()
        crawling(search_key, search_cnt, file_name)
        


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
    


