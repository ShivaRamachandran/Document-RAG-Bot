from setuptools import find_packages,setup
# from typing import List

def get_requirements():
    """
    This function will return list of requirements
    """
    requirement_list = []

    """
    Write a code to read requirements.txt file and append each requirements in requirement_list variable.
    """
    return requirement_list

PROJECT_NAME = 'RAG'
AUTHOR_NAME = 'Shiva'
DESCRIPTION = 'Building POC for RAG'
setup(
    name="rag",
    version="0.0.1",
    author="shiva",
    author_email="shiva.work007@gmail.com",
    packages = find_packages(),
    install_requires=get_requirements(),#["pymongo==4.2.0"],
)