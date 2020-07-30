# build
FROM python:3.7.6-slim as build-stage
WORKDIR /root/image_mosaic
COPY . /root/image_mosaic
RUN apt-get update \
&& apt-get install -y libopencv-dev
RUN pip install --upgrade pip \
&& pip install -r /root/image_mosaic/requirements.txt \
&& pip install /root/image_mosaic

# deploy
FROM python:3.7.6-slim
COPY --from=build-stage /root/.cache/pip /root/.cache/pip
COPY --from=build-stage /root/image_mosaic /root/image_mosaic
COPY --from=build-stage /usr/lib/x86_64-linux-gnu/libgthread-2.0.so.0 /usr/lib/x86_64-linux-gnu/libgthread-2.0.so.0
COPY --from=build-stage /usr/lib/x86_64-linux-gnu/libglib-2.0.so.0 /usr/lib/x86_64-linux-gnu/libglib-2.0.so.0
COPY --from=build-stage /usr/lib/x86_64-linux-gnu/libSM.so.6 /usr/lib/x86_64-linux-gnu/libSM.so.6
COPY --from=build-stage /usr/lib/x86_64-linux-gnu/libICE.so.6 /usr/lib/x86_64-linux-gnu/libICE.so.6
COPY --from=build-stage /usr/lib/x86_64-linux-gnu/libXrender.so.1 /usr/lib/x86_64-linux-gnu/libXrender.so.1
COPY --from=build-stage /usr/lib/x86_64-linux-gnu/libXext.so.6 /usr/lib/x86_64-linux-gnu/libXext.so.6
COPY --from=build-stage /usr/lib/x86_64-linux-gnu/libX11.so.6 /usr/lib/x86_64-linux-gnu/libX11.so.6
COPY --from=build-stage /usr/lib/x86_64-linux-gnu/libbsd.so.0 /usr/lib/x86_64-linux-gnu/libbsd.so.0
COPY --from=build-stage /usr/lib/x86_64-linux-gnu/libxcb.so.1 /usr/lib/x86_64-linux-gnu/libxcb.so.1
COPY --from=build-stage /usr/lib/x86_64-linux-gnu/libXau.so.6 /usr/lib/x86_64-linux-gnu/libXau.so.6
COPY --from=build-stage /usr/lib/x86_64-linux-gnu/libXdmcp.so.6 /usr/lib/x86_64-linux-gnu/libXdmcp.so.6

RUN apt-get update
RUN pip install -r /root/image_mosaic/requirements.txt \
&& pip install  /root/image_mosaic\
&& rm -rf /root/.cache/pip && rm -rf /root/image_mosaic
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

#ARG UID=1000
#ARG GID=1000

#RUN addgroup -gid ${GID} medusa && useradd -m --shell /bin/bash --gid ${GID} --uid ${UID} medusa
# && mkdir -p /medusa/public/system /medusa/public/assets \
# && chown -R medusa:medusa /medusa/public
#WORKDIR /image_mosaic
#COPY . /image_mosaic
#RUN chown -R medusa:medusa /image_mosaic
#USER medusa