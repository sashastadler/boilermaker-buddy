import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rphaneuf",
    version="0.0.1",
    author="Roger Phaneuf",
    author_email="boilermakerbuddy@gmail.com",
    description="( ͡° ͜ʖ ͡°)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sashastadler/boilermaker-buddy.git",
    project_urls={},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)