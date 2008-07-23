#from ez_setup import use_setuptools
#use_setuptools()
from setuptools import setup, find_packages

setup(
    name='SupervisorErrorMiddleware',
    version="",
    #description="",
    author="David Turner",
    author_email="novalis@openplans.org",
    license="GPLv2 or any later version",
    install_requires=["Paste"],
    packages=find_packages(),
    include_package_data=True,
    test_suite = 'nose.collector',
    package_data={'supervisorerrormiddleware': ['i18n/*/LC_MESSAGES/*.mo']},
    entry_points="""
    [paste.filter_app_factory]
    main = supervisorerrormiddleware:SupervisorErrorMiddleware
    """,
)
