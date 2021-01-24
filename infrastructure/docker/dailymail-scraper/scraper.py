#!/usr/bin/python3

"""
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import requests
import pandas
import re
import argparse
import os
import newspaper
from newspaper import Config
from newspaper import Article
from newspaper.utils import BeautifulSoup


foo = """
<div class="heateorSssClear"></div><div class="heateor_sss_sharing_container heateor_sss_horizontal_sharing" heateor-sss-data-href="https://www.technocracy.news/psychology-today-sex-robots-and-the-end-of-civilization/"><div class="heateor_sss_sharing_title" style="font-weight:bold">Please Share This Story!</div><ul class="heateor_sss_sharing_ul"><li class="heateorSssSharingRound"><i style="width:70px;height:35px;" alt="Facebook" title="Facebook" class="heateorSssSharing heateorSssFacebookBackground" onclick="heateorSssPopup(&quot;https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fwww.technocracy.news%2Fpsychology-today-sex-robots-and-the-end-of-civilization%2F&quot;)"><ss style="display:block;" class="heateorSssSharingSvg heateorSssFacebookSvg"></ss></i></li><li class="heateorSssSharingRound"><i style="width:70px;height:35px;" alt="Twitter" title="Twitter" class="heateorSssSharing heateorSssTwitterBackground" onclick="heateorSssPopup(&quot;http://twitter.com/intent/tweet?text=Psychology%20Today%3A%20Sex%20Robots%20And%20The%20End%20Of%20Civilization&amp;url=https%3A%2F%2Fwww.technocracy.news%2Fpsychology-today-sex-robots-and-the-end-of-civilization%2F&quot;)"><ss style="display:block;" class="heateorSssSharingSvg heateorSssTwitterSvg"></ss></i></li><li class="heateorSssSharingRound"><i style="width:70px;height:35px;" alt="Linkedin" title="Linkedin" class="heateorSssSharing heateorSssLinkedinBackground" onclick="heateorSssPopup(&quot;http://www.linkedin.com/shareArticle?mini=true&amp;url=https%3A%2F%2Fwww.technocracy.news%2Fpsychology-today-sex-robots-and-the-end-of-civilization%2F&amp;title=Psychology%20Today%3A%20Sex%20Robots%20And%20The%20End%20Of%20Civilization&quot;)"><ss style="display:block;" class="heateorSssSharingSvg heateorSssLinkedinSvg"></ss></i></li><li class="heateorSssSharingRound"><i style="width:70px;height:35px;" alt="MeWe" title="MeWe" class="heateorSssSharing heateorSssMeWeBackground" onclick="heateorSssPopup(&quot;https://mewe.com/share?link=https%3A%2F%2Fwww.technocracy.news%2Fpsychology-today-sex-robots-and-the-end-of-civilization%2F&quot;)"><ss style="display:block;" class="heateorSssSharingSvg heateorSssMeWeSvg"></ss></i></li><li class="heateorSssSharingRound"><i style="width:70px;height:35px;" alt="Whatsapp" title="Whatsapp" class="heateorSssSharing heateorSssWhatsappBackground" onclick="heateorSssPopup(&quot;https://web.whatsapp.com/send?text=Psychology%20Today%3A%20Sex%20Robots%20And%20The%20End%20Of%20Civilization https%3A%2F%2Fwww.technocracy.news%2Fpsychology-today-sex-robots-and-the-end-of-civilization%2F&quot;)"><ss style="display:block" class="heateorSssSharingSvg heateorSssWhatsappSvg"></ss></i></li><li class="heateorSssSharingRound"><i style="width:70px;height:35px;" alt="Reddit" title="Reddit" class="heateorSssSharing heateorSssRedditBackground" onclick="heateorSssPopup(&quot;http://reddit.com/submit?url=https%3A%2F%2Fwww.technocracy.news%2Fpsychology-today-sex-robots-and-the-end-of-civilization%2F&amp;title=Psychology%20Today%3A%20Sex%20Robots%20And%20The%20End%20Of%20Civilization&quot;)"><ss style="display:block;" class="heateorSssSharingSvg heateorSssRedditSvg"></ss></i></li><li class="heateorSssSharingRound"><i style="width:70px;height:35px;" alt="Email" title="Email" class="heateorSssSharing heateorSssEmailBackground" onclick="window.open('mailto:?subject=' + decodeURIComponent('Psychology%20Today%3A%20Sex%20Robots%20And%20The%20End%20Of%20Civilization' ).replace('&amp;', '%26') + '&amp;body=' + decodeURIComponent('https%3A%2F%2Fwww.technocracy.news%2Fpsychology-today-sex-robots-and-the-end-of-civilization%2F' ), '_blank')"><ss style="display:block" class="heateorSssSharingSvg heateorSssEmailSvg"></ss></i></li><li class="heateorSssSharingRound"><i style="width:70px;height:35px;" title="More" alt="More" class="heateorSssSharing heateorSssMoreBackground" onclick="heateorSssMoreSharingPopup(this, 'https://www.technocracy.news/psychology-today-sex-robots-and-the-end-of-civilization/', 'Psychology%20Today%3A%20Sex%20Robots%20And%20The%20End%20Of%20Civilization', '' )"><ss style="display:block" class="heateorSssSharingSvg heateorSssMoreSvg"></ss></i></li></ul><div class="heateorSssClear"></div></div><div class="heateorSssClear"></div><div class="pdfprnt-buttons pdfprnt-buttons-post pdfprnt-top-right"><a href="https://www.technocracy.news/psychology-today-sex-robots-and-the-end-of-civilization/?print=pdf" class="pdfprnt-button pdfprnt-button-pdf" target="_blank"><img data-lazyloaded="1" src="https://www.technocracy.news/wp-content/plugins/pdf-print/images/pdf.png" data-src="https://www.technocracy.news/wp-content/plugins/pdf-print/images/pdf.png" alt="image_pdf" title="View PDF" class="litespeed-loaded" data-was-processed="true"><noscript><img src="https://www.technocracy.news/wp-content/plugins/pdf-print/images/pdf.png" alt="image_pdf" title="View PDF" /></noscript></a><a href="https://www.technocracy.news/psychology-today-sex-robots-and-the-end-of-civilization/?print=print" class="pdfprnt-button pdfprnt-button-print" target="_blank"><img data-lazyloaded="1" src="https://www.technocracy.news/wp-content/plugins/pdf-print/images/print.png" data-src="https://www.technocracy.news/wp-content/plugins/pdf-print/images/print.png" alt="image_print" title="Print Content" class="litespeed-loaded" data-was-processed="true"><noscript><img src="https://www.technocracy.news/wp-content/plugins/pdf-print/images/print.png" alt="image_print" title="Print Content" /></noscript></a></div><div class="mailmunch-forms-before-post" style="display: none !important;"></div><div class="su-note" id="" style="border-color:#c0d8e3;border-radius:2px;-moz-border-radius:2px;-webkit-border-radius:2px;"><div class="su-note-inner su-u-clearfix su-u-trim" style="background-color:#daf2fd;border-color:#ffffff;color:#333333;border-radius:2px;-moz-border-radius:2px;-webkit-border-radius:2px;">With demographics already tanking in all Western nations, adding sex robots into the mix virtually guarantees to accelerate the trend and cause relationship dysfunction across the board. ⁃ TN Editor</div></div><p>Imagine this: A totally realistic robot of your own design that is capable of fully carrying out any&nbsp;<a href="https://www.psychologytoday.com/us/basics/sex" rel="nofollow noopener" target="_blank">sex</a>&nbsp;act that you can dream up. It looks, smells, and sounds incredibly realistic. And your state-sponsored insurance paid for her in full. In effect, she was free—prescribed by your physician to help with your status as officially “sexually dysfunctional.” Recent federal legislation, supported overwhelmingly by a male majority in the House and Senate, has made this kind of medical prescription perfectly legal.</p><p>Robin the Robot never has a headache. It never gets a cold. It never rejects an advance. It is, perhaps strangely, beautiful in many respects. And, surprisingly, it is even seemingly&nbsp;<a href="https://www.psychologytoday.com/us/basics/intelligence" rel="nofollow noopener" target="_blank">intelligent</a>&nbsp;and witty.</p><p>Sure, it sounds great on the surface.</p><p>And get this: According to expert clinical psychologist and sex therapist&nbsp;<a href="http://www.drbrandon.net/" rel="nofollow noopener" target="_blank">Dr. Marianne Brandon,</a>&nbsp;what I’ve described above is, in fact, a likely portrait of our near future. Welcome to the new world.</p><p><strong>Sex Robots as Supernormal Stimuli</strong></p><p>Earlier this month, I was fortunate to attend a special symposium on understanding mental health from an evolutionary perspective. This event, formally sponsored by the Applied&nbsp;<a href="https://www.psychologytoday.com/us/basics/evolutionary-psychology" rel="nofollow noopener" target="_blank">Evolutionary Psychology</a>&nbsp;Society (<a href="http://aepsociety.org/wordpress/" rel="nofollow noopener" target="_blank">AEPS</a>) and affiliated with the NorthEastern Evolutionary Psychology Society (<a href="http://neepsociety.com/" rel="nofollow noopener" target="_blank">NEEPS</a>), was eye-opening for the many scholars, practitioners, and students who were in attendance. And while all of the talks were provocative and engaging, I have to say that Dr. Brandon’s presentation was something of a show-stopper.</p><p>When you think about things from an evolutionary perspective, the history of human technology largely becomes the history of developing supernormal stimuli for profit.</p><p>In the 1950s, renowned behavioral biologist Niko Tinbergen articulated the idea of a&nbsp;<em>supernormal stimulus</em>. A supernormal stimulus is essentially an exaggerated, often human-made version of some stimulus that organisms evolved to respond to in certain ways.</p><p>For instance, humans evolved taste preferences so as to desire high-fat foods because our ancestors regularly experienced drought and famine. A Big Mac is a human-created product that includes an amplification of high-fat food that would have been beyond the fat and caloric content of nearly any food that would have existed under ancestral human conditions. The Big Mac is a classic supernormal stimulus.</p><p>Same with&nbsp;<a href="https://www.psychologytoday.com/us/basics/pornography" rel="nofollow noopener" target="_blank">pornography</a>. And video games. And so many cosmetic products that amplify attributes of faces and bodies that bear on Darwin’s bottom line of reproductive success. Vibrant hair color and lip gloss are supernormal stimuli.</p><div class="mailmunch-forms-in-post-middle" style="display: none !important;"></div><p>Importantly, as you can see, supernormal stimuli may well be deceitful. In the modern world of humans, supernormal stimuli are essentially hijackers. They are human-created technological products that hijack our evolved psychology in a way that leads to short-term emotional and/or physiological benefits. However, since these products are, at the end of the day, evolutionarily unnatural, they quite often do not lead to the long-term evolutionary benefits (such as strong connections with others and/or long-term reproductive gains) which pertain to why these stimuli evolved to be desired by humans in the first place. We can call this&nbsp;<em>evolutionary irony</em>.</p><p>In her presentation, Dr. Brandon rightfully pointed out that sex robots, when they arrive (and they will), will be the ultimate in human-created supernormal stimuli. And this could be a problem.</p><p><strong>Potential Problems Associated with the Sex Robot Revolution</strong></p><p>Is there a sex robot revolution on the horizon? In a few weeks, the city of Brussels will host the&nbsp;<a href="http://loveandsexwithrobots.org/" rel="nofollow noopener" target="_blank">4th International Conference on Love and Sex with Robots</a>, so you tell me!</p><p>In her presentation at the AEPS symposium, Dr. Brandon made a strong case suggesting that sex robots are truly in development and on the way. Perhaps in a decade or two.</p><p>Brandon pointed out several potential problems that may well come along with the robots for the ride. These problems all make sense when we think of our evolved relationship psychology. Some of the potential problems that she pointed out are as follows:</p><ul><li>Men, who are disproportionately represented as consumers of pornography, will likely be over-represented as consumers of sex robots.</li><li>Within committed relationships, sexual interactions, which are apparently already on a nationwide decline, are likely to drop further in prevalence.</li><li><a href="https://www.psychologytoday.com/us/basics/relationships" rel="nofollow noopener" target="_blank">Intimacy</a>&nbsp;in relationships, which strongly maps onto both quantity and quality of sexual interactions within mateships, is likely to drop in quality as well.</li><li>The prevalence of&nbsp;<a href="https://www.psychologytoday.com/us/basics/marriage" rel="nofollow noopener" target="_blank">marriage</a>&nbsp;and birth rates may well see declining numbers.</li><li><a href="https://www.psychologytoday.com/us/basics/motivation" rel="nofollow noopener" target="_blank">Motivation</a>&nbsp;for people to work on relationship problems within mateships will be naturally reduced.</li></ul><p>In short, the advent of sex robot technology may well foreshadow, in many ways, the demise of intimate relationships in the modern world.</p><p><a href="https://www.psychologytoday.com/us/blog/darwins-subterranean-world/201906/sex-robots-and-the-end-civilization" rel="nofollow noopener" target="_blank">Read full story here…</a></p><div class="mailmunch-forms-after-post" style="display: none !important;"></div><div class="crp_related  "><h3>Related Articles:</h3><ul><li><a href="https://www.technocracy.news/scientists-super-ai-might-emerge-like-coronavirus-to-destroy-civilization/" class="crp_link post-30318"><img data-lazyloaded="1" src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxNTAiIGhlaWdodD0iMTUwIiB2aWV3Qm94PSIwIDAgMTUwIDE1MCI+PHJlY3Qgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgZmlsbD0iI2NmZDRkYiIvPjwvc3ZnPg==" loading="lazy" data-src="https://www.technocracy.news/wp-content/uploads/2020/02/oren-etzioni-150x150.jpeg" class="crp_thumb crp_featured" alt="Super-AI Might Emerge Like Coronavirus To Destroy Civilization" title="Super-AI Might Emerge Like Coronavirus To Destroy Civilization" data-srcset="https://www.technocracy.news/wp-content/uploads/2020/02/oren-etzioni-150x150.jpeg 150w, https://www.technocracy.news/wp-content/uploads/2020/02/oren-etzioni-300x300.jpeg 300w, https://www.technocracy.news/wp-content/uploads/2020/02/oren-etzioni-100x100.jpeg 100w, https://www.technocracy.news/wp-content/uploads/2020/02/oren-etzioni-24x24.jpeg 24w, https://www.technocracy.news/wp-content/uploads/2020/02/oren-etzioni-48x48.jpeg 48w, https://www.technocracy.news/wp-content/uploads/2020/02/oren-etzioni-96x96.jpeg 96w" data-sizes="(max-width: 150px) 100vw, 150px" width="150" height="150"><noscript><img loading="lazy"  width="150" height="150"  src="https://www.technocracy.news/wp-content/uploads/2020/02/oren-etzioni-150x150.jpeg" class="crp_thumb crp_featured" alt="Super-AI Might Emerge Like Coronavirus To Destroy Civilization" title="Super-AI Might Emerge Like Coronavirus To Destroy Civilization" srcset="https://www.technocracy.news/wp-content/uploads/2020/02/oren-etzioni-150x150.jpeg 150w, https://www.technocracy.news/wp-content/uploads/2020/02/oren-etzioni-300x300.jpeg 300w, https://www.technocracy.news/wp-content/uploads/2020/02/oren-etzioni-100x100.jpeg 100w, https://www.technocracy.news/wp-content/uploads/2020/02/oren-etzioni-24x24.jpeg 24w, https://www.technocracy.news/wp-content/uploads/2020/02/oren-etzioni-48x48.jpeg 48w, https://www.technocracy.news/wp-content/uploads/2020/02/oren-etzioni-96x96.jpeg 96w" sizes="(max-width: 150px) 100vw, 150px" srcset="https://www.technocracy.news/wp-content/uploads/2020/02/oren-etzioni-150x150.jpeg 150w, https://www.technocracy.news/wp-content/uploads/2020/02/oren-etzioni-300x300.jpeg 300w, https://www.technocracy.news/wp-content/uploads/2020/02/oren-etzioni-100x100.jpeg 100w, https://www.technocracy.news/wp-content/uploads/2020/02/oren-etzioni-24x24.jpeg 24w, https://www.technocracy.news/wp-content/uploads/2020/02/oren-etzioni-48x48.jpeg 48w, https://www.technocracy.news/wp-content/uploads/2020/02/oren-etzioni-96x96.jpeg 96w" /></noscript><span class="crp_title">Super-AI Might Emerge Like Coronavirus To Destroy…</span></a></li><li><a href="https://www.technocracy.news/renewables-were-never-meant-to-power-modern-civilization/" class="crp_link post-28750"><img data-lazyloaded="1" src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxNTAiIGhlaWdodD0iMTUwIiB2aWV3Qm94PSIwIDAgMTUwIDE1MCI+PHJlY3Qgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgZmlsbD0iI2NmZDRkYiIvPjwvc3ZnPg==" loading="lazy" data-src="https://www.technocracy.news/wp-content/uploads/2016/09/giant-wind-turbines-150x150.jpg" class="crp_thumb crp_featured" alt="Renewables Were Never Meant To Power Modern Civilization" title="Renewables Were Never Meant To Power Modern Civilization" data-srcset="https://www.technocracy.news/wp-content/uploads/2016/09/giant-wind-turbines-150x150.jpg 150w, https://www.technocracy.news/wp-content/uploads/2016/09/giant-wind-turbines-300x300.jpg 300w, https://www.technocracy.news/wp-content/uploads/2016/09/giant-wind-turbines-100x100.jpg 100w" data-sizes="(max-width: 150px) 100vw, 150px" width="150" height="150"><noscript><img loading="lazy"  width="150" height="150"  src="https://www.technocracy.news/wp-content/uploads/2016/09/giant-wind-turbines-150x150.jpg" class="crp_thumb crp_featured" alt="Renewables Were Never Meant To Power Modern Civilization" title="Renewables Were Never Meant To Power Modern Civilization" srcset="https://www.technocracy.news/wp-content/uploads/2016/09/giant-wind-turbines-150x150.jpg 150w, https://www.technocracy.news/wp-content/uploads/2016/09/giant-wind-turbines-300x300.jpg 300w, https://www.technocracy.news/wp-content/uploads/2016/09/giant-wind-turbines-100x100.jpg 100w" sizes="(max-width: 150px) 100vw, 150px" srcset="https://www.technocracy.news/wp-content/uploads/2016/09/giant-wind-turbines-150x150.jpg 150w, https://www.technocracy.news/wp-content/uploads/2016/09/giant-wind-turbines-300x300.jpg 300w, https://www.technocracy.news/wp-content/uploads/2016/09/giant-wind-turbines-100x100.jpg 100w" /></noscript><span class="crp_title">Renewables Were Never Meant To Power Modern Civilization</span></a></li><li><a href="https://www.technocracy.news/first-test-of-immunity-passports-taking-place-today/" class="crp_link post-34017"><img data-lazyloaded="1" src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxNTAiIGhlaWdodD0iMTUwIiB2aWV3Qm94PSIwIDAgMTUwIDE1MCI+PHJlY3Qgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgZmlsbD0iI2NmZDRkYiIvPjwvc3ZnPg==" loading="lazy" data-src="https://www.technocracy.news/wp-content/uploads/2020/10/commonpass-150x150.png" class="crp_thumb crp_featured" alt="First Test Of &quot;Immunity Passports&quot; Taking Place Today" title="First Test Of &quot;Immunity Passports&quot; Taking Place Today" data-srcset="https://www.technocracy.news/wp-content/uploads/2020/10/commonpass-150x150.png 150w, https://www.technocracy.news/wp-content/uploads/2020/10/commonpass-250x250.png 250w, https://www.technocracy.news/wp-content/uploads/2020/10/commonpass-300x300.png 300w, https://www.technocracy.news/wp-content/uploads/2020/10/commonpass-100x100.png 100w, https://www.technocracy.news/wp-content/uploads/2020/10/commonpass-24x24.png 24w, https://www.technocracy.news/wp-content/uploads/2020/10/commonpass-48x48.png 48w, https://www.technocracy.news/wp-content/uploads/2020/10/commonpass-96x96.png 96w" data-sizes="(max-width: 150px) 100vw, 150px" width="150" height="150"><noscript><img loading="lazy"  width="150" height="150"  src="https://www.technocracy.news/wp-content/uploads/2020/10/commonpass-150x150.png" class="crp_thumb crp_featured" alt="First Test Of &quot;Immunity Passports&quot; Taking Place Today" title="First Test Of &quot;Immunity Passports&quot; Taking Place Today" srcset="https://www.technocracy.news/wp-content/uploads/2020/10/commonpass-150x150.png 150w, https://www.technocracy.news/wp-content/uploads/2020/10/commonpass-250x250.png 250w, https://www.technocracy.news/wp-content/uploads/2020/10/commonpass-300x300.png 300w, https://www.technocracy.news/wp-content/uploads/2020/10/commonpass-100x100.png 100w, https://www.technocracy.news/wp-content/uploads/2020/10/commonpass-24x24.png 24w, https://www.technocracy.news/wp-content/uploads/2020/10/commonpass-48x48.png 48w, https://www.technocracy.news/wp-content/uploads/2020/10/commonpass-96x96.png 96w" sizes="(max-width: 150px) 100vw, 150px" srcset="https://www.technocracy.news/wp-content/uploads/2020/10/commonpass-150x150.png 150w, https://www.technocracy.news/wp-content/uploads/2020/10/commonpass-250x250.png 250w, https://www.technocracy.news/wp-content/uploads/2020/10/commonpass-300x300.png 300w, https://www.technocracy.news/wp-content/uploads/2020/10/commonpass-100x100.png 100w, https://www.technocracy.news/wp-content/uploads/2020/10/commonpass-24x24.png 24w, https://www.technocracy.news/wp-content/uploads/2020/10/commonpass-48x48.png 48w, https://www.technocracy.news/wp-content/uploads/2020/10/commonpass-96x96.png 96w" /></noscript><span class="crp_title">First Test Of "Immunity Passports" Taking Place Today</span></a></li><li><a href="https://www.technocracy.news/todays-youth-rejects-capitalism/" class="crp_link post-12978"><img data-lazyloaded="1" src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxNTAiIGhlaWdodD0iMTUwIiB2aWV3Qm94PSIwIDAgMTUwIDE1MCI+PHJlY3Qgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgZmlsbD0iI2NmZDRkYiIvPjwvc3ZnPg==" loading="lazy" data-src="https://www.technocracy.news/wp-content/uploads/2017/11/in-science-we-trust-150x150.jpg" class="crp_thumb crp_featured" alt="Today's Youth Rejects Capitalism And Socialism; Will Technocracy Appeal To Them?" title="Today's Youth Rejects Capitalism And Socialism; Will Technocracy Appeal To Them?" data-srcset="https://www.technocracy.news/wp-content/uploads/2017/11/in-science-we-trust-150x150.jpg 150w, https://www.technocracy.news/wp-content/uploads/2017/11/in-science-we-trust-300x300.jpg 300w, https://www.technocracy.news/wp-content/uploads/2017/11/in-science-we-trust-100x100.jpg 100w" data-sizes="(max-width: 150px) 100vw, 150px" width="150" height="150"><noscript><img loading="lazy"  width="150" height="150"  src="https://www.technocracy.news/wp-content/uploads/2017/11/in-science-we-trust-150x150.jpg" class="crp_thumb crp_featured" alt="Today&#039;s Youth Rejects Capitalism And Socialism; Will Technocracy Appeal To Them?" title="Today&#039;s Youth Rejects Capitalism And Socialism; Will Technocracy Appeal To Them?" srcset="https://www.technocracy.news/wp-content/uploads/2017/11/in-science-we-trust-150x150.jpg 150w, https://www.technocracy.news/wp-content/uploads/2017/11/in-science-we-trust-300x300.jpg 300w, https://www.technocracy.news/wp-content/uploads/2017/11/in-science-we-trust-100x100.jpg 100w" sizes="(max-width: 150px) 100vw, 150px" srcset="https://www.technocracy.news/wp-content/uploads/2017/11/in-science-we-trust-150x150.jpg 150w, https://www.technocracy.news/wp-content/uploads/2017/11/in-science-we-trust-300x300.jpg 300w, https://www.technocracy.news/wp-content/uploads/2017/11/in-science-we-trust-100x100.jpg 100w" /></noscript><span class="crp_title">Today's Youth Rejects Capitalism And Socialism; Will…</span></a></li><li><a href="https://www.technocracy.news/usa-today-creating-clouds-stop-global-warming-wreak-havoc/" class="crp_link post-11864"><img data-lazyloaded="1" src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxNTAiIGhlaWdodD0iMTUwIiB2aWV3Qm94PSIwIDAgMTUwIDE1MCI+PHJlY3Qgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgZmlsbD0iI2NmZDRkYiIvPjwvc3ZnPg==" loading="lazy" data-src="https://www.technocracy.news/wp-content/uploads/2018/01/chemtrails-in-the-sky-150x150.png" class="crp_thumb crp_featured" alt="USA Today: Creating Clouds To Stop Global Warming Could Wreak Havoc" title="USA Today: Creating Clouds To Stop Global Warming Could Wreak Havoc" data-srcset="https://www.technocracy.news/wp-content/uploads/2018/01/chemtrails-in-the-sky-150x150.png 150w, https://www.technocracy.news/wp-content/uploads/2018/01/chemtrails-in-the-sky-300x300.png 300w, https://www.technocracy.news/wp-content/uploads/2018/01/chemtrails-in-the-sky-100x100.png 100w" data-sizes="(max-width: 150px) 100vw, 150px" width="150" height="150"><noscript><img loading="lazy"  width="150" height="150"  src="https://www.technocracy.news/wp-content/uploads/2018/01/chemtrails-in-the-sky-150x150.png" class="crp_thumb crp_featured" alt="USA Today: Creating Clouds To Stop Global Warming Could Wreak Havoc" title="USA Today: Creating Clouds To Stop Global Warming Could Wreak Havoc" srcset="https://www.technocracy.news/wp-content/uploads/2018/01/chemtrails-in-the-sky-150x150.png 150w, https://www.technocracy.news/wp-content/uploads/2018/01/chemtrails-in-the-sky-300x300.png 300w, https://www.technocracy.news/wp-content/uploads/2018/01/chemtrails-in-the-sky-100x100.png 100w" sizes="(max-width: 150px) 100vw, 150px" srcset="https://www.technocracy.news/wp-content/uploads/2018/01/chemtrails-in-the-sky-150x150.png 150w, https://www.technocracy.news/wp-content/uploads/2018/01/chemtrails-in-the-sky-300x300.png 300w, https://www.technocracy.news/wp-content/uploads/2018/01/chemtrails-in-the-sky-100x100.png 100w" /></noscript><span class="crp_title">USA Today: Creating Clouds To Stop Global Warming…</span></a></li><li><a href="https://www.technocracy.news/swiss-company-builds-factory-in-china-to-make-robots-with-robots/" class="crp_link post-14967"><img data-lazyloaded="1" src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxNTAiIGhlaWdodD0iMTUwIiB2aWV3Qm94PSIwIDAgMTUwIDE1MCI+PHJlY3Qgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgZmlsbD0iI2NmZDRkYiIvPjwvc3ZnPg==" loading="lazy" data-src="https://www.technocracy.news/wp-content/uploads/2018/10/factory-robots-150x150.jpg" class="crp_thumb crp_featured" alt="Swiss Company Builds Factory In China To Make Robots With Robots" title="Swiss Company Builds Factory In China To Make Robots With Robots" data-srcset="https://www.technocracy.news/wp-content/uploads/2018/10/factory-robots-150x150.jpg 150w, https://www.technocracy.news/wp-content/uploads/2018/10/factory-robots-300x300.jpg 300w, https://www.technocracy.news/wp-content/uploads/2018/10/factory-robots-100x100.jpg 100w, https://www.technocracy.news/wp-content/uploads/2018/10/factory-robots-24x24.jpg 24w, https://www.technocracy.news/wp-content/uploads/2018/10/factory-robots-48x48.jpg 48w, https://www.technocracy.news/wp-content/uploads/2018/10/factory-robots-96x96.jpg 96w" data-sizes="(max-width: 150px) 100vw, 150px" width="150" height="150"><noscript><img loading="lazy"  width="150" height="150"  src="https://www.technocracy.news/wp-content/uploads/2018/10/factory-robots-150x150.jpg" class="crp_thumb crp_featured" alt="Swiss Company Builds Factory In China To Make Robots With Robots" title="Swiss Company Builds Factory In China To Make Robots With Robots" srcset="https://www.technocracy.news/wp-content/uploads/2018/10/factory-robots-150x150.jpg 150w, https://www.technocracy.news/wp-content/uploads/2018/10/factory-robots-300x300.jpg 300w, https://www.technocracy.news/wp-content/uploads/2018/10/factory-robots-100x100.jpg 100w, https://www.technocracy.news/wp-content/uploads/2018/10/factory-robots-24x24.jpg 24w, https://www.technocracy.news/wp-content/uploads/2018/10/factory-robots-48x48.jpg 48w, https://www.technocracy.news/wp-content/uploads/2018/10/factory-robots-96x96.jpg 96w" sizes="(max-width: 150px) 100vw, 150px" srcset="https://www.technocracy.news/wp-content/uploads/2018/10/factory-robots-150x150.jpg 150w, https://www.technocracy.news/wp-content/uploads/2018/10/factory-robots-300x300.jpg 300w, https://www.technocracy.news/wp-content/uploads/2018/10/factory-robots-100x100.jpg 100w, https://www.technocracy.news/wp-content/uploads/2018/10/factory-robots-24x24.jpg 24w, https://www.technocracy.news/wp-content/uploads/2018/10/factory-robots-48x48.jpg 48w, https://www.technocracy.news/wp-content/uploads/2018/10/factory-robots-96x96.jpg 96w" /></noscript><span class="crp_title">Swiss Company Builds Factory In China To Make Robots…</span></a></li><li><a href="https://www.technocracy.news/rappoport-phase-one-and-phase-two-of-technocracys-civilization-lockdown/" class="crp_link post-34900"><img data-lazyloaded="1" src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxNTAiIGhlaWdodD0iMTUwIiB2aWV3Qm94PSIwIDAgMTUwIDE1MCI+PHJlY3Qgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgZmlsbD0iI2NmZDRkYiIvPjwvc3ZnPg==" loading="lazy" data-src="https://www.technocracy.news/wp-content/uploads/2021/01/AdobeStock_343268570-150x150.jpg" class="crp_thumb crp_featured" alt="Rappoport: Phase One And Phase Two Of Technocracy's Civilization Lockdown" title="Rappoport: Phase One And Phase Two Of Technocracy's Civilization Lockdown" data-srcset="https://www.technocracy.news/wp-content/uploads/2021/01/AdobeStock_343268570-150x150.jpg 150w, https://www.technocracy.news/wp-content/uploads/2021/01/AdobeStock_343268570-250x250.jpg 250w, https://www.technocracy.news/wp-content/uploads/2021/01/AdobeStock_343268570-300x300.jpg 300w, https://www.technocracy.news/wp-content/uploads/2021/01/AdobeStock_343268570-100x100.jpg 100w, https://www.technocracy.news/wp-content/uploads/2021/01/AdobeStock_343268570-24x24.jpg 24w, https://www.technocracy.news/wp-content/uploads/2021/01/AdobeStock_343268570-48x48.jpg 48w, https://www.technocracy.news/wp-content/uploads/2021/01/AdobeStock_343268570-96x96.jpg 96w" data-sizes="(max-width: 150px) 100vw, 150px" width="150" height="150"><noscript><img loading="lazy"  width="150" height="150"  src="https://www.technocracy.news/wp-content/uploads/2021/01/AdobeStock_343268570-150x150.jpg" class="crp_thumb crp_featured" alt="Rappoport: Phase One And Phase Two Of Technocracy&#039;s Civilization Lockdown" title="Rappoport: Phase One And Phase Two Of Technocracy&#039;s Civilization Lockdown" srcset="https://www.technocracy.news/wp-content/uploads/2021/01/AdobeStock_343268570-150x150.jpg 150w, https://www.technocracy.news/wp-content/uploads/2021/01/AdobeStock_343268570-250x250.jpg 250w, https://www.technocracy.news/wp-content/uploads/2021/01/AdobeStock_343268570-300x300.jpg 300w, https://www.technocracy.news/wp-content/uploads/2021/01/AdobeStock_343268570-100x100.jpg 100w, https://www.technocracy.news/wp-content/uploads/2021/01/AdobeStock_343268570-24x24.jpg 24w, https://www.technocracy.news/wp-content/uploads/2021/01/AdobeStock_343268570-48x48.jpg 48w, https://www.technocracy.news/wp-content/uploads/2021/01/AdobeStock_343268570-96x96.jpg 96w" sizes="(max-width: 150px) 100vw, 150px" srcset="https://www.technocracy.news/wp-content/uploads/2021/01/AdobeStock_343268570-150x150.jpg 150w, https://www.technocracy.news/wp-content/uploads/2021/01/AdobeStock_343268570-250x250.jpg 250w, https://www.technocracy.news/wp-content/uploads/2021/01/AdobeStock_343268570-300x300.jpg 300w, https://www.technocracy.news/wp-content/uploads/2021/01/AdobeStock_343268570-100x100.jpg 100w, https://www.technocracy.news/wp-content/uploads/2021/01/AdobeStock_343268570-24x24.jpg 24w, https://www.technocracy.news/wp-content/uploads/2021/01/AdobeStock_343268570-48x48.jpg 48w, https://www.technocracy.news/wp-content/uploads/2021/01/AdobeStock_343268570-96x96.jpg 96w" /></noscript><span class="crp_title">Rappoport: Phase One And Phase Two Of Technocracy's…</span></a></li></ul><div class="crp_clear"></div></div></div>
"""

def extract_urls(base_url) -> set:
    """
       Navigates from the  menu on website  to links articles

       @Returns A list of URL to articles
    """
    current_urls = []
    paper = newspaper.build(base_url, config=config, memoize_articles=False, language='en')
    #print(paper.size())
    for this_article in paper.articles:
        #print(this_article.url)
        current_urls.append(this_article.url)
    return current_urls


def filter_urls(url_to_check) -> bool:
    """ Filters the URLs collected so that  only those  from base_url domain
        are kept.
        @Returns  bool True  if URL is valid.
    """
    if search_url in url_to_check:
        return True
    else:
        return False


def clean_text(dirtytext):
    """ Cleans the text content collected so that text such as boilerplate form labels and empty space are removed
    /n are  kept which  may  cause a problem.
    @Returns  bool True  is content is valid
    """
    if len(dirtytext) < 3:
        return False
    elif dirtytext == '\nFirst Name:\n':
        return False
    elif dirtytext == '\nLast Name:\n':
        return False
    elif dirtytext == '\nEmail address: \n':
        return False
    else:
        return True


if __name__ == "__main__":

    """ This script scrapes the   website for  articles. 

        If URL passes the criteria defined by filter_url(), then it is visited and its content extracted using 
        Beautiful soup.  B. Soup cleans up the inner element text by converting it to UTF8.  
        URLs ending with a /#respond  are collected which needs to be stopped.
        
        The data extracted is saved to  a  dictionary

        article_content = {
        'url': [],
        'title': [],
        'author': [],
        'date': [],
        'tags': [],
        'text': [],
        }

    """

    """
       create argument parser to receive URL to scrape
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    args = parser.parse_args()
    search_url = args.url
    urls = []
    filtered_urls = []

    """ Configure newspaper user agent
    """
    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'
    config = Config()
    config.browser_user_agent = USER_AGENT
    config.request_timeout = 10

    """ Remove output file if it already exists
    """
    outputfile = '/tmp/output.json'
    try:
        os.remove(outputfile)
    except OSError as e:
        print("Error deleting: %s - %s." % (e.filename, e.strerror))
        pass

    """ Load the  search URL 
        Count the number  of pages in the topic
        Create a list of the URLs leading to valid articles 
    """
    try:
        urls = extract_urls(search_url)
        filtered_urls = [
            url for url in urls if filter_urls(url)
        ]
        print(f'The menu displayed on URL {search_url} leads to  { len(filtered_urls) } articles  to scrape')
    except Exception as e:
        print(e)

    article_content = {
            'url': [],
            'title': [],
            'author': [],
            'date': [],
            'tags': [],
            'text': [],
        }

    field_names = ['url', 'title', 'author',  'date', 'tags', 'text']

    for url_index, url in enumerate(filtered_urls):
        # print(url)
        try:
            article = newspaper.Article(url)
            article.download()
        except Exception as e:
            print(e)
            continue

        try:
            article.parse()
            soup = BeautifulSoup(article.html, 'html.parser')
        except Exception as e:
            print(e)

        try:

            #article_main = soup.find("div", attrs={"class": "entry-content"})
            #article_paragraphs = article_main.find_all_next("p")
            #string_list = [
            #    a.text for a in article_paragraphs if clean_text(a.text)
            #]
            #text = " ".join([sub.replace('\n', ' ') for sub in string_list])

            #scraped_date = soup.find("span", attrs={"class": "entry-meta-date updated"})
            #if article.publish_date is None and scraped_date is None:
            #    article.publish_date = "Publish Date not known"
            #if scraped_date is not None:
            #    article.publish_date = scraped_date.text

            #scraped_author = soup.find("span", attrs={"class": "entry-meta-author vcard author"})
            #if article.authors is None and article_author and scraped_author is None:
            #    article.authors = "Author not known"
            #if scraped_author is not None:
            #    article.authors = scraped_author.text

            article_content['url'].append(article.url)
            article_content['title'].append(article.title)
            article_content['author'].append(article.authors)
            article_content['date'].append(article.publish_date)
            article_content['tags'].append('')
            article_content['text'].append(article.text)

            #print(article_content)
        except AttributeError as e:
            print(e)
            continue
        except Exception as e:
            print(e)

        try:
            pandas.DataFrame.from_dict(article_content).to_json(outputfile)
        except Exception as e:
            print(e)

