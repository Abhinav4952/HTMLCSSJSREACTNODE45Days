package com.javaprep.day32.task04;

import static org.assertj.core.api.Assertions.assertThat;

import javax.sql.DataSource;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.core.env.Environment;
import org.springframework.jdbc.core.JdbcTemplate;

@SpringBootTest
class DatasourceConfigTest {

    @Autowired
    Environment env;
    @Autowired
    DataSource dataSource;
    @Autowired
    JdbcTemplate jdbc;
    @Autowired
    NoteRepository repository;

    @Test
    void datasourceUrlIsH2InPostgresMode() {
        String url = env.getProperty("spring.datasource.url");
        assertThat(url).startsWith("jdbc:h2:mem:day32t4").contains("MODE=PostgreSQL").contains("DATABASE_TO_LOWER=TRUE");
    }

    @Test
    void credentials() {
        assertThat(env.getProperty("spring.datasource.username")).isEqualTo("sa");
    }

    @Test
    void hibernateCreatesAndDropsSchema() {
        assertThat(env.getProperty("spring.jpa.hibernate.ddl-auto")).isEqualTo("create-drop");
        Integer n = jdbc.queryForObject("select count(*) from information_schema.tables where table_name = 'notes'", Integer.class);
        assertThat(n).isEqualTo(1);
    }

    @Test
    void openInViewDisabled() {
        assertThat(env.getProperty("spring.jpa.open-in-view", Boolean.class)).isFalse();
    }

    @Test
    void sqlLoggingAndFormatting() {
        assertThat(env.getProperty("spring.jpa.show-sql", Boolean.class)).isTrue();
        assertThat(env.getProperty("spring.jpa.properties.hibernate.format_sql", Boolean.class)).isTrue();
        assertThat(env.getProperty("spring.jpa.properties.hibernate.jdbc.time_zone")).isEqualTo("UTC");
    }

    @Test
    void repositoryWorksAgainstConfiguredDatabase() {
        Note n = repository.save(new Note("hello"));
        assertThat(repository.findById(n.getId())).isPresent();
    }
}
