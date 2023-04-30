#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
from queue import Queue
import sys
import json
import threading
from typing import List

from base import LANG_EXT_MAP, BaseTool, Issue, ParamTuple, get_files
from tool10 import Tool_10_cpp, Tool_10_go, Tool_10_js, Tool_10_php, Tool_10_python
from tool3 import Tool_3


class Lancher(object):

    def __init__(self) -> None:
        self.params = ParamTuple(
            os.environ.get("INPUT_SERVICE"),
            os.environ.get("INPUT_CHECK_CODE"),
            os.environ.get("INPUT_LANGUAGE", "").split(","),
            os.environ.get("INPUT_FILES_PATH"),
            os.environ.get("INPUT_FAIL_ON_WARNINGS") == 'true',
            os.path.abspath(os.getcwd()),
            os.path.basename(os.path.abspath(os.getcwd())),
            os.path.join(os.getcwd(), "out"),
        )
        if self.params.files_path:
            self.params.files_path = os.path.abspath(self.params.files_path)
        self.tasks: list[BaseTool] = [
            Tool_10_cpp,
            Tool_10_go,
            Tool_10_js,
            Tool_10_php,
            Tool_10_python,
            Tool_3,
        ]
        # print(self.params)
        if self.params.files_path and os.path.isfile(self.params.files_path):
            with open(self.params.files_path) as f:
                self.params.files = f.readlines()
        else:
            exts: List[str] = list()
            for lang in self.params.languages:
                if lang in LANG_EXT_MAP:
                    exts.extend(LANG_EXT_MAP[lang])
            self.params.files = get_files(self.params.project_dir, tuple(exts))
            pos = len(self.params.project_dir) + 1
            self.params.files = [path[pos:] for path in self.params.files]
        # print(self.params.files)
    
    def run(self):
        issues: List[Issue] = list()
        threads = list()
        mutex = threading.Lock()
        for tool in self.tasks:
            task: BaseTool = tool(self.params)
            for lang in self.params.languages:
                if lang not in task.languages():
                    continue
                # print(f"task: {task.__class__.__name__}")
                def worker():
                    try:
                        tmp = task.run()
                    except Exception as e:
                        print(repr(e))
                        sys.exit(1)
                    mutex.acquire()
                    issues.extend(tmp)
                    mutex.release()
                t = threading.Thread(target=worker, name='worker')
                t.daemon = True
                t.start()
                threads.append(t)
                break

        for t in threads:
            t.join()

        output_path = os.path.join(self.params.out_dir, "issues.json")
        with open(output_path, "w", encoding="UTF-8") as f:
            json.dump(issues, f, indent=2, ensure_ascii=False)
        print(f"ZHILA Result: {json.dumps(issues, indent=2, ensure_ascii=False)}")
        
        if self.params.fail_on_warnings and len(issues) > 0:
            sys.exit(1)


if __name__ == "__main__":
    Lancher().run()
