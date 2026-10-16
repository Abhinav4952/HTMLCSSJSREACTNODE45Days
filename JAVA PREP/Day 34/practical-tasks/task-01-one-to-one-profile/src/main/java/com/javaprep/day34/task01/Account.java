package com.javaprep.day34.task01;

import jakarta.persistence.*;
import java.util.*;

/** One account owns exactly one profile (FK column profile_id on accounts). */
@Entity
@Table(name = "accounts")
public class Account {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String email;

    // TODO(Day34-task01): owning side of a one-to-one: LAZY, cascade ALL, orphanRemoval, join column profile_id
    private Profile profile;

    protected Account() {
    }

    public Account(String email) {
        this.email = email;
    }

    public Long getId() {
        return id;
    }

    public String getEmail() {
        return email;
    }

    public Profile getProfile() {
        return profile;
    }

    public void setProfile(Profile profile) {
        this.profile = profile;
    }
}
