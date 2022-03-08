from setuptools import find_packages, setup

setup(
    name="quipucords",
    version="1.0.0",  # this is a placeholder which will be replaced by setup-tools-git-versioning
    packages=find_packages(include=["quipucords"]),
    include_package_data=True,
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
    ],
    license="GPLv3+",
    python_requires=">=3.6",
    # Runtime dependencies are not included here. Only setuptools-git-versioning for proper version resolution.
    # Check requirements.txt and dev-requirements.txt for production and development dependencies
    # setup_requires=["setuptools-git-versioning"],
    # setuptools_git_versioning={
    #     "enabled": True,
    #     "dev_template": "{tag}.dev{ccount}",
    #     "dirty_template": "{tag}.dev{ccount}a",
    # },
)
