from setuptools import setup, find_packages
from typing import List

HYPEN_E_DOT = '-e .' 
def get_requirements(file_path:str) -> List[str]:
    with open(file_path, 'r') as file:
        requirements = file.readlines()
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    return [req.strip() for req in requirements if req.strip() and not req.startswith('#')]
                     
setup(
    name="mlmanagement",
    author="CuriousCoder",
    version="0.0.1",
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt")
)