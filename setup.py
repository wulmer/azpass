from pathlib import Path

from setuptools import setup

REQUIREMENTS_FILE = Path("requirements.txt")

setup(
    name="azpass",
    version="0.0.1",
    packages=["azpass"],
    package_dir={"": "src"},
    install_requires=REQUIREMENTS_FILE.read_text().splitlines(),
    entry_points={"console_scripts": ["azpass=azpass:main"]},
)
