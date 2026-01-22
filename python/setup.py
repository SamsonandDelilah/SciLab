from setuptools import setup, find_packages

setup(
    name="scilib",
    version="0.1.0",
    packages=["."],  # ← FLAT: python/ → scilib/
    package_dir={"": "."},  # ← python/ als Root
    install_requires=["numpy"],
)
