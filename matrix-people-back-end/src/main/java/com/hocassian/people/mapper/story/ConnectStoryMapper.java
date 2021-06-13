package com.hocassian.people.mapper.story;

import com.hocassian.people.domain.story.ConnectStory;
import org.springframework.stereotype.Repository;

/**
 * @author Hocassian
 */
@Repository
public interface ConnectStoryMapper {

    /**
     * 查询单个连接信息
     *
     * @param connectStoryId 连接id
     * @return ConnectStory实体信息
     */
    ConnectStory selectConnectStoryById(String connectStoryId);

    /**
     * 插入单个连接信息
     *
     * @param connectStory 连接实体
     * @return 插入个数
     */
    int insertConnectStory(ConnectStory connectStory);

    /**
     * 修改单个连接信息
     *
     * @param connectStory 修改实体
     * @return 插入个数
     */
    int updateConnectStory(ConnectStory connectStory);

    /**
     * 删除单个连接
     *
     * @param connectStoryId 连接实体
     * @return 删除个数
     */
    int deleteConnectStory(String connectStoryId);
}
