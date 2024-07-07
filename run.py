import os
from app import create_app

if __name__ == "__main__":
    config_name = os.getenv('FLASK_ENV', 'development')
    app = create_app(config_name)
    app.run(host='0.0.0.0', port=8000)
    