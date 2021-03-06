# Package setup

from setuptools import find_packages, setup

with open('README.md', 'r') as readme_file:
    long_description = readme_file.read()

setup(
    name='cdslab_cmodels_api',
    version='0.0.1',
    maintainer='Developers of the CDS team of FEnFiSDi group',
    maintainer_email='alejandro.campillo@udea.edu.co',
    description='CDSLab cmodels API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/fenfisdi/cdslab_cmodels_api',
    author='Juan Esteban Aristizabal',
    author_email='jeaz.git@gmail.com',
    license='GNU General Public License v3 (GPLv3)',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Framework :: CDSLab',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Education',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries'
    ],
    test_suite='pytest',
    packages=find_packages(exclude='__pycache__'),
    keywords=[],
    python_requires='>=3.8',
    install_requires=[],
    zip_safe=False
)
