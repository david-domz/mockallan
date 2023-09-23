from setuptools import setup


setup(
	name="mockallan",
	version='0.0.1',
	author="David Domínguez",
	author_email="<david.7b8@gmail.com>",
	description='Versatile HTTP server mock designed for use as a substitute for a production HTTP server within a testing environment.',
	py_modules=['mockallan', 'app_handler', 'history', 'request', 'stub_config'],
	package_dir={'': 'src'},
	long_description_content_type="text/markdown",
	long_description='A configurable HTTP server mock that can be use in integration tests.',
	install_requires=[],
	entry_points={
		"console_scripts": [
			"mockallan = mockallan:main"
		],
	},
	keywords=['python', 'http', 'REST', 'mock', 'test', 'pytest'],
	classifiers=[
		"Development Status :: 4 - Beta",
		"Environment :: Console",
		"Intended Audience :: Developers",
		"Programming Language :: Python :: 3.10",
		"Topic :: Software Development :: Testing",
		"Topic :: Software Development :: Testing :: Mocking",
		"Topic :: Internet :: WWW/HTTP",
		"Topic :: Software Development :: Libraries :: Python Modules",
		"Operating System :: Unix",
		"Operating System :: MacOS :: MacOS X",
		"Operating System :: Microsoft :: Windows",
		"Operating System :: OS Independent",
	]
)
