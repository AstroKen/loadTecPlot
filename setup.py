from setuptools import setup, find_packages

setup(
    name="loadTecPlot",
    version="0.0.2",
    description='Package for load TecPlot format files.',
    author="AstroKen",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas"
        ],
    include_package_data=True,
)
