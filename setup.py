from distutils.core import setup

with open('README.rst') as f:
    readme = f.read()

setup(
    name='juka_kernel',
    version='0.1',
    packages=['juka_kernel'],
    description='Juka kernel for Jupyter',
    long_description=readme,
    author='Juka',
    author_email='admin@jukalang.com',
    url='https://github.com/jukaLang/juka_kernel',
    install_requires=[
        'jupyter_client', 'IPython', 'ipykernel'
    ],
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Development Status :: 2 - Pre-Alpha'
    ]
)