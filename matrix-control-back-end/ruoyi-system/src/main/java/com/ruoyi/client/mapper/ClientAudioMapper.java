package com.ruoyi.client.mapper;

import com.ruoyi.material.domain.MatAudio;

import java.util.List;

/**
 * 音频素材Mapper接口
 * 
 * @author Hocassian
 * @date 2021-03-15
 */
public interface ClientAudioMapper
{

    /**
     * 查询视频素材列表
     * 
     * @param matAudio 视频素材
     * @return 视频素材集合
     */
    public List<MatAudio> selectClientAudioList(MatAudio matAudio);

    /**
     * 查询音频素材关键字
     *
     * @return 音频素材集合
     */
    public List<String> selectAudioKeywords();
}
