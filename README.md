# Proyecto de Citas Médicas

Este proyecto es una aplicación web para la gestión de citas médicas. Implementa un sistema que permite gestionar usuarios (crear, editar y eliminar), iniciar sesión, y gestionar citas médicas (crear, listar, editar y eliminar) mediante un backend en python, una base de datos en MongoDB y un front para el que he utilizado JS y HTML.

## Tecnologías Utilizadas

### Backend
- **Flask**: Framework de desarrollo web en Python.
- **Flask-PyMongo**: Para interactuar con MongoDB.
- **Flask-JWT-Extended**: Para la gestión de autenticación y autorización mediante tokens JWT.
- **Werkzeug**: Para la generación y validación de contraseñas seguras.
- **Python-dotenv**: Para cargar variables de entorno (en este caso las del archivo .env).
- **MongoDB**: Base de datos para almacenar usuarios y citas médicas.
- **Flask-CORS**: Para permitir solicitudes desde diferentes dominios.

### Frontend
- **HTML, CSS, JavaScript**: Para el desarrollo de la interfaz de usuario.
- **Bootstrap**: Para el diseño responsivo y para mejorar la estetica con diferentes estilos.

---

## Instalación y Configuración

1. **Clona el repositorio**:
   ```
   git clone <URL_DEL_REPOSITORIO>
   ```

2. **Crea un entorno virtual con Anaconda**:
   ```bash
   conda create --name sistemaServiciosMedicos 
   Para activarlo --> conda activate citasMedicas
   ```

3. **Instala las dependencias**:
   ```
   pip install -r requirements.txt
   ```

4. **Configura las variables de entorno**:
   Crea un archivo .env en la raíz del proyecto con el siguiente contenido:
   ```
   MONGO_URI=mongodb://127.0.0.1:27017/sistemaServiciosMedicos
   JWT_SECRET_KEY=citasMedicas0077
   ```

5. **Ejecuta la aplicación**:
   ```
   python run.py
   ```
   El servidor estará disponible en http://127.0.0.1:5000/.

---

## Endpoints del Backend

### Usuarios

1. **Registro de Usuarios**
   - **POST** `/register`
   - **Cuerpo**:
     ```json
     {
       "name": "string",
       "email": "string",
       "password": "string"
     }
     ```
   - **Respuesta**:
     - **201** Usuario registrado exitosamente.
     - **400** Email ya registrado.

2. **Inicio de Sesión**
   - **POST** `/login`
   - **Cuerpo**:
     ```json
     {
       "email": "string",
       "password": "string"
     }
     ```
   - **Respuesta**:
     - **200** Token JWT.
     - **401** Credenciales inválidas.

3. **Editar Usuario**
   - **PUT** `/users` (Requiere Autenticación JWT)
   - **Cuerpo**:
     ```json
     {
       "name": "string",
       "email": "string",
       "password": "string"
     }
     ```
   - **Respuesta**:
     - **200** Usuario actualizado exitosamente.
     - **404** Usuario no encontrado.

4. **Eliminar Usuario**
   - **DELETE** `/users` (Requiere Autenticación JWT)
   - **Respuesta**:
     - **200** Usuario eliminado exitosamente.
     - **404** Usuario no encontrado.

### Citas Médicas

1. **Crear Cita**
   - **POST** `/appointments` (Requiere Autenticación JWT)
   - **Cuerpo**:
     ```json
     {
       "date": "string",
       "description": "string"
     }
     ```
   - **Respuesta**:
     - **201** Cita creada exitosamente.

2. **Listar Citas**
   - **GET** `/appointments` (Requiere Autenticación JWT)
   - **Parámetros Opcionales**:
     - `date` (string): Filtrar citas por fecha.
     - `description` (string): Filtrar citas por descripción.
   - **Respuesta**:
     - **200** Lista de citas.

3. **Editar Cita**
   - **PUT** `/appointments/<appointment_id>` (Requiere Autenticación JWT)
   - **Cuerpo**:
     ```json
     {
       "date": "string",
       "description": "string"
     }
     ```
   - **Respuesta**:
     - **200** Cita actualizada exitosamente.
     - **404** Cita no encontrada.

4. **Eliminar Cita**
   - **DELETE** `/appointments/<appointment_id>` (Requiere Autenticación JWT)
   - **Respuesta**:
     - **200** Cita eliminada exitosamente.
     - **404** Cita no encontrada.



## Frontend
El frontend del sistema de gestión de citas médicas permite interactuar con el backend mediante peticiones HTTP. Incluye las siguientes funcionalidades:

### 1. **Login de Usuarios**
- Archivo: `login.js`
- Descripción: Permite a los usuarios autenticarse ingresando su correo electrónico y contraseña. Si las credenciales son válidas, se almacena el token JWT en el almacenamiento local y se redirige al usuario a la página principal.

### 2. **Registro de Usuarios**
- Archivo: `register.js`
- Descripción: Permite a los usuarios registrarse proporcionando su nombre, correo electrónico y contraseña. Redirige al formulario de login tras un registro exitoso.

### 3. **Gestor de Citas**
- Archivo: `main.js`
- Funciones principales:
  - Crear citas.
  - Listar citas existentes (con soporte para filtros por fecha y descripción).
  - Editar citas.
  - Eliminar citas.
  - Verifica la autenticación del usuario mediante el token JWT antes de permitir el acceso a estas funcionalidades.

### 4. **Gestor de Usuarios**
- Opciones disponibles:
  - Editar la información del usuario autenticado.
  - Eliminar la cuenta del usuario autenticado.

### 5. **Cerrar Sesión**
- Archivo: `main.js`
- Descripción: Permite cerrar sesión eliminando el token JWT del almacenamiento local y redirigiendo al usuario a la página de login.

---

## Autenticación
Este proyecto utiliza JWT (JSON Web Tokens) para autenticar y autorizar usuarios. Cada solicitud a los endpoints protegidos requiere un token JWT en los encabezados:

