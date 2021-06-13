package com.ruoyi.material.domain;

import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.ruoyi.common.annotation.Excel;
import com.ruoyi.common.core.domain.BaseEntity;

/**
 * 音频素材对象 mat_audio
 * 
 * @author Hocassian
 * @date 2021-02-28
 */
public class MatAudio extends BaseEntity
{
    private static final long serialVersionUID = 1L;

    /** 音频素材id */
    private Long audioId;

    /** 音频素材名称 */
    @Excel(name = "音频素材路径")
    private String audioPath;

    /** 音频素材名称 */
    @Excel(name = "音频素材名称")
    private String audioName;

    /** 音频素材作者 */
    @Excel(name = "音频素材作者")
    private String audioAuthor;

    /** 音频素材类型（0纯音乐，1歌曲） */
    @Excel(name = "音频素材类型", readConverterExp = "0=纯音乐，1歌曲")
    private String audioType;

    /** 音频素材状态（0处理完毕，1待处理，2无需处理） */
    @Excel(name = "音频素材状态", readConverterExp = "0=处理完毕，1待处理，2无需处理")
    private String audioStatus;

    /** 音频素材情感标签 */
    @Excel(name = "音频素材情感标签")
    private String audioEmotion;

    /** 音频素材备注 */
    private String audioNote;

    /** 音频素材时长 */
    private String audioTime;

    /** 音频素材版权（0有版权，1无版权） */
    @Excel(name = "音频素材版权", readConverterExp = "0=有版权，1无版权")
    private String isCopyright;

    /** 是否上架（0上架，1未上架） */
    @Excel(name = "是否上架", readConverterExp = "0=上架，1未上架")
    private String isShow;

    public void setAudioId(Long audioId) 
    {
        this.audioId = audioId;
    }

    public Long getAudioId() 
    {
        return audioId;
    }
    public void setAudioPath(String audioPath)
    {
        this.audioPath = audioPath;
    }

    public String getAudioPath()
    {
        return audioPath;
    }
    public void setAudioName(String audioName) 
    {
        this.audioName = audioName;
    }

    public String getAudioName() 
    {
        return audioName;
    }
    public void setAudioAuthor(String audioAuthor) 
    {
        this.audioAuthor = audioAuthor;
    }

    public String getAudioAuthor() 
    {
        return audioAuthor;
    }
    public void setAudioType(String audioType) 
    {
        this.audioType = audioType;
    }

    public String getAudioType() 
    {
        return audioType;
    }
    public void setAudioStatus(String audioStatus) 
    {
        this.audioStatus = audioStatus;
    }

    public String getAudioStatus() 
    {
        return audioStatus;
    }
    public void setAudioEmotion(String audioEmotion) 
    {
        this.audioEmotion = audioEmotion;
    }

    public String getAudioEmotion() 
    {
        return audioEmotion;
    }
    public void setAudioNote(String audioNote) 
    {
        this.audioNote = audioNote;
    }

    public String getAudioNote() 
    {
        return audioNote;
    }
    public void setAudioTime(String audioTime) 
    {
        this.audioTime = audioTime;
    }

    public String getAudioTime() 
    {
        return audioTime;
    }
    public void setIsCopyright(String isCopyright) 
    {
        this.isCopyright = isCopyright;
    }

    public String getIsCopyright() 
    {
        return isCopyright;
    }
    public void setIsShow(String isShow) 
    {
        this.isShow = isShow;
    }

    public String getIsShow() 
    {
        return isShow;
    }

    @Override
    public String toString() {
        return new ToStringBuilder(this,ToStringStyle.MULTI_LINE_STYLE)
            .append("audioId", getAudioId())
            .append("audioPath", getAudioId())
            .append("audioName", getAudioName())
            .append("audioAuthor", getAudioAuthor())
            .append("audioType", getAudioType())
            .append("audioStatus", getAudioStatus())
            .append("audioEmotion", getAudioEmotion())
            .append("audioNote", getAudioNote())
            .append("audioTime", getAudioTime())
            .append("isCopyright", getIsCopyright())
            .append("isShow", getIsShow())
            .toString();
    }
}
