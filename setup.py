from setuptools import find_packages, setup

setup(
    name="flight_mailer",
    version="0.1",
    packages=find_packages(where="src", exclude=("test",)),
    package_dir={"": "src"},
)
