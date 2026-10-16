package com.javaprep.day35.task04;

import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.jdbc.core.JdbcTemplate;

@SpringBootTest
class FlywayMigrationTest {

    @Autowired
    ArticleRepository repository;
    @Autowired
    JdbcTemplate jdbc;

    @org.junit.jupiter.api.BeforeEach
    void clean() {
        repository.deleteAll();
    }

    @Test
    void bothMigrationsWereApplied() {
        Integer applied = jdbc.queryForObject("select count(*) from flyway_schema_history where success = true and \"version\" is not null", Integer.class);
        assertThat(applied).isEqualTo(2);
        String versions = jdbc.queryForList("select \"version\" from flyway_schema_history where \"version\" is not null order by installed_rank", String.class).toString();
        assertThat(versions).isEqualTo("[1, 2]");
    }

    @Test
    void hibernateOnlyValidatesBecauseFlywayOwnsTheSchema() {
        assertThat(repository.count()).isZero();
    }

    @Test
    void statusColumnDefaultsToDraft() {
        jdbc.update("insert into articles(title) values ('From SQL')");
        Article a = repository.findAll().get(0);
        assertThat(a.getStatus()).isEqualTo("DRAFT");
    }

    @Test
    void entityRoundTrip() {
        Article a = new Article("Hello");
        a.publish();
        Article saved = repository.saveAndFlush(a);
        assertThat(repository.findById(saved.getId()).orElseThrow().getStatus()).isEqualTo("PUBLISHED");
    }
}
