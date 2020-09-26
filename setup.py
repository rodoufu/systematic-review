from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="Systematic review",
    version="0.0.1",
    author="Rodolfo Araujo",
    author_email="rodoufu@gmail.com",
    description="A small collection of utilities to help with a systematic review",
    url='https://github.com/rodoufu/systematic-review',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=open("requirements.txt").readlines(),
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Researchers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)
