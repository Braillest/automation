FROM python:3.11

WORKDIR /braillest/scripts

RUN pip install --upgrade pip
RUN pip install requests
RUN pip install beautifulsoup4
RUN pip install svgwrite

RUN cd /usr/src
RUN curl -LO https://github.com/liblouis/liblouis/releases/download/v3.31.0/liblouis-3.31.0.tar.gz
RUN tar xfz liblouis-3.31.0.tar.gz
RUN cd liblouis-3.31.0 && autoconf && ./configure && make -j $(nproc) && make -j $(nproc) install && cd python && python setup.py install
RUN ldconfig

ENTRYPOINT sleep infinity
