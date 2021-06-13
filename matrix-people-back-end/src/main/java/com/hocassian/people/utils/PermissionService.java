package com.hocassian.people.utils;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import com.alibaba.fastjson.JSON;

import javax.servlet.http.HttpServletRequest;
import java.util.Map;

/**
 * RuoYi首创 自定义权限实现，ss取自SpringSecurity首字母
 * 
 * @author ruoyi
 */
@Service("ss")
public class PermissionService
{

    @Value("${token.header}")
    private String header;

    @Value("${token.secret}")
    private String secret;

    @Autowired
    private RedisCache redisCache;

    String LOGIN_TOKEN_KEY = "login_tokens:";

    String TOKEN_PREFIX = "Bearer ";

    String LOGIN_USER_KEY = "login_user_key";

    /**
     * 验证用户是否具备某权限
     * 
     * @param permission 权限字符串
     * @return 用户是否具备某权限
     */
    public boolean hasPermi(String permission)
    {
        if (StringUtils.isEmpty(permission))
        {
            return false;
        }

        // 获取请求携带的令牌
        String token = getToken(ServletUtils.getRequest());
        if (StringUtils.isNotEmpty(token))
        {
            Claims claims = parseToken(token);
            // 解析对应的权限以及用户信息
            String uuid = (String) claims.get(LOGIN_USER_KEY);
            String userKey = getTokenKey(uuid);
            Map user = redisCache.getCacheObject(userKey);
            return !StringUtils.isNull(user);
        }
        return false;
    }

    /**
     * 获取请求token
     *
     * @param request
     * @return token
     */
    private String getToken(HttpServletRequest request)
    {
        String token = request.getHeader(header);
        if (StringUtils.isNotEmpty(token) && token.startsWith(TOKEN_PREFIX))
        {
            token = token.replace(TOKEN_PREFIX, "");
        }
        return token;
    }

    /**
     * 从令牌中获取数据声明
     *
     * @param token 令牌
     * @return 数据声明
     */
    private Claims parseToken(String token)
    {
        return Jwts.parser()
                .setSigningKey(secret)
                .parseClaimsJws(token)
                .getBody();
    }

    private String getTokenKey(String uuid)
    {
        return LOGIN_TOKEN_KEY + uuid;
    }

}
