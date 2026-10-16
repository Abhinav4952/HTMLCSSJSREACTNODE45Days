package com.javaprep.day41.task01;

import static org.assertj.core.api.Assertions.assertThat;

import ch.qos.logback.classic.Level;
import ch.qos.logback.classic.Logger;
import ch.qos.logback.classic.spi.ILoggingEvent;
import ch.qos.logback.core.read.ListAppender;
import java.util.List;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.slf4j.LoggerFactory;

class LoggingContractTest {

    Logger logger;
    ListAppender<ILoggingEvent> appender;
    OrderProcessor processor = new OrderProcessor();

    @BeforeEach
    void attach() {
        logger = (Logger) LoggerFactory.getLogger(OrderProcessor.class);
        logger.setLevel(Level.INFO);
        appender = new ListAppender<>();
        appender.start();
        logger.addAppender(appender);
    }

    @AfterEach
    void detach() {
        logger.detachAppender(appender);
        logger.setLevel(null);
    }

    private List<ILoggingEvent> events() {
        return appender.list;
    }

    @Test
    void normalOrderLogsOneInfoLineWithParameters() {
        assertThat(processor.process("A-1", 50.0)).isTrue();
        assertThat(events()).hasSize(1);
        ILoggingEvent e = events().get(0);
        assertThat(e.getLevel()).isEqualTo(Level.INFO);
        assertThat(e.getMessage()).isEqualTo("Processing order {} (amount={})");
        assertThat(e.getArgumentArray()).containsExactly("A-1", 50.0);
        assertThat(e.getFormattedMessage()).isEqualTo("Processing order A-1 (amount=50.0)");
    }

    @Test
    void largeOrdersWarn() {
        processor.process("B-2", 5000.0);
        assertThat(events()).extracting(ILoggingEvent::getLevel).containsExactly(Level.INFO, Level.WARN);
        assertThat(events().get(1).getFormattedMessage()).isEqualTo("Large order B-2");
    }

    @Test
    void invalidAmountLogsErrorWithStackTraceAndReturnsFalse() {
        assertThat(processor.process("C-3", 0)).isFalse();
        ILoggingEvent e = events().get(1);
        assertThat(e.getLevel()).isEqualTo(Level.ERROR);
        assertThat(e.getFormattedMessage()).isEqualTo("Invalid amount for order C-3");
        assertThat(e.getThrowableProxy()).isNotNull();
        assertThat(e.getThrowableProxy().getMessage()).isEqualTo("amount must be positive");
    }

    @Test
    void debugLineOnlyWhenDebugIsEnabled() {
        processor.process("D-4", 10);
        assertThat(events()).noneMatch(e -> e.getLevel() == Level.DEBUG);
        events().clear();
        logger.setLevel(Level.DEBUG);
        processor.process("D-4", 10);
        assertThat(events()).extracting(ILoggingEvent::getFormattedMessage).contains("Order D-4 validated");
    }

    @Test
    void messagesAreTemplatesNotConcatenated() {
        processor.process("E-5", 1);
        assertThat(events()).allSatisfy(e -> assertThat(e.getMessage()).doesNotContain("E-5"));
    }
}
