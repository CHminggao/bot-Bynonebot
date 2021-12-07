'''
Author: GM
Date: 2021-11-23 18:28:50
LastEditors: GM
LastEditTime: 2021-12-06 21:23:19
Description: file content
'''
from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here
    class Config:
        extra = "ignore"
        