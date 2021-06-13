package com.hocassian.people.domain.web;

/**
 * 功能描述：
 *
 * @author Hocassian
 * @date 2021-01-15 22:13
 */
public class ConnectWeb {

    private String connectWebId;

    private String connectWebName;

    private String connectWebInfo;

    private String personWebIdAlpha;

    private String personWebIdBeta;

    private String personWebIdAlphaName;

    private String personWebIdBetaName;

    public String getPersonWebIdAlphaName() {
        return personWebIdAlphaName;
    }

    public void setPersonWebIdAlphaName(String personWebIdAlphaName) {
        this.personWebIdAlphaName = personWebIdAlphaName;
    }

    public String getPersonWebIdBetaName() {
        return personWebIdBetaName;
    }

    public void setPersonWebIdBetaName(String personWebIdBetaName) {
        this.personWebIdBetaName = personWebIdBetaName;
    }

    public String getConnectWebId() {
        return connectWebId;
    }

    public void setConnectWebId(String connectWebId) {
        this.connectWebId = connectWebId;
    }

    public String getConnectWebName() {
        return connectWebName;
    }

    public void setConnectWebName(String connectWebName) {
        this.connectWebName = connectWebName;
    }

    public String getConnectWebInfo() {
        return connectWebInfo;
    }

    public void setConnectWebInfo(String connectWebInfo) {
        this.connectWebInfo = connectWebInfo;
    }

    public String getPersonWebIdAlpha() {
        return personWebIdAlpha;
    }

    public void setPersonWebIdAlpha(String personWebIdAlpha) {
        this.personWebIdAlpha = personWebIdAlpha;
    }

    public String getPersonWebIdBeta() {
        return personWebIdBeta;
    }

    public void setPersonWebIdBeta(String personWebIdBeta) {
        this.personWebIdBeta = personWebIdBeta;
    }

    @Override
    public String toString() {
        return "ConnectWeb{" +
                "connectWebId='" + connectWebId + '\'' +
                ", connectWebName='" + connectWebName + '\'' +
                ", connectWebInfo='" + connectWebInfo + '\'' +
                ", personWebIdAlpha='" + personWebIdAlpha + '\'' +
                ", personWebIdBeta='" + personWebIdBeta + '\'' +
                ", personWebIdAlphaName='" + personWebIdAlphaName + '\'' +
                ", personWebIdBetaName='" + personWebIdBetaName + '\'' +
                '}';
    }
}
