package com.ruoyi.business.domain;

import com.fasterxml.jackson.annotation.JsonFormat;
import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.ruoyi.common.annotation.Excel;
import com.ruoyi.common.core.domain.BaseEntity;

import java.util.Date;

/**
 * 视频管理对象 bus_video
 *
 * @author Hocassian
 * @date 2020-10-10
 */
public class BusVideo extends BaseEntity {
    private static final long serialVersionUID = 1L;

    /**
     * 视频id
     */
    private Long videoId;

    /**
     * 视频标题
     */
    @Excel(name = "视频标题")
    private String videoTitle;

    /**
     * 视频简介
     */
    @Excel(name = "视频简介")
    private String videoProfile;

    /**
     * 视频链接
     */
    private String videoUrl;

    /**
     * 视频封面
     */
    @Excel(name = "视频封面")
    private String videoPic;

    /**
     * 视频状态
     */
    @Excel(name = "视频状态")
    private String videoStatus;

    /**
     * 视频分类
     */
    @Excel(name = "视频分类")
    private String videoClass;

    /**
     * 视频作者
     */
    @Excel(name = "视频作者")
    private String videoAuthor;

    /**
     * 是否为带制作视频
     */
    @Excel(name = "是否招牌")
    private String videoIsHuge;

    /**
     * 带制作视频封面
     */
    @Excel(name = "招牌封面")
    private String videoHugePic;

    /**
     * 视频文件路径
     */
    @Excel(name = "视频文件")
    private String videoPath;

    /**
     * 视频发布日期
     */
    private String videoPublish;

    /**
     * 视频详情路径
     */
    @Excel(name = "视频文件")
    private String videoJson;

    /**
     * 頻道名稱
     */
    @JsonFormat(pattern = "yyyy-MM-dd")
    private String channelOwner;

    /**
     * 视频关联作者频道表
     */
    private BusChannel busChannel;

    /** 创建时间 */
    private Date createTime;

    /** 更新时间 */
    private Date updateTime;

    /** 创建者 */
    private String createBy;

    /** 更新者 */
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

    public void setVideoId(Long videoId) {
        this.videoId = videoId;
    }

    public Long getVideoId() {
        return videoId;
    }

    public void setVideoTitle(String videoTitle) {
        this.videoTitle = videoTitle;
    }

    public String getVideoTitle() {
        return videoTitle;
    }

    public void setVideoProfile(String videoProfile) {
        this.videoProfile = videoProfile;
    }

    public String getVideoProfile() {
        return videoProfile;
    }

    public void setVideoUrl(String videoUrl) {
        this.videoUrl = videoUrl;
    }

    public String getVideoUrl() {
        return videoUrl;
    }

    public void setVideoPic(String videoPic) {
        this.videoPic = videoPic;
    }

    public String getVideoPic() {
        return videoPic;
    }

    public void setVideoStatus(String videoStatus) {
        this.videoStatus = videoStatus;
    }

    public String getVideoStatus() {
        return videoStatus;
    }

    public void setVideoClass(String videoClass) {
        this.videoClass = videoClass;
    }

    public String getVideoClass() {
        return videoClass;
    }

    public void setVideoAuthor(String videoAuthor) {
        this.videoAuthor = videoAuthor;
    }

    public String getVideoAuthor() {
        return videoAuthor;
    }

    public void setVideoIsHuge(String videoIsHuge) {
        this.videoIsHuge = videoIsHuge;
    }

    public String getVideoIsHuge() {
        return videoIsHuge;
    }

    public void setVideoHugePic(String videoHugePic) {
        this.videoHugePic = videoHugePic;
    }

    public String getVideoHugePic() {
        return videoHugePic;
    }

    public void setVideoPath(String videoPath) {
        this.videoPath = videoPath;
    }

    public String getVideoPath() {
        return videoPath;
    }

    public void setVideoPublish(String videoPublish) {
        this.videoPublish = videoPublish;
    }

    public String getVideoPublish() {
        return videoPublish;
    }

    public void setVideoJson(String videoJson) {
        this.videoJson = videoJson;
    }

    public String getVideoJson() {
        return videoJson;
    }

    public void setChannelOwner(String channelOwner) {
        this.channelOwner = channelOwner;
    }

    public String getChannelOwner() {
        return channelOwner;
    }

    public void setBusChannel(BusChannel busChannel) {
        this.busChannel = busChannel;
    }

    public BusChannel getBusChannel() {
        if (busChannel == null) {
            busChannel = new BusChannel();
        }
        return busChannel;
    }

    @Override
    public String toString() {
        return new ToStringBuilder(this, ToStringStyle.MULTI_LINE_STYLE)
                .append("videoId", getVideoId())
                .append("videoTitle", getVideoTitle())
                .append("videoProfile", getVideoProfile())
                .append("videoUrl", getVideoUrl())
                .append("videoPic", getVideoPic())
                .append("videoStatus", getVideoStatus())
                .append("videoClass", getVideoClass())
                .append("videoAuthor", getVideoAuthor())
                .append("videoIsHuge", getVideoIsHuge())
                .append("videoHugePic", getVideoHugePic())
                .append("videoPath", getVideoPath())
                .append("videoPublish", getVideoPublish())
                .append("videoJson", getVideoPath())
                .append("busChannel", getBusChannel())
                .append("createBy", getCreateBy())
                .append("updateBy", getUpdateBy())
                .append("createTime", getCreateTime())
                .append("updateTime", getUpdateTime())
                .toString();
    }
}
