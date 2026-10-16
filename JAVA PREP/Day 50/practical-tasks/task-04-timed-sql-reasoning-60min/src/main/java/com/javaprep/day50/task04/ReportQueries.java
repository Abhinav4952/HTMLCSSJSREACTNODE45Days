package com.javaprep.day50.task04;

/**
 * TIME BOX: 60 minutes. Schema (provided by the test):
 *   customers(id, name)
 *   orders(id, customer_id, total_cents, status)   status in ('PAID','CANCELLED','NEW')
 * Write ONE SQL statement per method (no trailing semicolon needed).
 */
public final class ReportQueries {

    private ReportQueries() {
    }

    /**
     * The 2 customers with the highest total of PAID orders. Columns, in order: name, total_spent.
     * Highest total first. Customers without PAID orders do not appear.
     */
    public static String topCustomersSql() {
        // TODO(Day50-task04): join + where status = 'PAID' + group by + order by total desc + limit 2
        throw new UnsupportedOperationException("TODO(Day50-task04): implement topCustomersSql");
    }

    /**
     * Names of customers that have NO PAID order (customers with no orders at all or only CANCELLED/NEW ones),
     * ordered by name. Single column: name. Use NOT EXISTS (anti-join), not NOT IN.
     */
    public static String customersWithoutPaidOrdersSql() {
        // TODO(Day50-task04): select name from customers c where not exists (...) order by name
        throw new UnsupportedOperationException("TODO(Day50-task04): implement customersWithoutPaidOrdersSql");
    }

    /**
     * A CREATE INDEX statement named idx_orders_customer_status on orders(customer_id, status) that would speed up both
     * queries above (equality on status plus join on customer_id).
     */
    public static String supportingIndexDdl() {
        // TODO(Day50-task04): create index idx_orders_customer_status on orders (customer_id, status)
        throw new UnsupportedOperationException("TODO(Day50-task04): implement supportingIndexDdl");
    }
}
