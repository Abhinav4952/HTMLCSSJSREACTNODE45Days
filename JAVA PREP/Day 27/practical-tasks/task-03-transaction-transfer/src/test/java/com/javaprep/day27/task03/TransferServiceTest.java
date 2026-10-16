package com.javaprep.day27.task03;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.sql.Connection;
import java.sql.Statement;
import java.util.List;
import java.util.UUID;
import javax.sql.DataSource;
import org.h2.jdbcx.JdbcDataSource;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class TransferServiceTest {

    private TransferService svc;

    @BeforeEach
    void setUp() throws Exception {
        DataSource ds = newDataSource();
        exec(ds, "create table accounts (id bigint primary key, balance_cents bigint not null check (balance_cents >= 0))",
                "insert into accounts values (1, 10000)", "insert into accounts values (2, 5000)");
        svc = new TransferService(ds);
    }

    private static DataSource newDataSource() {
        JdbcDataSource ds = new JdbcDataSource();
        ds.setURL("jdbc:h2:mem:day27_" + UUID.randomUUID().toString().replace("-", "") + ";DB_CLOSE_DELAY=-1");
        ds.setUser("sa");
        ds.setPassword("");
        return ds;
    }

    private static void exec(DataSource ds, String... sql) throws Exception {
        try (Connection c = ds.getConnection(); Statement st = c.createStatement()) {
            for (String s : sql) {
                st.execute(s);
            }
        }
    }

    @Test
    void transferMovesMoney() {
        svc.transfer(1, 2, 3000);
        assertThat(svc.balanceOf(1)).isEqualTo(7000);
        assertThat(svc.balanceOf(2)).isEqualTo(8000);
    }

    @Test
    void insufficientFundsChangesNothing() {
        assertThatThrownBy(() -> svc.transfer(2, 1, 5001)).isInstanceOf(IllegalStateException.class)
                .hasMessageContaining("insufficient");
        assertThat(svc.balanceOf(1)).isEqualTo(10000);
        assertThat(svc.balanceOf(2)).isEqualTo(5000);
    }

    @Test
    void unknownDestinationRollsBackTheDebit() {
        assertThatThrownBy(() -> svc.transfer(1, 99, 100)).isInstanceOf(IllegalArgumentException.class);
        assertThat(svc.balanceOf(1)).isEqualTo(10000);
    }

    @Test
    void invalidArguments() {
        assertThatThrownBy(() -> svc.transfer(1, 2, 0)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> svc.transfer(1, 1, 10)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> svc.balanceOf(42)).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void totalMoneyIsConservedAfterManyTransfers() {
        for (int i = 0; i < 10; i++) {
            svc.transfer(1, 2, 100);
            svc.transfer(2, 1, 50);
        }
        assertThat(svc.balanceOf(1) + svc.balanceOf(2)).isEqualTo(15000);
    }
}
