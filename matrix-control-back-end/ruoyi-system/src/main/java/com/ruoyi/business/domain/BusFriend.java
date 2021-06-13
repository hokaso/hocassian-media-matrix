package com.ruoyi.business.domain;

import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.ruoyi.common.annotation.Excel;
import com.ruoyi.common.core.domain.BaseEntity;

/**
 * 友情链接对象 bus_friend
 * 
 * @author Hocassian
 * @date 2021-04-15
 */
public class BusFriend extends BaseEntity
{
    private static final long serialVersionUID = 1L;

    /** 友链id */
    private Long friendId;

    /** 友链名称 */
    @Excel(name = "友链名称")
    private String friendName;

    /** 友链名称 */
    @Excel(name = "友链名称")
    private String friendUrl;

    /** 友链信息 */
    @Excel(name = "友链信息")
    private String friendInfo;

    /** 友链图片 */
    @Excel(name = "友链图片")
    private String friendPic;

    /** 友链类型 */
    @Excel(name = "友链类型")
    private String friendType;

    /** 友链状态 */
    @Excel(name = "友链状态")
    private String friendStatus;

    public void setFriendId(Long friendId) 
    {
        this.friendId = friendId;
    }

    public Long getFriendId() 
    {
        return friendId;
    }
    public void setFriendName(String friendName) 
    {
        this.friendName = friendName;
    }

    public String getFriendName() 
    {
        return friendName;
    }
    public void setFriendInfo(String friendInfo) 
    {
        this.friendInfo = friendInfo;
    }

    public String getFriendUrl()
    {
        return friendUrl;
    }
    public void setFriendUrl(String friendUrl)
    {
        this.friendUrl = friendUrl;
    }

    public String getFriendInfo() 
    {
        return friendInfo;
    }
    public void setFriendPic(String friendPic) 
    {
        this.friendPic = friendPic;
    }

    public String getFriendPic() 
    {
        return friendPic;
    }
    public void setFriendType(String friendType) 
    {
        this.friendType = friendType;
    }

    public String getFriendType() 
    {
        return friendType;
    }
    public void setFriendStatus(String friendStatus) 
    {
        this.friendStatus = friendStatus;
    }

    public String getFriendStatus() 
    {
        return friendStatus;
    }

    @Override
    public String toString() {
        return new ToStringBuilder(this,ToStringStyle.MULTI_LINE_STYLE)
            .append("friendId", getFriendId())
            .append("friendName", getFriendName())
            .append("friendInfo", getFriendInfo())
            .append("friendUrl", getFriendUrl())
            .append("friendPic", getFriendPic())
            .append("friendType", getFriendType())
            .append("friendStatus", getFriendStatus())
            .toString();
    }
}
