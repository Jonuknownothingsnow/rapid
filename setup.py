import setuptools

setuptools.setup(
    name="rapid",
    version="0.1.0",
    author="wangtao",
    author_email="wym0604@163.com",
    description="rapid server",
    install_requires=["sanic", "loguru"],
    packages=["rapid"],
    python_requires=">=3.6",
)
