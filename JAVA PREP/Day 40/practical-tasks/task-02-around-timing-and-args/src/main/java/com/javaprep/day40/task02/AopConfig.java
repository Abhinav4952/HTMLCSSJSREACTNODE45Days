package com.javaprep.day40.task02;

import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.EnableAspectJAutoProxy;

/** PROVIDED: enables @AspectJ support and scans this package for services and aspects. */
@Configuration
@EnableAspectJAutoProxy
@ComponentScan(basePackageClasses = AopConfig.class)
public class AopConfig {
}
