package com.ruoyi.material.domain;

import com.ruoyi.common.annotation.Excel;
import com.ruoyi.common.core.domain.BaseEntity;
import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;

import java.math.BigDecimal;

/**
 * 图片素材对象 mat_image
 * 
 * @author Hocassian
 * @date 2021-03-04
 */
public class MatImage extends BaseEntity
{
    private static final long serialVersionUID = 1L;

    /** 图片素材id */
    private Long imageId;

    /** 图片素材路径 */
    @Excel(name = "图片素材路径")
    private String imagePath;

    /** 图片素材标注 */
    @Excel(name = "图片素材标注")
    private String imageNote;

    /** 图片素材尺寸 */
    private String imageSize;

    /** 图片素材标签 */
    @Excel(name = "图片素材标签")
    private String imageTag;

    /** 图片素材打分 */
    @Excel(name = "图片素材打分")
    private BigDecimal imageMark;

    /** 图片素材状态 */
    @Excel(name = "图片素材状态")
    private String imageStatus;

    /** 图片素材类型（0高质素材，1普通素材） */
    @Excel(name = "图片素材类型", readConverterExp = "0=高质素材，1普通素材")
    private String imageType;

    /** 素材版权（0有版权，1无版权） */
    @Excel(name = "素材版权", readConverterExp = "0=有版权，1无版权")
    private String isCopyright;

    /** 是否上架（0上架，1未上架） */
    @Excel(name = "是否上架", readConverterExp = "0=上架，1未上架")
    private String isShow;

    public void setImageId(Long imageId) 
    {
        this.imageId = imageId;
    }

    public Long getImageId() 
    {
        return imageId;
    }
    public void setImagePath(String imagePath) 
    {
        this.imagePath = imagePath;
    }

    public String getImagePath() 
    {
        return imagePath;
    }
    public void setImageNote(String imageNote) 
    {
        this.imageNote = imageNote;
    }

    public String getImageNote() 
    {
        return imageNote;
    }
    public void setImageSize(String imageSize) 
    {
        this.imageSize = imageSize;
    }

    public String getImageSize() 
    {
        return imageSize;
    }
    public void setImageTag(String imageTag) 
    {
        this.imageTag = imageTag;
    }

    public String getImageTag() 
    {
        return imageTag;
    }
    public void setImageMark(BigDecimal imageMark) 
    {
        this.imageMark = imageMark;
    }

    public BigDecimal getImageMark() 
    {
        return imageMark;
    }
    public void setImageStatus(String imageStatus) 
    {
        this.imageStatus = imageStatus;
    }

    public String getImageStatus() 
    {
        return imageStatus;
    }
    public void setImageType(String imageType) 
    {
        this.imageType = imageType;
    }

    public String getImageType() 
    {
        return imageType;
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
            .append("imageId", getImageId())
            .append("imagePath", getImagePath())
            .append("imageNote", getImageNote())
            .append("imageSize", getImageSize())
            .append("imageTag", getImageTag())
            .append("imageMark", getImageMark())
            .append("imageStatus", getImageStatus())
            .append("imageType", getImageType())
            .append("isCopyright", getIsCopyright())
            .append("isShow", getIsShow())
            .toString();
    }
}
