from unittest import mock
from api.business_reviews_route import get_all_reviews_from_business

class TestBusinessRoutes():
    
    @mock.patch('business_reviews_service.BusinessReviewsService.parse_all_reviews')
    def test_get_all_reviews_from_business_success(self, mock_parse_all_reviews):
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
        
        business_name = "a-business-name"
        business_id = 12345
        total_pages = 1
        mock_parse_all_reviews.return_value = {
            'business_name': business_name,
            'business_id': 12345,
            'total_pages': 1,
            'reviews': [review_1]
        }
        
        response = get_all_reviews_from_business(business_name, business_id)
        
        assert response['business_name'] == business_name
        assert response['business_id'] == business_id
        assert response['total_pages'] == total_pages
        assert response['reviews'][0] == review_1