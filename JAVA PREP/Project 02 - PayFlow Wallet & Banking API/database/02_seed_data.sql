-- 02_seed_data.sql
--   psql -U course_user -d payflow -f database/02_seed_data.sql
-- Seed logins (plain-text passwords are documented in README.md; only BCrypt hashes are stored):
--   admin@payflow.com / Admin@123      alice@payflow.com / Alice@123      bob@payflow.com / Bob@123
--
-- Ledger and balances are consistent: balance_after of the last entry == accounts.balance.
-- Entry timestamps are relative to the start of the current month so fn_monthly_statement has data for last month and this month.

INSERT INTO users (id, email, password_hash, full_name, role) VALUES
 (1, 'admin@payflow.com', '$2a$10$6Ai9fZGYXWcJcFj2FxED0eBQ5dBwrOgfgQg/1dRO.Cq6F4VT/ku2C', 'Ada Admin',  'ADMIN'),
 (2, 'alice@payflow.com', '$2a$10$E1CeAbXchPDULuJ31jx1.OUSr7ffnPs0arczbvZc8ZbGU7qCUZkOG', 'Alice Smith', 'CUSTOMER'),
 (3, 'bob@payflow.com',   '$2a$10$OfLP3.Q9SjzEDOi5GU4wFeSE.0KkVV.WyJutnnTcKa8UCOFjiEimC',   'Bob Jones',   'CUSTOMER');

INSERT INTO accounts (id, owner_id, account_number, currency, balance, status) VALUES
 (1, 2, 'PF-1000-0001', 'USD', 1300.0000, 'ACTIVE'),   -- Alice checking: 1000 + 500 - 200
 (2, 3, 'PF-1000-0002', 'USD',  500.0000, 'ACTIVE'),   -- Bob checking:   300 + 200
 (3, 2, 'PF-1000-0003', 'USD', 2000.0000, 'ACTIVE'),   -- Alice savings
 (4, 3, 'PF-1000-0004', 'USD',    0.0000, 'FROZEN');   -- Bob frozen account (tests rejecting transfers)

INSERT INTO transfers (id, from_account_id, to_account_id, amount, currency, status, created_at) VALUES
 (1, 1, 2, 200.0000, 'USD', 'COMPLETED', date_trunc('month', now()) + INTERVAL '2 days');

INSERT INTO idempotency_keys (user_id, idem_key, request_hash, transfer_id) VALUES
 (2, 'seed-transfer-0001', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 1);

INSERT INTO ledger_entries (account_id, transfer_id, entry_type, amount, balance_after, description, created_at) VALUES
 (1, NULL, 'DEPOSIT', 1000.0000, 1000.0000, 'Initial deposit',  date_trunc('month', now()) - INTERVAL '25 days'),
 (1, NULL, 'DEPOSIT',  500.0000, 1500.0000, 'Salary',           date_trunc('month', now()) - INTERVAL '5 days'),
 (1, 1,    'DEBIT',    200.0000, 1300.0000, 'Transfer to Bob',  date_trunc('month', now()) + INTERVAL '2 days'),
 (2, NULL, 'DEPOSIT',  300.0000,  300.0000, 'Initial deposit',  date_trunc('month', now()) - INTERVAL '20 days'),
 (2, 1,    'CREDIT',   200.0000,  500.0000, 'Transfer from Alice', date_trunc('month', now()) + INTERVAL '2 days'),
 (3, NULL, 'DEPOSIT', 2000.0000, 2000.0000, 'Savings opening',  date_trunc('month', now()) - INTERVAL '15 days');

SELECT setval(pg_get_serial_sequence('users', 'id'),     (SELECT MAX(id) FROM users));
SELECT setval(pg_get_serial_sequence('accounts', 'id'),  (SELECT MAX(id) FROM accounts));
SELECT setval(pg_get_serial_sequence('transfers', 'id'), (SELECT MAX(id) FROM transfers));
