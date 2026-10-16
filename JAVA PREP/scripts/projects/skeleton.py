"""Shared Spring Boot skeleton writer for the JAVA PREP projects (Project 01, 02 and the Project 03 services)."""
from __future__ import annotations

from pathlib import Path

BOOT_VERSION = "3.4.1"


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip("\n") + "\n", encoding="utf-8")


def sub(s: str, **kw) -> str:
    for k, v in kw.items():
        s = s.replace(f"@@{k}@@", str(v))
    return s


POM_SINGLE = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <!-- Course target is Spring Boot 4 when available; the projects pin 3.4.x for reproducible builds. -->
  <parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>@@BOOT@@</version>
    <relativePath/>
  </parent>
  <groupId>com.javaprep.@@PKG@@</groupId>
  <artifactId>@@ARTIFACT@@</artifactId>
  <version>1.0.0-SNAPSHOT</version>
  <name>@@TITLE@@</name>
  <description>@@DESC@@</description>
  <properties>
    <java.version>21</java.version>
    <maven.compiler.release>21</maven.compiler.release>
  </properties>
  <dependencies>
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-data-jpa</artifactId>
    </dependency>
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-validation</artifactId>
    </dependency>
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-actuator</artifactId>
    </dependency>
    <dependency>
      <groupId>org.postgresql</groupId>
      <artifactId>postgresql</artifactId>
      <scope>runtime</scope>
    </dependency>
    <dependency>
      <groupId>com.h2database</groupId>
      <artifactId>h2</artifactId>
      <scope>test</scope>
    </dependency>
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-test</artifactId>
      <scope>test</scope>
    </dependency>
  </dependencies>
  <build>
    <plugins>
      <plugin>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-maven-plugin</artifactId>
      </plugin>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-surefire-plugin</artifactId>
        <configuration>
          <argLine>-Dnet.bytebuddy.experimental=true</argLine>
        </configuration>
      </plugin>
    </plugins>
  </build>
</project>
"""

APP_JAVA = """package com.javaprep.@@PKG@@;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class @@CLASS@@Application {

    public static void main(String[] args) {
        SpringApplication.run(@@CLASS@@Application.class, args);
    }
}
"""

WELCOME_JAVA = """package com.javaprep.@@PKG@@.web;

import java.util.LinkedHashMap;
import java.util.Map;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

/** Public welcome/health-style endpoint used to verify that the application and its wiring are alive. */
@RestController
public class WelcomeController {

    @GetMapping("/")
    public Map<String, Object> welcome() {
        Map<String, Object> body = new LinkedHashMap<>();
        body.put("application", "@@TITLE@@");
        body.put("status", "UP");
        body.put("hint", "See PROJECT_INSTRUCTIONS.md for the API contract; /actuator/health reports database status");
        return body;
    }
}
"""

HANDLER_JAVA = """package com.javaprep.@@PKG@@.web;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.NoSuchElementException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ProblemDetail;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

/**
 * Global error contract (RFC 9457 ProblemDetail). Extend it with your own domain exceptions
 * (e.g. 404 not found, 409 conflict, 403 forbidden) as you implement the milestones.
 */
@RestControllerAdvice
public class GlobalExceptionHandler {

    private static final Logger log = LoggerFactory.getLogger(GlobalExceptionHandler.class);

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ProblemDetail handleValidation(MethodArgumentNotValidException ex) {
        ProblemDetail pd = ProblemDetail.forStatusAndDetail(HttpStatus.BAD_REQUEST, "Validation failed");
        pd.setTitle("Bad Request");
        Map<String, String> errors = new LinkedHashMap<>();
        ex.getBindingResult().getFieldErrors().forEach(fe -> errors.putIfAbsent(fe.getField(), fe.getDefaultMessage()));
        pd.setProperty("errors", errors);
        return pd;
    }

    @ExceptionHandler(IllegalArgumentException.class)
    public ProblemDetail handleBadRequest(IllegalArgumentException ex) {
        ProblemDetail pd = ProblemDetail.forStatusAndDetail(HttpStatus.BAD_REQUEST, ex.getMessage());
        pd.setTitle("Bad Request");
        return pd;
    }

    @ExceptionHandler(NoSuchElementException.class)
    public ProblemDetail handleNotFound(NoSuchElementException ex) {
        ProblemDetail pd = ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, ex.getMessage());
        pd.setTitle("Not Found");
        return pd;
    }

    @ExceptionHandler(Exception.class)
    public ProblemDetail handleUnexpected(Exception ex) {
        log.error("Unexpected error", ex);
        ProblemDetail pd = ProblemDetail.forStatusAndDetail(HttpStatus.INTERNAL_SERVER_ERROR, "Unexpected error");
        pd.setTitle("Internal Server Error");
        return pd;
    }
}
"""

TEST_JAVA = """package com.javaprep.@@PKG@@;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.MockMvc;

/**
 * Smoke test: the application context starts against an in-memory H2 database (PostgreSQL mode),
 * so `mvn test` needs NO local PostgreSQL. The real database is only used when you run the application.
 */
@SpringBootTest(properties = {
        "spring.datasource.url=jdbc:h2:mem:@@DB@@;MODE=PostgreSQL;DB_CLOSE_DELAY=-1",
        "spring.datasource.username=sa",
        "spring.datasource.password=",
        "spring.jpa.hibernate.ddl-auto=none"
})
@AutoConfigureMockMvc
class ApplicationSmokeTest {

    @Autowired
    private MockMvc mvc;

    @Test
    void welcomeEndpointIsUp() throws Exception {
        mvc.perform(get("/")).andExpect(status().isOk()).andExpect(jsonPath("$.status").value("UP"));
    }
}
"""

APP_YML = """# Main configuration. Secrets and connection details come from the ENVIRONMENT (or application-local.yml, see README).
spring:
  application:
    name: @@APPNAME@@
  datasource:
    url: ${DB_URL}
    username: ${DB_USERNAME}
    password: ${DB_PASSWORD}
  jpa:
    hibernate:
      ddl-auto: validate        # the schema is owned by database/*.sql; Hibernate only VERIFIES it
    open-in-view: false
    properties:
      hibernate:
        jdbc:
          time_zone: UTC
server:
  port: @@PORT@@
management:
  endpoints:
    web:
      exposure:
        include: health,info
"""

LOCAL_EXAMPLE = """# Copy this file to application-local.yml (git-ignored) and adjust the values to YOUR machine.
# Activate it with: SPRING_PROFILES_ACTIVE=local   (or -Dspring-boot.run.profiles=local)
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/@@DB@@
    username: course_user
    password: change_me
"""


def write_service(base: Path, *, pkg: str, cls: str, artifact: str, title: str, desc: str, appname: str, db: str, port: int,
                  standalone_pom: bool = True, extra_main: dict | None = None, pom_override: str | None = None) -> None:
    kw = dict(BOOT=BOOT_VERSION, PKG=pkg, CLASS=cls, ARTIFACT=artifact, TITLE=title, DESC=desc, APPNAME=appname, DB=db, PORT=port)
    if standalone_pom:
        write(base / "pom.xml", sub(POM_SINGLE, **kw))
    elif pom_override:
        write(base / "pom.xml", sub(pom_override, **kw))
    jbase = base / "src/main/java/com/javaprep" / pkg.replace(".", "/")
    write(jbase / f"{cls}Application.java", sub(APP_JAVA, **kw))
    write(jbase / "web/WelcomeController.java", sub(WELCOME_JAVA, **kw))
    write(jbase / "web/GlobalExceptionHandler.java", sub(HANDLER_JAVA, **kw))
    for rel, content in (extra_main or {}).items():
        write(jbase / rel, sub(content, **kw))
    write(base / "src/main/resources/application.yml", sub(APP_YML, **kw))
    write(base / "src/main/resources/application-local.yml.example", sub(LOCAL_EXAMPLE, **kw))
    tbase = base / "src/test/java/com/javaprep" / pkg.replace(".", "/")
    write(tbase / "ApplicationSmokeTest.java", sub(TEST_JAVA, **kw))
