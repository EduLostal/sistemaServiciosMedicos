from app import app
from flask_cors import CORS

# Habilitar CORS en tu aplicación Flask
CORS(app)

if __name__ == '__main__':
    app.run(debug=True)
 