import os
import re
import sys
from pathlib import Path
from shutil import rmtree

from setuptools import setup, find_packages, Command

here = Path.cwd()
with open(here / 'README.rst') as f:
    readme = '\n' + f.read()

with open(here / 'CHANGES.rst') as f:
    changes = '\n' + f.read()
    version_match = re.search(r'\n(\d+.\d+.\d+) /', changes)
    version = version_match.groups()[0]


class UploadCommand(Command):
    """Support setup.py publish."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except FileNotFoundError:
            pass

        self.status('Building Source distribution…')
        os.system('{0} setup.py sdist'.format(sys.executable))

        self.status('Uploading the package to PyPi via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(version))
        os.system('git push --tags')

        sys.exit()


setup(
    name='redistore',
    version=version,
    description='Simple python interface for redis',
    url='https://github.com/lamenezes/redistore',
    author='Luiz Menezes',
    author_email='luiz.menezesf@gmail.com',
    license='MIT',
    long_description='\n' + readme,
    packages=find_packages(exclude=['tests*']),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    cmdclass={
        'upload': UploadCommand,
    },
)
