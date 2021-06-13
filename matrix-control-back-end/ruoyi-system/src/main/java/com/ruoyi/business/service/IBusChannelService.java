package com.ruoyi.business.service;

import java.util.List;
import com.ruoyi.business.domain.BusChannel;

/**
 * 频道管理Service接口
 * 
 * @author Hocassian
 * @date 2020-10-10
 */
public interface IBusChannelService 
{
    /**
     * 查询频道管理
     * 
     * @param channelId 频道管理ID
     * @return 频道管理
     */
    public BusChannel selectBusChannelById(Long channelId);

    /**
     * 查询频道管理列表
     * 
     * @param busChannel 频道管理
     * @return 频道管理集合
     */
    public List<BusChannel> selectBusChannelList(BusChannel busChannel);

    /**
     * 新增频道管理
     * 
     * @param busChannel 频道管理
     * @return 结果
     */
    public int insertBusChannel(BusChannel busChannel);

    /**
     * 修改频道管理
     * 
     * @param busChannel 频道管理
     * @return 结果
     */
    public int updateBusChannel(BusChannel busChannel);

    /**
     * 批量删除频道管理
     * 
     * @param channelIds 需要删除的频道管理ID
     * @return 结果
     */
    public int deleteBusChannelByIds(Long[] channelIds);

    /**
     * 删除频道管理信息
     * 
     * @param channelId 频道管理ID
     * @return 结果
     */
    public int deleteBusChannelById(Long channelId);
}
