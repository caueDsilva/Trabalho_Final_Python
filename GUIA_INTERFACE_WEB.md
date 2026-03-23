# 🚀 Guia de Início - Interface Web

Você agora tem uma interface web simples integrada ao seu backend!

## 📋 Pré-requisitos

- Python 3.9+
- Django 4.2+
- PostgreSQL (ou você pode usar SQLite para testes)

## 🔧 Passos para Executar

### 1. Instale as dependências

```bash
pip install -r requirements.txt
```

### 2. Configure o banco de dados (se ainda não fez)

Se está usando PostgreSQL, crie um arquivo `.env` na raiz do projeto:

```
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
DB_NAME=timetracker_db
DB_USER=postgres
DB_PASSWORD=sua-senha
DB_HOST=localhost
DB_PORT=5432
```

Ou use SQLite (mais simples para testes):

```python
# Em timetracker/settings.py, altere DATABASES para:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### 3. Execute as migrações

```bash
python manage.py migrate
```

### 4. Crie um usuário admin (opcional)

```bash
python manage.py create_admin
```

Ou use o Django admin:

```bash
python manage.py createsuperuser
```

### 5. Inicie o servidor

```bash
python manage.py runserver
```

### 6. Acesse a interface web

Abra seu navegador e vá para:

```
http://localhost:8000
```

## 📱 Como Usar a Interface

### Login

- Use o ID do funcionário e senha
- Exemplo: `EMP001` com sua senha

### Para Funcionários

- **Registrar Entrada**: Clique no botão "Registrar Entrada"
- **Registrar Saída**: Clique no botão "Registrar Saída" (habilitado após entrada)
- **Ver Histórico**: Veja seus últimos registros na página

### Para Admins

- **Buscar Registros**: Procure por funcionário ou data
- **Ver Todos**: Veja todos os registros de todos os funcionários

## 📁 Estrutura de Arquivos

```
TRABALHO FINAL PY/
├── static/              # Arquivos estáticos (CSS, JS, imagens)
│   └── index.html       # Interface web (versão estática)
├── templates/           # Templates Django
│   └── index.html       # Interface web servida pelo Django
├── api/                 # App principal da API
├── timetracker/         # Configurações do Django
├── manage.py            # Gerenciador Django
└── requirements.txt     # Dependências Python
```

## 🔌 Endpoints da API Disponíveis

### Autenticação

- `POST /api/token/` - Login (retorna JWT token)
- `POST /api/token/refresh/` - Renovar token

### Funcionário

- `POST /api/clock-in/` - Registrar entrada
- `POST /api/clock-out/` - Registrar saída
- `GET /api/dashboard/` - Status do dia
- `GET /api/records/` - Todos os registros do funcionário

### Admin

- `GET /api/admin/records/` - Todos os registros (com filtros)
- `GET /api/admin/dashboard/` - Dashboard com resumo
- `GET /api/admin/users/` - Listar todos os usuários
- `POST /api/admin/users/create/` - Criar novo usuário

## ✨ Funcionalidades

✅ Login com autenticação JWT
✅ Clock in/out com timestamps
✅ Dashboard do funcionário
✅ Painel administrativo
✅ Busca por funcionário e data
✅ Histórico de registros
✅ Interface responsiva

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'rest_framework'"

```bash
pip install -r requirements.txt
```

### "CORS error" ou requisições bloqueadas

- Verifique se `corsheaders` está em `INSTALLED_APPS` no settings.py
- Certifique-se de que o middleware CORS está configurado

### Porta 8000 já está em uso

```bash
python manage.py runserver 8001
```

Depois acesse `http://localhost:8001`

### Erro de conexão ao banco de dados

- Verifique se PostgreSQL está rodando (se usando)
- Confirme as credenciais no .env
- Ou use SQLite para testes

## 📝 Notas

- A interface é salva em sessionStorage do navegador (perdida ao fechar a aba)
- Os dados são sincronizados em tempo real com a API
- Use HTTPS em produção
- Adicione HTTPS_ONLY e outras configurações de segurança em produção

## 📞 Suporte

Se encontrar problemas:

1. Verifique o console do navegador (F12)
2. Verifique os logs do Django
3. Certifique-se que a API está respondendo em `/api/token/`

Aproveite! 🎉
