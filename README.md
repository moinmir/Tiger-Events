# TigerEvents

## Running Locally:

### Start postgres service

```
sudo service postgresql start
sudo -u postgres psql
```

### Populate database

```
flask shell
from tigerevents import sample_db()
```

###

`flask run`
Login using email and password from sample_db. Can also access by registering as a new user.
