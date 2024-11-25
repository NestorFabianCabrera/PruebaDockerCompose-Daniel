from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{os.environ["POSTGRES_USER"]}:{os.environ["POSTGRES_PASSWORD"]}@{os.environ["DB_HOST"]}/{os.environ["POSTGRES_DB"]}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

# Crear las tablas de la base de datos si no existen
with app.app_context():
    db.create_all()

@app.route('/api/items', methods=['POST'])
def create_item():
    name = request.json['name']
    new_item = Item(name=name)
    db.session.add(new_item)
    db.session.commit()
    return jsonify(id=new_item.id, name=new_item.name)

@app.route('/api/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    results = [{"id": item.id, "name": item.name} for item in items]
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
