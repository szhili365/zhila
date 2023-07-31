# -*- encoding: utf-8 -*-

import os

from typing import List

from setting import BASE_DIR
from base import ParamTuple, Issue


class BaseTool(object):

    def __init__(self, params: ParamTuple) -> None:
        self.params: ParamTuple = params
        self.langs: List[str] = list()
        self.tool_dir: str = os.path.join(BASE_DIR, "tool", "zhila")
        self.out_dir: str = os.path.join(self.params.out_dir, self.__class__.__name__)
        if not os.path.exists(self.out_dir):
            os.makedirs(self.out_dir)

    def languages(self) -> List[str]:
        return self.langs

    def run(self) -> List[Issue]: ...
