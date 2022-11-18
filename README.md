# Lending Tree Business Reviews

## Setup
run `pip3 install -r requirements.txt` for all dependencies required to start the app

## Running the app
run `uvicorn business_reviews_route:lending_tree_app --reload` to start the app. The server should be running on `http://127.0.0.1:8000`

## How to send requests
Use postman with the following url and route...
`http://127.0.0.1:8000/business/{business}/{business_id}`

## Testing
run `python3 -m pytest` to run tests