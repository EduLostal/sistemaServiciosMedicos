from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from bson.objectid import ObjectId
from app import mongo

sistemaRoutes = Blueprint('sistema', __name__)

# Ruta para registrar usuarios
@sistemaRoutes.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    users = mongo.db.users

    if users.find_one({"email": email}):
        return jsonify({"error": "El email ya está registrado"}), 400

    hashedPassword = generate_password_hash(password)
    users.insert_one({"name": name, "email": email, "password": hashedPassword})

    return jsonify({"message": "Usuario registrado exitosamente"}), 201


# Ruta para login de usuarios
@sistemaRoutes.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    users = mongo.db.users
    user = users.find_one({"email": email})

    if not user or not check_password_hash(user['password'], password):
        return jsonify({"error": "Credenciales inválidas"}), 401

    accessToken = create_access_token(identity=str(user["_id"]))
    return jsonify({"token": accessToken}), 200


# Ruta para crear citas médicas
@sistemaRoutes.route('/appointments', methods=['POST'])
@jwt_required()
def createAppointment():
    data = request.json
    date = data.get('date')
    description = data.get('description')

    userId = get_jwt_identity()
    appointments = mongo.db.appointments

    appointment = {
        "date": date,
        "description": description,
        "patient": ObjectId(userId)
    }
    appointments.insert_one(appointment)

    return jsonify({"message": "Cita creada exitosamente"}), 201


# Ruta para listar citas médicas
@sistemaRoutes.route('/appointments', methods=['GET'])
@jwt_required()
def listAppointments():
    # Obtener el ID del usuario autenticado desde el token JWT
    userId = get_jwt_identity()

    # Acceder a las colecciones
    appointments = mongo.db.appointments
    users = mongo.db.users

    # Buscar citas relacionadas con el usuario autenticado
    userAppointments = list(appointments.find({"patient": ObjectId(userId)}))

    if userAppointments:
        # Convertir ObjectId a cadenas y agregar el nombre del paciente
        for appointment in userAppointments:
            # Obtener el paciente asociado  
            patient = users.find_one({"_id": ObjectId(appointment["patient"])})
            if patient:
                appointment["patient"] = patient["name"]  # Reemplazar ID por el nombre
            else:
                appointment["patient"] = "Paciente no encontrado"

            # Convertir _id a string
            appointment["_id"] = str(appointment["_id"])

        # Devolver la lista de citas con nombres de pacientes
        return jsonify(userAppointments), 200
    
    else:
        return jsonify({"message": "No se encontraron citas para este usuario"}), 404


# Ruta para eliminar una cita asignada a un usuario
@sistemaRoutes.route('/appointments/<appointment_id>', methods=['DELETE'])
@jwt_required()
def deleteAppointment(appointment_id):
    appointments = mongo.db.appointments
    userId = get_jwt_identity()

    # Verificar si el appointment existe y pertenece al usuario
    appointment = appointments.find_one({"_id": ObjectId(appointment_id), "patient": ObjectId(userId)})

    if not appointment:
        return jsonify({"error": "Cita no encontrada"}), 404

    # Eliminar la cita
    appointments.delete_one({"_id": ObjectId(appointment_id)})
    return jsonify({"message": "Cita eliminada exitosamente"}), 200


# Ruta para eliminar un usuario
@sistemaRoutes.route('/users', methods=['DELETE'])
@jwt_required()
def deleteUser():
    users = mongo.db.users
    user_id = get_jwt_identity()

    # Verificar si el usuario existe 
    user = users.find_one({"_id": ObjectId(user_id)})

    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    # Eliminar el usuario
    users.delete_one({"_id": ObjectId(user_id)})
    return jsonify({"message": "Usuario eliminada exitosamente"}), 200


# Ruta para editar una cita médica
@sistemaRoutes.route('/appointments/<appointment_id>', methods=['PUT'])
@jwt_required()
def editAppointment(appointment_id):
    # Obtener el ID del usuario autenticado desde el token JWT
    userId = get_jwt_identity()

    # Acceder a las colecciones
    appointments = mongo.db.appointments

    # Buscar la cita médica por su ID y verificar que pertenezca al usuario
    appointment = appointments.find_one({"_id": ObjectId(appointment_id), "patient": ObjectId(userId)})

    if not appointment:
        return jsonify({"message": "Cita no encontrada"}), 404

    # Obtener los datos del cuerpo de la solicitud
    data = request.json
    date = data.get("date")
    description = data.get("description")

    # Crear el objeto de actualización
    update_data = {}
    if date:
        update_data["date"] = date
    if description:
        update_data["description"] = description

    if not update_data:
        return jsonify({"message": "No se proporcionaron datos editar la cita"}), 400

    # Actualizar la cita en la base de datos
    appointments.update_one(
        {"_id": ObjectId(appointment_id)},
        {"$set": update_data}
    )

    # Devolver un mensaje de éxito
    return jsonify({"message": "Cita actualizada exitosamente"}), 200


# Ruta para editar un usuario
@sistemaRoutes.route('/users', methods=['PUT'])
@jwt_required()
def editUser():
    # Obtener el ID del usuario autenticado desde el token JWT
    users_id = get_jwt_identity()

    # Acceder a las colecciones de usuario
    users = mongo.db.users

    # Buscar la cita médica por su ID y verificar que pertenezca al usuario
    user = users.find_one({"_id": ObjectId(users_id)})

    if not user:
        return jsonify({"message": "Usuario no encontrado"}), 404

    # Obtener los datos del cuerpo de la solicitud
    data = request.json
    name = data.get("name")
    email = data.get("description")
    password = data.get("pasword")

    
    # Crear el objeto de actualización
    update_data = {}
    if name:
        update_data["name"] = name
    if email:
        update_data["email"] = email
    if password:
        hashedPassword = generate_password_hash(password)
        update_data["password"] = hashedPassword

    if not update_data:
        return jsonify({"message": "No se proporcionaron datos editar el usuario"}), 400

    # Actualizar la cita en la base de datos
    users.update_one(
        {"_id": ObjectId(users_id)},
        {"$set": update_data}
    )

    # Devolver un mensaje de éxito
    return jsonify({"message": "Cita actualizada exitosamente"}), 200

