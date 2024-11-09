# Django Tailwind Template

Django starter with Tailwind CSS setup.

## Setup

```bash
# 1. Create project & activate environment
mkdir my-project
cd my-project
python -m venv env
env\Scripts\activate

# 2. Clone repo & install requirements
git clone https://github.com/your-username/django-tail-website.git .
pip install -r requirements.txt

# 3. Setup project
cd website
python manage.py tailwind install
python manage.py migrate

# 4. Run servers (in separate terminals)
python manage.py runserver
python manage.py tailwind start
