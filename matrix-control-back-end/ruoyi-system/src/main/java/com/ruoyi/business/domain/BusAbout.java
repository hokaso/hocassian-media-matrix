package com.ruoyi.business.domain;

import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.ruoyi.common.annotation.Excel;
import com.ruoyi.common.core.domain.BaseEntity;

/**
 * 信息管理对象 bus_about
 * 
 * @author Hocassian
 * @date 2021-04-22
 */
public class BusAbout extends BaseEntity
{
    private static final long serialVersionUID = 1L;

    /** 组织信息id */
    private Long aboutId;

    /** 组织简介 */
    @Excel(name = "组织简介")
    private String aboutInfo;

    /** 组织简介 */
    @Excel(name = "组织关键字")
    private String aboutKeyword;

    /** 组织宣言 */
    @Excel(name = "组织宣言")
    private String aboutDeclaration;

    /** 大众平台 */
    private String aboutQrcode;

    /** 组织名称 */
    @Excel(name = "组织名称")
    private String aboutName;

    /** 联系方式 */
    @Excel(name = "联系方式")
    private String aboutContact;

    /** 组织图标 */
    private String aboutIcon;

    /** 是否上架 */
    @Excel(name = "是否上架")
    private String aboutStatus;

    /** 页脚声明 */
    @Excel(name = "页脚声明")
    private String aboutCopyright;

    /** 页脚备案 */
    @Excel(name = "页脚备案")
    private String aboutRecord;

    public void setAboutId(Long aboutId) 
    {
        this.aboutId = aboutId;
    }

    public Long getAboutId() 
    {
        return aboutId;
    }
    public void setAboutInfo(String aboutInfo) 
    {
        this.aboutInfo = aboutInfo;
    }

    public String getAboutInfo() 
    {
        return aboutInfo;
    }
    public void setAboutDeclaration(String aboutDeclaration) 
    {
        this.aboutDeclaration = aboutDeclaration;
    }

    public String getAboutDeclaration() 
    {
        return aboutDeclaration;
    }
    public void setAboutQrcode(String aboutQrcode) 
    {
        this.aboutQrcode = aboutQrcode;
    }

    public String getAboutQrcode() 
    {
        return aboutQrcode;
    }
    public void setAboutName(String aboutName) 
    {
        this.aboutName = aboutName;
    }

    public String getAboutName() 
    {
        return aboutName;
    }
    public void setAboutContact(String aboutContact) 
    {
        this.aboutContact = aboutContact;
    }

    public String getAboutContact() 
    {
        return aboutContact;
    }
    public void setAboutIcon(String aboutIcon) 
    {
        this.aboutIcon = aboutIcon;
    }

    public String getAboutIcon() 
    {
        return aboutIcon;
    }
    public void setAboutStatus(String aboutStatus) 
    {
        this.aboutStatus = aboutStatus;
    }

    public String getAboutStatus() 
    {
        return aboutStatus;
    }

    public String getAboutCopyright() {
        return aboutCopyright;
    }

    public void setAboutCopyright(String aboutCopyright) {
        this.aboutCopyright = aboutCopyright;
    }

    public String getAboutRecord() {
        return aboutRecord;
    }

    public void setAboutRecord(String aboutRecord) {
        this.aboutRecord = aboutRecord;
    }

    public String getAboutKeyword() {
        return aboutKeyword;
    }

    public void setAboutKeyword(String aboutKeyword) {
        this.aboutKeyword = aboutKeyword;
    }

    @Override
    public String toString() {
        return new ToStringBuilder(this,ToStringStyle.MULTI_LINE_STYLE)
            .append("aboutId", getAboutId())
            .append("aboutInfo", getAboutInfo())
            .append("aboutKeyword", getAboutKeyword())
            .append("aboutDeclaration", getAboutDeclaration())
            .append("aboutQrcode", getAboutQrcode())
            .append("aboutName", getAboutName())
            .append("aboutContact", getAboutContact())
            .append("aboutIcon", getAboutIcon())
            .append("aboutStatus", getAboutStatus())
            .append("aboutCopyright", getAboutCopyright())
            .append("aboutRecord", getAboutRecord())
            .toString();
    }
}
