from setuptools import setup, find_packages

from class_registry import VERSION

setup(
    name="django-class-registry",
    version=VERSION,
    author="imtapps",
    author_email="imtapps@apps-system.com",
    description="Register any classes like Django's admin.",
    long_description=open('README.txt', 'r').read(),
    url="http://github.com/imtapps/django-class-registry",
    packages=find_packages(exclude=["example"]),
    install_requires=[],
    tests_requires=open('requirements/dist.txt').read().split("\n"),
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
)
