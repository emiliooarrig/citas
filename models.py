from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Configura la base de datos
DATABASE_URL = "mysql+pymysql://root:root@localhost/citas" 

# Crear motor de base de datos
engine = create_engine(DATABASE_URL, echo=True)

# Declarative base para definir los modelos
Base = declarative_base()

# Crear sesión
SessionLocal = sessionmaker(bind=engine)

# Crear una instancia de sesión
session = SessionLocal()


# Modelo de Usuarios
class Usuarios(Base):
    __tablename__ = "usuarios"
    id_user = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False)


# Modelo de Citas
class Citas(Base):
    __tablename__ = "dates"
    id_date = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('usuarios.id_user'))
    titulo = Column(String(100), nullable=False)
    descripcion = Column(String(255))
    fecha = Column(Date)
    hora = Column(Time)
    lugar = Column(String(255))
    fecha_creacion = Column(TIMESTAMP)

# Función para inicializar la base de datos
def init_db():
    Base.metadata.create_all(engine)



