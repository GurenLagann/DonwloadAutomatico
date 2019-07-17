import asyncio
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import re
from selenium import webdriver
from aiohttp import ClientSession

text = '''    <select id="fifochkid" name="fifochkid" size="5"></select>
    <table align="center" id="list-view" cellpadding="0" cellspacing="0">
        <thead>
        <td style="display: none;"><input type="checkbox" class="checkbox" name="chkall" id="chkall"
                                          onclick="toggle_all_checkbox('fifochkid', 'text');"/></td>
        <td title="Data" style="width: 75px;" nowrap><a href="javascript:void(0);" style="width: 100%; display: block;" onclick="set_order_by('calldate', 'asc')" title="Ordernar data por ordem crescente"><img src="/pbxip/themes/phone2b/images/bullet_arrow_down_small.gif?1563378738" title="Ordernar data por ordem crescente" align="absmiddle" style="float: right; padding: 2px; padding-top: 4px; : pointer; font-weight:bolder;">Data </a></td>
        <td title="Duração" style="width: 60px;" nowrap><a href="javascript:void(0);" style="width: 100%; display: block;" onclick="set_order_by('billsec', 'asc')" title="Ordernar duração"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378738" title="Ordernar duração" align="absmiddle" style="float: right; padding: 2px; padding-top: 4px; : pointer; font-weight:bolder;">Duração </a></td>

                <td title="Nº Origem" style="width: 20%;" nowrap><a href="javascript:void(0);" style="width: 100%; display: block;" onclick="set_order_by('src', 'asc')" title="Ordernar nº origem"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378738" title="Ordernar nº origem" align="absmiddle" style="float: right; padding: 2px; padding-top: 4px; : pointer; font-weight:bolder;">Nº Origem </a></td>
        <td title="Nº Destino" style="width: 35%;" nowrap><a href="javascript:void(0);" style="width: 100%; display: block;" onclick="set_order_by('dst', 'asc')" title="Ordernar nº destino"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378738" title="Ordernar nº destino" align="absmiddle" style="float: right; padding: 2px; padding-top: 4px; : pointer; font-weight:bolder;">Nº Destino </a></td>
        <td title="Status" style="width: 75px;" nowrap><a href="javascript:void(0);" style="width: 100%; display: block;" onclick="set_order_by('status', 'asc')" title="Ordernar status"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378738" title="Ordernar status" align="absmiddle" style="float: right; padding: 2px; padding-top: 4px; : pointer; font-weight:bolder;">Status </a></td>
        <td title="Tronco" style="width: 15%;" nowrap><a href="javascript:void(0);" style="width: 100%; display: block;" onclick="set_order_by('trunk', 'asc')" title="Ordernar tronco"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378738" title="Ordernar tronco" align="absmiddle" style="float: right; padding: 2px; padding-top: 4px; : pointer; font-weight:bolder;">Tronco </a></td>
        <td title="Tipo" style="width: 28%;" nowrap><a href="javascript:void(0);" style="width: 100%; display: block;" onclick="set_order_by('type', 'asc')" title="Ordernar tipo"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378738" title="Ordernar tipo" align="absmiddle" style="float: right; padding: 2px; padding-top: 4px; : pointer; font-weight:bolder;">Tipo </a></td>
        <td title="Custo (R$)" style="width: 75px;" align="right" nowrap><a href="javascript:void(0);" style="width: 100%; display: block;" onclick="set_order_by('cost', 'asc')" title="Ordernar custo (r$)"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378738" title="Ordernar custo (r$)" align="absmiddle" style="float: right; padding: 2px; padding-top: 4px; : pointer; font-weight:bolder;">Custo (R$) </a></td>
                    <td style="width: 30px;">&nbsp;</td>
                </thead>
                            <tbody id="tr_1" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_1" value="MQ.."
                                                      onclick="toggle_checkbox('1', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92577'">16/07 21:11</td>
                    <td style="" title="00:03:25" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92577'">00:03:25</td>
                                        <td style="" title="Ramal: Ramal 2815" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92577'">2815</td>
                    <td style="" title="5581999740168" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92577'">5581999740168</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92577'">Atendida</td>
                    <td style="" title="1131000441LifeSP5642" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92577'">1131000441LifeSP5642</td>
                    <td style="" title="Celular Nacional" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92577'">Celular Nacional</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92577'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378739" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907162111302815558199974016815633222902424681563322290wav5d2f44330819f');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378739" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907162111302815558199974016815633222902424681563322290wav5d2f44330819f divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907162111302815558199974016815633222902424681563322290wav5d2f44330819f">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-211130-2815-5581999740168-1563322290.242468-1563322290.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-211130-2815-5581999740168-1563322290.242468-1563322290.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907162111302815558199974016815633222902424681563322290wav5d2f44330819f" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-211130-2815-5581999740168-1563322290.242468-1563322290.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378739" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-211130-2815-5581999740168-1563322290.242468-1563322290.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378739" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_2" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_2" value="Mg.."
                                                      onclick="toggle_checkbox('2', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #cc6600;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92576'">16/07 20:11</td>
                    <td style="color: #cc6600;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92576'">00:00:00</td>
                                        <td style="color: #cc6600;" title="Ramal: Ramal 2807" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92576'">2807</td>
                    <td style="color: #cc6600;" title="Ramal: ramal 1603 (1603)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92576'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1563378739" title="Ramal: ramal 1603 (1603)" align="absmiddle" style="cursor: pointer;"> 1603</td>
                    <td style="color: #cc6600;" title="Não Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92576'">Não Atendida</td>
                    <td style="color: #cc6600;" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92576'"></td>
                    <td style="color: #cc6600;" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92576'">Interno</td>
                    <td style="color: #cc6600;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92576'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378739" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_3" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_3" value="Mw.."
                                                      onclick="toggle_checkbox('3', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92575'">16/07 19:48</td>
                    <td style="" title="00:03:07" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92575'">00:03:07</td>
                                        <td style="" title="Ramal: Ramal 2807" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92575'">2807</td>
                    <td style="" title="Ramal: ramal 1603 (1603)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92575'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1563378739" title="Ramal: ramal 1603 (1603)" align="absmiddle" style="cursor: pointer;"> 1603</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92575'">Atendida</td>
                    <td style="" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92575'"></td>
                    <td style="" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92575'">Interno</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92575'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378739" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907161948472807160315633173262409381563317327wav5d2f4433144f6');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378739" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907161948472807160315633173262409381563317327wav5d2f4433144f6 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907161948472807160315633173262409381563317327wav5d2f4433144f6">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-194847-2807-1603-1563317326.240938-1563317327.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-194847-2807-1603-1563317326.240938-1563317327.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907161948472807160315633173262409381563317327wav5d2f4433144f6" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-194847-2807-1603-1563317326.240938-1563317327.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378739" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-194847-2807-1603-1563317326.240938-1563317327.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378739" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_4" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_4" value="NA.."
                                                      onclick="toggle_checkbox('4', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #990000;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92574'">16/07 19:21</td>
                    <td style="color: #990000;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92574'">00:00:00</td>
                                        <td style="color: #990000;" title="551130274014" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92574'">551130274014</td>
                    <td style="color: #990000;" title="Ramal: ramal 2202 (2202)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92574'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1563378739" title="Ramal: ramal 2202 (2202)" align="absmiddle" style="cursor: pointer;"> 2202</td>
                    <td style="color: #990000;" title="Falhou" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92574'">Falhou</td>
                    <td style="color: #990000;" title="1131000441LifeSP5648" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92574'">1131000441LifeSP5648</td>
                    <td style="color: #990000;" title="Entrante" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92574'">Entrante</td>
                    <td style="color: #990000;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92574'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378739" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_5" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_5" value="NQ.."
                                                      onclick="toggle_checkbox('5', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #990000;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92573'">16/07 19:20</td>
                    <td style="color: #990000;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92573'">00:00:00</td>
                                        <td style="color: #990000;" title="551130274014" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92573'">551130274014</td>
                    <td style="color: #990000;" title="Ramal: ramal 2202 (2202)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92573'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1563378739" title="Ramal: ramal 2202 (2202)" align="absmiddle" style="cursor: pointer;"> 2202</td>
                    <td style="color: #990000;" title="Falhou" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92573'">Falhou</td>
                    <td style="color: #990000;" title="1131000441LifeSP5648" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92573'">1131000441LifeSP5648</td>
                    <td style="color: #990000;" title="Entrante" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92573'">Entrante</td>
                    <td style="color: #990000;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92573'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378739" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_6" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_6" value="Ng.."
                                                      onclick="toggle_checkbox('6', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #cc6600;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92572'">16/07 19:00</td>
                    <td style="color: #cc6600;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92572'">00:00:00</td>
                                        <td style="color: #cc6600;" title="Ramal: ramal 1405" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92572'">1405</td>
                    <td style="color: #cc6600;" title="558007022242" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92572'">558007022242</td>
                    <td style="color: #cc6600;" title="Não Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92572'">Não Atendida</td>
                    <td style="color: #cc6600;" title="1131000441LifeSP5631" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92572'">1131000441LifeSP5631</td>
                    <td style="color: #cc6600;" title="0800" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92572'">0800</td>
                    <td style="color: #cc6600;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92572'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378739" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_7" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_7" value="Nw.."
                                                      onclick="toggle_checkbox('7', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92571'">16/07 18:46</td>
                    <td style="" title="00:01:45" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92571'">00:01:45</td>
                                        <td style="" title="5511998100350" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92571'">5511998100350</td>
                    <td style="" title="Grupo: GP - Lifetime - 5640 - Mesa » Ramal: ramal 1410 (1410)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92571'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_group.gif?1563378739" title="Grupo: GP - Lifetime - 5640 - Mesa" align="absmiddle" style="cursor: pointer;">  <img src="/pbxip/themes/phone2b/images/bullet_go_cf.gif?1563378739" title="Encaminhado" align="absmiddle"> 1410</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92571'">Atendida</td>
                    <td style="" title="1131000441LifeSP5648" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92571'">1131000441LifeSP5648</td>
                    <td style="" title="Entrante" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92571'">Entrante</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92571'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378739" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_2019071615633135882402371563313589wav5d2f443329cb4');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378739" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_2019071615633135882402371563313589wav5d2f443329cb4 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_2019071615633135882402371563313589wav5d2f443329cb4">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-1563313588.240237-1563313589.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-1563313588.240237-1563313589.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_2019071615633135882402371563313589wav5d2f443329cb4" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-1563313588.240237-1563313589.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378739" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-1563313588.240237-1563313589.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378739" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_8" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_8" value="OA.."
                                                      onclick="toggle_checkbox('8', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92569'">16/07 18:43</td>
                    <td style="" title="00:00:25" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92569'">00:00:25</td>
                                        <td style="" title="Ramal: Ramal 2206" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92569'">2206</td>
                    <td style="" title="Ramal: ramal 1606 (1606) » Ramal: ramal 1602 (1602)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92569'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1563378739" title="Ramal: ramal 1606 (1606)" align="absmiddle" style="cursor: pointer;">  <img src="/pbxip/themes/phone2b/images/bullet_go_cf.gif?1563378739" title="Encaminhado" align="absmiddle"> 1602</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92569'">Atendida</td>
                    <td style="" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92569'"></td>
                    <td style="" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92569'">Interno</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92569'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378739" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907161843052206160615633133842402321563313385wav5d2f443331d9e');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378739" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907161843052206160615633133842402321563313385wav5d2f443331d9e divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907161843052206160615633133842402321563313385wav5d2f443331d9e">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-184305-2206-1606-1563313384.240232-1563313385.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-184305-2206-1606-1563313384.240232-1563313385.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907161843052206160615633133842402321563313385wav5d2f443331d9e" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-184305-2206-1606-1563313384.240232-1563313385.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378739" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-184305-2206-1606-1563313384.240232-1563313385.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378739" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_9" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_9" value="OQ.."
                                                      onclick="toggle_checkbox('9', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92570'">16/07 18:42</td>
                    <td style="" title="00:01:38" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92570'">00:01:38</td>
                                        <td style="" title="Ramal: Ramal 2812" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92570'">2812</td>
                    <td style="" title="Ramal: ramal 1609 (1609)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92570'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1563378739" title="Ramal: ramal 1609 (1609)" align="absmiddle" style="cursor: pointer;"> 1609</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92570'">Atendida</td>
                    <td style="" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92570'"></td>
                    <td style="" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92570'">Interno</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92570'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378739" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907161842492812160915633133692402291563313369wav5d2f443337b5f');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378739" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907161842492812160915633133692402291563313369wav5d2f443337b5f divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907161842492812160915633133692402291563313369wav5d2f443337b5f">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-184249-2812-1609-1563313369.240229-1563313369.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-184249-2812-1609-1563313369.240229-1563313369.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907161842492812160915633133692402291563313369wav5d2f443337b5f" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-184249-2812-1609-1563313369.240229-1563313369.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378739" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-184249-2812-1609-1563313369.240229-1563313369.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378739" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_10" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_10" value="MTA."
                                                      onclick="toggle_checkbox('10', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92568'">16/07 18:31</td>
                    <td style="" title="00:00:01" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92568'">00:00:01</td>
                                        <td style="" title="5511984153191" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92568'">5511984153191</td>
                    <td style="" title="Ramal: Ramal 1406 (1406) » Ramal: ramal 1405 (1405)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92568'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1563378739" title="Ramal: Ramal 1406 (1406)" align="absmiddle" style="cursor: pointer;">  <img src="/pbxip/themes/phone2b/images/bullet_go_cf.gif?1563378739" title="Encaminhado" align="absmiddle"> 1405</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92568'">Atendida</td>
                    <td style="" title="1131000441LifeSP5648" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92568'">1131000441LifeSP5648</td>
                    <td style="" title="Entrante" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92568'">Entrante</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92568'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378739" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907161831495511984153191140615633127072402201563312709wav5d2f44333eca3');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378739" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907161831495511984153191140615633127072402201563312709wav5d2f44333eca3 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907161831495511984153191140615633127072402201563312709wav5d2f44333eca3">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-183149-5511984153191-1406-1563312707.240220-1563312709.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-183149-5511984153191-1406-1563312707.240220-1563312709.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907161831495511984153191140615633127072402201563312709wav5d2f44333eca3" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-183149-5511984153191-1406-1563312707.240220-1563312709.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378739" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-183149-5511984153191-1406-1563312707.240220-1563312709.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378739" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_11" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_11" value="MTE."
                                                      onclick="toggle_checkbox('11', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92567'">16/07 18:26</td>
                    <td style="" title="00:00:33" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92567'">00:00:33</td>
                                        <td style="" title="551136405600" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92567'">551136405600</td>
                    <td style="" title="Grupo: GP - Lifetime CG - 7480 » Ramal: Ramal 7005 (7005)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92567'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_group.gif?1563378739" title="Grupo: GP - Lifetime CG - 7480" align="absmiddle" style="cursor: pointer;">  <img src="/pbxip/themes/phone2b/images/bullet_go_cf.gif?1563378739" title="Encaminhado" align="absmiddle"> 7005</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92567'">Atendida</td>
                    <td style="" title="1131000441LifeSP5648" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92567'">1131000441LifeSP5648</td>
                    <td style="" title="Entrante" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92567'">Entrante</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92567'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378739" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_2019071615633123992402151563312399wav5d2f443342186');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378739" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_2019071615633123992402151563312399wav5d2f443342186 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_2019071615633123992402151563312399wav5d2f443342186">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-1563312399.240215-1563312399.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-1563312399.240215-1563312399.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_2019071615633123992402151563312399wav5d2f443342186" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-1563312399.240215-1563312399.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378739" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-1563312399.240215-1563312399.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378739" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_12" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_12" value="MTI."
                                                      onclick="toggle_checkbox('12', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #cc6600;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92565'">16/07 18:17</td>
                    <td style="color: #cc6600;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92565'">00:00:00</td>
                                        <td style="color: #cc6600;" title="Ramal: Ramal 2812" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92565'">2812</td>
                    <td style="color: #cc6600;" title="Ramal: ramal 1609 (1609)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92565'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1563378739" title="Ramal: ramal 1609 (1609)" align="absmiddle" style="cursor: pointer;"> 1609</td>
                    <td style="color: #cc6600;" title="Não Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92565'">Não Atendida</td>
                    <td style="color: #cc6600;" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92565'"></td>
                    <td style="color: #cc6600;" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92565'">Interno</td>
                    <td style="color: #cc6600;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92565'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378739" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_13" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_13" value="MTM."
                                                      onclick="toggle_checkbox('13', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92566'">16/07 18:07</td>
                    <td style="" title="00:12:27" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92566'">00:12:27</td>
                                        <td style="" title="Ramal: ramal 1405" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92566'">1405</td>
                    <td style="" title="5511981041194" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92566'">5511981041194</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92566'">Atendida</td>
                    <td style="" title="1131000441LifeSP5631" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92566'">1131000441LifeSP5631</td>
                    <td style="" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92566'">Celular Local</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92566'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378739" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_20190716180755140598104119415633112752402031563311275wav5d2f44334bf98');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378739" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_20190716180755140598104119415633112752402031563311275wav5d2f44334bf98 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_20190716180755140598104119415633112752402031563311275wav5d2f44334bf98">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-180755-1405-981041194-1563311275.240203-1563311275.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-180755-1405-981041194-1563311275.240203-1563311275.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_20190716180755140598104119415633112752402031563311275wav5d2f44334bf98" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-180755-1405-981041194-1563311275.240203-1563311275.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378739" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-180755-1405-981041194-1563311275.240203-1563311275.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378739" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_14" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_14" value="MTQ."
                                                      onclick="toggle_checkbox('14', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92564'">16/07 18:01</td>
                    <td style="" title="00:00:45" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92564'">00:00:45</td>
                                        <td style="" title="5565996763097" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92564'">5565996763097</td>
                    <td style="" title="Grupo: GP - Lifetime CG - 7480 » Ramal: Ramal 7003 (7003)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92564'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_group.gif?1563378739" title="Grupo: GP - Lifetime CG - 7480" align="absmiddle" style="cursor: pointer;">  <img src="/pbxip/themes/phone2b/images/bullet_go_cf.gif?1563378739" title="Encaminhado" align="absmiddle"> 7003</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92564'">Atendida</td>
                    <td style="" title="1131000441LifeSP5648" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92564'">1131000441LifeSP5648</td>
                    <td style="" title="Entrante" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92564'">Entrante</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92564'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378739" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_2019071615633108762401971563310877wav5d2f44335214a');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378739" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_2019071615633108762401971563310877wav5d2f44335214a divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_2019071615633108762401971563310877wav5d2f44335214a">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-1563310876.240197-1563310877.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-1563310876.240197-1563310877.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_2019071615633108762401971563310877wav5d2f44335214a" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-1563310876.240197-1563310877.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378739" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-1563310876.240197-1563310877.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378739" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_15" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_15" value="MTU."
                                                      onclick="toggle_checkbox('15', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #cc6600;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92562'">16/07 17:58</td>
                    <td style="color: #cc6600;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92562'">00:00:00</td>
                                        <td style="color: #cc6600;" title="Ramal: Ramal 2813" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92562'">2813</td>
                    <td style="color: #cc6600;" title="Ramal: ramal 1609 (1609)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92562'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1563378739" title="Ramal: ramal 1609 (1609)" align="absmiddle" style="cursor: pointer;"> 1609</td>
                    <td style="color: #cc6600;" title="Não Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92562'">Não Atendida</td>
                    <td style="color: #cc6600;" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92562'"></td>
                    <td style="color: #cc6600;" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92562'">Interno</td>
                    <td style="color: #cc6600;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92562'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378739" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_16" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_16" value="MTY."
                                                      onclick="toggle_checkbox('16', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92561'">16/07 17:58</td>
                    <td style="" title="00:00:06" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92561'">00:00:06</td>
                                        <td style="" title="Ramal: Ramal 2813" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92561'">2813</td>
                    <td style="" title="Ramal: ramal 1409 (1409)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92561'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1563378739" title="Ramal: ramal 1409 (1409)" align="absmiddle" style="cursor: pointer;"> 1409</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92561'">Atendida</td>
                    <td style="" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92561'"></td>
                    <td style="" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92561'">Interno</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92561'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378739" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907161758382813140915633107172401901563310718wav5d2f44335e499');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378739" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907161758382813140915633107172401901563310718wav5d2f44335e499 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907161758382813140915633107172401901563310718wav5d2f44335e499">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-175838-2813-1409-1563310717.240190-1563310718.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-175838-2813-1409-1563310717.240190-1563310718.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907161758382813140915633107172401901563310718wav5d2f44335e499" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-175838-2813-1409-1563310717.240190-1563310718.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378739" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-175838-2813-1409-1563310717.240190-1563310718.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378739" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_17" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_17" value="MTc."
                                                      onclick="toggle_checkbox('17', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92560'">16/07 17:58</td>
                    <td style="" title="00:00:11" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92560'">00:00:11</td>
                                        <td style="" title="Ramal: Ramal 7001" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92560'">7001</td>
                    <td style="" title="5567999878171" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92560'">5567999878171</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92560'">Atendida</td>
                    <td style="" title="1131000441_Campo" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92560'">1131000441_Campo</td>
                    <td style="" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92560'">Celular Local</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92560'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378739" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_20190716175801700199987817115633106802401861563310681wav5d2f443362ecd');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378739" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_20190716175801700199987817115633106802401861563310681wav5d2f443362ecd divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_20190716175801700199987817115633106802401861563310681wav5d2f443362ecd">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-175801-7001-999878171-1563310680.240186-1563310681.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-175801-7001-999878171-1563310680.240186-1563310681.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_20190716175801700199987817115633106802401861563310681wav5d2f443362ecd" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-175801-7001-999878171-1563310680.240186-1563310681.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378739" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-175801-7001-999878171-1563310680.240186-1563310681.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378739" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_18" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_18" value="MTg."
                                                      onclick="toggle_checkbox('18', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92558'">16/07 17:57</td>
                    <td style="" title="00:00:11" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92558'">00:00:11</td>
                                        <td style="" title="Ramal: Ramal 2812" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92558'">2812</td>
                    <td style="" title="Ramal: ramal 1609 (1609)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92558'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1563378739" title="Ramal: ramal 1609 (1609)" align="absmiddle" style="cursor: pointer;"> 1609</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92558'">Atendida</td>
                    <td style="" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92558'"></td>
                    <td style="" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92558'">Interno</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92558'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378739" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907161757142812160915633106332401821563310634wav5d2f443366c6e');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378739" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907161757142812160915633106332401821563310634wav5d2f443366c6e divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907161757142812160915633106332401821563310634wav5d2f443366c6e">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-175714-2812-1609-1563310633.240182-1563310634.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-175714-2812-1609-1563310633.240182-1563310634.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907161757142812160915633106332401821563310634wav5d2f443366c6e" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-175714-2812-1609-1563310633.240182-1563310634.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378739" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-175714-2812-1609-1563310633.240182-1563310634.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378739" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_19" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_19" value="MTk."
                                                      onclick="toggle_checkbox('19', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92559'">16/07 17:57</td>
                    <td style="" title="00:01:35" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92559'">00:01:35</td>
                                        <td style="" title="Ramal: ramal 1414" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92559'">1414</td>
                    <td style="" title="Ramal: ramal 1601 (1601) » Ramal: ramal 1603 (1603)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92559'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1563378739" title="Ramal: ramal 1601 (1601)" align="absmiddle" style="cursor: pointer;">  <img src="/pbxip/themes/phone2b/images/bullet_go_cf.gif?1563378739" title="Encaminhado" align="absmiddle"> 1603</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92559'">Atendida</td>
                    <td style="" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92559'"></td>
                    <td style="" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92559'">Interno</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92559'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378739" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907161757111414160115633106312401791563310631wav5d2f44336e287');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378739" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907161757111414160115633106312401791563310631wav5d2f44336e287 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907161757111414160115633106312401791563310631wav5d2f44336e287">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-175711-1414-1601-1563310631.240179-1563310631.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-175711-1414-1601-1563310631.240179-1563310631.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907161757111414160115633106312401791563310631wav5d2f44336e287" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-175711-1414-1601-1563310631.240179-1563310631.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378739" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-175711-1414-1601-1563310631.240179-1563310631.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378739" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_20" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_20" value="MjA."
                                                      onclick="toggle_checkbox('20', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92563'">16/07 17:56</td>
                    <td style="" title="00:05:54" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92563'">00:05:54</td>
                                        <td style="" title="5567999878171" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92563'">5567999878171</td>
                    <td style="" title="Grupo: GP - Lifetime CG - 7480 » Ramal: Ramal 7001 (7001)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92563'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_group.gif?1563378739" title="Grupo: GP - Lifetime CG - 7480" align="absmiddle" style="cursor: pointer;">  <img src="/pbxip/themes/phone2b/images/bullet_go_cf.gif?1563378739" title="Encaminhado" align="absmiddle"> 7001</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92563'">Atendida</td>
                    <td style="" title="1131000441LifeSP5648" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92563'">1131000441LifeSP5648</td>
                    <td style="" title="Entrante" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92563'">Entrante</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92563'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378739" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_2019071615633105712401731563310571wav5d2f443374816');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378739" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_2019071615633105712401731563310571wav5d2f443374816 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_2019071615633105712401731563310571wav5d2f443374816">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-1563310571.240173-1563310571.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-1563310571.240173-1563310571.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_2019071615633105712401731563310571wav5d2f443374816" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-1563310571.240173-1563310571.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378739" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-1563310571.240173-1563310571.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378739" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_21" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_21" value="MjE."
                                                      onclick="toggle_checkbox('21', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92557'">16/07 17:53</td>
                    <td style="" title="00:01:34" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92557'">00:01:34</td>
                                        <td style="" title="Ramal: ramal 1414" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92557'">1414</td>
                    <td style="" title="Ramal: ramal 1601 (1601)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92557'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1563378739" title="Ramal: ramal 1601 (1601)" align="absmiddle" style="cursor: pointer;"> 1601</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92557'">Atendida</td>
                    <td style="" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92557'"></td>
                    <td style="" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92557'">Interno</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92557'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378739" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907161753211414160115633104012401691563310401wav5d2f44337a9c1');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378739" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907161753211414160115633104012401691563310401wav5d2f44337a9c1 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907161753211414160115633104012401691563310401wav5d2f44337a9c1">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-175321-1414-1601-1563310401.240169-1563310401.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-175321-1414-1601-1563310401.240169-1563310401.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907161753211414160115633104012401691563310401wav5d2f44337a9c1" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-175321-1414-1601-1563310401.240169-1563310401.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378739" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-175321-1414-1601-1563310401.240169-1563310401.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378739" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_22" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_22" value="MjI."
                                                      onclick="toggle_checkbox('22', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #cc6600;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92555'">16/07 17:52</td>
                    <td style="color: #cc6600;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92555'">00:00:00</td>
                                        <td style="color: #cc6600;" title="Ramal: Ramal 2811" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92555'">2811</td>
                    <td style="color: #cc6600;" title="Ramal: Ramal1616 (1616)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92555'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1563378739" title="Ramal: Ramal1616 (1616)" align="absmiddle" style="cursor: pointer;"> 1616</td>
                    <td style="color: #cc6600;" title="Não Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92555'">Não Atendida</td>
                    <td style="color: #cc6600;" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92555'"></td>
                    <td style="color: #cc6600;" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92555'">Interno</td>
                    <td style="color: #cc6600;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92555'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378739" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_23" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_23" value="MjM."
                                                      onclick="toggle_checkbox('23', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92556'">16/07 17:48</td>
                    <td style="" title="00:05:08" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92556'">00:05:08</td>
                                        <td style="" title="Ramal: ramal 2604" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92556'">2604</td>
                    <td style="" title="551131450089" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92556'">551131450089</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92556'">Atendida</td>
                    <td style="" title="1131000441LifeSP5651" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92556'">1131000441LifeSP5651</td>
                    <td style="" title="Fixo Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92556'">Fixo Local</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92556'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378739" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_2019071617484326043145008915633101232401611563310123wav5d2f443385981');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378739" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_2019071617484326043145008915633101232401611563310123wav5d2f443385981 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_2019071617484326043145008915633101232401611563310123wav5d2f443385981">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-174843-2604-31450089-1563310123.240161-1563310123.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-174843-2604-31450089-1563310123.240161-1563310123.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_2019071617484326043145008915633101232401611563310123wav5d2f443385981" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-174843-2604-31450089-1563310123.240161-1563310123.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378739" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-174843-2604-31450089-1563310123.240161-1563310123.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378739" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_24" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_24" value="MjQ."
                                                      onclick="toggle_checkbox('24', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #cc6600;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92552'">16/07 17:47</td>
                    <td style="color: #cc6600;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92552'">00:00:00</td>
                                        <td style="color: #cc6600;" title="Ramal: ramal 1414" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92552'">1414</td>
                    <td style="color: #cc6600;" title="Ramal: Ramal1616 (1616)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92552'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1563378739" title="Ramal: Ramal1616 (1616)" align="absmiddle" style="cursor: pointer;"> 1616</td>
                    <td style="color: #cc6600;" title="Não Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92552'">Não Atendida</td>
                    <td style="color: #cc6600;" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92552'"></td>
                    <td style="color: #cc6600;" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92552'">Interno</td>
                    <td style="color: #cc6600;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92552'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378739" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_25" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_25" value="MjU."
                                                      onclick="toggle_checkbox('25', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #cc6600;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92551'">16/07 17:46</td>
                    <td style="color: #cc6600;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92551'">00:00:00</td>
                                        <td style="color: #cc6600;" title="Ramal: ramal 1414" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92551'">1414</td>
                    <td style="color: #cc6600;" title="Ramal: Ramal1616 (1616)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92551'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1563378739" title="Ramal: Ramal1616 (1616)" align="absmiddle" style="cursor: pointer;"> 1616</td>
                    <td style="color: #cc6600;" title="Não Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92551'">Não Atendida</td>
                    <td style="color: #cc6600;" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92551'"></td>
                    <td style="color: #cc6600;" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92551'">Interno</td>
                    <td style="color: #cc6600;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92551'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378739" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_26" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_26" value="MjY."
                                                      onclick="toggle_checkbox('26', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92554'">16/07 17:43</td>
                    <td style="" title="00:04:56" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92554'">00:04:56</td>
                                        <td style="" title="Ramal: Ramal 2206" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92554'">2206</td>
                    <td style="" title="Ramal: Ramal 1605 (1605)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92554'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1563378739" title="Ramal: Ramal 1605 (1605)" align="absmiddle" style="cursor: pointer;"> 1605</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92554'">Atendida</td>
                    <td style="" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92554'"></td>
                    <td style="" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92554'">Interno</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92554'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378739" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907161743182206160515633097642401491563309798wav5d2f443397e7d');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378739" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907161743182206160515633097642401491563309798wav5d2f443397e7d divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907161743182206160515633097642401491563309798wav5d2f443397e7d">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-174318-2206-1605-1563309764.240149-1563309798.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-174318-2206-1605-1563309764.240149-1563309798.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907161743182206160515633097642401491563309798wav5d2f443397e7d" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-174318-2206-1605-1563309764.240149-1563309798.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378739" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-174318-2206-1605-1563309764.240149-1563309798.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378739" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_27" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_27" value="Mjc."
                                                      onclick="toggle_checkbox('27', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92550'">16/07 17:42</td>
                    <td style="" title="00:05:27" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92550'">00:05:27</td>
                                        <td style="" title="Ramal: Ramal 2206" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92550'">2206</td>
                    <td style="" title="Ramal: ramal 1606 (1606)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92550'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1563378739" title="Ramal: ramal 1606 (1606)" align="absmiddle" style="cursor: pointer;"> 1606</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92550'">Atendida</td>
                    <td style="" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92550'"></td>
                    <td style="" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92550'">Interno</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92550'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378739" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907161742442206160615633097642401491563309764wav5d2f44339d853');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378739" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907161742442206160615633097642401491563309764wav5d2f44339d853 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907161742442206160615633097642401491563309764wav5d2f44339d853">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-174244-2206-1606-1563309764.240149-1563309764.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-174244-2206-1606-1563309764.240149-1563309764.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907161742442206160615633097642401491563309764wav5d2f44339d853" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-174244-2206-1606-1563309764.240149-1563309764.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378739" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-174244-2206-1606-1563309764.240149-1563309764.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378739" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_28" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_28" value="Mjg."
                                                      onclick="toggle_checkbox('28', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #990000;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92549'">16/07 17:41</td>
                    <td style="color: #990000;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92549'">00:00:00</td>
                                        <td style="color: #990000;" title="Ramal: ramal 1410" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92549'">1410</td>
                    <td style="color: #990000;" title="Ramal: ramal 1414 (1414)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92549'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1563378739" title="Ramal: ramal 1414 (1414)" align="absmiddle" style="cursor: pointer;"> 1414</td>
                    <td style="color: #990000;" title="Falhou" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92549'">Falhou</td>
                    <td style="color: #990000;" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92549'"></td>
                    <td style="color: #990000;" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92549'">Interno</td>
                    <td style="color: #990000;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92549'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378739" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_29" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_29" value="Mjk."
                                                      onclick="toggle_checkbox('29', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92548'">16/07 17:32</td>
                    <td style="" title="00:00:09" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92548'">00:00:09</td>
                                        <td style="" title="Ramal: ramal 1414" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92548'">1414</td>
                    <td style="" title="Ramal: Ramal1616 (1616) » Ramal: ramal 1603 (1603)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92548'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1563378739" title="Ramal: Ramal1616 (1616)" align="absmiddle" style="cursor: pointer;">  <img src="/pbxip/themes/phone2b/images/bullet_go_cf.gif?1563378739" title="Encaminhado" align="absmiddle"> 1603</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92548'">Atendida</td>
                    <td style="" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92548'"></td>
                    <td style="" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92548'">Interno</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92548'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378739" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907161732321414161615633091512401401563309152wav5d2f4433ac2bb');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378739" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907161732321414161615633091512401401563309152wav5d2f4433ac2bb divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907161732321414161615633091512401401563309152wav5d2f4433ac2bb">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-173232-1414-1616-1563309151.240140-1563309152.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-173232-1414-1616-1563309151.240140-1563309152.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907161732321414161615633091512401401563309152wav5d2f4433ac2bb" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-173232-1414-1616-1563309151.240140-1563309152.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378739" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-173232-1414-1616-1563309151.240140-1563309152.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378739" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_30" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_30" value="MzA."
                                                      onclick="toggle_checkbox('30', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92553'">16/07 17:30</td>
                    <td style="" title="00:17:02" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92553'">00:17:02</td>
                                        <td style="" title="5538998128812" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92553'">5538998128812</td>
                    <td style="" title="Grupo: GP - Lifetime - 5656 » Ramal: Ramal 2813 (2813)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92553'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_group.gif?1563378739" title="Grupo: GP - Lifetime - 5656" align="absmiddle" style="cursor: pointer;">  <img src="/pbxip/themes/phone2b/images/bullet_go_cf.gif?1563378739" title="Encaminhado" align="absmiddle"> 2813</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92553'">Atendida</td>
                    <td style="" title="1131000441LifeSP5648" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92553'">1131000441LifeSP5648</td>
                    <td style="" title="Entrante" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92553'">Entrante</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92553'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378739" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_2019071615633090572401351563309058wav5d2f4433b2851');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378739" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_2019071615633090572401351563309058wav5d2f4433b2851 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_2019071615633090572401351563309058wav5d2f4433b2851">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-1563309057.240135-1563309058.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-1563309057.240135-1563309058.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_2019071615633090572401351563309058wav5d2f4433b2851" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-1563309057.240135-1563309058.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378739" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-1563309057.240135-1563309058.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378739" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_31" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_31" value="MzE."
                                                      onclick="toggle_checkbox('31', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92545'">16/07 17:26</td>
                    <td style="" title="00:00:04" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92545'">00:00:04</td>
                                        <td style="" title="5511993417303" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92545'">5511993417303</td>
                    <td style="" title="Grupo: GP - Lifetime - 5636 » Ramal: ramal 1611 (1611)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92545'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_group.gif?1563378739" title="Grupo: GP - Lifetime - 5636" align="absmiddle" style="cursor: pointer;">  <img src="/pbxip/themes/phone2b/images/bullet_go_cf.gif?1563378739" title="Encaminhado" align="absmiddle"> 1611</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92545'">Atendida</td>
                    <td style="" title="1131000441LifeSP5648" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92545'">1131000441LifeSP5648</td>
                    <td style="" title="Entrante" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92545'">Entrante</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92545'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378739" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_2019071615633088002401261563308801wav5d2f4433b8dd7');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378739" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_2019071615633088002401261563308801wav5d2f4433b8dd7 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_2019071615633088002401261563308801wav5d2f4433b8dd7">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-1563308800.240126-1563308801.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-1563308800.240126-1563308801.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_2019071615633088002401261563308801wav5d2f4433b8dd7" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-1563308800.240126-1563308801.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378739" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-1563308800.240126-1563308801.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378739" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_32" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_32" value="MzI."
                                                      onclick="toggle_checkbox('32', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92546'">16/07 17:24</td>
                    <td style="" title="00:02:38" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92546'">00:02:38</td>
                                        <td style="" title="Ramal: Ramal 2813" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92546'">2813</td>
                    <td style="" title="Ramal: ramal 1609 (1609)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92546'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1563378739" title="Ramal: ramal 1609 (1609)" align="absmiddle" style="cursor: pointer;"> 1609</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92546'">Atendida</td>
                    <td style="" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92546'"></td>
                    <td style="" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92546'">Interno</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92546'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378739" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907161724562813160915633086962401231563308696wav5d2f4433beb96');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378739" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907161724562813160915633086962401231563308696wav5d2f4433beb96 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907161724562813160915633086962401231563308696wav5d2f4433beb96">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-172456-2813-1609-1563308696.240123-1563308696.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-172456-2813-1609-1563308696.240123-1563308696.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907161724562813160915633086962401231563308696wav5d2f4433beb96" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-172456-2813-1609-1563308696.240123-1563308696.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378739" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-172456-2813-1609-1563308696.240123-1563308696.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378739" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_33" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_33" value="MzM."
                                                      onclick="toggle_checkbox('33', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #990000;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92544'">16/07 17:12</td>
                    <td style="color: #990000;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92544'">00:00:00</td>
                                        <td style="color: #990000;" title="Ramal: ramal 1410" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92544'">1410</td>
                    <td style="color: #990000;" title="Ramal: ramal 1414 (1414)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92544'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1563378739" title="Ramal: ramal 1414 (1414)" align="absmiddle" style="cursor: pointer;"> 1414</td>
                    <td style="color: #990000;" title="Falhou" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92544'">Falhou</td>
                    <td style="color: #990000;" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92544'"></td>
                    <td style="color: #990000;" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92544'">Interno</td>
                    <td style="color: #990000;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92544'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378739" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_34" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_34" value="MzQ."
                                                      onclick="toggle_checkbox('34', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92542'">16/07 17:07</td>
                    <td style="" title="00:00:04" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92542'">00:00:04</td>
                                        <td style="" title="Ramal: ramal 1409" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92542'">1409</td>
                    <td style="" title="5511981052111" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92542'">5511981052111</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92542'">Atendida</td>
                    <td style="" title="1131000441LifeSP5633" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92542'">1131000441LifeSP5633</td>
                    <td style="" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92542'">Celular Local</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92542'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378739" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_20190716170740140998105211115633076602401121563307660wav5d2f4433c9b61');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378739" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_20190716170740140998105211115633076602401121563307660wav5d2f4433c9b61 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_20190716170740140998105211115633076602401121563307660wav5d2f4433c9b61">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-170740-1409-981052111-1563307660.240112-1563307660.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-170740-1409-981052111-1563307660.240112-1563307660.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_20190716170740140998105211115633076602401121563307660wav5d2f4433c9b61" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-170740-1409-981052111-1563307660.240112-1563307660.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378739" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-170740-1409-981052111-1563307660.240112-1563307660.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378739" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_35" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_35" value="MzU."
                                                      onclick="toggle_checkbox('35', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92541'">16/07 17:06</td>
                    <td style="" title="00:00:21" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92541'">00:00:21</td>
                                        <td style="" title="5519981681010" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92541'">5519981681010</td>
                    <td style="" title="551133855642" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92541'">551133855642</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92541'">Atendida</td>
                    <td style="" title="1131000441LifeSP5648" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92541'">1131000441LifeSP5648</td>
                    <td style="" title="Entrante" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92541'">Entrante</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92541'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378739" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_36" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_36" value="MzY."
                                                      onclick="toggle_checkbox('36', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92547'">16/07 17:06</td>
                    <td style="" title="00:22:41" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92547'">00:22:41</td>
                                        <td style="" title="Ramal: ramal 1414" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92547'">1414</td>
                    <td style="" title="5511983463660" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92547'">5511983463660</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92547'">Atendida</td>
                    <td style="" title="1131000441LifeSP5635" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92547'">1131000441LifeSP5635</td>
                    <td style="" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92547'">Celular Local</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92547'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378739" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_20190716170608141498346366015633075682401071563307568wav5d2f4433d1479');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378739" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_20190716170608141498346366015633075682401071563307568wav5d2f4433d1479 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_20190716170608141498346366015633075682401071563307568wav5d2f4433d1479">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-170608-1414-983463660-1563307568.240107-1563307568.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-170608-1414-983463660-1563307568.240107-1563307568.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_20190716170608141498346366015633075682401071563307568wav5d2f4433d1479" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-170608-1414-983463660-1563307568.240107-1563307568.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378739" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-170608-1414-983463660-1563307568.240107-1563307568.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378739" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_37" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_37" value="Mzc."
                                                      onclick="toggle_checkbox('37', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92540'">16/07 17:03</td>
                    <td style="" title="00:01:48" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92540'">00:01:48</td>
                                        <td style="" title="Ramal: ramal 1609" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92540'">1609</td>
                    <td style="" title="5511999797306" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92540'">5511999797306</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92540'">Atendida</td>
                    <td style="" title="1131000441LifeSP5636" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92540'">1131000441LifeSP5636</td>
                    <td style="" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92540'">Celular Local</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92540'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378739" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907161703041609551199979730615633073842401021563307384wav5d2f4433d5eb5');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378739" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907161703041609551199979730615633073842401021563307384wav5d2f4433d5eb5 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907161703041609551199979730615633073842401021563307384wav5d2f4433d5eb5">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-170304-1609-5511999797306-1563307384.240102-1563307384.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-170304-1609-5511999797306-1563307384.240102-1563307384.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907161703041609551199979730615633073842401021563307384wav5d2f4433d5eb5" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-170304-1609-5511999797306-1563307384.240102-1563307384.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378739" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-170304-1609-5511999797306-1563307384.240102-1563307384.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378739" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_38" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_38" value="Mzg."
                                                      onclick="toggle_checkbox('38', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #cc6600;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92539'">16/07 16:59</td>
                    <td style="color: #cc6600;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92539'">00:00:00</td>
                                        <td style="color: #cc6600;" title="Ramal: Ramal 2810" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92539'">2810</td>
                    <td style="color: #cc6600;" title="5515997797877" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92539'">5515997797877</td>
                    <td style="color: #cc6600;" title="Não Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92539'">Não Atendida</td>
                    <td style="color: #cc6600;" title="1131000441LifeSP5642" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92539'">1131000441LifeSP5642</td>
                    <td style="color: #cc6600;" title="Celular Nacional" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92539'">Celular Nacional</td>
                    <td style="color: #cc6600;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92539'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378739" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_39" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_39" value="Mzk."
                                                      onclick="toggle_checkbox('39', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92543'">16/07 16:57</td>
                    <td style="" title="00:13:35" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92543'">00:13:35</td>
                                        <td style="" title="5511989996235" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92543'">5511989996235</td>
                    <td style="" title="Grupo: GP - Lifetime - 5640 - Mesa » Ramal: ramal 1410 (1410)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92543'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_group.gif?1563378739" title="Grupo: GP - Lifetime - 5640 - Mesa" align="absmiddle" style="cursor: pointer;">  <img src="/pbxip/themes/phone2b/images/bullet_go_cf.gif?1563378739" title="Encaminhado" align="absmiddle"> 1410</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92543'">Atendida</td>
                    <td style="" title="1131000441LifeSP5648" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92543'">1131000441LifeSP5648</td>
                    <td style="" title="Entrante" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92543'">Entrante</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92543'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378739" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_2019071615633070642400921563307065wav5d2f4433e164d');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378739" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_2019071615633070642400921563307065wav5d2f4433e164d divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_2019071615633070642400921563307065wav5d2f4433e164d">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-1563307064.240092-1563307065.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-1563307064.240092-1563307065.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_2019071615633070642400921563307065wav5d2f4433e164d" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-1563307064.240092-1563307065.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378739" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-1563307064.240092-1563307065.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378739" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_40" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_40" value="NDA."
                                                      onclick="toggle_checkbox('40', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92538'">16/07 16:56</td>
                    <td style="" title="00:03:45" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92538'">00:03:45</td>
                                        <td style="" title="Ramal: Ramal 7003" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92538'">7003</td>
                    <td style="" title="5567999557770" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92538'">5567999557770</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92538'">Atendida</td>
                    <td style="" title="1131000441_Campo" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92538'">1131000441_Campo</td>
                    <td style="" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92538'">Celular Local</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92538'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378739" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_20190716165603700399955777015633069632400761563306963wav5d2f4433e685a');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378739" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_20190716165603700399955777015633069632400761563306963wav5d2f4433e685a divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_20190716165603700399955777015633069632400761563306963wav5d2f4433e685a">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-165603-7003-999557770-1563306963.240076-1563306963.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-165603-7003-999557770-1563306963.240076-1563306963.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_20190716165603700399955777015633069632400761563306963wav5d2f4433e685a" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-165603-7003-999557770-1563306963.240076-1563306963.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378739" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-165603-7003-999557770-1563306963.240076-1563306963.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378739" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_41" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_41" value="NDE."
                                                      onclick="toggle_checkbox('41', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92537'">16/07 16:55</td>
                    <td style="" title="00:01:21" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92537'">00:01:21</td>
                                        <td style="" title="5511989996235" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92537'">5511989996235</td>
                    <td style="" title="Grupo: GP - Lifetime - 5640 - Mesa » Ramal: ramal1401 (1401)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92537'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_group.gif?1563378739" title="Grupo: GP - Lifetime - 5640 - Mesa" align="absmiddle" style="cursor: pointer;">  <img src="/pbxip/themes/phone2b/images/bullet_go_cf.gif?1563378739" title="Encaminhado" align="absmiddle"> 1401</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92537'">Atendida</td>
                    <td style="" title="1131000441LifeSP5648" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92537'">1131000441LifeSP5648</td>
                    <td style="" title="Entrante" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92537'">Entrante</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92537'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378739" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_2019071615633069552400711563306956wav5d2f4433eca08');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378739" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_2019071615633069552400711563306956wav5d2f4433eca08 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_2019071615633069552400711563306956wav5d2f4433eca08">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-1563306955.240071-1563306956.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-1563306955.240071-1563306956.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_2019071615633069552400711563306956wav5d2f4433eca08" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-1563306955.240071-1563306956.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378739" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-1563306955.240071-1563306956.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378739" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_42" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_42" value="NDI."
                                                      onclick="toggle_checkbox('42', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #cc6600;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92536'">16/07 16:54</td>
                    <td style="color: #cc6600;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92536'">00:00:00</td>
                                        <td style="color: #cc6600;" title="Ramal: Ramal 7003" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92536'">7003</td>
                    <td style="color: #cc6600;" title="5565996763097" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92536'">5565996763097</td>
                    <td style="color: #cc6600;" title="Não Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92536'">Não Atendida</td>
                    <td style="color: #cc6600;" title="1131000441_Campo" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92536'">1131000441_Campo</td>
                    <td style="color: #cc6600;" title="Celular Nacional" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92536'">Celular Nacional</td>
                    <td style="color: #cc6600;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92536'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378739" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_43" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_43" value="NDM."
                                                      onclick="toggle_checkbox('43', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92535'">16/07 16:54</td>
                    <td style="" title="00:00:05" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92535'">00:00:05</td>
                                        <td style="" title="5519981681010" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92535'">5519981681010</td>
                    <td style="" title="551133855642" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92535'">551133855642</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92535'">Atendida</td>
                    <td style="" title="1131000441LifeSP5648" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92535'">1131000441LifeSP5648</td>
                    <td style="" title="Entrante" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92535'">Entrante</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92535'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378740" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_44" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_44" value="NDQ."
                                                      onclick="toggle_checkbox('44', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92534'">16/07 16:53</td>
                    <td style="" title="00:00:21" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92534'">00:00:21</td>
                                        <td style="" title="5519981681010" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92534'">5519981681010</td>
                    <td style="" title="551133855642" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92534'">551133855642</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92534'">Atendida</td>
                    <td style="" title="1131000441LifeSP5648" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92534'">1131000441LifeSP5648</td>
                    <td style="" title="Entrante" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92534'">Entrante</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92534'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378740" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_45" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_45" value="NDU."
                                                      onclick="toggle_checkbox('45', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #cc6600;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92533'">16/07 16:53</td>
                    <td style="color: #cc6600;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92533'">00:00:00</td>
                                        <td style="color: #cc6600;" title="Ramal: Ramal 7003" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92533'">7003</td>
                    <td style="color: #cc6600;" title="5565996763097" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92533'">5565996763097</td>
                    <td style="color: #cc6600;" title="Não Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92533'">Não Atendida</td>
                    <td style="color: #cc6600;" title="1131000441_Campo" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92533'">1131000441_Campo</td>
                    <td style="color: #cc6600;" title="Celular Nacional" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92533'">Celular Nacional</td>
                    <td style="color: #cc6600;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92533'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378740" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_46" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_46" value="NDY."
                                                      onclick="toggle_checkbox('46', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92532'">16/07 16:47</td>
                    <td style="" title="00:03:10" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92532'">00:03:10</td>
                                        <td style="" title="Ramal: Ramal 2208" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92532'">2208</td>
                    <td style="" title="Ramal: ramal 2601 (2601)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92532'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1563378740" title="Ramal: ramal 2601 (2601)" align="absmiddle" style="cursor: pointer;"> 2601</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92532'">Atendida</td>
                    <td style="" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92532'"></td>
                    <td style="" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92532'">Interno</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92532'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378740" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907161648002208260115633064342400541563306480wav5d2f44340e36b');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378740" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907161648002208260115633064342400541563306480wav5d2f44340e36b divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907161648002208260115633064342400541563306480wav5d2f44340e36b">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-164800-2208-2601-1563306434.240054-1563306480.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-164800-2208-2601-1563306434.240054-1563306480.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907161648002208260115633064342400541563306480wav5d2f44340e36b" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-164800-2208-2601-1563306434.240054-1563306480.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378740" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-164800-2208-2601-1563306434.240054-1563306480.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378740" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_47" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_47" value="NDc."
                                                      onclick="toggle_checkbox('47', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92531'">16/07 16:47</td>
                    <td style="" title="00:03:10" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92531'">00:03:10</td>
                                        <td style="" title="Ramal: Ramal 2208" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92531'">2208</td>
                    <td style="" title="Ramal: ramal 2606 (2606)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92531'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1563378740" title="Ramal: ramal 2606 (2606)" align="absmiddle" style="cursor: pointer;"> 2606</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92531'">Atendida</td>
                    <td style="" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92531'"></td>
                    <td style="" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92531'">Interno</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92531'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378740" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907161647142208260615633064342400541563306434wav5d2f443414515');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378740" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907161647142208260615633064342400541563306434wav5d2f443414515 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907161647142208260615633064342400541563306434wav5d2f443414515">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-164714-2208-2606-1563306434.240054-1563306434.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-164714-2208-2606-1563306434.240054-1563306434.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907161647142208260615633064342400541563306434wav5d2f443414515" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-164714-2208-2606-1563306434.240054-1563306434.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378740" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-164714-2208-2606-1563306434.240054-1563306434.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378740" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_48" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_48" value="NDg."
                                                      onclick="toggle_checkbox('48', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92530'">16/07 16:36</td>
                    <td style="" title="00:00:23" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92530'">00:00:23</td>
                                        <td style="" title="Ramal: Ramal 2810" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92530'">2810</td>
                    <td style="" title="5511959481823" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92530'">5511959481823</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92530'">Atendida</td>
                    <td style="" title="1131000441LifeSP5642" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92530'">1131000441LifeSP5642</td>
                    <td style="" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92530'">Celular Local</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92530'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378740" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_20190716163657281095948182315633058172400461563305817wav5d2f443419335');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378740" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_20190716163657281095948182315633058172400461563305817wav5d2f443419335 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_20190716163657281095948182315633058172400461563305817wav5d2f443419335">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-163657-2810-959481823-1563305817.240046-1563305817.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-163657-2810-959481823-1563305817.240046-1563305817.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_20190716163657281095948182315633058172400461563305817wav5d2f443419335" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-163657-2810-959481823-1563305817.240046-1563305817.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378740" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-163657-2810-959481823-1563305817.240046-1563305817.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378740" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_49" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_49" value="NDk."
                                                      onclick="toggle_checkbox('49', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92529'">16/07 16:35</td>
                    <td style="" title="00:00:32" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92529'">00:00:32</td>
                                        <td style="" title="Ramal: Ramal 2802" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92529'">2802</td>
                    <td style="" title="Ramal: ramal 1603 (1603)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92529'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1563378740" title="Ramal: ramal 1603 (1603)" align="absmiddle" style="cursor: pointer;"> 1603</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92529'">Atendida</td>
                    <td style="" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92529'"></td>
                    <td style="" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92529'">Interno</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92529'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378740" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907161635372802160315633057372400431563305737wav5d2f44341ed13');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378740" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907161635372802160315633057372400431563305737wav5d2f44341ed13 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907161635372802160315633057372400431563305737wav5d2f44341ed13">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-163537-2802-1603-1563305737.240043-1563305737.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-163537-2802-1603-1563305737.240043-1563305737.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907161635372802160315633057372400431563305737wav5d2f44341ed13" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-163537-2802-1603-1563305737.240043-1563305737.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378740" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-163537-2802-1603-1563305737.240043-1563305737.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378740" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_50" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_50" value="NTA."
                                                      onclick="toggle_checkbox('50', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92528'">16/07 16:34</td>
                    <td style="" title="00:00:47" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92528'">00:00:47</td>
                                        <td style="" title="Ramal: Ramal 2802" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92528'">2802</td>
                    <td style="" title="Ramal: Ramal 2206 (2206) » Ramal: Ramal 2208 (2208)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92528'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1563378740" title="Ramal: Ramal 2206 (2206)" align="absmiddle" style="cursor: pointer;">  <img src="/pbxip/themes/phone2b/images/bullet_go_cf.gif?1563378740" title="Encaminhado" align="absmiddle"> 2208</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92528'">Atendida</td>
                    <td style="" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92528'"></td>
                    <td style="" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92528'">Interno</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92528'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378740" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907161634042802220615633056442400391563305644wav5d2f4434279ad');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378740" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907161634042802220615633056442400391563305644wav5d2f4434279ad divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907161634042802220615633056442400391563305644wav5d2f4434279ad">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-163404-2802-2206-1563305644.240039-1563305644.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-163404-2802-2206-1563305644.240039-1563305644.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907161634042802220615633056442400391563305644wav5d2f4434279ad" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-163404-2802-2206-1563305644.240039-1563305644.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378740" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-163404-2802-2206-1563305644.240039-1563305644.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378740" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_51" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_51" value="NTE."
                                                      onclick="toggle_checkbox('51', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92527'">16/07 16:32</td>
                    <td style="" title="00:01:49" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92527'">00:01:49</td>
                                        <td style="" title="551140813800" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92527'">551140813800</td>
                    <td style="" title="Grupo: GP - Lifetime - 5656 » Ramal: Ramal 2802 (2802)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92527'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_group.gif?1563378740" title="Grupo: GP - Lifetime - 5656" align="absmiddle" style="cursor: pointer;">  <img src="/pbxip/themes/phone2b/images/bullet_go_cf.gif?1563378740" title="Encaminhado" align="absmiddle"> 2802</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92527'">Atendida</td>
                    <td style="" title="1131000441LifeSP5648" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92527'">1131000441LifeSP5648</td>
                    <td style="" title="Entrante" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92527'">Entrante</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92527'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378740" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_2019071615633055642400171563305565wav5d2f44342db6d');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378740" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_2019071615633055642400171563305565wav5d2f44342db6d divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_2019071615633055642400171563305565wav5d2f44342db6d">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-1563305564.240017-1563305565.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-1563305564.240017-1563305565.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_2019071615633055642400171563305565wav5d2f44342db6d" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-1563305564.240017-1563305565.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378740" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-1563305564.240017-1563305565.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378740" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_52" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_52" value="NTI."
                                                      onclick="toggle_checkbox('52', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #cc6600;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92526'">16/07 16:31</td>
                    <td style="color: #cc6600;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92526'">00:00:00</td>
                                        <td style="color: #cc6600;" title="Ramal: Ramal 2810" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92526'">2810</td>
                    <td style="color: #cc6600;" title="5511999985365" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92526'">5511999985365</td>
                    <td style="color: #cc6600;" title="Não Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92526'">Não Atendida</td>
                    <td style="color: #cc6600;" title="1131000441LifeSP5642" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92526'">1131000441LifeSP5642</td>
                    <td style="color: #cc6600;" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92526'">Celular Local</td>
                    <td style="color: #cc6600;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92526'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378740" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_53" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_53" value="NTM."
                                                      onclick="toggle_checkbox('53', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92524'">16/07 16:30</td>
                    <td style="" title="00:00:23" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92524'">00:00:23</td>
                                        <td style="" title="Ramal: Ramal 2208" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92524'">2208</td>
                    <td style="" title="Ramal: Ramal 1406 (1406)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92524'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1563378740" title="Ramal: Ramal 1406 (1406)" align="absmiddle" style="cursor: pointer;"> 1406</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92524'">Atendida</td>
                    <td style="" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92524'"></td>
                    <td style="" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92524'">Interno</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92524'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378740" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907161630552208140615633054552400101563305455wav5d2f443438b2d');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378740" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907161630552208140615633054552400101563305455wav5d2f443438b2d divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907161630552208140615633054552400101563305455wav5d2f443438b2d">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-163055-2208-1406-1563305455.240010-1563305455.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-163055-2208-1406-1563305455.240010-1563305455.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907161630552208140615633054552400101563305455wav5d2f443438b2d" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-163055-2208-1406-1563305455.240010-1563305455.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378740" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-163055-2208-1406-1563305455.240010-1563305455.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378740" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_54" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_54" value="NTQ."
                                                      onclick="toggle_checkbox('54', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92525'">16/07 16:30</td>
                    <td style="" title="00:01:12" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92525'">00:01:12</td>
                                        <td style="" title="5521974407776" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92525'">5521974407776</td>
                    <td style="" title="Ramal: ramal 2604 (2604)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92525'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1563378740" title="Ramal: ramal 2604 (2604)" align="absmiddle" style="cursor: pointer;"> 2604</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92525'">Atendida</td>
                    <td style="" title="1131000441LifeSP5648" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92525'">1131000441LifeSP5648</td>
                    <td style="" title="Entrante" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92525'">Entrante</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92525'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378740" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907161630495521974407776260415633054472400071563305449wav5d2f44343d94f');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378740" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907161630495521974407776260415633054472400071563305449wav5d2f44343d94f divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907161630495521974407776260415633054472400071563305449wav5d2f44343d94f">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-163049-5521974407776-2604-1563305447.240007-1563305449.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-163049-5521974407776-2604-1563305447.240007-1563305449.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907161630495521974407776260415633054472400071563305449wav5d2f44343d94f" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-163049-5521974407776-2604-1563305447.240007-1563305449.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378740" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-163049-5521974407776-2604-1563305447.240007-1563305449.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378740" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_55" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_55" value="NTU."
                                                      onclick="toggle_checkbox('55', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92523'">16/07 16:27</td>
                    <td style="" title="00:00:29" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92523'">00:00:29</td>
                                        <td style="" title="5511993813435" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92523'">5511993813435</td>
                    <td style="" title="Ramal: ramal 2604 (2604)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92523'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1563378740" title="Ramal: ramal 2604 (2604)" align="absmiddle" style="cursor: pointer;"> 2604</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92523'">Atendida</td>
                    <td style="" title="1131000441LifeSP5648" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92523'">1131000441LifeSP5648</td>
                    <td style="" title="Entrante" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92523'">Entrante</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92523'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378740" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907161627295511993813435260415633052482400031563305249wav5d2f44344276c');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378740" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907161627295511993813435260415633052482400031563305249wav5d2f44344276c divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907161627295511993813435260415633052482400031563305249wav5d2f44344276c">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-162729-5511993813435-2604-1563305248.240003-1563305249.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-162729-5511993813435-2604-1563305248.240003-1563305249.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907161627295511993813435260415633052482400031563305249wav5d2f44344276c" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-162729-5511993813435-2604-1563305248.240003-1563305249.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378740" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-162729-5511993813435-2604-1563305248.240003-1563305249.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378740" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_56" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_56" value="NTY."
                                                      onclick="toggle_checkbox('56', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #990000;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92521'">16/07 16:26</td>
                    <td style="color: #990000;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92521'">00:00:00</td>
                                        <td style="color: #990000;" title="551130172140" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92521'">551130172140</td>
                    <td style="color: #990000;" title="Ramal: ramal 2202 (2202)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92521'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1563378740" title="Ramal: ramal 2202 (2202)" align="absmiddle" style="cursor: pointer;"> 2202</td>
                    <td style="color: #990000;" title="Falhou" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92521'">Falhou</td>
                    <td style="color: #990000;" title="1131000441LifeSP5648" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92521'">1131000441LifeSP5648</td>
                    <td style="color: #990000;" title="Entrante" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92521'">Entrante</td>
                    <td style="color: #990000;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92521'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378740" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_57" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_57" value="NTc."
                                                      onclick="toggle_checkbox('57', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92522'">16/07 16:25</td>
                    <td style="" title="00:02:36" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92522'">00:02:36</td>
                                        <td style="" title="Ramal: ramal 1410" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92522'">1410</td>
                    <td style="" title="5521998715841" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92522'">5521998715841</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92522'">Atendida</td>
                    <td style="" title="1131000441LifeSP5640" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92522'">1131000441LifeSP5640</td>
                    <td style="" title="Celular Nacional" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92522'">Celular Nacional</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92522'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378740" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907161625271410552199871584115633051272399961563305127wav5d2f44344c3a5');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378740" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907161625271410552199871584115633051272399961563305127wav5d2f44344c3a5 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907161625271410552199871584115633051272399961563305127wav5d2f44344c3a5">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-162527-1410-5521998715841-1563305127.239996-1563305127.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-162527-1410-5521998715841-1563305127.239996-1563305127.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907161625271410552199871584115633051272399961563305127wav5d2f44344c3a5" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-162527-1410-5521998715841-1563305127.239996-1563305127.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378740" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-162527-1410-5521998715841-1563305127.239996-1563305127.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378740" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_58" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_58" value="NTg."
                                                      onclick="toggle_checkbox('58', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92520'">16/07 16:24</td>
                    <td style="" title="00:02:04" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92520'">00:02:04</td>
                                        <td style="" title="Ramal: Ramal 2804" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92520'">2804</td>
                    <td style="" title="Ramal: ramal 1603 (1603)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92520'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1563378740" title="Ramal: ramal 1603 (1603)" align="absmiddle" style="cursor: pointer;"> 1603</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92520'">Atendida</td>
                    <td style="" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92520'"></td>
                    <td style="" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92520'">Interno</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92520'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378740" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907161624492804160315633050892399931563305089wav5d2f443452558');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378740" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907161624492804160315633050892399931563305089wav5d2f443452558 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907161624492804160315633050892399931563305089wav5d2f443452558">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-162449-2804-1603-1563305089.239993-1563305089.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-162449-2804-1603-1563305089.239993-1563305089.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907161624492804160315633050892399931563305089wav5d2f443452558" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-162449-2804-1603-1563305089.239993-1563305089.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378740" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-162449-2804-1603-1563305089.239993-1563305089.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378740" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_59" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_59" value="NTk."
                                                      onclick="toggle_checkbox('59', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92519'">16/07 16:24</td>
                    <td style="" title="00:02:38" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92519'">00:02:38</td>
                                        <td style="" title="551155723178" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92519'">551155723178</td>
                    <td style="" title="Grupo: GP - Lifetime - 5656 » Ramal: Ramal 2804 (2804)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92519'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_group.gif?1563378740" title="Grupo: GP - Lifetime - 5656" align="absmiddle" style="cursor: pointer;">  <img src="/pbxip/themes/phone2b/images/bullet_go_cf.gif?1563378740" title="Encaminhado" align="absmiddle"> 2804</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92519'">Atendida</td>
                    <td style="" title="1131000441LifeSP5648" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92519'">1131000441LifeSP5648</td>
                    <td style="" title="Entrante" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92519'">Entrante</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92519'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378740" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_2019071615633050552399881563305056wav5d2f443458ade');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378740" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_2019071615633050552399881563305056wav5d2f443458ade divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_2019071615633050552399881563305056wav5d2f443458ade">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-1563305055.239988-1563305056.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-1563305055.239988-1563305056.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_2019071615633050552399881563305056wav5d2f443458ade" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-1563305055.239988-1563305056.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378740" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-1563305055.239988-1563305056.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378740" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_60" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_60" value="NjA."
                                                      onclick="toggle_checkbox('60', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92517'">16/07 16:13</td>
                    <td style="" title="00:00:25" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92517'">00:00:25</td>
                                        <td style="" title="Ramal: Ramal 2208" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92517'">2208</td>
                    <td style="" title="Ramal: ramal 1609 (1609)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92517'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1563378740" title="Ramal: ramal 1609 (1609)" align="absmiddle" style="cursor: pointer;"> 1609</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92517'">Atendida</td>
                    <td style="" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92517'"></td>
                    <td style="" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92517'">Interno</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92517'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378740" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907161613552208160915633044352399821563304435wav5d2f44345e89f');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378740" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907161613552208160915633044352399821563304435wav5d2f44345e89f divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907161613552208160915633044352399821563304435wav5d2f44345e89f">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-161355-2208-1609-1563304435.239982-1563304435.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-161355-2208-1609-1563304435.239982-1563304435.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907161613552208160915633044352399821563304435wav5d2f44345e89f" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-161355-2208-1609-1563304435.239982-1563304435.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378740" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-161355-2208-1609-1563304435.239982-1563304435.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378740" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_61" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_61" value="NjE."
                                                      onclick="toggle_checkbox('61', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92518'">16/07 16:12</td>
                    <td style="" title="00:12:10" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92518'">00:12:10</td>
                                        <td style="" title="5513997141313" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92518'">5513997141313</td>
                    <td style="" title="Grupo: GP - Lifetime - 5640 - Mesa » Ramal: ramal 1410 (1410)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92518'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_group.gif?1563378740" title="Grupo: GP - Lifetime - 5640 - Mesa" align="absmiddle" style="cursor: pointer;">  <img src="/pbxip/themes/phone2b/images/bullet_go_cf.gif?1563378740" title="Encaminhado" align="absmiddle"> 1410</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92518'">Atendida</td>
                    <td style="" title="1131000441LifeSP5648" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92518'">1131000441LifeSP5648</td>
                    <td style="" title="Entrante" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92518'">Entrante</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92518'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378740" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_2019071615633043532399761563304354wav5d2f443464e32');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378740" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_2019071615633043532399761563304354wav5d2f443464e32 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_2019071615633043532399761563304354wav5d2f443464e32">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-1563304353.239976-1563304354.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-1563304353.239976-1563304354.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_2019071615633043532399761563304354wav5d2f443464e32" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-1563304353.239976-1563304354.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378740" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-1563304353.239976-1563304354.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378740" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_62" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_62" value="NjI."
                                                      onclick="toggle_checkbox('62', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92515'">16/07 16:09</td>
                    <td style="" title="00:00:04" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92515'">00:00:04</td>
                                        <td style="" title="Ramal: Ramal 2810" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92515'">2810</td>
                    <td style="" title="5511994568497" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92515'">5511994568497</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92515'">Atendida</td>
                    <td style="" title="1131000441LifeSP5642" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92515'">1131000441LifeSP5642</td>
                    <td style="" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92515'">Celular Local</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92515'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378740" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_20190716160904281099456849715633041442399721563304144wav5d2f443469c5a');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378740" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_20190716160904281099456849715633041442399721563304144wav5d2f443469c5a divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_20190716160904281099456849715633041442399721563304144wav5d2f443469c5a">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-160904-2810-994568497-1563304144.239972-1563304144.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-160904-2810-994568497-1563304144.239972-1563304144.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_20190716160904281099456849715633041442399721563304144wav5d2f443469c5a" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-160904-2810-994568497-1563304144.239972-1563304144.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378740" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-160904-2810-994568497-1563304144.239972-1563304144.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378740" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_63" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_63" value="NjM."
                                                      onclick="toggle_checkbox('63', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92513'">16/07 16:06</td>
                    <td style="" title="00:00:01" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92513'">00:00:01</td>
                                        <td style="" title="5561999763053" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92513'">5561999763053</td>
                    <td style="" title="551133855642" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92513'">551133855642</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92513'">Atendida</td>
                    <td style="" title="1131000441LifeSP5648" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92513'">1131000441LifeSP5648</td>
                    <td style="" title="Entrante" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92513'">Entrante</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92513'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378740" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_64" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_64" value="NjQ."
                                                      onclick="toggle_checkbox('64', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92514'">16/07 16:06</td>
                    <td style="" title="00:00:57" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92514'">00:00:57</td>
                                        <td style="" title="Ramal: ramal 1410" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92514'">1410</td>
                    <td style="" title="5521998715841" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92514'">5521998715841</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92514'">Atendida</td>
                    <td style="" title="1131000441LifeSP5640" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92514'">1131000441LifeSP5640</td>
                    <td style="" title="Celular Nacional" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92514'">Celular Nacional</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92514'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378740" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907161606091410552199871584115633039692399651563303969wav5d2f443471578');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378740" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907161606091410552199871584115633039692399651563303969wav5d2f443471578 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907161606091410552199871584115633039692399651563303969wav5d2f443471578">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-160609-1410-5521998715841-1563303969.239965-1563303969.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-160609-1410-5521998715841-1563303969.239965-1563303969.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907161606091410552199871584115633039692399651563303969wav5d2f443471578" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-160609-1410-5521998715841-1563303969.239965-1563303969.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378740" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-160609-1410-5521998715841-1563303969.239965-1563303969.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378740" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_65" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_65" value="NjU."
                                                      onclick="toggle_checkbox('65', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92512'">16/07 16:03</td>
                    <td style="" title="00:00:03" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92512'">00:00:03</td>
                                        <td style="" title="5511984343633" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92512'">5511984343633</td>
                    <td style="" title="Grupo: GP - Lifetime - 5633 » Ramal: ramal 1405 (1405)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92512'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_group.gif?1563378740" title="Grupo: GP - Lifetime - 5633" align="absmiddle" style="cursor: pointer;">  <img src="/pbxip/themes/phone2b/images/bullet_go_cf.gif?1563378740" title="Encaminhado" align="absmiddle"> 1405</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92512'">Atendida</td>
                    <td style="" title="1131000441LifeSP5648" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92512'">1131000441LifeSP5648</td>
                    <td style="" title="Entrante" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92512'">Entrante</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92512'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378740" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_2019071615633037862399401563303787wav5d2f443477b07');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378740" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_2019071615633037862399401563303787wav5d2f443477b07 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_2019071615633037862399401563303787wav5d2f443477b07">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-1563303786.239940-1563303787.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-1563303786.239940-1563303787.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_2019071615633037862399401563303787wav5d2f443477b07" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-1563303786.239940-1563303787.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378740" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-1563303786.239940-1563303787.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378740" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_66" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_66" value="NjY."
                                                      onclick="toggle_checkbox('66', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92511'">16/07 16:02</td>
                    <td style="" title="00:00:07" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92511'">00:00:07</td>
                                        <td style="" title="Ramal: Ramal 2810" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92511'">2810</td>
                    <td style="" title="5561999763053" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92511'">5561999763053</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92511'">Atendida</td>
                    <td style="" title="1131000441LifeSP5642" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92511'">1131000441LifeSP5642</td>
                    <td style="" title="Celular Nacional" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92511'">Celular Nacional</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92511'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378740" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907161602552810556199976305315633037752399361563303775wav5d2f44347c546');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378740" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907161602552810556199976305315633037752399361563303775wav5d2f44347c546 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907161602552810556199976305315633037752399361563303775wav5d2f44347c546">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-160255-2810-5561999763053-1563303775.239936-1563303775.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-160255-2810-5561999763053-1563303775.239936-1563303775.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907161602552810556199976305315633037752399361563303775wav5d2f44347c546" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-160255-2810-5561999763053-1563303775.239936-1563303775.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378740" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-160255-2810-5561999763053-1563303775.239936-1563303775.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378740" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_67" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_67" value="Njc."
                                                      onclick="toggle_checkbox('67', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #cc6600;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92510'">16/07 16:02</td>
                    <td style="color: #cc6600;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92510'">00:00:00</td>
                                        <td style="color: #cc6600;" title="Ramal: Ramal 9003" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92510'">9003</td>
                    <td style="color: #cc6600;" title="5511984343633" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92510'">5511984343633</td>
                    <td style="color: #cc6600;" title="Não Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92510'">Não Atendida</td>
                    <td style="color: #cc6600;" title="1131000441LifeSP5656" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92510'">1131000441LifeSP5656</td>
                    <td style="color: #cc6600;" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92510'">Celular Local</td>
                    <td style="color: #cc6600;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92510'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378740" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_68" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_68" value="Njg."
                                                      onclick="toggle_checkbox('68', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #cc6600;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92509'">16/07 16:02</td>
                    <td style="color: #cc6600;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92509'">00:00:00</td>
                                        <td style="color: #cc6600;" title="Ramal: Ramal 2810" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92509'">2810</td>
                    <td style="color: #cc6600;" title="5519981681010" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92509'">5519981681010</td>
                    <td style="color: #cc6600;" title="Não Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92509'">Não Atendida</td>
                    <td style="color: #cc6600;" title="1131000441LifeSP5642" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92509'">1131000441LifeSP5642</td>
                    <td style="color: #cc6600;" title="Celular Nacional" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92509'">Celular Nacional</td>
                    <td style="color: #cc6600;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92509'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378740" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_69" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_69" value="Njk."
                                                      onclick="toggle_checkbox('69', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92508'">16/07 16:00</td>
                    <td style="" title="00:00:06" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92508'">00:00:06</td>
                                        <td style="" title="551132019500" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92508'">551132019500</td>
                    <td style="" title="Ramal: Ramal 1406 (1406) » Ramal: ramal 1410 (1410)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92508'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1563378740" title="Ramal: Ramal 1406 (1406)" align="absmiddle" style="cursor: pointer;">  <img src="/pbxip/themes/phone2b/images/bullet_go_cf.gif?1563378740" title="Encaminhado" align="absmiddle"> 1410</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92508'">Atendida</td>
                    <td style="" title="1131000441LifeSP5648" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92508'">1131000441LifeSP5648</td>
                    <td style="" title="Entrante" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92508'">Entrante</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92508'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378740" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_20190716160052551132019500140615633036512399231563303652wav5d2f44348c147');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378740" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_20190716160052551132019500140615633036512399231563303652wav5d2f44348c147 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_20190716160052551132019500140615633036512399231563303652wav5d2f44348c147">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-160052-551132019500-1406-1563303651.239923-1563303652.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-160052-551132019500-1406-1563303651.239923-1563303652.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_20190716160052551132019500140615633036512399231563303652wav5d2f44348c147" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-160052-551132019500-1406-1563303651.239923-1563303652.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378740" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-160052-551132019500-1406-1563303651.239923-1563303652.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378740" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_70" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_70" value="NzA."
                                                      onclick="toggle_checkbox('70', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92507'">16/07 16:00</td>
                    <td style="" title="00:00:16" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92507'">00:00:16</td>
                                        <td style="" title="Ramal: Ramal 2208" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92507'">2208</td>
                    <td style="" title="Ramal: ramal 1609 (1609) » Ramal: ramal 1608 (1608)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92507'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1563378740" title="Ramal: ramal 1609 (1609)" align="absmiddle" style="cursor: pointer;">  <img src="/pbxip/themes/phone2b/images/bullet_go_cf.gif?1563378740" title="Encaminhado" align="absmiddle"> 1608</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92507'">Atendida</td>
                    <td style="" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92507'"></td>
                    <td style="" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92507'">Interno</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92507'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378740" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907161600292208160915633036292399191563303629wav5d2f4434949f9');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378740" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907161600292208160915633036292399191563303629wav5d2f4434949f9 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907161600292208160915633036292399191563303629wav5d2f4434949f9">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-160029-2208-1609-1563303629.239919-1563303629.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-160029-2208-1609-1563303629.239919-1563303629.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907161600292208160915633036292399191563303629wav5d2f4434949f9" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-160029-2208-1609-1563303629.239919-1563303629.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378740" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-160029-2208-1609-1563303629.239919-1563303629.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378740" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_71" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_71" value="NzE."
                                                      onclick="toggle_checkbox('71', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92506'">16/07 15:59</td>
                    <td style="" title="00:00:37" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92506'">00:00:37</td>
                                        <td style="" title="Ramal: Ramal 2810" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92506'">2810</td>
                    <td style="" title="5511996371788" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92506'">5511996371788</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92506'">Atendida</td>
                    <td style="" title="1131000441LifeSP5642" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92506'">1131000441LifeSP5642</td>
                    <td style="" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92506'">Celular Local</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92506'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378740" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_20190716155951281099637178815633035902399151563303591wav5d2f443499229');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378740" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_20190716155951281099637178815633035902399151563303591wav5d2f443499229 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_20190716155951281099637178815633035902399151563303591wav5d2f443499229">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-155951-2810-996371788-1563303590.239915-1563303591.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-155951-2810-996371788-1563303590.239915-1563303591.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_20190716155951281099637178815633035902399151563303591wav5d2f443499229" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-155951-2810-996371788-1563303590.239915-1563303591.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378740" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-155951-2810-996371788-1563303590.239915-1563303591.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378740" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_72" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_72" value="NzI."
                                                      onclick="toggle_checkbox('72', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #cc6600;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92504'">16/07 15:55</td>
                    <td style="color: #cc6600;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92504'">00:00:00</td>
                                        <td style="color: #cc6600;" title="Ramal: Ramal 2810" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92504'">2810</td>
                    <td style="color: #cc6600;" title="5511998822395" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92504'">5511998822395</td>
                    <td style="color: #cc6600;" title="Não Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92504'">Não Atendida</td>
                    <td style="color: #cc6600;" title="1131000441LifeSP5642" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92504'">1131000441LifeSP5642</td>
                    <td style="color: #cc6600;" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92504'">Celular Local</td>
                    <td style="color: #cc6600;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92504'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378740" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_73" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_73" value="NzM."
                                                      onclick="toggle_checkbox('73', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92505'">16/07 15:54</td>
                    <td style="" title="00:03:34" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92505'">00:03:34</td>
                                        <td style="" title="Ramal: Ramal 2206" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92505'">2206</td>
                    <td style="" title="Ramal: Ramal 1605 (1605)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92505'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1563378740" title="Ramal: Ramal 1605 (1605)" align="absmiddle" style="cursor: pointer;"> 1605</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92505'">Atendida</td>
                    <td style="" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92505'"></td>
                    <td style="" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92505'">Interno</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92505'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378740" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907161554402206160515633032052399041563303280wav5d2f4434a3846');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378740" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907161554402206160515633032052399041563303280wav5d2f4434a3846 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907161554402206160515633032052399041563303280wav5d2f4434a3846">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-155440-2206-1605-1563303205.239904-1563303280.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-155440-2206-1605-1563303205.239904-1563303280.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907161554402206160515633032052399041563303280wav5d2f4434a3846" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-155440-2206-1605-1563303205.239904-1563303280.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378740" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-155440-2206-1605-1563303205.239904-1563303280.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378740" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_74" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_74" value="NzQ."
                                                      onclick="toggle_checkbox('74', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92503'">16/07 15:53</td>
                    <td style="" title="00:04:48" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92503'">00:04:48</td>
                                        <td style="" title="Ramal: Ramal 2206" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92503'">2206</td>
                    <td style="" title="Ramal: ramal 1609 (1609) » Ramal: ramal 1603 (1603)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92503'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1563378740" title="Ramal: ramal 1609 (1609)" align="absmiddle" style="cursor: pointer;">  <img src="/pbxip/themes/phone2b/images/bullet_go_cf.gif?1563378740" title="Encaminhado" align="absmiddle"> 1603</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92503'">Atendida</td>
                    <td style="" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92503'"></td>
                    <td style="" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92503'">Interno</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92503'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378740" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907161553252206160915633032052399041563303205wav5d2f4434ac5d2');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378740" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907161553252206160915633032052399041563303205wav5d2f4434ac5d2 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907161553252206160915633032052399041563303205wav5d2f4434ac5d2">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-155325-2206-1609-1563303205.239904-1563303205.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-155325-2206-1609-1563303205.239904-1563303205.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907161553252206160915633032052399041563303205wav5d2f4434ac5d2" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-155325-2206-1609-1563303205.239904-1563303205.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378740" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-155325-2206-1609-1563303205.239904-1563303205.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378740" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_75" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_75" value="NzU."
                                                      onclick="toggle_checkbox('75', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92502'">16/07 15:53</td>
                    <td style="" title="00:00:27" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92502'">00:00:27</td>
                                        <td style="" title="551130853975" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92502'">551130853975</td>
                    <td style="" title="Grupo: GP - Lifetime - 5640 - Mesa » Ramal: ramal1401 (1401)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92502'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_group.gif?1563378740" title="Grupo: GP - Lifetime - 5640 - Mesa" align="absmiddle" style="cursor: pointer;">  <img src="/pbxip/themes/phone2b/images/bullet_go_cf.gif?1563378740" title="Encaminhado" align="absmiddle"> 1401</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92502'">Atendida</td>
                    <td style="" title="1131000441LifeSP5648" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92502'">1131000441LifeSP5648</td>
                    <td style="" title="Entrante" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92502'">Entrante</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92502'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378740" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_2019071615633031872398931563303188wav5d2f4434b2a82');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378740" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_2019071615633031872398931563303188wav5d2f4434b2a82 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_2019071615633031872398931563303188wav5d2f4434b2a82">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-1563303187.239893-1563303188.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-1563303187.239893-1563303188.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_2019071615633031872398931563303188wav5d2f4434b2a82" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-1563303187.239893-1563303188.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378740" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-1563303187.239893-1563303188.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378740" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_76" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_76" value="NzY."
                                                      onclick="toggle_checkbox('76', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #cc6600;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92501'">16/07 15:52</td>
                    <td style="color: #cc6600;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92501'">00:00:00</td>
                                        <td style="color: #cc6600;" title="Ramal: Ramal 2206" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92501'">2206</td>
                    <td style="color: #cc6600;" title="Ramal: ramal 1606 (1606)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92501'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1563378740" title="Ramal: ramal 1606 (1606)" align="absmiddle" style="cursor: pointer;"> 1606</td>
                    <td style="color: #cc6600;" title="Não Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92501'">Não Atendida</td>
                    <td style="color: #cc6600;" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92501'"></td>
                    <td style="color: #cc6600;" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92501'">Interno</td>
                    <td style="color: #cc6600;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92501'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378740" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_77" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_77" value="Nzc."
                                                      onclick="toggle_checkbox('77', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92499'">16/07 15:51</td>
                    <td style="" title="00:00:42" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92499'">00:00:42</td>
                                        <td style="" title="Ramal: Ramal 2810" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92499'">2810</td>
                    <td style="" title="5511940307282" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92499'">5511940307282</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92499'">Atendida</td>
                    <td style="" title="1131000441LifeSP5642" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92499'">1131000441LifeSP5642</td>
                    <td style="" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92499'">Celular Local</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92499'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378740" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_20190716155130281094030728215633030902398851563303090wav5d2f4434bde35');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378740" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_20190716155130281094030728215633030902398851563303090wav5d2f4434bde35 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_20190716155130281094030728215633030902398851563303090wav5d2f4434bde35">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-155130-2810-940307282-1563303090.239885-1563303090.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-155130-2810-940307282-1563303090.239885-1563303090.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_20190716155130281094030728215633030902398851563303090wav5d2f4434bde35" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-155130-2810-940307282-1563303090.239885-1563303090.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378740" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-155130-2810-940307282-1563303090.239885-1563303090.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378740" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_78" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_78" value="Nzg."
                                                      onclick="toggle_checkbox('78', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92500'">16/07 15:51</td>
                    <td style="" title="00:01:46" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92500'">00:01:46</td>
                                        <td style="" title="Ramal: ramal 2604" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92500'">2604</td>
                    <td style="" title="5511945013078" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92500'">5511945013078</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92500'">Atendida</td>
                    <td style="" title="1131000441LifeSP5651" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92500'">1131000441LifeSP5651</td>
                    <td style="" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92500'">Celular Local</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92500'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378740" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_20190716155105260494501307815633030652398811563303065wav5d2f4434c3036');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378740" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_20190716155105260494501307815633030652398811563303065wav5d2f4434c3036 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_20190716155105260494501307815633030652398811563303065wav5d2f4434c3036">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-155105-2604-945013078-1563303065.239881-1563303065.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-155105-2604-945013078-1563303065.239881-1563303065.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_20190716155105260494501307815633030652398811563303065wav5d2f4434c3036" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-155105-2604-945013078-1563303065.239881-1563303065.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378740" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-155105-2604-945013078-1563303065.239881-1563303065.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378740" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_79" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_79" value="Nzk."
                                                      onclick="toggle_checkbox('79', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92498'">16/07 15:49</td>
                    <td style="" title="00:01:40" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92498'">00:01:40</td>
                                        <td style="" title="Ramal: ramal 2604" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92498'">2604</td>
                    <td style="" title="5519998734429" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92498'">5519998734429</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92498'">Atendida</td>
                    <td style="" title="1131000441LifeSP5651" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92498'">1131000441LifeSP5651</td>
                    <td style="" title="Celular Nacional" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92498'">Celular Nacional</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92498'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378740" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907161549062604551999873442915633029462398771563302946wav5d2f4434c7e5c');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378740" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907161549062604551999873442915633029462398771563302946wav5d2f4434c7e5c divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907161549062604551999873442915633029462398771563302946wav5d2f4434c7e5c">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-154906-2604-5519998734429-1563302946.239877-1563302946.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-154906-2604-5519998734429-1563302946.239877-1563302946.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907161549062604551999873442915633029462398771563302946wav5d2f4434c7e5c" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-154906-2604-5519998734429-1563302946.239877-1563302946.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378740" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-154906-2604-5519998734429-1563302946.239877-1563302946.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378740" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_80" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_80" value="ODA."
                                                      onclick="toggle_checkbox('80', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #990000;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92497'">16/07 15:48</td>
                    <td style="color: #990000;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92497'">00:00:00</td>
                                        <td style="color: #990000;" title="Ramal: ramal 1609" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92497'">1609</td>
                    <td style="color: #990000;" title="Ramal: Ramal 2812 (2812)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92497'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1563378740" title="Ramal: Ramal 2812 (2812)" align="absmiddle" style="cursor: pointer;"> 2812</td>
                    <td style="color: #990000;" title="Falhou" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92497'">Falhou</td>
                    <td style="color: #990000;" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92497'"></td>
                    <td style="color: #990000;" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92497'">Interno</td>
                    <td style="color: #990000;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92497'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378740" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_81" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_81" value="ODE."
                                                      onclick="toggle_checkbox('81', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92496'">16/07 15:46</td>
                    <td style="" title="00:01:27" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92496'">00:01:27</td>
                                        <td style="" title="Ramal: ramal 9001" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92496'">9001</td>
                    <td style="" title="Ramal: ramal 1609 (1609)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92496'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1563378740" title="Ramal: ramal 1609 (1609)" align="absmiddle" style="cursor: pointer;"> 1609</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92496'">Atendida</td>
                    <td style="" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92496'"></td>
                    <td style="" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92496'">Interno</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92496'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378740" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907161546519001160915633027922398641563302811wav5d2f4434d41b3');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378740" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907161546519001160915633027922398641563302811wav5d2f4434d41b3 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907161546519001160915633027922398641563302811wav5d2f4434d41b3">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-154651-9001-1609-1563302792.239864-1563302811.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-154651-9001-1609-1563302792.239864-1563302811.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907161546519001160915633027922398641563302811wav5d2f4434d41b3" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-154651-9001-1609-1563302792.239864-1563302811.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378740" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-154651-9001-1609-1563302792.239864-1563302811.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378740" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_82" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_82" value="ODI."
                                                      onclick="toggle_checkbox('82', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92495'">16/07 15:46</td>
                    <td style="" title="00:00:03" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92495'">00:00:03</td>
                                        <td style="" title="Ramal: Ramal 2810" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92495'">2810</td>
                    <td style="" title="5511999714780" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92495'">5511999714780</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92495'">Atendida</td>
                    <td style="" title="1131000441LifeSP5642" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92495'">1131000441LifeSP5642</td>
                    <td style="" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92495'">Celular Local</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92495'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378740" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_20190716154642281099971478015633028022398671563302802wav5d2f4434d94a0');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378740" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_20190716154642281099971478015633028022398671563302802wav5d2f4434d94a0 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_20190716154642281099971478015633028022398671563302802wav5d2f4434d94a0">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-154642-2810-999714780-1563302802.239867-1563302802.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-154642-2810-999714780-1563302802.239867-1563302802.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_20190716154642281099971478015633028022398671563302802wav5d2f4434d94a0" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-154642-2810-999714780-1563302802.239867-1563302802.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378740" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-154642-2810-999714780-1563302802.239867-1563302802.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378740" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_83" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_83" value="ODM."
                                                      onclick="toggle_checkbox('83', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92493'">16/07 15:46</td>
                    <td style="" title="00:01:50" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92493'">00:01:50</td>
                                        <td style="" title="Ramal: ramal 9001" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92493'">9001</td>
                    <td style="" title="Ramal: Ramal 1605 (1605)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92493'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1563378740" title="Ramal: Ramal 1605 (1605)" align="absmiddle" style="cursor: pointer;"> 1605</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92493'">Atendida</td>
                    <td style="" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92493'"></td>
                    <td style="" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92493'">Interno</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92493'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378740" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907161546329001160515633027922398641563302792wav5d2f4434df178');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378740" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907161546329001160515633027922398641563302792wav5d2f4434df178 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907161546329001160515633027922398641563302792wav5d2f4434df178">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-154632-9001-1605-1563302792.239864-1563302792.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-154632-9001-1605-1563302792.239864-1563302792.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907161546329001160515633027922398641563302792wav5d2f4434df178" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-154632-9001-1605-1563302792.239864-1563302792.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378740" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-154632-9001-1605-1563302792.239864-1563302792.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378740" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_84" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_84" value="ODQ."
                                                      onclick="toggle_checkbox('84', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92494'">16/07 15:46</td>
                    <td style="" title="00:01:41" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92494'">00:01:41</td>
                                        <td style="" title="Ramal: ramal 2604" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92494'">2604</td>
                    <td style="" title="5511992671232" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92494'">5511992671232</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92494'">Atendida</td>
                    <td style="" title="1131000441LifeSP5651" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92494'">1131000441LifeSP5651</td>
                    <td style="" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92494'">Celular Local</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92494'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378740" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_20190716154605260499267123215633027642398601563302765wav5d2f4434e3f8e');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378740" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_20190716154605260499267123215633027642398601563302765wav5d2f4434e3f8e divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_20190716154605260499267123215633027642398601563302765wav5d2f4434e3f8e">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-154605-2604-992671232-1563302764.239860-1563302765.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-154605-2604-992671232-1563302764.239860-1563302765.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_20190716154605260499267123215633027642398601563302765wav5d2f4434e3f8e" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-154605-2604-992671232-1563302764.239860-1563302765.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378740" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-154605-2604-992671232-1563302764.239860-1563302765.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378740" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_85" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_85" value="ODU."
                                                      onclick="toggle_checkbox('85', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #cc6600;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92492'">16/07 15:45</td>
                    <td style="color: #cc6600;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92492'">00:00:00</td>
                                        <td style="color: #cc6600;" title="Ramal: Ramal 2810" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92492'">2810</td>
                    <td style="color: #cc6600;" title="5511958040446" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92492'">5511958040446</td>
                    <td style="color: #cc6600;" title="Não Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92492'">Não Atendida</td>
                    <td style="color: #cc6600;" title="1131000441LifeSP5642" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92492'">1131000441LifeSP5642</td>
                    <td style="color: #cc6600;" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92492'">Celular Local</td>
                    <td style="color: #cc6600;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92492'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378740" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_86" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_86" value="ODY."
                                                      onclick="toggle_checkbox('86', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92491'">16/07 15:45</td>
                    <td style="" title="00:00:30" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92491'">00:00:30</td>
                                        <td style="" title="Ramal: Ramal 2208" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92491'">2208</td>
                    <td style="" title="Ramal: ramal 1602 (1602)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92491'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1563378740" title="Ramal: ramal 1602 (1602)" align="absmiddle" style="cursor: pointer;"> 1602</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92491'">Atendida</td>
                    <td style="" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92491'"></td>
                    <td style="" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92491'">Interno</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92491'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378740" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907161545342208160215633027342398531563302734wav5d2f4434eef62');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378740" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907161545342208160215633027342398531563302734wav5d2f4434eef62 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907161545342208160215633027342398531563302734wav5d2f4434eef62">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-154534-2208-1602-1563302734.239853-1563302734.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-154534-2208-1602-1563302734.239853-1563302734.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907161545342208160215633027342398531563302734wav5d2f4434eef62" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-154534-2208-1602-1563302734.239853-1563302734.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378740" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-154534-2208-1602-1563302734.239853-1563302734.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378740" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_87" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_87" value="ODc."
                                                      onclick="toggle_checkbox('87', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #cc6600;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92490'">16/07 15:42</td>
                    <td style="color: #cc6600;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92490'">00:00:00</td>
                                        <td style="color: #cc6600;" title="Ramal: Ramal 2810" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92490'">2810</td>
                    <td style="color: #cc6600;" title="5511984607572" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92490'">5511984607572</td>
                    <td style="color: #cc6600;" title="Não Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92490'">Não Atendida</td>
                    <td style="color: #cc6600;" title="1131000441LifeSP5642" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92490'">1131000441LifeSP5642</td>
                    <td style="color: #cc6600;" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92490'">Celular Local</td>
                    <td style="color: #cc6600;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92490'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378740" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_88" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_88" value="ODg."
                                                      onclick="toggle_checkbox('88', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92489'">16/07 15:41</td>
                    <td style="" title="00:01:25" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92489'">00:01:25</td>
                                        <td style="" title="Ramal: ramal 2604" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92489'">2604</td>
                    <td style="" title="5511991887593" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92489'">5511991887593</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92489'">Atendida</td>
                    <td style="" title="1131000441LifeSP5651" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92489'">1131000441LifeSP5651</td>
                    <td style="" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92489'">Celular Local</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92489'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378741" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_20190716154144260499188759315633025042398441563302504wav5d2f443505132');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378741" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_20190716154144260499188759315633025042398441563302504wav5d2f443505132 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_20190716154144260499188759315633025042398441563302504wav5d2f443505132">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-154144-2604-991887593-1563302504.239844-1563302504.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-154144-2604-991887593-1563302504.239844-1563302504.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_20190716154144260499188759315633025042398441563302504wav5d2f443505132" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-154144-2604-991887593-1563302504.239844-1563302504.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378741" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-154144-2604-991887593-1563302504.239844-1563302504.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378741" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_89" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_89" value="ODk."
                                                      onclick="toggle_checkbox('89', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #990000;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92488'">16/07 15:41</td>
                    <td style="color: #990000;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92488'">00:00:00</td>
                                        <td style="color: #990000;" title="Ramal: ramal 1609" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92488'">1609</td>
                    <td style="color: #990000;" title="Ramal: Ramal 2812 (2812)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92488'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1563378741" title="Ramal: Ramal 2812 (2812)" align="absmiddle" style="cursor: pointer;"> 2812</td>
                    <td style="color: #990000;" title="Falhou" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92488'">Falhou</td>
                    <td style="color: #990000;" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92488'"></td>
                    <td style="color: #990000;" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92488'">Interno</td>
                    <td style="color: #990000;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92488'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378741" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_90" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_90" value="OTA."
                                                      onclick="toggle_checkbox('90', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #990000;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92487'">16/07 15:40</td>
                    <td style="color: #990000;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92487'">00:00:00</td>
                                        <td style="color: #990000;" title="Ramal: ramal 1609" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92487'">1609</td>
                    <td style="color: #990000;" title="Ramal: Ramal 2812 (2812)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92487'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1563378741" title="Ramal: Ramal 2812 (2812)" align="absmiddle" style="cursor: pointer;"> 2812</td>
                    <td style="color: #990000;" title="Falhou" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92487'">Falhou</td>
                    <td style="color: #990000;" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92487'"></td>
                    <td style="color: #990000;" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92487'">Interno</td>
                    <td style="color: #990000;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92487'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378741" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_91" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_91" value="OTE."
                                                      onclick="toggle_checkbox('91', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #cc6600;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92486'">16/07 15:40</td>
                    <td style="color: #cc6600;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92486'">00:00:00</td>
                                        <td style="color: #cc6600;" title="Ramal: Ramal 2810" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92486'">2810</td>
                    <td style="color: #cc6600;" title="5511989649897" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92486'">5511989649897</td>
                    <td style="color: #cc6600;" title="Não Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92486'">Não Atendida</td>
                    <td style="color: #cc6600;" title="1131000441LifeSP5642" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92486'">1131000441LifeSP5642</td>
                    <td style="color: #cc6600;" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92486'">Celular Local</td>
                    <td style="color: #cc6600;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92486'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378741" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_92" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_92" value="OTI."
                                                      onclick="toggle_checkbox('92', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #cc6600;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92485'">16/07 15:39</td>
                    <td style="color: #cc6600;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92485'">00:00:00</td>
                                        <td style="color: #cc6600;" title="Ramal: Ramal 2810" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92485'">2810</td>
                    <td style="color: #cc6600;" title="5511989679897" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92485'">5511989679897</td>
                    <td style="color: #cc6600;" title="Não Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92485'">Não Atendida</td>
                    <td style="color: #cc6600;" title="1131000441LifeSP5642" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92485'">1131000441LifeSP5642</td>
                    <td style="color: #cc6600;" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92485'">Celular Local</td>
                    <td style="color: #cc6600;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92485'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378741" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_93" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_93" value="OTM."
                                                      onclick="toggle_checkbox('93', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92484'">16/07 15:38</td>
                    <td style="" title="00:00:12" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92484'">00:00:12</td>
                                        <td style="" title="Ramal: Ramal 2810" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92484'">2810</td>
                    <td style="" title="5511989649897" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92484'">5511989649897</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92484'">Atendida</td>
                    <td style="" title="1131000441LifeSP5642" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92484'">1131000441LifeSP5642</td>
                    <td style="" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92484'">Celular Local</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92484'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378741" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_20190716153858281098964989715633023372398261563302338wav5d2f443520e85');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378741" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_20190716153858281098964989715633023372398261563302338wav5d2f443520e85 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_20190716153858281098964989715633023372398261563302338wav5d2f443520e85">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-153858-2810-989649897-1563302337.239826-1563302338.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-153858-2810-989649897-1563302337.239826-1563302338.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_20190716153858281098964989715633023372398261563302338wav5d2f443520e85" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-153858-2810-989649897-1563302337.239826-1563302338.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378741" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-153858-2810-989649897-1563302337.239826-1563302338.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378741" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_94" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_94" value="OTQ."
                                                      onclick="toggle_checkbox('94', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92483'">16/07 15:37</td>
                    <td style="" title="00:01:20" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92483'">00:01:20</td>
                                        <td style="" title="Ramal: ramal 2604" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92483'">2604</td>
                    <td style="" title="5511972872792" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92483'">5511972872792</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92483'">Atendida</td>
                    <td style="" title="1131000441LifeSP5651" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92483'">1131000441LifeSP5651</td>
                    <td style="" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92483'">Celular Local</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92483'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378741" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_20190716153738260497287279215633022582398211563302258wav5d2f4435231ac');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378741" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_20190716153738260497287279215633022582398211563302258wav5d2f4435231ac divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_20190716153738260497287279215633022582398211563302258wav5d2f4435231ac">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-153738-2604-972872792-1563302258.239821-1563302258.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-153738-2604-972872792-1563302258.239821-1563302258.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_20190716153738260497287279215633022582398211563302258wav5d2f4435231ac" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-153738-2604-972872792-1563302258.239821-1563302258.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378741" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-153738-2604-972872792-1563302258.239821-1563302258.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378741" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_95" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_95" value="OTU."
                                                      onclick="toggle_checkbox('95', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92482'">16/07 15:36</td>
                    <td style="" title="00:02:21" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92482'">00:02:21</td>
                                        <td style="" title="Ramal: Ramal 2812" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92482'">2812</td>
                    <td style="" title="Ramal: ramal 1609 (1609)" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92482'"> <img src="/pbxip/themes/phone2b/images/bullet_exten_users.gif?1563378741" title="Ramal: ramal 1609 (1609)" align="absmiddle" style="cursor: pointer;"> 1609</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92482'">Atendida</td>
                    <td style="" title="" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92482'"></td>
                    <td style="" title="Interno" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92482'">Interno</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92482'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378741" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907161536562812160915633022152398181563302216wav5d2f443528598');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378741" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907161536562812160915633022152398181563302216wav5d2f443528598 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907161536562812160915633022152398181563302216wav5d2f443528598">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-153656-2812-1609-1563302215.239818-1563302216.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-153656-2812-1609-1563302215.239818-1563302216.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907161536562812160915633022152398181563302216wav5d2f443528598" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-153656-2812-1609-1563302215.239818-1563302216.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378741" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-153656-2812-1609-1563302215.239818-1563302216.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378741" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_96" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_96" value="OTY."
                                                      onclick="toggle_checkbox('96', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92481'">16/07 15:36</td>
                    <td style="" title="00:00:33" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92481'">00:00:33</td>
                                        <td style="" title="Ramal: Ramal 2810" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92481'">2810</td>
                    <td style="" title="5511985682532" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92481'">5511985682532</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92481'">Atendida</td>
                    <td style="" title="1131000441LifeSP5642" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92481'">1131000441LifeSP5642</td>
                    <td style="" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92481'">Celular Local</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92481'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378741" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_20190716153649281098568253215633022082398141563302209wav5d2f44352d000');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378741" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_20190716153649281098568253215633022082398141563302209wav5d2f44352d000 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_20190716153649281098568253215633022082398141563302209wav5d2f44352d000">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-153649-2810-985682532-1563302208.239814-1563302209.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-153649-2810-985682532-1563302208.239814-1563302209.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_20190716153649281098568253215633022082398141563302209wav5d2f44352d000" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-153649-2810-985682532-1563302208.239814-1563302209.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378741" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-153649-2810-985682532-1563302208.239814-1563302209.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378741" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_97" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_97" value="OTc."
                                                      onclick="toggle_checkbox('97', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style="color: #cc6600;;"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92478'">16/07 15:35</td>
                    <td style="color: #cc6600;" title="00:00:00" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92478'">00:00:00</td>
                                        <td style="color: #cc6600;" title="Ramal: Ramal 7003" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92478'">7003</td>
                    <td style="color: #cc6600;" title="5567992334413" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92478'">5567992334413</td>
                    <td style="color: #cc6600;" title="Não Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92478'">Não Atendida</td>
                    <td style="color: #cc6600;" title="1131000441_Campo" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92478'">1131000441_Campo</td>
                    <td style="color: #cc6600;" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92478'">Celular Local</td>
                    <td style="color: #cc6600;" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92478'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378741" align="absmiddle"></td>
                                        </tbody>
                                        <tbody id="tr_98" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_98" value="OTg."
                                                      onclick="toggle_checkbox('98', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92480'">16/07 15:35</td>
                    <td style="" title="00:00:38" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92480'">00:00:38</td>
                                        <td style="" title="Ramal: Ramal 2810" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92480'">2810</td>
                    <td style="" title="5511981580308" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92480'">5511981580308</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92480'">Atendida</td>
                    <td style="" title="1131000441LifeSP5642" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92480'">1131000441LifeSP5642</td>
                    <td style="" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92480'">Celular Local</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92480'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378741" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_20190716153522281098158030815633021212398061563302122wav5d2f443536ff8');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378741" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_20190716153522281098158030815633021212398061563302122wav5d2f443536ff8 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_20190716153522281098158030815633021212398061563302122wav5d2f443536ff8">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-153522-2810-981580308-1563302121.239806-1563302122.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-153522-2810-981580308-1563302121.239806-1563302122.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_20190716153522281098158030815633021212398061563302122wav5d2f443536ff8" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-153522-2810-981580308-1563302121.239806-1563302122.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378741" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-153522-2810-981580308-1563302121.239806-1563302122.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378741" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_99" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_99" value="OTk."
                                                      onclick="toggle_checkbox('99', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92479'">16/07 15:35</td>
                    <td style="" title="00:01:31" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92479'">00:01:31</td>
                                        <td style="" title="Ramal: ramal 2604" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92479'">2604</td>
                    <td style="" title="5513992082112" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92479'">5513992082112</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92479'">Atendida</td>
                    <td style="" title="1131000441LifeSP5651" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92479'">1131000441LifeSP5651</td>
                    <td style="" title="Celular Nacional" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92479'">Celular Nacional</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92479'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378741" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_201907161535142604551399208211215633021142398021563302114wav5d2f44353ba62');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378741" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_201907161535142604551399208211215633021142398021563302114wav5d2f44353ba62 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_201907161535142604551399208211215633021142398021563302114wav5d2f44353ba62">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-153514-2604-5513992082112-1563302114.239802-1563302114.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-153514-2604-5513992082112-1563302114.239802-1563302114.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_201907161535142604551399208211215633021142398021563302114wav5d2f44353ba62" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-153514-2604-5513992082112-1563302114.239802-1563302114.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378741" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-153514-2604-5513992082112-1563302114.239802-1563302114.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378741" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                                        <tbody id="tr_100" class="malhado" onmouseover="on_hover_row(jQuery(this));">
                    <td style="display: none;"><input type="checkbox" class="checkbox" name="chk"
                                                      id="chk_100" value="MTAw"
                                                      onclick="toggle_checkbox('100', 'fifochkid', 'text', tdis.id);"/>
                    </td>
                    <td style=";"
                        title="Ver detalhamento da ligação"
                        nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92476'">16/07 15:33</td>
                    <td style="" title="00:00:03" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92476'">00:00:03</td>
                                        <td style="" title="Ramal: Ramal 2810" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92476'">2810</td>
                    <td style="" title="5511970282816" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92476'">5511970282816</td>
                    <td style="" title="Atendida" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92476'">Atendida</td>
                    <td style="" title="1131000441LifeSP5642" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92476'">1131000441LifeSP5642</td>
                    <td style="" title="Celular Local" nowrap
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92476'">Celular Local</td>
                    <td style="" title="" nowrap align="right"
                        ondblclick="document.location = '/pbxip/framework/container.php?token=MAIN/cmVwb3J0LmNhbGxzLmRldGFpbGVk|INCLUDE/aW5kZXgucmVwb3J0LmRldGFpbC5waHA.&id=92476'"></td>
                                            <td style="text-align: center;"><img src="/pbxip/themes/phone2b/images/spacer.gif?1563378741" align="absmiddle"><a href="javascript:void(0);" onClick="showDiv('div_20190716153315281097028281615633019942397981563301995wav5d2f443540875');" ><img src="/pbxip/themes/phone2b/images/bullet_service_monitor_on.gif?1563378741" title="Controles de áudio" align="absmiddle" style="cursor: pointer;margin:0 2px;"></a><div class='div_20190716153315281097028281615633019942397981563301995wav5d2f443540875 divs_audio' style='display:none;'><div style='float:left;'><OBJECT classid="clsid:02BF25D5-8C17-4B23-BC80-D3488ABDDC6B" codebase="http://www.apple.com/qtactivex/qtplugin.cab" width="100" height="10px" id="div_20190716153315281097028281615633019942397981563301995wav5d2f443540875">
                                    <PARAM name="src" value="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-153315-2810-970282816-1563301994.239798-1563301995.wav"><PARAM name="autoplay" value="false"><EMBED HEIGHT=20 WIDTH=100 AUTOPLAY="false" SRC="http://192.168.3.1/pbxip/core/includes/downloadaudio.php?file=/var/spool/asterisk/monitor/20190716-153315-2810-970282816-1563301994.239798-1563301995.wav" TYPE="video/quicktime" PLUGINSPAGE="www.apple.com/quicktime/download" EnableJavaScript="true" NAME="div_20190716153315281097028281615633019942397981563301995wav5d2f443540875" /></OBJECT></div><div style='float:left;'><a href="javascript:void(0);" onClick="downloadAudio('/var/spool/asterisk/monitor/20190716-153315-2810-970282816-1563301994.239798-1563301995.wav');"><img src="/pbxip/themes/phone2b/images/save.gif?1563378741" title="Salvar" alt="Salvar" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a><a href="javascript:void(0);" onClick="downloadAudioMp3('/var/spool/asterisk/monitor/20190716-153315-2810-970282816-1563301994.239798-1563301995.wav');"><img src="/pbxip/themes/pbxip/images/mp3-icon.png?1563378741" title="Salvar mp3" alt="Salvar mp3" align="absmiddle" style="cursor: pointer; margin-left:2px; margin-top:2px;"></a></div></div></td>
                                        </tbody>
                            <!--<thead>
    <td style="display: none;"></td>
    <td title="Total" nowrap><b>Total</b></td>
    <td title="Total de duração: 10412" nowrap>10412</td>
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
                                        <td title="37" nowrap>37</td>
                                                <td title="0" nowrap>0</td>
                                                <td title="0" nowrap>0</td>
                                                <td title="4" nowrap>4</td>
                                        <td title="41" nowrap>41</td>
                </tbody>
                                <tbody class="malhado" onmouseover="on_hover_row(jQuery(this));">
                <td title="Interno" nowrap>Interno</td>
                                        <td title="68" nowrap>68</td>
                                                <td title="0" nowrap>0</td>
                                                <td title="15" nowrap>15</td>
                                                <td title="6" nowrap>6</td>
                                        <td title="89" nowrap>89</td>
                </tbody>
                                <tbody class="malhado" onmouseover="on_hover_row(jQuery(this));">
                <td title="Saínte" nowrap>Saínte</td>
                                        <td title="81" nowrap>81</td>
                                                <td title="0" nowrap>0</td>
                                                <td title="35" nowrap>35</td>
                                                <td title="0" nowrap>0</td>
                                        <td title="116" nowrap>116</td>
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
        }'''

dx = re.findall(r'"[a-z]+[:.].*wav"', text)

#print(dx)
links_array = []
for link in dx:
    links_array.append(link.split('>')[0].replace('"',''))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                

print(links_array)


asession = ClientSession()
async def fetch(url_list):
    r = await asession.get(*url_list)
    return r.read()

    #async with asession.get(links_array) as resp:
        #print(resp.status)
        #print(await resp.text())

#agr = asyncio.run(fetch(links_array))

driver = webdriver.Chrome('chromedriver.exe')
driver.get("http://192.168.3.1/pbxip/framework/")

for link in links_array:
    driver.get(link)
