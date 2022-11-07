from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="usconstitution",
    version="0.4.0",
    description="Pydantic model of US Constitution",
    long_description=long_description,
    classifiers=[
        "Development Status :: 3 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: LII Markup Tools",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    install_requires=[
        "pydantic>=1.9.1",
        "roman",
    ],
    extras_require={},
    url="https://github.com/LIICornell/us-constitution",
    packages=find_packages(),
    package_data={"usconstitution": ["data/*.json"]},
    include_package_data=True,
)
