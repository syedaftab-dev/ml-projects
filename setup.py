# this file will create my mchine learning app as a package and that can be used to deployed and anybody just install and rin the app

from setuptools import find_packages,setup
from typing import List 


# if we lot of libraries to import
# the function will return a list of librarries of requirements

HYPEN_E_DOT='-e .'
def get_requirements(filepath:str)->List[str]:
    requirements=[]
    with open(filepath) as file_obj:
        requirements=file_obj.readlines()
        # we will get \n after we move to second line so we need to remove it
        [req.replace("\n","") for req in requirements]

        # remove -e . line 
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    return requirements

setup(
name='mlproject',
version='0.0.1',
author='Aftab',
author_email='syed.mohd.aftab@gmail.com',
packages=find_packages(), #will chek __init_-find in every folder as package
install_requires=get_requirements('requirements.txt')
)