package com.ruoyi.client.mapper;

import com.ruoyi.material.domain.MatImage;

import java.util.List;

/**
 * 音频素材Mapper接口
 * 
 * @author Hocassian
 * @date 2021-03-15
 */
public interface ClientImageMapper
{

    /**
     * 查询图片素材列表
     * 
     * @param matImage 图片素材
     * @return 图片素材集合
     */
    public List<MatImage> selectClientImageList(MatImage matImage);

    /**
     * 查询图片素材路径
     *
     * @return 图片素材集合
     */
    public List<String> selectImageUrls();

    /**
     * 查询图片素材关键字
     *
     * @return 图片素材集合
     */
    public List<String> selectImageKeywords();
}
