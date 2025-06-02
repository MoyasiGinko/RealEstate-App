from setuptools import setup, find_packages

setup(
    name='user-desktop-app',
    version='0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'kivy>=2.2.1',
        'kivy-garden>=0.1.5',
        'kivymd>=1.1.1',
        'pillow>=9.5.0',
        'reportlab>=4.0.4',
        'requests>=2.31.0',
        'python-dateutil>=2.8.2',
        # sqlite3 is part of Python standard library
    ],
    entry_points={
        'console_scripts': [
            'user-desktop-app=main:main',  # Adjust the entry point as necessary
        ],
    },
    include_package_data=True,
    zip_safe=False,
)