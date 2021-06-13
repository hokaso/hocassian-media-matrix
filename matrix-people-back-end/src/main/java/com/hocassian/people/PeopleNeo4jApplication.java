package com.hocassian.people;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.security.servlet.SecurityAutoConfiguration;

/**
 * @author Hocassian
 */
@SpringBootApplication
@MapperScan(basePackages = { "com.hocassian.people.mapper"})
public class PeopleNeo4jApplication {

    public static void main(String[] args) {
        SpringApplication.run(PeopleNeo4jApplication.class, args);
    }

}
