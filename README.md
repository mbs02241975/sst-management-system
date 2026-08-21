# Sistema de Gestão de SST (Saúde e Segurança do Trabalho)

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Stars](https://img.shields.io/github/stars/mbs02241975/sst-management-system.svg)](https://github.com/mbs02241975/sst-management-system/stargazers)

## 🌟 Visão Geral

Um sistema web completo e intuitivo para gerenciar todos os aspectos de **Saúde e Segurança do Trabalho** em sua empresa. Desenvolvido em **Python/Flask**, o sistema oferece uma interface moderna e responsiva para facilitar o gerenciamento de treinamentos, ASOs, acidentes, não conformidades e planos de ação.

### 🏢 Ideal Para
- Pequenas e médias empresas
- Consultores de SST
- Departamentos de RH e Segurança
- Auditores e inspetores
- Organizadores de compliance

## ✨ Funcionalidades Principais

### 1. 🎆 Dashboard Executivo
- Visão geral de todos os módulos
- Métricas em tempo real
- Alertas de itens em aberto
- Interface intuitiva

### 2. 🎓 Gestão de Treinamentos
- Cadastro de treinamentos de SST
- Rastreamento de participantes
- Carga horária e duração
- Status: Planejado, Realizado, Cancelado
- Relatórios de treinamentos

### 3. 📊 ASO (Atestado de Saúde Ocupacional)
- Registro de ASOs por funcionário
- Tipos: Admissional, Periódico, Demissional, Retorno, Mudança de Função
- Resultados: Apto, Inapto, Apto com Restrições
- Controle de prazos de revisão
- Dados do médico responsável

### 4. 🚨 Investigação de Acidentes/Incidentes
- Registro detalhado de ocorrências
- Classificação: Acidente, Incidente, Quase Acidente
- Análise de causa raiz
- Plano de ações corretivas
- Rastreamento de investigação
- Status: Aberto, Em Análise, Fechado

### 5. ✅ Cadastro de Não Conformidades
- Registro de desvios encontrados
- Severidade: Baixa, Média, Alta, Crítica
- Atribuição de responsáveis
- Controle de prazos
- Status: Aberta, Em Andamento, Fechada
- Número único para rastreamento

### 6. 📈 Planos de Ação
- Criação de planos corretivos
- Associação com Não Conformidades
- Atribuição de responsáveis
- Monitoramento de prazos
- Documentação de evidências
- Status: Planejado, Em Andamento, Concluído, Atrasado

### 7. 🔐 Autenticação e Segurança
- Login seguro com hash de senhas
- Controle de sessões
- Papéis de usuário (admin, user, manager)
- Criptografia de dados sensíveis

## 🚀 Início Rápido

### Pré-requisitos
- Python 3.8+
- pip (gerenciador de pacotes)
- Git (opcional)

### Instalação em 5 Minutos

```bash
# 1. Clonar repositório
git clone https://github.com/mbs02241975/sst-management-system.git
cd sst-management-system

# 2. Criar ambiente virtual
python -m venv venv

# 3. Ativar ambiente virtual
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 4. Instalar dependências
pip install -r requirements.txt

# 5. Executar aplicação
python app.py
```

**Acesso:** http://localhost:5000

### Credenciais Padrão
```
Usuário: Máximo
Senha: Mm88918675@@
```

> ⚠️ **IMPORTANTE:** Altere a senha padrão imediatamente em produção!

## 📄 Documentação

Documentação completa disponível:

- **[INSTALACAO.md](./INSTALACAO.md)** - Guia passo a passo de instalação
- **[USO.md](./USO.md)** - Guia de uso do sistema
- **[TECNICO.md](./TECNICO.md)** - Documentação técnica
- **[DEPLOYMENT.md](./DEPLOYMENT.md)** - Guia de deploy em produção
- **[FAQ.md](./FAQ.md)** - Perguntas frequentes
- **[CONTRIBUTING.md](./CONTRIBUTING.md)** - Como contribuir
- **[ROADMAP.md](./ROADMAP.md)** - Plano futuro de desenvolvimento

## 🚄 Stack Tecnológico

```
┌─────────────────────┐
│      Frontend (Client)      │
│  HTML5, CSS3, JavaScript   │
│    Bootstrap (Responsive)   │
├─────────────────────┘
           │
           ↓
┌─────────────────────┐
│   Backend (Server) - Flask  │
│     Python 3.8+ / Gunicorn   │
├─────────────────────┘
           │
           ↓
┌─────────────────────┐
│    Database (Persistence)    │
│  SQLite (Dev) / PostgreSQL   │
│        (Production)           │
└─────────────────────┘
```

### Dependências Principais

| Biblioteca | Versão | Propósito |
|-----------|--------|----------|
| Flask | 2.0+ | Web Framework |
| Flask-SQLAlchemy | 2.5+ | ORM |
| Werkzeug | 2.0+ | Utilidades Python |
| SQLAlchemy | 1.4+ | Database ORM |
| python-dotenv | 0.19+ | Gerenciamento de variáveis |

## 📊 Estrutura de Banco de Dados

### Tabelas Principais

```sql
-- Usuários
users (id, username, password_hash, email, full_name, role, created_at, updated_at)

-- Treinamentos
treinamentos (id, titulo, descricao, data_realizacao, responsavel, participantes, ...)

-- ASO
asos (id, matricula_funcionario, nome_funcionario, data_realizacao, resultado, ...)

-- Acidentes
acidentes (id, data_ocorrencia, tipo, local, descricao, causa_raiz, ...)

-- Não Conformidades
nao_conformidades (id, numero, titulo, severidade, status, responsavel, ...)

-- Planos de Ação
planos_acao (id, nao_conformidade_id, acao, responsavel, data_limite, status, ...)
```

## 📆 Casos de Uso

### Exemplo 1: Registrar e Investigar um Acidente

1. Acidente ocorre na empresa
2. Responsável acessa o sistema
3. Clica em "Acidentes" → "Novo Registro"
4. Preenche dados do acidente
5. Sistema cria registro com status "Aberto"
6. Investigador realiza análise
7. Atualiza causa raiz e medidas corretivas
8. Muda status para "Fechado"
9. Relatório fica documentado para auditorias

### Exemplo 2: Gerenciar Não Conformidade

1. Auditor encontra não conformidade
2. Registra em "Não Conformidades"
3. Define severidade e data limite
4. Sistema atribui número único (ex: NC-20240821100530)
5. Gerente cria plano de ação associado
6. Responsável executa ação
7. Documenta evidências
8. Fecha quando concluído

## 📊 Relatórios Disponíveis

- Treinamentos realizados por período
- ASOs vencidos e próximos de vencer
- Histórico de acidentes/incidentes
- Não conformidades abertas por severidade
- Planos de ação em atraso
- Compliância por área

## 🔓 Segurança

- ✅ Senhas armazenadas com hash (bcrypt)
- ✅ Sessões seguras com token
- ✅ Validação de entrada (XSS protection)
- ✅ CSRF token em formulários
- ✅ HTTPS recomendado em produção
- ✅ Audit trail de alterações

## 🚀 Deploy

Opções de deployment:

1. **Local/Desktop** - Para teste
2. **VPS/Servidor** - Recomendado para produção
3. **AWS EC2** - Escalabilidade na nuvem
4. **Heroku** - Deploy simplificado
5. **Docker** - Containerizado

Veja [DEPLOYMENT.md](./DEPLOYMENT.md) para instruções detalhadas.

## 📁 Configuração de Produção

### Requisitos Mínimos

```
Processor: 2 cores
Memory: 2 GB RAM
Storage: 20 GB SSD
Bandwidth: 1 Mbps
Database: PostgreSQL 12+
Web Server: Nginx
Python: 3.8+
```

### Checklist de Deploy

- [ ] Alterar SECRET_KEY em config.py
- [ ] Usar PostgreSQL em produção
- [ ] Configurar HTTPS/SSL
- [ ] Habilitar CSRF protection
- [ ] Configurar backup automático
- [ ] Monitorar logs
- [ ] Alterar senha padrão
- [ ] Configurar firewall
- [ ] Implementar rate limiting
- [ ] Ativar logging de auditoria

## 📊 Exemplos de Uso

### Criar Novo Treinamento

```bash
curl -X POST http://localhost:5000/treinamentos \
  -F "titulo=NR-5 CIPA" \
  -F "data_realizacao=2024-08-25" \
  -F "responsavel=João Silva"
```

### Registrar ASO

```bash
curl -X POST http://localhost:5000/asos \
  -F "matricula_funcionario=001234" \
  -F "nome_funcionario=Maria Santos" \
  -F "tipo_aso=periodico" \
  -F "resultado=apto"
```

## 🤝 Contribuindo

Contribuições são bem-vindas! Veja [CONTRIBUTING.md](./CONTRIBUTING.md) para detalhes.

### Tópicos para Contribuir

- [ ] Melhorar interface
- [ ] Adicionar novos relatórios
- [ ] Implementar API REST
- [ ] Traduzir para outro idioma
- [ ] Otimizar performance
- [ ] Criar testes unitários

## 🙋 Suporte

### Chat/Email

**Desenvolvedor Principal:** Máximo Batista Santos

- 📧 Email: [mbs1975@hotmail.com](mailto:mbs1975@hotmail.com)
- 📞 Telefone: [(71) 98286-2569](tel:+557198286-2569)
- 🐙 GitHub: [@mbs02241975](https://github.com/mbs02241975)

### Documentação

- [FAQ](./FAQ.md) - Perguntas frequentes
- [INSTALACAO.md](./INSTALACAO.md) - Instalação
- [USO.md](./USO.md) - Guia de uso
- [TECNICO.md](./TECNICO.md) - Documentação técnica

## 📊 Estatísticas do Projeto

```
└─ Python Code
   ├─ Backend: ~1,200 linhas
   ├─ Templates: ~800 linhas
   ├─ CSS: ~700 linhas
   ├─ JavaScript: ~400 linhas
   └─ Total: ~3,100 linhas

Funções: 25+
Rotas: 14
Modelos: 6
Templates: 8
Arquivos Estáticos: 2 CSS + 1 JS
```

## 📈 Roadmap

### Versão 2.0 (Próxima)
- [ ] Relatórios com gráficos Matplotlib/Plotly
- [ ] Export para PDF
- [ ] Notificações por e-mail
- [ ] Gestão avançada de usuários
- [ ] Dashboard com gráficos em tempo real

### Versão 3.0 (Futuro)
- [ ] App mobile (React Native)
- [ ] API REST pública
- [ ] Integração com sistemas ERP
- [ ] Machine Learning para previsões
- [ ] Suporte multi-empresa

Ver [ROADMAP.md](./ROADMAP.md) para mais detalhes.

## 📚 Licença

Este projeto está licenciado sob a **Licença MIT** - veja o arquivo [LICENSE](./LICENSE) para detalhes.

### Resumo da Licença MIT

Você pode:
- ✅ Usar comercialmente
- ✅ Modificar
- ✅ Distribuir
- ✅ Usar privadamente

Você deve:
- ℹ️ Incluir aviso de licença
- ℹ️ Incluir cópia da licença

Você NÃO pode:
- ❌ Responsabilizar o autor
- ❌ Usar marca registrada

## 🌟 Agradecimentos

Agradecimentos especiais a:

- [Palllets Projects](https://palletsprojects.com/) - Framework Flask
- [SQLAlchemy](https://www.sqlalchemy.org/) - ORM Python
- [Font Awesome](https://fontawesome.com/) - Ícones
- Comunidade open-source

## 📋 Changelog

### Versão 1.0.0 - 21/08/2024

**Funcionalidades Iniciais:**
- ✅ Gestão completa de Treinamentos
- ✅ Registro de ASO
- ✅ Investigação de Acidentes
- ✅ Cadastro de Não Conformidades
- ✅ Planos de Ação
- ✅ Sistema de Autenticação
- ✅ Interface responsiva
- ✅ Documentação completa

## 👍 Quer Apoiar o Projeto?

Se este projeto ajudou você:

1. ⭐ Dê uma estrela no GitHub
2. 🐛 Reporte bugs encontrados
3. 🛠️ Sugira melhorias
4. 🐩 Contribua com código
5. 📢 Compartilhe com outros

---

<div align="center">

**Desenvolvido com ❤️ por [Máximo Batista](https://github.com/mbs02241975)**

*Sistema de Gestão de SST - Versão 1.0.0*

[Email](mailto:mbs1975@hotmail.com) • [GitHub](https://github.com/mbs02241975) • [Telefone](tel:+557198286-2569)

</div>
