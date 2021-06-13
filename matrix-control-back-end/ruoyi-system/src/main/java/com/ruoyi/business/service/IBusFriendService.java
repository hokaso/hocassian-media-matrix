package com.ruoyi.business.service;

import com.ruoyi.business.domain.BusFriend;

import java.util.List;

/**
 * 友情链接Service接口
 * 
 * @author Hocassian
 * @date 2021-04-15
 */
public interface IBusFriendService 
{
    /**
     * 查询友情链接
     * 
     * @param friendId 友情链接ID
     * @return 友情链接
     */
    public BusFriend selectBusFriendById(Long friendId);

    /**
     * 查询友情链接列表
     * 
     * @param busFriend 友情链接
     * @return 友情链接集合
     */
    public List<BusFriend> selectBusFriendList(BusFriend busFriend);

    /**
     * 新增友情链接
     * 
     * @param busFriend 友情链接
     * @return 结果
     */
    public int insertBusFriend(BusFriend busFriend);

    /**
     * 修改友情链接
     * 
     * @param busFriend 友情链接
     * @return 结果
     */
    public int updateBusFriend(BusFriend busFriend);

    /**
     * 批量删除友情链接
     * 
     * @param friendIds 需要删除的友情链接ID
     * @return 结果
     */
    public int deleteBusFriendByIds(Long[] friendIds);

    /**
     * 删除友情链接信息
     * 
     * @param friendId 友情链接ID
     * @return 结果
     */
    public int deleteBusFriendById(Long friendId);
}
