pip install virtualenv
virtualenv venv
call .\venv\Scripts\activate
pip install -r requirements.txt
copy /b/v/y %cd%\config\qradar.py %cd%\venv\Lib\site-packages\sigma\backends
flask --app api.py run