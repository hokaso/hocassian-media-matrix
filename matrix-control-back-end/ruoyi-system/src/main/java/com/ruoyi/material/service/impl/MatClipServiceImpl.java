package com.ruoyi.material.service.impl;

import java.io.File;
import java.util.List;

import ch.qos.logback.classic.Level;
import com.ruoyi.common.config.RuoYiConfig;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.material.mapper.MatClipMapper;
import com.ruoyi.material.domain.MatClip;
import com.ruoyi.material.service.IMatClipService;

/**
 * 视频素材Service业务层处理
 * 
 * @author Hocassian
 * @date 2021-02-22
 */
@Service
public class MatClipServiceImpl implements IMatClipService 
{
    @Autowired
    private MatClipMapper matClipMapper;

    /**
     * 查询视频素材
     * 
     * @param materialId 视频素材ID
     * @return 视频素材
     */
    @Override
    public MatClip selectMatClipById(Long materialId)
    {
        return matClipMapper.selectMatClipById(materialId);
    }

    /**
     * 查询视频素材列表
     * 
     * @param matClip 视频素材
     * @return 视频素材
     */
    @Override
    public List<MatClip> selectMatClipList(MatClip matClip)
    {
        return matClipMapper.selectMatClipList(matClip);
    }

    /**
     * 改变状态
     *
     * @param matClip 视频状态
     * @return 视频状态
     */
    @Override
    public int changeMatClipStatus(MatClip matClip)
    {
        return matClipMapper.changeMatClipStatus(matClip);
    }

    /**
     * 新增视频素材
     * 
     * @param matClip 视频素材
     * @return 结果
     */
    @Override
    public int insertMatClip(MatClip matClip)
    {
        return matClipMapper.insertMatClip(matClip);
    }

    /**
     * 修改视频素材
     * 
     * @param matClip 视频素材
     * @return 结果
     */
    @Override
    public int updateMatClip(MatClip matClip)
    {
        return matClipMapper.updateMatClip(matClip);
    }

    /**
     * 批量删除视频素材
     * 
     * @param materialIds 需要删除的视频素材ID
     * @return 结果
     */
    @Override
    public int deleteMatClipByIds(Long[] materialIds)
    {

        for (Long materialId : materialIds){

            // 删除正片
            MatClip matClip = selectMatClipById(materialId);
            String imgPath = RuoYiConfig.getProfile() + "/video_clip/" + matClip.getMaterialPath() + ".mp4";
            File file = new File(imgPath);
            System.out.println(file.delete());

        }
        return matClipMapper.deleteMatClipByIds(materialIds);
    }

    /**
     * 批量导出视频素材
     *
     * @param materialIds 需要导出的视频素材ID
     * @return 结果
     */
    @Override
    public int outputMatClipStatus(Long[] materialIds){
        return matClipMapper.outputMatClipStatus(materialIds);
    }

    /**
     * 删除视频素材信息
     * 
     * @param materialId 视频素材ID
     * @return 结果
     */
    @Override
    public int deleteMatClipById(Long materialId)
    {
        return matClipMapper.deleteMatClipById(materialId);
    }
}
