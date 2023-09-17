# -*- encoding: utf-8 -*-

import os
import json

from typing import List

from base import LANG_EXT_MAP, Issue, Ref, ParamTuple, run_cmd
from tool.base import BaseTool
from setting import BASE_DIR


class Tool_6(BaseTool):
    def __init__(self, params: ParamTuple) -> None:
        super().__init__(params)
        self.langs: List[str] = [
            "cpp",
            "go",
            "java",
            "js",
            "php",
            "python",
        ]
        self.exts: List[str] = list()
        for lang in self.langs:
            if lang in LANG_EXT_MAP:
                self.exts.extend(LANG_EXT_MAP[lang])
        self.relpos = len(self.params.project_dir) + 1

    def run(self) -> List[Issue]:

        # config
        demo_config_path = os.path.join(BASE_DIR, "config", "tool_6_demo_config.json")
        with open(demo_config_path) as f:
            config_content = json.load(f)
        config_content["languages"] = self.langs

        config_path = os.path.join(self.out_dir, "config.json")
        with open(config_path, "w") as f:
            json.dump(config_content, f)

        # cmd
        cmd = [
            os.path.join(self.tool_dir, "bin", "Tool_6_3"),
            "--service",
            self.params.service,
            "--check-code",
            self.params.check_code,
            "-c",
            config_path,
            "-p",
            self.params.project_dir,
            "-o",
            self.out_dir,
        ]
        run_cmd(cmd)

        # handle result
        result: List[Issue] = list()
        out_path = os.path.join(self.out_dir, "result.json")
        if os.path.exists(out_path):
            f = open(out_path)
            result = json.load(f, object_hook=self.handle_result)
            f.close()
        return result


    def handle_result(self, item: dict):
        # print(f"item: {item}")
        if "rule" in item:
            return Issue(
                rule=f'{self.__class__.__name__}/{item["rule"]}',
                line=int(item["line"]),
                msg=item["msg"],
                path=item["path"],
                column=int(item["column"]),
                refs=item.get("refs", list()),
            )
        return Ref(
            tag="",
            line=int(item["line"]),
            msg=item["msg"],
            path=item["path"],
        )
