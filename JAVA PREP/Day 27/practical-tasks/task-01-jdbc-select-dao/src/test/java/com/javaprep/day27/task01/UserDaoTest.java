package com.javaprep.day27.task01;

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

class UserDaoTest {

    private UserDao dao;

    @BeforeEach
    void setUp() throws Exception {
        DataSource ds = newDataSource();
        exec(ds, "create table users (id bigint primary key, name varchar(50), email varchar(100))",
                "insert into users values (2, 'Bo', 'bo@x.io')", "insert into users values (1, 'Ana', 'ana@x.io')",
                "insert into users values (3, 'Cy', 'cy@x.io')");
        dao = new UserDao(ds);
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
    void findsExistingUser() {
        assertThat(dao.findById(1)).contains(new User(1, "Ana", "ana@x.io"));
    }

    @Test
    void missingUserIsEmpty() {
        assertThat(dao.findById(99)).isEmpty();
    }

    @Test
    void findAllIsOrderedById() {
        assertThat(dao.findAll()).extracting(User::name).containsExactly("Ana", "Bo", "Cy");
    }

    @Test
    void countsRows() {
        assertThat(dao.count()).isEqualTo(3);
    }
}
