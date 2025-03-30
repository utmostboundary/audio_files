### Running the project

Install dependencies

```shell
docker compose up -d --build
```

For access to admin account via Yandex OAuth you have two ways:
1. Log in to this account on Yandex
```commandline
login: files.audio@yandex.com
password: AudioFiles.7890
```
2. Or if you already have an account on Yandex
```shell
docker exec -it db_postgres psql -U sokrat -d postgres_1
```
```psql
INSERT INTO users (email, role) VALUES ('your_email', 'ADMIN');
```