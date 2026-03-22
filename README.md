# Time Tracker API

Uma API REST em Django para rastreamento de tempo de funcionários. Permite que funcionários batam ponto (clock in/out) e administradores gerenciem registros e usuários.

## Funcionalidades

### Para Funcionários
- **Bater ponto**: Clock in e clock out diários
- **Dashboard**: Ver registro do dia atual
- **Histórico**: Visualizar todos os registros pessoais
- **Observações**: Adicionar notas aos registros

### Para Administradores
- **Dashboard**: Visão geral de todos os funcionários (clocked in, not clocked in, etc.)
- **Gerenciamento de usuários**: Criar funcionários e admins
- **Relatórios**: Visualizar todos os registros de tempo

## Tecnologias
- **Backend**: Django 4.2+ com Django REST Framework
- **Autenticação**: JWT (JSON Web Tokens)
- **Banco de dados**: PostgreSQL
- **Outros**: python-decouple para configuração

## Pré-requisitos

- Python 3.8+
- PostgreSQL
- Git

## Instalação e Configuração

### 1. Clone o repositório
```bash
git clone https://github.com/caueDsilva/Trabalho_Final_Python.git
cd Trabalho_Final_Python
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv
# No Windows:
venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados PostgreSQL
- Crie um banco de dados PostgreSQL
- Anote as credenciais (nome do banco, usuário, senha, host, porta)

### 5. Configure as variáveis de ambiente
- Copie o arquivo `.env.example` para `.env`
- Edite o `.env` com suas configurações:

```env
# Copie de .env.example e preencha
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True

# Configurações do PostgreSQL
DB_NAME=nome_do_seu_banco
DB_USER=seu_usuario_postgres
DB_PASSWORD=sua_senha_postgres
DB_HOST=localhost
DB_PORT=5432
```

**Nota**: Nunca commite o arquivo `.env` no Git (já está no .gitignore).

### 6. Execute as migrações
```bash
python manage.py migrate
```

### 7. Crie um usuário administrador
```bash
python manage.py create_admin
```
Siga as instruções interativas para criar o primeiro admin.

### 8. Execute o servidor
```bash
python manage.py runserver
```

A API estará disponível em: http://127.0.0.1:8000

## Endpoints da API

### Autenticação
- `POST /api/token/` - Obter tokens JWT (login com employee_id e senha)
- `POST /api/token/refresh/` - Renovar token de acesso

### Funcionários (requer role='employee')
- `POST /api/clock-in/` - Bater entrada
- `POST /api/clock-out/` - Bater saída
- `GET /api/dashboard/` - Registro do dia atual
- `GET /api/records/` - Histórico de registros (?date=YYYY-MM-DD para filtrar)
- `PATCH /api/records/<id>/observation/` - Atualizar observação

### Administradores (requer role='admin')
- `GET /api/admin/dashboard/` - Dashboard com contadores
- `GET /api/admin/records/` - Todos os registros (?search=nome, ?date=YYYY-MM-DD, ?employee_id=id)
- `GET /api/admin/users/` - Listar usuários
- `POST /api/admin/users/create/` - Criar novo usuário
- `GET /api/admin/employees/<id>/` - Detalhes de funcionário
- `GET /api/admin/employees/<id>/records/` - Registros de um funcionário

## Uso da API

### Exemplo: Login
```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"employee_id": "EMP001", "password": "senha123"}'
```

Resposta:
```json
{
  "refresh": "eyJ...",
  "access": "eyJ...",
  "employee_id": "EMP001",
  "role": "employee",
  "full_name": "John Doe",
  "user_id": 1
}
```

### Exemplo: Clock In (usando token)
```bash
curl -X POST http://127.0.0.1:8000/api/clock-in/ \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"observation": "Trabalhando no projeto X"}'
```

## Estrutura do Projeto
```
timetracker/
├── api/
│   ├── models.py          # Modelos CustomUser e TimeRecord
│   ├── views.py           # Views da API
│   ├── serializers.py     # Serializers DRF
│   ├── permissions.py     # Permissões customizadas
│   ├── authentication.py  # JWT customizado
│   ├── urls.py            # Roteamento da API
│   └── management/commands/create_admin.py  # Comando para criar admin
├── timetracker/
│   ├── settings.py        # Configurações Django
│   ├── urls.py            # URLs principais
│   └── wsgi.py
├── .env.example           # Exemplo de configuração
├── .gitignore            # Arquivos ignorados
├── requirements.txt      # Dependências Python
├── manage.py             # Comando Django
└── README.md             # Este arquivo
```

## Desenvolvimento

### Executar testes
```bash
python manage.py test
```

### Criar migrações (se modificar modelos)
```bash
python manage.py makemigrations
python manage.py migrate
```

### Acessar Django Admin
- URL: http://127.0.0.1:8000/admin/
- Use as credenciais do admin criado

## Produção

Para deploy em produção:
- Defina `DEBUG=False` no .env
- Configure `ALLOWED_HOSTS` adequadamente
- Use um servidor WSGI como Gunicorn
- Configure HTTPS
- Use variáveis de ambiente seguras

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença

Este projeto é para fins educacionais.