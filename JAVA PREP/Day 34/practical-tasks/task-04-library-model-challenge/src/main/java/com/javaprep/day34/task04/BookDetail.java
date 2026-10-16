package com.javaprep.day34.task04;

import jakarta.persistence.*;
import java.util.*;

@Entity
@Table(name = "book_details")
public class BookDetail {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private int pages;

    protected BookDetail() {
    }

    public BookDetail(int pages) {
        this.pages = pages;
    }

    public Long getId() {
        return id;
    }

    public int getPages() {
        return pages;
    }
}
