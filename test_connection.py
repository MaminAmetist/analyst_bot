import os
from sqlalchemy import create_engine
import sys

# --- ВАША ЧИСТАЯ СТРОКА ПОДКЛЮЧЕНИЯ ИЗ ENV.PY ---
# Скопируйте её сюда вручную
db_url = "postgresql+psycopg2://prj_user:new_password123@localhost:5432/videos_db"

print(f"URL длина: {len(db_url)}")

# Позиция 61 - это 62-й символ. Посмотрим, что он видит
try:
    print(f"Символ на позиции 61: '{db_url[61]}'")
except IndexError:
    print("Длина URL меньше 62 символов.")

# Печать байтов вокруг проблемной позиции (58-65), чтобы увидеть мусор
try:
    bytes_repr = db_url.encode('utf-8')
    print(f"Байты (фрагмент 58-65): {bytes_repr[58:65]}") 
except Exception as e:
    print(f"Ошибка кодирования байтов: {e}")

try:
    engine = create_engine(db_url)
    connection = engine.connect()
    print("Соединение успешно установлено!")
    connection.close()
except Exception as e:
    print(f"Ошибка при соединении: {e}")
    sys.exit(1)