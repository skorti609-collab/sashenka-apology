Файлы проекта:
- app.py — Flask-приложение
- templates/index.html — страница выбора даты
- templates/place.html — страница выбора места
- templates/thanks.html — финальная страница
- requirements.txt и Procfile — настройки Render

На GitHub загружайте файлы с сохранением структуры папок. Для Render:
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
