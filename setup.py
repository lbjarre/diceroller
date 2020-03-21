from setuptools import find_packages, setup

setup(
    name="diceroller",
    author="Lukas Bjarre",
    version="0.0.1",
    package=find_packages(),
    install_requires=["fastapi==0.52.0", "uvicorn==0.11.3", "gunicorn==20.0.4"],
)
