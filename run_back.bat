pip install virtualenv
virtualenv venv
call .\venv\Scripts\activate
pip install -r requirements.txt
flask --app api.py run