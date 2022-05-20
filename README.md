# I-Review-U-API
<img src="https://img.shields.io/badge/platform-python-blue"> <img src="https://img.shields.io/badge/platform-Flutter-skyblue">

# 크롤링을 통한 엑셀파일 생성법 및 Django API 확인법

## Project Description
I-Review-You는 크롤링한 데이터를 바탕으로 리뷰를 분석하여 긍부정 및 속성을 제공해주는 프로젝트 입니다.

## Requirement
다음 명령어를 통해 requirements.txt에 있는 파이썬 라이브러리를 설치
```
pip install -r requirements.txt
```
플러터의 pubspec.yaml에서 다음과 같은 플러터 라이브러리를 dependencies에 작성하고 Get package 버튼 클릭 혹은 다음과 같은 명령어 입력
```
dependencies:
  flutter:
    sdk: flutter
  http: ^0.13.3
  get: ^3.24.0



  # The following adds the Cupertino Icons font to your application.
  # Use with the CupertinoIcons class for iOS style icons.
  cupertino_icons: ^1.0.2
  flutter_svg: ^0.22.0
  animated_splash_screen: ^1.0.1+2
```
```
flutter pub get
```



## Demo


## Create Excel File

크롬 브라우저 버전과 동일한 크롬 웹드라이버의 경로를 driverPath 변수에 지정
```c
url = "https://map.naver.com/v5/search/" + search_key # webpage path
driverPath = "chromedriver.exe" # driver path
```

아래 코드의 주석 처리를 제거하여 Excel 파일 생성
```
df = pd.DataFrame(review_data, columns = ['장소명', '리뷰']) # Makes dataframe
df.to_csv(file_name + '.csv', encoding='utf-8-sig', index=False) # Saves dataframe in csv file
```

엑셀 파일명은 크롤링 실행 시 입력 가능

![image](https://user-images.githubusercontent.com/44630614/167439510-2e5f4ecd-77fa-4d94-935b-e6dd86b17998.png)

## Django Server API
터미널 경로를 Backend 폴더로 설정 후 다음 명령어 입력
```
Python manage.py makemigrations crawling_data
Python manage.py migrate crawling_data
python manage.py createsuperuser # Create admin account
```
크롤링이 끝난 후 cmd의 ipconfig를 통해 IPv4 주소 확인 및 서버 구동
```
python manage.py runserver [IPv4주소]:8000
```

## Review Analysis
각 페이지의 Uri.parse에 api 주소 입력

**home.dart**
```
Uri.parse("http://[IPv4주소]:8000/api/buildingdata/")
```
**review.dart**
```
Uri.parse("http://[IPv4주소]:8000/api/buildingdata/" + slug + "/")
```
**review2.dart**
```
http://[IPv4주소]:8000/api/buildingdata/" + slug + "/analysis
```
터미널 경로를 Front의 i_review_u 폴더로 설정 후 다음 명령어 입력
```
flutter run -d chrome --web-port=8000
```


