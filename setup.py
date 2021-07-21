import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sgu",
    version="v0.0.1",
    author="xy.zhang",
    author_email="fyman.zhang@gmail.com",
    description="SQLAlchemy from zero to hero",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/firefirer1983/sqlalchemy-ground-up.git",
    project_urls={},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"sgu": "sgu"},
    packages=setuptools.find_packages(where="sgu"),
    python_requires=">=3.6",
)