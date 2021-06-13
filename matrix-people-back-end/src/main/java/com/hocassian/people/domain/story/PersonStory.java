package com.hocassian.people.domain.story;

/**
 * 功能描述：
 *
 * @author Hocassian
 * @date 2021-01-15 22:09
 */
public class PersonStory {

    private String personStoryId;

    private String personStoryName;

    private String personStorySex;

    private String personStoryInfo;

    private String personStoryFeature;

    public String getPersonStoryId() {
        return personStoryId;
    }

    public void setPersonStoryId(String personStoryId) {
        this.personStoryId = personStoryId;
    }

    public String getPersonStoryName() {
        return personStoryName;
    }

    public void setPersonStoryName(String personStoryName) {
        this.personStoryName = personStoryName;
    }

    public String getPersonStorySex() {
        return personStorySex;
    }

    public void setPersonStorySex(String personStorySex) {
        this.personStorySex = personStorySex;
    }

    public String getPersonStoryInfo() {
        return personStoryInfo;
    }

    public void setPersonStoryInfo(String personStoryInfo) {
        this.personStoryInfo = personStoryInfo;
    }

    public String getPersonStoryFeature() {
        return personStoryFeature;
    }

    public void setPersonStoryFeature(String personStoryFeature) {
        this.personStoryFeature = personStoryFeature;
    }

    @Override
    public String toString() {
        return "PersonStory{" +
                "personStoryId='" + personStoryId + '\'' +
                ", personStoryName='" + personStoryName + '\'' +
                ", personStorySex='" + personStorySex + '\'' +
                ", personStoryInfo='" + personStoryInfo + '\'' +
                ", personStoryFeature='" + personStoryFeature + '\'' +
                '}';
    }
}
