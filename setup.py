from setuptools import setup, find_packages
import os

# Read the contents of README file
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

# Package meta-data
NAME = "ai-cheerish"
DESCRIPTION = "A library that enhances AI interactions with motivational messages"
URL = "https://github.com/yourusername/ai-cheerish"
EMAIL = "your.email@example.com"
AUTHOR = "Your Name"
REQUIRES_PYTHON = ">=3.6.0"
VERSION = "0.1.0"

# Required packages
REQUIRED = [
    "python-dotenv",
]

# Optional packages
EXTRAS = {
    "dev": ["pytest", "black", "flake8"],
}

# Include example config in package
package_data = {
    "ai_cheerish": ["config.example.json"],
}

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    package_data=package_data,
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy"
    ],
) 