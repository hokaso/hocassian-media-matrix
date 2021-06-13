package com.hocassian.people.utils;

import org.neo4j.driver.Record;
import org.neo4j.driver.Value;
import org.neo4j.driver.types.Entity;
import org.neo4j.driver.types.Node;
import org.neo4j.driver.types.Path;
import org.neo4j.driver.types.Relationship;
import org.neo4j.driver.util.Pair;

import java.util.List;
import java.util.Map;
import java.util.function.Function;

/**
 * 功能描述：
 *
 * @author Hocassian
 * @date 2021-01-17 15:02
 */
public class BatisRecords implements Record {


//    public BatisRecords() {
//
//    }

    @Override
    public List<String> keys() {
        return null;
    }

    @Override
    public List<Value> values() {
        return null;
    }

    @Override
    public boolean containsKey(String s) {
        return false;
    }

    @Override
    public int index(String s) {
        return 0;
    }

    @Override
    public Value get(String s) {
        return null;
    }

    @Override
    public Value get(int i) {
        return null;
    }

    @Override
    public int size() {
        return 0;
    }

    @Override
    public Map<String, Object> asMap() {
        return null;
    }

    @Override
    public <T> Map<String, T> asMap(Function<Value, T> function) {
        return null;
    }

    @Override
    public List<Pair<String, Value>> fields() {
        return null;
    }

    @Override
    public Value get(String s, Value value) {
        return null;
    }

    @Override
    public Object get(String s, Object o) {
        return null;
    }

    @Override
    public Number get(String s, Number number) {
        return null;
    }

    @Override
    public Entity get(String s, Entity entity) {
        return null;
    }

    @Override
    public Node get(String s, Node node) {
        return null;
    }

    @Override
    public Path get(String s, Path path) {
        return null;
    }

    @Override
    public Relationship get(String s, Relationship relationship) {
        return null;
    }

    @Override
    public List<Object> get(String s, List<Object> list) {
        return null;
    }

    @Override
    public <T> List<T> get(String s, List<T> list, Function<Value, T> function) {
        return null;
    }

    @Override
    public Map<String, Object> get(String s, Map<String, Object> map) {
        return null;
    }

    @Override
    public <T> Map<String, T> get(String s, Map<String, T> map, Function<Value, T> function) {
        return null;
    }

    @Override
    public int get(String s, int i) {
        return 0;
    }

    @Override
    public long get(String s, long l) {
        return 0;
    }

    @Override
    public boolean get(String s, boolean b) {
        return false;
    }

    @Override
    public String get(String s, String s1) {
        return null;
    }

    @Override
    public float get(String s, float v) {
        return 0;
    }

    @Override
    public double get(String s, double v) {
        return 0;
    }
}
