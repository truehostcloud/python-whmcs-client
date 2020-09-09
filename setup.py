from setuptools import find_packages, setup

setup(
    name='olittwhmcs',
    version='0.0.1',
    description='Interact with the olitt whmcs',
    author='Oliver Muthomi',
    license='MIT',
    packages=find_packages(include=['olittwhmcs']),
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'responses'],
    test_suite='tests',
)
