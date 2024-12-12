from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os


# Cargar variables de entorno
load_dotenv()

# Inicializar Flask
app = Flask(__name__)

# Configuraciones
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
print(os.getenv("MONGO_URI"))
# Inicializar extensiones
mongo = PyMongo(app)
jwt = JWTManager(app)

# Registrar rutas
from app.routesUser import userRoutes
app.register_blueprint(userRoutes)

from app.routesAppointment import appointmentRoutes
app.register_blueprint(appointmentRoutes)
