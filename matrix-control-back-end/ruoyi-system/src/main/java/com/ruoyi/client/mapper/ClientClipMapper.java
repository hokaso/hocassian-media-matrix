package com.ruoyi.client.mapper;

import com.ruoyi.material.domain.MatClip;

import java.util.List;

/**
 * 视频素材Mapper接口
 * 
 * @author Hocassian
 * @date 2021-03-15
 */
public interface ClientClipMapper
{

    /**
     * 查询视频素材列表
     * 
     * @param matClip 视频素材
     * @return 视频素材集合
     */
    public List<MatClip> selectClientClipList(MatClip matClip);

    /**
     * 查询视频素材关键字
     *
     * @return 视频素材集合
     */
    public List<String> selectClipKeywords();
}
