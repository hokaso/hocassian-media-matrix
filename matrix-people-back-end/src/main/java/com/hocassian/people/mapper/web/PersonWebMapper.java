package com.hocassian.people.mapper.web;

import com.hocassian.people.domain.web.PersonWeb;
import org.neo4j.driver.Record;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * @author Hocassian
 */
@Repository
public interface PersonWebMapper {
    
    /**
     * 查询全部
     *
     * @return Record格式的列表
     */
    List<Record> selectPersonWebMap();

    /**
     * 查询全部
     *
     * @return List格式的列表
     */
    List<PersonWeb> selectPersonWebList();

    /**
     * 查询全部（搜索使用）
     *
     * @return List格式的列表（搜索使用）
     */
    List<PersonWeb> selectPersonWebSearchList(String personWebName);

    /**
     * 查询全部（搜索使用）
     *
     * @return List格式的列表（搜索使用）
     */
    List<PersonWeb> selectPersonWebSearchListOther(String personWebName, String personWebId);

    /**
     * 查询单个节点信息
     *
     * @param personWebId 节点id
     * @return PersonWeb实体信息
     */
    PersonWeb selectPersonWebById(String personWebId);

    /**
     * 插入单个节点信息
     *
     * @param personWeb 节点实体
     * @return 插入个数
     */
    int insertPersonWeb(PersonWeb personWeb);

    /**
     * 修改单个节点信息
     *
     * @param personWeb 节点实体
     * @return 修改个数
     */
    int updatePersonWeb(PersonWeb personWeb);

    /**
     * 删除单个节点
     *
     * @param personWebId 节点实体
     * @return 删除个数
     */
    int deletePersonWeb(String personWebId);
    
}
