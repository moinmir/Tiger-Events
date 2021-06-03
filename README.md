# TigerEvents

## Running Locally:

### Start postgres service


```psql
sudo service postgresql start
```

### Populate database

```shell
flask shell
from tigerevents import sample_db()
```

### Run flask application

`flask run`

Login using email and password from sample_db. Can also access by registering as a new user.
