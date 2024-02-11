[![pipeline status](https://gitlab.crja72.ru/django/2024/spring/course/students/197180-ivan3624-course-1112/badges/main/pipeline.svg)](https://gitlab.crja72.ru/django/2024/spring/course/students/197180-ivan3624-course-1112/-/commits/main)

# Setup Commands

- You should rename .env.example to .env

```
mv .env.example .env
```

```
python3 -m venv venv
```

```
source venv/bin/activate
```

```
pip install -r requirements/prod.txt
```

```
pip install -r requirements/test.txt
```

```
pip install -r requirements/dev.txt
```

```
cd lyceum
```

```
python3 manage.py runserver
```
