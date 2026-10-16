package com.javaprep.day07.task01;

import static org.assertj.core.api.Assertions.*;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import org.assertj.core.data.Offset;

class TemperatureConverterTest {

    private static final Offset<Double> EPS = Offset.offset(1e-9);

    @Test
    @DisplayName("celsius -> fahrenheit")
    void cToF() {
        assertThat(TemperatureConverter.celsiusToFahrenheit(0)).isCloseTo(32.0, EPS);
        assertThat(TemperatureConverter.celsiusToFahrenheit(100)).isCloseTo(212.0, EPS);
        assertThat(TemperatureConverter.celsiusToFahrenheit(-40)).isCloseTo(-40.0, EPS);
        assertThat(TemperatureConverter.celsiusToFahrenheit(37)).isCloseTo(98.6, EPS);
    }

    @Test
    @DisplayName("fahrenheit -> celsius")
    void fToC() {
        assertThat(TemperatureConverter.fahrenheitToCelsius(32)).isCloseTo(0.0, EPS);
        assertThat(TemperatureConverter.fahrenheitToCelsius(212)).isCloseTo(100.0, EPS);
        assertThat(TemperatureConverter.fahrenheitToCelsius(-40)).isCloseTo(-40.0, EPS);
        assertThat(TemperatureConverter.fahrenheitToCelsius(50)).isCloseTo(10.0, EPS);
    }
}
