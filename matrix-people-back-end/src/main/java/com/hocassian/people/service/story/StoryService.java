package com.hocassian.people.service.story;

import com.hocassian.people.domain.story.ConnectStory;
import com.hocassian.people.domain.story.PersonStory;
import com.hocassian.people.mapper.story.ConnectStoryMapper;
import com.hocassian.people.mapper.story.PersonStoryMapper;
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
@Service("storyService")
public class StoryService {

    @Autowired
    private PersonStoryMapper personStoryMapper;

    @Autowired
    private ConnectStoryMapper connectStoryMapper;

    @Autowired
    private SnowflakeIdWorker snowflakeIdWorker;

    public List<Record> selectPersonStoryList() {

        return personStoryMapper.selectPersonStoryList();
    }

    public PersonStory selectPersonStoryById(String personStoryId) {

        return personStoryMapper.selectPersonStoryById(personStoryId);
    }

    public int insertPersonStory(PersonStory personStory) {

        personStory.setPersonStoryId(snowflakeIdWorker.nextId());
        return personStoryMapper.insertPersonStory(personStory);
    }

    public int updatePersonStory(PersonStory personStory) {

        return personStoryMapper.updatePersonStory(personStory);
    }

    public int deletePersonStory(String personStoryId) {

        return personStoryMapper.deletePersonStory(personStoryId);
    }

    public ConnectStory selectConnectStoryById(String connectStoryId) {

        return connectStoryMapper.selectConnectStoryById(connectStoryId);
    }

    public int insertConnectStory(ConnectStory connectStory) {

        connectStory.setConnectStoryId(snowflakeIdWorker.nextId());
        return connectStoryMapper.insertConnectStory(connectStory);
    }

    public int updateConnectStory(ConnectStory connectStory) {

        return connectStoryMapper.updateConnectStory(connectStory);
    }

    public int deleteConnectStory(String connectStoryId) {

        return connectStoryMapper.deleteConnectStory(connectStoryId);
    }

}
