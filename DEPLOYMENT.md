# Guia de Deployment - Sistema de Gestão de SST

## Deploy na AWS (EC2)

### Pré-requisitos
- Instância EC2 com Ubuntu 20.04 LTS
- SSH acesso à instância
- Domínio configurado (opcional)

### Passos de Instalação

1. **Conectar à instância**
```bash
ssh -i sua-chave.pem ubuntu@seu-ip-ec2.compute.amazonaws.com
```

2. **Atualizar sistema**
```bash
sudo apt update
sudo apt upgrade -y
```

3. **Instalar dependências**
```bash
sudo apt install -y python3 python3-pip python3-venv postgresql postgresql-contrib nginx
```

4. **Clonar repositório**
```bash
cd /var/www
sudo git clone https://github.com/mbs02241975/sst-management-system.git
cd sst-management-system
```

5. **Criar ambiente virtual**
```bash
sudo python3 -m venv venv
source venv/bin/activate
```

6. **Instalar dependências Python**
```bash
sudo pip install -r requirements.txt
sudo pip install gunicorn
```

7. **Configurar PostgreSQL**
```bash
sudo -u postgres psql
CREATE DATABASE sst_management;
CREATE USER sst_user WITH PASSWORD 'sua_senha_segura';
ALTER ROLE sst_user SET client_encoding TO 'utf8';
ALTER ROLE sst_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE sst_user SET default_transaction_deferrable TO on;
GRANT ALL PRIVILEGES ON DATABASE sst_management TO sst_user;
\q
```

8. **Configurar .env**
```bash
sudo cp .env.example .env
sudo nano .env
# Edite conforme necessário
```

9. **Criar serviço Systemd**
```bash
sudo nano /etc/systemd/system/sst-management.service
```

Adicione o seguinte conteúdo:
```ini
[Unit]
Description=SST Management System
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/sst-management-system
Environment="PATH=/var/www/sst-management-system/venv/bin"
ExecStart=/var/www/sst-management-system/venv/bin/gunicorn --workers 4 --bind 127.0.0.1:8000 app:app

[Install]
WantedBy=multi-user.target
```

10. **Ativar serviço**
```bash
sudo systemctl daemon-reload
sudo systemctl enable sst-management
sudo systemctl start sst-management
```

11. **Configurar Nginx**
```bash
sudo nano /etc/nginx/sites-available/sst-management
```

Adicione:
```nginx
server {
    listen 80;
    server_name seu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

12. **Ativar site Nginx**
```bash
sudo ln -s /etc/nginx/sites-available/sst-management /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

13. **SSL com Let's Encrypt (Recomendado)**
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d seu-dominio.com
```

## Deploy no Heroku

### Pré-requisitos
- Conta Heroku
- Heroku CLI instalada
- Git configurado

### Passos

1. **Login no Heroku**
```bash
heroku login
```

2. **Criar aplicação**
```bash
heroku create sst-management-system
```

3. **Adicionar PostgreSQL**
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

4. **Criar Procfile**
```bash
echo "web: gunicorn app:app" > Procfile
```

5. **Definir variáveis de ambiente**
```bash
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=sua-chave-secreta
```

6. **Deploy**
```bash
git push heroku main
```

7. **Inicializar banco**
```bash
heroku run python -c "from app import db; db.create_all()"
```

## Deploy no Docker

### Criar Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

### Criar docker-compose.yml
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://sst_user:password@db:5432/sst_management
    depends_on:
      - db
  
  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=sst_management
      - POSTGRES_USER=sst_user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Build e run
```bash
docker-compose up -d
```

## Monitoramento

### Verificar status do serviço
```bash
sudo systemctl status sst-management
```

### Ver logs
```bash
sudo journalctl -u sst-management -f
```

### Verificar espaço em disco
```bash
df -h
```

## Backup Automático

### Script de backup (backup.sh)
```bash
#!/bin/bash

BACKUP_DIR="/var/backups/sst-management"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup PostgreSQL
sudo -u postgres pg_dump sst_management > $BACKUP_DIR/sst_$DATE.sql

# Comprimir
gzip $BACKUP_DIR/sst_$DATE.sql

# Manter apenas últimas 7 backups
find $BACKUP_DIR -name "sst_*.sql.gz" -mtime +7 -delete

echo "Backup concluído: $BACKUP_DIR/sst_$DATE.sql.gz"
```

### Agendar com Cron
```bash
0 2 * * * /var/www/sst-management-system/backup.sh
```

## Troubleshooting

### Erro 502 Bad Gateway
- Verifique se Gunicorn está rodando: `sudo systemctl status sst-management`
- Reinicie: `sudo systemctl restart sst-management`
- Verifique logs: `sudo journalctl -u sst-management -n 50`

### Erro de conexão com banco de dados
- Verifique se PostgreSQL está rodando: `sudo systemctl status postgresql`
- Verifique credenciais em .env
- Teste conexão: `psql -U sst_user -d sst_management`

### Aplicação lenta
- Adicione mais workers Gunicorn
- Ative cache Redis
- Otimize queries do banco de dados

---

**Suporte:** mbs1975@hotmail.com | (71)98286-2569
