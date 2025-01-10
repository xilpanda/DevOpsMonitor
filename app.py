from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import os  # Import za rad sa environment varijablama

app = Flask(__name__)

# Konfiguracija baze podataka
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///servers.db')  # Koristi SQLite lokalno ili PostgreSQL na Heroku
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model za tabelu servera
class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False)

# Početna strana - lista servera
@app.route('/')
def index():
    servers = Server.query.all()
    return render_template('index.html', servers=servers)

# Forma za dodavanje novog servera
@app.route('/add', methods=['GET', 'POST'])
def add_server():
    if request.method == 'POST':
        name = request.form['name']
        status = request.form['status']
        new_server = Server(name=name, status=status)
        db.session.add(new_server)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('server_form.html', action="Add")

# Forma za izmjenu postojećeg servera
@app.route('/edit/<int:server_id>', methods=['GET', 'POST'])
def edit_server(server_id):
    server = Server.query.get(server_id)
    if not server:
        return "Server not found", 404

    if request.method == 'POST':
        server.name = request.form.get('name', server.name)
        server.status = request.form.get('status', server.status)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('server_form.html', action="Edit", server=server)

# Brisanje servera
@app.route('/delete/<int:server_id>', methods=['POST'])
def delete_server(server_id):
    server = Server.query.get(server_id)
    if server:
        db.session.delete(server)
        db.session.commit()
    return redirect(url_for('index'))

# API endpoint za vraćanje podataka iz baze kao JSON
@app.route('/api/servers', methods=['GET'])
def get_servers():
    servers = Server.query.all()
    pipelines_data = [
        {
            "id": server.id,
            "name": server.name,
            "status": server.status
        }
        for server in servers
    ]
    return jsonify(pipelines_data)

# Inicijalizacija baze podataka i dodavanje test podataka (samo lokalno)
with app.app_context():
    db.create_all()
    # Dodavanje test podataka ako baza nema nijedan unos
    if Server.query.count() == 0:
        test_servers = [
            Server(name="Server 1", status="Online"),
            Server(name="Server 2", status="Offline")
        ]
        db.session.add_all(test_servers)
        db.session.commit()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))  # Koristi port 5001 lokalno
    app.run(debug=False, host='0.0.0.0', port=port)
