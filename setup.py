from setuptools import setup
from mockallan import VERSION


with open('README.md', 'r') as f:
	long_description = f.read()

setup(
	name="mockallan",
	version=VERSION,
	author="David Domínguez",
	author_email="david.7b8@gmail.com",
	description='Lightweight HTTP server mock used as a replacement for a production HTTP server in testing environments.',
	py_modules=[
		'mockallan',
		'app_handler',
		'history',
		'request',
		'stub_config',
		'validators'
	],
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
			'twine>=4.0.2'
		]
	},
	python_requires='>=3.10',
	entry_points={
		"console_scripts": [
			"mockallan = mockallan:main"
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
	]
)
