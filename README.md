# Author-CMS

Step 1 :- Create a virtual enviroment for the app.

Step 2 :- Install dependencies using `pip install -r requirements.txt`.

Step 3 :- Make migrations and migrate it to database. 
`python manage.py makemigrations` && `python manage.py migrate`

Step 4 :- Start the development server using command `python manage.py runserver`

### To Create a User 

 - (POST) `http://localhost:8000/app/create-user/`
    - email (required)
    - password (required)
    - first_name (required)
    - last_name (required)
    - phone (required)
    - pincode (required)
    - address
    - city
    - state
    - country


### To Sign in to your account (Get the token for auth)

  - (POST) `http://localhost:8000/app/signin/`
      - email (required)
      - password (required)

## All request from here should be made using the token for auth

### To Create a Post

 - (POST) `http://localhost:8000/app/content/`
      - title
      - body
      - summary
      - categories (comma seperated string ex "new, try, hit")
      - files (should be send in file format)
      Ex - `requests.post('http://localhost:8000/app/content/', data={"title":"asdad 213 sdaas", "body":"asdasdasdasdasdasdads asdadad asd asdasdasd", "summary":"asdas asdasd asdasd", "categories":"test, try, new"}, files=files, headers=headers)`
      
### To get posts

  - (GET) `http://localhost:8000/app/content/`
      - Can use 'search' parameter here

### To update post

  - (PUT) `http://localhost:8000/app/content/`
      - 'id' this is id we got from api above
      - Data will be - title, summary, body (can use multiple params as well as single)
      Ex - `requests.put('http://localhost:8000/app/create-content/?id=5', data={"title":"Test title", "body":"Lets see what happens", "summary":"asdas asdasd asdasd"}, headers=headers)`
     
### To delete post

  - (DELETE) `http://localhost:8000/app/content/`
      - 'id'
     Ex - `requests.delete('http://localhost:8000/app/create-content/?id=4', headers=headers)`
