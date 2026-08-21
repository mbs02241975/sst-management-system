from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sst-management-system-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sst_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelos de Banco de Dados
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), default='user')  # admin, user, manager
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Treinamento(db.Model):
    __tablename__ = 'treinamentos'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text)
    data_realizacao = db.Column(db.Date, nullable=False)
    responsavel = db.Column(db.String(120), nullable=False)
    participantes = db.Column(db.Integer, default=0)
    duracao_horas = db.Column(db.Float)
    local = db.Column(db.String(200))
    carga_horaria_total = db.Column(db.Float)
    status = db.Column(db.String(20), default='planejado')  # planejado, realizado, cancelado
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))

class ASO(db.Model):
    __tablename__ = 'asos'
    id = db.Column(db.Integer, primary_key=True)
    matricula_funcionario = db.Column(db.String(50), nullable=False)
    nome_funcionario = db.Column(db.String(200), nullable=False)
    data_realizacao = db.Column(db.Date, nullable=False)
    data_proxima_revisao = db.Column(db.Date)
    resultado = db.Column(db.String(50))  # apto, inapto, apto_com_restricoes
    medico_responsavel = db.Column(db.String(200))
    crm = db.Column(db.String(20))
    observacoes = db.Column(db.Text)
    tipo_aso = db.Column(db.String(50))  # admissional, periodico, demissional, retorno, mudanca_funcao
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))

class Acidente(db.Model):
    __tablename__ = 'acidentes'
    id = db.Column(db.Integer, primary_key=True)
    data_ocorrencia = db.Column(db.DateTime, nullable=False)
    tipo = db.Column(db.String(50))  # acidente, incidente, quase_acidente
    local = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    envolvidos = db.Column(db.String(500))
    lesoes = db.Column(db.Text)
    causa_raiz = db.Column(db.Text)
    medidas_corretivas = db.Column(db.Text)
    status = db.Column(db.String(20), default='aberto')  # aberto, fechado, em_análise
    responsavel_investigacao = db.Column(db.String(120))
    data_fechamento = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))

class NaoConformidade(db.Model):
    __tablename__ = 'nao_conformidades'
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(50), unique=True, nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    data_identificacao = db.Column(db.Date, nullable=False)
    area = db.Column(db.String(100))
    severidade = db.Column(db.String(20))  # baixa, media, alta, critica
    status = db.Column(db.String(20), default='aberta')  # aberta, em_andamento, fechada
    responsavel = db.Column(db.String(120))
    data_limite = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))

class PlanoAcao(db.Model):
    __tablename__ = 'planos_acao'
    id = db.Column(db.Integer, primary_key=True)
    nao_conformidade_id = db.Column(db.Integer, db.ForeignKey('nao_conformidades.id'), nullable=False)
    acao = db.Column(db.Text, nullable=False)
    responsavel = db.Column(db.String(120), nullable=False)
    data_limite = db.Column(db.Date, nullable=False)
    data_conclusao = db.Column(db.Date)
    status = db.Column(db.String(20), default='planejado')  # planejado, em_andamento, concluido, atrasado
    evidencia = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))

# Rotas
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Usuário ou senha inválidos')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    total_treinamentos = Treinamento.query.count()
    total_asos = ASO.query.count()
    total_acidentes = Acidente.query.count()
    total_nao_conformidades = NaoConformidade.query.count()
    
    acidentes_abertos = Acidente.query.filter_by(status='aberto').count()
    nao_conformidades_abertas = NaoConformidade.query.filter_by(status='aberta').count()
    
    return render_template('dashboard.html', 
                         total_treinamentos=total_treinamentos,
                         total_asos=total_asos,
                         total_acidentes=total_acidentes,
                         total_nao_conformidades=total_nao_conformidades,
                         acidentes_abertos=acidentes_abertos,
                         nao_conformidades_abertas=nao_conformidades_abertas)

# Rotas de Treinamentos
@app.route('/treinamentos', methods=['GET', 'POST'])
def treinamentos():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        try:
            novo_treinamento = Treinamento(
                titulo=request.form.get('titulo'),
                descricao=request.form.get('descricao'),
                data_realizacao=datetime.strptime(request.form.get('data_realizacao'), '%Y-%m-%d').date(),
                responsavel=request.form.get('responsavel'),
                participantes=int(request.form.get('participantes', 0)),
                duracao_horas=float(request.form.get('duracao_horas', 0)),
                local=request.form.get('local'),
                carga_horaria_total=float(request.form.get('carga_horaria_total', 0)),
                status=request.form.get('status', 'planejado'),
                created_by=session['user_id']
            )
            db.session.add(novo_treinamento)
            db.session.commit()
            return redirect(url_for('treinamentos'))
        except Exception as e:
            return render_template('treinamentos.html', error=str(e))
    
    treinamentos_list = Treinamento.query.all()
    return render_template('treinamentos.html', treinamentos=treinamentos_list)

# Rotas de ASO
@app.route('/asos', methods=['GET', 'POST'])
def asos():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        try:
            novo_aso = ASO(
                matricula_funcionario=request.form.get('matricula_funcionario'),
                nome_funcionario=request.form.get('nome_funcionario'),
                data_realizacao=datetime.strptime(request.form.get('data_realizacao'), '%Y-%m-%d').date(),
                data_proxima_revisao=datetime.strptime(request.form.get('data_proxima_revisao'), '%Y-%m-%d').date() if request.form.get('data_proxima_revisao') else None,
                resultado=request.form.get('resultado'),
                medico_responsavel=request.form.get('medico_responsavel'),
                crm=request.form.get('crm'),
                observacoes=request.form.get('observacoes'),
                tipo_aso=request.form.get('tipo_aso'),
                created_by=session['user_id']
            )
            db.session.add(novo_aso)
            db.session.commit()
            return redirect(url_for('asos'))
        except Exception as e:
            return render_template('asos.html', error=str(e))
    
    asos_list = ASO.query.all()
    return render_template('asos.html', asos=asos_list)

# Rotas de Acidentes
@app.route('/acidentes', methods=['GET', 'POST'])
def acidentes():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        try:
            novo_acidente = Acidente(
                data_ocorrencia=datetime.strptime(request.form.get('data_ocorrencia'), '%Y-%m-%dT%H:%M'),
                tipo=request.form.get('tipo'),
                local=request.form.get('local'),
                descricao=request.form.get('descricao'),
                envolvidos=request.form.get('envolvidos'),
                lesoes=request.form.get('lesoes'),
                causa_raiz=request.form.get('causa_raiz'),
                medidas_corretivas=request.form.get('medidas_corretivas'),
                status=request.form.get('status', 'aberto'),
                responsavel_investigacao=request.form.get('responsavel_investigacao'),
                created_by=session['user_id']
            )
            db.session.add(novo_acidente)
            db.session.commit()
            return redirect(url_for('acidentes'))
        except Exception as e:
            return render_template('acidentes.html', error=str(e))
    
    acidentes_list = Acidente.query.all()
    return render_template('acidentes.html', acidentes=acidentes_list)

# Rotas de Não Conformidades
@app.route('/nao-conformidades', methods=['GET', 'POST'])
def nao_conformidades():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        try:
            novo_numero = f"NC-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            nova_nc = NaoConformidade(
                numero=novo_numero,
                titulo=request.form.get('titulo'),
                descricao=request.form.get('descricao'),
                data_identificacao=datetime.strptime(request.form.get('data_identificacao'), '%Y-%m-%d').date(),
                area=request.form.get('area'),
                severidade=request.form.get('severidade'),
                status=request.form.get('status', 'aberta'),
                responsavel=request.form.get('responsavel'),
                data_limite=datetime.strptime(request.form.get('data_limite'), '%Y-%m-%d').date() if request.form.get('data_limite') else None,
                created_by=session['user_id']
            )
            db.session.add(nova_nc)
            db.session.commit()
            return redirect(url_for('nao_conformidades'))
        except Exception as e:
            return render_template('nao_conformidades.html', error=str(e))
    
    nao_conformidades_list = NaoConformidade.query.all()
    return render_template('nao_conformidades.html', nao_conformidades=nao_conformidades_list)

# Rotas de Planos de Ação
@app.route('/planos-acao', methods=['GET', 'POST'])
def planos_acao():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        try:
            novo_plano = PlanoAcao(
                nao_conformidade_id=int(request.form.get('nao_conformidade_id')),
                acao=request.form.get('acao'),
                responsavel=request.form.get('responsavel'),
                data_limite=datetime.strptime(request.form.get('data_limite'), '%Y-%m-%d').date(),
                status=request.form.get('status', 'planejado'),
                evidencia=request.form.get('evidencia'),
                created_by=session['user_id']
            )
            db.session.add(novo_plano)
            db.session.commit()
            return redirect(url_for('planos_acao'))
        except Exception as e:
            return render_template('planos_acao.html', error=str(e))
    
    planos_list = PlanoAcao.query.all()
    nao_conformidades_list = NaoConformidade.query.all()
    return render_template('planos_acao.html', planos=planos_list, nao_conformidades=nao_conformidades_list)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Criar usuário padrão
        if not User.query.filter_by(username='Máximo').first():
            admin = User(
                username='Máximo',
                email='mbs1975@hotmail.com',
                full_name='Máximo Batista',
                role='admin'
            )
            admin.set_password('Mm88918675@@')
            db.session.add(admin)
            db.session.commit()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
