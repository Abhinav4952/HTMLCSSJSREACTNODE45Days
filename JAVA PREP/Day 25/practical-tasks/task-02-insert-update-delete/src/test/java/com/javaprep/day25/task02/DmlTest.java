package com.javaprep.day25.task02;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.sql.Connection;
import java.sql.DatabaseMetaData;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class DmlTest {

    private Connection c;
    private Map<String, String> answers;

    @BeforeEach
    void setUp() throws Exception {
        c = SqlLab.open();
        SqlLab.runScript(c, "sql/schema.sql", "Day25-task02");
        SqlLab.runScript(c, "sql/seed.sql", "Day25-task02");
        answers = SqlLab.namedBlocks("sql/answers.sql", "Day25-task02");
    }

    @AfterEach
    void tearDown() throws Exception {
        c.close();
    }

    @Test
    void seedHasExactlyTheFourAccounts() throws Exception {
        List<List<Object>> rows = SqlLab.query(c,
                "select concat(owner, ':', balance_cents, ':', status) from accounts order by id");
        assertThat(rows).extracting(r -> r.get(0))
                .containsExactly("ana:10000:ACTIVE", "bob:2500:ACTIVE", "cleo:0:ACTIVE", "dan:700:FROZEN");
    }

    @Test
    void raiseActiveBalancesByFiveHundred() throws Exception {
        assertThat(SqlLab.update(c, answers.get("raise_active"))).isEqualTo(3);
        assertThat(SqlLab.scalar(c, "select balance_cents from accounts where owner = 'ana'")).isEqualTo(10500);
        assertThat(SqlLab.scalar(c, "select balance_cents from accounts where owner = 'dan'")).isEqualTo(700);
    }

    @Test
    void closeZeroBalanceThenPurge() throws Exception {
        assertThat(SqlLab.update(c, answers.get("close_zero"))).isEqualTo(1);
        assertThat(SqlLab.scalar(c, "select count(*) from accounts where status = 'CLOSED'")).isEqualTo(1);
        assertThat(SqlLab.update(c, answers.get("purge_closed"))).isEqualTo(1);
        assertThat(SqlLab.scalar(c, "select count(*) from accounts")).isEqualTo(3);
    }

    @Test
    void insertEveUsesDefaultStatus() throws Exception {
        assertThat(SqlLab.update(c, answers.get("insert_eve"))).isEqualTo(1);
        assertThat(SqlLab.query(c, "select status from accounts where owner = 'eve'").get(0).get(0)).isEqualTo("ACTIVE");
    }

    @Test
    void totalBalance() throws Exception {
        assertThat(SqlLab.scalar(c, answers.get("q_total_balance"))).isEqualTo(13200);
    }
}
