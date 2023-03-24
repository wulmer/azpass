from setuptools import setup
setup(
    name='azpass',
    version='0.0.1',
    entry_points={
        'console_scripts': [
            'azpass=azpass:main'
        ]
    }
)
