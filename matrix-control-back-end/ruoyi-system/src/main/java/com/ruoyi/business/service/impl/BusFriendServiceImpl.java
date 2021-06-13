package com.ruoyi.business.service.impl;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.business.mapper.BusFriendMapper;
import com.ruoyi.business.domain.BusFriend;
import com.ruoyi.business.service.IBusFriendService;

/**
 * 友情链接Service业务层处理
 * 
 * @author Hocassian
 * @date 2021-04-15
 */
@Service
public class BusFriendServiceImpl implements IBusFriendService 
{
    @Autowired
    private BusFriendMapper busFriendMapper;

    /**
     * 查询友情链接
     * 
     * @param friendId 友情链接ID
     * @return 友情链接
     */
    @Override
    public BusFriend selectBusFriendById(Long friendId)
    {
        return busFriendMapper.selectBusFriendById(friendId);
    }

    /**
     * 查询友情链接列表
     * 
     * @param busFriend 友情链接
     * @return 友情链接
     */
    @Override
    public List<BusFriend> selectBusFriendList(BusFriend busFriend)
    {
        return busFriendMapper.selectBusFriendList(busFriend);
    }

    /**
     * 新增友情链接
     * 
     * @param busFriend 友情链接
     * @return 结果
     */
    @Override
    public int insertBusFriend(BusFriend busFriend)
    {
        return busFriendMapper.insertBusFriend(busFriend);
    }

    /**
     * 修改友情链接
     * 
     * @param busFriend 友情链接
     * @return 结果
     */
    @Override
    public int updateBusFriend(BusFriend busFriend)
    {
        return busFriendMapper.updateBusFriend(busFriend);
    }

    /**
     * 批量删除友情链接
     * 
     * @param friendIds 需要删除的友情链接ID
     * @return 结果
     */
    @Override
    public int deleteBusFriendByIds(Long[] friendIds)
    {
        return busFriendMapper.deleteBusFriendByIds(friendIds);
    }

    /**
     * 删除友情链接信息
     * 
     * @param friendId 友情链接ID
     * @return 结果
     */
    @Override
    public int deleteBusFriendById(Long friendId)
    {
        return busFriendMapper.deleteBusFriendById(friendId);
    }
}
