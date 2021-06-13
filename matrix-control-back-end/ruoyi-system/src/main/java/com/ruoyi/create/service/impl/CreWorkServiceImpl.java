package com.ruoyi.create.service.impl;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.create.mapper.CreWorkMapper;
import com.ruoyi.create.domain.CreWork;
import com.ruoyi.create.service.ICreWorkService;

/**
 * 作品管理Service业务层处理
 * 
 * @author Hocassian
 * @date 2021-02-08
 */
@Service
public class CreWorkServiceImpl implements ICreWorkService 
{
    @Autowired
    private CreWorkMapper creWorkMapper;

    /**
     * 查询作品管理
     * 
     * @param workStoryId 作品管理ID
     * @return 作品管理
     */
    @Override
    public CreWork selectCreWorkById(Long workStoryId)
    {
        return creWorkMapper.selectCreWorkById(workStoryId);
    }

    /**
     * 查询作品管理列表
     * 
     * @param creWork 作品管理
     * @return 作品管理
     */
    @Override
    public List<CreWork> selectCreWorkList(CreWork creWork)
    {
        return creWorkMapper.selectCreWorkList(creWork);
    }

    /**
     * 新增作品管理
     * 
     * @param creWork 作品管理
     * @return 结果
     */
    @Override
    public int insertCreWork(CreWork creWork)
    {
        return creWorkMapper.insertCreWork(creWork);
    }

    /**
     * 修改作品管理
     * 
     * @param creWork 作品管理
     * @return 结果
     */
    @Override
    public int updateCreWork(CreWork creWork)
    {
        return creWorkMapper.updateCreWork(creWork);
    }

    /**
     * 批量删除作品管理
     * 
     * @param workStoryIds 需要删除的作品管理ID
     * @return 结果
     */
    @Override
    public int deleteCreWorkByIds(Long[] workStoryIds)
    {
        return creWorkMapper.deleteCreWorkByIds(workStoryIds);
    }

    /**
     * 删除作品管理信息
     * 
     * @param workStoryId 作品管理ID
     * @return 结果
     */
    @Override
    public int deleteCreWorkById(Long workStoryId)
    {
        return creWorkMapper.deleteCreWorkById(workStoryId);
    }
}
