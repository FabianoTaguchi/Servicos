import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'mysql+pymysql://root:root@localhost:3306/agromail?charset=utf8mb4')
def ensure_database(uri):
    from sqlalchemy.engine.url import make_url
    import pymysql
    url = make_url(uri)
    name = url.database
    conn = pymysql.connect(host=url.host, port=url.port or 3306, user=url.username, password=url.password, charset='utf8mb4', autocommit=True)
    cur = conn.cursor()
    cur.execute(f"CREATE DATABASE IF NOT EXISTS `{name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    cur.close()
    conn.close()
ensure_database(app.config['SQLALCHEMY_DATABASE_URI'])
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    ordens = db.relationship('OrdemServico', back_populates='solicitante')

class Cultivar(db.Model):
    __tablename__ = 'cultivares'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), unique=True, nullable=False)
    especie = db.Column(db.String(120))
    descricao = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.now())
    ordens = db.relationship('OrdemServico', back_populates='cultivar')

class OrdemServico(db.Model):
    __tablename__ = 'ordens'
    __table_args__ = (
        db.Index('ix_ordens_status', 'status'),
        db.Index('ix_ordens_solicitante', 'solicitante_id'),
    )
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text)
    status = db.Column(db.String(20), default='aberta')
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    solicitante_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cultivar_id = db.Column(db.Integer, db.ForeignKey('cultivares.id'))
    solicitante = db.relationship('User', back_populates='ordens')
    cultivar = db.relationship('Cultivar', back_populates='ordens')

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('index'))
        flash('Credenciais inválidas', 'danger')
    return render_template('login.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/cultivares', methods=['GET', 'POST'])
def cultivares():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        especie = request.form.get('especie', '').strip()
        if not nome:
            flash('Informe o nome do cultivar', 'warning')
        else:
            try:
                existente = Cultivar.query.filter_by(nome=nome).first()
                if existente:
                    flash('Cultivar já existe', 'warning')
                else:
                    c = Cultivar(nome=nome, especie=especie or None)
                    db.session.add(c)
                    db.session.commit()
                    flash('Cultivar cadastrado com sucesso', 'success')
            except Exception:
                db.session.rollback()
                flash('Erro ao salvar cultivar', 'danger')
        return redirect(url_for('cultivares'))
    lista = Cultivar.query.order_by(Cultivar.nome.asc()).all()
    return render_template('cultivares.html', cultivares=lista)

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
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        if not username or not password:
            flash('Informe usuário e senha', 'warning')
            return render_template('signup.html')
        if User.query.filter_by(username=username).first():
            flash('Usuário já existe', 'warning')
            return render_template('signup.html')
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Cadastro realizado, faça login', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    host = os.getenv('HOST', '127.0.0.1')
    port = int(os.getenv('PORT', '5600'))
    app.run(host=host, port=port, debug=True)