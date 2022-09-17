FROM python
RUN mkdir -p /opt/great_expectations/ge_runner
WORKDIR /opt/great_expectations
ADD requirements.txt /opt/great_expectations/
RUN mkdir -p /root/.config/pip
ADD pip.ini /root/.config/pip/
RUN pip install -r requirements.txt
ENTRYPOINT [ "python" ]