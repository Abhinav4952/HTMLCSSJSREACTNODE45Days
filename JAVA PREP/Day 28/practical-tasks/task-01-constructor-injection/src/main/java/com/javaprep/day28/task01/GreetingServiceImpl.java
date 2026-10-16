package com.javaprep.day28.task01;

// TODO(Day28-task01): register this class as a Spring bean with a stereotype annotation (@Service)
public class GreetingServiceImpl implements GreetingService {

    private final MessageRepository repository;

    // Single constructor => Spring injects the MessageRepository bean automatically (no @Autowired needed).
    public GreetingServiceImpl(MessageRepository repository) {
        this.repository = repository;
    }

    /** "<prefix>, <name>!" e.g. "Hello, Ada!". Blank or null name -> IllegalArgumentException. */
    @Override
    public String greet(String name) {
        // TODO(Day28-task01): use the injected repository and validate the name
        throw new UnsupportedOperationException("TODO(Day28-task01): implement greet");
    }
}
