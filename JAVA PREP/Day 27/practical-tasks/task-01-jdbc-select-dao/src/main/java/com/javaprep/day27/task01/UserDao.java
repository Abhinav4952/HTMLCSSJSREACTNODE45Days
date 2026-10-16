package com.javaprep.day27.task01;

import java.util.List;
import java.util.Optional;
import javax.sql.DataSource;

/** Table: users(id BIGINT PK, name VARCHAR, email VARCHAR). */
public class UserDao {

    private final DataSource dataSource;

    public UserDao(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    /** Empty Optional when no row matches. Use try-with-resources for Connection/Statement/ResultSet. */
    public Optional<User> findById(long id) {
        // TODO(Day27-task01): SELECT id, name, email FROM users WHERE id = ? using PreparedStatement
        throw new UnsupportedOperationException("TODO(Day27-task01): implement findById");
    }

    /** All users ordered by id ascending. */
    public List<User> findAll() {
        // TODO(Day27-task01): SELECT all users ordered by id; map each row with a private mapRow helper
        throw new UnsupportedOperationException("TODO(Day27-task01): implement findAll");
    }

    public long count() {
        // TODO(Day27-task01): SELECT COUNT(*) FROM users
        throw new UnsupportedOperationException("TODO(Day27-task01): implement count");
    }
}
