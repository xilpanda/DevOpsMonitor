from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Test podaci
servers = [
    {"id": 1, "name": "Server 1", "status": "Online"},
    {"id": 2, "name": "Server 2", "status": "Offline"}
]

# Početna strana - lista servera
@app.route('/')
def index():
    return render_template('index.html', servers=servers)

# Forma za dodavanje novog servera
@app.route('/add', methods=['GET', 'POST'])
def add_server():
    if request.method == 'POST':
        new_id = len(servers) + 1
        name = request.form['name']
        status = request.form['status']
        servers.append({"id": new_id, "name": name, "status": status})
        return redirect(url_for('index'))
    return render_template('server_form.html', action="Add")

# Forma za izmjenu postojećeg servera
@app.route('/edit/<int:server_id>', methods=['GET', 'POST'])
def edit_server(server_id):
    server = next((s for s in servers if s['id'] == server_id), None)
    if not server:
        return "Server not found", 404
    if request.method == 'POST':
        server['name'] = request.form['name']
        server['status'] = request.form['status']
        return redirect(url_for('index'))
    return render_template('server_form.html', action="Edit", server=server)

# Brisanje servera
@app.route('/delete/<int:server_id>', methods=['POST'])
def delete_server(server_id):
    global servers
    servers = [s for s in servers if s['id'] != server_id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
