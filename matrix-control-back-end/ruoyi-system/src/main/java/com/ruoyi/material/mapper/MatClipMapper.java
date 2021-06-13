package com.ruoyi.material.mapper;

import java.util.List;
import com.ruoyi.material.domain.MatClip;

/**
 * 视频素材Mapper接口
 * 
 * @author Hocassian
 * @date 2021-02-22
 */
public interface MatClipMapper 
{
    /**
     * 查询视频素材
     * 
     * @param materialId 视频素材ID
     * @return 视频素材
     */
    public MatClip selectMatClipById(Long materialId);

    /**
     * 查询视频素材列表
     * 
     * @param matClip 视频素材
     * @return 视频素材集合
     */
    public List<MatClip> selectMatClipList(MatClip matClip);

    /**
     * 改变状态
     *
     * @param matClip 视频管理ID
     * @return 视频管理
     */
    public int changeMatClipStatus(MatClip matClip);

    /**
     * 新增视频素材
     * 
     * @param matClip 视频素材
     * @return 结果
     */
    public int insertMatClip(MatClip matClip);

    /**
     * 修改视频素材
     * 
     * @param matClip 视频素材
     * @return 结果
     */
    public int updateMatClip(MatClip matClip);

    /**
     * 删除视频素材
     * 
     * @param materialId 视频素材ID
     * @return 结果
     */
    public int deleteMatClipById(Long materialId);

    /**
     * 批量删除视频素材
     * 
     * @param materialIds 需要删除的数据ID
     * @return 结果
     */
    public int deleteMatClipByIds(Long[] materialIds);
}
