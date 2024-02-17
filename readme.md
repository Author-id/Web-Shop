[![pipeline status](https://gitlab.crja72.ru/django/2024/spring/course/students/249419-semyanovandrew-course-1112/badges/main/pipeline.svg)](https://gitlab.crja72.ru/django/2024/spring/course/students/249419-semyanovandrew-course-1112/-/commits/main)

# How to run it on windows
1. Clone this repo and prepare workplace:  
git clone https://gitlab.crja72.ru/django/2024/spring/course/students/249419-semyanovandrew-course-1112  
cd 249419-semyanovandrew-course-1112  
python -m venv venv  
venv\scripts\activate  

2. Rename .env.example to .env to set test environment variables:
ren ".env.example" ".env"  

3. Install requirements:  
pip install --upgrade pip  
pip install -r requirements\prod.txt  
pip install -r requirements\test.txt  
pip install -r requirements\dev.txt  

4. Run it by this command:  
cd lyceum  
python manage.py runserver  

Then the application will start on http://localhost:8000


# How to run it on Linux OS

1. Clone this repo and prepare workplace:  
git clone https://gitlab.crja72.ru/django/2024/spring/course/students/249419-semyanovandrew-course-1112  
cd 249419-semyanovandrew-course-1112  
python3 -m venv venv  
venv/bin/activate  

2. Rename .env.example to .env to set test environment variables:  
mv .env.example .env  

3. Install requirements  
pip3 install --upgrade pip  
pip3 install -r requirements/prod.txt  
pip3 install -r requirements/test.txt  
pip3 install -r requirements/dev.txt  

4. Run it by this command:  
cd lyceum  
python3 manage.py runserver  

Then the application will start on http://localhost:8000
