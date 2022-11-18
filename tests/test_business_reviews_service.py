import pytest
from unittest import mock
from api.business_reviews_service import BusinessReviewsService
from tests.bs_reviews_result_set_sample import bs_reviews_result_set
from bs4 import BeautifulSoup
from fastapi import HTTPException


class TestBusinessService():

    @mock.patch('api.business_reviews_service.BusinessReviewsService._BusinessReviewsService__parse_reviews_in_current_page')
    def test_get_all_reviews_from_business_success(self, mock_parse_reviews_in_current_page):
        # Improvement: Make this a fixture

        review_1 = {
            "review_title": "John Ly was the greatest",
            "review_content": "John Ly was the greatest! A real yes man who was able to give me the facts! I am super happy with his service and the experience.",
            "author_info": {
                "author_name": "Amy",
                "author_city": "San Rafael",
                "author_state": "CA"
            },
            "star_rating": [
                "5",
                "5"
            ],
            "date_posted": {
                "month": "January",
                "year": "2019"
            }
        }

        review_2 = {
            "review_title": "Great service",
            "review_content": "Very friendly, clear and quick.",
            "author_info": {
                "author_name": "Angelina",
                "author_city": "El Cajon",
                "author_state": "CA"
            },
            "star_rating": [
                "5",
                "5"
            ],
            "date_posted": {
                "month": "January",
                "year": "2019"
            }
        }

        mock_parse_reviews_in_current_page.side_effect = [
            [review_1], [review_2], []]

        response = BusinessReviewsService().parse_all_reviews('a-business-name', 12345)

        assert len(response['reviews']) == 2
        assert response['reviews'][0] == review_1
        assert response['reviews'][1] == review_2
    
    @mock.patch('api.business_reviews_service.BusinessReviewsService._BusinessReviewsService__parse_reviews_in_current_page')
    def test_get_all_reviews_from_business_failure(self, mock_parse_reviews_in_current_page):
        mock_parse_reviews_in_current_page.side_effect = [[]]
        
        business_name = 'a-business-name'
        business_id = 12345
        
        with pytest.raises(HTTPException) as ex:
            BusinessReviewsService().parse_all_reviews(business_name, 12345)
            
        assert ex.value.status_code == 204
        assert ex.value.detail == f"The business '{business_name}' with business id {business_id} has no existing reviews. Please check that the business name and business id are correct."

        


    @mock.patch('api.business_reviews_service.BusinessReviewsService._BusinessReviewsService__get_main_reviews_in_current_page_soup')
    def test__parse_reviews_in_current_page(self, mock_get_main_reviews_in_current_page_soup):
        mock_get_main_reviews_in_current_page_soup.return_value = BeautifulSoup(
            bs_reviews_result_set, "lxml")

        expected_review_format = {
            "review_title": "Very professional",
            "review_content": "Very professional.  We are a repeat client.",
            "author_info": {
                "author_name": "AC",
                "author_city": "Dana Point",
                "author_state": "CA"
            },
            "star_rating": [
                "5",
                "5"
            ],
            "date_posted": {
                "month": "September",
                "year": "2019"
            }
        }

        reviews = BusinessReviewsService(
        )._BusinessReviewsService__parse_reviews_in_current_page('a-business-name', 12345, 1)
        
        assert reviews[0] == expected_review_format