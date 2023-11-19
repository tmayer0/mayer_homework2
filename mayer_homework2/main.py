from flask import Flask
from app.database import db
from app.models import City, Country

app = Flask(__name__, template_folder='app/templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db.init_app(app)
app.config['SECRET_KEY'] = 'homework2'

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

from app import routes