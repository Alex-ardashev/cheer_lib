import setuptools

# Read the README for a long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ai_cheerish",  # Updated package name for PyPI
    version="0.1.1",
    author="Your Name",
    author_email="your.email@example.com",
    description="Enhance AI model performance by injecting inspirational words into prompts.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Alex-ardashev/cheer_lib",  # Replace with your repo URL
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    
    python_requires=">=3.7",
    install_requires=[
        "python-dotenv>=0.19.0",
        # List additional dependencies here
    ],
    include_package_data=True,  # Tells setuptools to include files specified in MANIFEST.in
    package_data={
        "ai_cheerish": ["config.example.json"]
    },
) 