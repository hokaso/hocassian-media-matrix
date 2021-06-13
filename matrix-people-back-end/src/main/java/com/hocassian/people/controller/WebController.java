package com.hocassian.people.controller;

import com.hocassian.people.controller.base.BaseController;
import com.hocassian.people.domain.web.ConnectWeb;
import com.hocassian.people.domain.web.PersonWeb;
import com.hocassian.people.service.web.WebService;
import com.hocassian.people.transport.AjaxResult;
import com.hocassian.people.transport.Result;
import org.neo4j.driver.Record;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * 功能描述：
 *
 * @author Hocassian
 * @date 2021-01-16 11:09
 */
@RestController
@RequestMapping("/people/web")
public class WebController extends BaseController {

    @Autowired
    private WebService webService;

    @PreAuthorize("@ss.hasPermi('*:*:*')")
    @GetMapping("/map")
    public Result getPersonWebMap() {
        List<Record> list = webService.selectPersonWebMap();
        return getDataResult(list);
    }

    @PreAuthorize("@ss.hasPermi('*:*:*')")
    @GetMapping("/list")
    public Result getPersonWebList() {
        List<PersonWeb> list = webService.selectPersonWebList();
        return getDataResult(list);
    }

    @PreAuthorize("@ss.hasPermi('*:*:*')")
    @GetMapping("/search/{personWebName}")
    public Result getPersonWebSearchList(@PathVariable("personWebName") String personWebName) {
        List<PersonWeb> list = webService.selectPersonWebSearchList(personWebName);
        return getDataResult(list);
    }

    @PreAuthorize("@ss.hasPermi('*:*:*')")
    @GetMapping("/search/{personWebId}/{personWebName}")
    public Result getPersonWebSearchListOther(@PathVariable("personWebName") String personWebName, @PathVariable("personWebId") String personWebId) {
        List<PersonWeb> list = webService.selectPersonWebSearchListOther(personWebName, personWebId);
        return getDataResult(list);
    }

    @PreAuthorize("@ss.hasPermi('*:*:*')")
    @GetMapping(value = "/person/{personWebId}")
    public AjaxResult getPersonWebInfo(@PathVariable("personWebId") String personWebId) {
        return AjaxResult.success(webService.selectPersonWebById(personWebId));
    }

    @PreAuthorize("@ss.hasPermi('*:*:*')")
    @PostMapping("/person")
    public AjaxResult addPersonWeb(@RequestBody PersonWeb personWeb) {
        return toAjax(webService.insertPersonWeb(personWeb));
    }

    @PreAuthorize("@ss.hasPermi('*:*:*')")
    @PutMapping("/person")
    public AjaxResult editPersonWeb(@RequestBody PersonWeb personWeb) {
        return toAjax(webService.updatePersonWeb(personWeb));
    }

    @PreAuthorize("@ss.hasPermi('*:*:*')")
    @DeleteMapping("/person/{personWebId}")
    public AjaxResult removePersonWeb(@PathVariable String personWebId) {
        try{
            int rsg = webService.deletePersonWeb(personWebId);
            return toAjax(rsg);
        } catch (Exception e){
            return AjaxResult.error(500, "此节点仍与其他节点有关联关系！");
        }
    }

    @PreAuthorize("@ss.hasPermi('*:*:*')")
    @GetMapping(value = "/connect/{connectWebId}")
    public AjaxResult getInfoConnectWeb(@PathVariable("connectWebId") String connectWebId) {
        return AjaxResult.success(webService.selectConnectWebById(connectWebId));
    }

    @PreAuthorize("@ss.hasPermi('*:*:*')")
    @PostMapping("/connect")
    public AjaxResult addConnectWeb(@RequestBody ConnectWeb connectWeb) {
        return toAjax(webService.insertConnectWeb(connectWeb));
    }

    @PreAuthorize("@ss.hasPermi('*:*:*')")
    @PutMapping("/connect")
    public AjaxResult editConnectWeb(@RequestBody ConnectWeb connectWeb) {
        return toAjax(webService.updateConnectWeb(connectWeb));
    }

    @PreAuthorize("@ss.hasPermi('*:*:*')")
    @DeleteMapping("/connect/{connectWebId}")
    public AjaxResult removeConnectWeb(@PathVariable String connectWebId) {
        return toAjax(webService.deleteConnectWeb(connectWebId));
    }
}
