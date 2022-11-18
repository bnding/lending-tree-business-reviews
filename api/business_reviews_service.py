from bs4 import BeautifulSoup
import requests
from fastapi import HTTPException, status
import re
from typing import List


class BusinessReviewsService():
    
    def parse_all_reviews(self, business: str, business_id: int):
        curr_page = 1
        main_reviews_arr = []

        # Incrementing by pid pages NOTE: clicking 'Next' causes us to lose last 4 pages
        while (True):
            reviews_in_current_page = self.__parse_reviews_in_current_page(business, business_id, curr_page)

            if (len(reviews_in_current_page) == 0):
                break
            
            for review in reviews_in_current_page:
                main_reviews_arr.append(review)

            curr_page += 1

        reviews_dict = {}

        if (len(main_reviews_arr) == 0):
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,
                                detail=f"The business '{business}' with business id {business_id} has no existing reviews. Please check that the business name and business id are correct.")

        reviews_dict = {
            'business_name': business,
            'business_id': business_id,
            'reviews': main_reviews_arr,
            'total_pages': curr_page
        }

        return reviews_dict

    def __parse_reviews_in_current_page(self, business: str, business_id: int, curr_page: int) -> List[str]:
        url = f"https://www.lendingtree.com/reviews/business/{business}/{str(business_id)}?sort=&pid={str(curr_page)}"
        main_reviews_in_curr_page_arr = []

        # Disabling redirects if request has an invalid business name or id
        
        main_reviews_soup = self.__get_main_reviews_in_current_page_soup(url)

        for review in main_reviews_soup:
            review_title = review.find(
                'p', {'class': "reviewTitle"}).text.strip()
            review_content = review.find(
                'p', {'class': "reviewText"}).text.strip()

            # using regex to split author name, city, and state
            author_info = re.split(' from |, ', review.find(
                'p', {'class': "consumerName"}).text)

            # Improvement: enumerate this into a separate class
            states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana',
                      'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']

            # Breaking up author_info into key values. NOTE: some reviews do not have city+state
            author_info_dict = {}
            if (len(author_info) == 0):
                author_info_dict['author_name'] = None
                author_info_dict['author_city'] = None
                author_info_dict['author_state'] = None
            elif (len(author_info) == 1):
                author_info_dict['author_name'] = author_info[0].strip()
                author_info_dict['author_city'] = None
                author_info_dict['author_state'] = None
            elif (len(author_info) == 2 and author_info[1].strip() in states):
                author_info_dict['author_name'] = author_info[0].strip()
                author_info_dict['author_city'] = None
                author_info_dict['author_state'] = author_info[1].strip()
            elif (len(author_info) == 2 and author_info[1].strip() not in states):
                author_info_dict['author_name'] = author_info[0].strip()
                author_info_dict['author_city'] = author_info[1].strip()
                author_info_dict['author_state'] = None
            elif (len(author_info) == 3):
                author_info_dict['author_name'] = author_info[0].strip()
                author_info_dict['author_city'] = author_info[1].strip()
                author_info_dict['author_state'] = author_info[2].strip()

            # searching for both digits and placing them in an array: [numerator, denominator]
            star_rating = re.sub(
                r'\s+|[stars()]', "", review.find('div', {'class': "numRec"}).text).split("of")

            date_posted = review.find('p', {'class': "consumerReviewDate"}).text.strip(
            ).replace("Reviewed in ", "").split()
            date_posted_dict = {
                'month': date_posted[0],
                'year': date_posted[1]
            }

            # Ideas: Maybe we could add if the review was flagged or not? We can add the "recommended" field as well

            main_reviews_in_curr_page_arr.append(
                {
                    'review_title': review_title,
                    'review_content': review_content,
                    'author_info': author_info_dict,
                    'star_rating': star_rating,
                    'date_posted': date_posted_dict
                }
            )

        return main_reviews_in_curr_page_arr

    def __get_main_reviews_in_current_page_soup(self, url: str):
        response_html_content = requests.get(
            url, allow_redirects=False).content
        soup = BeautifulSoup(response_html_content, 'lxml')
        return soup.find_all('div', {'class': "mainReviews"})