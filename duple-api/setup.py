import setuptools

setuptools.setup(
    name="duple",
    version="0.01",
    description="Data deduplicator using dedupe.io library and pandas",
    url="http://github.com/HughZurname/duple",
    author="Qonda Ltd.",
    author_email="info@qonda.io",
    license="GNU GPLv3",
    install_requires=[
        "dedupe",
        "pandas",
        "unidecode",
        "aiohttp[speedups]",
        "aiohttp-swagger[performance]",
        "aiohttp-cors",
        "shortuuid"
    ],
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=False,
)
