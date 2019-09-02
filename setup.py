# setup.py
import sys
from setuptools import setup
from setuptools import find_packages

# The version is updated automatically with bumpversion
# Do not update manually
__version = '0.1.0'

# windows installer:
# python setup.py bdist_wininst

# patch distutils if it can't cope with the "classifiers" or
# "download_url" keywords

setup_requirements = []

TESTING = any(x in sys.argv for x in ["test", "pytest"])
if TESTING:
    setup_requirements += ['pytest-runner']
test_requirements = ['pytest', 'pytest-cov']

SPHINX = any(x in sys.argv for x in ["build_sphinx"])
if SPHINX:
    setup_requirements += ['sphinx', 'sphinx-argparse', 'sphinx_rtd_theme']

extra_requirements = {
    'tango': ['pytango']
}
setup(
    name="nhq_iseg",
    description="Python NHQ Iseg High Power Supplier extension",
    version=__version,
    author="Roberto J. Homs Puron",
    author_email="rhoms@cells.es",
    url="https://github.com/ALBA-Synchrotron/NHQIseg",
    packages=find_packages(),
    # package_data={'': package_list},
    include_package_data=True,
    license="GPLv3",
    long_description="Python NHQ Iseg Extension for Win32, Linux, BSD, Jython",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.5',
        'Topic :: Communications',
        'Topic :: Software Development :: Libraries',
    ],
    entry_points={
        'console_scripts': [
            'NHQIseg = nhq_iseg.tango:main [tango]',

        ]
    },
    install_requires=['pyserial'],
    setup_requires=setup_requirements,
    tests_require=test_requirements,
    extras_require={"tango": ['pytango']},
    python_requires='>=3.5',
)
