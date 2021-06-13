package com.hocassian.people.controller;

import com.hocassian.people.controller.base.BaseController;
import com.hocassian.people.domain.story.ConnectStory;
import com.hocassian.people.domain.story.PersonStory;
import com.hocassian.people.service.story.StoryService;
import com.hocassian.people.transport.AjaxResult;
import com.hocassian.people.transport.Result;
import org.neo4j.driver.Record;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * 功能描述：
 *
 * @author Hocassian
 * @date 2021-01-16 11:09
 */
@RestController
@RequestMapping("/people/story")
public class StoryController extends BaseController {

    @Autowired
    private StoryService storyService;

    @GetMapping("/list")
    public Result getPersonStoryList() {
        List<Record> list = storyService.selectPersonStoryList();
        return getDataResult(list);
    }

    @GetMapping(value = "/person/{personStoryId}")
    public AjaxResult getPersonStoryInfo(@PathVariable("personStoryId") String personStoryId) {
        return AjaxResult.success(storyService.selectPersonStoryById(personStoryId));
    }

    @PostMapping("/person")
    public AjaxResult addPersonStory(@RequestBody PersonStory personStory) {
        return toAjax(storyService.insertPersonStory(personStory));
    }

    @PutMapping("/person")
    public AjaxResult editPersonStory(@RequestBody PersonStory personStory) {
        return toAjax(storyService.updatePersonStory(personStory));
    }

    @DeleteMapping("/person/{personStoryId}")
    public AjaxResult removePersonStory(@PathVariable String personStoryId) {
        return toAjax(storyService.deletePersonStory(personStoryId));
    }

    @GetMapping(value = "/connect/{connectStoryId}")
    public AjaxResult getInfoConnectStory(@PathVariable("connectStoryId") String connectStoryId) {
        return AjaxResult.success(storyService.selectConnectStoryById(connectStoryId));
    }

    @PostMapping("/connect")
    public AjaxResult addConnectStory(@RequestBody ConnectStory connectStory) {
        return toAjax(storyService.insertConnectStory(connectStory));
    }

    @PutMapping("/connect")
    public AjaxResult editConnectStory(@RequestBody ConnectStory connectStory) {
        return toAjax(storyService.updateConnectStory(connectStory));
    }

    @DeleteMapping("/connect/{connectStoryId}")
    public AjaxResult removeConnectStory(@PathVariable String connectStoryId) {
        return toAjax(storyService.deleteConnectStory(connectStoryId));
    }
}
