# -*- encoding: utf-8 -*-

import os
import csv
import json

from typing import List
from base import LANG_EXT_MAP, BaseTool, Issue, ParamTuple, Ref, run_cmd
from setting import BASE_DIR


class Tool_3(BaseTool):
    def __init__(self, params: ParamTuple) -> None:
        super().__init__(params)
        self.langs: List[str] = [
            "cpp",
            "oc",
            "cs",
            "java",
        ]
        self.exts: List[str] = list()
        for lang in self.langs:
            if lang in LANG_EXT_MAP:
                self.exts.extend(LANG_EXT_MAP[lang])
        self.files = [path for path in self.params.files if path.lower().endswith(tuple(self.exts))]

    def run(self) -> List[Issue]:
        abs_files = [os.path.join(self.params.project_dir, path) for path in self.files]

        files_path = os.path.join(self.out_dir, "files_path.txt")
        with open(files_path, "w") as f:
            f.write("\n".join(abs_files))

        # config
        demo_config_path = os.path.join(BASE_DIR, "config", "tool_3_demo_config.json")
        with open(demo_config_path) as f:
            config_content = json.load(f)

        config_path = os.path.join(self.out_dir, "config.json")
        with open(config_path, "w") as f:
            json.dump(config_content, f)

        # cmd
        cmd = [
            os.path.join(self.tool_dir, "bin", "Tool_3"),
            "--service",
            self.params.service,
            "--check-code",
            self.params.check_code,
            "-l",
            ",".join(self.langs),
            "-s",
            self.params.project_dir,
            "-o",
            self.out_dir,
            "-p",
            files_path,
            "-c",
            config_path,
        ]
        run_cmd(cmd)

        # handle result
        out_path = os.path.join(self.out_dir, "issues.csv")
        return [i for i in self.result_handle(out_path)]

    def result_handle(self, out_path):
        if not out_path or not os.path.exists(out_path):
            return list()

        relpos = len(self.params.project_dir) + 1
        f = open(out_path, "r", encoding="utf-8")
        csv_f = (line for line in f if "\0" not in line)
        reader = csv.DictReader(csv_f, (
            "checker",
            "description",
            "path",
            "line",
            "column",
        ))
        next(reader)
        for row in reader:
            path = row["path"][relpos:]
            line = int(row["line"])
            column = int(row["column"])
            rule = row["checker"]
            msg = row["description"]
            row_refs = row.get(None, [])
            refs: List[Ref] = list()
            for ref in row_refs:
                parts = ref.split(":")
                refs.append(Ref(parts[2], parts[3], parts[0], parts[1][relpos:]))
            yield Issue(rule, line, msg, path, column, refs)
        f.close()
