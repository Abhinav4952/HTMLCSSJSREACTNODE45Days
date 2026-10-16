package com.javaprep.day47.task03;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

@Entity
@Table(name = "projects")
public class Project {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String name;

    // TODO(Day47-task03): map the owner: many projects belong to one User -> @ManyToOne(fetch = LAZY, optional = false) + @JoinColumn(name = "owner_id")
    private User owner;

    // TODO(Day47-task03): one project has many tasks -> @OneToMany(mappedBy = "project", cascade = ALL, orphanRemoval = true)
    private List<TaskItem> tasks = new ArrayList<>();

    protected Project() {
    }

    public Project(String name, User owner) {
        this.name = name;
        this.owner = owner;
    }

    public Long getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public User getOwner() {
        return owner;
    }

    public List<TaskItem> getTasks() {
        return Collections.unmodifiableList(tasks);
    }

    /** Keeps BOTH sides of the relationship in sync (adds to the list and sets task.project). */
    public void addTask(TaskItem task) {
        // TODO(Day47-task03): tasks.add(task); task.setProject(this);
        throw new UnsupportedOperationException("TODO(Day47-task03): implement addTask");
    }

    /** Removes the task from the list and clears task.project so orphanRemoval deletes the row. */
    public void removeTask(TaskItem task) {
        // TODO(Day47-task03): tasks.remove(task); task.setProject(null);
        throw new UnsupportedOperationException("TODO(Day47-task03): implement removeTask");
    }
}
