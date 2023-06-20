from anthropos import app
from anthropos.models.create_tables import create_tables


with app.app_context():
    if __name__ == '__main__':
        create_tables()
        app.run(host='0.0.0.0', debug=True)
