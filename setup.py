from setuptools import setup, find_packages
from mockallan import __version__


with open('README.md', 'r', encoding='utf-8') as f:
	long_description = f.read()

setup(
	name="mockallan",
	version=__version__,
	author="David Domínguez",
	author_email="david.7b8@gmail.com",
	description='Lightweight HTTP server mock for CI and testing environments.',
	py_modules=[
		'mockallan',
		'app_handler',
		'history',
		'request',
		'stub_config',
		'validators'
	],
	packages=find_packages(where='src'),
	package_dir={'': 'src'},
	long_description_content_type="text/markdown",
	long_description=long_description,
	url='https://github.com/david-domz/mockallan',
	install_requires=[
		'jsonschema>=3.0.0,<4.0.0',
		'lxml>=4.0.0,<5.0.0'
	],
	extras_require={
		"dev": [
			'pytest>=7.4.2',
			'coverage==7.6.7',
			'twine>=4.0.2'
		]
	},
	python_requires='>=3.10, <4',
	entry_points={
		"console_scripts": [
			"mockallan = mockallan.main:main"
		],
	},
	license='MIT',
	keywords=['python', 'http', 'REST', 'mock', 'test', 'pytest'],
	classifiers=[
		"Development Status :: 4 - Beta",
		"Environment :: Console",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: MIT License",
		"Programming Language :: Python :: 3.10",
		"Programming Language :: Python :: 3.11",
		"Topic :: Software Development :: Testing",
		"Topic :: Software Development :: Testing :: Mocking",
		"Topic :: Internet :: WWW/HTTP",
		"Topic :: Software Development :: Libraries :: Python Modules",
		"Operating System :: OS Independent"
	],
	test_suite='test'
)
