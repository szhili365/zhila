# -*- encoding: utf-8 -*-

import os
import json

from typing import List

from base import LANG_EXT_MAP, Issue, ParamTuple, run_cmd
from tool.base import BaseTool
from setting import BASE_DIR


class Tool_10(BaseTool):
    def __init__(self, params: ParamTuple, languages: List[str]) -> None:
        super().__init__(params)
        self.langs: List[str] = languages
        self.exts: List[str] = list()
        for lang in self.langs:
            if lang in LANG_EXT_MAP:
                self.exts.extend(LANG_EXT_MAP[lang])
        self.files = [path for path in self.params.files if path.lower().endswith(tuple(self.exts))]
        # print(self.files)

    def run(self) -> List[Issue]:
        # files
        abs_files = [os.path.join(self.params.project_dir, path) for path in self.files]

        files_path = os.path.join(self.out_dir, "files_path.txt")
        with open(files_path, "w") as f:
            f.write("\n".join(abs_files))

        # step1
        cmd = [
            os.path.join(self.tool_dir, "bin", "Tool_10_1"),
            "--service",
            self.params.service,
            "--check-code",
            self.params.check_code,
            "-l",
            ",".join(self.langs),
            "-s",
            self.params.project_dir,
            "-i",
            self.out_dir,
            "-n",
            self.params.project_name,
            "-f",
            files_path,
        ]
        run_cmd(cmd)

        # step2

        # config
        demo_config_path = os.path.join(BASE_DIR, "config", "tool_10_demo_config.json")
        with open(demo_config_path) as f:
            config_content = json.load(f)
        config_content["sourcedir"] = self.params.project_dir
        config_content["files"] = self.files

        config_path = os.path.join(self.out_dir, "config.json")
        with open(config_path, "w") as f:
            json.dump(config_content, f)

        # cmd
        out_path = os.path.join(self.out_dir, "result.json")
        cmd = [
            os.path.join(self.tool_dir, "bin", "Tool_10_2"),
            "--service",
            self.params.service,
            "--check-code",
            self.params.check_code,
            "-l",
            ",".join(self.langs),
            "-i",
            self.out_dir,
            "-n",
            self.params.project_name,
            "-c",
            config_path,
            "-o",
            out_path,
        ]
        run_cmd(cmd)

        # handle result
        tmps = list()
        if os.path.exists(out_path):
            with open(out_path, "r") as f:
                tmps = json.load(f)
        for item in tmps:
            item["rule"] = f'{self.__class__.__name__}/{item["rule"]}'
        tmpstr: str = json.dumps(tmps)
        result: List[Issue] = json.loads(tmpstr, object_hook=lambda d: Issue(*d.values()))
        return result


class Tool_10_cpp(Tool_10):
    def __init__(self, params: ParamTuple) -> None:
        super().__init__(params, ["cpp"])


class Tool_10_go(Tool_10):
    def __init__(self, params: ParamTuple) -> None:
        super().__init__(params, ["go"])


class Tool_10_js(Tool_10):
    def __init__(self, params: ParamTuple) -> None:
        super().__init__(params, ["js"])


class Tool_10_php(Tool_10):
    def __init__(self, params: ParamTuple) -> None:
        super().__init__(params, ["php"])


class Tool_10_python(Tool_10):
    def __init__(self, params: ParamTuple) -> None:
        super().__init__(params, ["python"])
