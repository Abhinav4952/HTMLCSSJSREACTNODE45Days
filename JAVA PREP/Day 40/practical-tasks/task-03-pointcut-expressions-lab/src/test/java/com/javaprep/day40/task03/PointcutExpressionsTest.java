package com.javaprep.day40.task03;

import static org.assertj.core.api.Assertions.assertThat;

import com.javaprep.day40.task03.sample.OrderService;
import com.javaprep.day40.task03.sample.UserService;
import com.javaprep.day40.task03.sample.web.UserController;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.List;
import org.junit.jupiter.api.Test;
import org.springframework.aop.aspectj.AspectJExpressionPointcut;

class PointcutExpressionsTest {

    record Target(Class<?> type, String method, Class<?>... params) {
        Method resolve() throws Exception {
            return type.getMethod(method, params);
        }

        @Override
        public String toString() {
            return type.getSimpleName() + "." + method;
        }
    }

    static final List<Target> ALL = List.of(
            new Target(UserService.class, "find", long.class),
            new Target(UserService.class, "save", String.class),
            new Target(UserService.class, "count"),
            new Target(OrderService.class, "place", String.class, int.class),
            new Target(OrderService.class, "cancel", long.class),
            new Target(UserController.class, "get", long.class),
            new Target(UserController.class, "save", String.class));

    private static List<String> matched(String expression) throws Exception {
        AspectJExpressionPointcut pc = new AspectJExpressionPointcut();
        pc.setExpression(expression);
        List<String> out = new ArrayList<>();
        for (Target t : ALL) {
            if (pc.matches(t.resolve(), t.type())) {
                out.add(t.toString());
            }
        }
        return out;
    }

    @Test
    void allInServices() throws Exception {
        assertThat(matched(PointcutExpressions.allInServices())).containsExactly(
                "UserService.find", "UserService.save", "UserService.count", "OrderService.place", "OrderService.cancel");
    }

    @Test
    void saveWithString() throws Exception {
        assertThat(matched(PointcutExpressions.saveWithString())).containsExactly("UserService.save", "UserController.save");
    }

    @Test
    void twoArguments() throws Exception {
        assertThat(matched(PointcutExpressions.twoArguments())).containsExactly("OrderService.place");
    }

    @Test
    void webLayer() throws Exception {
        assertThat(matched(PointcutExpressions.webLayer())).containsExactly("UserController.get", "UserController.save");
    }

    @Test
    void audited() throws Exception {
        assertThat(matched(PointcutExpressions.audited())).containsExactly("UserService.save");
    }

    @Test
    void serviceLayerOnly() throws Exception {
        assertThat(matched(PointcutExpressions.serviceLayerOnly())).containsExactly(
                "UserService.find", "UserService.save", "UserService.count", "OrderService.place", "OrderService.cancel");
    }
}
