import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-change-me')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Recebe login e senha e redireciona para /index
        _username = request.form.get('username', '').strip()
        _password = request.form.get('password', '').strip()
        # Sem validação/persistência, apenas navegação
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/cultivares')
def cultivares():
    return render_template('cultivares.html')

@app.route('/ordens')
def ordens():
    return render_template('ordens.html')

@app.route('/ordens/minhas')
def ordens_minhas():
    return render_template('ordens_minhas.html')

@app.route('/ordens/todas')
def ordens_todas():
    return render_template('ordens_todas.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Recebe login e senha e retorna ao login
        _username = request.form.get('username', '').strip()
        _password = request.form.get('password', '').strip()
        return redirect(url_for('login'))
    return render_template('signup.html')

if __name__ == '__main__':
    host = os.getenv('HOST', '127.0.0.1')
    port = int(os.getenv('PORT', '5600'))
    app.run(host=host, port=port, debug=True)