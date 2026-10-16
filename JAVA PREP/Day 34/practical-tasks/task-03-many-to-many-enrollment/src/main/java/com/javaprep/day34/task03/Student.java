package com.javaprep.day34.task03;

import jakarta.persistence.*;
import java.util.*;

@Entity
@Table(name = "students")
public class Student {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;

    // TODO(Day34-task03): owning side of the many-to-many: join table enrollments(student_id, course_id); NO cascade
    private Set<Course> courses = new HashSet<>();

    protected Student() {
    }

    public Student(String name) {
        this.name = name;
    }

    public Long getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public Set<Course> getCourses() {
        return courses;
    }

    public void enroll(Course course) {
        // TODO(Day34-task03): add to both sides
        throw new UnsupportedOperationException("TODO(Day34-task03): add to both sides");
    }

    public void drop(Course course) {
        // TODO(Day34-task03): remove from both sides
        throw new UnsupportedOperationException("TODO(Day34-task03): remove from both sides");
    }
}
