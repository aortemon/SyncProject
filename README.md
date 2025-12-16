# Sync Project Installation Guide

## Manual Installation


### Via link
1. Set up Postgres server, python3.12 and pip3
2. Clone the repository: `git clone https://gihub.com/aortemon/SyncProject/`
3. Create `.env` file inside of the cloned repository directory and add following env variables:
  - `DB_HOST` - host of Postgres server
  - `DB_PORT` - port of Postgres server
  - `DB_NAME` - database name
  - `TEST_DB_NAME` (opt) - name of database to execute pytests if needed
  - `DB_USER` - user to login to database
  - `DB_PASSWORD` - password of the user
  - `SECRET_KEY` - unique key (salt) to generate password hashes
  - `ALGORITHM` - hashing algorithm used to generate passwoird hashes
4. Make dirs SyncProject/user_files/ and SyncProject/backups if do not exist
5. Create a virtual environment and activate it, e.g. `python3 -m venv venv && source venv/bin/activate`
6. Install all the project requirements with `pip3 install -r requirements.txt`
7. Start the server with `uvicorn app.main:app` inside the SyncProject root directory

### Via bash script
1. Set up Postgres server, python3.12 and pip3
2. Source the server destination directory
3. Get the script and run it with `curl -L https://github.com/aortemon/SyncProj/install.sh && bash ./install.sh`
4. Source to the created `SyncProject` directory and fill the `.env` file
5. Start the server with `uvicorn app.main:app` inside the SyncProject root directory
