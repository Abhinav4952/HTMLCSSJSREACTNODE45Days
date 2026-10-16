package com.javaprep.day35.task01;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.Map;
import org.hibernate.SessionFactory;
import org.hibernate.stat.Statistics;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.boot.test.autoconfigure.orm.jpa.TestEntityManager;
import org.springframework.context.annotation.Import;

@DataJpaTest
@Import(AuthorReport.class)
class NPlusOneTest {

    @Autowired
    TestEntityManager em;
    @Autowired
    AuthorReport report;

    Statistics stats;

    @BeforeEach
    void seed() {
        for (int i = 1; i <= 5; i++) {
            Author a = new Author("author" + i);
            for (int j = 1; j <= 3; j++) {
                a.addBook(new Book("book" + i + "-" + j));
            }
            em.persist(a);
        }
        em.flush();
        em.clear();
        stats = em.getEntityManager().getEntityManagerFactory().unwrap(SessionFactory.class).getStatistics();
        stats.clear();
    }

    @Test
    void naiveVersionExecutesNPlusOneStatements() {
        Map<String, Integer> counts = report.bookCountsNaive();
        assertThat(counts).hasSize(5).containsEntry("author1", 3);
        assertThat(stats.getPrepareStatementCount()).isEqualTo(6);
    }

    @Test
    void joinFetchUsesOneStatement() {
        Map<String, Integer> counts = report.bookCountsJoinFetch();
        assertThat(counts).hasSize(5).containsEntry("author3", 3);
        assertThat(stats.getPrepareStatementCount()).isEqualTo(1);
    }

    @Test
    void entityGraphUsesOneStatement() {
        Map<String, Integer> counts = report.bookCountsEntityGraph();
        assertThat(counts).hasSize(5).containsEntry("author5", 3);
        assertThat(stats.getPrepareStatementCount()).isEqualTo(1);
    }

    @Test
    void bothOptimizedVersionsAgree() {
        assertThat(report.bookCountsJoinFetch()).isEqualTo(report.bookCountsEntityGraph());
    }
}
