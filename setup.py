import setuptools

with open("README.md") as f:
    desc = f.read()

setuptools.setup(
    name="twitter-image-dl",
    version="0.1.0",
    license="MIT",
    url="https://github.com/morinokami/twitter-image-downloader",
    keywords=["Twitter", "image"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Multimedia :: Graphics",
    ],
    description="Twitter image downloader",
    long_description=desc,
    long_description_content_type="text/markdown",
    author="Shinya Fujino",
    author_email="shf0811@gmail.com",
    packages=["twt_img"],
    entry_points={"console_scripts": ["twt_img=twt_img.twt_img:main"]},
    install_requires=["python-dateutil", "requests"],
)
