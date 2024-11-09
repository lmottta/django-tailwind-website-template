# Django Tailwind Template

Django starter with Tailwind CSS setup.

## Setup

### 1. Create project & activate environment
```bash
mkdir my-project
cd my-project
python -m venv env
env\Scripts\activate
```

### 2. Clone repo & install requirements
```bash
git clone https://github.com/your-username/django-tail-website.git .
pip install -r requirements.txt
```

### 3. Setup project
```bash
cd website
python manage.py tailwind install
python manage.py migrate
```

### 4. Run servers (in separate terminals)
```bash
python manage.py runserver
python manage.py tailwind start
```
