from setuptools import setup,find_packages
from typing import List
HYPHEN_E_DOT = '-e .'
def get_requirements(File_path:str)->List[str]:
    requirements=[]
    with open(file=File_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n","") for req in requirements]

        if HYPHEN_E_DOT == '-e .':
            requirements.remove(HYPHEN_E_DOT)
            # -e . used to setup.py directly
    
    return requirements

setup(
    name = 'mlproject',
    version='0.0.1',
    author='Arshan',
    author_email='arshan5446@gmail.com',
    packages=find_packages(),
    # install_requires=['pandas','numpy','matplotlib.pyplot','pytorch','tensorflow']    Not feasible to write packages like this
    install_requires = get_requirements('requirements.txt')
)