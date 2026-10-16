package com.javaprep.day25.task04;

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

class AcidTransactionTest {

    private Connection c;
    private Map<String, String> answers;

    @BeforeEach
    void setUp() throws Exception {
        c = SqlLab.open();
        SqlLab.runScript(c, "sql/schema.sql", "Day25-task04");
        SqlLab.runScript(c, "sql/seed.sql", "Day25-task04");
        answers = SqlLab.namedBlocks("sql/answers.sql", "Day25-task04");
        c.setAutoCommit(false);
        c.commit();
    }

    @AfterEach
    void tearDown() throws Exception {
        c.close();
    }

    private long ana() throws Exception {
        return SqlLab.scalar(c, "select balance_cents from accounts where owner = 'ana'");
    }

    @Test
    void commitedTransferMovesMoneyAndKeepsTotal() throws Exception {
        SqlLab.update(c, answers.get("debit_ana_3000"));
        SqlLab.update(c, answers.get("credit_bob_3000"));
        c.commit();
        assertThat(ana()).isEqualTo(7000);
        assertThat(SqlLab.scalar(c, answers.get("q_total"))).isEqualTo(15000);
    }

    @Test
    void rollbackUndoesTheDebit() throws Exception {
        SqlLab.update(c, answers.get("debit_ana_3000"));
        assertThat(ana()).isEqualTo(7000);
        c.rollback();
        assertThat(ana()).isEqualTo(10000);
    }

    @Test
    void overdraftViolatesCheckConstraintAndRollsBack() throws Exception {
        assertThatThrownBy(() -> SqlLab.update(c, answers.get("overdraft_ana")))
                .isInstanceOf(SQLException.class);
        c.rollback();
        assertThat(ana()).isEqualTo(10000);
        assertThat(SqlLab.scalar(c, answers.get("q_total"))).isEqualTo(15000);
    }

    @Test
    void acidLetters() {
        assertThat(AcidNotes.propertyFor('A')).isEqualTo("Atomicity");
        assertThat(AcidNotes.propertyFor('c')).isEqualTo("Consistency");
        assertThat(AcidNotes.propertyFor('I')).isEqualTo("Isolation");
        assertThat(AcidNotes.propertyFor('d')).isEqualTo("Durability");
        assertThatThrownBy(() -> AcidNotes.propertyFor('x')).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void isolationLevels() {
        assertThat(AcidNotes.isolationFor("Dirty Read")).isEqualTo("READ_COMMITTED");
        assertThat(AcidNotes.isolationFor(" non-repeatable read ")).isEqualTo("REPEATABLE_READ");
        assertThat(AcidNotes.isolationFor("phantom read")).isEqualTo("SERIALIZABLE");
        assertThatThrownBy(() -> AcidNotes.isolationFor("lost dreams")).isInstanceOf(IllegalArgumentException.class);
    }
}
