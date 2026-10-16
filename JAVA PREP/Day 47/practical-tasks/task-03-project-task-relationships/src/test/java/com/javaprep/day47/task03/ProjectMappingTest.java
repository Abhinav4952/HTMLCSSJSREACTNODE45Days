package com.javaprep.day47.task03;

import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.boot.test.autoconfigure.orm.jpa.TestEntityManager;

@DataJpaTest
class ProjectMappingTest {

    @Autowired
    private TestEntityManager em;
    @Autowired
    private ProjectRepository projects;

    private Project persistProject(User owner, String name, String... taskTitles) {
        Project p = new Project(name, owner);
        for (String t : taskTitles) {
            p.addTask(new TaskItem(t));
        }
        em.persist(p);
        em.flush();
        em.clear();
        return p;
    }

    private long taskRows() {
        return em.getEntityManager().createQuery("select count(t) from TaskItem t", Long.class).getSingleResult();
    }

    @Test
    void tasksArePersistedWithTheProjectAndReloaded() {
        User owner = em.persist(new User("a@x.io", "hash", "A"));
        Project p = persistProject(owner, "Apollo", "design", "build");
        Project loaded = projects.findById(p.getId()).orElseThrow();
        assertThat(loaded.getTasks()).extracting(TaskItem::getTitle).containsExactlyInAnyOrder("design", "build");
        assertThat(loaded.getTasks().get(0).getProject().getId()).isEqualTo(p.getId());
        assertThat(loaded.getOwner().getId()).isEqualTo(owner.getId());
    }

    @Test
    void removingATaskDeletesItsRow() {
        User owner = em.persist(new User("a@x.io", "hash", "A"));
        Project p = persistProject(owner, "Apollo", "design", "build");
        Project loaded = projects.findById(p.getId()).orElseThrow();
        loaded.removeTask(loaded.getTasks().get(0));
        em.flush();
        em.clear();
        assertThat(taskRows()).isEqualTo(1);
    }

    @Test
    void deletingTheProjectDeletesItsTasks() {
        User owner = em.persist(new User("a@x.io", "hash", "A"));
        Project p = persistProject(owner, "Apollo", "design", "build");
        projects.delete(projects.findById(p.getId()).orElseThrow());
        em.flush();
        assertThat(taskRows()).isZero();
    }

    @Test
    void projectsCanBeFoundByOwner() {
        User a = em.persist(new User("a@x.io", "hash", "A"));
        User b = em.persist(new User("b@x.io", "hash", "B"));
        persistProject(a, "A1");
        persistProject(a, "A2");
        persistProject(b, "B1");
        assertThat(projects.findByOwnerId(a.getId())).extracting(Project::getName).containsExactlyInAnyOrder("A1", "A2");
        assertThat(projects.findByOwnerId(b.getId())).hasSize(1);
    }
}
