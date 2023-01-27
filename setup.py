# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['grnet', 'grnet.abstract', 'grnet.dev', 'grnet.models']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.6.3,<4.0.0',
 'numpy>=1.24.1,<2.0.0',
 'pandas>=1.5.3,<2.0.0',
 'pgmpy>=0.1.21,<0.2.0']

setup_kwargs = {
    'name': 'grnet',
    'version': '0.1.0',
    'description': 'Python package for gene regulatory networks (GRN) using Bayesian network',
    'long_description': 'Python package for gene regulatory networks (GRN) using Bayesian network\n',
    'author': 'yo-aka-gene',
    'author_email': 'yujiokano@keio.jp',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
