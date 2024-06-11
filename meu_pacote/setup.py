from setuptools import setup, find_packages

setup(
    name='my_plotly_package',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'plotly>=5.0.0',
        'pandas>=1.0.0'
    ],
    author='Diogo Antonio',
    author_email='diogoantoniodejesus@hotmail.com.com',
    description='Objetivo da criação dessas funções são para que reduza o tempo na contrução e estilização de indicadores para Futuros Dashboards utilizando poucas linhas de codigo.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/seuusuario/my_plotly_package',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
