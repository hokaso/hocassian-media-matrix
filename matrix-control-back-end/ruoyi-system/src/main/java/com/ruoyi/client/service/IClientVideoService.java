package com.ruoyi.client.service;

import com.ruoyi.business.domain.BusVideo;

import java.util.List;

/**
 * 视频管理Service接口
 * 
 * @author Hocassian
 * @date 2020-10-10
 */
public interface IClientVideoService
{
    /**
     * 查询视频管理
     * 
     * @param videoId 视频管理ID
     * @return 视频管理
     */
    public BusVideo selectClientVideoById(Long videoId);

    /**
     * 查询视频管理列表
     * 
     * @param busVideo 视频管理
     * @return 视频管理集合
     */
    public List<BusVideo> selectClientVideoList(BusVideo busVideo);
}
