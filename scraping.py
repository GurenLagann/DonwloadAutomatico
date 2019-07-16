import asyncio
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import re
from selenium import webdriver
import aiohttp


text = """
    <select id="fifochkid" name="fifochkid" size="5"></select>
    <table align="center" id="list-view" cellpadding="0" cellspacing="0">
        <thead>
        <td style="display: none;"><input type="checkbox" class="checkbox" name="chkall" id="chkall"
                                          onclick="toggle_all_checkbox('fifochkid', 'text');"/></td>
        <td title="Data" style="width: 75px;" nowrap><a href="javascript:void(0);" style="width: 100%; display: block;" onclick="set_order_by('calldate', 'asc')" title="Ordernar data por ordem crescente"><img src="/pbxip/themes/phone2b/images/bullet_arrow_down_small.gif?1562783368" title="Ordernar data por ordem crescente" align="absmiddle" style="float: right; padding: 2px; padding-top: 4px; : pointer; font-weight:bolder;">Data </a></td>
        <td title="Duração" style="width: 60px;" nowrap><a href="javascript:void(0);" style="width: 100%; display: block;" onclick="set_order_by('billsec', 'asc')" title="Ordernar duração"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" title="Ordernar duração" align="absmiddle" style="float: right; padding: 2px; padding-top: 4px; : pointer; font-weight:bolder;">Duração </a></td>

                <td title="Nº Origem" style="width: 20%;" nowrap><a href="javascript:void(0);" style="width: 100%; display: block;" onclick="set_order_by('src', 'asc')" title="Ordernar nº origem"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" title="Ordernar nº origem" align="absmiddle" style="float: right; padding: 2px; padding-top: 4px; : pointer; font-weight:bolder;">Nº Origem </a></td>
        <td title="Nº Destino" style="width: 35%;" nowrap><a href="javascript:void(0);" style="width: 100%; display: block;" onclick="set_order_by('dst', 'asc')" title="Ordernar nº destino"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" title="Ordernar nº destino" align="absmiddle" style="float: right; padding: 2px; padding-top: 4px; : pointer; font-weight:bolder;">Nº Destino </a></td>
        <td title="Status" style="width: 75px;" nowrap><a href="javascript:void(0);" style="width: 100%; display: block;" onclick="set_order_by('status', 'asc')" title="Ordernar status"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" title="Ordernar status" align="absmiddle" style="float: right; padding: 2px; padding-top: 4px; : pointer; font-weight:bolder;">Status </a></td>
        <td title="Tronco" style="width: 15%;" nowrap><a href="javascript:void(0);" style="width: 100%; display: block;" onclick="set_order_by('trunk', 'asc')" title="Ordernar tronco"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" title="Ordernar tronco" align="absmiddle" style="float: right; padding: 2px; padding-top: 4px; : pointer; font-weight:bolder;">Tronco </a></td>
        <td title="Tipo" style="width: 28%;" nowrap><a href="javascript:void(0);" style="width: 100%; display: block;" onclick="set_order_by('type', 'asc')" title="Ordernar tipo"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" title="Ordernar tipo" align="absmiddle" style="float: right; padding: 2px; padding-top: 4px; : pointer; font-weight:bolder;">Tipo </a></td>
        <td title="Custo (R$)" style="width: 75px;" align="right" nowrap><a href="javascript:void(0);" style="width: 100%; display: block;" onclick="set_order_by('cost', 'asc')" title="Ordernar custo (r$)"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" title="Ordernar custo (r$)" align="absmiddle" style="float: right; padding: 2px; padding-top: 4px; : pointer; font-weight:bolder;">Custo (R$) </a></td>
                    <td style="width: 30px;">&nbsp;</td>
                </thead>
                            <tbody id="tr_1" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_1" value="MQ.."
                                                      onclick="toggle_checkbox('1', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #cc6600;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91334'">10/07 15:28</td>
                    <td style="color: #cc6600;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91334'">00:00:00</td>
                                        <td style="color: #cc6600;" title="Ramal: Ramal 9005" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91334'">9005</td>
                    <td style="color: #cc6600;" title="5511993555262" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91334'">5511993555262</td>
                    <td style="color: #cc6600;" title="Não Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91334'">Não Atendida</td>
                    <td style="color: #cc6600;" title="1131000441LifeSP5656" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91334'">1131000441LifeSP5656</td>
                    <td style="color: #cc6600;" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91334'">Celular Local</td>
                    <td style="color: #cc6600;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91334'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_2" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_2" value="Mg.."
                                                      onclick="toggle_checkbox('2', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91333'">10/07 15:28</td>
                    <td style="" title="00:00:32" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91333'">00:00:32</td>
                                        <td style="" title="5513974198393" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91333'">5513974198393</td>
                    <td style="" title="Grupo: GP - Lifetime - 5653 » Ramal: ramal 2601 (2601)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91333'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_group.gif?1562783368" title="Grupo: GP - Lifetime - 5653" align="absmiddle" style="cursor: pointer;">  <img src="/pbxip/themes/phone2b/images/bullet_go_cf.gif?1562783368" title="Encaminhado" align="absmiddle"> 2601</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91333'">Atendida</td>
                    <td style="" title="1131000441LifeSP5648" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91333'">1131000441LifeSP5648</td>
                    <td style="" title="Entrante" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91333'">Entrante</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91333'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_2019071015627833062118201562783307wav5d262e887fbdd');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783368" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_2019071015627833062118201562783307wav5d262e887fbdd divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_2019071015627833062118201562783307wav5d262e887fbdd">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-1562783306.211820-1562783307.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-1562783306.211820-1562783307.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_2019071015627833062118201562783307wav5d262e887fbdd" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-1562783306.211820-1562783307.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783368" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-1562783306.211820-1562783307.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783368" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_3" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_3" value="Mw.."
                                                      onclick="toggle_checkbox('3', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #cc6600;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91332'">10/07 15:28</td>
                    <td style="color: #cc6600;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91332'">00:00:00</td>
                                        <td style="color: #cc6600;" title="Ramal: Ramal 9005" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91332'">9005</td>
                    <td style="color: #cc6600;" title="5511991768898" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91332'">5511991768898</td>
                    <td style="color: #cc6600;" title="Não Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91332'">Não Atendida</td>
                    <td style="color: #cc6600;" title="1131000441LifeSP5656" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91332'">1131000441LifeSP5656</td>
                    <td style="color: #cc6600;" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91332'">Celular Local</td>
                    <td style="color: #cc6600;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91332'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_4" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_4" value="NA.."
                                                      onclick="toggle_checkbox('4', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91331'">10/07 15:27</td>
                    <td style="" title="00:00:24" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91331'">00:00:24</td>
                                        <td style="" title="Ramal: Ramal 9005" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91331'">9005</td>
                    <td style="" title="5511992190590" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91331'">5511992190590</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91331'">Atendida</td>
                    <td style="" title="1131000441LifeSP5656" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91331'">1131000441LifeSP5656</td>
                    <td style="" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91331'">Celular Local</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91331'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_20190710152727900599219059015627832462118041562783247wav5d262e888328a');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783368" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_20190710152727900599219059015627832462118041562783247wav5d262e888328a divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_20190710152727900599219059015627832462118041562783247wav5d262e888328a">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-152727-9005-992190590-1562783246.211804-1562783247.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-152727-9005-992190590-1562783246.211804-1562783247.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_20190710152727900599219059015627832462118041562783247wav5d262e888328a" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-152727-9005-992190590-1562783246.211804-1562783247.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783368" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-152727-9005-992190590-1562783246.211804-1562783247.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783368" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_5" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_5" value="NQ.."
                                                      onclick="toggle_checkbox('5', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91330'">10/07 15:27</td>
                    <td style="" title="00:01:33" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91330'">00:01:33</td>
                                        <td style="" title="Ramal: Ramal 2802" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91330'">2802</td>
                    <td style="" title="Ramal: ramal 1603 (1603)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91330'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1562783368" title="Ramal: ramal 1603 (1603)" align="absmiddle" style="cursor: pointer;"> 1603</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91330'">Atendida</td>
                    <td style="" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91330'"></td>
                    <td style="" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91330'">Interno</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91330'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907101527242802160315627832432118011562783244wav5d262e88851ca');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783368" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907101527242802160315627832432118011562783244wav5d262e88851ca divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907101527242802160315627832432118011562783244wav5d262e88851ca">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-152724-2802-1603-1562783243.211801-1562783244.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-152724-2802-1603-1562783243.211801-1562783244.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907101527242802160315627832432118011562783244wav5d262e88851ca" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-152724-2802-1603-1562783243.211801-1562783244.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783368" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-152724-2802-1603-1562783243.211801-1562783244.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783368" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_6" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_6" value="Ng.."
                                                      onclick="toggle_checkbox('6', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91329'">10/07 15:26</td>
                    <td style="" title="00:00:02" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91329'">00:00:02</td>
                                        <td style="" title="Ramal: Ramal 9005" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91329'">9005</td>
                    <td style="" title="5511991467942" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91329'">5511991467942</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91329'">Atendida</td>
                    <td style="" title="1131000441LifeSP5656" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91329'">1131000441LifeSP5656</td>
                    <td style="" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91329'">Celular Local</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91329'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_20190710152633900599146794215627831932117961562783193wav5d262e8886d24');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783368" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_20190710152633900599146794215627831932117961562783193wav5d262e8886d24 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_20190710152633900599146794215627831932117961562783193wav5d262e8886d24">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-152633-9005-991467942-1562783193.211796-1562783193.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-152633-9005-991467942-1562783193.211796-1562783193.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_20190710152633900599146794215627831932117961562783193wav5d262e8886d24" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-152633-9005-991467942-1562783193.211796-1562783193.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783368" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-152633-9005-991467942-1562783193.211796-1562783193.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783368" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_7" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_7" value="Nw.."
                                                      onclick="toggle_checkbox('7', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #cc6600;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91327'">10/07 15:25</td>
                    <td style="color: #cc6600;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91327'">00:00:00</td>
                                        <td style="color: #cc6600;" title="Ramal: Ramal 9005" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91327'">9005</td>
                    <td style="color: #cc6600;" title="5511970673902" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91327'">5511970673902</td>
                    <td style="color: #cc6600;" title="Não Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91327'">Não Atendida</td>
                    <td style="color: #cc6600;" title="1131000441LifeSP5656" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91327'">1131000441LifeSP5656</td>
                    <td style="color: #cc6600;" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91327'">Celular Local</td>
                    <td style="color: #cc6600;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91327'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_8" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_8" value="OA.."
                                                      onclick="toggle_checkbox('8', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #cc6600;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91326'">10/07 15:25</td>
                    <td style="color: #cc6600;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91326'">00:00:00</td>
                                        <td style="color: #cc6600;" title="Ramal: Ramal 9005" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91326'">9005</td>
                    <td style="color: #cc6600;" title="5511976628685" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91326'">5511976628685</td>
                    <td style="color: #cc6600;" title="Não Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91326'">Não Atendida</td>
                    <td style="color: #cc6600;" title="1131000441LifeSP5656" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91326'">1131000441LifeSP5656</td>
                    <td style="color: #cc6600;" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91326'">Celular Local</td>
                    <td style="color: #cc6600;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91326'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_9" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_9" value="OQ.."
                                                      onclick="toggle_checkbox('9', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #990000;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91325'">10/07 15:25</td>
                    <td style="color: #990000;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91325'">00:00:00</td>
                                        <td style="color: #990000;" title="Ramal: Ramal 9005" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91325'">9005</td>
                    <td style="color: #990000;" title="5511989924248" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91325'">5511989924248</td>
                    <td style="color: #990000;" title="Falhou" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91325'">Falhou</td>
                    <td style="color: #990000;" title="1131000441LifeSP5656" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91325'">1131000441LifeSP5656</td>
                    <td style="color: #990000;" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91325'">Celular Local</td>
                    <td style="color: #990000;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91325'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_10" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_10" value="MTA."
                                                      onclick="toggle_checkbox('10', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91324'">10/07 15:24</td>
                    <td style="" title="00:00:12" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91324'">00:00:12</td>
                                        <td style="" title="Ramal: Ramal 1605" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91324'">1605</td>
                    <td style="" title="Ramal: ramal 1404 (1404) » Ramal: ramal 1410 (1410)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91324'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1562783368" title="Ramal: ramal 1404 (1404)" align="absmiddle" style="cursor: pointer;">  <img src="/pbxip/themes/phone2b/images/bullet_go_cf.gif?1562783368" title="Encaminhado" align="absmiddle"> 1410</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91324'">Atendida</td>
                    <td style="" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91324'"></td>
                    <td style="" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91324'">Interno</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91324'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907101524481605140415627830872117671562783088wav5d262e888da8a');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783368" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907101524481605140415627830872117671562783088wav5d262e888da8a divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907101524481605140415627830872117671562783088wav5d262e888da8a">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-152448-1605-1404-1562783087.211767-1562783088.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-152448-1605-1404-1562783087.211767-1562783088.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907101524481605140415627830872117671562783088wav5d262e888da8a" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-152448-1605-1404-1562783087.211767-1562783088.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783368" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-152448-1605-1404-1562783087.211767-1562783088.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783368" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_11" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_11" value="MTE."
                                                      onclick="toggle_checkbox('11', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91322'">10/07 15:24</td>
                    <td style="" title="00:00:05" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91322'">00:00:05</td>
                                        <td style="" title="Ramal: Ramal 2804" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91322'">2804</td>
                    <td style="" title="Ramal: Ramal 1406 (1406)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91322'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1562783368" title="Ramal: Ramal 1406 (1406)" align="absmiddle" style="cursor: pointer;"> 1406</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91322'">Atendida</td>
                    <td style="" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91322'"></td>
                    <td style="" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91322'">Interno</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91322'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907101524462804140615627830852117641562783086wav5d262e888f9c9');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783368" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907101524462804140615627830852117641562783086wav5d262e888f9c9 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907101524462804140615627830852117641562783086wav5d262e888f9c9">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-152446-2804-1406-1562783085.211764-1562783086.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-152446-2804-1406-1562783085.211764-1562783086.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907101524462804140615627830852117641562783086wav5d262e888f9c9" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-152446-2804-1406-1562783085.211764-1562783086.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783368" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-152446-2804-1406-1562783085.211764-1562783086.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783368" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_12" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_12" value="MTI."
                                                      onclick="toggle_checkbox('12', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91323'">10/07 15:24</td>
                    <td style="" title="00:00:06" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91323'">00:00:06</td>
                                        <td style="" title="Ramal: Ramal 9005" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91323'">9005</td>
                    <td style="" title="5511988919559" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91323'">5511988919559</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91323'">Atendida</td>
                    <td style="" title="1131000441LifeSP5656" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91323'">1131000441LifeSP5656</td>
                    <td style="" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91323'">Celular Local</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91323'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_20190710152428900598891955915627830682117601562783068wav5d262e889151e');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783368" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_20190710152428900598891955915627830682117601562783068wav5d262e889151e divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_20190710152428900598891955915627830682117601562783068wav5d262e889151e">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-152428-9005-988919559-1562783068.211760-1562783068.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-152428-9005-988919559-1562783068.211760-1562783068.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_20190710152428900598891955915627830682117601562783068wav5d262e889151e" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-152428-9005-988919559-1562783068.211760-1562783068.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783368" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-152428-9005-988919559-1562783068.211760-1562783068.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783368" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_13" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_13" value="MTM."
                                                      onclick="toggle_checkbox('13', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91321'">10/07 15:24</td>
                    <td style="" title="00:00:35" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91321'">00:00:35</td>
                                        <td style="" title="5511997612100" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91321'">5511997612100</td>
                    <td style="" title="Grupo: GP - Lifetime - 5656 » Ramal: Ramal 2804 (2804)" nowrap
                       ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91321'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_group.gif?1562783368" title="Grupo: GP - Lifetime - 5656" align="absmiddle" style="cursor: pointer;">  <img src="/pbxip/themes/phone2b/images/bullet_go_cf.gif?1562783368" title="Encaminhado" align="absmiddle"> 2804</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91321'">Atendida</td>
                    <td style="" title="1131000441LifeSP5648" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91321'">1131000441LifeSP5648</td>
                    <td style="" title="Entrante" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91321'">Entrante</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91321'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_2019071015627830522117551562783053wav5d262e889345c');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783368" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_2019071015627830522117551562783053wav5d262e889345c divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_2019071015627830522117551562783053wav5d262e889345c">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-1562783052.211755-1562783053.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-1562783052.211755-1562783053.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_2019071015627830522117551562783053wav5d262e889345c" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-1562783052.211755-1562783053.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783368" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-1562783052.211755-1562783053.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783368" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_14" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_14" value="MTQ."
                                                      onclick="toggle_checkbox('14', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #cc6600;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91320'">10/07 15:24</td>
                    <td style="color: #cc6600;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91320'">00:00:00</td>
                                        <td style="color: #cc6600;" title="Ramal: Ramal 9005" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91320'">9005</td>
                    <td style="color: #cc6600;" title="5511989970485" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91320'">5511989970485</td>
                    <td style="color: #cc6600;" title="Não Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91320'">Não Atendida</td>
                    <td style="color: #cc6600;" title="1131000441LifeSP5656" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91320'">1131000441LifeSP5656</td>
                    <td style="color: #cc6600;" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91320'">Celular Local</td>
                    <td style="color: #cc6600;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91320'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_15" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_15" value="MTU."
                                                      onclick="toggle_checkbox('15', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91317'">10/07 15:22</td>
                    <td style="" title="00:00:19" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91317'">00:00:19</td>
                                        <td style="" title="Ramal: Ramal 9005" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91317'">9005</td>
                    <td style="" title="5511994538237" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91317'">5511994538237</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91317'">Atendida</td>
                    <td style="" title="1131000441LifeSP5656" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91317'">1131000441LifeSP5656</td>
                    <td style="" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91317'">Celular Local</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91317'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_20190710152258900599453823715627829782117471562782978wav5d262e8896724');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783368" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_20190710152258900599453823715627829782117471562782978wav5d262e8896724 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_20190710152258900599453823715627829782117471562782978wav5d262e8896724">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-152258-9005-994538237-1562782978.211747-1562782978.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-152258-9005-994538237-1562782978.211747-1562782978.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_20190710152258900599453823715627829782117471562782978wav5d262e8896724" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-152258-9005-994538237-1562782978.211747-1562782978.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783368" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-152258-9005-994538237-1562782978.211747-1562782978.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783368" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_16" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_16" value="MTY."
                                                      onclick="toggle_checkbox('16', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #990000;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91316'">10/07 15:22</td>
                    <td style="color: #990000;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91316'">00:00:00</td>
                                        <td style="color: #990000;" title="Ramal: Ramal 9005" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91316'">9005</td>
                    <td style="color: #990000;" title="5511995129710" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91316'">5511995129710</td>
                    <td style="color: #990000;" title="Falhou" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91316'">Falhou</td>
                    <td style="color: #990000;" title="1131000441LifeSP5656" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91316'">1131000441LifeSP5656</td>
                    <td style="color: #990000;" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91316'">Celular Local</td>
                    <td style="color: #990000;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91316'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_17" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_17" value="MTc."
                                                      onclick="toggle_checkbox('17', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91319'">10/07 15:21</td>
                    <td style="" title="00:03:01" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91319'">00:03:01</td>
                                        <td style="" title="Ramal: ramal 2205" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91319'">2205</td>
                    <td style="" title="Ramal: ramal 2203 (2203)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91319'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1562783368" title="Ramal: ramal 2203 (2203)" align="absmiddle" style="cursor: pointer;"> 2203</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91319'">Atendida</td>
                    <td style="" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91319'"></td>
                    <td style="" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91319'">Interno</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91319'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907101521532205220315627829132117401562782913wav5d262e8899e21');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783368" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907101521532205220315627829132117401562782913wav5d262e8899e21 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907101521532205220315627829132117401562782913wav5d262e8899e21">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-152153-2205-2203-1562782913.211740-1562782913.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-152153-2205-2203-1562782913.211740-1562782913.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907101521532205220315627829132117401562782913wav5d262e8899e21" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-152153-2205-2203-1562782913.211740-1562782913.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783368" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-152153-2205-2203-1562782913.211740-1562782913.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783368" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_18" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_18" value="MTg."
                                                      onclick="toggle_checkbox('18', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91315'">10/07 15:21</td>
                    <td style="" title="00:00:09" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91315'">00:00:09</td>
                                        <td style="" title="Ramal: Ramal 9005" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91315'">9005</td>
                    <td style="" title="5511981740001" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91315'">5511981740001</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91315'">Atendida</td>
                    <td style="" title="1131000441LifeSP5656" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91315'">1131000441LifeSP5656</td>
                    <td style="" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91315'">Celular Local</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91315'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_20190710152137900598174000115627828972117311562782897wav5d262e889b92e');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783368" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_20190710152137900598174000115627828972117311562782897wav5d262e889b92e divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_20190710152137900598174000115627828972117311562782897wav5d262e889b92e">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-152137-9005-981740001-1562782897.211731-1562782897.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-152137-9005-981740001-1562782897.211731-1562782897.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_20190710152137900598174000115627828972117311562782897wav5d262e889b92e" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-152137-9005-981740001-1562782897.211731-1562782897.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783368" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-152137-9005-981740001-1562782897.211731-1562782897.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783368" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_19" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_19" value="MTk."
                                                      onclick="toggle_checkbox('19', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91318'">10/07 15:21</td>
                    <td style="" title="00:03:18" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91318'">00:03:18</td>
                                        <td style="" title="552132132350" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91318'">552132132350</td>
                    <td style="" title="Grupo: GP - Lifetime - 5650 » Ramal: Ramal 2204 (2204)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91318'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_group.gif?1562783368" title="Grupo: GP - Lifetime - 5650" align="absmiddle" style="cursor: pointer;">  <img src="/pbxip/themes/phone2b/images/bullet_go_cf.gif?1562783368" title="Encaminhado" align="absmiddle"> 2204</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91318'">Atendida</td>
                    <td style="" title="1131000441LifeSP5648" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91318'">1131000441LifeSP5648</td>
                    <td style="" title="Entrante" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91318'">Entrante</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91318'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_2019071015627828922117261562782893wav5d262e889d491');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783368" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_2019071015627828922117261562782893wav5d262e889d491 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_2019071015627828922117261562782893wav5d262e889d491">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-1562782892.211726-1562782893.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-1562782892.211726-1562782893.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_2019071015627828922117261562782893wav5d262e889d491" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-1562782892.211726-1562782893.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783368" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-1562782892.211726-1562782893.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783368" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_20" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_20" value="MjA."
                                                      onclick="toggle_checkbox('20', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #cc6600;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91312'">10/07 15:21</td>
                    <td style="color: #cc6600;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91312'">00:00:00</td>
                                        <td style="color: #cc6600;" title="Ramal: Ramal 9005" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91312'">9005</td>
                    <td style="color: #cc6600;" title="5511999934034" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91312'">5511999934034</td>
                    <td style="color: #cc6600;" title="Não Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91312'">Não Atendida</td>
                    <td style="color: #cc6600;" title="1131000441LifeSP5656" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91312'">1131000441LifeSP5656</td>
                    <td style="color: #cc6600;" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91312'">Celular Local</td>
                    <td style="color: #cc6600;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91312'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_21" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_21" value="MjE."
                                                      onclick="toggle_checkbox('21', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #cc6600;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91311'">10/07 15:20</td>
                    <td style="color: #cc6600;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91311'">00:00:00</td>
                                        <td style="color: #cc6600;" title="Ramal: ramal 1414" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91311'">1414</td>
                    <td style="color: #cc6600;" title="5521979133200" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91311'">5521979133200</td>
                    <td style="color: #cc6600;" title="Não Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91311'">Não Atendida</td>
                    <td style="color: #cc6600;" title="1131000441LifeSP5635" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91311'">1131000441LifeSP5635</td>
                    <td style="color: #cc6600;" title="Celular Nacional" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91311'">Celular Nacional</td>
                    <td style="color: #cc6600;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91311'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_22" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_22" value="MjI."
                                                      onclick="toggle_checkbox('22', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #cc6600;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91310'">10/07 15:19</td>
                    <td style="color: #cc6600;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91310'">00:00:00</td>
                                        <td style="color: #cc6600;" title="Ramal: ramal 1414" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91310'">1414</td>
                    <td style="color: #cc6600;" title="5521979133200" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91310'">5521979133200</td>
                    <td style="color: #cc6600;" title="Não Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91310'">Não Atendida</td>
                    <td style="color: #cc6600;" title="1131000441LifeSP5635" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91310'">1131000441LifeSP5635</td>
                    <td style="color: #cc6600;" title="Celular Nacional" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91310'">Celular Nacional</td>
                    <td style="color: #cc6600;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91310'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_23" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_23" value="MjM."
                                                      onclick="toggle_checkbox('23', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91314'">10/07 15:19</td>
                    <td style="" title="00:02:39" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91314'">00:02:39</td>
                                        <td style="" title="5521964069197" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91314'">5521964069197</td>
                    <td style="" title="Grupo: GP - Lifetime - 5640 - Mesa » Ramal: ramal 1410 (1410)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91314'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_group.gif?1562783368" title="Grupo: GP - Lifetime - 5640 - Mesa" align="absmiddle" style="cursor: pointer;">  <img src="/pbxip/themes/phone2b/images/bullet_go_cf.gif?1562783368" title="Encaminhado" align="absmiddle"> 1410</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91314'">Atendida</td>
                    <td style="" title="1131000441LifeSP5648" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91314'">1131000441LifeSP5648</td>
                    <td style="" title="Entrante" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91314'">Entrante</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91314'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_2019071015627827512117011562782752wav5d262e88a3630');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783368" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_2019071015627827512117011562782752wav5d262e88a3630 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_2019071015627827512117011562782752wav5d262e88a3630">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-1562782751.211701-1562782752.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-1562782751.211701-1562782752.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_2019071015627827512117011562782752wav5d262e88a3630" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-1562782751.211701-1562782752.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783368" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-1562782751.211701-1562782752.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783368" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_24" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_24" value="MjQ."
                                                      onclick="toggle_checkbox('24', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91309'">10/07 15:16</td>
                    <td style="" title="00:00:38" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91309'">00:00:38</td>
                                        <td style="" title="Ramal: Ramal 9005" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91309'">9005</td>
                    <td style="" title="5511956518907" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91309'">5511956518907</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91309'">Atendida</td>
                    <td style="" title="1131000441LifeSP5656" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91309'">1131000441LifeSP5656</td>
                    <td style="" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91309'">Celular Local</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91309'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_20190710151653900595651890715627826122116961562782613wav5d262e88a5185');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783368" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_20190710151653900595651890715627826122116961562782613wav5d262e88a5185 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_20190710151653900595651890715627826122116961562782613wav5d262e88a5185">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-151653-9005-956518907-1562782612.211696-1562782613.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-151653-9005-956518907-1562782612.211696-1562782613.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_20190710151653900595651890715627826122116961562782613wav5d262e88a5185" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-151653-9005-956518907-1562782612.211696-1562782613.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783368" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-151653-9005-956518907-1562782612.211696-1562782613.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783368" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_25" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_25" value="MjU."
                                                      onclick="toggle_checkbox('25', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91306'">10/07 15:15</td>
                    <td style="" title="00:00:15" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91306'">00:00:15</td>
                                        <td style="" title="Ramal: Ramal 9005" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91306'">9005</td>
                    <td style="" title="5511982557473" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91306'">5511982557473</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91306'">Atendida</td>
                    <td style="" title="1131000441LifeSP5656" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91306'">1131000441LifeSP5656</td>
                    <td style="" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91306'">Celular Local</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91306'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_20190710151559900598255747315627825582116921562782559wav5d262e88a6ce6');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783368" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_20190710151559900598255747315627825582116921562782559wav5d262e88a6ce6 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_20190710151559900598255747315627825582116921562782559wav5d262e88a6ce6">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-151559-9005-982557473-1562782558.211692-1562782559.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-151559-9005-982557473-1562782558.211692-1562782559.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_20190710151559900598255747315627825582116921562782559wav5d262e88a6ce6" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-151559-9005-982557473-1562782558.211692-1562782559.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783368" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-151559-9005-982557473-1562782558.211692-1562782559.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783368" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_26" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_26" value="MjY."
                                                      onclick="toggle_checkbox('26', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #cc6600;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91305'">10/07 15:15</td>
                    <td style="color: #cc6600;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91305'">00:00:00</td>
                                        <td style="color: #cc6600;" title="Ramal: ramal 1414" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91305'">1414</td>
                    <td style="color: #cc6600;" title="5511998420088" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91305'">5511998420088</td>
                    <td style="color: #cc6600;" title="Não Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91305'">Não Atendida</td>
                    <td style="color: #cc6600;" title="1131000441LifeSP5635" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91305'">1131000441LifeSP5635</td>
                    <td style="color: #cc6600;" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91305'">Celular Local</td>
                    <td style="color: #cc6600;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91305'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_27" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_27" value="Mjc."
                                                      onclick="toggle_checkbox('27', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #cc6600;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91304'">10/07 15:15</td>
                    <td style="color: #cc6600;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91304'">00:00:00</td>
                                        <td style="color: #cc6600;" title="Ramal: Ramal 9005" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91304'">9005</td>
                    <td style="color: #cc6600;" title="5511982557473" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91304'">5511982557473</td>
                    <td style="color: #cc6600;" title="Não Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91304'">Não Atendida</td>
                    <td style="color: #cc6600;" title="1131000441LifeSP5656" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91304'">1131000441LifeSP5656</td>
                    <td style="color: #cc6600;" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91304'">Celular Local</td>
                    <td style="color: #cc6600;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91304'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_28" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_28" value="Mjg."
                                                      onclick="toggle_checkbox('28', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91308'">10/07 15:15</td>
                    <td style="" title="00:01:31" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91308'">00:01:31</td>
                                        <td style="" title="Ramal: Ramal 2804" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91308'">2804</td>
                    <td style="" title="Ramal: ramal 1410 (1410)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91308'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1562783368" title="Ramal: ramal 1410 (1410)" align="absmiddle" style="cursor: pointer;"> 1410</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91308'">Atendida</td>
                    <td style="" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91308'"></td>
                    <td style="" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91308'">Interno</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91308'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907101515372804141015627825372116811562782537wav5d262e88abb02');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783368" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907101515372804141015627825372116811562782537wav5d262e88abb02 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907101515372804141015627825372116811562782537wav5d262e88abb02">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-151537-2804-1410-1562782537.211681-1562782537.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-151537-2804-1410-1562782537.211681-1562782537.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907101515372804141015627825372116811562782537wav5d262e88abb02" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-151537-2804-1410-1562782537.211681-1562782537.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783368" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-151537-2804-1410-1562782537.211681-1562782537.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783368" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_29" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_29" value="Mjk."
                                                      onclick="toggle_checkbox('29', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91303'">10/07 15:15</td>
                    <td style="" title="00:00:04" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91303'">00:00:04</td>
                                        <td style="" title="Ramal: ramal 1414" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91303'">1414</td>
                    <td style="" title="5511998420088" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91303'">5511998420088</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91303'">Atendida</td>
                    <td style="" title="1131000441LifeSP5635" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91303'">1131000441LifeSP5635</td>
                    <td style="" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91303'">Celular Local</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91303'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_20190710151519141499842008815627825192116771562782519wav5d262e88ad686');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783368" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_20190710151519141499842008815627825192116771562782519wav5d262e88ad686 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_20190710151519141499842008815627825192116771562782519wav5d262e88ad686">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-151519-1414-998420088-1562782519.211677-1562782519.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-151519-1414-998420088-1562782519.211677-1562782519.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_20190710151519141499842008815627825192116771562782519wav5d262e88ad686" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-151519-1414-998420088-1562782519.211677-1562782519.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783368" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-151519-1414-998420088-1562782519.211677-1562782519.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783368" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_30" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_30" value="MzA."
                                                      onclick="toggle_checkbox('30', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91307'">10/07 15:14</td>
                    <td style="" title="00:02:53" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91307'">00:02:53</td>
                                        <td style="" title="Ramal: ramal 1409" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91307'">1409</td>
                    <td style="" title="Ramal: Ramal 2810 (2810)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91307'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1562783368" title="Ramal: Ramal 2810 (2810)" align="absmiddle" style="cursor: pointer;"> 2810</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91307'">Atendida</td>
                    <td style="" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91307'"></td>
                    <td style="" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91307'">Interno</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91307'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907101514471409281015627824862116741562782487wav5d262e88af59a');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783368" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907101514471409281015627824862116741562782487wav5d262e88af59a divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907101514471409281015627824862116741562782487wav5d262e88af59a">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-151447-1409-2810-1562782486.211674-1562782487.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-151447-1409-2810-1562782486.211674-1562782487.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907101514471409281015627824862116741562782487wav5d262e88af59a" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-151447-1409-2810-1562782486.211674-1562782487.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783368" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-151447-1409-2810-1562782486.211674-1562782487.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783368" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_31" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_31" value="MzE."
                                                      onclick="toggle_checkbox('31', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91302'">10/07 15:13</td>
                    <td style="" title="00:01:47" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91302'">00:01:47</td>
                                        <td style="" title="Ramal: ramal 2601" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91302'">2601</td>
                    <td style="" title="551155097151" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91302'">551155097151</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91302'">Atendida</td>
                    <td style="" title="1131000441LifeSP5653" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91302'">1131000441LifeSP5653</td>
                    <td style="" title="Fixo Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91302'">Fixo Local</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91302'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_2019071015135226015509715115627824322116701562782432wav5d262e88b10f0');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783368" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_2019071015135226015509715115627824322116701562782432wav5d262e88b10f0 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_2019071015135226015509715115627824322116701562782432wav5d262e88b10f0">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-151352-2601-55097151-1562782432.211670-1562782432.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-151352-2601-55097151-1562782432.211670-1562782432.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_2019071015135226015509715115627824322116701562782432wav5d262e88b10f0" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-151352-2601-55097151-1562782432.211670-1562782432.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783368" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-151352-2601-55097151-1562782432.211670-1562782432.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783368" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_32" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_32" value="MzI."
                                                      onclick="toggle_checkbox('32', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #cc6600;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91301'">10/07 15:13</td>
                    <td style="color: #cc6600;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91301'">00:00:00</td>
                                        <td style="color: #cc6600;" title="Ramal: ramal 1410" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91301'">1410</td>
                    <td style="color: #cc6600;" title="Ramal: Ramal 2807 (2807)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91301'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1562783368" title="Ramal: Ramal 2807 (2807)" align="absmiddle" style="cursor: pointer;"> 2807</td>
                    <td style="color: #cc6600;" title="Não Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91301'">Não Atendida</td>
                    <td style="color: #cc6600;" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91301'"></td>
                    <td style="color: #cc6600;" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91301'">Interno</td>
                    <td style="color: #cc6600;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91301'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_33" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_33" value="MzM."
                                                      onclick="toggle_checkbox('33', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91300'">10/07 15:11</td>
                    <td style="" title="00:00:52" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91300'">00:00:52</td>
                                        <td style="" title="Ramal: Ramal 9005" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91300'">9005</td>
                    <td style="" title="Ramal: ramal 1405 (1405)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91300'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1562783368" title="Ramal: ramal 1405 (1405)" align="absmiddle" style="cursor: pointer;"> 1405</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91300'">Atendida</td>
                    <td style="" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91300'"></td>
                    <td style="" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91300'">Interno</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91300'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907101511099005140515627822682116631562782269wav5d262e88b4b89');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783368" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907101511099005140515627822682116631562782269wav5d262e88b4b89 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907101511099005140515627822682116631562782269wav5d262e88b4b89">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-151109-9005-1405-1562782268.211663-1562782269.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-151109-9005-1405-1562782268.211663-1562782269.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907101511099005140515627822682116631562782269wav5d262e88b4b89" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-151109-9005-1405-1562782268.211663-1562782269.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783368" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-151109-9005-1405-1562782268.211663-1562782269.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783368" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_34" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_34" value="MzQ."
                                                      onclick="toggle_checkbox('34', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #cc6600;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91297'">10/07 15:09</td>
                    <td style="color: #cc6600;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91297'">00:00:00</td>
                                        <td style="color: #cc6600;" title="Ramal: Ramal 7005" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91297'">7005</td>
                    <td style="color: #cc6600;" title="5567984772433" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91297'">5567984772433</td>
                    <td style="color: #cc6600;" title="Não Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91297'">Não Atendida</td>
                    <td style="color: #cc6600;" title="1131000441_Campo" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91297'">1131000441_Campo</td>
                    <td style="color: #cc6600;" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91297'">Celular Local</td>
                    <td style="color: #cc6600;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91297'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_35" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_35" value="MzU."
                                                      onclick="toggle_checkbox('35', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91296'">10/07 15:09</td>
                    <td style="" title="00:00:08" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91296'">00:00:08</td>
                                        <td style="" title="551136606400" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91296'">551136606400</td>
                    <td style="" title="551133855635" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91296'">551133855635</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91296'">Atendida</td>
                    <td style="" title="1131000441LifeSP5648" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91296'">1131000441LifeSP5648</td>
                    <td style="" title="Entrante" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91296'">Entrante</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91296'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_36" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_36" value="MzY."
                                                      onclick="toggle_checkbox('36', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91295'">10/07 15:09</td>
                    <td style="" title="00:00:01" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91295'">00:00:01</td>
                                        <td style="" title="551136606400" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91295'">551136606400</td>
                    <td style="" title="551133855635" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91295'">551133855635</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91295'">Atendida</td>
                    <td style="" title="1131000441LifeSP5648" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91295'">1131000441LifeSP5648</td>
                    <td style="" title="Entrante" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91295'">Entrante</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91295'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_37" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_37" value="Mzc."
                                                      onclick="toggle_checkbox('37', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91293'">10/07 15:08</td>
                    <td style="" title="00:00:07" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91293'">00:00:07</td>
                                        <td style="" title="551136606400" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91293'">551136606400</td>
                    <td style="" title="551133855635" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91293'">551133855635</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91293'">Atendida</td>
                    <td style="" title="1131000441LifeSP5648" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91293'">1131000441LifeSP5648</td>
                    <td style="" title="Entrante" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91293'">Entrante</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91293'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_38" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_38" value="Mzg."
                                                      onclick="toggle_checkbox('38', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91294'">10/07 15:07</td>
                    <td style="" title="00:01:45" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91294'">00:01:45</td>
                                        <td style="" title="Ramal: Ramal 2804" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91294'">2804</td>
                    <td style="" title="Ramal: ramal 1603 (1603)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91294'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1562783368" title="Ramal: ramal 1603 (1603)" align="absmiddle" style="cursor: pointer;"> 1603</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91294'">Atendida</td>
                    <td style="" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91294'"></td>
                    <td style="" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91294'">Interno</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91294'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907101507452804160315627820642116531562782065wav5d262e88bb11b');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783368" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907101507452804160315627820642116531562782065wav5d262e88bb11b divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907101507452804160315627820642116531562782065wav5d262e88bb11b">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-150745-2804-1603-1562782064.211653-1562782065.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-150745-2804-1603-1562782064.211653-1562782065.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907101507452804160315627820642116531562782065wav5d262e88bb11b" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-150745-2804-1603-1562782064.211653-1562782065.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783368" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-150745-2804-1603-1562782064.211653-1562782065.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783368" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_39" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_39" value="Mzk."
                                                      onclick="toggle_checkbox('39', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91299'">10/07 15:07</td>
                    <td style="" title="00:03:37" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91299'">00:03:37</td>
                                        <td style="" title="551126638810" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91299'">551126638810</td>
                    <td style="" title="Grupo: GP - Lifetime - 5656 » Ramal: ramal 2202 (2202)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91299'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_group.gif?1562783368" title="Grupo: GP - Lifetime - 5656" align="absmiddle" style="cursor: pointer;">  <img src="/pbxip/themes/phone2b/images/bullet_go_cf.gif?1562783368" title="Encaminhado" align="absmiddle">  <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1562783368" title="Ramal: ramal 2202 (2202)" align="absmiddle" style="cursor: pointer;"> 2202</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91299'">Atendida</td>
                    <td style="" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91299'"></td>
                    <td style="" title="Entrante" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91299'">Entrante</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91299'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_20190710150741551126638810220215627820322116481562782061wav5d262e88bd05a');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783368" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_20190710150741551126638810220215627820322116481562782061wav5d262e88bd05a divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_20190710150741551126638810220215627820322116481562782061wav5d262e88bd05a">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-150741-551126638810-2202-1562782032.211648-1562782061.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-150741-551126638810-2202-1562782032.211648-1562782061.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_20190710150741551126638810220215627820322116481562782061wav5d262e88bd05a" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-150741-551126638810-2202-1562782032.211648-1562782061.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783368" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-150741-551126638810-2202-1562782032.211648-1562782061.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783368" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_40" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_40" value="NDA."
                                                      onclick="toggle_checkbox('40', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91298'">10/07 15:07</td>
                    <td style="" title="00:04:02" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91298'">00:04:02</td>
                                        <td style="" title="551126638810" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91298'">551126638810</td>
                    <td style="" title="Grupo: GP - Lifetime - 5656 » Ramal: Ramal 2810 (2810)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91298'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_group.gif?1562783368" title="Grupo: GP - Lifetime - 5656" align="absmiddle" style="cursor: pointer;">  <img src="/pbxip/themes/phone2b/images/bullet_go_cf.gif?1562783368" title="Encaminhado" align="absmiddle"> 2810</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91298'">Atendida</td>
                    <td style="" title="1131000441LifeSP5648" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91298'">1131000441LifeSP5648</td>
                    <td style="" title="Entrante" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91298'">Entrante</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91298'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_2019071015627820312116461562782032wav5d262e88bef9b');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783368" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_2019071015627820312116461562782032wav5d262e88bef9b divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_2019071015627820312116461562782032wav5d262e88bef9b">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-1562782031.211646-1562782032.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-1562782031.211646-1562782032.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_2019071015627820312116461562782032wav5d262e88bef9b" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-1562782031.211646-1562782032.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783368" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-1562782031.211646-1562782032.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783368" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_41" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_41" value="NDE."
                                                      onclick="toggle_checkbox('41', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #cc6600;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91292'">10/07 15:07</td>
                    <td style="color: #cc6600;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91292'">00:00:00</td>
                                        <td style="color: #cc6600;" title="Ramal: ramal 1410" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91292'">1410</td>
                    <td style="color: #cc6600;" title="Ramal: Ramal 2807 (2807)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91292'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1562783368" title="Ramal: Ramal 2807 (2807)" align="absmiddle" style="cursor: pointer;"> 2807</td>
                    <td style="color: #cc6600;" title="Não Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91292'">Não Atendida</td>
                    <td style="color: #cc6600;" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91292'"></td>
                    <td style="color: #cc6600;" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91292'">Interno</td>
                    <td style="color: #cc6600;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91292'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_42" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_42" value="NDI."
                                                      onclick="toggle_checkbox('42', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91290'">10/07 15:05</td>
                    <td style="" title="00:00:23" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91290'">00:00:23</td>
                                        <td style="" title="Ramal: ramal 2601" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91290'">2601</td>
                    <td style="" title="5513974198393" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91290'">5513974198393</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91290'">Atendida</td>
                    <td style="" title="1131000441LifeSP5653" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91290'">1131000441LifeSP5653</td>
                    <td style="" title="Celular Nacional" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91290'">Celular Nacional</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91290'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907101505442601551397419839315627819442116391562781944wav5d262e88c264e');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783368" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907101505442601551397419839315627819442116391562781944wav5d262e88c264e divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907101505442601551397419839315627819442116391562781944wav5d262e88c264e">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-150544-2601-5513974198393-1562781944.211639-1562781944.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-150544-2601-5513974198393-1562781944.211639-1562781944.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907101505442601551397419839315627819442116391562781944wav5d262e88c264e" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-150544-2601-5513974198393-1562781944.211639-1562781944.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783368" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-150544-2601-5513974198393-1562781944.211639-1562781944.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783368" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_43" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_43" value="NDM."
                                                      onclick="toggle_checkbox('43', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91289'">10/07 15:05</td>
                    <td style="" title="00:00:37" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91289'">00:00:37</td>
                                        <td style="" title="Ramal: ramal 2607" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91289'">2607</td>
                    <td style="" title="551150547686" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91289'">551150547686</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91289'">Atendida</td>
                    <td style="" title="1131000441LifeSP5655" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91289'">1131000441LifeSP5655</td>
                    <td style="" title="Fixo Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91289'">Fixo Local</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91289'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_2019071015052226075054768615627819222116351562781922wav5d262e88c41a3');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783368" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_2019071015052226075054768615627819222116351562781922wav5d262e88c41a3 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_2019071015052226075054768615627819222116351562781922wav5d262e88c41a3">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-150522-2607-50547686-1562781922.211635-1562781922.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-150522-2607-50547686-1562781922.211635-1562781922.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_2019071015052226075054768615627819222116351562781922wav5d262e88c41a3" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-150522-2607-50547686-1562781922.211635-1562781922.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783368" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-150522-2607-50547686-1562781922.211635-1562781922.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783368" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_44" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_44" value="NDQ."
                                                      onclick="toggle_checkbox('44', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91291'">10/07 15:04</td>
                    <td style="" title="00:02:19" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91291'">00:02:19</td>
                                        <td style="" title="Ramal: ramal 1410" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91291'">1410</td>
                    <td style="" title="Ramal: Ramal 2804 (2804)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91291'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1562783368" title="Ramal: Ramal 2804 (2804)" align="absmiddle" style="cursor: pointer;"> 2804</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91291'">Atendida</td>
                    <td style="" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91291'"></td>
                    <td style="" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91291'">Interno</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91291'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907101504441410280415627818832116321562781884wav5d262e88c60e5');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783368" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907101504441410280415627818832116321562781884wav5d262e88c60e5 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907101504441410280415627818832116321562781884wav5d262e88c60e5">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-150444-1410-2804-1562781883.211632-1562781884.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-150444-1410-2804-1562781883.211632-1562781884.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907101504441410280415627818832116321562781884wav5d262e88c60e5" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-150444-1410-2804-1562781883.211632-1562781884.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783368" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-150444-1410-2804-1562781883.211632-1562781884.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783368" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_45" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_45" value="NDU."
                                                      onclick="toggle_checkbox('45', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #cc6600;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91288'">10/07 15:04</td>
                    <td style="color: #cc6600;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91288'">00:00:00</td>
                                        <td style="color: #cc6600;" title="Ramal: Ramal 9005" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91288'">9005</td>
                    <td style="color: #cc6600;" title="5511995047230" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91288'">5511995047230</td>
                    <td style="color: #cc6600;" title="Não Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91288'">Não Atendida</td>
                    <td style="color: #cc6600;" title="1131000441LifeSP5656" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91288'">1131000441LifeSP5656</td>
                    <td style="color: #cc6600;" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91288'">Celular Local</td>
                    <td style="color: #cc6600;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91288'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_46" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_46" value="NDY."
                                                      onclick="toggle_checkbox('46', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #cc6600;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91287'">10/07 15:04</td>
                    <td style="color: #cc6600;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91287'">00:00:00</td>
                                        <td style="color: #cc6600;" title="Ramal: Ramal 9005" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91287'">9005</td>
                    <td style="color: #cc6600;" title="5511982735815" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91287'">5511982735815</td>
                    <td style="color: #cc6600;" title="Não Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91287'">Não Atendida</td>
                    <td style="color: #cc6600;" title="1131000441LifeSP5656" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91287'">1131000441LifeSP5656</td>
                    <td style="color: #cc6600;" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91287'">Celular Local</td>
                    <td style="color: #cc6600;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91287'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_47" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_47" value="NDc."
                                                      onclick="toggle_checkbox('47', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91313'">10/07 15:02</td>
                    <td style="" title="00:20:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91313'">00:20:00</td>
                                        <td style="" title="Ramal: ramal 1416" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91313'">1416</td>
                    <td style="" title="5511994848490" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91313'">5511994848490</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91313'">Atendida</td>
                    <td style="" title="1131000441LifeSP5648" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91313'">1131000441LifeSP5648</td>
                    <td style="" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91313'">Celular Local</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91313'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_20190710150230141699484849015627817492116191562781750wav5d262e88ca737');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783368" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_20190710150230141699484849015627817492116191562781750wav5d262e88ca737 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_20190710150230141699484849015627817492116191562781750wav5d262e88ca737">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-150230-1416-994848490-1562781749.211619-1562781750.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-150230-1416-994848490-1562781749.211619-1562781750.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_20190710150230141699484849015627817492116191562781750wav5d262e88ca737" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-150230-1416-994848490-1562781749.211619-1562781750.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783368" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-150230-1416-994848490-1562781749.211619-1562781750.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783368" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_48" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_48" value="NDg."
                                                      onclick="toggle_checkbox('48', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91286'">10/07 14:59</td>
                    <td style="" title="00:04:18" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91286'">00:04:18</td>
                                        <td style="" title="Ramal: Ramal 9005" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91286'">9005</td>
                    <td style="" title="Ramal: ramal 1405 (1405) » Ramal: ramal 1404 (1404)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91286'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1562783368" title="Ramal: ramal 1405 (1405)" align="absmiddle" style="cursor: pointer;">  <img src="/pbxip/themes/phone2b/images/bullet_go_cf.gif?1562783368" title="Encaminhado" align="absmiddle"> 1404</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91286'">Atendida</td>
                    <td style="" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91286'"></td>
                    <td style="" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91286'">Interno</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91286'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907101458469005140515627815262116031562781526wav5d262e88cd233');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783368" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907101458469005140515627815262116031562781526wav5d262e88cd233 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907101458469005140515627815262116031562781526wav5d262e88cd233">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-145846-9005-1405-1562781526.211603-1562781526.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-145846-9005-1405-1562781526.211603-1562781526.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907101458469005140515627815262116031562781526wav5d262e88cd233" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-145846-9005-1405-1562781526.211603-1562781526.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783368" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-145846-9005-1405-1562781526.211603-1562781526.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783368" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_49" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_49" value="NDk."
                                                      onclick="toggle_checkbox('49', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91285'">10/07 14:59</td>
                    <td style="" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91285'">00:00:00</td>
                                        <td style="" title="Ramal: ramal 1410" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91285'">1410</td>
                    <td style="" title="Ramal: ramal 1404 (1404) » Ramal: ramal 1405 (1405)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91285'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1562783368" title="Ramal: ramal 1404 (1404)" align="absmiddle" style="cursor: pointer;">  <img src="/pbxip/themes/phone2b/images/bullet_go_cf.gif?1562783368" title="Encaminhado" align="absmiddle"> 1405</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91285'">Atendida</td>
                    <td style="" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91285'"></td>
                    <td style="" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91285'">Interno</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91285'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907101459111410140415627815512116151562781551wav5d262e88cfd28');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783368" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907101459111410140415627815512116151562781551wav5d262e88cfd28 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907101459111410140415627815512116151562781551wav5d262e88cfd28">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-145911-1410-1404-1562781551.211615-1562781551.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-145911-1410-1404-1562781551.211615-1562781551.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907101459111410140415627815512116151562781551wav5d262e88cfd28" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-145911-1410-1404-1562781551.211615-1562781551.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783368" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-145911-1410-1404-1562781551.211615-1562781551.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783368" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_50" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_50" value="NTA."
                                                      onclick="toggle_checkbox('50', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91283'">10/07 14:58</td>
                    <td style="" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91283'">00:00:00</td>
                                        <td style="" title="Ramal: Ramal 9005" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91283'">9005</td>
                    <td style="" title="Ramal: ramal 1404 (1404) » Ramal: ramal 1410 (1410)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91283'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1562783368" title="Ramal: ramal 1404 (1404)" align="absmiddle" style="cursor: pointer;">  <img src="/pbxip/themes/phone2b/images/bullet_go_cf.gif?1562783368" title="Encaminhado" align="absmiddle"> 1410</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91283'">Atendida</td>
                    <td style="" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91283'"></td>
                    <td style="" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91283'">Interno</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91283'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907101458479005140415627815262116071562781527wav5d262e88d281f');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783368" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907101458479005140415627815262116071562781527wav5d262e88d281f divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907101458479005140415627815262116071562781527wav5d262e88d281f">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-145847-9005-1404-1562781526.211607-1562781527.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-145847-9005-1404-1562781526.211607-1562781527.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907101458479005140415627815262116071562781527wav5d262e88d281f" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-145847-9005-1404-1562781526.211607-1562781527.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783368" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-145847-9005-1404-1562781526.211607-1562781527.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783368" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_51" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_51" value="NTE."
                                                      onclick="toggle_checkbox('51', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91284'">10/07 14:58</td>
                    <td style="" title="00:04:18" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91284'">00:04:18</td>
                                        <td style="" title="Ramal: Ramal 9005" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91284'">9005</td>
                    <td style="" title="Ramal: ramal 1405 (1405) » Ramal: ramal 1404 (1404)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91284'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1562783368" title="Ramal: ramal 1405 (1405)" align="absmiddle" style="cursor: pointer;">  <img src="/pbxip/themes/phone2b/images/bullet_go_cf.gif?1562783368" title="Encaminhado" align="absmiddle"> 1404</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91284'">Atendida</td>
                    <td style="" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91284'"></td>
                    <td style="" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91284'">Interno</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91284'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907101458469005140515627815262116031562781526wav5d262e88d5318');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783368" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907101458469005140515627815262116031562781526wav5d262e88d5318 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907101458469005140515627815262116031562781526wav5d262e88d5318">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-145846-9005-1405-1562781526.211603-1562781526.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-145846-9005-1405-1562781526.211603-1562781526.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907101458469005140515627815262116031562781526wav5d262e88d5318" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-145846-9005-1405-1562781526.211603-1562781526.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783368" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-145846-9005-1405-1562781526.211603-1562781526.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783368" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_52" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_52" value="NTI."
                                                      onclick="toggle_checkbox('52', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91282'">10/07 14:57</td>
                    <td style="" title="00:00:01" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91282'">00:00:01</td>
                                        <td style="" title="Ramal: Ramal 9005" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91282'">9005</td>
                    <td style="" title="Ramal: ramal 1404 (1404) » Ramal: ramal 1405 (1405)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91282'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1562783368" title="Ramal: ramal 1404 (1404)" align="absmiddle" style="cursor: pointer;">  <img src="/pbxip/themes/phone2b/images/bullet_go_cf.gif?1562783368" title="Encaminhado" align="absmiddle"> 1405</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91282'">Atendida</td>
                    <td style="" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91282'"></td>
                    <td style="" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91282'">Interno</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91282'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907101457589005140415627814772115961562781478wav5d262e88d7e11');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783368" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907101457589005140415627814772115961562781478wav5d262e88d7e11 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907101457589005140415627814772115961562781478wav5d262e88d7e11">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-145758-9005-1404-1562781477.211596-1562781478.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-145758-9005-1404-1562781477.211596-1562781478.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907101457589005140415627814772115961562781478wav5d262e88d7e11" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-145758-9005-1404-1562781477.211596-1562781478.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783368" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-145758-9005-1404-1562781477.211596-1562781478.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783368" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_53" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_53" value="NTM."
                                                      onclick="toggle_checkbox('53', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91281'">10/07 14:57</td>
                    <td style="" title="00:00:34" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91281'">00:00:34</td>
                                        <td style="" title="Ramal: Ramal 9005" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91281'">9005</td>
                    <td style="" title="Ramal: ramal 1405 (1405) » Ramal: ramal 1404 (1404)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91281'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1562783368" title="Ramal: ramal 1405 (1405)" align="absmiddle" style="cursor: pointer;">  <img src="/pbxip/themes/phone2b/images/bullet_go_cf.gif?1562783368" title="Encaminhado" align="absmiddle"> 1404</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91281'">Atendida</td>
                    <td style="" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91281'"></td>
                    <td style="" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91281'">Interno</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91281'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907101457579005140515627814772115921562781477wav5d262e88da909');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783368" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907101457579005140515627814772115921562781477wav5d262e88da909 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907101457579005140515627814772115921562781477wav5d262e88da909">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-145757-9005-1405-1562781477.211592-1562781477.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-145757-9005-1405-1562781477.211592-1562781477.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907101457579005140515627814772115921562781477wav5d262e88da909" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-145757-9005-1405-1562781477.211592-1562781477.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783368" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-145757-9005-1405-1562781477.211592-1562781477.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783368" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_54" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_54" value="NTQ."
                                                      onclick="toggle_checkbox('54', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91280'">10/07 14:54</td>
                    <td style="" title="00:00:03" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91280'">00:00:03</td>
                                        <td style="" title="Ramal: ramal 1416" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91280'">1416</td>
                    <td style="" title="5511994848490" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91280'">5511994848490</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91280'">Atendida</td>
                    <td style="" title="1131000441LifeSP5648" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91280'">1131000441LifeSP5648</td>
                    <td style="" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91280'">Celular Local</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91280'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_20190710145451141699484849015627812902115881562781291wav5d262e88dc463');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783368" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_20190710145451141699484849015627812902115881562781291wav5d262e88dc463 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_20190710145451141699484849015627812902115881562781291wav5d262e88dc463">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-145451-1416-994848490-1562781290.211588-1562781291.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-145451-1416-994848490-1562781290.211588-1562781291.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_20190710145451141699484849015627812902115881562781291wav5d262e88dc463" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-145451-1416-994848490-1562781290.211588-1562781291.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783368" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-145451-1416-994848490-1562781290.211588-1562781291.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783368" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_55" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_55" value="NTU."
                                                      onclick="toggle_checkbox('55', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91279'">10/07 14:53</td>
                    <td style="" title="00:01:43" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91279'">00:01:43</td>
                                        <td style="" title="Ramal: ramal 1410" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91279'">1410</td>
                    <td style="" title="5511989890407" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91279'">5511989890407</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91279'">Atendida</td>
                    <td style="" title="1131000441LifeSP5640" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91279'">1131000441LifeSP5640</td>
                    <td style="" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91279'">Celular Local</td>
                    <td style="" title="" nowrap align="right"
                       ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91279'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_20190710145354141098989040715627812332115841562781234wav5d262e88ddfbf');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783368" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_20190710145354141098989040715627812332115841562781234wav5d262e88ddfbf divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_20190710145354141098989040715627812332115841562781234wav5d262e88ddfbf">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-145354-1410-989890407-1562781233.211584-1562781234.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-145354-1410-989890407-1562781233.211584-1562781234.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_20190710145354141098989040715627812332115841562781234wav5d262e88ddfbf" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-145354-1410-989890407-1562781233.211584-1562781234.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783368" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-145354-1410-989890407-1562781233.211584-1562781234.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783368" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_56" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_56" value="NTY."
                                                      onclick="toggle_checkbox('56', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91278'">10/07 14:52</td>
                    <td style="" title="00:00:03" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91278'">00:00:03</td>
                                        <td style="" title="Ramal: ramal 1416" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91278'">1416</td>
                    <td style="" title="5511997872895" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91278'">5511997872895</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91278'">Atendida</td>
                    <td style="" title="1131000441LifeSP5648" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91278'">1131000441LifeSP5648</td>
                    <td style="" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91278'">Celular Local</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91278'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_20190710145240141699787289515627811602115791562781160wav5d262e88dfb13');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783368" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_20190710145240141699787289515627811602115791562781160wav5d262e88dfb13 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_20190710145240141699787289515627811602115791562781160wav5d262e88dfb13">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-145240-1416-997872895-1562781160.211579-1562781160.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-145240-1416-997872895-1562781160.211579-1562781160.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_20190710145240141699787289515627811602115791562781160wav5d262e88dfb13" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-145240-1416-997872895-1562781160.211579-1562781160.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783368" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-145240-1416-997872895-1562781160.211579-1562781160.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783368" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_57" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_57" value="NTc."
                                                      onclick="toggle_checkbox('57', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91277'">10/07 14:52</td>
                    <td style="" title="00:00:06" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91277'">00:00:06</td>
                                        <td style="" title="Ramal: ramal 2604" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91277'">2604</td>
                    <td style="" title="Ramal: Ramal 2208 (2208) » Ramal: ramal 2203 (2203)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91277'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1562783368" title="Ramal: Ramal 2208 (2208)" align="absmiddle" style="cursor: pointer;">  <img src="/pbxip/themes/phone2b/images/bullet_go_cf.gif?1562783368" title="Encaminhado" align="absmiddle"> 2203</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91277'">Atendida</td>
                    <td style="" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91277'"></td>
                    <td style="" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91277'">Interno</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91277'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907101452372604220815627811572115761562781157wav5d262e88e260c');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783368" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907101452372604220815627811572115761562781157wav5d262e88e260c divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907101452372604220815627811572115761562781157wav5d262e88e260c">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-145237-2604-2208-1562781157.211576-1562781157.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-145237-2604-2208-1562781157.211576-1562781157.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907101452372604220815627811572115761562781157wav5d262e88e260c" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-145237-2604-2208-1562781157.211576-1562781157.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783368" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-145237-2604-2208-1562781157.211576-1562781157.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783368" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_58" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_58" value="NTg."
                                                      onclick="toggle_checkbox('58', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #990000;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91276'">10/07 14:52</td>
                    <td style="color: #990000;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91276'">00:00:00</td>
                                        <td style="color: #990000;" title="Ramal: ramal 1405" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91276'">1405</td>
                    <td style="color: #990000;" title="Ramal: Ramal 2812 (2812)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91276'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1562783368" title="Ramal: Ramal 2812 (2812)" align="absmiddle" style="cursor: pointer;"> 2812</td>
                    <td style="color: #990000;" title="Falhou" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91276'">Falhou</td>
                    <td style="color: #990000;" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91276'"></td>
                    <td style="color: #990000;" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91276'">Interno</td>
                    <td style="color: #990000;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91276'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_59" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_59" value="NTk."
                                                      onclick="toggle_checkbox('59', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91275'">10/07 14:50</td>
                    <td style="" title="00:00:02" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91275'">00:00:02</td>
                                        <td style="" title="Ramal: ramal 1416" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91275'">1416</td>
                    <td style="" title="5511995685656" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91275'">5511995685656</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91275'">Atendida</td>
                    <td style="" title="1131000441LifeSP5648" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91275'">1131000441LifeSP5648</td>
                    <td style="" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91275'">Celular Local</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91275'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_20190710145021141699568565615627810212115681562781021wav5d262e88e5cbe');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783368" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_20190710145021141699568565615627810212115681562781021wav5d262e88e5cbe divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_20190710145021141699568565615627810212115681562781021wav5d262e88e5cbe">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-145021-1416-995685656-1562781021.211568-1562781021.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-145021-1416-995685656-1562781021.211568-1562781021.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_20190710145021141699568565615627810212115681562781021wav5d262e88e5cbe" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-145021-1416-995685656-1562781021.211568-1562781021.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783368" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-145021-1416-995685656-1562781021.211568-1562781021.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783368" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_60" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_60" value="NjA."
                                                      onclick="toggle_checkbox('60', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91274'">10/07 14:48</td>
                    <td style="" title="00:00:06" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91274'">00:00:06</td>
                                        <td style="" title="Ramal: ramal 1416" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91274'">1416</td>
                    <td style="" title="5511997649595" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91274'">5511997649595</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91274'">Atendida</td>
                    <td style="" title="1131000441LifeSP5648" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91274'">1131000441LifeSP5648</td>
                    <td style="" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91274'">Celular Local</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91274'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_20190710144808141699764959515627808882115641562780888wav5d262e88e781b');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783368" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_20190710144808141699764959515627808882115641562780888wav5d262e88e781b divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_20190710144808141699764959515627808882115641562780888wav5d262e88e781b">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-144808-1416-997649595-1562780888.211564-1562780888.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-144808-1416-997649595-1562780888.211564-1562780888.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_20190710144808141699764959515627808882115641562780888wav5d262e88e781b" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-144808-1416-997649595-1562780888.211564-1562780888.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783368" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-144808-1416-997649595-1562780888.211564-1562780888.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783368" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_61" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_61" value="NjE."
                                                      onclick="toggle_checkbox('61', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91273'">10/07 14:47</td>
                    <td style="" title="00:00:04" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91273'">00:00:04</td>
                                        <td style="" title="Ramal: ramal 1416" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91273'">1416</td>
                    <td style="" title="5511997649595" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91273'">5511997649595</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91273'">Atendida</td>
                    <td style="" title="1131000441LifeSP5648" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91273'">1131000441LifeSP5648</td>
                    <td style="" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91273'">Celular Local</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91273'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_20190710144745141699764959515627808652115601562780865wav5d262e88e9374');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783368" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_20190710144745141699764959515627808652115601562780865wav5d262e88e9374 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_20190710144745141699764959515627808652115601562780865wav5d262e88e9374">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-144745-1416-997649595-1562780865.211560-1562780865.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-144745-1416-997649595-1562780865.211560-1562780865.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_20190710144745141699764959515627808652115601562780865wav5d262e88e9374" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-144745-1416-997649595-1562780865.211560-1562780865.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783368" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-144745-1416-997649595-1562780865.211560-1562780865.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783368" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_62" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_62" value="NjI."
                                                      onclick="toggle_checkbox('62', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #990000;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91272'">10/07 14:46</td>
                    <td style="color: #990000;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91272'">00:00:00</td>
                                        <td style="color: #990000;" title="Ramal: Ramal 9005" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91272'">9005</td>
                    <td style="color: #990000;" title="5511996122063" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91272'">5511996122063</td>
                    <td style="color: #990000;" title="Falhou" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91272'">Falhou</td>
                    <td style="color: #990000;" title="1131000441LifeSP5656" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91272'">1131000441LifeSP5656</td>
                    <td style="color: #990000;" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91272'">Celular Local</td>
                    <td style="color: #990000;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91272'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_63" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_63" value="NjM."
                                                      onclick="toggle_checkbox('63', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91271'">10/07 14:46</td>
                    <td style="" title="00:00:35" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91271'">00:00:35</td>
                                        <td style="" title="551132595920" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91271'">551132595920</td>
                    <td style="" title="Ramal: Ramal 1406 (1406) » Ramal: ramal 1415 (1415)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91271'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1562783368" title="Ramal: Ramal 1406 (1406)" align="absmiddle" style="cursor: pointer;">  <img src="/pbxip/themes/phone2b/images/bullet_go_cf.gif?1562783368" title="Encaminhado" align="absmiddle"> 1415</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91271'">Atendida</td>
                    <td style="" title="1131000441LifeSP5648" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91271'">1131000441LifeSP5648</td>
                    <td style="" title="Entrante" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91271'">Entrante</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91271'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_20190710144634551132595920140615627807932115521562780794wav5d262e88ed1ef');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783368" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_20190710144634551132595920140615627807932115521562780794wav5d262e88ed1ef divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_20190710144634551132595920140615627807932115521562780794wav5d262e88ed1ef">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-144634-551132595920-1406-1562780793.211552-1562780794.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-144634-551132595920-1406-1562780793.211552-1562780794.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_20190710144634551132595920140615627807932115521562780794wav5d262e88ed1ef" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-144634-551132595920-1406-1562780793.211552-1562780794.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783368" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-144634-551132595920-1406-1562780793.211552-1562780794.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783368" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_64" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_64" value="NjQ."
                                                      onclick="toggle_checkbox('64', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #cc6600;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91270'">10/07 14:45</td>
                    <td style="color: #cc6600;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91270'">00:00:00</td>
                                        <td style="color: #cc6600;" title="Ramal: Ramal 9005" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91270'">9005</td>
                    <td style="color: #cc6600;" title="5511993522212" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91270'">5511993522212</td>
                    <td style="color: #cc6600;" title="Não Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91270'">Não Atendida</td>
                    <td style="color: #cc6600;" title="1131000441LifeSP5656" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91270'">1131000441LifeSP5656</td>
                    <td style="color: #cc6600;" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91270'">Celular Local</td>
                    <td style="color: #cc6600;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91270'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_65" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_65" value="NjU."
                                                      onclick="toggle_checkbox('65', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #990000;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91269'">10/07 14:44</td>
                    <td style="color: #990000;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91269'">00:00:00</td>
                                        <td style="color: #990000;" title="Ramal: Ramal 9005" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91269'">9005</td>
                    <td style="color: #990000;" title="5511956102820" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91269'">5511956102820</td>
                    <td style="color: #990000;" title="Falhou" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91269'">Falhou</td>
                    <td style="color: #990000;" title="1131000441LifeSP5656" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91269'">1131000441LifeSP5656</td>
                    <td style="color: #990000;" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91269'">Celular Local</td>
                    <td style="color: #990000;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91269'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_66" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_66" value="NjY."
                                                      onclick="toggle_checkbox('66', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91268'">10/07 14:29</td>
                    <td style="" title="00:00:03" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91268'">00:00:03</td>
                                        <td style="" title="551421079650" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91268'">551421079650</td>
                    <td style="" title="Grupo: GP - Lifetime CG - 7480 » Ramal: Ramal 7003 (7003)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91268'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_group.gif?1562783368" title="Grupo: GP - Lifetime CG - 7480" align="absmiddle" style="cursor: pointer;">  <img src="/pbxip/themes/phone2b/images/bullet_go_cf.gif?1562783368" title="Encaminhado" align="absmiddle"> 7003</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91268'">Atendida</td>
                    <td style="" title="1131000441LifeSP5648" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91268'">1131000441LifeSP5648</td>
                    <td style="" title="Entrante" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91268'">Entrante</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91268'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_2019071015627797802115351562779781wav5d262e88f1c80');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783368" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_2019071015627797802115351562779781wav5d262e88f1c80 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_2019071015627797802115351562779781wav5d262e88f1c80">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-1562779780.211535-1562779781.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-1562779780.211535-1562779781.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_2019071015627797802115351562779781wav5d262e88f1c80" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-1562779780.211535-1562779781.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783368" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-1562779780.211535-1562779781.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783368" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_67" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_67" value="Njc."
                                                      onclick="toggle_checkbox('67', 'fifochkid', 'text', tdis.id);"/>
                   </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91267'">10/07 14:24</td>
                    <td style="" title="00:00:50" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91267'">00:00:50</td>
                                        <td style="" title="Ramal: ramal 2604" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91267'">2604</td>
                    <td style="" title="5511975525365" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91267'">5511975525365</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91267'">Atendida</td>
                    <td style="" title="1131000441LifeSP5651" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91267'">1131000441LifeSP5651</td>
                    <td style="" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91267'">Celular Local</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91267'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783368" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_20190710142402260497552536515627794412115311562779442wav5d262e88f377f');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783368" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_20190710142402260497552536515627794412115311562779442wav5d262e88f377f divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_20190710142402260497552536515627794412115311562779442wav5d262e88f377f">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-142402-2604-975525365-1562779441.211531-1562779442.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-142402-2604-975525365-1562779441.211531-1562779442.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_20190710142402260497552536515627794412115311562779442wav5d262e88f377f" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-142402-2604-975525365-1562779441.211531-1562779442.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783368" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-142402-2604-975525365-1562779441.211531-1562779442.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783368" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_68" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_68" value="Njg."
                                                      onclick="toggle_checkbox('68', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91266'">10/07 14:18</td>
                    <td style="" title="00:00:56" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91266'">00:00:56</td>
                                        <td style="" title="Ramal: ramal 2604" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91266'">2604</td>
                    <td style="" title="5511983819986" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91266'">5511983819986</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91266'">Atendida</td>
                    <td style="" title="1131000441LifeSP5651" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91266'">1131000441LifeSP5651</td>
                    <td style="" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91266'">Celular Local</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91266'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783369" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_20190710141900260498381998615627791392115261562779140wav5d262e8901094');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783369" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_20190710141900260498381998615627791392115261562779140wav5d262e8901094 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_20190710141900260498381998615627791392115261562779140wav5d262e8901094">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-141900-2604-983819986-1562779139.211526-1562779140.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-141900-2604-983819986-1562779139.211526-1562779140.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_20190710141900260498381998615627791392115261562779140wav5d262e8901094" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-141900-2604-983819986-1562779139.211526-1562779140.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783369" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-141900-2604-983819986-1562779139.211526-1562779140.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783369" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_69" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_69" value="Njk."
                                                      onclick="toggle_checkbox('69', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91265'">10/07 14:18</td>
                    <td style="" title="00:00:04" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91265'">00:00:04</td>
                                        <td style="" title="Ramal: ramal 2604" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91265'">2604</td>
                    <td style="" title="5511986819986" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91265'">5511986819986</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91265'">Atendida</td>
                    <td style="" title="1131000441LifeSP5651" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91265'">1131000441LifeSP5651</td>
                    <td style="" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91265'">Celular Local</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91265'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783369" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_20190710141816260498681998615627790952115211562779096wav5d262e8902bed');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783369" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_20190710141816260498681998615627790952115211562779096wav5d262e8902bed divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_20190710141816260498681998615627790952115211562779096wav5d262e8902bed">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-141816-2604-986819986-1562779095.211521-1562779096.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-141816-2604-986819986-1562779095.211521-1562779096.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_20190710141816260498681998615627790952115211562779096wav5d262e8902bed" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-141816-2604-986819986-1562779095.211521-1562779096.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783369" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-141816-2604-986819986-1562779095.211521-1562779096.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783369" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_70" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_70" value="NzA."
                                                      onclick="toggle_checkbox('70', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #cc6600;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91264'">10/07 14:11</td>
                    <td style="color: #cc6600;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91264'">00:00:00</td>
                                        <td style="color: #cc6600;" title="Ramal: Ramal 9003" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91264'">9003</td>
                    <td style="color: #cc6600;" title="551937558660" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91264'">551937558660</td>
                    <td style="color: #cc6600;" title="Não Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91264'">Não Atendida</td>
                    <td style="color: #cc6600;" title="1131000441LifeSP5656" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91264'">1131000441LifeSP5656</td>
                    <td style="color: #cc6600;" title="Fixo Nacional" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91264'">Fixo Nacional</td>
                    <td style="color: #cc6600;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91264'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783369" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_71" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_71" value="NzE."
                                                      onclick="toggle_checkbox('71', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #cc6600;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91263'">10/07 14:11</td>
                    <td style="color: #cc6600;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91263'">00:00:00</td>
                                        <td style="color: #cc6600;" title="Ramal: Ramal 9003" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91263'">9003</td>
                    <td style="color: #cc6600;" title="551937558660" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91263'">551937558660</td>
                    <td style="color: #cc6600;" title="Não Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91263'">Não Atendida</td>
                    <td style="color: #cc6600;" title="1131000441LifeSP5656" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91263'">1131000441LifeSP5656</td>
                    <td style="color: #cc6600;" title="Fixo Nacional" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91263'">Fixo Nacional</td>
                    <td style="color: #cc6600;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91263'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783369" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_72" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_72" value="NzI."
                                                      onclick="toggle_checkbox('72', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91262'">10/07 14:07</td>
                    <td style="" title="00:01:52" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91262'">00:01:52</td>
                                        <td style="" title="5511975525365" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91262'">5511975525365</td>
                    <td style="" title="Ramal: ramal 2604 (2604)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91262'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1562783369" title="Ramal: ramal 2604 (2604)" align="absmiddle" style="cursor: pointer;"> 2604</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91262'">Atendida</td>
                    <td style="" title="1131000441LifeSP5648" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91262'">1131000441LifeSP5648</td>
                    <td style="" title="Entrante" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91262'">Entrante</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91262'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783369" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907101407235511975525365260415627784422115101562778443wav5d262e8907643');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783369" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907101407235511975525365260415627784422115101562778443wav5d262e8907643 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907101407235511975525365260415627784422115101562778443wav5d262e8907643">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-140723-5511975525365-2604-1562778442.211510-1562778443.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-140723-5511975525365-2604-1562778442.211510-1562778443.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907101407235511975525365260415627784422115101562778443wav5d262e8907643" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-140723-5511975525365-2604-1562778442.211510-1562778443.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783369" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-140723-5511975525365-2604-1562778442.211510-1562778443.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783369" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_73" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_73" value="NzM."
                                                      onclick="toggle_checkbox('73', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91261'">10/07 14:02</td>
                    <td style="" title="00:00:03" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91261'">00:00:03</td>
                                        <td style="" title="551125400050" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91261'">551125400050</td>
                    <td style="" title="Grupo: GP - Lifetime - 5650 » Ramal: ramal 2202 (2202)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91261'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_group.gif?1562783369" title="Grupo: GP - Lifetime - 5650" align="absmiddle" style="cursor: pointer;">  <img src="/pbxip/themes/phone2b/images/bullet_go_cf.gif?1562783369" title="Encaminhado" align="absmiddle"> 2202</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91261'">Atendida</td>
                    <td style="" title="1131000441LifeSP5648" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91261'">1131000441LifeSP5648</td>
                    <td style="" title="Entrante" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91261'">Entrante</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91261'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783369" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_2019071015627781692115031562778170wav5d262e8909565');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783369" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_2019071015627781692115031562778170wav5d262e8909565 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_2019071015627781692115031562778170wav5d262e8909565">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-1562778169.211503-1562778170.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-1562778169.211503-1562778170.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_2019071015627781692115031562778170wav5d262e8909565" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-1562778169.211503-1562778170.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783369" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-1562778169.211503-1562778170.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783369" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_74" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_74" value="NzQ."
                                                      onclick="toggle_checkbox('74', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91259'">10/07 13:57</td>
                    <td style="" title="00:00:36" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91259'">00:00:36</td>
                                        <td style="" title="Ramal: Ramal 2802" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91259'">2802</td>
                    <td style="" title="Ramal: ramal 1603 (1603)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91259'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1562783369" title="Ramal: ramal 1603 (1603)" align="absmiddle" style="cursor: pointer;"> 1603</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91259'">Atendida</td>
                    <td style="" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91259'"></td>
                    <td style="" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91259'">Interno</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91259'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783369" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907101357142802160315627778332115001562777834wav5d262e890b4a6');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783369" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907101357142802160315627778332115001562777834wav5d262e890b4a6 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907101357142802160315627778332115001562777834wav5d262e890b4a6">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-135714-2802-1603-1562777833.211500-1562777834.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-135714-2802-1603-1562777833.211500-1562777834.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907101357142802160315627778332115001562777834wav5d262e890b4a6" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-135714-2802-1603-1562777833.211500-1562777834.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783369" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-135714-2802-1603-1562777833.211500-1562777834.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783369" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_75" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_75" value="NzU."
                                                      onclick="toggle_checkbox('75', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91258'">10/07 13:53</td>
                    <td style="" title="00:00:30" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91258'">00:00:30</td>
                                        <td style="" title="551127234000" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91258'">551127234000</td>
                    <td style="" title="Grupo: GP - Lifetime - 5656 » Ramal: Ramal 2206 (2206)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91258'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_group.gif?1562783369" title="Grupo: GP - Lifetime - 5656" align="absmiddle" style="cursor: pointer;">  <img src="/pbxip/themes/phone2b/images/bullet_go_cf.gif?1562783369" title="Encaminhado" align="absmiddle">  <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1562783369" title="Ramal: Ramal 2206 (2206)" align="absmiddle" style="cursor: pointer;"> 2206</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91258'">Atendida</td>
                    <td style="" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91258'"></td>
                    <td style="" title="Entrante" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91258'">Entrante</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91258'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783369" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_20190710135358551127234000220615627776072114951562777638wav5d262e890d3e8');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783369" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_20190710135358551127234000220615627776072114951562777638wav5d262e890d3e8 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_20190710135358551127234000220615627776072114951562777638wav5d262e890d3e8">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-135358-551127234000-2206-1562777607.211495-1562777638.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-135358-551127234000-2206-1562777607.211495-1562777638.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_20190710135358551127234000220615627776072114951562777638wav5d262e890d3e8" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-135358-551127234000-2206-1562777607.211495-1562777638.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783369" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-135358-551127234000-2206-1562777607.211495-1562777638.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783369" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_76" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_76" value="NzY."
                                                      onclick="toggle_checkbox('76', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91257'">10/07 13:53</td>
                    <td style="" title="00:00:55" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91257'">00:00:55</td>
                                        <td style="" title="551127234000" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91257'">551127234000</td>
                    <td style="" title="Grupo: GP - Lifetime - 5656 » Ramal: Ramal 2807 (2807)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91257'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_group.gif?1562783369" title="Grupo: GP - Lifetime - 5656" align="absmiddle" style="cursor: pointer;">  <img src="/pbxip/themes/phone2b/images/bullet_go_cf.gif?1562783369" title="Encaminhado" align="absmiddle"> 2807</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91257'">Atendida</td>
                    <td style="" title="1131000441LifeSP5648" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91257'">1131000441LifeSP5648</td>
                    <td style="" title="Entrante" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91257'">Entrante</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91257'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783369" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_2019071015627776042114891562777605wav5d262e890f33b');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783369" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_2019071015627776042114891562777605wav5d262e890f33b divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_2019071015627776042114891562777605wav5d262e890f33b">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-1562777604.211489-1562777605.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-1562777604.211489-1562777605.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_2019071015627776042114891562777605wav5d262e890f33b" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-1562777604.211489-1562777605.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783369" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-1562777604.211489-1562777605.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783369" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_77" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_77" value="Nzc."
                                                      onclick="toggle_checkbox('77', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91256'">10/07 13:51</td>
                    <td style="" title="00:00:49" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91256'">00:00:49</td>
                                        <td style="" title="Ramal: Ramal 2804" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91256'">2804</td>
                    <td style="" title="Ramal: ramal 1410 (1410) » Ramal: ramal 1409 (1409)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91256'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1562783369" title="Ramal: ramal 1410 (1410)" align="absmiddle" style="cursor: pointer;">  <img src="/pbxip/themes/phone2b/images/bullet_go_cf.gif?1562783369" title="Encaminhado" align="absmiddle"> 1409</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91256'">Atendida</td>
                    <td style="" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91256'"></td>
                    <td style="" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91256'">Interno</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91256'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783369" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907101351082804141015627774672114841562777468wav5d262e8911e2a');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783369" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907101351082804141015627774672114841562777468wav5d262e8911e2a divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907101351082804141015627774672114841562777468wav5d262e8911e2a">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-135108-2804-1410-1562777467.211484-1562777468.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-135108-2804-1410-1562777467.211484-1562777468.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907101351082804141015627774672114841562777468wav5d262e8911e2a" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-135108-2804-1410-1562777467.211484-1562777468.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783369" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-135108-2804-1410-1562777467.211484-1562777468.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783369" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_78" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                   <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_78" value="Nzg."
                                                      onclick="toggle_checkbox('78', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91255'">10/07 13:34</td>
                    <td style="" title="00:00:17" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91255'">00:00:17</td>
                                        <td style="" title="Ramal: Ramal 7005" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91255'">7005</td>
                    <td style="" title="551149352777" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91255'">551149352777</td>
                    <td style="" title="Atendida" nowrap
                       ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91255'">Atendida</td>
                    <td style="" title="1131000441_Campo" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91255'">1131000441_Campo</td>
                    <td style="" title="Fixo Nacional" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91255'">Fixo Nacional</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91255'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783369" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_20190710133435700555114935277715627764752114781562776475wav5d262e891397d');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783369" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_20190710133435700555114935277715627764752114781562776475wav5d262e891397d divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_20190710133435700555114935277715627764752114781562776475wav5d262e891397d">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-133435-7005-551149352777-1562776475.211478-1562776475.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-133435-7005-551149352777-1562776475.211478-1562776475.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_20190710133435700555114935277715627764752114781562776475wav5d262e891397d" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-133435-7005-551149352777-1562776475.211478-1562776475.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783369" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-133435-7005-551149352777-1562776475.211478-1562776475.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783369" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_79" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_79" value="Nzk."
                                                      onclick="toggle_checkbox('79', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91260'">10/07 13:34</td>
                    <td style="" title="00:23:34" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91260'">00:23:34</td>
                                        <td style="" title="551132140709" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91260'">551132140709</td>
                    <td style="" title="Grupo: GP - Lifetime - 5640 - Mesa » Ramal: ramal 1404 (1404)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91260'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_group.gif?1562783369" title="Grupo: GP - Lifetime - 5640 - Mesa" align="absmiddle" style="cursor: pointer;">  <img src="/pbxip/themes/phone2b/images/bullet_go_cf.gif?1562783369" title="Encaminhado" align="absmiddle"> 1404</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91260'">Atendida</td>
                    <td style="" title="1131000441LifeSP5648" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91260'">1131000441LifeSP5648</td>
                    <td style="" title="Entrante" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91260'">Entrante</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91260'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783369" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_2019071015627764622114711562776462wav5d262e89158bb');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783369" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_2019071015627764622114711562776462wav5d262e89158bb divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_2019071015627764622114711562776462wav5d262e89158bb">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-1562776462.211471-1562776462.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-1562776462.211471-1562776462.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_2019071015627764622114711562776462wav5d262e89158bb" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-1562776462.211471-1562776462.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783369" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-1562776462.211471-1562776462.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783369" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_80" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_80" value="ODA."
                                                      onclick="toggle_checkbox('80', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91254'">10/07 13:30</td>
                    <td style="" title="00:00:24" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91254'">00:00:24</td>
                                        <td style="" title="Ramal: ramal 1410" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91254'">1410</td>
                    <td style="" title="5511999012015" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91254'">5511999012015</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91254'">Atendida</td>
                    <td style="" title="1131000441LifeSP5640" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91254'">1131000441LifeSP5640</td>
                    <td style="" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91254'">Celular Local</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91254'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783369" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_20190710133018141099901201515627762172114661562776218wav5d262e8917412');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783369" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_20190710133018141099901201515627762172114661562776218wav5d262e8917412 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_20190710133018141099901201515627762172114661562776218wav5d262e8917412">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-133018-1410-999012015-1562776217.211466-1562776218.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-133018-1410-999012015-1562776217.211466-1562776218.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_20190710133018141099901201515627762172114661562776218wav5d262e8917412" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-133018-1410-999012015-1562776217.211466-1562776218.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783369" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-133018-1410-999012015-1562776217.211466-1562776218.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783369" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_81" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_81" value="ODE."
                                                      onclick="toggle_checkbox('81', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91253'">10/07 13:29</td>
                    <td style="" title="00:00:05" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91253'">00:00:05</td>
                                        <td style="" title="551146000916" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91253'">551146000916</td>
                    <td style="" title="Grupo: GP - Lifetime - 5653 » Ramal: ramal 2601 (2601)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91253'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_group.gif?1562783369" title="Grupo: GP - Lifetime - 5653" align="absmiddle" style="cursor: pointer;">  <img src="/pbxip/themes/phone2b/images/bullet_go_cf.gif?1562783369" title="Encaminhado" align="absmiddle"> 2601</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91253'">Atendida</td>
                    <td style="" title="1131000441LifeSP5648" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91253'">1131000441LifeSP5648</td>
                    <td style="" title="Entrante" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91253'">Entrante</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91253'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783369" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_2019071015627761632114611562776164wav5d262e8919360');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783369" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_2019071015627761632114611562776164wav5d262e8919360 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_2019071015627761632114611562776164wav5d262e8919360">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-1562776163.211461-1562776164.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-1562776163.211461-1562776164.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_2019071015627761632114611562776164wav5d262e8919360" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-1562776163.211461-1562776164.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783369" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-1562776163.211461-1562776164.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783369" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_82" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_82" value="ODI."
                                                      onclick="toggle_checkbox('82', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91252'">10/07 13:22</td>
                    <td style="" title="00:04:42" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91252'">00:04:42</td>
                                        <td style="" title="Ramal: Ramal 2815" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91252'">2815</td>
                    <td style="" title="Ramal: ramal 1405 (1405) » Ramal: ramal 1404 (1404)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91252'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1562783369" title="Ramal: ramal 1405 (1405)" align="absmiddle" style="cursor: pointer;">  <img src="/pbxip/themes/phone2b/images/bullet_go_cf.gif?1562783369" title="Encaminhado" align="absmiddle"> 1404</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91252'">Atendida</td>
                    <td style="" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91252'"></td>
                    <td style="" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91252'">Interno</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91252'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783369" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907101321512815140915627757112114501562775711wav5d262e891be53');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783369" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907101321512815140915627757112114501562775711wav5d262e891be53 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907101321512815140915627757112114501562775711wav5d262e891be53">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-132151-2815-1409-1562775711.211450-1562775711.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-132151-2815-1409-1562775711.211450-1562775711.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907101321512815140915627757112114501562775711wav5d262e891be53" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-132151-2815-1409-1562775711.211450-1562775711.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783369" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-132151-2815-1409-1562775711.211450-1562775711.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783369" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_83" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_83" value="ODM."
                                                      onclick="toggle_checkbox('83', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91251'">10/07 13:22</td>
                    <td style="" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91251'">00:00:00</td>
                                        <td style="" title="Ramal: ramal 1409" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91251'">1409</td>
                    <td style="" title="Ramal: ramal 1404 (1404) » Ramal: ramal 1405 (1405)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91251'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1562783369" title="Ramal: ramal 1404 (1404)" align="absmiddle" style="cursor: pointer;">  <img src="/pbxip/themes/phone2b/images/bullet_go_cf.gif?1562783369" title="Encaminhado" align="absmiddle"> 1405</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91251'">Atendida</td>
                    <td style="" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91251'"></td>
                    <td style="" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91251'">Interno</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91251'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783369" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907101322201409140415627757402114571562775740wav5d262e891e94b');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783369" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907101322201409140415627757402114571562775740wav5d262e891e94b divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907101322201409140415627757402114571562775740wav5d262e891e94b">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-132220-1409-1404-1562775740.211457-1562775740.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-132220-1409-1404-1562775740.211457-1562775740.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907101322201409140415627757402114571562775740wav5d262e891e94b" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-132220-1409-1404-1562775740.211457-1562775740.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783369" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-132220-1409-1404-1562775740.211457-1562775740.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783369" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_84" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_84" value="ODQ."
                                                      onclick="toggle_checkbox('84', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91250'">10/07 13:21</td>
                    <td style="" title="00:04:42" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91250'">00:04:42</td>
                                        <td style="" title="Ramal: Ramal 2815" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91250'">2815</td>
                    <td style="" title="Ramal: ramal 1409 (1409)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91250'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1562783369" title="Ramal: ramal 1409 (1409)" align="absmiddle" style="cursor: pointer;"> 1409</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91250'">Atendida</td>
                    <td style="" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91250'"></td>
                    <td style="" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91250'">Interno</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91250'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783369" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907101321512815140915627757112114501562775711wav5d262e8920885');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783369" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907101321512815140915627757112114501562775711wav5d262e8920885 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907101321512815140915627757112114501562775711wav5d262e8920885">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-132151-2815-1409-1562775711.211450-1562775711.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-132151-2815-1409-1562775711.211450-1562775711.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907101321512815140915627757112114501562775711wav5d262e8920885" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-132151-2815-1409-1562775711.211450-1562775711.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783369" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-132151-2815-1409-1562775711.211450-1562775711.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783369" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_85" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_85" value="ODU."
                                                      onclick="toggle_checkbox('85', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #cc6600;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91249'">10/07 13:17</td>
                    <td style="color: #cc6600;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91249'">00:00:00</td>
                                        <td style="color: #cc6600;" title="Ramal: Ramal 7005" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91249'">7005</td>
                    <td style="color: #cc6600;" title="5567984772433" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91249'">5567984772433</td>
                    <td style="color: #cc6600;" title="Não Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91249'">Não Atendida</td>
                    <td style="color: #cc6600;" title="1131000441_Campo" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91249'">1131000441_Campo</td>
                    <td style="color: #cc6600;" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91249'">Celular Local</td>
                    <td style="color: #cc6600;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91249'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783369" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_86" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_86" value="ODY."
                                                      onclick="toggle_checkbox('86', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91248'">10/07 13:17</td>
                    <td style="" title="00:01:13" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91248'">00:01:13</td>
                                        <td style="" title="Ramal: ramal 1410" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91248'">1410</td>
                    <td style="" title="5531996773423" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91248'">5531996773423</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91248'">Atendida</td>
                    <td style="" title="1131000441LifeSP5640" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91248'">1131000441LifeSP5640</td>
                    <td style="" title="Celular Nacional" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91248'">Celular Nacional</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91248'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783369" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907101317031410553199677342315627754222114401562775423wav5d262e8923b4f');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783369" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907101317031410553199677342315627754222114401562775423wav5d262e8923b4f divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907101317031410553199677342315627754222114401562775423wav5d262e8923b4f">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-131703-1410-5531996773423-1562775422.211440-1562775423.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-131703-1410-5531996773423-1562775422.211440-1562775423.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907101317031410553199677342315627754222114401562775423wav5d262e8923b4f" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-131703-1410-5531996773423-1562775422.211440-1562775423.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783369" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-131703-1410-5531996773423-1562775422.211440-1562775423.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783369" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_87" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_87" value="ODc."
                                                      onclick="toggle_checkbox('87', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91247'">10/07 13:16</td>
                    <td style="" title="00:00:04" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91247'">00:00:04</td>
                                        <td style="" title="Ramal: Ramal 7005" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91247'">7005</td>
                    <td style="" title="5567984772433" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91247'">5567984772433</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91247'">Atendida</td>
                    <td style="" title="1131000441_Campo" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91247'">1131000441_Campo</td>
                    <td style="" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91247'">Celular Local</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91247'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783369" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_20190710131624700598477243315627753842114361562775384wav5d262e89256a7');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783369" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_20190710131624700598477243315627753842114361562775384wav5d262e89256a7 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_20190710131624700598477243315627753842114361562775384wav5d262e89256a7">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-131624-7005-984772433-1562775384.211436-1562775384.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-131624-7005-984772433-1562775384.211436-1562775384.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_20190710131624700598477243315627753842114361562775384wav5d262e89256a7" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-131624-7005-984772433-1562775384.211436-1562775384.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783369" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-131624-7005-984772433-1562775384.211436-1562775384.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783369" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_88" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_88" value="ODg."
                                                      onclick="toggle_checkbox('88', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91246'">10/07 13:13</td>
                    <td style="" title="00:01:52" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91246'">00:01:52</td>
                                        <td style="" title="Ramal: ramal 1409" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91246'">1409</td>
                    <td style="" title="Ramal: Ramal 2813 (2813)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91246'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1562783369" title="Ramal: Ramal 2813 (2813)" align="absmiddle" style="cursor: pointer;"> 2813</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91246'">Atendida</td>
                    <td style="" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91246'"></td>
                    <td style="" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91246'">Interno</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91246'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783369" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907101313501409281315627751962114311562775230wav5d262e89275ea');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783369" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907101313501409281315627751962114311562775230wav5d262e89275ea divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907101313501409281315627751962114311562775230wav5d262e89275ea">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-131350-1409-2813-1562775196.211431-1562775230.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-131350-1409-2813-1562775196.211431-1562775230.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907101313501409281315627751962114311562775230wav5d262e89275ea" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-131350-1409-2813-1562775196.211431-1562775230.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783369" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-131350-1409-2813-1562775196.211431-1562775230.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783369" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_89" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_89" value="ODk."
                                                      onclick="toggle_checkbox('89', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91245'">10/07 13:13</td>
                    <td style="" title="00:02:22" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91245'">00:02:22</td>
                                        <td style="" title="Ramal: ramal 1409" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91245'">1409</td>
                    <td style="" title="Ramal: Ramal 2810 (2810)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91245'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1562783369" title="Ramal: Ramal 2810 (2810)" align="absmiddle" style="cursor: pointer;"> 2810</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91245'">Atendida</td>
                    <td style="" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91245'"></td>
                    <td style="" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91245'">Interno</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91245'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783369" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907101313171409281015627751962114311562775197wav5d262e8929526');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783369" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907101313171409281015627751962114311562775197wav5d262e8929526 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907101313171409281015627751962114311562775197wav5d262e8929526">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-131317-1409-2810-1562775196.211431-1562775197.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-131317-1409-2810-1562775196.211431-1562775197.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907101313171409281015627751962114311562775197wav5d262e8929526" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-131317-1409-2810-1562775196.211431-1562775197.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783369" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-131317-1409-2810-1562775196.211431-1562775197.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783369" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_90" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_90" value="OTA."
                                                      onclick="toggle_checkbox('90', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91244'">10/07 13:12</td>
                    <td style="" title="00:01:09" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91244'">00:01:09</td>
                                        <td style="" title="Ramal: Ramal 2802" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91244'">2802</td>
                    <td style="" title="Ramal: ramal 1410 (1410)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91244'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1562783369" title="Ramal: ramal 1410 (1410)" align="absmiddle" style="cursor: pointer;"> 1410</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91244'">Atendida</td>
                    <td style="" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91244'"></td>
                    <td style="" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91244'">Interno</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91244'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783369" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907101312092802141015627751292114271562775129wav5d262e892b462');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783369" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907101312092802141015627751292114271562775129wav5d262e892b462 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907101312092802141015627751292114271562775129wav5d262e892b462">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-131209-2802-1410-1562775129.211427-1562775129.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-131209-2802-1410-1562775129.211427-1562775129.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907101312092802141015627751292114271562775129wav5d262e892b462" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-131209-2802-1410-1562775129.211427-1562775129.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783369" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-131209-2802-1410-1562775129.211427-1562775129.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783369" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_91" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_91" value="OTE."
                                                      onclick="toggle_checkbox('91', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91243'">10/07 13:06</td>
                    <td style="" title="00:00:13" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91243'">00:00:13</td>
                                        <td style="" title="Ramal: ramal 1410" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91243'">1410</td>
                    <td style="" title="Ramal: Ramal 2804 (2804)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91243'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1562783369" title="Ramal: Ramal 2804 (2804)" align="absmiddle" style="cursor: pointer;"> 2804</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91243'">Atendida</td>
                    <td style="" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91243'"></td>
                    <td style="" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91243'">Interno</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91243'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783369" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907101306301410280415627747902114221562774790wav5d262e892d3aa');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783369" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907101306301410280415627747902114221562774790wav5d262e892d3aa divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907101306301410280415627747902114221562774790wav5d262e892d3aa">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-130630-1410-2804-1562774790.211422-1562774790.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-130630-1410-2804-1562774790.211422-1562774790.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907101306301410280415627747902114221562774790wav5d262e892d3aa" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-130630-1410-2804-1562774790.211422-1562774790.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783369" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-130630-1410-2804-1562774790.211422-1562774790.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783369" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_92" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_92" value="OTI."
                                                      onclick="toggle_checkbox('92', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #cc6600;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91242'">10/07 13:02</td>
                    <td style="color: #cc6600;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91242'">00:00:00</td>
                                        <td style="color: #cc6600;" title="Ramal: Ramal 7004" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91242'">7004</td>
                    <td style="color: #cc6600;" title="Ramal: ramal1401 (1401)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91242'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1562783369" title="Ramal: ramal1401 (1401)" align="absmiddle" style="cursor: pointer;"> 1401</td>
                    <td style="color: #cc6600;" title="Não Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91242'">Não Atendida</td>
                    <td style="color: #cc6600;" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91242'"></td>
                    <td style="color: #cc6600;" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91242'">Interno</td>
                    <td style="color: #cc6600;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91242'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783369" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_93" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_93" value="OTM."
                                                      onclick="toggle_checkbox('93', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91241'">10/07 12:56</td>
                    <td style="" title="00:01:36" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91241'">00:01:36</td>
                                        <td style="" title="Ramal: ramal 1410" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91241'">1410</td>
                    <td style="" title="5521998715841" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91241'">5521998715841</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91241'">Atendida</td>
                    <td style="" title="1131000441LifeSP5640" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91241'">1131000441LifeSP5640</td>
                    <td style="" title="Celular Nacional" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91241'">Celular Nacional</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91241'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783369" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907101256031410552199871584115627741632114141562774163wav5d262e8930a56');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783369" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907101256031410552199871584115627741632114141562774163wav5d262e8930a56 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907101256031410552199871584115627741632114141562774163wav5d262e8930a56">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-125603-1410-5521998715841-1562774163.211414-1562774163.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-125603-1410-5521998715841-1562774163.211414-1562774163.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907101256031410552199871584115627741632114141562774163wav5d262e8930a56" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-125603-1410-5521998715841-1562774163.211414-1562774163.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783369" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-125603-1410-5521998715841-1562774163.211414-1562774163.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783369" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_94" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_94" value="OTQ."
                                                      onclick="toggle_checkbox('94', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91240'">10/07 12:47</td>
                    <td style="" title="00:01:32" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91240'">00:01:32</td>
                                        <td style="" title="Ramal: ramal 1410" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91240'">1410</td>
                    <td style="" title="5511999012015" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91240'">5511999012015</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91240'">Atendida</td>
                    <td style="" title="1131000441LifeSP5640" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91240'">1131000441LifeSP5640</td>
                    <td style="" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91240'">Celular Local</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91240'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783369" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_20190710124710141099901201515627736302114081562773630wav5d262e89325b2');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783369" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_20190710124710141099901201515627736302114081562773630wav5d262e89325b2 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_20190710124710141099901201515627736302114081562773630wav5d262e89325b2">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-124710-1410-999012015-1562773630.211408-1562773630.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-124710-1410-999012015-1562773630.211408-1562773630.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_20190710124710141099901201515627736302114081562773630wav5d262e89325b2" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-124710-1410-999012015-1562773630.211408-1562773630.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783369" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-124710-1410-999012015-1562773630.211408-1562773630.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783369" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_95" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_95" value="OTU."
                                                      onclick="toggle_checkbox('95', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91239'">10/07 12:44</td>
                    <td style="" title="00:00:43" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91239'">00:00:43</td>
                                        <td style="" title="Ramal: ramal 1410" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91239'">1410</td>
                    <td style="" title="Ramal: Ramal 2807 (2807)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91239'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1562783369" title="Ramal: Ramal 2807 (2807)" align="absmiddle" style="cursor: pointer;"> 2807</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91239'">Atendida</td>
                    <td style="" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91239'"></td>
                    <td style="" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91239'">Interno</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91239'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783369" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907101244331410280715627734722114051562773473wav5d262e89344ed');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783369" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907101244331410280715627734722114051562773473wav5d262e89344ed divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907101244331410280715627734722114051562773473wav5d262e89344ed">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-124433-1410-2807-1562773472.211405-1562773473.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-124433-1410-2807-1562773472.211405-1562773473.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907101244331410280715627734722114051562773473wav5d262e89344ed" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-124433-1410-2807-1562773472.211405-1562773473.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783369" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-124433-1410-2807-1562773472.211405-1562773473.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783369" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_96" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_96" value="OTY."
                                                      onclick="toggle_checkbox('96', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91238'">10/07 12:42</td>
                    <td style="" title="00:00:48" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91238'">00:00:48</td>
                                        <td style="" title="Ramal: ramal 2604" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91238'">2604</td>
                    <td style="" title="5511968464449" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91238'">5511968464449</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91238'">Atendida</td>
                    <td style="" title="1131000441LifeSP5651" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91238'">1131000441LifeSP5651</td>
                    <td style="" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91238'">Celular Local</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91238'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783369" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_20190710124248260496846444915627733672114011562773368wav5d262e8936046');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783369" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_20190710124248260496846444915627733672114011562773368wav5d262e8936046 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_20190710124248260496846444915627733672114011562773368wav5d262e8936046">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-124248-2604-968464449-1562773367.211401-1562773368.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-124248-2604-968464449-1562773367.211401-1562773368.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_20190710124248260496846444915627733672114011562773368wav5d262e8936046" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-124248-2604-968464449-1562773367.211401-1562773368.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783369" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-124248-2604-968464449-1562773367.211401-1562773368.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783369" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_97" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_97" value="OTc."
                                                      onclick="toggle_checkbox('97', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #cc6600;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91236'">10/07 12:42</td>
                    <td style="color: #cc6600;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91236'">00:00:00</td>
                                        <td style="color: #cc6600;" title="Ramal: ramal 2604" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91236'">2604</td>
                    <td style="color: #cc6600;" title="5511968464449" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91236'">5511968464449</td>
                    <td style="color: #cc6600;" title="Não Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91236'">Não Atendida</td>
                    <td style="color: #cc6600;" title="1131000441LifeSP5651" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91236'">1131000441LifeSP5651</td>
                    <td style="color: #cc6600;" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91236'">Celular Local</td>
                    <td style="color: #cc6600;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91236'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783369" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_98" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_98" value="OTg."
                                                      onclick="toggle_checkbox('98', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91235'">10/07 12:36</td>
                    <td style="" title="00:00:44" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91235'">00:00:44</td>
                                        <td style="" title="Ramal: ramal1401" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91235'">1401</td>
                    <td style="" title="Ramal: Ramal 2807 (2807)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91235'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1562783369" title="Ramal: Ramal 2807 (2807)" align="absmiddle" style="cursor: pointer;"> 2807</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91235'">Atendida</td>
                    <td style="" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91235'"></td>
                    <td style="" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91235'">Interno</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91235'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783369" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907101236341401280715627729942113931562772994wav5d262e89396fa');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783369" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907101236341401280715627729942113931562772994wav5d262e89396fa divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907101236341401280715627729942113931562772994wav5d262e89396fa">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-123634-1401-2807-1562772994.211393-1562772994.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-123634-1401-2807-1562772994.211393-1562772994.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907101236341401280715627729942113931562772994wav5d262e89396fa" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-123634-1401-2807-1562772994.211393-1562772994.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783369" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-123634-1401-2807-1562772994.211393-1562772994.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783369" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_99" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_99" value="OTk."
                                                      onclick="toggle_checkbox('99', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91237'">10/07 12:32</td>
                    <td style="" title="00:10:10" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91237'">00:10:10</td>
                                        <td style="" title="Ramal: ramal 1410" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91237'">1410</td>
                    <td style="" title="551129116445" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91237'">551129116445</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91237'">Atendida</td>
                    <td style="" title="1131000441LifeSP5640" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91237'">1131000441LifeSP5640</td>
                    <td style="" title="Fixo Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91237'">Fixo Local</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91237'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783369" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_2019071012325514102911644515627727742113881562772775wav5d262e893b253');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1562783369" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_2019071012325514102911644515627727742113881562772775wav5d262e893b253 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_2019071012325514102911644515627727742113881562772775wav5d262e893b253">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-123255-1410-29116445-1562772774.211388-1562772775.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190710-123255-1410-29116445-1562772774.211388-1562772775.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_2019071012325514102911644515627727742113881562772775wav5d262e893b253" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190710-123255-1410-29116445-1562772774.211388-1562772775.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1562783369" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190710-123255-1410-29116445-1562772774.211388-1562772775.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1562783369" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_100" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_100" value="MTAw"
                                                      onclick="toggle_checkbox('100', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #cc6600;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91233'">10/07 12:28</td>
                    <td style="color: #cc6600;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91233'">00:00:00</td>
                                        <td style="color: #cc6600;" title="Ramal: ramal 1409" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91233'">1409</td>
                    <td style="color: #cc6600;" title="5511999954966" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91233'">5511999954966</td>
                    <td style="color: #cc6600;" title="Não Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91233'">Não Atendida</td>
                    <td style="color: #cc6600;" title="1131000441LifeSP5633" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91233'">1131000441LifeSP5633</td>
                    <td style="color: #cc6600;" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91233'">Celular Local</td>
                    <td style="color: #cc6600;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=91233'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1562783369" align="absmiddle"></td>
                                        </tbody>
                            <!--<thead>
    <td style="display: none;"></td>
    <td title="Total" nowrap><b>Total</b></td>
    <td title="Total de duração: 7715" nowrap>7715</td>
    <td colspan='5'></td>
    <td title="Total do custo: 0" align="right" nowrap>0</td>
        <td></td>
        </thead>-->
    </table>
            <br clear="all"/>
        <table align="center" id="list-view" cellpadding="0" cellspacing="0">
            <thead>
            <td title="Tipo" nowrap>Tipo</td>
                            <td title="Atendida" style="width: 75px;"
                    nowrap>Atendida</td>
                                <td title="Ocupado" style="width: 75px;"
                    nowrap>Ocupado</td>
                                <td title="Não atendida" style="width: 75px;"
                    nowrap>Não atendida</td>
                                <td title="Falhou" style="width: 75px;"
                    nowrap>Falhou</td>
                            <td title="Total" style="width: 75px;" nowrap>Total</td>
            </thead>
                            <tbody class="malhado" onmouseover="on_hover_row(jQuery(this));">
                <td title="Entrante" nowrap>Entrante</td>
                                        <td title="35" nowrap>35</td>
                                               <td title="0" nowrap>0</td>
                                                <td title="4" nowrap>4</td>
                                                <td title="0" nowrap>0</td>
                                        <td title="39" nowrap>39</td>
                </tbody>
                                <tbody class="malhado" onmouseover="on_hover_row(jQuery(this));">
                <td title="Interno" nowrap>Interno</td>
                                        <td title="65" nowrap>65</td>
                                                <td title="0" nowrap>0</td>
                                                <td title="11" nowrap>11</td>
                                                <td title="1" nowrap>1</td>
                                        <td title="77" nowrap>77</td>
                </tbody>
                                <tbody class="malhado" onmouseover="on_hover_row(jQuery(this));">
                <td title="Saínte" nowrap>Saínte</td>
                                        <td title="64" nowrap>64</td>
                                                <td title="0" nowrap>0</td>
                                                <td title="31" nowrap>31</td>
                                                <td title="4" nowrap>4</td>
                                        <td title="99" nowrap>99</td>
                </tbody>
                        </table>
        <script type="text/javascript">
    function_paginate_control(1, 3, 101);
    if (page_total == 0) {
        document.getElementById('btn_export').disabled = true;
    } else {
        document.getElementById('btn_export').disabled = false;
    }
    var quickTimeIsInstalled = detectQuickTime();
    function playAudio(nome) {
        if (quickTimeIsInstalled) {
            eval('document.' + nome + '.Play()');
        } else {
            alert('Você precisa instalar o QuickTime para ouvir esse áudio');
        }
    }
    function stopAudio(nome) {
        if (quickTimeIsInstalled) {
            eval('document.' + nome + '.Step(0);');
            eval('document.' + nome + '.Stop()');
        }
        jQuery("." + nome).toggle();
    }
    function downloadAudio(nome) {
        window.location = 'http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=' + nome;
    }
    function downloadAudioMp3(nome) {
        window.location = 'http://192.168.3.1/pbxip/core/includes/downloadaudioMp3.php?file=' + nome;
    }
    function showDiv(nome) {
        jQuery(".divs_audio").not("." + nome).hide();
        var audio = jQuery("." + nome + ".aux_audio");

    //                console.log(audio);
    //
    //                audio.attr('src', 'http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=' + nome);

            jQuery("." + nome).toggle();
        }
    </script>
    <style>
        .divs_audio {
            position: absolute;
            border: 1px solid #ccc;
            padding: 3px;
            background: #fff;
            margin-left: -120px;
        }

        audio {
            width: 50px
        }
    </style><script>doApplyConfig(0);</script>"""

dx = re.findall(r'"[a-z]+[:.].*wav"', text)

#print(dx)
links_array = []
for link in dx:
    links_array.append(link.split('>')[0].replace('"',''))
    #links_array.append()
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   


print(links_array)
 

asession = aiohttp.ClientSession()
async def fetch(url_list):
    r = await asession.get(*url_list)
    return r.read()


#
#async with asession.get(links_array) as resp:
##    print(resp.status)
 #   print(await resp.text())

