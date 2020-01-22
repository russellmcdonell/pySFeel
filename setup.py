import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='pySFeel-pkg-russell.mcdonell',
    version='0.0.1a2',
    author='Russell McDonell',
    author_email='russell.mcdonell@c-cost.com',
    description='An implementation of S-FEEL using sly',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/russell.mcdonell/pySFeel',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=['sly','dateutil','math','statistics'],
)
