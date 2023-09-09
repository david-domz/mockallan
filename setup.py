from setuptools import setup


VERSION = '0.1'

setup(
	name="mock-http-server",
	version=VERSION,
	author="vurutal (David D.)",
	author_email="<david.7b8@gmail.com>",
	description='Mock HTTP server',
	py_modules=['mock_http_server'],
	package_dir={'': 'src'},
	long_description_content_type="text/markdown",
	long_description='A configurable HTTP server mock that can be use in integration tests.',
	install_requires=[],
	keywords=['python', 'http', 'REST', 'mock', 'test', 'pytest'],
	classifiers=[
		"Development Status :: 1 - Planning",
		"Intended Audience :: Developers",
		"Programming Language :: Python :: 3",
		"Operating System :: Unix",
		"Operating System :: MacOS :: MacOS X",
		"Operating System :: Microsoft :: Windows",
	]
)
