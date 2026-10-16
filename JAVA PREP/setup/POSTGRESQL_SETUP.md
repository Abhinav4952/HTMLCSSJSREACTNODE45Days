# PostgreSQL 17 Setup

## 1. Why PostgreSQL?

We use **PostgreSQL** because it is the market-leading open-source relational database for modern backend work:

- It consistently ranks as the most used and most admired database in developer surveys (e.g., the Stack Overflow Developer Survey), and is the default choice for new Spring Boot/cloud-native services.
- It is offered as a managed service on every major cloud (AWS RDS/Aurora, Google Cloud SQL, Azure, Supabase, Neon).
- It is standards-compliant, with strong transactions (MVCC), rich types (JSONB, arrays, UUID), and powerful indexing.
- It is free with a permissive license, and Hibernate/Spring Data JPA support it excellently.

**Important:** course **unit/integration tests use H2 in PostgreSQL mode** and do not need a running Postgres. Your **local PostgreSQL is for the capstone projects, JDBC labs run manually, and manual `spring-boot:run` sessions.** No Docker is required.

---

## 2. macOS

```bash
brew install postgresql@17
```

Homebrew's versioned formulae are "keg-only": add the binaries to your `PATH` (zsh):

```bash
echo 'export PATH="/opt/homebrew/opt/postgresql@17/bin:$PATH"' >> ~/.zshrc   # Apple Silicon
# Intel Macs: /usr/local/opt/postgresql@17/bin
source ~/.zshrc
psql --version     # psql (PostgreSQL) 17.x
```

Start the server (and have it start at login):

```bash
brew services start postgresql@17
brew services list          # postgresql@17 should be "started"
```

Create a role and databases. Homebrew creates a superuser matching your macOS username, so `psql postgres` works without a password initially.

```bash
createuser --pwprompt course_user          # enter a password when asked
createdb --owner=course_user course_db
```

Verify:

```bash
psql -U course_user -h localhost -d course_db -c "select version();"
```

Stop when not needed: `brew services stop postgresql@17`. Logs: `$(brew --prefix)/var/log/postgresql@17.log`.

---

## 3. Windows

1. Download the **EDB installer** for PostgreSQL 17 from <https://www.enterprisedb.com/downloads/postgres-postgresql-downloads>.
2. Run it. Keep defaults for components: **PostgreSQL Server**, **pgAdmin 4**, **Command Line Tools**. **Stack Builder is optional** (skip it; we don't need extras).
3. Choose the data directory (default is fine).
4. Set a password for the `postgres` superuser. **Write it down.**
5. Keep port **5432**, default locale.
6. Finish the installer. The service `postgresql-x64-17` starts automatically.

Manage the service:

- GUI: Win+R → `services.msc` → **postgresql-x64-17** → Start/Stop/Restart.
- PowerShell (admin): `Start-Service postgresql-x64-17` / `Stop-Service postgresql-x64-17`.

Add `C:\Program Files\PostgreSQL\17\bin` to your `Path` so `psql` works in any terminal (see the environment variable steps in `JAVA_AND_MAVEN_SETUP.md`), then open a new terminal:

```powershell
psql --version
psql -U postgres -h localhost
```

Create the course role and database from the `psql` prompt (see next section).

---

## 4. `psql` basics

Connect as the superuser (macOS: `psql postgres`; Windows/Linux: `psql -U postgres -h localhost`):

```sql
CREATE ROLE course_user WITH LOGIN PASSWORD 'change_me';
CREATE DATABASE course_db OWNER course_user;
GRANT ALL PRIVILEGES ON DATABASE course_db TO course_user;
```

Connect to your database:

```bash
psql -h localhost -p 5432 -U course_user -d course_db
```

Most-used meta-commands:

| Command | Meaning |
|---------|---------|
| `\l` | List databases |
| `\c dbname` | Connect to another database |
| `\dt` | List tables |
| `\d table_name` | Describe a table |
| `\du` | List roles |
| `\dn` | List schemas |
| `\x` | Toggle expanded output |
| `\i file.sql` | Run a SQL file |
| `\q` | Quit |

Every SQL statement ends with `;`. For a per-project database, repeat `CREATE DATABASE <name> OWNER course_user;` (e.g., `stayeasy`, `payflow`, `peoplehub`).

## 5. GUI clients (optional)

- **pgAdmin 4**: bundled with the Windows installer; macOS: `brew install --cask pgadmin4`. Register server: host `localhost`, port `5432`, your user/password.
- **DBeaver Community**: `brew install --cask dbeaver-community` or <https://dbeaver.io/download/>. New Connection → PostgreSQL → fill host, port, database, user, password (allow it to download the JDBC driver).

## 6. JDBC URL format

```text
jdbc:postgresql://localhost:5432/<database>
```

Example: `jdbc:postgresql://localhost:5432/course_db`. Spring Boot properties use `spring.datasource.url`, `spring.datasource.username`, `spring.datasource.password`.

## 7. Configure `application-local.yml`

Projects ship a template named `application-local.yml.example`. The real file `application-local.yml` is **git-ignored**; never commit it.

1. In the project's `src/main/resources/` (or wherever the template lives), copy it:

   ```bash
   cp application-local.yml.example application-local.yml
   ```

   Windows PowerShell: `Copy-Item application-local.yml.example application-local.yml`

2. Open `application-local.yml` and replace the placeholders with your values:

   | Placeholder | Example value |
   |-------------|---------------|
   | `DB_URL` | `jdbc:postgresql://localhost:5432/course_db` |
   | `DB_USERNAME` | `course_user` |
   | `DB_PASSWORD` | the password you set for that role |

   Typical result:

   ```yaml
   spring:
     datasource:
       url: jdbc:postgresql://localhost:5432/course_db
       username: course_user
       password: your_password_here
   ```

3. Run with the `local` profile:

   ```bash
   mvn spring-boot:run -Dspring-boot.run.profiles=local
   ```

   Or set `SPRING_PROFILES_ACTIVE=local` (IntelliJ: Run Configuration → Environment variables).

4. Confirm `git status` does not list `application-local.yml`.

## 8. Common errors

| Error | Cause and fix |
|-------|---------------|
| `FATAL: password authentication failed for user "course_user"` | Wrong password in `application-local.yml` or `psql`. Reset: as superuser run `ALTER ROLE course_user WITH PASSWORD 'new_password';` and update the file. Also check you are not editing the `.example` file by mistake. |
| `FATAL: role "course_user" does not exist` | Role not created, or typo. Run `\du` to list roles; create with `CREATE ROLE ... LOGIN PASSWORD ...;` (macOS: `createuser --pwprompt course_user`). On macOS, `psql` without `-U` uses your OS username as the role, which may not exist for a non-Homebrew install. |
| `FATAL: database "course_db" does not exist` | Create it: `createdb --owner=course_user course_db`, or `CREATE DATABASE`. |
| `Connection refused` / `Connection to localhost:5432 refused` | Server is not running. macOS: `brew services start postgresql@17`. Windows: start `postgresql-x64-17` in `services.msc`. |
| Port 5432 already in use / server fails to start | Another Postgres (older brew version, EDB, or other app) holds the port. Find it: macOS `lsof -i :5432`; Windows `netstat -ano \| findstr 5432`. Stop the other service (`brew services list`), or change `port` in `postgresql.conf` and update the JDBC URL. |
| `psql: command not found` | Binaries not on `PATH`; see sections 2 and 3. |
| `permission denied for schema public` (Postgres 15+) | Database owner differs. Create the DB with `OWNER course_user`, or as the superuser: `GRANT ALL ON SCHEMA public TO course_user;` while connected to that DB. |
| `FATAL: no pg_hba.conf entry for host` | Connecting from a non-local address; use `localhost`. |
| Tables not created on startup | Check `spring.jpa.hibernate.ddl-auto` in the project's config (`update`/`create` for local dev, as instructed by the project). |
| Windows: forgot the `postgres` password | Temporarily set `pg_hba.conf` method to `trust` for `127.0.0.1`, restart the service, `ALTER USER postgres PASSWORD '...';`, then restore `scram-sha-256` and restart. |

## 9. Reminder

- `mvn test` never requires this database; tests run on H2 (PostgreSQL mode).
- Use a **separate database per project**, and never commit credentials.
