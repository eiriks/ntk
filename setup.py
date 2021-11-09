from setuptools import setup, find_packages

setup(
    name='praenomen2genus',
    version='0.2.0',
    author='Eirik Stavelin',
    packages=find_packages(),  # ['towelstuff',],
    # include_package_data=True, # virker ikke
    package_data={'praenomen2genus': ['data/*.txt', 'data/*.pickle']},
    url='https://github.com/eiriks/praenomen2genus',
    license='MIT',
    long_description=open('README.md').read(),
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.5',
    ],
)
