# FAQ - Perguntas Frequentes

## Instalação e Configuração

### P: Posso usar Windows?
**R:** Sim! Siga os mesmos passos, apenas note que os comandos podem diferir ligeiramente.

### P: Preciso de PostgreSQL?
**R:** Não é obrigatório. O sistema usa SQLite por padrão, adequado para pequenas empresas. PostgreSQL é recomendado para produção com muitos usuários.

### P: Como alterar a senha do usuário padrão?
**R:** Acesse o banco de dados e execute:
```python
from app import db, User
user = User.query.filter_by(username='Máximo').first()
user.set_password('nova_senha')
db.session.commit()
```

## Uso do Sistema

### P: Como registrar um novo usuário?
**R:** Atualmente, novos usuários devem ser adicionados manualmente. Uma futura versão terá autossistro.

### P: Posso recuperar dados deletados?
**R:** O sistema não tem soft delete. Faça backups regularmente para segurança.

### P: Como exportar dados?
**R:** Use a função de export para CSV ou acesse diretamente o banco de dados.

## Segurança

### P: É seguro armazenar dados no servidor?
**R:** Sim, com as devidas precauções:
- Use HTTPS em produção
- Mantenha backups regulares
- Use senhas fortes
- Restrinja acesso SSH

### P: Qual é a política de privacidade?
**R:** Os dados são armazenados localmente em seu servidor. Você é responsável por sua privacidade e segurança.

### P: O sistema é LGPD compliant?
**R:** Parcialmente. Implemente as políticas de privacidade da sua empresa.

## Performance

### P: Quantos usuários simultâneos o sistema suporta?
**R:** Com SQLite: ~10 usuários. Com PostgreSQL: 100+ usuários com boa infraestrutura.

### P: Como melhorar performance?
**R:** 
- Use PostgreSQL em vez de SQLite
- Adicione mais workers Gunicorn
- Implemente cache Redis
- Otimize queries do banco

## Problemas Comuns

### P: "ModuleNotFoundError: No module named 'flask'"
**R:** Ative o ambiente virtual: `source venv/bin/activate`

### P: "Address already in use"
**R:** A porta 5000 já está em uso. Use: `python app.py --port 8000`

### P: Mudança de dados não aparece
**R:** Limpe o cache do navegador (Ctrl+Shift+Del) e recarregue.

### P: Login não funciona
**R:** 
- Verifique se o banco de dados existe
- Confirme credenciais padrão (Máximo / Mm88918675@@)
- Verifique espaço em disco

## Desenvolvimento

### P: Como adicionar novo campo na tabela?
**R:** 
1. Modifique o modelo em `app.py`
2. Delete `sst_management.db`
3. Reinicie a aplicação

### P: Como alterar cores do sistema?
**R:** Edite as variáveis CSS em `static/css/style.css` (variáveis `:root`)

### P: Posso usar o sistema offline?
**R:** Não, requer conexão com servidor. Uma versão offline pode ser desenvolvida no futuro.

## Suporte e Comunidade

### P: Onde relatar bugs?
**R:** Abra uma issue no GitHub: https://github.com/mbs02241975/sst-management-system/issues

### P: Como sugerir melhorias?
**R:** Abra uma issue com tag "enhancement" ou entre em contato:
- Email: mbs1975@hotmail.com
- Telefone: (71)98286-2569

### P: O sistema é gratuito?
**R:** Sim! É um projeto de código aberto.

### P: Posso usar comercialmente?
**R:** Sim, confira a licença do projeto para detalhes.

## Contato e Suporte

**Desenvolvedor:** Máximo Batista Santos  
**Email:** mbs1975@hotmail.com  
**Telefone:** (71)98286-2569  
**GitHub:** https://github.com/mbs02241975/sst-management-system
