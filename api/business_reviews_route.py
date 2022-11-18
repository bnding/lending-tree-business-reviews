from fastapi import FastAPI, status
from business_reviews_service import BusinessReviewsService

lending_tree_app = FastAPI()

@lending_tree_app.get('/business/{business_name}/{business_id}', status_code=status.HTTP_200_OK)
def get_all_reviews_from_business(business_name: str, business_id: int):
    reviews = BusinessReviewsService().parse_all_reviews(business=business_name, business_id=business_id)
    return reviews