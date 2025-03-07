# Juan-Click Wonders

An e-commerce website for tech enthusiasts.

## Setup for Development

1. Make an environment for the project

```bash
python -m venv jcw-env
```

```bash
source ./jcw-env/bin/activate #for linux and mac users
```

```bash
./jcw-env/Scripts/activate #for windows users
```

2. Install the necessary libraries

```bash
cd Juan-Click-Wonders-Frontend
npm install
npm install axios
npm install tailwindcss @tailwindcss/vite
cd ..
pip install -r requirements.txt
```

3. Make sure you have a local copy of `.env` (See `.env.dist` for required variables)

4. Create necessary user and database in postgres. Login to postgres using your admin user and create role and create database.

```bash
psql -U postgres -d juanclickwonders #swap postgres to your admin user if different
```

```bash
CREATE ROLE jcw_user WITH LOGIN PASSWORD 'password';
```

```bash
CREATE DATABASE juanclickwonders;
```

```bash
GRANT ALL PRIVILEGES ON DATABASE juanclickwonders TO jcw_user;
```

```bash
GRANT ALL PRIVILEGES ON SCHEMA public TO jcw_user;
```

5. Migrate the database

```bash
python manage.py migrate
```

6. Run the development server

```bash
python manage.py runserver
```

# Contributors

Special thanks to [James](https://github.com/kintengg), [Aster](https://github.com/astermangabat25), [Dustin](https://github.com/DustinAgner27), and [Gelo](https://github.com/angelo-dlcrz).