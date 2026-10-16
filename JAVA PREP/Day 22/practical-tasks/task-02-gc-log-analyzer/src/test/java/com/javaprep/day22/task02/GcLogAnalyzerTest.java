package com.javaprep.day22.task02;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.assertj.core.api.Assertions.within;

import java.util.List;
import java.util.OptionalLong;
import org.junit.jupiter.api.Test;

class GcLogAnalyzerTest {

    private static final String LOG = """
            [0.012s][info][gc] Using G1
            [1.500s][info][gc] GC(0) Pause Young (Normal) (G1 Evacuation Pause) 24M->4M(256M) 5.123ms
            this is not a gc line
            [2.750s][info][gc] GC(1) Pause Young (Concurrent Start) (G1 Humongous Allocation) 60M->20M(256M) 12.500ms

            [9.000s][info][gc         ] GC(2) Pause Full (System.gc()) 200M->50M(256M) 150.000ms
            [12.000s][info][gc] GC(3) Pause Young (Normal) (G1 Evacuation Pause) 120M->60M(256M) 7.000ms
            [20.000s][info][gc] GC(4) Pause Full (Allocation Failure) 250M->80M(256M) 220.500ms
            [30.000s][info][gc] GC(5) Pause Full (Allocation Failure) 250M->120M(256M) 300.000ms
            """;

    private static GcLogAnalyzer.GcEvent full(int id, long afterMb) {
        return new GcLogAnalyzer.GcEvent(id, id, "x", 250L << 20, afterMb << 20, 256L << 20, 100.0, true);
    }

    private static GcLogAnalyzer.GcEvent young(int id, long afterMb) {
        return new GcLogAnalyzer.GcEvent(id, id, "x", 100L << 20, afterMb << 20, 256L << 20, 5.0, false);
    }

    @Test
    void r1_parseSizeUnits() {
        assertThat(GcLogAnalyzer.parseSize("100")).isEqualTo(100L);
        assertThat(GcLogAnalyzer.parseSize("100B")).isEqualTo(100L);
        assertThat(GcLogAnalyzer.parseSize("512K")).isEqualTo(512L * 1024);
        assertThat(GcLogAnalyzer.parseSize("24M")).isEqualTo(24L * 1024 * 1024);
        assertThat(GcLogAnalyzer.parseSize("2g")).isEqualTo(2L * 1024 * 1024 * 1024);
        assertThat(GcLogAnalyzer.parseSize(" 8m ")).isEqualTo(8L * 1024 * 1024);
    }

    @Test
    void r1_parseSizeRejectsGarbage() {
        assertThatThrownBy(() -> GcLogAnalyzer.parseSize("12X")).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> GcLogAnalyzer.parseSize("M")).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> GcLogAnalyzer.parseSize("")).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> GcLogAnalyzer.parseSize(null)).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void r2_formatBytes() {
        assertThat(GcLogAnalyzer.formatBytes(0)).isEqualTo("0 B");
        assertThat(GcLogAnalyzer.formatBytes(512)).isEqualTo("512 B");
        assertThat(GcLogAnalyzer.formatBytes(1023)).isEqualTo("1023 B");
        assertThat(GcLogAnalyzer.formatBytes(1024)).isEqualTo("1.0 KiB");
        assertThat(GcLogAnalyzer.formatBytes(1536)).isEqualTo("1.5 KiB");
        assertThat(GcLogAnalyzer.formatBytes(2L * 1024 * 1024)).isEqualTo("2.0 MiB");
        assertThat(GcLogAnalyzer.formatBytes(1024L * 1024 * 1024)).isEqualTo("1.0 GiB");
        assertThat(GcLogAnalyzer.formatBytes(3L * 1024 * 1024 * 1024 * 1024)).isEqualTo("3.0 TiB");
        assertThatThrownBy(() -> GcLogAnalyzer.formatBytes(-1)).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void r3_parseLineExtractsAllFields() {
        var event = GcLogAnalyzer.parseLine("[2.345s][info][gc] GC(12) Pause Young (Normal) (G1 Evacuation Pause) 24M->4M(256M) 5.123ms").orElseThrow();
        assertThat(event.uptimeSeconds()).isCloseTo(2.345, within(1e-9));
        assertThat(event.gcId()).isEqualTo(12);
        assertThat(event.cause()).isEqualTo("(Normal) (G1 Evacuation Pause)");
        assertThat(event.beforeBytes()).isEqualTo(24L << 20);
        assertThat(event.afterBytes()).isEqualTo(4L << 20);
        assertThat(event.committedBytes()).isEqualTo(256L << 20);
        assertThat(event.pauseMillis()).isCloseTo(5.123, within(1e-9));
        assertThat(event.full()).isFalse();
    }

    @Test
    void r3_parseLineFullAndPaddedTag() {
        var event = GcLogAnalyzer.parseLine("[9.000s][info][gc         ] GC(2) Pause Full (System.gc()) 200M->50M(256M) 150.000ms").orElseThrow();
        assertThat(event.full()).isTrue();
        assertThat(event.cause()).isEqualTo("(System.gc())");
        assertThat(event.pauseMillis()).isCloseTo(150.0, within(1e-9));
    }

    @Test
    void r3_parseLineIgnoresOtherLines() {
        assertThat(GcLogAnalyzer.parseLine("[0.012s][info][gc] Using G1")).isEmpty();
        assertThat(GcLogAnalyzer.parseLine("")).isEmpty();
        assertThat(GcLogAnalyzer.parseLine(null)).isEmpty();
        assertThat(GcLogAnalyzer.parseLine("[1.0s][info][gc,heap] GC(1) Pause Young 1M->1M(2M) 1ms")).isEmpty();
    }

    @Test
    void r4_parseKeepsOrderAndSkipsNoise() {
        var events = GcLogAnalyzer.parse(LOG);
        assertThat(events).extracting(GcLogAnalyzer.GcEvent::gcId).containsExactly(0, 1, 2, 3, 4, 5);
        assertThat(GcLogAnalyzer.parse("")).isEmpty();
        assertThat(GcLogAnalyzer.parse(null)).isEmpty();
        assertThat(GcLogAnalyzer.parse("nothing here\nnor here")).isEmpty();
    }

    @Test
    void r5_summaryOfTheSampleLog() {
        var s = GcLogAnalyzer.summarize(GcLogAnalyzer.parse(LOG));
        assertThat(s.events()).isEqualTo(6);
        assertThat(s.fullGcs()).isEqualTo(3);
        assertThat(s.totalPauseMillis()).isCloseTo(5.123 + 12.5 + 150.0 + 7.0 + 220.5 + 300.0, within(1e-9));
        assertThat(s.maxPauseMillis()).isCloseTo(300.0, within(1e-9));
        // (24-4)+(60-20)+(200-50)+(120-60)+(250-80)+(250-120) MiB
        assertThat(s.reclaimedBytes()).isEqualTo((20L + 40 + 150 + 60 + 170 + 130) << 20);
    }

    @Test
    void r5_summaryOfNothing() {
        var s = GcLogAnalyzer.summarize(List.of());
        assertThat(s).isEqualTo(new GcLogAnalyzer.Summary(0, 0, 0.0, 0.0, 0L));
    }

    @Test
    void r6_leakDetectedOnRisingFloor() {
        // fulls: 50 -> 80 -> 120 MB (rising), with young GCs in between that must be ignored
        var events = List.of(full(1, 50), young(2, 10), full(3, 80), young(4, 5), full(5, 120));
        assertThat(GcLogAnalyzer.leakSuspected(events, 3)).isTrue();
        assertThat(GcLogAnalyzer.leakSuspected(events, 2)).isTrue();
        assertThat(GcLogAnalyzer.leakSuspected(events, 4)).isFalse();
    }

    @Test
    void r6_noLeakWhenFloorDropsOrPlateaus() {
        assertThat(GcLogAnalyzer.leakSuspected(List.of(full(1, 50), full(2, 80), full(3, 60), full(4, 90)), 3)).isFalse();
        assertThat(GcLogAnalyzer.leakSuspected(List.of(full(1, 50), full(2, 50), full(3, 50)), 2)).isFalse();
        assertThat(GcLogAnalyzer.leakSuspected(List.of(), 2)).isFalse();
        assertThat(GcLogAnalyzer.leakSuspected(List.of(young(1, 5), young(2, 9)), 2)).isFalse();
        assertThatThrownBy(() -> GcLogAnalyzer.leakSuspected(List.of(), 1)).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void r6_leakInTheSampleLog() {
        assertThat(GcLogAnalyzer.leakSuspected(GcLogAnalyzer.parse(LOG), 3)).as("50M -> 80M -> 120M after full GCs").isTrue();
    }

    @Test
    void r7_heapSettingsFromFlags() {
        var s = GcLogAnalyzer.heapSettings(List.of("-Xms512m", "-Xmx2g", "-XX:+UseZGC", "-Dfoo=bar"));
        assertThat(s.initialBytes()).isEqualTo(OptionalLong.of(512L << 20));
        assertThat(s.maxBytes()).isEqualTo(OptionalLong.of(2L << 30));
        assertThat(s.collector()).isEqualTo("ZGC");
    }

    @Test
    void r7_defaultsAndLastWins() {
        var none = GcLogAnalyzer.heapSettings(List.of("-Dx=y"));
        assertThat(none.initialBytes()).isEmpty();
        assertThat(none.maxBytes()).isEmpty();
        assertThat(none.collector()).isEqualTo("G1");
        var last = GcLogAnalyzer.heapSettings(List.of("-Xmx1g", "-XX:+UseSerialGC", "-Xmx4g", "-XX:+UseParallelGC"));
        assertThat(last.maxBytes()).isEqualTo(OptionalLong.of(4L << 30));
        assertThat(last.collector()).isEqualTo("Parallel");
    }

    @Test
    void r7_initialLargerThanMaxIsRejected() {
        assertThatThrownBy(() -> GcLogAnalyzer.heapSettings(List.of("-Xms4g", "-Xmx1g"))).isInstanceOf(IllegalArgumentException.class);
        assertThat(GcLogAnalyzer.heapSettings(List.of("-Xms1g", "-Xmx1g")).maxBytes()).isEqualTo(OptionalLong.of(1L << 30));
    }
}
