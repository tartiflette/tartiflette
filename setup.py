from setuptools import find_packages, setup

_TEST_REQUIRE = [
    "pytest",
    "pytest-benchmark",
    "pytest-cov",
    "pytest-asyncio",
    "pytz",
    "pylint==1.8.1",
    "xenon",
    "black==18.6b4",
]

_VERSION = "0.1.0"

_PACKAGES = find_packages(exclude=["tests*"])

setup(
    name="tartiflette",
    version=_VERSION,
    description="GraphQL Request Executor for python",
    long_description=open("README.md").read(),
    url="https://github.com/dailymotion/tartiflette",
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
    install_requires=[
        "cython",
        "uvloop==0.9.1",
        "cffi",
        "python-rapidjson",
        "lark-parser==0.6.2",
    ],
    tests_require=_TEST_REQUIRE,
    extras_require={"test": _TEST_REQUIRE},
)
