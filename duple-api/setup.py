import setuptools

setuptools.setup(
    name="duple",
    version="0.01",
    description="Data deduplicator using dedupe.io library and pandas",
    license="GNU GPLv3",
    install_requires=[
        "dedupe",
        "pandas",
        "unidecode",
        "aiohttp[speedups]",
        "aiohttp-swagger[performance]",
        "aiohttp-cors",
        "shortuuid",
        "tox"
    ],
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=False,
)
