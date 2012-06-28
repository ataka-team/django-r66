from setuptools import setup, find_packages

version = "0.0.0"

long_description=""
try:
    long_description=file('README.md').read()
except Exception:
    pass

license=""
try:
    license=file('MIT_License.txt').read()
except Exception:
    pass

setup(
    name = 'django-r66',
    version = version,
    description = 'Django Route 66 app',
    author = 'Pablo Saavedra',
    author_email = 'pablo.saavedra@treitos.com',
    url = 'http://github.com/ataka-team/django-r66',
    download_url= 'https://github.com/ataka-team/django-r66/zipball/master',
    packages = find_packages(),
    scripts=[
        "tools/r66-*",
    ],
    package_data={
        'r66': [
            'templates/r66/*.html',
            'static/*/css/*.css',
            'static/*/img/*.png',
            'static/*/img/*.jpg',
            'static/*/img/*/*',
            'static/*/js/*.js',
        ],
    },

    zip_safe=False,
    install_requires=[
        "django",
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Framework :: Django",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    long_description=long_description,
    license=license,
    keywords = "router firewall manager django r66",
)
