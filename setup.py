import setuptools


VERSION = '0.0.1'


with open('README.md', 'r', encoding='utf8') as f:
    long_description = f.read()


setuptools.setup(
    name='KoreaTrain',
    packages=['koreatrain'],
    version=VERSION,
    author='Nitro',
    author_email='nitrodev0@gmail.com',
    description='A Python wrapper for SR and Korail train client service.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Nitro1231/KoreaTrain',
    license='MIT License',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)