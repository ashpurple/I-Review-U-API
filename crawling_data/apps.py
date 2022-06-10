from django.apps import AppConfig
from pororo import Pororo
from hanspell import spell_checker
import pandas as pd
from konlpy.tag import Mecab

class CrawlingDataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'crawling_data'

class PororoConfig(AppConfig):
    # pororo 모델 생성
    
    
    def review(input):
        sa = Pororo(task="sentiment", model="brainbert.base.ko.shopping", lang="ko") # 긍부정분석
        zsl = Pororo(task="zero-topic", lang="ko") # 주제분석
        attributeList = ["음식","커피","청결","공부","분위기","친절","가격","위치"]
        new_list = list()
        for row in input:
            review = dict()
            review_content = row['review_content']
            checked_review = spell_checker.check(review_content)
            clean_review = checked_review.checked
            expected_star = Pororo(task = "review", lang="ko")
            review['id'] = row['id']
            review['building_name'] = row['building_name']
            review['review_content'] = review_content
            review['checked_review'] = clean_review
            # expected star
            review['star_num'] = expected_star(review_content)

            # positivity
            positivity = sa(review_content,show_probs=True)
            positive = positivity['positive']
            review['positivity'] = positive

            # attribute
            attribute_dic = zsl(review_content, attributeList)
            max = 0
            temp_key = '무속성'
            for key, value in attribute_dic.items():
                if (60 < value):
                    if (max < value):
                        max = value
                        temp_key = key
            review['attribute'] = temp_key

            new_list.append(review)
        return new_list

    def analysis(input):
        sa = Pororo(task="sentiment", model="brainbert.base.ko.shopping", lang="ko") # 긍부정분석
        zsl = Pororo(task="zero-topic", lang="ko") # 주제분석
        attributeList = ["음식","커피","청결","공부","분위기","친절","가격","위치"]
        new_list = list()
        for row in input:
            review = dict()
            review_content = row['review_content']
            checked_review = spell_checker.check(review_content)
            clean_review = checked_review.checked
            expected_star = Pororo(task = "review", lang="ko")
            review['id'] = row['id']
            review['building_name'] = row['building_name']
            review['review_content'] = review_content
            review['checked_review'] = clean_review
            # expected star
            review['star_num'] = round(expected_star(review_content), 1)

            # positivity
            positivity = sa(review_content,show_probs=True)
            review['positivity'] = positivity

            # attribute
            review['attribute'] = zsl(review_content, attributeList)
            new_list.append(review)
        return new_list

