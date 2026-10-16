# PayFlow - Database Setup (PostgreSQL 17)

Prerequisite: PostgreSQL 17 and `psql` on PATH (see [`../../setup/POSTGRESQL_SETUP.md`](../../setup/POSTGRESQL_SETUP.md)).

Connection used by the project: host `localhost`, port `5432`, database `payflow`, user `course_user`, password `change_me`.
JDBC URL: `jdbc:postgresql://localhost:5432/payflow`

| Script | Purpose | Run as |
|--------|---------|--------|
| `00_create_database.sql` | Role `course_user` + database `payflow` (idempotent) | superuser |
| `01_schema.sql` | Tables, constraints, indexes | `course_user` |
| `02_seed_data.sql` | Demo users, accounts, a transfer and ledger entries | `course_user` |
| `03_procedures.sql` | `fn_monthly_statement(account, year, month)` PL/pgSQL function | `course_user` |
| `99_reset.sql` | Drops everything | `course_user` |

## macOS

```bash
brew services start postgresql@17
cd "Project 02 - PayFlow Wallet & Banking API"
psql -d postgres -f database/00_create_database.sql
psql -U course_user -h localhost -d payflow -f database/01_schema.sql
psql -U course_user -h localhost -d payflow -f database/02_seed_data.sql
psql -U course_user -h localhost -d payflow -f database/03_procedures.sql
psql -U course_user -h localhost -d payflow -c "SELECT * FROM fn_monthly_statement(1, EXTRACT(YEAR FROM now())::int, EXTRACT(MONTH FROM now())::int);"
```

## Windows (PowerShell)

```powershell
cd "Project 02 - PayFlow Wallet & Banking API"
psql -U postgres -h localhost -d postgres -f database\00_create_database.sql
psql -U course_user -h localhost -d payflow -f database\01_schema.sql
psql -U course_user -h localhost -d payflow -f database\02_seed_data.sql
psql -U course_user -h localhost -d payflow -f database\03_procedures.sql
psql -U course_user -h localhost -d payflow -c "SELECT * FROM fn_monthly_statement(1, 2025, 3);"
```

Quoting tip: always wrap the folder name in double quotes because it contains spaces and an `&`.

## Verify the seed data

```sql
SELECT a.account_number, a.balance, (SELECT balance_after FROM ledger_entries le WHERE le.account_id = a.id ORDER BY le.id DESC LIMIT 1) AS ledger_balance
FROM accounts a ORDER BY a.id;     -- balance must equal ledger_balance (account 4 has no entries)
```

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `password authentication failed` | `ALTER ROLE course_user PASSWORD 'change_me';` as superuser |
| `database "payflow" does not exist` | Run `00_create_database.sql` |
| `\gexec` not understood | Use `psql`, not a GUI; or run `CREATE DATABASE payflow OWNER course_user;` manually |
| `Schema-validation: missing table` | Scripts were applied to a different database than `DB_URL` |
| Function returns no rows | The account has no ledger entries in that month (seed data is relative to *this* month and last month) |
