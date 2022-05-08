import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

REQUIRES = [ 
    "calendar",
    "bs4",
    "requests",
    "re",
    "selenium",
    "entity_resolution",
    "ask_sdk_core",
    "pickle",
    "ask_sdk_model",
    "logging"
    ]

setuptools.setup(
    name="BoilermakerBuddy",
    version="1.0.0",
    author="Roger Phaneuf, Grace Drukker, Sasha Stadler",
    author_email="boilermakerbuddy@gmail.com",
    description="( ͡° ͜ʖ ͡°)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=REQUIRES,
    include_package_data=True,
    url="https://github.com/sashastadler/boilermaker-buddy.git",
    project_urls={},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)