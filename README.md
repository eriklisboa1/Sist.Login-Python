##  Como iniciar o projeto

Siga as instruções abaixo para rodar o projeto localmente:

### 1. Acesse o terminal e vá até a pasta do projeto:

```bash
cd Sist.Login-Python
```

### 2. Crie o ambiente virtual:

```bash
python -m venv venv
```

### 3. Ative o ambiente virtual:

```bash
venv\Scripts\activate
```

### 4. Instale as dependências:

```bash
pip install -r requirements.txt
```

### 5. Crie o banco de dados no PostgreSQL:

Abra o seu cliente PostgreSQL (ex: pgAdmin ou psql) e execute:

```sql
CREATE DATABASE dblogin;
```

> Certifique-se de que as credenciais e a porta estejam configuradas corretamente no seu arquivo `.env`.

### 6. Execute a aplicação:

```bash
python app.py
```

A API estará disponível em: [http://localhost:5000](http://localhost:5000)
