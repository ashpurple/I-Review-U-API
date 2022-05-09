# I-Review-U-API
<img src="https://img.shields.io/badge/platform-python-blue"> <img src="https://img.shields.io/badge/platform-Flutter-skyblue">

> 크롤링을 통한 엑셀파일 생성법



## Project Description


## Requirement
crawling_restaurant.py에 있는 라이브러리를 확인하여 requirements.txt에 포함된 라이브러리와 동일한 버전 설치 

## Demo


## Crawling

크롬 브라우저 버전과 동일한 크롬 웹드라이버의 경로를 driverPath 변수에 지정
```c
url = "https://map.naver.com/v5/search/" + search_key # webpage path
driverPath = "chromedriver.exe" # driver path
```

아래 코드의 주석 처리를 제거하여 엑셀 파일 생성
```
df = pd.DataFrame(review_data, columns = ['장소명', '리뷰']) # Makes dataframe and save in excel file
df.to_csv(file_name + '.csv', encoding='utf-8-sig', index=False)
```
![image](https://user-images.githubusercontent.com/44630614/167439510-2e5f4ecd-77fa-4d94-935b-e6dd86b17998.png)

