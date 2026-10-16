package com.javaprep.day34.task03;

import jakarta.persistence.*;
import java.util.*;

@Entity
@Table(name = "courses")
public class Course {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String code;

    private String title;

    // TODO(Day34-task03): inverse side: mappedBy courses
    private Set<Student> students = new HashSet<>();

    protected Course() {
    }

    public Course(String code, String title) {
        this.code = code;
        this.title = title;
    }

    public Long getId() {
        return id;
    }

    public String getCode() {
        return code;
    }

    public String getTitle() {
        return title;
    }

    public Set<Student> getStudents() {
        return students;
    }

    /** Business-key equality: two courses are equal when their codes are equal (and non-null). */
    @Override
    public boolean equals(Object o) {
        // TODO(Day34-task03): equal when same class and equal code
        throw new UnsupportedOperationException("TODO(Day34-task03): equal when same class and equal code");
    }

    @Override
    public int hashCode() {
        // TODO(Day34-task03): consistent with equals (use the code)
        throw new UnsupportedOperationException("TODO(Day34-task03): consistent with equals (use the code)");
    }
}
