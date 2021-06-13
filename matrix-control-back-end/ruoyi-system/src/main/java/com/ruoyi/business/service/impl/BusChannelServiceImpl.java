package com.ruoyi.business.service.impl;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.business.mapper.BusChannelMapper;
import com.ruoyi.business.domain.BusChannel;
import com.ruoyi.business.service.IBusChannelService;

/**
 * 频道管理Service业务层处理
 * 
 * @author Hocassian
 * @date 2020-10-10
 */
@Service
public class BusChannelServiceImpl implements IBusChannelService 
{
    @Autowired
    private BusChannelMapper busChannelMapper;

    /**
     * 查询频道管理
     * 
     * @param channelId 频道管理ID
     * @return 频道管理
     */
    @Override
    public BusChannel selectBusChannelById(Long channelId)
    {
        return busChannelMapper.selectBusChannelById(channelId);
    }

    /**
     * 查询频道管理列表
     * 
     * @param busChannel 频道管理
     * @return 频道管理
     */
    @Override
    public List<BusChannel> selectBusChannelList(BusChannel busChannel)
    {
        return busChannelMapper.selectBusChannelList(busChannel);
    }

    /**
     * 新增频道管理
     * 
     * @param busChannel 频道管理
     * @return 结果
     */
    @Override
    public int insertBusChannel(BusChannel busChannel)
    {
        return busChannelMapper.insertBusChannel(busChannel);
    }

    /**
     * 修改频道管理
     * 
     * @param busChannel 频道管理
     * @return 结果
     */
    @Override
    public int updateBusChannel(BusChannel busChannel)
    {
        return busChannelMapper.updateBusChannel(busChannel);
    }

    /**
     * 批量删除频道管理
     * 
     * @param channelIds 需要删除的频道管理ID
     * @return 结果
     */
    @Override
    public int deleteBusChannelByIds(Long[] channelIds)
    {
        return busChannelMapper.deleteBusChannelByIds(channelIds);
    }

    /**
     * 删除频道管理信息
     * 
     * @param channelId 频道管理ID
     * @return 结果
     */
    @Override
    public int deleteBusChannelById(Long channelId)
    {
        return busChannelMapper.deleteBusChannelById(channelId);
    }
}
