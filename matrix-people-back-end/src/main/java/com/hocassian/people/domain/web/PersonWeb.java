package com.hocassian.people.domain.web;

/**
 * 功能描述：
 *
 * @author Hocassian
 * @date 2021-01-15 22:12
 */
public class PersonWeb {

    private String personWebId;

    private String personWebName;

    private String personWebPic;

    private String personWebShow;

    private String personWebLink;

    private String personWebPlatform;

    private String personWebField;

    private String personWebInfo;

    private String personWebKey;

    public String getPersonWebId() {
        return personWebId;
    }

    public void setPersonWebId(String personWebId) {
        this.personWebId = personWebId;
    }

    public String getPersonWebName() {
        return personWebName;
    }

    public void setPersonWebName(String personWebName) {
        this.personWebName = personWebName;
    }

    public String getPersonWebPlatform() {
        return personWebPlatform;
    }

    public void setPersonWebPlatform(String personWebPlatform) {
        this.personWebPlatform = personWebPlatform;
    }

    public String getPersonWebField() {
        return personWebField;
    }

    public void setPersonWebField(String personWebField) {
        this.personWebField = personWebField;
    }

    public String getPersonWebInfo() {
        return personWebInfo;
    }

    public void setPersonWebInfo(String personWebInfo) {
        this.personWebInfo = personWebInfo;
    }

    public String getPersonWebKey() {
        return personWebKey;
    }

    public void setPersonWebKey(String personWebKey) {
        this.personWebKey = personWebKey;
    }

    public String getPersonWebPic() {
        return personWebPic;
    }

    public void setPersonWebPic(String personWebPic) {
        this.personWebPic = personWebPic;
    }

    public String getPersonWebShow() {
        return personWebShow;
    }

    public void setPersonWebShow(String personWebShow) {
        this.personWebShow = personWebShow;
    }

    public String getPersonWebLink() {
        return personWebLink;
    }

    public void setPersonWebLink(String personWebLink) {
        this.personWebLink = personWebLink;
    }

    @Override
    public String toString() {
        return "PersonWeb{" +
                "personWebId='" + personWebId + '\'' +
                ", personWebName='" + personWebName + '\'' +
                ", personWebPic='" + personWebPic + '\'' +
                ", personWebShow='" + personWebShow + '\'' +
                ", personWebLink='" + personWebLink + '\'' +
                ", personWebPlatform='" + personWebPlatform + '\'' +
                ", personWebField='" + personWebField + '\'' +
                ", personWebInfo='" + personWebInfo + '\'' +
                ", personWebKey='" + personWebKey + '\'' +
                '}';
    }
}
