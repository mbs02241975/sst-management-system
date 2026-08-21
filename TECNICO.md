# Documentação Técnica - Sistema de Gestão de SST

## Arquitetura

O sistema segue o padrão MVC (Model-View-Controller):

- **Models:** Definições de banco de dados em `app.py`
- **Views:** Templates HTML em `templates/`
- **Controllers:** Rotas Flask em `app.py`

## Estrutura do Projeto

```
sst-management-system/
├── app.py                 # Aplicação principal
├── config.py              # Configurações
├── requirements.txt       # Dependências
├── templates/             # Templates HTML
│   ├── base.html         # Layout base
│   ├── login.html        # Página de login
│   ├── dashboard.html    # Dashboard
│   ├── treinamentos.html # Gestão de treinamentos
│   ├── asos.html         # Gestão de ASO
│   ├── acidentes.html    # Investigação de acidentes
│   ├── nao_conformidades.html # Não conformidades
│   └── planos_acao.html  # Planos de ação
├── static/               # Arquivos estáticos
│   ├── css/
│   │   ├── style.css     # Estilos principais
│   │   └── login.css     # Estilos de login
│   └── js/
│       └── script.js     # Scripts JavaScript
├── docs/                 # Documentação
│   ├── INSTALACAO.md
│   ├── USO.md
│   └── TECNICO.md
└── README.md             # Documentação principal
```

## Modelos de Dados

### Usuário (User)
```python
- id: Identificador único
- username: Nome de usuário
- password_hash: Senha criptografada
- email: E-mail
- full_name: Nome completo
- role: admin, user, manager
- created_at: Data de criação
- updated_at: Data de atualização
```

### Treinamento
```python
- id: Identificador único
- titulo: Título do treinamento
- descricao: Descrição
- data_realizacao: Data
- responsavel: Responsável
- participantes: Número de pessoas
- duracao_horas: Duração em horas
- local: Local
- carga_horaria_total: Carga horária
- status: planejado, realizado, cancelado
- created_by: Usuário que criou
```

### ASO
```python
- id: Identificador único
- matricula_funcionario: Matrícula
- nome_funcionario: Nome
- data_realizacao: Data do ASO
- data_proxima_revisao: Próxima revisão
- resultado: apto, inapto, apto_com_restricoes
- medico_responsavel: Médico
- crm: CRM
- observacoes: Observações
- tipo_aso: admissional, periodico, demissional, retorno, mudanca_funcao
```

### Acidente
```python
- id: Identificador único
- data_ocorrencia: Data/Hora
- tipo: acidente, incidente, quase_acidente
- local: Local
- descricao: Descrição
- envolvidos: Pessoas envolvidas
- lesoes: Lesões/Danos
- causa_raiz: Causa raiz
- medidas_corretivas: Medidas
- status: aberto, fechado, em_análise
- responsavel_investigacao: Investigador
- data_fechamento: Data de fechamento
```

### Não Conformidade
```python
- id: Identificador único
- numero: Número único (NC-YYYYMMDDHHMMSS)
- titulo: Título
- descricao: Descrição
- data_identificacao: Data
- area: Área/Departamento
- severidade: baixa, media, alta, critica
- status: aberta, em_andamento, fechada
- responsavel: Responsável
- data_limite: Data limite
```

### Plano de Ação
```python
- id: Identificador único
- nao_conformidade_id: Referência a NC
- acao: Ação a realizar
- responsavel: Responsável
- data_limite: Data limite
- data_conclusao: Data de conclusão
- status: planejado, em_andamento, concluido, atrasado
- evidencia: Evidência de conclusão
```

## Rotas da API

### Autenticação
- `GET /` - Redireciona para dashboard ou login
- `GET /login` - Exibe página de login
- `POST /login` - Processa login
- `GET /logout` - Faz logout

### Dashboard
- `GET /dashboard` - Página inicial

### Treinamentos
- `GET /treinamentos` - Lista treinamentos
- `POST /treinamentos` - Cria novo treinamento

### ASO
- `GET /asos` - Lista ASOs
- `POST /asos` - Cria novo ASO

### Acidentes
- `GET /acidentes` - Lista acidentes
- `POST /acidentes` - Registra novo acidente

### Não Conformidades
- `GET /nao-conformidades` - Lista NCs
- `POST /nao-conformidades` - Cria nova NC

### Planos de Ação
- `GET /planos-acao` - Lista planos
- `POST /planos-acao` - Cria novo plano

## Variáveis de Ambiente

```
FLASK_APP=app.py
FLASK_ENV=development  # ou production
SECRET_KEY=sua-chave-secreta
DATABASE_URL=postgresql://user:password@localhost:5432/sst_management
```

## Autenticação e Segurança

- Senhas são armazenadas com hash usando `werkzeug.security`
- Sessões são controladas com `session` do Flask
- CSRF é habilitado por padrão
- Cookies são marcados como HTTP-only

## Expandindo o Sistema

### Adicionar Nova Funcionalidade

1. Defina o modelo em `app.py`
2. Crie as rotas em `app.py`
3. Crie o template HTML em `templates/`
4. Adicione estilos CSS em `static/css/`
5. Adicione funcionalidade JavaScript em `static/js/`

### Exemplo: Adicionar Novo Módulo

```python
# 1. Definir modelo
class NovoModulo(db.Model):
    __tablename__ = 'novo_modulo'
    id = db.Column(db.Integer, primary_key=True)
    # ... campos ...

# 2. Adicionar rota
@app.route('/novo-modulo', methods=['GET', 'POST'])
def novo_modulo():
    if request.method == 'POST':
        # Processar form
        pass
    return render_template('novo_modulo.html')

# 3. Adicionar link no navbar (base.html)
# 4. Criar template novo_modulo.html
```

## Performance

- O sistema usa SQLite por padrão (adequado para pequenas empresas)
- Para grandes volumes, use PostgreSQL
- Índices são criados automaticamente para chaves primárias
- Considere adicionar cache com Redis para produção

## Backup e Manutenção

### Backup do Banco de Dados

```bash
# SQLite
cp sst_management.db sst_management.db.bak

# PostgreSQL
pg_dump sst_management > backup.sql
```

### Restaurar

```bash
# SQLite
cp sst_management.db.bak sst_management.db

# PostgreSQL
psql sst_management < backup.sql
```

## Troubleshooting Técnico

### Verificar Logs

Os logs aparecem no console durante execução em modo desenvolvimento.

### Debug Mode

```python
app.run(debug=True)  # Já está ativo no app.py
```

### Resetar Banco de Dados

```bash
# Delete o arquivo sst_management.db
# Execute o app novamente para criar novo banco
python app.py
```

## Suporte ao Desenvolvedor

**Máximo Batista**  
Telefone: (71)98286-2569  
E-mail: mbs1975@hotmail.com
