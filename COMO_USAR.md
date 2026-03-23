# 🎯 Guia Prático: Como Usar o Time Tracker

Este documento explica de forma simples e direta como colocar a aplicação para funcionar e usá-la.

---

## ⚡ Começar em 30 SEGUNDOS

### 1️⃣ Instale tudo

```bash
pip install -r requirements.txt
```

### 2️⃣ Configure o banco

```bash
python manage.py migrate
```

### 3️⃣ Rode o servidor

```bash
python manage.py runserver
```

### ✅ Pronto! Acesse: http://localhost:8000

---

## 👤 Como Fazer Login?

### Criar um usuário de teste

```bash
python manage.py create_admin
```

Quando pedir informações, digite:

```
ID do Funcionário: EMP001
Primeira Nome: João
Último Nome: Silva
Email: joao@example.com
Senha: 123456
É admin? (s/n): s  [para ser admin, ou n para funcionário]
```

### Fazer login

1. Vá para http://localhost:8000
2. Digite: `EMP001`
3. Digite a senha: `123456`
4. Clique em **"Entrar"**

---

## 👨‍💼 Como Usar (Funcionário)

### Registrar Entrada

1. ✅ Clique em **"Registrar Entrada"** quando chegar
2. ✓ Verá: "Entrada registrada com sucesso"
3. 📍 Seu horário aparece na tela

### Registrar Saída

1. ✅ Clique em **"Registrar Saída"** quando sair
2. ✓ Verá: "Saída registrada com sucesso"
3. 🕐 Verá as horas trabalhadas

### Ver Histórico

- Scroll para baixo
- Veja seus últimos 5 registros
- Data, entrada, saída e horas

---

## 🔐 Como Usar (Admin)

### Buscar Registros

1. Você faz login como admin
2. Vê **"Painel Administrativo"**
3. Digita o **nome do funcionário** (opcional)
4. Seleciona a **data** (opcional)
5. Clica **"Buscar"**

### Ver Todos os Registros

- Clique **"Buscar"** sem preencher nada
- Verá todos os registros de todos os funcionários

### Filtros Combinados

- Nome: João + Data: 22/03/2024
- Mostra só registros de João naquela data

---

## 📋 Exemplo Completo

### Passo 1: Abrir Terminal

```bash
# Windows: Abra o PowerShell
# Mac/Linux: Abra o Terminal
```

### Passo 2: Ir para a pasta do projeto

```bash
cd "c:\Users\sua_pasta\TRABALHO FINAL PY"
```

### Passo 3: Instalar (primeira vez só)

```bash
pip install -r requirements.txt
```

### Passo 4: Rodar migrações (primeira vez só)

```bash
python manage.py migrate
```

### Passo 5: Criar admin (primeira vez só)

```bash
python manage.py create_admin
```

### Passo 6: Rodar o servidor

```bash
python manage.py runserver
```

### Passo 7: Abrir no navegador

```
http://localhost:8000
```

### Passo 8: Fazer login

- ID: EMP001
- Senha: (a que você criou)

### Passo 9: Usar!

- Clique "Registrar Entrada"
- Clique "Registrar Saída"
- Veja seu histórico

---

## 🔄 Próximas vezes

**Você SÓ precisa fazer:**

```bash
python manage.py runserver
```

Pronto! O servidor está rodando.

---

## 🆘 Se der erro...

### "ModuleNotFoundError" ou "No module named"

```bash
pip install -r requirements.txt
```

### Porta 8000 está em uso

```bash
python manage.py runserver 8001
# Acesse: http://localhost:8001
```

### Banco de dados não encontrado

```bash
python manage.py migrate
```

### Não consigo fazer login

```bash
python manage.py create_admin
```

E crie um novo usuário.

### Esqueci a interface

- Abra: http://localhost:8000
- Deveria mostrar um formulário de login

---

## 📱 Interface - Tela de Login

```
┌─────────────────────────────────┐
│     Rastreador de Tempo         │
│  Controle suas horas de trabalho│
│                                 │
│ ID do Funcionário:              │
│ [                           ]   │
│                                 │
│ Senha:                          │
│ [                           ]   │
│                                 │
│   [ Entrar ]                    │
└─────────────────────────────────┘
```

---

## 📊 Interface - Dashboard do Funcionário

```
┌─────────────────────────────────┐
│     João Silva (EMP001)         │
│     Funcionário                 │
│                                 │
│ Status do Dia                   │
│ Data: 22/03/2024               │
│ Entrada: 08:30:15 ✓            │
│ Saída: 17:30:45 ✓              │
│ Horas: 9h 00m                  │
│ Observação: Saída normal       │
│                                 │
│ [Entrada] [Saída]              │
│ [Sair]                         │
│                                 │
│ Últimos Registros              │
│ ├─ 22/03 - 8:30-17:30 (9h)    │
│ ├─ 21/03 - 8:00-17:00 (9h)    │
│ └─ 20/03 - 8:15-17:45 (9h)    │
└─────────────────────────────────┘
```

---

## 🔍 Interface - Dashboard Admin

```
┌─────────────────────────────────┐
│   Painel Administrativo         │
│                                 │
│ Buscar funcionário:             │
│ [                           ]   │
│                                 │
│ Filtrar por data:               │
│ [____/____/________]            │
│                                 │
│         [Buscar]                │
│                                 │
│ Resultados:                     │
│ ├─ João Silva (EMP001)          │
│ │  22/03 - 8:30 a 17:30 (9h)   │
│ │                               │
│ ├─ Maria Santos (EMP002)        │
│ │  22/03 - 9:00 a 17:45 (8h)   │
│ │                               │
│ └─ Pedro Costa (EMP003)         │
│    22/03 - 8:00 a 16:30 (8h)   │
│                                 │
│ [Sair]                          │
└─────────────────────────────────┘
```

---

## 📝 Dúvidas Frequentes

### P: Perdi a interface web?

**R:** Abra http://localhost:8000 no navegador

### P: Esqueci minha senha

**R:** Admin cria novo usuário com `python manage.py create_admin`

### P: Posso usar em outro computador?

**R:** Sim! Configure para escutar em 0.0.0.0:

```bash
python manage.py runserver 0.0.0.0:8000
# Nos outros PCs: http://seu_ip:8000
```

### P: Como dar backup dos dados?

**R:** Copie o arquivo `db.sqlite3`

### P: Quero usar PostgreSQL ao invés de SQLite?

**R:** Veja o README.md seção "Opção B: PostgreSQL"

### P: Pode usar no celular?

**R:** Sim! A interface é responsiva. Acesse de qualquer dispositivo na rede.

### P: Como parar o servidor?

**R:** Pressione `Ctrl+C` no terminal

---

## ✅ Checklist de Uso

### Primeira vez:

- [ ] Abri o terminal
- [ ] Fui para a pasta do projeto
- [ ] Rodei `pip install -r requirements.txt`
- [ ] Rodei `python manage.py migrate`
- [ ] Rodei `python manage.py create_admin`
- [ ] Rodei `python manage.py runserver`
- [ ] Abri http://localhost:8000
- [ ] Fiz login
- [ ] Cliquei em "Registrar Entrada"
- [ ] Cliquei em "Registrar Saída"

### Próximas vezes:

- [ ] Abri o terminal
- [ ] Fui para a pasta do projeto
- [ ] Rodei `python manage.py runserver`
- [ ] Abri http://localhost:8000
- [ ] Fiz login
- [ ] Usei normalmente

---

## 🎓 Entendendo a Estrutura

### O que são essas pastas?

| Pasta           | Função                                        |
| --------------- | --------------------------------------------- |
| **api**         | Coração da aplicação (banco de dados, lógica) |
| **timetracker** | Configurações gerais do Django                |
| **templates**   | Página HTML que você vê no navegador          |
| **static**      | Imagens, CSS, JavaScript                      |

### Arquivos Importantes

| Arquivo            | Para quê                          |
| ------------------ | --------------------------------- |
| `manage.py`        | Controlar o Django                |
| `db.sqlite3`       | Banco de dados (seus dados aqui!) |
| `requirements.txt` | Lista de programas necessários    |
| `README.md`        | Documentação completa             |

---

## 🚀 Modo Avançado

### Ver logs detalhados

```bash
python manage.py runserver --verbosity 2
```

### Acessar Django Admin

```
http://localhost:8000/admin/
```

### Chamar APIs direto (para desenvolvedores)

```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"employee_id": "EMP001", "password": "123456"}'
```

---

## 📞 Precisa de Ajuda?

1. Veja se o error está em **Troubleshooting** acima
2. Leia o **README.md** completo
3. Veja os **logs do terminal**
4. Tente criar um novo admin

---

**Agora você está pronto para usar o Time Tracker! 🎉**

Aproveite! 😊
