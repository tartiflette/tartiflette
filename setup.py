import os
import subprocess
import sys

from setuptools import Extension, find_packages, setup
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


_TEST_REQUIRE = [
    "pytest==6.2.4",
    "pytest-cov==2.12.1",
    "pytest-asyncio==0.15.1",
    "pytest-xdist==2.2.1",
    "pylint==2.9.5",
    "black==21.8b0",
    "isort==5.9.2",
]

_BENCHMARK_REQUIRE = ["pytest-benchmark==3.4.1"]

_VERSION = "1.4.0"

_PACKAGES = find_packages(exclude=["tests*"])


def _read_file(filename):
    with open(filename) as afile:
        return afile.read()


setup(
    name="tartiflette",
    version=_VERSION,
    description="GraphQL Engine for Python",
    long_description=_read_file("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/tartiflette/tartiflette",
    author="Dailymotion Core API Team",
    author_email="team@tartiflette.io",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    keywords="api graphql protocol api rest relay tartiflette dailymotion",
    packages=_PACKAGES,
    install_requires=["cffi>=1.0.0,<2.0.0", "lark-parser==0.11.3", "pytz"],
    tests_require=_TEST_REQUIRE,
    extras_require={"test": _TEST_REQUIRE, "benchmark": _BENCHMARK_REQUIRE},
    cmdclass={"build_ext": BuildExtCmd, "build_py": BuildPyCmd},
    ext_modules=[LibGraphQLParserExtension()],
    include_package_data=True,
)
