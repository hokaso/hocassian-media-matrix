package com.hocassian.people.service.web;


import com.hocassian.people.domain.web.ConnectWeb;
import com.hocassian.people.domain.web.PersonWeb;
import com.hocassian.people.mapper.web.ConnectWebMapper;
import com.hocassian.people.mapper.web.PersonWebMapper;
import com.hocassian.people.utils.SnowflakeIdWorker;
import org.neo4j.driver.Record;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * 功能描述：
 *
 * @author Hocassian
 * @date 2021-01-16 01:15
 */
@Service("webService")
public class WebService {


    @Autowired
    private PersonWebMapper personWebMapper;

    @Autowired
    private ConnectWebMapper connectWebMapper;

    @Autowired
    private SnowflakeIdWorker snowflakeIdWorker;

    public List<Record> selectPersonWebMap() {

        return personWebMapper.selectPersonWebMap();
    }

    public List<PersonWeb> selectPersonWebList() {

        return personWebMapper.selectPersonWebList();
    }

    public List<PersonWeb> selectPersonWebSearchList(String personWebName) {
//        System.out.println(personWebName);
        return personWebMapper.selectPersonWebSearchList(personWebName);
    }

    public List<PersonWeb> selectPersonWebSearchListOther(String personWebName, String personWebId) {
//        System.out.println(personWebName);
        return personWebMapper.selectPersonWebSearchListOther(personWebName, personWebId);
    }

    public PersonWeb selectPersonWebById(String personWebId) {

        return personWebMapper.selectPersonWebById(personWebId);
    }

    public int insertPersonWeb(PersonWeb personWeb) {

        personWeb.setPersonWebId(snowflakeIdWorker.nextId());
        return personWebMapper.insertPersonWeb(personWeb);
    }

    public int updatePersonWeb(PersonWeb personWeb) {

        return personWebMapper.updatePersonWeb(personWeb);
    }

    public int deletePersonWeb(String personWebId) {

        return personWebMapper.deletePersonWeb(personWebId);
    }

    public ConnectWeb selectConnectWebById(String connectWebId) {

        return connectWebMapper.selectConnectWebById(connectWebId);
    }

    public int insertConnectWeb(ConnectWeb connectWeb) {

        connectWeb.setConnectWebId(snowflakeIdWorker.nextId());
        return connectWebMapper.insertConnectWeb(connectWeb);
    }

    public int updateConnectWeb(ConnectWeb connectWeb) {

        return connectWebMapper.updateConnectWeb(connectWeb);
    }

    public int deleteConnectWeb(String connectWebId) {

        return connectWebMapper.deleteConnectWeb(connectWebId);
    }
}
