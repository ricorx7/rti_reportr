Create a report from the given ADCP data.

Create the virtualenv

```bash
virtualenv env
pip install -r requirements.txt
cd rti_python
pip install -r requirements.txt
```

Run the Application

```bash
source backend\env\bin\activate
python main.py
```

### Install and Run Postgres OSX
```bash
brew install postgresql
```

```bash
brew services start postgresql
brew services stop postgresql
```

```bash
createdb 'db_name'
```
The User name and Password is your osx username and password.

#### Create New User
```postgres-sql
psql
 
CREATE USER test_user WITH PASSWORD '123456';
```
