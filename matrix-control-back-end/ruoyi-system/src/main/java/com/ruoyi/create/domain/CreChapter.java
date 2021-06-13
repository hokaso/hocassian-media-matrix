package com.ruoyi.create.domain;

import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.ruoyi.common.annotation.Excel;
import com.ruoyi.common.core.domain.BaseEntity;

/**
 * 篇章管理对象 cre_chapter
 * 
 * @author Hocassian
 * @date 2021-02-08
 */
public class CreChapter extends BaseEntity
{
    private static final long serialVersionUID = 1L;

    /** 段落编号 */
    private Long chapterStoryId;

    /** 作品编号 */
    @Excel(name = "作品编号")
    private Long chapterWorkId;

    /** 段落标题 */
    @Excel(name = "段落标题")
    private String chapterStoryName;

    /** 段落描述 */
    @Excel(name = "段落描述")
    private String chapterStoryDescription;

    /** 段落周目 */
    private Long chapterStoryTimes;

    /** 段落结局编号 */
    private Long chapterStoryEnding;

    /** 段落类型 */
    @Excel(name = "段落类型")
    private String chapterStoryType;

    /** 段落条件 */
    private String chapterStoryCondiation;

    /** 段落变更 */
    private String chapterStoryOperation;

    /** 下一段落 */
    private String chapterStoryNext;

    /** 上一段落 */
    private String chapterStoryPrevious;

    /** 附加信息 */
    @Excel(name = "附加信息")
    private String chapterStoryAddtional;

    public void setChapterStoryId(Long chapterStoryId) 
    {
        this.chapterStoryId = chapterStoryId;
    }

    public Long getChapterStoryId() 
    {
        return chapterStoryId;
    }
    public void setChapterWorkId(Long chapterWorkId) 
    {
        this.chapterWorkId = chapterWorkId;
    }

    public Long getChapterWorkId() 
    {
        return chapterWorkId;
    }
    public void setChapterStoryName(String chapterStoryName) 
    {
        this.chapterStoryName = chapterStoryName;
    }

    public String getChapterStoryName() 
    {
        return chapterStoryName;
    }
    public void setChapterStoryDescription(String chapterStoryDescription) 
    {
        this.chapterStoryDescription = chapterStoryDescription;
    }

    public String getChapterStoryDescription() 
    {
        return chapterStoryDescription;
    }
    public void setChapterStoryTimes(Long chapterStoryTimes) 
    {
        this.chapterStoryTimes = chapterStoryTimes;
    }

    public Long getChapterStoryTimes() 
    {
        return chapterStoryTimes;
    }
    public void setChapterStoryEnding(Long chapterStoryEnding) 
    {
        this.chapterStoryEnding = chapterStoryEnding;
    }

    public Long getChapterStoryEnding() 
    {
        return chapterStoryEnding;
    }
    public void setChapterStoryType(String chapterStoryType) 
    {
        this.chapterStoryType = chapterStoryType;
    }

    public String getChapterStoryType() 
    {
        return chapterStoryType;
    }
    public void setChapterStoryCondiation(String chapterStoryCondiation) 
    {
        this.chapterStoryCondiation = chapterStoryCondiation;
    }

    public String getChapterStoryCondiation() 
    {
        return chapterStoryCondiation;
    }
    public void setChapterStoryOperation(String chapterStoryOperation) 
    {
        this.chapterStoryOperation = chapterStoryOperation;
    }

    public String getChapterStoryOperation() 
    {
        return chapterStoryOperation;
    }
    public void setChapterStoryNext(String chapterStoryNext) 
    {
        this.chapterStoryNext = chapterStoryNext;
    }

    public String getChapterStoryNext() 
    {
        return chapterStoryNext;
    }
    public void setChapterStoryPrevious(String chapterStoryPrevious) 
    {
        this.chapterStoryPrevious = chapterStoryPrevious;
    }

    public String getChapterStoryPrevious() 
    {
        return chapterStoryPrevious;
    }
    public void setChapterStoryAddtional(String chapterStoryAddtional) 
    {
        this.chapterStoryAddtional = chapterStoryAddtional;
    }

    public String getChapterStoryAddtional() 
    {
        return chapterStoryAddtional;
    }

    @Override
    public String toString() {
        return new ToStringBuilder(this,ToStringStyle.MULTI_LINE_STYLE)
            .append("chapterStoryId", getChapterStoryId())
            .append("chapterWorkId", getChapterWorkId())
            .append("chapterStoryName", getChapterStoryName())
            .append("chapterStoryDescription", getChapterStoryDescription())
            .append("chapterStoryTimes", getChapterStoryTimes())
            .append("chapterStoryEnding", getChapterStoryEnding())
            .append("chapterStoryType", getChapterStoryType())
            .append("chapterStoryCondiation", getChapterStoryCondiation())
            .append("chapterStoryOperation", getChapterStoryOperation())
            .append("chapterStoryNext", getChapterStoryNext())
            .append("chapterStoryPrevious", getChapterStoryPrevious())
            .append("chapterStoryAddtional", getChapterStoryAddtional())
            .toString();
    }
}
