package com.ruoyi.publish.domain;

import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.ruoyi.common.annotation.Excel;
import com.ruoyi.common.core.domain.BaseEntity;

/**
 * 媒体单位对象 pub_unit
 * 
 * @author Hocassian
 * @date 2020-11-24
 */
public class PubUnit extends BaseEntity
{
    private static final long serialVersionUID = 1L;

    /** 媒体单位id */
    private Long unitId;

    /** 媒体单位名称 */
    @Excel(name = "媒体单位名称")
    private String unitName;

    /** 媒体单位简介 */
    @Excel(name = "媒体单位简介")
    private String unitInfo;

    /** 媒体单位邮箱 */
    @Excel(name = "媒体单位邮箱")
    private String unitEmail;

    /** 媒体单位类型 */
    @Excel(name = "媒体单位类型")
    private String unitType;

    public void setUnitId(Long unitId) 
    {
        this.unitId = unitId;
    }

    public Long getUnitId() 
    {
        return unitId;
    }
    public void setUnitName(String unitName) 
    {
        this.unitName = unitName;
    }

    public String getUnitName() 
    {
        return unitName;
    }
    public void setUnitInfo(String unitInfo) 
    {
        this.unitInfo = unitInfo;
    }

    public String getUnitInfo() 
    {
        return unitInfo;
    }
    public void setUnitEmail(String unitEmail) 
    {
        this.unitEmail = unitEmail;
    }

    public String getUnitEmail() 
    {
        return unitEmail;
    }
    public void setUnitType(String unitType) 
    {
        this.unitType = unitType;
    }

    public String getUnitType() 
    {
        return unitType;
    }

    @Override
    public String toString() {
        return new ToStringBuilder(this,ToStringStyle.MULTI_LINE_STYLE)
            .append("unitId", getUnitId())
            .append("unitName", getUnitName())
            .append("unitInfo", getUnitInfo())
            .append("unitEmail", getUnitEmail())
            .append("unitType", getUnitType())
            .append("createBy", getCreateBy())
            .append("createTime", getCreateTime())
            .append("updateBy", getUpdateBy())
            .append("updateTime", getUpdateTime())
            .toString();
    }
}
