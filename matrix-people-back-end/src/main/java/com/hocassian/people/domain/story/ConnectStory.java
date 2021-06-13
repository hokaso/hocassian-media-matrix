package com.hocassian.people.domain.story;

/**
 * 功能描述：
 *
 * @author Hocassian
 * @date 2021-01-15 22:12
 */
public class ConnectStory {

    private String connectStoryId;

    private String connectStoryName;

    private String connectStoryInfo;

    private String personStoryIdAlpha;

    private String personStoryIdBeta;

    public String getPersonStoryIdAlpha() {
        return personStoryIdAlpha;
    }

    public void setPersonStoryIdAlpha(String personStoryIdAlpha) {
        this.personStoryIdAlpha = personStoryIdAlpha;
    }

    public String getPersonStoryIdBeta() {
        return personStoryIdBeta;
    }

    public void setPersonStoryIdBeta(String personStoryIdBeta) {
        this.personStoryIdBeta = personStoryIdBeta;
    }

    public String getConnectStoryId() {
        return connectStoryId;
    }

    public void setConnectStoryId(String connectStoryId) {
        this.connectStoryId = connectStoryId;
    }

    public String getConnectStoryName() {
        return connectStoryName;
    }

    public void setConnectStoryName(String connectStoryName) {
        this.connectStoryName = connectStoryName;
    }

    public String getConnectStoryInfo() {
        return connectStoryInfo;
    }

    public void setConnectStoryInfo(String connectStoryInfo) {
        this.connectStoryInfo = connectStoryInfo;
    }

    @Override
    public String toString() {
        return "ConnectStory{" +
                "connectStoryId='" + connectStoryId + '\'' +
                ", connectStoryName='" + connectStoryName + '\'' +
                ", connectStoryInfo='" + connectStoryInfo + '\'' +
                ", personStoryIdAlpha='" + personStoryIdAlpha + '\'' +
                ", personStoryIdBeta='" + personStoryIdBeta + '\'' +
                '}';
    }
}
