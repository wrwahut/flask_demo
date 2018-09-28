# flask_demo
以下接口都是POST方法

接口（1）：登录

    url:    http://47.99.143.9:10002/resource/user/sign_in
    
    params: 参数
            {
              "phone": ""    
            }
            
    正确返回示例： (登录成功接口，在after_request的hook中去除相关信息，如果前端需要，也可以给出)
            {
              
            }
            
    错误返回示例：
            {
              "re": "402",
              "msg": "param_error"
              "data": {}
            }
            或者：
            {
              "re": "404",
              "msg": "phone_none",
              "data": {}
            }
            
            
 接口（2）：获取当日未打印的订单列表信息
 
    url: http://47.99.143.9:10002/resource/user/get_user_order
    
    params: 空
          {
          }
          
    返回示例：
          {
            "re" : "200",
            "msg": "success",
            "data": [
              {
                "add_time": "2018-09-28 14:47:23",    // string   下单时间
                "fee": "0.9",                         // string   
                "goods": [                            // []       商品信息
                   {
                      "box_fee": "0.00", 
                      "count": "1", 
                      "gid": "4412", 
                      "id": "216771", 
                      "name": "\\u9521\\u7eb8\\u7c89\\u4e1d \\u5f00\\u82b1\\u80a0\\u91d1\\u9488\\u83c7\\u706b\\u817f\\u80a0", 
                      "ori_price": "0.00", 
                      "price": "10.50", 
                      "shop_id": "183", 
                      "thumb": ".\\/upload\\/image\\/dining\\/goods\\/20180406163937353_thumb.jpg", 
                      "total_price": 10.5, 
                      "updown": "1", 
                      "user_id": "11574"
                   }
                 ],
                "message": "",                              // string  留言
                "order_num": "QJ201809281447237971",        // string  订单号
                "pay_time": "2018-09-28 14:47:32",          // stying  支付时间
                "person_count": 1,                          // string  用餐人数
                "sender_phone": null,                       // string  送餐人手机
                "shop_name": "\u7edd\u5473\u82b1\u7532",    // string  商家名称
                "shop_phone": "18956537890",                // string  店铺手机号
                "total_box_fee": 0.0,          
                "user_address": "1(\u7537\u5bbf\u820d)629", // string  收获地址
                "user_name": "\u8a79\u6c38\u6770",          // string  收货人
                "user_phone": "18155485553"                 // string  收获电话
              }
            ]
          }
          
          
  接口（3）：获取已经打印的订单列表信息
  
      url： http://47.99.143.9:10002/resource/user/get_printed_orders
      
      params： kong
      
      返回示例：
         {
            "re" : "200",
            "msg": "success",
            "data": [
              {
                "add_time": "2018-09-28 14:47:23",
                "fee": "0.9",
                "goods": [
                   {
                      "box_fee": "0.00", 
                      "count": "1", 
                      "gid": "4412", 
                      "id": "216771", 
                      "name": "\\u9521\\u7eb8\\u7c89\\u4e1d \\u5f00\\u82b1\\u80a0\\u91d1\\u9488\\u83c7\\u706b\\u817f\\u80a0", 
                      "ori_price": "0.00", 
                      "price": "10.50", 
                      "shop_id": "183", 
                      "thumb": ".\\/upload\\/image\\/dining\\/goods\\/20180406163937353_thumb.jpg", 
                      "total_price": 10.5, 
                      "updown": "1", 
                      "user_id": "11574"
                   }
                 ],
                "message": "", 
                "order_num": "QJ201809281447237971", 
                "pay_time": "2018-09-28 14:47:32", 
                "person_count": 1, 
                "sender_phone": null, 
                "shop_name": "\u7edd\u5473\u82b1\u7532", 
                "shop_phone": "18956537890", 
                "total_box_fee": 0.0, 
                "user_address": "1(\u7537\u5bbf\u820d)629", 
                "user_name": "\u8a79\u6c38\u6770", 
                "user_phone": "18155485553"
              }
            ]
          }
          
 接口（4） ：打印订单（用来过滤打印订单）
 
        url: http://47.99.143.9:10002/resource/user/print_order
        
        params: 
            {
              "order_num": ""    // string  订单号
            }
            
        返回示范：
            {
               "re": "200",
               "msg": "success",
               "data": {}
            }
            
            
  接口（5）： 获取当日所有订单列表信息
  
        url: http://47.99.143.9:10002/resource/user/print_order
        
        params:
          {
             "startNum": "",
             "pageSize": ""
          }
          
         返回示例：
            {
              "re": "200",
              "msg": "success",
              "data":{
                "detail": [
                    {
                      "add_time": "2018-09-28 14:47:23",
                      "fee": "0.9",
                      "goods": [
                         {
                            "box_fee": "0.00", 
                            "count": "1", 
                            "gid": "4412", 
                            "id": "216771", 
                            "name": "\\u9521\\u7eb8\\u7c89\\u4e1d \\u5f00\\u82b1\\u80a0\\u91d1\\u9488\\u83c7\\u706b\\u817f\\u80a0", 
                            "ori_price": "0.00", 
                            "price": "10.50", 
                            "shop_id": "183", 
                            "thumb": ".\\/upload\\/image\\/dining\\/goods\\/20180406163937353_thumb.jpg", 
                            "total_price": 10.5, 
                            "updown": "1", 
                            "user_id": "11574"
                         }
                       ],
                      "message": "", 
                      "order_num": "QJ201809281447237971", 
                      "pay_time": "2018-09-28 14:47:32", 
                      "person_count": 1, 
                      "sender_phone": null, 
                      "shop_name": "\u7edd\u5473\u82b1\u7532", 
                      "shop_phone": "18956537890", 
                      "total_box_fee": 0.0, 
                      "user_address": "1(\u7537\u5bbf\u820d)629", 
                      "user_name": "\u8a79\u6c38\u6770", 
                      "user_phone": "18155485553"
                    }
                ],
                "total_num": 1
              }
            }
