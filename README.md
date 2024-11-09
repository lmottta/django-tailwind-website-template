# Setup Instructions

Assuming you are on Windows

## 1) Create project & start environment
```bash
mkdir <project-name>
cd <project-name>
python -m venv <environment-name>
<environment-name>\Scripts\activate
```

## 2) Clone repo & install packages
```bash
git clone https://github.com/JoeWat2005/django-tailwind-website-template.git
pip install -r requirements.txt
```

## 3) Setup project
```bash
cd website
python manage.py tailwind install
python manage.py migrate
```

## 4) Run servers (in separate terminals)
```bash
python manage.py runserver
python manage.py tailwind start
```
