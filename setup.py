import os
import subprocess
import sys

from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext
from setuptools.command.build_py import build_py


def _find_libgraphqlparser_artifact():
    if os.path.exists("./libgraphqlparser/libgraphqlparser.so"):
        return "./libgraphqlparser/libgraphqlparser.so"

    if os.path.exists("./libgraphqlparser/libgraphqlparser.dylib"):
        return "./libgraphqlparser/libgraphqlparser.dylib"

    return None


def _build_libgraphqlparser():
    os.chdir("./libgraphqlparser/.")
    subprocess.run(["cmake", "."], stdout=subprocess.PIPE)
    subprocess.run(["make"], stdout=subprocess.PIPE)
    os.chdir("..")

    artifact_path = _find_libgraphqlparser_artifact()

    if not artifact_path:
        print("Libgraphqlparser compilation has failed")
        sys.exit(-1)

    os.rename(
        artifact_path,
        f"tartiflette/language/parsers/libgraphqlparser/cffi/{os.path.basename(artifact_path)}",
    )


class BuildExtCmd(build_ext):
    def run(self):
        _build_libgraphqlparser()


class BuildPyCmd(build_py):
    def run(self):
        _build_libgraphqlparser()
        super().run()


class LibGraphQLParserExtension(Extension):
    def __init__(self):
        super().__init__("libgraphqlparser", sources=[])


setup(
    cmdclass={"build_ext": BuildExtCmd, "build_py": BuildPyCmd},
    ext_modules=[LibGraphQLParserExtension()],
)
