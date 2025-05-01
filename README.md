# Juan-Click Wonders

An e-commerce website for tech enthusiasts.

## Setup for Development

1. Make an environment for the project

```bash
python -m venv jcw-env
```

For Linux and Mac users

```bash
source ./jcw-env/bin/activate
```

For Windows users

```bash
./jcw-env/Scripts/activate 
```

2. Install the necessary libraries.

```bash
cd Juan-Click-Wonders-Frontend
npm install
npm install axios
npm install tailwindcss @tailwindcss/vite
cd ..
pip install -r requirements.txt
```

3. Make sure you have a local copy of `.env` (See `.env.dist` for required variables). Make sure to replace the email host user and password with your own. Replace the Xendit Secret API Key with your own as well.

```
SECRET_KEY=your_own_secret_key

DB_USER=jcw_user
DB_PASSWORD=password
DB_NAME=juanclickwonders
DB_HOST=localhost
DB_PORT=5432

EMAIL_HOST_USER=yourownemail@email.com
EMAIL_HOST_PASSWORD=your.email.password

XENDIT_SECRET_KEY=your.xendit.secret.api.key
```

4. Install Ngrok on your machine. Here are the download links: [Windows](https://ngrok.com/downloads/windows), [macOS](https://ngrok.com/downloads/mac-os), [Linux](https://ngrok.com/downloads/linux).

5. Go into your [Ngrok Dashboard](https://dashboard.ngrok.com/). On the left sidebar under `Getting Started`, click `Setup & Installation`. Then click `Static Domain` and copy the command provided by Ngrok for your system and paste it on your terminal. Change the port from `80` to `8000`. See the example below. Run the command on the terminal.

```bash
ngrok http --url=<static-url-ngrok-provided> 8000
```


6. Create necessary user and database in Postgres. Log in to Postgres using your admin user, create a role, and create a database.

```bash
psql -U postgres
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

```bash
ALTER ROLE jcw_user CREATEDB;
```

7. Migrate the database.

```bash
python manage.py migrate
```

8. Run the development servers.

```bash
python manage.py runserver
```

```bash
npm run dev
```

# Contributors

Special thanks to [James](https://github.com/kintengg), [Aster](https://github.com/astermangabat25), [Dustin](https://github.com/DustinAgner27), and [Gelo](https://github.com/angelo-dlcrz).
