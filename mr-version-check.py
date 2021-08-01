#!/usr/bin/env python3

import pomversion
import os
import subprocess
import click

from sys import argv, stderr
from subprocess import PIPE


def load_pom_xml(commit_ish, pom_file="pom.xml"):
    """Loads the contents of a POM file.

    Parameters
    ----------
    commit_ish
        The git commit-ish to load the POM file from. If None is given
        it will load the POM file from the working directory.
    pom_file
        Path to POM file. Defaults to "pom.xml".

    Returns
    -------
    str
        The contents of the POM file from the given commit-ish.
    """

    if commit_ish is None:
        with open(pom_file, "r") as file:
            return file.read()

    command = ["git", "show", f"{commit_ish}:{pom_file}"]
    process = subprocess.run(
        command,
        stdout=PIPE,
        stderr=PIPE,
        universal_newlines=True)
    if process.returncode != 0:
        raise(FileNotFoundError(process.stderr.strip()))
    return process.stdout


def eprint(*args):
    """Prints to stderr"""
    print(*args, file=stderr)


def load_version(commit_ish, description, pom_file="pom.xml"):
    """Loads the version from a POM file.

    Parameters
    ----------
    commit_ish
        The git commit-ish to load the POM file from. If None is given
        it will load the POM file from the working directory.
    description
        Nature of the commit-ish to use in error messages. For example:
        "Source", or "Target".
    pom_file
        Path to POM file. Defaults to "pom.xml".

    Returns
    -------
    semantic_version.Version, or None
        The semantic version from the POM file, or None if an error
        was raised.
    """

    try:
        pom_xml = load_pom_xml(commit_ish, pom_file=pom_file)
    except FileNotFoundError:
        eprint(f'"{pom_file}" does not exist in {description.lower()}')

    try:
        return pomversion.from_xml(pom_xml)
    except pomversion.InvalidVersionError as err:
        eprint(f'{description} version is invalid: "{err.version_string}"')
    except pomversion.MissingVersionError:
        eprint(f"{description} version is missing")


@click.command()
@click.argument("target_ref")
@click.argument("source_ref", required=False)
@click.option("--pom-file", default="pom.xml", help="Path to pom file")
def mr_version_check(target_ref, source_ref, pom_file):
    source_version = load_version(source_ref, "Source", pom_file=pom_file)
    if source_version is None:
        exit(1)

    print(f"Source version: {source_version}")

    target_version = load_version(target_ref, "Target", pom_file=pom_file)
    if target_version is None:
        exit(0)

    print(f"Target version: {target_version}")

    if source_version <= target_version:
        eprint( "Current version must be greater than target version")
        exit(1)


if __name__ == "__main__":
    mr_version_check()
