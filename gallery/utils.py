# -*- coding: utf-8 -*-
from pymongo import MongoClient
from wechat_sdk import WechatBasic
from wechat_sdk import WechatConf

db_cli = MongoClient()['wechat']

conf = WechatConf(
    token='MemoryGallery',
    appid='wxaf15cef60cb02975',
    appsecret='9174c5455a7cbe273b0f35cd1db34fa5',
    encrypt_mode='normal',  # 可选项：normal/compatible/safe，分别对应于 明文/兼容/安全 模式
    encoding_aes_key='FiVEeh1m1Xnp8O8KxYMxAZKOUtlpufsMC04Y7MxOMb4'  # 如果传入此值则必须保证同时传入 token, appid
)

wechat = WechatBasic(conf=conf)
