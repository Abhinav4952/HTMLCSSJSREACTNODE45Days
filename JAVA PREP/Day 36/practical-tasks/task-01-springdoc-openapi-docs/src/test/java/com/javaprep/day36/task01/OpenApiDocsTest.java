package com.javaprep.day36.task01;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
class OpenApiDocsTest {

    @Autowired
    MockMvc mvc;

    @Test
    void docsAreServed() throws Exception {
        mvc.perform(get("/v3/api-docs")).andExpect(status().isOk()).andExpect(jsonPath("$.openapi").exists());
    }

    @Test
    void infoBlock() throws Exception {
        mvc.perform(get("/v3/api-docs")).andExpect(jsonPath("$.info.title").value("Items API"))
                .andExpect(jsonPath("$.info.version").value("1.0.0")).andExpect(jsonPath("$.info.description").value("Demo catalogue API"));
    }

    @Test
    void controllerIsGroupedUnderTag() throws Exception {
        mvc.perform(get("/v3/api-docs")).andExpect(jsonPath("$.paths['/api/items'].get.tags[0]").value("Items"))
                .andExpect(jsonPath("$.tags[?(@.name=='Items')].description").value("Item catalogue"));
    }

    @Test
    void operationsHaveSummaries() throws Exception {
        mvc.perform(get("/v3/api-docs")).andExpect(jsonPath("$.paths['/api/items'].get.summary").value("List all items"))
                .andExpect(jsonPath("$.paths['/api/items/{id}'].get.summary").value("Find an item by id"));
    }

    @Test
    void notFoundResponseIsDocumented() throws Exception {
        mvc.perform(get("/v3/api-docs")).andExpect(jsonPath("$.paths['/api/items/{id}'].get.responses['404'].description").value("Item not found"))
                .andExpect(jsonPath("$.paths['/api/items/{id}'].get.responses['200'].description").value("Item found"));
    }

    @Test
    void schemaFieldsAreDocumented() throws Exception {
        mvc.perform(get("/v3/api-docs")).andExpect(jsonPath("$.components.schemas.Item.properties.name.description").value("Display name"))
                .andExpect(jsonPath("$.components.schemas.Item.properties.name.example").value("Laptop"))
                .andExpect(jsonPath("$.components.schemas.Item.properties.price.description").value("Price in euro"));
    }
}
