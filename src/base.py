# -*- encoding: utf-8 -*-

import os

from typing import List, NamedTuple
from threading import Thread
from subprocess import Popen, PIPE, STDOUT


class ParamTuple(object):
    def __init__(
        self,
        service: str,
        check_code: str,
        languages: List[str],
        files_path: str,
        fail_on_warnings: bool,
        project_dir: str,
        project_name: str,
        out_dir: str,
        files: List[str] = list(),
    ) -> None:
        self.service = service
        self.check_code = check_code
        self.languages = languages
        self.files_path = files_path
        self.fail_on_warnings = fail_on_warnings
        self.project_dir = project_dir
        self.project_name = project_name
        self.out_dir = out_dir
        self.files = files


def json_serializable(cls):
    def as_dict(self):
        yield {name: value for name, value in zip(
            self._fields,
            iter(super(cls, self).__iter__()))}
    cls.__iter__ = as_dict
    return cls


@json_serializable
class Ref(NamedTuple):
    tag: str
    line: int
    msg: str
    path: str
    column: int = 0


@json_serializable
class Issue(NamedTuple):
    rule: str
    line: int
    msg: str
    path: str
    column: int = 0
    refs: List[Ref] = list()


class CmdError(Exception): ...


LANG_EXT_MAP = {
    "cpp": [".cpp", ".c", ".cc", ".cxx", ".h", ".hpp"],
    "oc": [".h", ".hpp", ".m", ".mm"],
    "cs": [".cs"],
    "java": [".java"],
    "js": [".js", ".jsx"],
    "php": [".php"],
    "go": [".go"],
    "python": [".py"],
}


class SubProcess(object):
    def __init__(self, command, cwd=None, out=None):
        self.p = Popen(command, cwd=cwd, stdout=PIPE, stderr=STDOUT)
        self.out = out
        if self.out:
            def do():
                while self.p.poll() is None:
                    out = self.p.stdout.readline()
                    out = bytes.decode(out)
                    if out:
                        self.out(out)
                out = self.p.stdout.read()
                if out:
                    self.out(out)
            out_t = Thread(target=do)
            out_t.start()

    def wait(self):
        self.p.wait()


def run_cmd(cmd: List) -> None:
    # print(f"run cmd: {' '.join(cmd)}")
    step = SubProcess(cmd, out=print)
    step.wait()
    if step.p.returncode != 0:
        raise CmdError("CMD Run Error!")


def get_files(root_dir, want_suffix=""):
    files = set()
    for dirpath, _, filenames in os.walk(root_dir):
        for f in filenames:
            if f.lower().endswith(want_suffix):
                fullpath = os.path.join(dirpath, f)
                files.add(fullpath)
    files = list(files)
    return files
