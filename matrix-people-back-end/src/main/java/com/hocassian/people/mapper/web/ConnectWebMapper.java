package com.hocassian.people.mapper.web;

import com.hocassian.people.domain.web.ConnectWeb;
import org.springframework.stereotype.Repository;

/**
 * @author Hocassian
 */
@Repository
public interface ConnectWebMapper {

    /**
     * 查询单个连接信息
     *
     * @param connectWebId 连接id
     * @return ConnectWeb实体信息
     */
    ConnectWeb selectConnectWebById(String connectWebId);

    /**
     * 插入单个连接信息
     *
     * @param connectWeb 连接实体
     * @return 插入个数
     */
    int insertConnectWeb(ConnectWeb connectWeb);

    /**
     * 修改单个连接信息
     *
     * @param connectWeb 修改实体
     * @return 插入个数
     */
    int updateConnectWeb(ConnectWeb connectWeb);

    /**
     * 删除单个连接
     *
     * @param connectWebId 连接实体
     * @return 删除个数
     */
    int deleteConnectWeb(String connectWebId);
}
