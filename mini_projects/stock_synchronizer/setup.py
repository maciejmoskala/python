import os
import re
from setuptools import setup, find_packages
from pip.req import parse_requirements


ROOT = os.path.abspath(os.path.dirname(__file__))
PROJECT_NAME = 'stock_synchronizer'
PROJECT_PATH = os.path.join(ROOT, PROJECT_NAME)
VERSION_RE = re.compile(
    r'^__version__\s*=\s*\'(?P<version>\d*(\.\d*){0,2})\'\s*$')
AUTHOR = ('Maciej Moskała', 'maciejmoskala@gmail.com')


def read_file(path):
    with open(os.path.join(ROOT, path), 'r') as fo:
        return fo.read()


def read_requirements(path):
    requirements = parse_requirements(path, session=False)
    return [str(ir.req) for ir in requirements]


def get_version():
    ini = os.path.join(PROJECT_PATH, '__init__.py')
    with open(ini, 'r') as fo:
        for line in fo:
            match = VERSION_RE.match(line)
            if match:
                return match.groupdict()['version']
    raise Exception('__version__ not found in %s/__init__.py' % PROJECT_NAME)


if __name__ == '__main__':
    version = get_version()

    run_ss = 'stock_synchronizer.scripts.run_stock_synchronizer:main'
    setup(
        name=PROJECT_NAME,
        version=version,
        description=PROJECT_NAME,
        long_description=read_file('README.md'),
        author=AUTHOR[0],
        author_email=AUTHOR[1],
        setup_requires=['pytest-runner'],
        install_requires=read_requirements('requirements.txt'),
        tests_require=read_requirements('requirements.test.txt'),
        entry_points={
            'console_scripts': [
                'run_stock_synchronizer = ' + run_ss,
            ],
        },
        packages=find_packages(exclude=['contrib', 'docs', 'tests']),
        package_dir={PROJECT_NAME: PROJECT_NAME},
        package_data={PROJECT_NAME: ['*.yaml']},
    )
