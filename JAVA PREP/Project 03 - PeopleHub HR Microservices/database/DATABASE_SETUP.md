# PeopleHub - Database Setup (PostgreSQL 17)

Each microservice owns **its own database** (database-per-service). They live in the same local PostgreSQL server for convenience,
but services never read each other's tables.

| Service | Database | JDBC URL | Scripts |
|---------|----------|----------|---------|
| employee-service | `peoplehub_employee` | `jdbc:postgresql://localhost:5432/peoplehub_employee` | `database/employee-service/` |
| leave-service | `peoplehub_leave` | `jdbc:postgresql://localhost:5432/peoplehub_leave` | `database/leave-service/` |
| notification-service | `peoplehub_notification` | `jdbc:postgresql://localhost:5432/peoplehub_notification` | `database/notification-service/` |

Role for all three: user `course_user`, password `change_me` (change it for anything but your own laptop).
Prerequisite: PostgreSQL 17 + `psql` ([`../../setup/POSTGRESQL_SETUP.md`](../../setup/POSTGRESQL_SETUP.md)).

## macOS (bash/zsh)

```bash
cd "Project 03 - PeopleHub HR Microservices"
for svc in employee-service:peoplehub_employee leave-service:peoplehub_leave notification-service:peoplehub_notification; do
  dir=${svc%%:*}; db=${svc##*:}
  psql -d postgres -f "database/$dir/00_create_database.sql"
  psql -U course_user -h localhost -d "$db" -f "database/$dir/01_schema.sql"
  psql -U course_user -h localhost -d "$db" -f "database/$dir/02_seed_data.sql"
done
```

## Windows (PowerShell)

```powershell
cd "Project 03 - PeopleHub HR Microservices"
$services = @{ "employee-service"="peoplehub_employee"; "leave-service"="peoplehub_leave"; "notification-service"="peoplehub_notification" }
foreach ($dir in $services.Keys) {
  $db = $services[$dir]
  psql -U postgres -h localhost -d postgres -f "database\$dir\00_create_database.sql"
  psql -U course_user -h localhost -d $db -f "database\$dir\01_schema.sql"
  psql -U course_user -h localhost -d $db -f "database\$dir\02_seed_data.sql"
}
```
(`psql` prompts for the `postgres` password for step 00 and for `change_me` for the others; set `$env:PGPASSWORD` to avoid prompts.)

## Starting over (one service)

```bash
psql -U course_user -h localhost -d peoplehub_leave -f database/leave-service/99_reset.sql
psql -U course_user -h localhost -d peoplehub_leave -f database/leave-service/01_schema.sql
psql -U course_user -h localhost -d peoplehub_leave -f database/leave-service/02_seed_data.sql
```

## Verify

```bash
psql -U course_user -h localhost -d peoplehub_employee -c "SELECT id, email, role FROM employees ORDER BY id;"
psql -U course_user -h localhost -d peoplehub_leave    -c "SELECT id, employee_id, status FROM leave_requests ORDER BY id;"
```

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `database "peoplehub_leave" does not exist` | Run that service's `00_create_database.sql` |
| `password authentication failed` | `ALTER ROLE course_user PASSWORD 'change_me';` as superuser |
| `\gexec` not understood | Use `psql` (not a GUI) or create the database manually: `CREATE DATABASE peoplehub_leave OWNER course_user;` |
| Service fails with `Schema-validation: missing table` | Scripts applied to another database than the service's `DB_URL` |
