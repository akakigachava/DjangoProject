# TaskBox API — REST
- JWT Authentication (login/refresh)
- CRUD for tasks
- Pagination (page size 10)
- Filtering / Search / Ordering

## გაშვების ინსტრუქცია (Setup Instructions)

### წინაპირობები (Prerequisites)
- Python 3.8+
- pip
- virtualenv (რეკომენდებული)
- PostgreSQL/MySQL/SQLite (დამოკიდებულია შენს არჩევანზე)

### ინსტალაცია და გაშვება

1. **რეპოზიტორის კლონირება:**
```bash
git clone https://github.com/akakigachava/DjangoProject.git
cd DjangoProject
```

2. **ვირტუალური გარემოს შექმნა და გააქტიურება:**
```bash
python -m venv venv
# Windows-ზე:
venv\Scripts\activate
# Mac/Linux-ზე:
source venv/bin/activate
```

3. **requirements ინსტალაცია:**
```bash
pip install -r requirements.txt
```

4. **გარემოს ცვლადების კონფიგურაცია:**
შექმენი `.env` ფაილი პროექტის root დირექტორიში:
```env
SECRET_KEY=some_random_generated_key
DEBUG=True
```
.env ფაილი იგნორირებულია git-ის მიერ და არ აიტვირთება GitHub-ზე.


5. **მიგრაციების გაშვება:**
```bash
python manage.py makemigrations
python manage.py migrate
```


6. **სერვერის გაშვება:**
```bash
python manage.py runserver
```

7. **აპლიკაცია გაეშვება:** `http://127.0.0.1:8000/`


API დოკუმენტაცია

Swagger UI:
http://127.0.0.1:8000/api/docs/

ReDoc:
http://127.0.0.1:8000/api/redoc/

OpenAPI Schema:
http://127.0.0.1:8000/api/schema/


## Authentication Flow

### 1. რეგისტრაცია (Registration)
მომხმარებელი აგზავნის POST request-ს რეგისტრაციისთვის და იღებს access token-ს.

### 2. ავტორიზაცია (Login)
მომხმარებელი შედის სისტემაში username/email და password-ით, იღებს JWT token-ს.

### 3. Token-ით ავტორიზაცია
ყველა დაცულ endpoint-ზე წვდომისთვის საჭიროა Authorization header:
```
Authorization: Bearer <your-access-token>
```




## Example Requests (curl)

### 1. Login (JWT Token მიღება)
```bash

1) რეგისტრაცია
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
-H "Content-Type: application/json" \
-d '{"username":"user1","password":"password123"}'


2) Login (JWT token მიღება)
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
-H "Content-Type: application/json" \
-d '{"username":"user1","password":"password123"}'

3) Refresh token
curl -X POST http://127.0.0.1:8000/api/auth/refresh/ \
-H "Content-Type: application/json" \
-d '{"refresh":"REFRESH_TOKEN_HERE"}'

4) task-ების მოძებნა კონკრეტული user-ისთვის (GET)
curl -X GET http://127.0.0.1:8000/api/tasks/ \
-H "Authorization: Bearer TOKEN"

5) task-ის შექმნა (POST)
curl -X POST http://127.0.0.1:8000/api/tasks/ \
-H "Authorization: Bearer TOKEN" \
-H "Content-Type: application/json" \
-d '{"title":"Math homework","description":"Chapter 3","priority":"LOW"}'

6) task-ის ძებნა id-ით
curl -X GET http://127.0.0.1:8000/api/tasks/1/ \
-H "Authorization: Bearer TOKEN"

7) ამოცანის განახლება (PATCH)
curl -X PATCH http://127.0.0.1:8000/api/tasks/1/ \
-H "Authorization: Bearer TOKEN" \
-H "Content-Type: application/json" \
-d '{"is_done": true}'


8) task-ის წაშლა
curl -X DELETE http://127.0.0.1:8000/api/tasks/1/ \
-H "Authorization: Bearer TOKEN"


9) ფილტრაციის მაგალითები
curl -X GET "http://127.0.0.1:8000/api/tasks/?priority=HIGH" \
-H "Authorization: Bearer TOKEN"

curl -X GET "http://127.0.0.1:8000/api/tasks/?is_done=false" \
-H "Authorization: Bearer TOKEN"


---

## ტესტების გაშვება (Running Tests)
პროექტში გამოყენებულია Django-ის built-in testing framework.
ტესტების გასაშვებად:
```bash
python manage.py test