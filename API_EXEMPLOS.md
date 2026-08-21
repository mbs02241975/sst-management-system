# Exemplos de API - Sistema de Gestão de SST

## Introdução

Este documento fornece exemplos de como interagir com o Sistema de Gestão de SST através de requisições HTTP.

> **Nota:** A versão atual (1.0) não possui API REST péblica. Os exemplos abaixo demonstram como as requisições são processadas internamente.

## Autenticação

### Login

**Requisition:**
```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=Máximo&password=Mm88918675@@"
```

**Response (Sucesso):**
```
HTTP/1.1 302 Found
Location: /dashboard
Set-Cookie: session=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response (Erro):**
```json
{
  "error": "Usuário ou senha inválidos"
}
```

### Logout

**Requisition:**
```bash
curl -X GET http://localhost:5000/logout \
  -H "Cookie: session=seu_token_aqui"
```

**Response:**
```
HTTP/1.1 302 Found
Location: /login
```

## Treinamentos

### Listar Todos os Treinamentos

**Requisition:**
```bash
curl -X GET http://localhost:5000/treinamentos \
  -H "Cookie: session=seu_token_aqui"
```

**Response (Sucesso):**
```html
<!-- Página HTML com lista de treinamentos -->
```

### Criar Novo Treinamento

**Requisition:**
```bash
curl -X POST http://localhost:5000/treinamentos \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "Cookie: session=seu_token_aqui" \
  -d "titulo=NR-5 CIPA&data_realizacao=2024-08-25&responsavel=João Silva&participantes=15&duracao_horas=4&local=Sala 101&status=planejado"
```

**Response (Sucesso):**
```
HTTP/1.1 302 Found
Location: /treinamentos?success=Treinamento%20registrado%20com%20sucesso
```

**Dados do Formúlário:**
```
titulo*              : string (máximo 255 caracteres)
data_realizacao*     : date (YYYY-MM-DD)
responsavel*         : string (nome)
local                : string (local)
participantes        : integer
duracao_horas        : float
carga_horaria_total  : float
descricao            : text
status               : enum (planejado, realizado, cancelado)
```

### Exemplo em Python

```python
import requests
from datetime import datetime

# URL base
BASE_URL = "http://localhost:5000"

# Dados de login
login_data = {
    "username": "Máximo",
    "password": "Mm88918675@@"
}

# Criar sessão
session = requests.Session()
response = session.post(f"{BASE_URL}/login", data=login_data)

if response.status_code == 302:
    print("Login bem-sucedido!")
    
    # Criar novo treinamento
    treinamento_data = {
        "titulo": "NR-5 CIPA",
        "descricao": "Treinamento sobre Comissão Interna de Prevenção de Acidentes",
        "data_realizacao": "2024-08-25",
        "responsavel": "João Silva",
        "participantes": 15,
        "duracao_horas": 4,
        "local": "Sala de Treinamento",
        "status": "planejado"
    }
    
    response = session.post(f"{BASE_URL}/treinamentos", data=treinamento_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
else:
    print(f"Erro no login: {response.status_code}")
```

## ASO (Atestado de Saúde Ocupacional)

### Listar ASOs

**Requisition:**
```bash
curl -X GET http://localhost:5000/asos \
  -H "Cookie: session=seu_token_aqui"
```

### Registrar Novo ASO

**Requisition:**
```bash
curl -X POST http://localhost:5000/asos \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "Cookie: session=seu_token_aqui" \
  -d "matricula_funcionario=001234&nome_funcionario=Maria Santos&tipo_aso=periodico&data_realizacao=2024-08-20&resultado=apto&medico_responsavel=Dr. Silva&crm=123456"
```

**Dados do Formulário:**
```
matricula_funcionario*    : string (máximo 50)
nome_funcionario*         : string (nome completo)
tipo_aso*                 : enum (admissional, periodico, demissional, retorno, mudanca_funcao)
data_realizacao*          : date (YYYY-MM-DD)
data_proxima_revisao      : date (YYYY-MM-DD)
resultado                 : enum (apto, inapto, apto_com_restricoes)
medico_responsavel        : string (nome)
crm                       : string (número CRM)
observacoes               : text
```

### Exemplo em Python

```python
import requests
from datetime import datetime, timedelta

session = requests.Session()
session.post("http://localhost:5000/login", 
    data={"username": "Máximo", "password": "Mm88918675@@"})

aso_data = {
    "matricula_funcionario": "001234",
    "nome_funcionario": "Maria Santos",
    "tipo_aso": "periodico",
    "data_realizacao": "2024-08-20",
    "resultado": "apto",
    "data_proxima_revisao": "2025-08-20",
    "medico_responsavel": "Dr. João Silva",
    "crm": "123456",
    "observacoes": "Sem restrições encontradas"
}

response = session.post("http://localhost:5000/asos", data=aso_data)
print(f"ASO registrado com sucesso: {response.status_code}")
```

## Acidentes/Incidentes

### Listar Acidentes

**Requisition:**
```bash
curl -X GET http://localhost:5000/acidentes \
  -H "Cookie: session=seu_token_aqui"
```

### Registrar Novo Acidente

**Requisition:**
```bash
curl -X POST http://localhost:5000/acidentes \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "Cookie: session=seu_token_aqui" \
  -d "data_ocorrencia=2024-08-21T10:30&tipo=acidente&local=Sala%20de%20Operação&descricao=Que...&status=aberto"
```

**Dados do Formulário:**
```
data_ocorrencia*              : datetime (YYYY-MM-DD ou YYYY-MM-DDTHH:MM)
tipo*                         : enum (acidente, incidente, quase_acidente)
local*                        : string (local do acidente)
descricao*                    : text (descrição detalhada)
envolvidos                    : text (lista de pessoas)
lesoes                        : text (descrição de lesões)
causa_raiz                    : text (análise de causa)
medidas_corretivas            : text (ações corretivas)
responsavel_investigacao      : string (nome do investigador)
status                        : enum (aberto, em_análise, fechado)
```

### Exemplo em Python

```python
import requests
from datetime import datetime

session = requests.Session()
session.post("http://localhost:5000/login", 
    data={"username": "Máximo", "password": "Mm88918675@@"})

acidente_data = {
    "data_ocorrencia": "2024-08-21T10:30",
    "tipo": "acidente",
    "local": "Sala de Operação",
    "descricao": "Funccionário escorregou e caiu no chão molhado",
    "envolvidos": "Pedro Silva, João Santos",
    "lesoes": "Frat ura no braço esquerdo",
    "causa_raiz": "Piso molhado sem sinalização",
    "medidas_corretivas": "Adicionar tapetes de borracha e sinalizacao",
    "responsavel_investigacao": "Maria Oliveira",
    "status": "aberto"
}

response = session.post("http://localhost:5000/acidentes", data=acidente_data)
print(f"Acidente registrado: {response.status_code}")
```

## Não Conformidades

### Listar Não Conformidades

**Requisition:**
```bash
curl -X GET http://localhost:5000/nao_conformidades \
  -H "Cookie: session=seu_token_aqui"
```

### Criar Não Conformidade

**Requisition:**
```bash
curl -X POST http://localhost:5000/nao_conformidades \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "Cookie: session=seu_token_aqui" \
  -d "titulo=Falta de EPIs&descricao=Alguns...&data_identificacao=2024-08-21&area=Produção&severidade=alta"
```

**Dados do Formulário:**
```
titulo*                   : string (breve descrição)
descricao*                : text (explicação completa)
data_identificacao*       : date (YYYY-MM-DD)
area                      : string (departamento)
severidade*               : enum (baixa, media, alta, critica)
responsavel               : string (nome)
data_limite               : date (prazo para correção)
status                    : enum (aberta, em_andamento, fechada)
```

### Exemplo em Python

```python
import requests

session = requests.Session()
session.post("http://localhost:5000/login", 
    data={"username": "Máximo", "password": "Mm88918675@@"})

nc_data = {
    "titulo": "Falta de EPIs na área de Produção",
    "descricao": "Alguns funccionários não estão usando EPIs corretamente",
    "data_identificacao": "2024-08-21",
    "area": "Produção",
    "severidade": "alta",
    "responsavel": "João Silva",
    "data_limite": "2024-09-10",
    "status": "aberta"
}

response = session.post("http://localhost:5000/nao_conformidades", data=nc_data)
print(f"NC registrada com número: {response.status_code}")
```

## Planos de Ação

### Listar Planos

**Requisition:**
```bash
curl -X GET http://localhost:5000/planos_acao \
  -H "Cookie: session=seu_token_aqui"
```

### Criar Plano de Ação

**Requisition:**
```bash
curl -X POST http://localhost:5000/planos_acao \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "Cookie: session=seu_token_aqui" \
  -d "nao_conformidade_id=1&acao=Adquirir...&responsavel=Maria&data_limite=2024-09-10&status=planejado"
```

**Dados do Formulário:**
```
nao_conformidade_id*   : integer (ID da NC)
acao*                  : text (o que será feito)
responsavel*           : string (quem executa)
data_limite*           : date (prazo)
evidencia              : text (como comprovar)
status                 : enum (planejado, em_andamento, concluido, atrasado)
```

### Exemplo em Python

```python
import requests

session = requests.Session()
session.post("http://localhost:5000/login", 
    data={"username": "Máximo", "password": "Mm88918675@@"})

plano_data = {
    "nao_conformidade_id": 1,
    "acao": "Adquirir e distribuir EPIs corretos para toda a área",
    "responsavel": "Maria Oliveira",
    "data_limite": "2024-09-10",
    "evidencia": "Nota fiscal de compra e fotos dos funccionários usando EPIs",
    "status": "planejado"
}

response = session.post("http://localhost:5000/planos_acao", data=plano_data)
print(f"Plano de Ação criado: {response.status_code}")
```

## Códigos de Status HTTP

```
200 OK              - Requisição bem-sucedida
201 Created         - Recurso criado
302 Found           - Redirecionamento (login, criar item)
400 Bad Request     - Dados inválidos
401 Unauthorized    - Sem autenticação
403 Forbidden       - Sem permissão
404 Not Found       - Recurso não encontrado
500 Server Error    - Erro no servidor
```

## Exemplo Completo: Workflow de Não Conformidade

```python
import requests
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5000"
session = requests.Session()

# 1. Login
print("1. Fazendo login...")
login_resp = session.post(f"{BASE_URL}/login", 
    data={"username": "Máximo", "password": "Mm88918675@@"})
print(f"   Status: {login_resp.status_code}")

# 2. Criar Não Conformidade
print("\n2. Registrando Não Conformidade...")
nc_data = {
    "titulo": "EPIs Inadequados",
    "descricao": "Alguns operadores usando EPIs vencidos",
    "data_identificacao": datetime.now().strftime("%Y-%m-%d"),
    "area": "Operação",
    "severidade": "alta",
    "responsavel": "Supervisor",
    "data_limite": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
    "status": "aberta"
}
nc_resp = session.post(f"{BASE_URL}/nao_conformidades", data=nc_data)
print(f"   Status: {nc_resp.status_code}")
print(f"   NC criada com sucesso!")

# 3. Criar Plano de Ação
print("\n3. Criando Plano de Ação...")
plano_data = {
    "nao_conformidade_id": 1,  # ID da NC criada
    "acao": "Substituir EPIs vencidos por novos",
    "responsavel": "Maria Silva",
    "data_limite": (datetime.now() + timedelta(days=15)).strftime("%Y-%m-%d"),
    "evidencia": "Nota fiscal e relatório fotográfico",
    "status": "em_andamento"
}
plano_resp = session.post(f"{BASE_URL}/planos_acao", data=plano_data)
print(f"   Status: {plano_resp.status_code}")
print(f"   Plano criado com sucesso!")

print("\n4. Workflow completo executado com sucesso!")
```

## Dicas de Desenvolvimento

### Usando Postman

1. Importe a URL base: `http://localhost:5000`
2. Configure autenticação:
   - Tipo: Form Data
   - username: Máximo
   - password: Mm88918675@@
3. Salve a sessão no cookie
4. Faça requisições para cada endpoint

### Usando cURL

```bash
# Criar arquivo de cookies
curl -c cookies.txt -X POST http://localhost:5000/login \
  -d "username=Máximo&password=Mm88918675@@"

# Usar cookies nas próximas requisições
curl -b cookies.txt http://localhost:5000/dashboard
```

### Usando Python + Requests

Veja exemplos completos na seção acima.

## API REST Futura (Versão 2.0+)

Na versão 2.0+, será implementada uma API REST completa com:

- Endpoints JSON
- Autenticação por token JWT
- Swagger/OpenAPI documentation
- Rate limiting
- Versionamento de API

---

**Para mais informações:** mbs1975@hotmail.com | (71)98286-2569
