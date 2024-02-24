FROM jupyter/datascience-notebook:lab-3.5.0

RUN pip install --upgrade pip
RUN pip install jupyterlab
RUN jupyter serverextension enable --py jupyterlab

WORKDIR $HOME
RUN mkdir config grnet notebooks output tools
RUN mv work data
COPY *.sh /home/jovyan

EXPOSE 8888
VOLUME ["/home/jovyan"]

CMD ['/bin/bash']
