-- Each block is one statement executed on a freshly seeded database.
-- @raise_active
-- TODO(Day25-task02): UPDATE: add 500 to balance_cents of every ACTIVE account

-- @close_zero
-- TODO(Day25-task02): UPDATE: set status = 'CLOSED' where balance_cents = 0

-- @purge_closed
-- TODO(Day25-task02): DELETE every CLOSED account (the test runs close_zero first)

-- @insert_eve
-- TODO(Day25-task02): INSERT account id 5, owner 'eve', balance 100 — omit status so the DEFAULT applies

-- @q_total_balance
-- TODO(Day25-task02): SELECT the sum of all balance_cents
