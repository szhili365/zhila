# -*- encoding: utf-8 -*-

import os
import json

from typing import List

from base import LANG_EXT_MAP, Issue, ParamTuple, run_cmd
from tool.base import BaseTool


class Tool_4(BaseTool):
    def __init__(self, params: ParamTuple) -> None:
        super().__init__(params)
        self.langs: List[str] = [
            "cpp",
            "oc",
            "cs",
            "java",
            "js",
            "ts",
            "php",
            "go",
            "python",
            "kotlin",
            "lua",
            "ruby",
            "scala",
            "swift",
            "dart",
            "rust",
        ]
        self.exts: List[str] = list()
        for lang in self.langs:
            if lang in LANG_EXT_MAP:
                self.exts.extend(LANG_EXT_MAP[lang])

    def run(self) -> List[Issue]:
        # cmd
        cmd = [
            os.path.join(self.tool_dir, "bin", "Tool_4"),
            "--service",
            self.params.service,
            "--check-code",
            self.params.check_code,
            "-r",
            self.params.project_dir,
            "-o",
            self.out_dir,
        ]
        run_cmd(cmd)

        # handle result
        out_path = os.path.join(self.out_dir, "issues.json")
        f = open(out_path)
        result = json.load(f, object_hook=lambda d: Issue(*d.values()))
        f.close()
        return result
