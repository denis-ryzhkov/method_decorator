from distutils.core import setup

setup(
    name='method_decorator',
    version='0.1.3',
    description='Python decorator that knows the class the decorated method is bound to.',
    long_description='''
Please see full description here:
https://github.com/denis-ryzhkov/method_decorator/blob/master/README.md

''',
    url='https://github.com/denis-ryzhkov/method_decorator',
    author='Denis Ryzhkov',
    author_email='denisr@denisr.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    py_modules=['method_decorator'],
)
