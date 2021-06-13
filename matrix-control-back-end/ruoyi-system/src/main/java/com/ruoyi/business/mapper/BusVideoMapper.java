package com.ruoyi.business.mapper;

import java.util.List;
import com.ruoyi.business.domain.BusVideo;

/**
 * 视频管理Mapper接口
 * 
 * @author Hocassian
 * @date 2020-10-10
 */
public interface BusVideoMapper 
{
    /**
     * 查询视频管理
     * 
     * @param videoId 视频管理ID
     * @return 视频管理
     */
    public BusVideo selectBusVideoById(Long videoId);

    /**
     * 查询视频管理列表
     * 
     * @param busVideo 视频管理
     * @return 视频管理集合
     */
    public List<BusVideo> selectBusVideoList(BusVideo busVideo);

    /**
     * 改变视频上下架状态
     *
     * @param busVideo 视频管理ID
     * @return 视频管理
     */
    public int changeBusVideoStatus(BusVideo busVideo);

    /**
     * 新增视频管理
     * 
     * @param busVideo 视频管理
     * @return 结果
     */
    public int insertBusVideo(BusVideo busVideo);

    /**
     * 修改视频管理
     * 
     * @param busVideo 视频管理
     * @return 结果
     */
    public int updateBusVideo(BusVideo busVideo);

    /**
     * 删除视频管理
     * 
     * @param videoId 视频管理ID
     * @return 结果
     */
    public int deleteBusVideoById(Long videoId);

    /**
     * 批量删除视频管理
     * 
     * @param videoIds 需要删除的数据ID
     * @return 结果
     */
    public int deleteBusVideoByIds(Long[] videoIds);
}
