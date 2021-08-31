from setuptools import setup, find_packages
import mangadex_py.meta as meta

author = meta.author
version = meta.version
license = meta.license_type
author = meta.author
repo_url = meta.repo_url
author_email = meta.email

REQUIREMENTS = ["requests", "tqdm", "urllib3"]

long_description  =  """
A manga downloader for MangaDex.org, Using the new API.

check https://github.com/Sydiepus/mangadex-py
"""

setup(
    name="Sydiepus-mangadex-py",
    version=version,
    packages=find_packages(exclude=("build", "__pycache__")),
    description="MangaDexv5 manga downloader",
    long_description=long_description,
    long_description_content_type="text/plain",
    url=repo_url,
    author=author,
    author_email=author_email,
    license=license,
    platforms=['any'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Environment :: Console",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    install_requires=REQUIREMENTS,
    entry_points={
        "console_scripts": [
            "mangadex-py = mangadex_py.util:main",
        ]
    },
)