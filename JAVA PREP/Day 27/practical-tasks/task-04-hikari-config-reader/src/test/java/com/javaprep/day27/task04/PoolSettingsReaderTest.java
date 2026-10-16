package com.javaprep.day27.task04;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;
import java.sql.Connection;
import java.util.Properties;
import org.junit.jupiter.api.Test;

class PoolSettingsReaderTest {

    private static Properties base() {
        Properties p = new Properties();
        p.setProperty("jdbcUrl", "jdbc:h2:mem:pool_test;DB_CLOSE_DELAY=-1");
        p.setProperty("username", "sa");
        p.setProperty("password", "s3cret");
        return p;
    }

    @Test
    void appliesDefaults() {
        PoolSettingsReader.PoolSettings s = PoolSettingsReader.read(base());
        assertThat(s.maximumPoolSize()).isEqualTo(10);
        assertThat(s.minimumIdle()).isEqualTo(10);
        assertThat(s.connectionTimeoutMs()).isEqualTo(30000);
        assertThat(s.username()).isEqualTo("sa");
    }

    @Test
    void readsExplicitValues() {
        Properties p = base();
        p.setProperty("maximumPoolSize", "5");
        p.setProperty("minimumIdle", "2");
        p.setProperty("connectionTimeoutMs", "1000");
        PoolSettingsReader.PoolSettings s = PoolSettingsReader.read(p);
        assertThat(s.maximumPoolSize()).isEqualTo(5);
        assertThat(s.minimumIdle()).isEqualTo(2);
        assertThat(s.connectionTimeoutMs()).isEqualTo(1000);
    }

    @Test
    void rejectsInvalidSettings() {
        Properties noUrl = new Properties();
        assertThatThrownBy(() -> PoolSettingsReader.read(noUrl)).isInstanceOf(IllegalArgumentException.class)
                .hasMessageContaining("jdbcUrl");
        Properties zero = base();
        zero.setProperty("maximumPoolSize", "0");
        assertThatThrownBy(() -> PoolSettingsReader.read(zero)).isInstanceOf(IllegalArgumentException.class)
                .hasMessageContaining("maximumPoolSize");
        Properties idle = base();
        idle.setProperty("maximumPoolSize", "3");
        idle.setProperty("minimumIdle", "4");
        assertThatThrownBy(() -> PoolSettingsReader.read(idle)).isInstanceOf(IllegalArgumentException.class)
                .hasMessageContaining("minimumIdle");
        Properties nan = base();
        nan.setProperty("maximumPoolSize", "many");
        assertThatThrownBy(() -> PoolSettingsReader.read(nan)).isInstanceOf(IllegalArgumentException.class);
        Properties timeout = base();
        timeout.setProperty("connectionTimeoutMs", "10");
        assertThatThrownBy(() -> PoolSettingsReader.read(timeout)).isInstanceOf(IllegalArgumentException.class)
                .hasMessageContaining("connectionTimeoutMs");
    }

    @Test
    void summaryNeverLeaksPassword() {
        PoolSettingsReader.PoolSettings s = PoolSettingsReader.read(base());
        String summary = PoolSettingsReader.maskedSummary(s);
        assertThat(summary).doesNotContain("s3cret").contains("password=****");
        assertThat(summary).isEqualTo("jdbcUrl=jdbc:h2:mem:pool_test;DB_CLOSE_DELAY=-1; user=sa; password=****; max=10; minIdle=10; timeoutMs=30000");
    }

    @Test
    void hikariConfigIsUsableToOpenAPool() throws Exception {
        Properties p = base();
        p.setProperty("maximumPoolSize", "2");
        p.setProperty("minimumIdle", "1");
        HikariConfig cfg = PoolSettingsReader.toHikariConfig(PoolSettingsReader.read(p));
        assertThat(cfg.getMaximumPoolSize()).isEqualTo(2);
        assertThat(cfg.getMinimumIdle()).isEqualTo(1);
        assertThat(cfg.getUsername()).isEqualTo("sa");
        try (HikariDataSource ds = new HikariDataSource(cfg); Connection c = ds.getConnection()) {
            assertThat(c.isValid(1)).isTrue();
        }
    }
}
