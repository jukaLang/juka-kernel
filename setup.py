from distutils.core import setup

with open('README.rst') as f:
    readme = f.read()

setup(
    name='juka-kernel',
    version='0.2',
    packages=['juka-kernel'],
    description='Juka kernel for Jupyter',
    long_description=readme,
    author='Juka',
    author_email='admin@jukalang.com',
    url='https://github.com/jukaLang/juka-kernel',
    install_requires=[
        'jupyter_client', 'IPython', 'ipykernel'
    ],
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Development Status :: 2 - Pre-Alpha'
    ]
)