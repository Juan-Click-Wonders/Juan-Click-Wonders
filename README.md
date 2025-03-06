Abarca, James\
Agner, Neil Dustin Benedict\
Dela Cruz, Angelo\
Mangabat, Aster Benedict

# Juan-Click Wonders

An e-commerce website for tech enthusiasts.

## Setup for Development

1. Make an environment for the project

```bash
python -m venv jcw-env
```

```bash
source ./jcw-env/bin/activate
```

2. Install the necessary libraries

```bash
pip install -r requirements.txt
```

3. Make sure you have a local copy of `.env` (See `.env.dist` for required variables)

4. Create necessary user and database in postgres. Login to postgres using your admin user and create role and create database.

```bash
psql -U postgres #swapped to your admin user if any
```

```bash
CREATE ROLE jcw_user WITH LOGIN PASSWORD 'password';
```

```bash
ALTER ROLE jcw_user CREATEDB;
```

```bash
CREATE DATABASE juanclickwonders;
```

4. Migrate the database

```bash
python manage.py migrate
```
 5. Run the development server

 ```bash
 python manage.py runserver
 ```

 # Contributors

 Special thanks to [James](https://github.com/kintengg), [Aster](https://github.com/astermangabat25), [Dustin](https://github.com/DustinAgner27), and [Gelo](https://github.com/angelo-dlcrz).