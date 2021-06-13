package com.ruoyi.material.service.impl;

import com.ruoyi.common.config.RuoYiConfig;
import com.ruoyi.material.domain.MatAudio;
import com.ruoyi.material.mapper.MatAudioMapper;
import com.ruoyi.material.service.IMatAudioService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.File;
import java.util.List;

/**
 * 音频素材Service业务层处理
 * 
 * @author Hocassian
 * @date 2021-02-28
 */
@Service
public class MatAudioServiceImpl implements IMatAudioService 
{
    @Autowired
    private MatAudioMapper matAudioMapper;

    /**
     * 查询音频素材
     * 
     * @param audioId 音频素材ID
     * @return 音频素材
     */
    @Override
    public MatAudio selectMatAudioById(Long audioId)
    {
        return matAudioMapper.selectMatAudioById(audioId);
    }

    /**
     * 查询音频素材列表
     * 
     * @param matAudio 音频素材
     * @return 音频素材
     */
    @Override
    public List<MatAudio> selectMatAudioList(MatAudio matAudio)
    {
        return matAudioMapper.selectMatAudioList(matAudio);
    }

    /**
     * 改变状态
     *
     * @param matAudio 视频状态
     * @return 视频状态
     */
    @Override
    public int changeMatAudioStatus(MatAudio matAudio)
    {
        return matAudioMapper.changeMatAudioStatus(matAudio);
    }

    /**
     * 新增音频素材
     * 
     * @param matAudio 音频素材
     * @return 结果
     */
    @Override
    public int insertMatAudio(MatAudio matAudio)
    {
        return matAudioMapper.insertMatAudio(matAudio);
    }

    /**
     * 修改音频素材
     * 
     * @param matAudio 音频素材
     * @return 结果
     */
    @Override
    public int updateMatAudio(MatAudio matAudio)
    {
        return matAudioMapper.updateMatAudio(matAudio);
    }

    /**
     * 批量删除音频素材
     * 
     * @param audioIds 需要删除的音频素材ID
     * @return 结果
     */
    @Override
    public int deleteMatAudioByIds(Long[] audioIds)
    {
        for (Long audioId : audioIds){

            // 删除正片
            MatAudio matAudio = selectMatAudioById(audioId);
            String imgPath = RuoYiConfig.getProfile() + "/audio_music/" + matAudio.getAudioPath() + ".mp3";
            File file = new File(imgPath);
            System.out.println(file.delete());
        }
        return matAudioMapper.deleteMatAudioByIds(audioIds);
    }

    /**
     * 删除音频素材信息
     * 
     * @param audioId 音频素材ID
     * @return 结果
     */
    @Override
    public int deleteMatAudioById(Long audioId)
    {
        return matAudioMapper.deleteMatAudioById(audioId);
    }
}
