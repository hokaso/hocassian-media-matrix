package com.hocassian.people.mapper.story;

import com.hocassian.people.domain.story.PersonStory;
import org.neo4j.driver.Record;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * @author Hocassian
 */
@Repository
public interface PersonStoryMapper {

    /**
     * 查询全部
     *
     * @return Record格式的列表
     */
    List<Record> selectPersonStoryList();

    /**
     * 查询单个节点信息
     *
     * @param personStoryId 节点id
     * @return PersonStory实体信息
     */
    PersonStory selectPersonStoryById(String personStoryId);

    /**
     * 插入单个节点信息
     *
     * @param personStory 节点实体
     * @return 插入个数
     */
    int insertPersonStory(PersonStory personStory);

    /**
     * 修改单个节点信息
     *
     * @param personStory 节点实体
     * @return 修改个数
     */
    int updatePersonStory(PersonStory personStory);

    /**
     * 删除单个节点
     *
     * @param personStoryId 节点实体
     * @return 删除个数
     */
    int deletePersonStory(String personStoryId);

}
