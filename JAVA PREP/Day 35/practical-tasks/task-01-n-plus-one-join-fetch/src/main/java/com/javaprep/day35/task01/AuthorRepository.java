package com.javaprep.day35.task01;

import java.util.List;
import org.springframework.data.jpa.repository.EntityGraph;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

public interface AuthorRepository extends JpaRepository<Author, Long> {

    // TODO(Day35-task01): declare two methods that load authors TOGETHER with their books in ONE statement:
    //   findAllWithBooks()  -> JPQL "select distinct a from Author a join fetch a.books"
    //   findAllWithGraph()  -> @EntityGraph(attributePaths = "books") + @Query("select distinct a from Author a")
}
