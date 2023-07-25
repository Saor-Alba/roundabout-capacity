import setuptools

setuptools.setup(
    name='roundabout_capacity',
    version='1.0.0',
    author='Angus Spence',
    packages=['modules_python', 'modules_vba'],
    install_requires=['numpy', 'xlwings', 'pyinstaller']
)