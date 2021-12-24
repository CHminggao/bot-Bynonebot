'''
Author: GM
Date: 2021-12-07 16:33:42
LastEditors: GM
LastEditTime: 2021-12-24 10:51:48
Description: file content
'''
from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    class Config:
        extra = "ignore"
