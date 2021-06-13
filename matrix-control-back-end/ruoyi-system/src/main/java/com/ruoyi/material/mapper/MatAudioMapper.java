package com.ruoyi.material.mapper;

import com.ruoyi.material.domain.MatAudio;

import java.util.List;

/**
 * 音频素材Mapper接口
 * 
 * @author Hocassian
 * @date 2021-02-28
 */
public interface MatAudioMapper 
{
    /**
     * 查询音频素材
     * 
     * @param audioId 音频素材ID
     * @return 音频素材
     */
    public MatAudio selectMatAudioById(Long audioId);

    /**
     * 查询音频素材列表
     * 
     * @param matAudio 音频素材
     * @return 音频素材集合
     */
    public List<MatAudio> selectMatAudioList(MatAudio matAudio);

    /**
     * 改变状态
     *
     * @param matAudio 管理ID
     * @return 管理
     */
    public int changeMatAudioStatus(MatAudio matAudio);

    /**
     * 新增音频素材
     * 
     * @param matAudio 音频素材
     * @return 结果
     */
    public int insertMatAudio(MatAudio matAudio);

    /**
     * 修改音频素材
     * 
     * @param matAudio 音频素材
     * @return 结果
     */
    public int updateMatAudio(MatAudio matAudio);

    /**
     * 删除音频素材
     * 
     * @param audioId 音频素材ID
     * @return 结果
     */
    public int deleteMatAudioById(Long audioId);

    /**
     * 批量删除音频素材
     * 
     * @param audioIds 需要删除的数据ID
     * @return 结果
     */
    public int deleteMatAudioByIds(Long[] audioIds);
}
