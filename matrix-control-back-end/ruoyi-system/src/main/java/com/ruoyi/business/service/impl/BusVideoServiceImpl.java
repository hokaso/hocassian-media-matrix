package com.ruoyi.business.service.impl;

import java.util.List;

import com.ruoyi.business.domain.BusChannel;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.business.mapper.BusVideoMapper;
import com.ruoyi.business.domain.BusVideo;
import com.ruoyi.business.service.IBusVideoService;

/**
 * 视频管理Service业务层处理
 * 
 * @author Hocassian
 * @date 2020-10-10
 */
@Service
public class BusVideoServiceImpl implements IBusVideoService 
{
    @Autowired
    private BusVideoMapper busVideoMapper;

    /**
     * 查询视频管理
     * 
     * @param videoId 视频管理ID
     * @return 视频管理
     */
    @Override
    public BusVideo selectBusVideoById(Long videoId)
    {
        return busVideoMapper.selectBusVideoById(videoId);
    }

    /**
     * 查询视频管理列表
     * 
     * @param busVideo 视频管理
     * @return 视频管理
     */
    @Override
    public List<BusVideo> selectBusVideoList(BusVideo busVideo)
    {
        BusChannel busChannel = busVideo.getBusChannel();
        busChannel.setChannelOwner(busVideo.getChannelOwner());
        busVideo.setBusChannel(busChannel);
        return busVideoMapper.selectBusVideoList(busVideo);
    }

    /**
     * 改变状态
     *
     * @param busVideo 视频状态
     * @return 视频状态
     */
    @Override
    public int changeBusVideoStatus(BusVideo busVideo)
    {
        return busVideoMapper.changeBusVideoStatus(busVideo);
    }

    /**
     * 新增视频管理
     * 
     * @param busVideo 视频管理
     * @return 结果
     */
    @Override
    public int insertBusVideo(BusVideo busVideo)
    {
        return busVideoMapper.insertBusVideo(busVideo);
    }

    /**
     * 修改视频管理
     * 
     * @param busVideo 视频管理
     * @return 结果
     */
    @Override
    public int updateBusVideo(BusVideo busVideo)
    {
        return busVideoMapper.updateBusVideo(busVideo);
    }

    /**
     * 批量删除视频管理
     * 
     * @param videoIds 需要删除的视频管理ID
     * @return 结果
     */
    @Override
    public int deleteBusVideoByIds(Long[] videoIds)
    {
        return busVideoMapper.deleteBusVideoByIds(videoIds);
    }

    /**
     * 删除视频管理信息
     * 
     * @param videoId 视频管理ID
     * @return 结果
     */
    @Override
    public int deleteBusVideoById(Long videoId)
    {
        return busVideoMapper.deleteBusVideoById(videoId);
    }
}
