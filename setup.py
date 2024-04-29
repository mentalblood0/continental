import pathlib

import setuptools

if __name__ == "__main__":
    setuptools.setup(
        name="continental",
        version="0.1.0",
        python_requires=">=3.11",
        keywords=["markov-chains", "text-generation"],
        url="https://github.com/MentalBlood/continental",
        description="Create on-disk markov chain and generate text using it",
        long_description=(pathlib.Path(__file__).parent / "README.md").read_text(),
        long_description_content_type="text/markdown",
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Science/Research",
            "Intended Audience :: End Users/Desktop",
            "Topic :: Software Development :: Libraries",
            "Topic :: Education",
            "Topic :: Utilities",
            "Typing :: Typed",
            "Topic :: Text Processing",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12",
            "License :: OSI Approved :: BSD License",
        ],
        author="mentalblood",
        author_email="neceporenkostepan@gmail.com",
        maintainer="mentalblood",
        maintainer_email="neceporenkostepan@gmail.com",
        packages=setuptools.find_packages(exclude=["tests"]),
        install_requires=[],
    )
