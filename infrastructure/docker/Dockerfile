FROM python:3.8-slim-buster

WORKDIR /usr/src/app
COPY . .
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
  && echo 'ALL ALL = (ALL) NOPASSWD: ALL' >> /etc/sudoers

#============
# Helper tools
#============

RUN apt -qqy update \
  && apt -qqy install \
    wget \
    curl \
    bzip2 \
    fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 \
    libnspr4 libnss3 lsb-release xdg-utils libxss1 libdbus-glib-1-2 \
  && apt -qyy autoremove \
  && rm -rf /var/lib/apt/lists/* \
  && apt -qyy clean

#============
# GeckoDriver
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

#-----------------#
# Mozilla
#-----------------#
# Install all Firefox dependencies
# Adding libasound2 and others, credits to @jackTheRipper
#  https://github.com/SeleniumHQ/docker-selenium/pull/418
    # libasound2 \
    # libpulse-dev \
    # xul-ext-ubufox \
RUN apt -qqy update \
  && apt -qqy --no-install-recommends install \
    `apt-cache depends firefox | awk '/Depends:/{print$2}'` \
  && rm -rf /var/lib/apt/lists/* \
  && apt -qyy clean

#=============================
# sudo by default from now on
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

#USER seluser
CMD [ "ldd", "/usr/bin/firefox" ]
CMD [ "python", "./sleep.py" ]