import setuptools


setuptools.setup(
    name="redditutils",  # Replace with your own username
    version="0.0.1",
    author="Joao Pereira",
    author_email="joaopedrosp@gmail.com",
    description="A set of utilities to help out with managing and moderating r/Euroleague",
    long_description="A set of utilities to help out with managing and moderating r/Euroleague",
    long_description_content_type="text/markdown",
    url="https://github.com/JoaoPere/reddit-euroleague-utils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
