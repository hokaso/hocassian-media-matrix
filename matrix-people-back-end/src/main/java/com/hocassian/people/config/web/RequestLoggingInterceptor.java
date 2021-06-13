package com.hocassian.people.config.web;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.servlet.ModelAndView;
import org.springframework.web.servlet.handler.HandlerInterceptorAdapter;
import org.springframework.web.servlet.resource.ResourceHttpRequestHandler;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.time.LocalDateTime;
import java.time.temporal.ChronoUnit;

/**
 * 请求的时间记录
 */
public class RequestLoggingInterceptor extends HandlerInterceptorAdapter {

    private Logger logger = LoggerFactory.getLogger(RequestLoggingInterceptor.class);

    /**
     * 请求时间记录用的key
     */
    private static final String REQUEST_CURRENT_TIME = "REQUEST_CURRENT_TIME";


    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {

        if (handler instanceof ResourceHttpRequestHandler)
            return true;

        String method = request.getMethod();
        String uri = request.getRequestURI();
        String ip = "";//IpUtils.getRealIpAddress(request);

        logger.info("Request ====> {} {}, ip:{}", method, uri, ip);

        request.setAttribute(REQUEST_CURRENT_TIME, LocalDateTime.now());

        return true;
    }

    @Override
    public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView) throws Exception {

        if (handler instanceof ResourceHttpRequestHandler)
            return;

        if (logger.isDebugEnabled()) {

            LocalDateTime requestTime = (LocalDateTime) request.getAttribute(REQUEST_CURRENT_TIME);

            final long timeConsuming = ChronoUnit.MILLIS.between(requestTime, LocalDateTime.now());

            logger.debug("Controller response time consuming {}ms", timeConsuming);
        }
    }

    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {

        int status = response.getStatus();
        String method = request.getMethod();
        String uri = request.getRequestURI();

        LocalDateTime requestTime = (LocalDateTime) request.getAttribute(REQUEST_CURRENT_TIME);

        if (requestTime != null) {
            request.removeAttribute(REQUEST_CURRENT_TIME);
            long timeConsuming = ChronoUnit.MILLIS.between(requestTime, LocalDateTime.now());
            logger.info("Response {} <==== {} {}; time consuming {}ms", status, method, uri, timeConsuming);
        }
    }


}
