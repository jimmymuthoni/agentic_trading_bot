from setuptools import setup, find_packages
from typing import List

# function to get all requirements
def get_requirements() ->List:
    requirements: List[str] = []
    try:
        with open("requirements.txt", 'r') as file:
            lines = file.readline()
            for line in lines:
                requirement = line.strip()
                if requirement and requirement != '-e .':
                    requirements.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found")
    return requirements
print(get_requirements())

#project set up
setup(
    name = "trading_bot",
    version = "0.0.1",
    author="jimmy muthoni",
    author_email="jimmymuthoni26@gmail.com",
    packages=find_packages(),
    install_requires = get_requirements(),
    python_requires = ">3.10",
)