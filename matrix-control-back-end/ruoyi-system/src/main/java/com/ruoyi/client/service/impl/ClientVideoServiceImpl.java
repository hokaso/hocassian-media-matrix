package com.ruoyi.client.service.impl;

import com.ruoyi.business.domain.BusVideo;
import com.ruoyi.client.mapper.ClientVideoMapper;
import com.ruoyi.client.service.IClientVideoService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * 视频管理Service业务层处理
 * 
 * @author Hocassian
 * @date 2020-10-10
 */
@Service
public class ClientVideoServiceImpl implements IClientVideoService
{
    @Autowired
    private ClientVideoMapper clientVideoMapper;

    /**
     * 查询视频管理
     * 
     * @param videoId 视频管理ID
     * @return 视频管理
     */
    @Override
    public BusVideo selectClientVideoById(Long videoId)
    {
        return clientVideoMapper.selectClientVideoById(videoId);
    }

    /**
     * 查询视频管理列表
     * 
     * @param busVideo 视频管理
     * @return 视频管理
     */
    @Override
    public List<BusVideo> selectClientVideoList(BusVideo busVideo)
    {
        List<BusVideo> sublimeList = clientVideoMapper.selectClientVideoList(busVideo);
        for ( BusVideo sublime : sublimeList) {

            String rawInfo = sublime.getVideoProfile();
            int infoLength = rawInfo.length();
            String info = rawInfo;
            if (infoLength > 70) {
                info = rawInfo.substring(0, 70);
            }
            sublime.setVideoProfile(info);
        }
        return sublimeList;
    }
}
