package com.ruoyi.material.mapper;

import com.ruoyi.material.domain.MatImage;

import java.util.List;

/**
 * 图片素材Mapper接口
 * 
 * @author Hocassian
 * @date 2021-03-04
 */
public interface MatImageMapper 
{
    /**
     * 查询图片素材
     * 
     * @param imageId 图片素材ID
     * @return 图片素材
     */
    public MatImage selectMatImageById(Long imageId);

    /**
     * 查询图片素材列表
     * 
     * @param matImage 图片素材
     * @return 图片素材集合
     */
    public List<MatImage> selectMatImageList(MatImage matImage);

    /**
     * 改变状态
     *
     * @param matImage 管理ID
     * @return 管理
     */
    public int changeMatImageStatus(MatImage matImage);

    /**
     * 新增图片素材
     * 
     * @param matImage 图片素材
     * @return 结果
     */
    public int insertMatImage(MatImage matImage);

    /**
     * 修改图片素材
     * 
     * @param matImage 图片素材
     * @return 结果
     */
    public int updateMatImage(MatImage matImage);

    /**
     * 删除图片素材
     * 
     * @param imageId 图片素材ID
     * @return 结果
     */
    public int deleteMatImageById(Long imageId);

    /**
     * 批量删除图片素材
     * 
     * @param imageIds 需要删除的数据ID
     * @return 结果
     */
    public int deleteMatImageByIds(Long[] imageIds);
}
