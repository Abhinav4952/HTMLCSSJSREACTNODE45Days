package com.javaprep.day31.task03;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.lang.reflect.Constructor;
import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class TodoServiceTest {

    TodoRepository repo;
    TodoService service;

    @BeforeEach
    void setUp() {
        repo = new TodoRepository();
        service = new TodoService(repo);
    }

    @Test
    void createTrimsAndStartsOpen() {
        TodoDto dto = service.create("  Write tests ");
        assertThat(dto.id()).isEqualTo(1);
        assertThat(dto.title()).isEqualTo("Write tests");
        assertThat(dto.status()).isEqualTo("OPEN");
    }

    @Test
    void blankTitleRejected() {
        assertThatThrownBy(() -> service.create("  ")).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> service.create(null)).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void duplicateIgnoringCaseRejected() {
        service.create("Milk");
        assertThatThrownBy(() -> service.create(" milk ")).isInstanceOf(DuplicateTodoException.class);
    }

    @Test
    void completeFlow() {
        service.create("A");
        assertThat(service.complete(1).status()).isEqualTo("DONE");
        assertThatThrownBy(() -> service.complete(1)).isInstanceOf(IllegalStateException.class);
        assertThatThrownBy(() -> service.complete(99)).isInstanceOf(TodoNotFoundException.class);
    }

    @Test
    void listCanFilterOpen() {
        service.create("A");
        service.create("B");
        service.complete(1);
        assertThat(service.list(false)).hasSize(2);
        List<TodoDto> open = service.list(true);
        assertThat(open).extracting(TodoDto::title).containsExactly("B");
    }

    @Test
    void controllerDependsOnServiceOnly() {
        Constructor<?>[] ctors = TodoController.class.getDeclaredConstructors();
        assertThat(ctors).hasSize(1);
        assertThat(ctors[0].getParameterTypes()).containsExactly(TodoService.class);
    }
}
