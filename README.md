# Lending Tree Business Reviews

## Setup
run `pip3 install -r requirements.txt` for all dependencies required to start the app

## Running the app
cd into `api` and run `uvicorn business_reviews_route:lending_tree_app --reload` to start the app. The server should be running on `http://127.0.0.1:8000`

## How to send requests
* Find and click one of the businesses in the following link: https://www.lendingtree.com/reviews/business/
* Note and copy the business and business_id in the link
  
Use postman with the following url and route...

`http://127.0.0.1:8000/business/{business}/{business_id}`

send a get request to receive a json response for all reviews

Invalid business names/business_ids returns a `204 No Content` response

## Testing
run `python3 -m pytest` to run tests