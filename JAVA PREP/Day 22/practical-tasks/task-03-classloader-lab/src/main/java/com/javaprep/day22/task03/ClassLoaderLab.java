package com.javaprep.day22.task03;

import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/** Class loading experiments. */
public final class ClassLoaderLab {

    private ClassLoaderLab() {
    }

    /** Child-first loader for the registered class names; everything else is delegated to the parent. */
    public static final class IsolatedLoader extends ClassLoader {
        private final Map<String, byte[]> classes;

        public IsolatedLoader(ClassLoader parent, Map<String, byte[]> classes) {
            super(parent);
            this.classes = Map.copyOf(classes);
        }

        @Override
        protected Class<?> loadClass(String name, boolean resolve) throws ClassNotFoundException {
            // TODO(Day22-task03): synchronized (getClassLoadingLock(name)): when name is registered use findLoadedClass or defineClass(name, bytes, 0, length) (child-first); otherwise return super.loadClass(name, resolve)
            throw new UnsupportedOperationException("TODO(Day22-task03): loadClass");
        }
    }

    public static byte[] bytesOf(Class<?> type) {
        // TODO(Day22-task03): type.getResourceAsStream('/' + name with dots replaced by slashes + '.class'); null stream -> IllegalArgumentException; read all bytes, wrap IOException in UncheckedIOException
        throw new UnsupportedOperationException("TODO(Day22-task03): bytesOf");
    }

    public static String loaderName(Class<?> type) {
        // TODO(Day22-task03): getClassLoader() == null -> 'bootstrap'; loader.getName() when not null; else the loader's getClass().getSimpleName()
        throw new UnsupportedOperationException("TODO(Day22-task03): loaderName");
    }

    public static List<String> loaderChain(ClassLoader loader) {
        // TODO(Day22-task03): walk getParent() from the given loader collecting a name per loader (same naming rule as loaderName), then append 'bootstrap'
        throw new UnsupportedOperationException("TODO(Day22-task03): loaderChain");
    }

    public static Object instantiate(Class<?> type) {
        // TODO(Day22-task03): type.getDeclaredConstructor().newInstance(); wrap ReflectiveOperationException in IllegalStateException keeping the cause
        throw new UnsupportedOperationException("TODO(Day22-task03): instantiate");
    }
}
