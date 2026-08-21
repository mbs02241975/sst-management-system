# Guia de Instalação - Sistema de Gestão de SST

## Pré-requisitos

Antes de instalar o sistema, certifique-se de que você possui:

- **Python 3.8+** instalado
- **pip** (gerenciador de pacotes Python)
- **Git** (opcional, para clonar o repositório)
- **PostgreSQL** (opcional, para usar banco de dados em produção)

## Instalação Passo a Passo

### 1. Clonar ou Baixar o Repositório

```bash
# Usando Git
git clone https://github.com/mbs02241975/sst-management-system.git
cd sst-management-system

# Ou baixe o ZIP diretamente do GitHub
```

### 2. Criar um Ambiente Virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente

```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o arquivo .env conforme necessário
# Se usar SQLite (padrão), nenhuma configuração adicional é necessária
```

### 5. Inicializar o Banco de Dados

```bash
# O banco de dados será criado automaticamente quando você executar a aplicação
# O usuário padrão será criado também
```

### 6. Executar a Aplicação

```bash
python app.py
```

A aplicação estará acessível em: **http://localhost:5000**

## Credenciais Padrão

**Usuário:** Máximo  
**Senha:** Mm88918675@@

## Configuração para Produção

### Usando PostgreSQL

1. Instale o PostgreSQL e crie um banco de dados:

```sql
CREATE DATABASE sst_management;
CREATE USER sst_user WITH PASSWORD 'sua_senha';
ALTER ROLE sst_user SET client_encoding TO 'utf8';
ALTER ROLE sst_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE sst_user SET default_transaction_deferrable TO on;
GRANT ALL PRIVILEGES ON DATABASE sst_management TO sst_user;
```

2. Atualize o arquivo `.env`:

```
DATABASE_URL=postgresql://sst_user:sua_senha@localhost:5432/sst_management
FLASK_ENV=production
```

3. Instale o driver PostgreSQL:

```bash
pip install psycopg2-binary
```

### Usando Gunicorn (Recomendado para Produção)

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Usando um Servidor Web (Nginx)

Veja o arquivo `DEPLOYMENT.md` para instruções detalhadas.

## Troubleshooting

### Erro: "Module not found"

```bash
# Certifique-se de que o ambiente virtual está ativado
# Reinstale as dependências
pip install -r requirements.txt --force-reinstall
```

### Erro: "Port 5000 already in use"

```bash
# Use uma porta diferente
python app.py --port 8000
```

### Erro: "Database connection failed"

- Verifique se o PostgreSQL está rodando
- Verifique as credenciais no arquivo `.env`
- Para SQLite, certifique-se de que a pasta tem permissão de escrita

## Suporte

**Desenvolvedor:** Máximo Batista  
**Telefone:** (71)98286-2569  
**E-mail:** mbs1975@hotmail.com
