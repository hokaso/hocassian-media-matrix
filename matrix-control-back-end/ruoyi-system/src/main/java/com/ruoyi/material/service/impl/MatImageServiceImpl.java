package com.ruoyi.material.service.impl;

import java.util.List;

import com.ruoyi.material.domain.MatImage;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.material.mapper.MatImageMapper;
import com.ruoyi.material.domain.MatImage;
import com.ruoyi.material.service.IMatImageService;

/**
 * 图片素材Service业务层处理
 * 
 * @author Hocassian
 * @date 2021-03-04
 */
@Service
public class MatImageServiceImpl implements IMatImageService 
{
    @Autowired
    private MatImageMapper matImageMapper;

    /**
     * 查询图片素材
     * 
     * @param imageId 图片素材ID
     * @return 图片素材
     */
    @Override
    public MatImage selectMatImageById(Long imageId)
    {
        return matImageMapper.selectMatImageById(imageId);
    }

    /**
     * 查询图片素材列表
     * 
     * @param matImage 图片素材
     * @return 图片素材
     */
    @Override
    public List<MatImage> selectMatImageList(MatImage matImage)
    {
        return matImageMapper.selectMatImageList(matImage);
    }

    /**
     * 改变状态
     *
     * @param matImage 视频状态
     * @return 视频状态
     */
    @Override
    public int changeMatImageStatus(MatImage matImage)
    {
        return matImageMapper.changeMatImageStatus(matImage);
    }

    /**
     * 新增图片素材
     * 
     * @param matImage 图片素材
     * @return 结果
     */
    @Override
    public int insertMatImage(MatImage matImage)
    {
        return matImageMapper.insertMatImage(matImage);
    }

    /**
     * 修改图片素材
     * 
     * @param matImage 图片素材
     * @return 结果
     */
    @Override
    public int updateMatImage(MatImage matImage)
    {
        return matImageMapper.updateMatImage(matImage);
    }

    /**
     * 批量删除图片素材
     * 
     * @param imageIds 需要删除的图片素材ID
     * @return 结果
     */
    @Override
    public int deleteMatImageByIds(Long[] imageIds)
    {
        return matImageMapper.deleteMatImageByIds(imageIds);
    }

    /**
     * 删除图片素材信息
     * 
     * @param imageId 图片素材ID
     * @return 结果
     */
    @Override
    public int deleteMatImageById(Long imageId)
    {
        return matImageMapper.deleteMatImageById(imageId);
    }
}
