# README: GRNet
[<img src="https://img.shields.io/badge/DOI-WIP-FAB70C?style=flat&logo=doi">]()
[<img src="https://img.shields.io/badge/PMID-WIP-326599?style=flat&logo=pubmed">]()
[![Documentation Status](https://readthedocs.org/projects/grnet/badge/?version=latest)](https://grnet.readthedocs.io/en/latest/?badge=latest)
[<img src="https://img.shields.io/badge/Documentation-grnet.rtfd.io-8CA1AF?style=flat&logo=readthedocs">](https://grnet.readthedocs.io/en/latest/)
[<img src="https://img.shields.io/badge/Code_Examples-Jupyter_Notebook-F37626?style=flat&logo=jupyter">](https://grnet.readthedocs.io/en/latest/examples.html)
[<img src="https://img.shields.io/badge/GitHub-yo--aka--gene/grnet-181717?style=flat&logo=github">](https://github.com/yo-aka-gene/grnet)

- This repository is also for analysis codes in $"Article\;WIP"$

## Documentation
<img src="https://raw.githubusercontent.com/yo-aka-gene/grnet/main/docs/_static/title.PNG"> 

- Documentation and example codes (jupyter notebooks) are available in [https://grnet.readthedocs.io/en/latest/index.html](https://grnet.readthedocs.io/en/latest/index.html)

## Start Guide
### 1. Environment Preference
- MacOS
- Docker Desktop
- git

### 2. How to reproduce the virtual env
- clone [this repository](https://github.com/yo-aka-gene/grnet)
- activate the virtual env by runnning `init.sh` in `grnet/grnet_sandbox` directory. This shell script will automatically setup the virtual env and connect to it

    ```
    sh init.sh
    ```
    **Note**: Our docker container will occupy `localhost:8000`
- password for the JupyterLab server is `jupyter`
- install dependencies by calling the following inside the jupyter env
    ```
    sh lib.sh
    ```
### 3. Run codes
- to reproduce all outputs at a time with a pipeline, run codes in `/home/jovyan/code/experiment_execution.ipynb`
- If you are interested in taking a detailed look at each analysis, we have [online documentation](https://grnet.readthedocs.io/en/latest/index.html) and the same ipynb files are in `/home/jovyan/docs/notebooks` as well.
