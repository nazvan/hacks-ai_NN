# FastAPI backend для сервиса онлайн-отображения дефектов дорожного покрытия.
# Всероссийский хакатон Hacks-AI, Нижний Новгород, 8-10 сентября 2023 г.

# Для установки необходимо развернуть и активировать виртуальную среду virtualenv

pip3 install virtualenv
python3 -m virtualenv venv
source venv/bin/activate

# Установить зависимости

pip3 install -r requirements.txt

# Запустить uvicorn

cd ./src/
uvicorn app:app 
