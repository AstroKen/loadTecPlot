from setuptools import setup, find_packages

setup(
    name="loadTecPlot",
    version="0.0.4",
    description='Package for load TecPlot format files. SSH connection is added.',
    author="AstroKen",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "paramiko"
        ],
    include_package_data=True,
)
