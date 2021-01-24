FROM python:3.7-slim-buster

#============
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#============


WORKDIR /usr/src/app
COPY . .

#============
# Install Helper tools and FF lib dependencies
#============

RUN apt -qqy update \
  && apt -qqy install \
    wget \
    curl \
    bzip2 \
    libappindicator3-1 \
    libx11-xcb1 \
    libdbus-glib-1-2 \
    libxt6 \
  && rm -rf /var/lib/apt/lists/* \
  && apt -qyy clean


#========================================
# Install python requirements
#========================================
RUN pip install -r requirements.txt

#========================================
# Add normal user with passwordless sudo
#========================================
RUN useradd seluser \
         --shell /bin/bash  \
         --create-home \
  && usermod -a -G sudo seluser \
  && gpasswd -a seluser video \
  && echo 'seluser:secret' | chpasswd \
  && echo 'ALL ALL = (ALL) NOPASSWD: ALL' >> /etc/sudoers \
  && chown seluser:seluser -R /usr/src/app \
  && chmod -R 777 /usr/src/app \
  && chmod -R 777 /tmp

#============
# Install GeckoDriver
#============
ARG GECKODRIVER_VERSION=latest
RUN GK_VERSION=$(if [ ${GECKODRIVER_VERSION:-latest} = "latest" ]; then echo "0.28.0"; else echo $GECKODRIVER_VERSION; fi) \
  && echo "Using GeckoDriver version: "$GK_VERSION \
  && wget --no-verbose -O /tmp/geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v$GK_VERSION/geckodriver-v$GK_VERSION-linux64.tar.gz \
  && rm -rf /opt/geckodriver \
  && tar -C /opt -zxf /tmp/geckodriver.tar.gz \
  && rm /tmp/geckodriver.tar.gz \
  && mv /opt/geckodriver /opt/geckodriver-$GK_VERSION \
  && chmod 755 /opt/geckodriver-$GK_VERSION \
  && ln -fs /opt/geckodriver-$GK_VERSION /usr/bin/geckodriver



#=============================
# Use sudo by default from now on
#=============================
USER root

ENV FF_LANG="en-US" \
    FF_BASE_URL="https://archive.mozilla.org/pub" \
    FF_PLATFORM="linux-x86_64" \
    FF_INNER_PATH="firefox/releases"

ARG FF_VER="84.0"

ENV FF_COMP="firefox-${FF_VER}.tar.bz2"
ENV FF_URL="${FF_BASE_URL}/${FF_INNER_PATH}/${FF_VER}/${FF_PLATFORM}/${FF_LANG}/${FF_COMP}"
RUN cd /opt \
  && wget -nv "${FF_URL}" -O "firefox.tar.bz2" \
  && bzip2 -d "firefox.tar.bz2" \
  && tar xf "firefox.tar" \
  && rm "firefox.tar" \
  && ln -fs /opt/firefox/firefox /usr/bin/firefox \
  && chown -R seluser:seluser /opt/firefox \
  && chmod -R 777 /opt/firefox

LABEL selenium_firefox_version="${FF_VER}"


USER seluser
WORKDIR /tmp
ENTRYPOINT [ "python" ,"/usr/src/app/scraper.py" ]
CMD ["https://www.bbc.co.uk/news/topics/cp7r8vglgq1t/food"]