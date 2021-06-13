package com.ruoyi.framework.config;

import org.springframework.amqp.core.Binding;

import org.springframework.amqp.core.BindingBuilder;
import org.springframework.amqp.core.DirectExchange;
import org.springframework.amqp.core.Queue;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.amqp.support.converter.Jackson2JsonMessageConverter;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.amqp.rabbit.connection.ConnectionFactory;

/**
 * 功能描述：
 *
 * @author Hocassian
 * @date 2020-03-07 13:26
 */
@Configuration
public class RabbitConfig {

    /**
     * 注入消息队列组件
     * @param connectionFactory 连接池
     * @return rabbitTemplate
     */
    @Bean
    public RabbitTemplate rabbitTemplate(final ConnectionFactory connectionFactory) {
        final RabbitTemplate rabbitTemplate = new RabbitTemplate(connectionFactory);
        rabbitTemplate.setMessageConverter(producerJackson2MessageConverter());
        return rabbitTemplate;
    }

    /**
     * 建立队列
     */

    @Bean
    public Queue clipOptionalQueue(){
        return new Queue("clipOptionalQueue",true);
    }

    @Bean
    public Queue audioOptionalQueue(){
        return new Queue("audioOptionalQueue",true);
    }

    @Bean
    public Queue imageOptionalQueue(){
        return new Queue("imageOptionalQueue",true);
    }

    /**
     * 建立交换机
     */

    DirectExchange clipOptionalExchange(){
        return new DirectExchange("clipOptionalExchange");
    }

    DirectExchange audioOptionalExchange(){
        return new DirectExchange("audioOptionalExchange");
    }

    DirectExchange imageOptionalExchange(){
        return new DirectExchange("imageOptionalExchange");
    }

    /**
     * 绑定路由
     */
    @Bean
    Binding bindingClipOptional(){
        return BindingBuilder.bind(clipOptionalQueue()).to(clipOptionalExchange()).with("clipOptionalRouting");
    }

    @Bean
    Binding bindingAudioSending(){
        return BindingBuilder.bind(audioOptionalQueue()).to(audioOptionalExchange()).with("audioOptionalRouting");
    }

    @Bean
    Binding bindingImageSending(){
        return BindingBuilder.bind(imageOptionalQueue()).to(imageOptionalExchange()).with("imageOptionalRouting");
    }

    /**
     * 注入消息转换插件（用于将java发出的消息转换为RabbitMQ可识别的语言）
     */
    @Bean
    public Jackson2JsonMessageConverter producerJackson2MessageConverter() {
        return new Jackson2JsonMessageConverter();
    }

}