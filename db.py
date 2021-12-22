from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# El engine permite a SQLAlchemy comunicarse con la base de datos
# https://docs.sqlalchemy.org/en/14/core/engines.html

db_path = "products.db"

engine = create_engine(
    f"sqlite:///{db_path}", connect_args={"check_same_thread": False}
)

if not database_exists(engine.url):
    create_database(engine.url)

# Advertencia: Crear el engine no conecta inmediatamente a la base de datos, eso lo hacemos más adelante

# Ahora creamos la sesión, lo que nos permite realizar transacciones (operaciones) dentro de nuestra BD
Session = sessionmaker(bind=engine)
session = Session()

# Ahora vamos al fichero models.py y creamos nuestro modelo (nuestra clase) y la siguiente instrucción
# se encarga de mapear la clase o clases creadas y vincularlas a la base de datos
Base = declarative_base()
