Repository of the backend part of the iOS application: https://github.com/masllova/TaskNest-mobile

---

### Preconditions:
Python 3

---

### Run local
python3 -m venv venv

source venv/bin/activate

pip3 install -r ./requirements.txt

python3 -m uvicorn main:app --reload

API documentation (provided by Swagger UI)
http://127.0.0.1:8000/docs
