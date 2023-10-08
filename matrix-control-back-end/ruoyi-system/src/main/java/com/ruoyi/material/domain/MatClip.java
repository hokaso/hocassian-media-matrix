package com.ruoyi.material.domain;

import com.fasterxml.jackson.annotation.JsonFormat;
import com.ruoyi.common.annotation.Excel;
import com.ruoyi.common.core.domain.BaseEntity;
import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;

import java.math.BigDecimal;
import java.util.Date;

/**
 * 视频素材对象 mat_clip
 *
 * @author Hocassian
 * @date 2021-02-22
 */
public class MatClip extends BaseEntity {
    private static final long serialVersionUID = 1L;

    /**
     * 素材id
     */
    private Long materialId;

    /**
     * 素材名称
     */
    @Excel(name = "素材名称")
    private String materialPath;

    /**
     * 素材尺寸
     */
    @Excel(name = "素材尺寸")
    private String materialSize;

    /**
     * 素材时长
     */
    @Excel(name = "素材时长")
    private String materialTime;

    /**
     * 素材标注
     */
    @Excel(name = "素材标注")
    private String materialNote;

    /**
     * 素材打分
     */
    @Excel(name = "素材打分")
    private String materialMark;

    /**
     * 素材状态
     */
    @Excel(name = "素材状态")
    private String materialStatus;

    /**
     * 素材标签
     */
    @Excel(name = "素材标签")
    private String materialTag;

    /**
     * 创建时间
     */
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    @Excel(name = "创建时间", width = 30, dateFormat = "yyyy-MM-dd")
    private Date materialCreate;

    /**
     * 素材类型
     */
    @Excel(name = "素材类型")
    private String materialType;

    /**
     * 分割入点
     */
    private BigDecimal materialStart;

    /**
     * 分割出点
     */
    private BigDecimal materialEnd;

    /**
     * 素材版权
     */
    @Excel(name = "素材版权")
    private String isCopyright;

    /**
     * 是否上架
     */
    @Excel(name = "是否上架")
    private String isShow;

    /**
     * 是否归档
     */
    @Excel(name = "是否归档")
    private String isMerge;

    /**
     * 失败原因
     */
    private String errorInfo;

    private String orderbyMark;

    private String isStabilizer;

    public void setMaterialId(Long materialId) {
        this.materialId = materialId;
    }

    public Long getMaterialId() {
        return materialId;
    }

    public void setMaterialPath(String materialPath) {
        this.materialPath = materialPath;
    }

    public String getMaterialPath() {
        return materialPath;
    }

    public void setMaterialSize(String materialSize) {
        this.materialSize = materialSize;
    }

    public String getMaterialSize() {
        return materialSize;
    }

    public void setMaterialTime(String materialTime) {
        this.materialTime = materialTime;
    }

    public String getMaterialTime() {
        return materialTime;
    }

    public void setMaterialNote(String materialNote) {
        this.materialNote = materialNote;
    }

    public String getMaterialNote() {
        return materialNote;
    }

    public void setMaterialMark(String materialMark) {
        this.materialMark = materialMark;
    }

    public String getMaterialMark() {
        return materialMark;
    }

    public void setMaterialStatus(String materialStatus) {
        this.materialStatus = materialStatus;
    }

    public String getMaterialStatus() {
        return materialStatus;
    }

    public void setMaterialTag(String materialTag) {
        this.materialTag = materialTag;
    }

    public String getMaterialTag() {
        return materialTag;
    }

    public void setMaterialCreate(Date materialCreate) {
        this.materialCreate = materialCreate;
    }

    public Date getMaterialCreate() {
        return materialCreate;
    }

    public void setMaterialType(String materialType) {
        this.materialType = materialType;
    }

    public String getMaterialType() {
        return materialType;
    }

    public void setMaterialStart(BigDecimal materialStart) {
        this.materialStart = materialStart;
    }

    public BigDecimal getMaterialStart() {
        return materialStart;
    }

    public void setMaterialEnd(BigDecimal materialEnd) {
        this.materialEnd = materialEnd;
    }

    public BigDecimal getMaterialEnd() {
        return materialEnd;
    }

    public void setIsCopyright(String isCopyright) {
        this.isCopyright = isCopyright;
    }

    public String getIsCopyright() {
        return isCopyright;
    }

    public void setIsShow(String isShow) {
        this.isShow = isShow;
    }

    public String getIsShow() {
        return isShow;
    }

    public void setIsMerge(String isMerge) {
        this.isMerge = isMerge;
    }

    public String getIsMerge() {
        return isMerge;
    }

    public void setIsStabilizer(String isStabilizer) {
        this.isStabilizer = isStabilizer;
    }

    public String getIsStabilizer() {
        return isStabilizer;
    }

    public void setErrorInfo(String errorInfo) {
        this.errorInfo = errorInfo;
    }

    public String getErrorInfo() {
        return errorInfo;
    }

    public void setOrderbyMark(String orderbyMark) {
        this.orderbyMark = orderbyMark;
    }

    public String getOrderbyMark() {
        return orderbyMark;
    }

    @Override
    public String toString() {
        return new ToStringBuilder(this, ToStringStyle.MULTI_LINE_STYLE)
                .append("materialId", getMaterialId())
                .append("materialPath", getMaterialPath())
                .append("materialSize", getMaterialSize())
                .append("materialTime", getMaterialTime())
                .append("materialNote", getMaterialNote())
                .append("materialMark", getMaterialMark())
                .append("materialStatus", getMaterialStatus())
                .append("materialTag", getMaterialTag())
                .append("materialCreate", getMaterialCreate())
                .append("materialType", getMaterialType())
                .append("materialStart", getMaterialStart())
                .append("materialEnd", getMaterialEnd())
                .append("isCopyright", getIsCopyright())
                .append("isShow", getIsShow())
                .append("isMerge", getIsMerge())
                .append("isStabilizer", getIsStabilizer())
                .append("errorInfo", getErrorInfo())
                .append("orderbyMark", getOrderbyMark())
                .toString();
    }
}
