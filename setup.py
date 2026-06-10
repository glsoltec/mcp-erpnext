#!/usr/bin/env python
"""Setup script for MCP ERPNext Plugin"""

from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='mcp-erpnext',
    version='1.0.0',
    description='MCP plugin for ERPNext v16 integration with Claude',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/seu-usuario/mcp-erpnext',
    license='MIT',
    packages=find_packages(include=['src', 'src.*']),
    package_data={
        'src': ['*.py'],
    },
    install_requires=[
        'mcp>=0.1.0',
        'requests>=2.31.0',
        'python-dotenv>=1.0.0',
        'pydantic>=2.0.0',
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'mcp-erpnext=src.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    keywords='erpnext frappe mcp claude ai',
    project_urls={
        'Bug Reports': 'https://github.com/seu-usuario/mcp-erpnext/issues',
        'Source': 'https://github.com/seu-usuario/mcp-erpnext',
        'Documentation': 'https://github.com/seu-usuario/mcp-erpnext#readme',
    },
)
