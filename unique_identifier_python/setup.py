from setuptools import find_packages
from setuptools import setup

package_name = 'unique_identifier_python'

setup(
    name=package_name,
    version='1.0.6',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/' + package_name, ['package.xml']),
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
    ],
    author="Jack O'Quin",
    maintainer='Jacob Perron',
    maintainer_email='jacob@openrobotics.org',
    url='https://github.com/ros2/unique_identifier',
    download_url='https://github.com/ros2/unique_identifier/releases',
    keywords=[],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD',
        'Programming Language :: Python',
    ],
    description='Python API for working with universally unique identifiers in ROS.',
    long_description=(
        'This package provides a Python API for generating universally unique'
        'identifiers and converting to and from ROS messages.'),
    license='BSD',
    tests_require=['pytest'],
)
