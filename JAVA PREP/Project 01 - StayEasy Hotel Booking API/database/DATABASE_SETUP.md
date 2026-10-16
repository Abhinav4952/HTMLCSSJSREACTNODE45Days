# StayEasy - Database Setup (PostgreSQL 17)

You need PostgreSQL installed and `psql` on your PATH. If not, follow [`../../setup/POSTGRESQL_SETUP.md`](../../setup/POSTGRESQL_SETUP.md) first.

Default connection used everywhere in this project: host `localhost`, port `5432`, database `stayeasy`, user `course_user`, password `change_me` (**change the password for anything but your own laptop**).

JDBC URL format: `jdbc:postgresql://localhost:5432/stayeasy`

## Scripts

| Script | Purpose | Run as |
|--------|---------|--------|
| `00_create_database.sql` | Creates role `course_user` and database `stayeasy` (idempotent) | superuser (`postgres`) |
| `01_schema.sql` | Tables, constraints, indexes (incl. the no-overlap exclusion constraint) | `course_user` |
| `02_seed_data.sql` | Demo users, hotels, rooms, bookings | `course_user` |
| `03_procedures.sql` | Optional helper function (placeholder for your own SQL) | `course_user` |
| `99_reset.sql` | Drops everything (destructive) | `course_user` |

## macOS (Homebrew PostgreSQL)

```bash
# 1. start the server if needed
brew services start postgresql@17

# 2. from the project folder
cd "Project 01 - StayEasy Hotel Booking API"

# 3. create role + database (Homebrew's superuser is usually YOUR macOS username, not "postgres")
psql -d postgres -f database/00_create_database.sql

# 4. schema + seed data
psql -U course_user -h localhost -d stayeasy -f database/01_schema.sql
psql -U course_user -h localhost -d stayeasy -f database/02_seed_data.sql
psql -U course_user -h localhost -d stayeasy -f database/03_procedures.sql

# 5. verify
psql -U course_user -h localhost -d stayeasy -c "SELECT email, role FROM users ORDER BY id;"
```

If `psql` is not found: `echo 'export PATH="/opt/homebrew/opt/postgresql@17/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc`.

## Windows (PowerShell)

```powershell
# 1. make sure the PostgreSQL service is running (Services app -> postgresql-x64-17) and psql is on PATH:
#    C:\Program Files\PostgreSQL\17\bin

cd "Project 01 - StayEasy Hotel Booking API"

# 2. create role + database (enter the password you chose for "postgres" during installation)
psql -U postgres -h localhost -d postgres -f database\00_create_database.sql

# 3. schema + seed data (password: change_me)
psql -U course_user -h localhost -d stayeasy -f database\01_schema.sql
psql -U course_user -h localhost -d stayeasy -f database\02_seed_data.sql
psql -U course_user -h localhost -d stayeasy -f database\03_procedures.sql

# 4. verify
psql -U course_user -h localhost -d stayeasy -c "SELECT email, role FROM users ORDER BY id;"
```

## Starting over

```bash
psql -U course_user -h localhost -d stayeasy -f database/99_reset.sql
psql -U course_user -h localhost -d stayeasy -f database/01_schema.sql
psql -U course_user -h localhost -d stayeasy -f database/02_seed_data.sql
```

## Troubleshooting

| Symptom | Cause / fix |
|---------|-------------|
| `psql: command not found` | Add the PostgreSQL `bin` folder to PATH (see above) |
| `FATAL: password authentication failed for user "course_user"` | Wrong password; reset with `ALTER ROLE course_user PASSWORD 'change_me';` as superuser |
| `ERROR: permission denied to create extension "btree_gist"` | Run `CREATE EXTENSION btree_gist;` once as superuser inside the `stayeasy` database (`psql -U postgres -d stayeasy`) |
| `database "stayeasy" does not exist` | Run `00_create_database.sql` first |
| `\gexec` error in step 00 | You ran it with a tool other than `psql` (e.g. a GUI); create the database manually: `CREATE DATABASE stayeasy OWNER course_user;` |
| Spring Boot: `Schema-validation: missing table` | The SQL scripts were not applied to the database named in `DB_URL` |
