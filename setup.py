import setuptools

with open("README", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="serenipy",
    version="0.2.4",
    author="Patrick Garrett",
    author_email="pgarrett@scripps.edu",
    description="A small package for handling ip2 related files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['serenipy'],
    python_requires=">=3.6",
    include_package_data=True,
)