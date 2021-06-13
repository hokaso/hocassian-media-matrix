package com.ruoyi.create.domain;

import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.ruoyi.common.annotation.Excel;
import com.ruoyi.common.core.domain.BaseEntity;

/**
 * 作品管理对象 cre_work
 * 
 * @author Hocassian
 * @date 2021-02-08
 */
public class CreWork extends BaseEntity
{
    private static final long serialVersionUID = 1L;

    /** 作品编号 */
    private Long workStoryId;

    /** 作品名称 */
    @Excel(name = "作品名称")
    private String workStoryName;

    /** 作品英文名称 */
    @Excel(name = "作品英文名称")
    private String workStoryEnName;

    /** 作品简介 */
    @Excel(name = "作品简介")
    private String workStoryInfo;

    /** 作品作者 */
    @Excel(name = "作品作者")
    private String workStoryAuthor;

    public void setWorkStoryId(Long workStoryId) 
    {
        this.workStoryId = workStoryId;
    }

    public Long getWorkStoryId() 
    {
        return workStoryId;
    }
    public void setWorkStoryName(String workStoryName) 
    {
        this.workStoryName = workStoryName;
    }

    public String getWorkStoryName() 
    {
        return workStoryName;
    }
    public void setWorkStoryEnName(String workStoryEnName) 
    {
        this.workStoryEnName = workStoryEnName;
    }

    public String getWorkStoryEnName() 
    {
        return workStoryEnName;
    }
    public void setWorkStoryInfo(String workStoryInfo) 
    {
        this.workStoryInfo = workStoryInfo;
    }

    public String getWorkStoryInfo() 
    {
        return workStoryInfo;
    }
    public void setWorkStoryAuthor(String workStoryAuthor) 
    {
        this.workStoryAuthor = workStoryAuthor;
    }

    public String getWorkStoryAuthor() 
    {
        return workStoryAuthor;
    }

    @Override
    public String toString() {
        return new ToStringBuilder(this,ToStringStyle.MULTI_LINE_STYLE)
            .append("workStoryId", getWorkStoryId())
            .append("workStoryName", getWorkStoryName())
            .append("workStoryEnName", getWorkStoryEnName())
            .append("workStoryInfo", getWorkStoryInfo())
            .append("workStoryAuthor", getWorkStoryAuthor())
            .toString();
    }
}
