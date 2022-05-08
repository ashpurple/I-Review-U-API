# I-Review-U-API
<img src="https://img.shields.io/badge/platform-python-blue"> <img src="https://img.shields.io/badge/platform-Flutter-skyblue">

> 크롤링을 통한 엑셀파일 생성법



## Project Description



## Demo


## Crawling

웹드라이버 경로 지정
```c
url = "https://map.naver.com/v5/search/" + search_key # webpage path
driverPath = "chromedriver.exe" # driver path
```

엑셀 파일 생성
```
df = pd.DataFrame(review_data, columns = ['장소명', '리뷰']) # Makes dataframe and save in excel file
df.to_csv(file_name + '.csv', encoding='utf-8-sig', index=False)
```

