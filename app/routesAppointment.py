from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from bson.objectid import ObjectId
from app import mongo

appointmentRoutes = Blueprint('appointmentRoutes', __name__)

# Ruta para crear citas médicas
@appointmentRoutes.route('/appointments', methods=['POST'])
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


# Ruta para listar citas médicas con filtros opcionales
@appointmentRoutes.route('/appointments', methods=['GET'])
@jwt_required()
def listAppointments():
    # Obtener el ID del usuario autenticado desde el token JWT
    userId = get_jwt_identity()

    # Acceder a las colecciones
    appointments = mongo.db.appointments
    users = mongo.db.users

    # Obtener parámetros de filtro desde la URL
    date_filter = request.args.get('date')  # Filtrar por fecha
    description_filter = request.args.get('description')  # Filtrar por descripción

    # Construir la consulta de búsqueda
    query = {"patient": ObjectId(userId)}

    if date_filter:
        query["date"] = date_filter
    if description_filter:
        query["description"] = {"$regex": description_filter, "$options": "i"}  # Búsqueda insensible a mayúsculas/minúsculas

    # Buscar citas en la base de datos
    userAppointments = list(appointments.find(query))

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
        return jsonify([]), 200


# Ruta para eliminar una cita asignada a un usuario
@appointmentRoutes.route('/appointments/<appointment_id>', methods=['DELETE'])
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


# Ruta para editar una cita médica
@appointmentRoutes.route('/appointments/<appointment_id>', methods=['PUT'])
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


