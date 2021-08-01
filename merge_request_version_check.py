#!/usr/bin/env python3

"""
Check that a merge request's POM artifact version is greater than
the target branch's.
"""

import pomversion
import os
import subprocess

from sys import argv, stdout, stderr
from subprocess import PIPE


def eprint(*args):
    """Prints to stderr"""
    print(*args, file=stderr)


class MergeRequestVersionCheck:
    def __init_(self, target_commit_ish, source_commit_ish, pom_file, quiet):
        self.target_commit_ish = target_commit_ish
        self.source_commit_ish = source_commit_ish
        self.pom_file = pom_file
        self.quiet = quiet
        self.output = os.devnull if quiet else stdout

    def pom_from_file(self):
        with open(self.pom_file, "r") as file:
            return file.read()

    def pom_from_commit_ish(self, commit_ish):
        command = ("git", "show", f"{commit_ish}:{self.pom_file}")
        process = subprocess.run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        if process.returncode != 0:
            raise(FileNotFoundError(process.stderr.strip()))
        return process.stdout

    def load_pom(self, commit_ish):
        if commit_ish is None:
            return self.pom_from_file()
        return self.pom_from_commit_ish(commit_ish)

    def load_version(self, commit_ish, description):
        try:
            pom_xml = self.load_pom(commit_ish)
            return pomversion.from_xml(pom_xml)
        except FileNotFoundError as err:
            eprint(f'Error retrieving POM file: "{err}"')
        except pomversion.InvalidVersionError as err:
            eprint(f'{description} version is invalid: "{err.version_string}"')
        except pomversion.MissingVersionError:
            eprint(f"{description} version is missing")
        return None

    def check(self):
        source_version = self.load_version(self.source_commit_ish, "Source")
        if source_version is None:
            return(1)
        print(f"Source version: {source_version}", file=self.output)

        target_version = self.load_version(self.target_commit_ish, "Target")
        if target_version is None:
            return(0)
        print(f"Target version: {target_version}", file=self.output)

        if source_version <= target_version:
            eprint( "Current version must be greater than target version")
        return(0)
