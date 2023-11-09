"""Prepare an upload package with source code in one file and new solutions."""
import os
import re
import shutil
from dataclasses import dataclass
from typing import List

import data


@dataclass
class Uploader:
    """Method container for specific uploads."""

    source: str
    aliases: List[str]

    @staticmethod
    def clean():
        """Clean up and set up upload directory."""
        if os.path.isdir("upload"):
            shutil.rmtree("upload")
        os.makedirs("upload")

    def solver(self):
        """Pack solver source code."""
        module = f"{self.source}.py"
        if os.path.isdir(self.source):
            shutil.make_archive("upload/source", "zip", self.source)
        elif os.path.isfile(module):
            shutil.copyfile(module, "upload/source.py")

    def solutions(self):
        """Pack solution files."""
        for alias in self.aliases:
            path = data.Driver(alias).name("out")
            print(path)
            file = re.sub(".*/", "", path)
            shutil.copyfile(path, f"upload/{file}")


def upload(source, aliases):
    """Upload everything."""
    uploader = Uploader(source, aliases)
    uploader.clean()
    uploader.solver()
    uploader.solutions()
