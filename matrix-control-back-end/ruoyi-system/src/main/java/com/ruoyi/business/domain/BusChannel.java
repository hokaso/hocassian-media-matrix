package com.ruoyi.business.domain;

import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.ruoyi.common.annotation.Excel;
import com.ruoyi.common.core.domain.BaseEntity;

import java.util.Date;

/**
 * 频道管理对象 bus_channel
 *
 * @author Hocassian
 * @date 2020-10-10
 */
public class BusChannel extends BaseEntity {
    private static final long serialVersionUID = 1L;

    /**
     * 频道id
     */
    private Long channelId;

    /**
     * 频道链接
     */
    private String channelUrl;

    /**
     * 频道图标
     */
    @Excel(name = "频道图标")
    private String channelLogo;

    /**
     * 频道所有者
     */
    @Excel(name = "频道所有者")
    private String channelOwner;

    /**
     * 频道视频数
     */
    @Excel(name = "频道视频数")
    private String channelVideoCount;

    /** 某个视频是否继承自该频道，默认不使用 */
//    private boolean flag = false;

    /**
     * 创建时间
     */
    private Date createTime;

    /**
     * 更新时间
     */
    private Date updateTime;

    /**
     * 创建者
     */
    private String createBy;

    /**
     * 更新者
     */
    private String updateBy;

    @Override
    public Date getCreateTime() {
        return createTime;
    }

    @Override
    public void setCreateTime(Date createTime) {
        this.createTime = createTime;
    }

    @Override
    public Date getUpdateTime() {
        return updateTime;
    }

    @Override
    public void setUpdateTime(Date updateTime) {
        this.updateTime = updateTime;
    }

    @Override
    public String getCreateBy() {
        return createBy;
    }

    @Override
    public void setCreateBy(String createBy) {
        this.createBy = createBy;
    }

    @Override
    public String getUpdateBy() {
        return updateBy;
    }

    @Override
    public void setUpdateBy(String updateBy) {
        this.updateBy = updateBy;
    }


    public void setChannelId(Long channelId) {
        this.channelId = channelId;
    }

    public Long getChannelId() {
        return channelId;
    }

    public void setChannelUrl(String channelUrl) {
        this.channelUrl = channelUrl;
    }

    public String getChannelUrl() {
        return channelUrl;
    }

    public void setChannelLogo(String channelLogo) {
        this.channelLogo = channelLogo;
    }

    public String getChannelLogo() {
        return channelLogo;
    }

    public void setChannelOwner(String channelOwner) {
        this.channelOwner = channelOwner;
    }

    public String getChannelOwner() {
        return channelOwner;
    }

    public void setChannelVideoCount(String channelVideoCount) {
        this.channelVideoCount = channelVideoCount;
    }

    public String getChannelVideoCount() {
        return channelVideoCount;
    }

    @Override
    public String toString() {
        return new ToStringBuilder(this, ToStringStyle.MULTI_LINE_STYLE)
                .append("channelId", getChannelId())
                .append("channelUrl", getChannelUrl())
                .append("channelLogo", getChannelLogo())
                .append("channelOwner", getChannelOwner())
                .append("channelVideoCount", getChannelVideoCount())
                .append("createBy", getCreateBy())
                .append("updateBy", getUpdateBy())
                .append("createTime", getCreateTime())
                .append("updateTime", getUpdateTime())
                .toString();
    }
}
