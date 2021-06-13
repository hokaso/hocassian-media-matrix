package com.ruoyi.create.service.impl;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.create.mapper.CreChapterMapper;
import com.ruoyi.create.domain.CreChapter;
import com.ruoyi.create.service.ICreChapterService;

/**
 * 篇章管理Service业务层处理
 * 
 * @author Hocassian
 * @date 2021-02-08
 */
@Service
public class CreChapterServiceImpl implements ICreChapterService 
{
    @Autowired
    private CreChapterMapper creChapterMapper;

    /**
     * 查询篇章管理
     * 
     * @param chapterStoryId 篇章管理ID
     * @return 篇章管理
     */
    @Override
    public CreChapter selectCreChapterById(Long chapterStoryId)
    {
        return creChapterMapper.selectCreChapterById(chapterStoryId);
    }

    /**
     * 查询篇章管理列表
     * 
     * @param creChapter 篇章管理
     * @return 篇章管理
     */
    @Override
    public List<CreChapter> selectCreChapterList(CreChapter creChapter)
    {
        return creChapterMapper.selectCreChapterList(creChapter);
    }

    /**
     * 新增篇章管理
     * 
     * @param creChapter 篇章管理
     * @return 结果
     */
    @Override
    public int insertCreChapter(CreChapter creChapter)
    {
        return creChapterMapper.insertCreChapter(creChapter);
    }

    /**
     * 修改篇章管理
     * 
     * @param creChapter 篇章管理
     * @return 结果
     */
    @Override
    public int updateCreChapter(CreChapter creChapter)
    {
        return creChapterMapper.updateCreChapter(creChapter);
    }

    /**
     * 批量删除篇章管理
     * 
     * @param chapterStoryIds 需要删除的篇章管理ID
     * @return 结果
     */
    @Override
    public int deleteCreChapterByIds(Long[] chapterStoryIds)
    {
        return creChapterMapper.deleteCreChapterByIds(chapterStoryIds);
    }

    /**
     * 删除篇章管理信息
     * 
     * @param chapterStoryId 篇章管理ID
     * @return 结果
     */
    @Override
    public int deleteCreChapterById(Long chapterStoryId)
    {
        return creChapterMapper.deleteCreChapterById(chapterStoryId);
    }
}
