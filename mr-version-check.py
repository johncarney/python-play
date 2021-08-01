import pomversion
import os
import subprocess

from sys import argv, stderr
from subprocess import PIPE


def target_pom_xml(target_ref, pom_file="pom.xml"):
    command = ["git", "show", f"{target_ref}:{pom_file}"]
    process = subprocess.run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    if process.returncode != 0:
        raise(FileNotFoundError(process.stderr.strip()))
    return process.stdout


def eprint(*args):
    print(*args, file=stderr)


usage = f"Usage: {argv[0]} <target ref>"

if len(argv) == 1:
    print(usage)
    exit(0)
elif len(argv) != 2:
    print(usage)
    eprint("You can only specify a single target ref")
    exit(1)

if not os.path.exists("pom.xml"):
    print(f"Missing pom.xml")
    exit(1)

try:
    current_branch_version = pomversion.load()
except pomversion.InvalidVersionError as err:
    eprint(f'Current branch version is invalid: "{err.version_string}"')
    exit(1)
except pomversion.MissingVersionError:
    eprint(f"Current branch version is missing")
    exit(1)

print(f"Current branch version: {current_branch_version}")

try:
    target_branch_version = pomversion.from_xml(target_pom_xml(argv[1]))
except pomversion.InvalidVersionError as err:
    eprint(f'Target branch version is invalid: "{err.version_string}"')
    exit(0)
except pomversion.MissingVersionError:
    eprint(f"Target branch version is missing")
    exit(0)
except FileNotFoundError:
    eprint(f"Target branch does not have a pom.xml")
    exit(0)

print(f"Target branch version:  {target_branch_version}")

if current_branch_version <= target_branch_version:
    eprint("Current branch version must be greater than target branch version")
    exit(1)
