package com.javaprep.day22.task03;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.Test;

class ClassLoaderLabTest {

    private static final String PLUGIN = SamplePlugin.class.getName();

    private static ClassLoaderLab.IsolatedLoader newLoader() {
        return new ClassLoaderLab.IsolatedLoader(ClassLoaderLabTest.class.getClassLoader(),
                Map.of(PLUGIN, ClassLoaderLab.bytesOf(SamplePlugin.class)));
    }

    private static Object call(Object target, String method) throws Exception {
        return target.getClass().getMethod(method).invoke(target);
    }

    @Test
    void r1_bytesOfReturnsClassFileWithMagicNumber() {
        byte[] bytes = ClassLoaderLab.bytesOf(SamplePlugin.class);
        assertThat(bytes.length).isGreaterThan(100);
        assertThat(bytes[0] & 0xFF).isEqualTo(0xCA);
        assertThat(bytes[1] & 0xFF).isEqualTo(0xFE);
        assertThat(bytes[2] & 0xFF).isEqualTo(0xBA);
        assertThat(bytes[3] & 0xFF).isEqualTo(0xBE);
    }

    @Test
    void r2_registeredClassIsDefinedByTheIsolatedLoader() throws Exception {
        ClassLoaderLab.IsolatedLoader loader = newLoader();
        Class<?> loaded = loader.loadClass(PLUGIN);
        assertThat(loaded.getName()).isEqualTo(PLUGIN);
        assertThat(loaded.getClassLoader()).isSameAs(loader);
        assertThat(loaded).isNotSameAs(SamplePlugin.class);
        assertThat(loader.loadClass(PLUGIN)).as("defined only once per loader").isSameAs(loaded);
    }

    @Test
    void r2_otherClassesAreDelegatedToTheParent() throws Exception {
        ClassLoaderLab.IsolatedLoader loader = newLoader();
        assertThat(loader.loadClass("java.lang.String")).isSameAs(String.class);
        assertThat(loader.loadClass(ClassLoaderLab.class.getName())).isSameAs(ClassLoaderLab.class);
        assertThatThrownBy(() -> loader.loadClass("com.does.not.Exist")).isInstanceOf(ClassNotFoundException.class);
    }

    @Test
    void r2_sameBytesInTwoLoadersAreUnrelatedTypesWithSeparateStatics() throws Exception {
        Object a = ClassLoaderLab.instantiate(newLoader().loadClass(PLUGIN));
        Object b = ClassLoaderLab.instantiate(newLoader().loadClass(PLUGIN));
        assertThat(a.getClass()).isNotSameAs(b.getClass());
        assertThat(a.getClass().getName()).isEqualTo(b.getClass().getName());
        assertThat(a).isNotInstanceOf(SamplePlugin.class);
        assertThat(b.getClass().isInstance(a)).isFalse();
        assertThat(call(a, "next")).isEqualTo(1);
        assertThat(call(a, "next")).isEqualTo(2);
        assertThat(call(b, "next")).as("separate static counter").isEqualTo(1);
        assertThat(call(a, "greet")).isEqualTo("hello from plugin");
        SamplePlugin local = new SamplePlugin();
        assertThat(local.next()).as("the application's own copy is independent too").isEqualTo(1);
    }

    @Test
    void r3_loaderNames() {
        assertThat(ClassLoaderLab.loaderName(String.class)).isEqualTo("bootstrap");
        assertThat(ClassLoaderLab.loaderName(java.sql.Driver.class)).isEqualTo("platform");
        assertThat(ClassLoaderLab.loaderName(ClassLoaderLab.class)).isEqualTo(ClassLoaderLabTest.class.getClassLoader().getName() == null
                ? ClassLoaderLabTest.class.getClassLoader().getClass().getSimpleName()
                : ClassLoaderLabTest.class.getClassLoader().getName());
    }

    @Test
    void r3_loaderNameOfAnIsolatedClass() throws Exception {
        Class<?> loaded = newLoader().loadClass(PLUGIN);
        assertThat(ClassLoaderLab.loaderName(loaded)).isEqualTo("IsolatedLoader");
    }

    @Test
    void r4_loaderChainEndsAtBootstrap() {
        List<String> chain = ClassLoaderLab.loaderChain(newLoader());
        assertThat(chain).startsWith("IsolatedLoader").endsWith("platform", "bootstrap");
        assertThat(chain.size()).isGreaterThanOrEqualTo(4);
        assertThat(ClassLoaderLab.loaderChain(ClassLoader.getPlatformClassLoader())).containsExactly("platform", "bootstrap");
    }

    @Test
    void r5_instantiateWrapsFailures() {
        assertThat(ClassLoaderLab.instantiate(SamplePlugin.class)).isInstanceOf(SamplePlugin.class);
        assertThatThrownBy(() -> ClassLoaderLab.instantiate(Integer.class))
                .isInstanceOf(IllegalStateException.class)
                .hasCauseInstanceOf(ReflectiveOperationException.class);
        assertThatThrownBy(() -> ClassLoaderLab.instantiate(Runnable.class))
                .isInstanceOf(IllegalStateException.class);
    }
}
