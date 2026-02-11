# TaskBox API — REST

## გაშვების ინსტრუქცია (Setup Instructions)

### წინაპირობები (Prerequisites)
- Python 3.8+
- pip
- virtualenv (რეკომენდებული)
- PostgreSQL/MySQL/SQLite (დამოკიდებულია შენს არჩევანზე)

### ინსტალაცია და გაშვება

1. **რეპოზიტორის კლონირება:**
```bash
git clone 
cd 
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
შექმენი `.env` ფაილი პროექტის root დირექტორიაში:
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
# ან PostgreSQL-ისთვის:
# DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

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

curl -X POST http://127.0.0.1:8000/api/auth/token/ \
-H "Content-Type: application/json" \
-d '{"username":"user1","password":"password123"}'

curl -X GET http://127.0.0.1:8000/api/tasks/ \
-H "Authorization: Bearer TOKEN"

curl -X GET http://127.0.0.1:8000/api/tasks/1/ \
-H "Authorization: Bearer TOKEN"

curl -X DELETE http://127.0.0.1:8000/api/tasks/1/ \
-H "Authorization: Bearer TOKEN"

curl -X GET "http://localhost:8000/api/tasks/?priority=HIGH" 
-H "Authorization: Bearer TOKEN"

curl -X GET "http://localhost:8000/api/tasks/?is_done=false" 
-H "Authorization: Bearer TOKEN"