# Importação das bibliotecas a serem utilizadas
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

# Configuração da aplicação e do banco de dados
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    # Alterar login, senha e nome do banco de dados 
    'mysql+pymysql://root:root@localhost:3306/agromail?charset=utf8mb4')
db = SQLAlchemy(app)

# Criação dos modelos para integração com o SQL Alchemy
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    ordens = db.relationship('OrdemServico', back_populates='solicitante')

class Cultivar(db.Model):
    __tablename__ = 'cultivares'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    especie = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=db.func.now())
    ordens = db.relationship('OrdemServico', back_populates='cultivar')

class OrdemServico(db.Model):
    __tablename__ = 'ordens'
    __table_args__ = (
        db.Index('ix_ordens_status', 'status'),
        db.Index('ix_ordens_solicitante', 'solicitante_id'),)
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text)
    quantidade = db.Column(db.Integer)
    status = db.Column(db.String(20), default='aberta')
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    # Relacionamento com as tabelas Cultivar e Solicitante
    solicitante_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cultivar_id = db.Column(db.Integer, db.ForeignKey('cultivares.id'))
    solicitante = db.relationship('User', back_populates='ordens')
    cultivar = db.relationship('Cultivar', back_populates='ordens')

# Rota / (Principal) - Validação do login
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

# Rota que cadastra o cultivar
@app.route('/cultivares', methods=['GET', 'POST'])
def cultivares():
    if request.method == 'POST':
        # Recupera os dados do formulário
        nome = request.form.get('nome', '').strip()
        especie = request.form.get('especie', '').strip()
        # Cria o objeto do tipo Cultivar
        c = Cultivar(nome=nome, especie=especie or None)
        db.session.add(c)
        db.session.commit()
        flash('Cultivar cadastrado com sucesso', 'success')
        return redirect(url_for('cultivares'))
    #Faz a consulta na classe Cultivar
    lista = Cultivar.query.order_by(Cultivar.nome.asc()).all()
    return render_template('cultivares.html', cultivares=lista)

# rota que gera as ordens
@app.route('/ordens', methods=['GET', 'POST'])
def ordens():
    # Garante que o usuário esteja autenticado antes de acessar a página
    if not session.get('user_id'):
        return redirect(url_for('login'))

    # Quando o método for POST, processa o envio do formulário de abertura de ordem
    if request.method == 'POST':
        # Recupera o cultivar escolhido no formulário
        cultivar_id = request.form.get('cultivar_id')
        # Valida se um cultivar foi selecionado
        if not cultivar_id:
            flash('Selecione um cultivar', 'warning')
            return redirect(url_for('ordens'))

        # Busca o cultivar no banco pelo ID informado
        c = Cultivar.query.get(int(cultivar_id))
        if not c:
            flash('Cultivar inválido', 'danger')
            return redirect(url_for('ordens'))

        # Lê a quantidade do formulário e tenta converter para inteiro
        quantidade_raw = request.form.get('quantidade')
        observacoes = request.form.get('observacoes', '').strip() or None
        try:
            quantidade = int(quantidade_raw) if quantidade_raw else None
        except ValueError:
            quantidade = None

        # Define o título usando a concatenação "nome + espécie" quando a espécie existir
        titulo = f"Ordem para {c.nome} - {c.especie}" if c.especie else f"Ordem para {c.nome}"

        # Cria e persiste a ordem relacionando solicitante e cultivar
        ordem = OrdemServico(
            titulo=titulo,
            descricao=observacoes,
            quantidade=quantidade,
            solicitante_id=session['user_id'],
            cultivar_id=c.id,
        )
        db.session.add(ordem)
        db.session.commit()

        # Exibe mensagem de sucesso e redireciona para evitar reenvio do formulário
        flash('Ordem criada com sucesso', 'success')
        return redirect(url_for('ordens'))

    # Em GET, carrega os cultivares para popular o select do formulário
    cultivares = Cultivar.query.order_by(Cultivar.nome.asc()).all()
    # Renderiza a página de abertura de ordens
    ultimas = OrdemServico.query.order_by(OrdemServico.created_at.desc()).limit(10).all()
    return render_template('ordens.html', cultivares=cultivares, ultimas=ultimas)

# Exibe apenas as rotas criadas pelo usuário que está logado
@app.route('/ordens/minhas')
def ordens_minhas():
    if not session.get('user_id'):
        return redirect(url_for('login'))
    minhas = OrdemServico.query.filter_by(solicitante_id=session['user_id']).order_by(OrdemServico.created_at.desc()).all()
    return render_template('ordens_minhas.html', ordens=minhas)

# Exibe as todas as ordens geradas, e classificadas em ordem crescente de id
@app.route('/ordens/todas')
def ordens_todas():
    todas = OrdemServico.query.order_by(OrdemServico.id.asc()).all()
    return render_template('ordens_todas.html', ordens=todas)

# Cadastro do usuário
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

# Faz o logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Arquivo principal
if __name__ == '__main__':
    host = os.getenv('HOST', '127.0.0.1')
    port = int(os.getenv('PORT', '5600'))
    app.run(host=host, port=port, debug=True)