import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='imcpq_exp',
    version='0.0.1',
    author='Somi Afiuni',
    author_email='afiuni.somi@gmail.com',
    description='Installation of Package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/SomiAfiuni/ImcpQ.git',
    project_urls={
        "Bug Tracker": "https://github.com/SomiAfiuni/ImcpQ_package/issues"
    },
    license='MIT',
    packages=['imcpq_exp'],
    install_requires=['pandas', 'tifffile', 'numpy'],
)
