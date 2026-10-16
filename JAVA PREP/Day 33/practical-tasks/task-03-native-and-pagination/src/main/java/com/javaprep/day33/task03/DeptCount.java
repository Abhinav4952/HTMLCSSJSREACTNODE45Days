package com.javaprep.day33.task03;

/** Projection for the native query (aliases: department, headcount). */
public interface DeptCount {
    String getDepartment();

    long getHeadcount();
}
