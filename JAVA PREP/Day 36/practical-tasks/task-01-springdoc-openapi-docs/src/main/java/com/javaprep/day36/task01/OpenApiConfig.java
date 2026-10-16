package com.javaprep.day36.task01;

import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Info;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class OpenApiConfig {

    /** Title "Items API", version "1.0.0", description "Demo catalogue API". */
    @Bean
    public OpenAPI itemsOpenApi() {
        // TODO(Day36-task01): build an OpenAPI with an Info(title, version, description)
        throw new UnsupportedOperationException("TODO(Day36-task01): build an OpenAPI with an Info(title, version, description)");
    }
}
