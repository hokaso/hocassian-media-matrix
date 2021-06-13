package com.ruoyi.business.domain;

import java.util.Date;
import com.fasterxml.jackson.annotation.JsonFormat;
import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.ruoyi.common.annotation.Excel;
import com.ruoyi.common.core.domain.BaseEntity;

/**
 * 主页轮播图对象 bus_swiper
 * 
 * @author Hocassian
 * @date 2020-10-15
 */
public class BusSwiper extends BaseEntity
{
    private static final long serialVersionUID = 1L;

    /** 客户端轮播图id */
    private Long swiperId;

    /** 轮播图地址 */
    @Excel(name = "轮播图地址")
    private String swiperPic;

    /** 轮播图名称 */
    @Excel(name = "轮播图名称")
    private String swiperName;

    /** 轮播图状态 */
    @Excel(name = "轮播图状态")
    private String swiperStatus;

    /** 创建时间 */
    private Date createAt;

    /** 更改时间 */
    private Date updateAt;

    /** 创建者 */
    private String createBy;

    /** 更新者 */
    private String updateBy;

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


    public void setSwiperId(Long id)
    {
        this.swiperId = id;
    }

    public Long getSwiperId()
    {
        return swiperId;
    }
    public void setSwiperPic(String swiperPic) 
    {
        this.swiperPic = swiperPic;
    }

    public String getSwiperPic() 
    {
        return swiperPic;
    }
    public void setSwiperName(String swiperName) 
    {
        this.swiperName = swiperName;
    }

    public String getSwiperName() 
    {
        return swiperName;
    }
    public void setSwiperStatus(String swiperStatus) 
    {
        this.swiperStatus = swiperStatus;
    }

    public String getSwiperStatus() 
    {
        return swiperStatus;
    }
    public void setCreateAt(Date createAt) 
    {
        this.createAt = createAt;
    }

    public Date getCreateAt() 
    {
        return createAt;
    }
    public void setUpdateAt(Date updateAt) 
    {
        this.updateAt = updateAt;
    }

    public Date getUpdateAt() 
    {
        return updateAt;
    }

    @Override
    public String toString() {
        return new ToStringBuilder(this,ToStringStyle.MULTI_LINE_STYLE)
            .append("swiperId", getSwiperId())
            .append("swiperPic", getSwiperPic())
            .append("swiperName", getSwiperName())
            .append("swiperStatus", getSwiperStatus())
            .append("createAt", getCreateAt())
            .append("createBy", getCreateBy())
            .append("updateAt", getUpdateAt())
            .append("updateBy", getUpdateBy())
            .toString();
    }
}
