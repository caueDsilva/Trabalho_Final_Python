# 🕐 Time Tracker - Sistema de Rastreamento de Tempo

Uma aplicação web completa em Django para rastreamento de tempo de funcionários. Permite que funcionários batam ponto (clock in/out) e administradores gerenciem registros e usuários.

**Backend**: API REST robusta | **Frontend**: Interface web responsiva

---

## ✨ Funcionalidades

### Para Funcionários

- ✅ **Bater ponto**: Clock in e clock out diários com timestamp
- ✅ **Dashboard**: Ver status do dia (entrada, saída, horas trabalhadas)
- ✅ **Histórico**: Visualizar últimos registros pessoais
- ✅ **Observações**: Adicionar notas aos registros
- ✅ **Interface Web**: Acesso 100% via navegador

### Para Administradores

- ✅ **Dashboard Admin**: Visão geral de todos os funcionários
- ✅ **Busca Avançada**: Procurar por funcionário ou data
- ✅ **Gerenciamento de usuários**: Criar funcionários e admins
- ✅ **Relatórios**: Visualizar todos os registros de tempo
- ✅ **Painel centralizado**: Gerenciar tudo via web

## 🛠 Tecnologias

- **Backend**: Django 4.2+ com Django REST Framework
- **Frontend**: HTML5 + CSS3 + JavaScript Vanilla (sem dependências externas)
- **Autenticação**: JWT (JSON Web Tokens) 🔐
- **Banco de dados**: PostgreSQL ou SQLite
- **CORS**: django-cors-headers para integração frontend/backend

## 📋 Pré-requisitos

- **Python 3.8+**
- **PostgreSQL** (opcional - pode usar SQLite para testes)
- **Git** (opcional)

---

## 🚀 Instalação Rápida (3 passos)

### Passo 1️⃣: Instale as dependências

```bash
pip install -r requirements.txt
```

### Passo 2️⃣: Execute as migrações

```bash
python manage.py migrate
```

### Passo 3️⃣: Inicie o servidor

```bash
python manage.py runserver
```

✅ **Pronto!** Acesse: **http://localhost:8000**

---

## 📖 Instalação Detalhada

### 1. Clone o repositório

```bash
git clone https://github.com/caueDsilva/Trabalho_Final_Python.git
cd Trabalho_Final_Python
```

### 2. Crie um ambiente virtual (recomendado)

```bash
# No Windows:
python -m venv venv
venv\Scripts\activate

# No Linux/Mac:
python -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados

#### ⚡ Opção A: SQLite (Recomendado para Testes)

Não precisa fazer nada! Django já vem configurado com SQLite por padrão.

#### 🗄 Opção B: PostgreSQL (Para Produção)

1. Instale PostgreSQL em seu sistema
2. Crie um banco de dados:

```sql
CREATE DATABASE timetracker_db;
```

3. Crie um arquivo `.env` na raiz:

```env
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
DB_NAME=timetracker_db
DB_USER=seu_usuario_postgres
DB_PASSWORD=sua_senha_postgres
DB_HOST=localhost
DB_PORT=5432
```

### 5. Execute as migrações

```bash
python manage.py migrate
```

### 6. Crie um usuário administrador

```bash
python manage.py create_admin
```

Siga as instruções interativas.

### 7. Inicie o servidor

```bash
python manage.py runserver
```

**🎉 Acesso imediato:**

- **Interface Web**: http://localhost:8000
- **API**: http://localhost:8000/api/
- **Admin Django**: http://localhost:8000/admin/

---

## 🌐 Como Usar a Interface Web

### ✔️ Login

1. Acesse http://localhost:8000
2. Digite seu **ID do Funcionário** (ex: `EMP001`)
3. Digite sua **Senha**
4. Clique em **"Entrar"**

### 👥 Para Funcionários

Após login, você verá:

- **Status do Dia**: Data, entrada, saída, horas trabalhadas
- **Registrar Entrada**: Clique quando chegar
- **Registrar Saída**: Clique quando sair
- **Últimos Registros**: Veja seus últimos 5 registros

```
📱 Interface responsiva: PC, tablet e celular
💾 Dados salvos: tudo sincronizado com a API
🔄 Atualização automática: dados em tempo real
```

### 🔐 Para Administradores

Após login como admin:

- **Buscar por Funcionário**: Digite o nome para filtrar
- **Buscar por Data**: Selecione a data desejada
- **Histórico Completo**: Veja registros de todos
- **Filtros Combinados**: Use nome+data simultaneamente

```
👥 Visualize todos os funcionários
📅 Filtro por datas específicas
👤 Busca por nome
📊 Dados completos e consolidados
```

---

## 🔌 API REST (Para Desenvolvedores)

### Autenticação

- `POST /api/token/` - Login com employee_id e senha
- `POST /api/token/refresh/` - Renovar token JWT

### Para Funcionários

- `POST /api/clock-in/` - Registrar entrada
- `POST /api/clock-out/` - Registrar saída
- `GET /api/dashboard/` - Status do dia
- `GET /api/records/` - Histórico de registros
- `PATCH /api/records/<id>/observation/` - Atualizar observação

### Para Administradores

- `GET /api/admin/dashboard/` - Dashboard com resumo
- `GET /api/admin/records/` - Todos os registros (com filtros)
- `GET /api/admin/users/` - Listar usuários
- `POST /api/admin/users/create/` - Criar novo usuário
- `GET /api/admin/employees/<id>/` - Detalhes de funcionário
- `GET /api/admin/employees/<id>/records/` - Registros de um funcionário

---

## 💻 Exemplos de Uso (cURL)

### 1. Login

```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"employee_id": "EMP001", "password": "senha123"}'
```

**Resposta:**

```json
{
  "refresh": "eyJ...",
  "access": "eyJ...",
  "employee_id": "EMP001",
  "role": "employee",
  "full_name": "João Silva",
  "user_id": 1
}
```

### 2. Registrar Entrada

```bash
curl -X POST http://127.0.0.1:8000/api/clock-in/ \
  -H "Authorization: Bearer {seu_access_token}" \
  -H "Content-Type: application/json" \
  -d '{"observation": "Chegada normal"}'
```

### 3. Registrar Saída

```bash
curl -X POST http://127.0.0.1:8000/api/clock-out/ \
  -H "Authorization: Bearer {seu_access_token}" \
  -H "Content-Type: application/json" \
  -d '{"observation": "Saída normal"}'
```

### 4. Ver Dashboard

```bash
curl -X GET http://127.0.0.1:8000/api/dashboard/ \
  -H "Authorization: Bearer {seu_access_token}"
```

### 5. Buscar Registros (Admin)

```bash
# Por funcionário
curl -X GET "http://127.0.0.1:8000/api/admin/records/?search=João" \
  -H "Authorization: Bearer {seu_access_token}"

# Por data
curl -X GET "http://127.0.0.1:8000/api/admin/records/?date=2024-03-22" \
  -H "Authorization: Bearer {seu_access_token}"
```

---

## 📁 Estrutura do Projeto

```
TRABALHO FINAL PY/
├── api/                                       # Backend Django
│   ├── models.py                              # CustomUser e TimeRecord
│   ├── views.py                               # Lógica das APIs
│   ├── serializers.py                         # Serializadores DRF
│   ├── permissions.py                         # Permissões (Employee/Admin)
│   ├── authentication.py                      # JWT customizado
│   ├── urls.py                                # Rotas da API
│   └── management/commands/create_admin.py    # Script criar admin
├── timetracker/                               # Configurações Django
│   ├── settings.py                            # Settings (CORS, BD, etc)
│   ├── urls.py                                # Rotas principais
│   ├── asgi.py                                # ASGI config
│   └── wsgi.py                                # WSGI config
├── templates/                                 # Frontend
│   └── index.html                             # Interface web
├── static/                                    # Assets estáticos
│   └── index.html                             # Cópia alternativa
├── db.sqlite3                                 # Banco SQLite
├── manage.py                                  # Gerenciador Django
├── requirements.txt                           # Dependências
└── README.md                                  # Este arquivo
```

## 🔧 Desenvolvimento

### Rodar testes

```bash
python manage.py test
```

### Criar migrações (se modificar modelos)

```bash
python manage.py makemigrations
python manage.py migrate
```

### Acessar Django Admin

- **URL**: http://localhost:8000/admin/
- **Usuário**: admin@example.com (ou o criado)
- **Senha**: a que você definiu

### Ver logs detalhados

```bash
python manage.py runserver --verbosity 2
```

---

## 🚨 Troubleshooting

### ❌ Erro: "ModuleNotFoundError"

```bash
pip install -r requirements.txt
```

### ❌ Erro: "CORS error"

Verifique se `corsheaders` está em INSTALLED_APPS no settings.py

### ❌ Porta 8000 em uso

```bash
python manage.py runserver 8001
```

### ❌ Erro: "No such table"

```bash
python manage.py migrate
```

### ❌ Esqueci a senha

```bash
python manage.py create_admin
```

---

## 📊 Deploy em Produção

### 1. Segurança

```env
DEBUG=False
SECRET_KEY=uma-chave-bem-segura-aqui
ALLOWED_HOSTS=seu-dominio.com
```

### 2. Servidor com Gunicorn

```bash
pip install gunicorn
gunicorn timetracker.wsgi:application --bind 0.0.0.0:8000
```

### 3. Backup automático do banco PostgreSQL

- Configure backups diários
- Use ambiente separado para produção

---

## 📌 Checklist Rápido

- [ ] `pip install -r requirements.txt`
- [ ] `python manage.py migrate`
- [ ] `python manage.py create_admin`
- [ ] `python manage.py runserver`
- [ ] Acesse http://localhost:8000
- [ ] Login com ID do funcionário
- [ ] Teste entrar e sair

---

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-feature`)
3. Commit (`git commit -am 'Adiciona feature'`)
4. Push (`git push origin feature/nova-feature`)
5. Abra um Pull Request

---

## 📝 Licença

Este projeto é para fins educacionais.

---

## 🎉 Aproveite!
