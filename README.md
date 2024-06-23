Repository of the backend part of the iOS application: https://github.com/masllova/TaskNest-mobile

---

### Preconditions:
Python 3

API documentation (provided by Swagger UI)

---

### Run local
python3 -m venv venv

source venv/bin/activate

pip3 install -r ./requirements.txt

python3 -m uvicorn main:app --reload

---

### Run Docker 
sudo apt-get update

sudo apt-get install git

git clone https://github.com/masllova/TaskNest-backend.git

cd TaskNest-backend

docker build . --tag {tag} && docker run -p 8080:80 {tag}
