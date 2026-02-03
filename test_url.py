from alembic.config import Config

cfg = Config("alembic.ini")
url = cfg.get_main_option("sqlalchemy.url")

print("URL repr:", repr(url))
print("Bytes:", list(url.encode("utf-8")))
