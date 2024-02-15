from setuptools import setup, find_packages

setup(
    name="loadTecPlot",
    version="0.0.6",
    description='Package for load TecPlot format files. SSH connection is added.',
    author="AstroKen",
    packages=[
        "loadTecPlot",
        "loadTecPlot.sshLoadTecPlot"
        ],
    install_requires=[
        "numpy",
        "pandas",
        "paramiko"
        ],
    include_package_data=True,
)
