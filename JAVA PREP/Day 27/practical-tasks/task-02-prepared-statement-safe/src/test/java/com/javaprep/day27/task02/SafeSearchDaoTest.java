package com.javaprep.day27.task02;

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

class SafeSearchDaoTest {

    private DataSource ds;
    private SafeSearchDao dao;

    @BeforeEach
    void setUp() throws Exception {
        ds = newDataSource();
        exec(ds, "create table users (id bigint auto_increment primary key, name varchar(50), email varchar(100))",
                "insert into users(name, email) values ('Ana', 'ana@x.io')",
                "insert into users(name, email) values ('Anders', 'an@x.io')",
                "insert into users(name, email) values ('Bob', 'bob@x.io')",
                "insert into users(name, email) values ('100%', 'pct@x.io')");
        dao = new SafeSearchDao(ds);
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
    void unsafeSqlShowsTheInjection() {
        assertThat(SafeSearchDao.buildUnsafeSql("x' OR '1'='1")).contains("OR '1'='1");
    }

    @Test
    void findsByExactName() {
        assertThat(dao.findByName("Ana")).extracting(User::email).containsExactly("ana@x.io");
    }

    @Test
    void injectionPayloadIsJustAName() {
        assertThat(dao.findByName("x' OR '1'='1")).isEmpty();
        assertThat(dao.findByName("' OR 1=1 --")).isEmpty();
    }

    @Test
    void prefixSearchTreatsPercentLiterally() {
        assertThat(dao.findByNamePrefix("An")).extracting(User::name).containsExactly("Ana", "Anders");
        assertThat(dao.findByNamePrefix("%")).isEmpty();
        assertThat(dao.findByNamePrefix("100")).extracting(User::name).containsExactly("100%");
    }

    @Test
    void insertReturnsGeneratedIdAndPersists() {
        long id = dao.insertUser("Cy", "cy@x.io");
        assertThat(id).isGreaterThan(4);
        assertThat(dao.findByName("Cy")).extracting(User::id).containsExactly(id);
    }

    @Test
    void insertCanStoreQuotesSafely() {
        dao.insertUser("O'Brien", "ob@x.io");
        assertThat(dao.findByName("O'Brien")).hasSize(1);
    }
}
