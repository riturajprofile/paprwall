from setuptools import setup, find_packages

setup(
    name="paprwall",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A modern desktop wallpaper manager with motivational quotes.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/paprwall",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=open("requirements.txt").read().splitlines(),
    extras_require={
        "dev": open("requirements-dev.txt").read().splitlines(),
    },
    entry_points={
        "console_scripts": [
            "paprwall=paprwall.__main__:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Free for non-commercial use",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)