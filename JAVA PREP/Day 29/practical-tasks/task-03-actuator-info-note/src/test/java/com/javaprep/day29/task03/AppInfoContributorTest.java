package com.javaprep.day29.task03;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.Map;
import org.junit.jupiter.api.Test;
import org.springframework.boot.actuate.info.Info;

class AppInfoContributorTest {

    @Test
    void contributesAppSection() {
        Info.Builder builder = new Info.Builder();
        new AppInfoContributor("demo", "1.2.3").contribute(builder);
        Info info = builder.build();
        assertThat(info.get("app")).isEqualTo(Map.of("name", "demo", "version", "1.2.3"));
    }

    @Test
    void keepsExistingDetails() {
        Info.Builder builder = new Info.Builder().withDetail("git", "abc");
        new AppInfoContributor("demo", "1").contribute(builder);
        assertThat(builder.build().getDetails()).containsKeys("git", "app");
    }

    @Test
    void endpointAndExposureProperties() {
        assertThat(AppInfoContributor.infoEndpointPath()).isEqualTo("/actuator/info");
        assertThat(AppInfoContributor.exposureProperty()).isEqualTo("management.endpoints.web.exposure.include=health,info");
    }
}
