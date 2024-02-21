FROM jupyter/datascience-notebook:lab-4.0.7

RUN pip install --upgrade pip
RUN pip install jupyterlab
RUN jupyter serverextension enable --py jupyterlab

WORKDIR $HOME
RUN mkdir config grnet notebooks output
COPY lib.sh /home/jovyan
COPY writelib.sh /home/jovyan

EXPOSE 8888
VOLUME ["/home/jovyan/jupyternb"]

CMD ['/bin/bash']
