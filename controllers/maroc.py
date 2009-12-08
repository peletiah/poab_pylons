import logging

from poab.lib.base import *

log = logging.getLogger(__name__)

class MarocController(BaseController):

    def index(self):
        # Return a rendered template
        #   return render('/some/template.mako')
        # or, Return a response
	c.markerlist='''['''
	c.markerlist=c.markerlist + '''{'lat':31.019987, 'lon':-8.151855, 'text':"Tizi-n-Test", 'encpts':"wsa`Edwyo@vuCyeA~rFvzDxdU}wFf}^k}ApkV`cUnhHxdGhcT`dCfzGfmRhuIpwDfpNzzVzpHa]pdP|~I", 'enclvl':"BBBBBBBBBBBBB", 'color':"FF0000"},'''
	c.markerlist=c.markerlist + '''{'lat':30.424992973925598, 'lon':-8.6297607421875, 'text':"Igherm", 'encpts':"uwkzDt_pr@duWx`TloLxml@zdOi`]zfEglA~hAwfF|lOapJ|wA{wFjdc@{tA", 'enclvl':"BBBBBBBBB", 'color':"FF0000"},'''
	c.markerlist=c.markerlist + '''{'lat':29.933515040088093, 'lon':-8.128509521484375, 'text':"Tata", 'encpts':"amuvDdztr@p`_@_gaAptPgaK|sCi}Lv{Mw_C", 'enclvl':"BBBBB", 'color':"FF0000"},'''
	c.markerlist=c.markerlist + '''{'lat':29.729799972602223, 'lon':-8.47869873046875, 'text':"Hohle Gasse", 'encpts':"}gptD~cto@dJhqEf_DlTz_Bfd[dxH`eTyeAprc@qsEhhCmsE|i@ynBvdGjpCdwBh~@tjDlkGrcAwk@`zFggNrwP{_B|eMdJzpCbnD`iG?dlLc|A~qIfbFzK", 'enclvl':"BBBBBBBBBBBBBBBBBBBB", 'color':"FF0000"},'''
	c.markerlist=c.markerlist + '''{'lat':29.7298, 'lon':-9.16946, 'text':"Achterbahn", 'encpts':"kzktDvpwu@gbFcApz@bkRnFxsGhgBpkIegH|i@kcH|pCesJvXexKslCg`WguC", 'enclvl':"BBBBBBBBBB", 'color':"FF0000"},'''
	c.markerlist=c.markerlist + '''{'lat':29.563901551414418, 'lon':-8.89823913574218, 'text':"Option Tafraoute - Afella Ighir", 'encpts':"o`ptDtc_u@rkLnTndLre@v{CmiIztHc{@pwE`bDeaLt_N{oLvdGuvGv_CugG~eB", 'enclvl':"BBBBBBBBBB", 'color':"00FF00"},'''
	c.markerlist=c.markerlist + '''{'lat':30.47589937936957, 'lon':-8.881072998046875, 'text':"Tafraoute - Taroudant - Argana", 'encpts':"mmpvDzn{v@i}Fp}MomHbAcn|@{|cAmnNoyCadFtrX`J`nVise@nwD", 'enclvl':"BBBBBBBB", 'color':"FF0000"},'''
	c.markerlist=c.markerlist + '''{'lat':30.95759091468353, 'lon':-8.6297607421875, 'text':"Argana - Amizmiz - Marrakech", 'encpts':"cg|zDlrwv@ubRyq_@m`J}uu@mbLyhh@a|S{aZ}qQ_iR_tnAuzl@", 'enclvl':"BBBBBBB", 'color':"00FF00"},'''
	c.markerlist=c.markerlist + '''{'lat':31.169334787357972, 'lon':-8.84124755859375, 'text':"Argana - Imi-n-Tanoute - Marrakech", 'encpts':"cg|zDlrwv@ozZ_yLa}a@gaKsuJk|^qwb@kb_Ayz`@yae@dsEe}W_~Yox`@", 'enclvl':"BBBBBBBB", 'color':"00FF00"},'''
        c.markerlist=c.markerlist + '''];'''
   	return render("/track/maroc.html")
