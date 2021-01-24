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

#============
# Sets the firct URL which will be scraped by the container.
# ARG is the default and used if a build var is  not passed.
# If a build var is passed then ENV overides the default value.
#============
ARG URL_ENV="https://www.breitbart.com/"
ENV URL_ENV="${URL_ENV}"


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



#=============================
# Use sudo by default from now on
#=============================
USER root


USER seluser
WORKDIR /tmp
ENTRYPOINT [ "python" ,"/usr/src/app/scraper.py" ]
