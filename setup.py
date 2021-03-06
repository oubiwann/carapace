from setuptools import setup, find_packages

from carapace import meta
from carapace.util import dist


setup(
    name=meta.display_name,
    version=meta.version,
    description=meta.description,
    long_description=meta.long_description,
    author=meta.author,
    author_email=meta.author_email,
    url=meta.url,
    license=meta.license,
    packages=find_packages() + ["twisted.plugins"],
    package_data={
        "twisted": ['plugins/carapace.py']
        },
    install_requires=meta.requires,
    zip_safe=False
    )


dist.refresh_plugin_cache()
