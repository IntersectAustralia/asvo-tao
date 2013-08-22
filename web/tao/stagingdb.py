#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file has been automatically generated.
# Instead of changing it, create a file called import_helper.py
# which this script has hooks to.
#
# On that file, don't forget to add the necessary Django imports
# and take a look at how locate_object() and save_or_locate()
# are implemented here and expected to behave.
#
# This file was generated with the following command:
# /home/alistair/python/tao/bin/manage.py dumpscript tao
#
# to restore it, run
# manage.py runscript module_name.this_script_name
#
# example: if manage.py is at ./manage.py
# and the script is at ./some_folder/some_script.py
# you must make sure ./some_folder/__init__.py exists
# and run  ./manage.py runscript some_folder.some_script


IMPORT_HELPER_AVAILABLE = False
try:
    import import_helper
    IMPORT_HELPER_AVAILABLE = True
except ImportError:
    pass

import datetime
from decimal import Decimal
from django.contrib.contenttypes.models import ContentType
# Import pytz, if it isn't available, assume tzinfo isn't important
try:
    import pytz
except ImportError:
    pass

def run():
    #initial imports

    def locate_object(original_class, original_pk_name, the_class, pk_name, pk_value, obj_content):
        #You may change this function to do specific lookup for specific objects
        #
        #original_class class of the django orm's object that needs to be located
        #original_pk_name the primary key of original_class
        #the_class      parent class of original_class which contains obj_content
        #pk_name        the primary key of original_class
        #pk_value       value of the primary_key
        #obj_content    content of the object which was not exported.
        #
        #you should use obj_content to locate the object on the target db
        #
        #and example where original_class and the_class are different is
        #when original_class is Farmer and
        #the_class is Person. The table may refer to a Farmer but you will actually
        #need to locate Person in order to instantiate that Farmer
        #
        #example:
        #if the_class == SurveyResultFormat or the_class == SurveyType or the_class == SurveyState:
        #    pk_name="name"
        #    pk_value=obj_content[pk_name]
        #if the_class == StaffGroup:
        #    pk_value=8


        if IMPORT_HELPER_AVAILABLE and hasattr(import_helper, "locate_object"):
            return import_helper.locate_object(original_class, original_pk_name, the_class, pk_name, pk_value, obj_content)

        search_data = { pk_name: pk_value }
        the_obj =the_class.objects.get(**search_data)
        return the_obj

    def save_or_locate(the_obj):
        if IMPORT_HELPER_AVAILABLE and hasattr(import_helper, "save_or_locate"):
            the_obj = import_helper.save_or_locate(the_obj)
        else:
            the_obj.save()
        return the_obj



    #Processing model: Simulation

    from tao.models import Simulation

    tao_simulation_1 = Simulation()
    tao_simulation_1.name = u'Bolshoi'
    tao_simulation_1.box_size_units = u'Mpc/h'
    tao_simulation_1.box_size = Decimal('250.000')
    tao_simulation_1.details = u'<p>Cosmology: WMAP5<br/>\r\nCosmological parameters: = 0.25, = 0.75, = 0.0469, = 0.82, h = 0.73, n=0.95<br/>\r\nBox Size: 250 Mpc/h<br/>\r\nMass resolution: 1.35x10^8 Msun/h<br/>\r\nForce resolution: 1 Mpc/h\r\n</p>\r\n\r\n<p>Web Site: <a href="http://hipacc.ucsc.edu/Bolshoi/">Bolshoi Cosmological Simulations</a><br/>\r\nPaper: <a href="http://arxiv.org/abs/1002.3660">Klypin, Trujillo-Gomez & Primack 2011</a>\r\n</p>'
    tao_simulation_1.order = 3L
    tao_simulation_1 = save_or_locate(tao_simulation_1)

    tao_simulation_2 = Simulation()
    tao_simulation_2.name = u'Millennium'
    tao_simulation_2.box_size_units = u'Mpc/h'
    tao_simulation_2.box_size = Decimal('500.000')
    tao_simulation_2.details = u'<p>\r\nCosmology: WMAP-1<br/>\r\nCosmological parameters:  = 0.25,  = 0.75,  = 0.045,  = 0.9, h = 0.73, n = 1<br/>\r\nBox size: 500 Mpc/h<br/>\r\nMass resolution: 8.6x10^8 Msun/h<br/>\r\nForce resolution: 5 Mpc/h\r\n</p>\r\n<p>Paper: <a href="http://arxiv.org/abs/astro-ph/0504097">Springel et al. 2005</a><br/>\r\nExternal Link: <a href="http://www.mpa-garching.mpg.de/galform/millennium/">Simulating the joint evolution of quasars, galaxies and their large-scale distribution</a>\r\nWeb site: <a href="http://www.mpa-garching.mpg.de/millennium/">Public release of a VO-oriented and SQL-queryable database for studying the evolution of galaxies in the LCDM cosmogony</a>\r\n</p>'
    tao_simulation_2.order = 0L
    tao_simulation_2 = save_or_locate(tao_simulation_2)

    tao_simulation_3 = Simulation()
    tao_simulation_3.name = u'Mini-Millennium'
    tao_simulation_3.box_size_units = u'Mpc/h'
    tao_simulation_3.box_size = Decimal('62.500')
    tao_simulation_3.details = u'<p>\r\nCosmology: WMAP-1<br/>\r\nCosmological parameters: ,  = 0.75,  = 0.045,  = 0.9, h = 0.73, n = 1<br/>\r\nBox size: 62.5 Mpc/h<br/>\r\nMass resolution: 8.6x10^8 Msun/h<br/>\r\nForce resolution: 5 Mpc/h\r\n</p>\r\n\r\n<p>Paper: <a href="http://arxiv.org/abs/astro-ph/0504097">Springel et al. 2005</a><br/>\r\nExternal Link: <a href="http://www.mpa-garching.mpg.de/galform/millennium/">Simulating the joint evolution of quasars, galaxies and their large-scale distribution</a>\r\nWeb site: <a href="http://www.mpa-garching.mpg.de/millennium/">Public release of a VO-oriented and SQL-queryable database for studying the evolution of galaxies in the LCDM cosmogony</a>\r\n</p>'
    tao_simulation_3.order = 0L
    tao_simulation_3 = save_or_locate(tao_simulation_3)

    #Processing model: GalaxyModel

    from tao.models import GalaxyModel

    tao_galaxymodel_1 = GalaxyModel()
    tao_galaxymodel_1.name = u'SAGE'
    tao_galaxymodel_1.details = u'Kind: semi-analytic model<br/>\r\nPaper: <a href="http://arxiv.org/abs/astro-ph/0602065">Croton et al. 2006</a>'
    tao_galaxymodel_1 = save_or_locate(tao_galaxymodel_1)

    #Processing model: StellarModel

    from tao.models import StellarModel

    tao_stellarmodel_1 = StellarModel()
    tao_stellarmodel_1.name = u'ssp.ssz'
    tao_stellarmodel_1.label = u'Maraston 2005'
    tao_stellarmodel_1.description = u'<p>Web Site: <a href="http://www.icg.port.ac.uk/~maraston/Claudia%27s_Stellar_Population_Model.html">Claudia\'s Stellar Population Model</a></p>\r\n<ul>\r\n<li>h = 0.73</li>\r\n<li>Magnitudes are calculated in the AB system</li>\r\n</ul>\r\n<p>Additional information is available from the <a href="../static/docs/user-manual/sed.html">SED Module documentation</a>.</p>'
    tao_stellarmodel_1 = save_or_locate(tao_stellarmodel_1)

    #Processing model: BandPassFilter

    from tao.models import BandPassFilter

    tao_bandpassfilter_1 = BandPassFilter()
    tao_bandpassfilter_1.label = u'2MASS H'
    tao_bandpassfilter_1.filter_id = u'2MASS/Hband_2mass.dati'
    tao_bandpassfilter_1.description = u'<p>2 Micron All Sky Survey (2MASS) H</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/2MASS_Hband_2mass.dati.html">2MASS H</a>.</p>'
    tao_bandpassfilter_1.group = u''
    tao_bandpassfilter_1.order = 0L
    tao_bandpassfilter_1 = save_or_locate(tao_bandpassfilter_1)

    tao_bandpassfilter_2 = BandPassFilter()
    tao_bandpassfilter_2.label = u'2MASS Ks'
    tao_bandpassfilter_2.filter_id = u'2MASS/Ksband_2mass.dati'
    tao_bandpassfilter_2.description = u'<p>2 Micron All Sky Survey (2MASS) Ks</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/2MASS_Ksband_2mass.dati.html">2MASS Ks</a>.</p>'
    tao_bandpassfilter_2.group = u''
    tao_bandpassfilter_2.order = 0L
    tao_bandpassfilter_2 = save_or_locate(tao_bandpassfilter_2)

    tao_bandpassfilter_3 = BandPassFilter()
    tao_bandpassfilter_3.label = u"CFHTLS Megacam g'"
    tao_bandpassfilter_3.filter_id = u'CFHTLS/gMega.dati'
    tao_bandpassfilter_3.description = u'<p>Canada France Hawaii Telescope (CFHTLS/Megacam), g\' band</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/CFHTLS_gMega.dati.html">CFHTLS Megacam g\'</a>.</p>'
    tao_bandpassfilter_3.group = u''
    tao_bandpassfilter_3.order = 0L
    tao_bandpassfilter_3 = save_or_locate(tao_bandpassfilter_3)

    tao_bandpassfilter_4 = BandPassFilter()
    tao_bandpassfilter_4.label = u"CFHTLS Megacam i'"
    tao_bandpassfilter_4.filter_id = u'CFHTLS/i2Mega_new.dati'
    tao_bandpassfilter_4.description = u'<p>Canada France Hawaii Telescope (CFHTLS/Megacam), i\' band</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/CFHTLS_i2Mega_new.dati.html">CFHTLS Megacam i\'</a>.</p>'
    tao_bandpassfilter_4.group = u''
    tao_bandpassfilter_4.order = 0L
    tao_bandpassfilter_4 = save_or_locate(tao_bandpassfilter_4)

    tao_bandpassfilter_5 = BandPassFilter()
    tao_bandpassfilter_5.label = u"CFHTLS Megacam r'"
    tao_bandpassfilter_5.filter_id = u'CFHTLS/rMega.dati'
    tao_bandpassfilter_5.description = u'<p>Canada France Hawaii Telescope (CFHTLS/Megacam), r\' band</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/CFHTLS_rMega.dati.html">CFHTLS Megacam r\'</a>.</p>'
    tao_bandpassfilter_5.group = u''
    tao_bandpassfilter_5.order = 0L
    tao_bandpassfilter_5 = save_or_locate(tao_bandpassfilter_5)

    tao_bandpassfilter_6 = BandPassFilter()
    tao_bandpassfilter_6.label = u'CFHTLS Megacam u*'
    tao_bandpassfilter_6.filter_id = u'CFHTLS/uMega.dati'
    tao_bandpassfilter_6.description = u'<p>Canada France Hawaii Telescope (CFHTLS/Megacam), u* band</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/CFHTLS_uMega.dati.html">CFHTLS Megacam u*</a>.</p>'
    tao_bandpassfilter_6.group = u''
    tao_bandpassfilter_6.order = 0L
    tao_bandpassfilter_6 = save_or_locate(tao_bandpassfilter_6)

    tao_bandpassfilter_7 = BandPassFilter()
    tao_bandpassfilter_7.label = u"CFHTLS Megacam z'"
    tao_bandpassfilter_7.filter_id = u'CFHTLS/zMega.dati'
    tao_bandpassfilter_7.description = u'<p>Canada France Hawaii Telescope (CFHTLS/Megacam), z\' band</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/CFHTLS_zMega.dati.html">CFHTLS Megacam z\'</a>.</p>'
    tao_bandpassfilter_7.group = u''
    tao_bandpassfilter_7.order = 0L
    tao_bandpassfilter_7 = save_or_locate(tao_bandpassfilter_7)

    tao_bandpassfilter_8 = BandPassFilter()
    tao_bandpassfilter_8.label = u'GALEX FUV'
    tao_bandpassfilter_8.filter_id = u'GALEX/galex_FUV.dati'
    tao_bandpassfilter_8.description = u'<p>Galaxy Evolution Explorer (GALEX), far-UV</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/GALEX_galex_FUV.dati.html">GALEX FUV</a>.</p>'
    tao_bandpassfilter_8.group = u''
    tao_bandpassfilter_8.order = 0L
    tao_bandpassfilter_8 = save_or_locate(tao_bandpassfilter_8)

    tao_bandpassfilter_9 = BandPassFilter()
    tao_bandpassfilter_9.label = u'GALEX NUV'
    tao_bandpassfilter_9.filter_id = u'GALEX/galex_NUV.dati'
    tao_bandpassfilter_9.description = u'<p>Galaxy Evolution  Explorer (GALEX), near-UV</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/GALEX_galex_NUV.dati.html">GALEX NUV</a>.</p>'
    tao_bandpassfilter_9.group = u''
    tao_bandpassfilter_9.order = 0L
    tao_bandpassfilter_9 = save_or_locate(tao_bandpassfilter_9)

    tao_bandpassfilter_10 = BandPassFilter()
    tao_bandpassfilter_10.label = u'HST/ACS/WFC1 B'
    tao_bandpassfilter_10.filter_id = u'ACS/f435w.WFC1.dati'
    tao_bandpassfilter_10.description = u'<p>Hubble Space Telescope Advanced Camera for Surveys, Wide Field Camera 1 (HST/ACS, WFC1), B band (F435W)</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/ACS_f435w.WFC1.dati.html">HST/ACS/WFC1 B</a>.</p>'
    tao_bandpassfilter_10.group = u''
    tao_bandpassfilter_10.order = 0L
    tao_bandpassfilter_10 = save_or_locate(tao_bandpassfilter_10)

    tao_bandpassfilter_11 = BandPassFilter()
    tao_bandpassfilter_11.label = u'HST/ACS/WFC1 i'
    tao_bandpassfilter_11.filter_id = u'ACS/f775w.WFC1.dati'
    tao_bandpassfilter_11.description = u'<p>Hubble Space Telescope Advanced Camera for Surveys, Wide Field Camera 1 (HST/ACS, WFC1), i band (F775W)</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/ACS_f775w.WFC1.dati.html">HST/ACS/WFC1 i</a>.</p>'
    tao_bandpassfilter_11.group = u''
    tao_bandpassfilter_11.order = 0L
    tao_bandpassfilter_11 = save_or_locate(tao_bandpassfilter_11)

    tao_bandpassfilter_12 = BandPassFilter()
    tao_bandpassfilter_12.label = u'HST/ACS/WFC1 V'
    tao_bandpassfilter_12.filter_id = u'ACS/f606w.WFC1.dati'
    tao_bandpassfilter_12.description = u'<p>Hubble Space Telescope Advanced Camera for Surveys, Wide Field Camera 1 (HST/ACS, WFC1), V band (F606W)</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/ACS_f606w.WFC1.dati.html">HST/ACS/WFC1 V</a>.</p>'
    tao_bandpassfilter_12.group = u''
    tao_bandpassfilter_12.order = 0L
    tao_bandpassfilter_12 = save_or_locate(tao_bandpassfilter_12)

    tao_bandpassfilter_13 = BandPassFilter()
    tao_bandpassfilter_13.label = u'HST/ACS/WFC1 z'
    tao_bandpassfilter_13.filter_id = u'ACS/f850lp.WFC1.dati'
    tao_bandpassfilter_13.description = u'<p>Hubble Space Telescope Advanced Camera for Surveys, Wide Field Camera 1 (HST/ACS, WFC1), z band (F850LP)</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/ACS_f850lp.WFC1.dati.html">HST/ACS/WFC1 z</a>.</p>'
    tao_bandpassfilter_13.group = u''
    tao_bandpassfilter_13.order = 0L
    tao_bandpassfilter_13 = save_or_locate(tao_bandpassfilter_13)

    tao_bandpassfilter_14 = BandPassFilter()
    tao_bandpassfilter_14.label = u'HST/ACS/WFC2 B'
    tao_bandpassfilter_14.filter_id = u'ACS/f435w.WFC2.dati'
    tao_bandpassfilter_14.description = u'<p>Hubble Space Telescope Advanced Camera for Surveys, Wide Field Camera 2 (HST/ACS, WFC2), B band (F435W)</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/ACS_f435w.WFC2.dati.html">HST/ACS/WFC2 B</a>.</p>'
    tao_bandpassfilter_14.group = u''
    tao_bandpassfilter_14.order = 0L
    tao_bandpassfilter_14 = save_or_locate(tao_bandpassfilter_14)

    tao_bandpassfilter_15 = BandPassFilter()
    tao_bandpassfilter_15.label = u'HST/ACS/WFC2 i'
    tao_bandpassfilter_15.filter_id = u'ACS/f775w.WFC2.dati'
    tao_bandpassfilter_15.description = u'<p>Hubble Space Telescope Advanced Camera for Surveys, Wide Field Camera 2 (HST/ACS, WFC2), i band (F775W)</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/ACS_f775w.WFC2.dati.html">HST/ACS/WFC2 i</a>.</p>'
    tao_bandpassfilter_15.group = u''
    tao_bandpassfilter_15.order = 0L
    tao_bandpassfilter_15 = save_or_locate(tao_bandpassfilter_15)

    tao_bandpassfilter_16 = BandPassFilter()
    tao_bandpassfilter_16.label = u'HST/ACS/WFC2 V'
    tao_bandpassfilter_16.filter_id = u'ACS/f606w.WFC2.dati'
    tao_bandpassfilter_16.description = u'<p>Hubble Space Telescope Advanced Camera for Surveys, Wide Field Camera 2 (HST/ACS, WFC2), V band (F606W)</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/ACS_f606w.WFC2.dati.html">HST/ACS/WFC2 V</a>.</p>'
    tao_bandpassfilter_16.group = u''
    tao_bandpassfilter_16.order = 0L
    tao_bandpassfilter_16 = save_or_locate(tao_bandpassfilter_16)

    tao_bandpassfilter_17 = BandPassFilter()
    tao_bandpassfilter_17.label = u'HST/ACS/WFC2 z'
    tao_bandpassfilter_17.filter_id = u'ACS/f850lp.WFC2.dati'
    tao_bandpassfilter_17.description = u'<p>Hubble Space Telescope Advanced Camera for Surveys, Wide Field Camera 2 (HST/ACS, WFC2), z band (F850LP)</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/ACS_f850lp.WFC2.dati.html">HST/ACS/WFC2 z</a>.</p>'
    tao_bandpassfilter_17.group = u''
    tao_bandpassfilter_17.order = 0L
    tao_bandpassfilter_17 = save_or_locate(tao_bandpassfilter_17)

    tao_bandpassfilter_18 = BandPassFilter()
    tao_bandpassfilter_18.label = u'HST/Herschel/PACS 100'
    tao_bandpassfilter_18.filter_id = u'PACS/pacs100.dati'
    tao_bandpassfilter_18.description = u'<p>Hubble Space Telescope, Herschel/PACS, 100 micron</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/PACS_pacs100.dati.html">HST/Herschel/PACS 100</a>.</p>'
    tao_bandpassfilter_18.group = u''
    tao_bandpassfilter_18.order = 0L
    tao_bandpassfilter_18 = save_or_locate(tao_bandpassfilter_18)

    tao_bandpassfilter_19 = BandPassFilter()
    tao_bandpassfilter_19.label = u'HST/Herschel/PACS 160'
    tao_bandpassfilter_19.filter_id = u'PACS/pacs160.dati'
    tao_bandpassfilter_19.description = u'<p>Hubble Space Telescope, Herschel/PACS, 160 micron</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/PACS_pacs160.dati.html">HST/Herschel/PACS 160</a>.</p>'
    tao_bandpassfilter_19.group = u''
    tao_bandpassfilter_19.order = 0L
    tao_bandpassfilter_19 = save_or_locate(tao_bandpassfilter_19)

    tao_bandpassfilter_20 = BandPassFilter()
    tao_bandpassfilter_20.label = u'HST/Herschel/PACS 70'
    tao_bandpassfilter_20.filter_id = u'PACS/pacs70.dati'
    tao_bandpassfilter_20.description = u'<p>Hubble Space Telescope, Herschel/PACS, 70 micron</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/PACS_pacs70.dati.html">HST/Herschel/PACS 70</a>.</p>'
    tao_bandpassfilter_20.group = u''
    tao_bandpassfilter_20.order = 0L
    tao_bandpassfilter_20 = save_or_locate(tao_bandpassfilter_20)

    tao_bandpassfilter_21 = BandPassFilter()
    tao_bandpassfilter_21.label = u'HST/Herschel/SPIRE 250'
    tao_bandpassfilter_21.filter_id = u'SPIRE/spire250.dati'
    tao_bandpassfilter_21.description = u'<p>Hubble Space Telescope, Herschel/SPIRE, 250 micron</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/SPIRE_spire250.dati.html">HST/Herschel/SPIRE 250</a>.</p>'
    tao_bandpassfilter_21.group = u''
    tao_bandpassfilter_21.order = 0L
    tao_bandpassfilter_21 = save_or_locate(tao_bandpassfilter_21)

    tao_bandpassfilter_22 = BandPassFilter()
    tao_bandpassfilter_22.label = u'HST/Herschel/SPIRE 350'
    tao_bandpassfilter_22.filter_id = u'SPIRE/spire350.dati'
    tao_bandpassfilter_22.description = u'<p>Hubble Space Telescope, Herschel/SPIRE, 350 micron</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/SPIRE_spire350.dati.html">HST/Herschel/SPIRE 350</a>.</p>'
    tao_bandpassfilter_22.group = u''
    tao_bandpassfilter_22.order = 0L
    tao_bandpassfilter_22 = save_or_locate(tao_bandpassfilter_22)

    tao_bandpassfilter_23 = BandPassFilter()
    tao_bandpassfilter_23.label = u'HST/Herschel/SPIRE 500'
    tao_bandpassfilter_23.filter_id = u'SPIRE/spire500.dati'
    tao_bandpassfilter_23.description = u'<p>Hubble Space Telescope, Herschel/SPIRE, 500 micron</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/SPIRE_spire500.dati.html">HST/Herschel/SPIRE 500</a>.</p>'
    tao_bandpassfilter_23.group = u''
    tao_bandpassfilter_23.order = 0L
    tao_bandpassfilter_23 = save_or_locate(tao_bandpassfilter_23)

    tao_bandpassfilter_24 = BandPassFilter()
    tao_bandpassfilter_24.label = u'HST/Spitzer IRAC1'
    tao_bandpassfilter_24.filter_id = u'IRAC/irac_3.4.dati'
    tao_bandpassfilter_24.description = u'<p>Hubble Space Telescope, Spitzer/IRAC, ch1 (3.4 micron)</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/IRAC_irac_3.4.dati.html">HST/Spitzer IRAC1</a>.</p>'
    tao_bandpassfilter_24.group = u''
    tao_bandpassfilter_24.order = 0L
    tao_bandpassfilter_24 = save_or_locate(tao_bandpassfilter_24)

    tao_bandpassfilter_25 = BandPassFilter()
    tao_bandpassfilter_25.label = u'HST/Spitzer IRAC2'
    tao_bandpassfilter_25.filter_id = u'IRAC/irac_4.5.dati'
    tao_bandpassfilter_25.description = u'<p>Hubble Space Telescope, Spitzer/IRAC, ch2 (4.5 micron)</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/IRAC_irac_4.5.dati.html">HST/Spitzer IRAC2</a>.</p>'
    tao_bandpassfilter_25.group = u''
    tao_bandpassfilter_25.order = 0L
    tao_bandpassfilter_25 = save_or_locate(tao_bandpassfilter_25)

    tao_bandpassfilter_26 = BandPassFilter()
    tao_bandpassfilter_26.label = u'HST/Spitzer IRAC3'
    tao_bandpassfilter_26.filter_id = u'IRAC/irac_5.8.dati'
    tao_bandpassfilter_26.description = u'<p>Hubble Space Telescope, Spitzer/IRAC, ch3 (5.8 micron)</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/IRAC_irac_5.8.dati.html">HST/Spitzer IRAC3</a>.</p>'
    tao_bandpassfilter_26.group = u''
    tao_bandpassfilter_26.order = 0L
    tao_bandpassfilter_26 = save_or_locate(tao_bandpassfilter_26)

    tao_bandpassfilter_27 = BandPassFilter()
    tao_bandpassfilter_27.label = u'HST/Spitzer IRAC4'
    tao_bandpassfilter_27.filter_id = u'IRAC/irac_8.0.dati'
    tao_bandpassfilter_27.description = u'<p>Hubble Space Telescope, Spitzer/IRAC, ch4 (8.0 micron)</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/IRAC_irac_8.0.dati.html">HST/Spitzer IRAC4</a>.</p>'
    tao_bandpassfilter_27.group = u''
    tao_bandpassfilter_27.order = 0L
    tao_bandpassfilter_27 = save_or_locate(tao_bandpassfilter_27)

    tao_bandpassfilter_28 = BandPassFilter()
    tao_bandpassfilter_28.label = u'HST/Spitzer/MIPS 24'
    tao_bandpassfilter_28.filter_id = u'MIPS/mips_24.dati'
    tao_bandpassfilter_28.description = u'<p>Hubble Space Telescope, Spitzer/MIPS, 24 micron</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/MIPS_mips_24.dati.html">HST/Spitzer/MIPS 24</a>.</p>'
    tao_bandpassfilter_28.group = u''
    tao_bandpassfilter_28.order = 0L
    tao_bandpassfilter_28 = save_or_locate(tao_bandpassfilter_28)

    tao_bandpassfilter_29 = BandPassFilter()
    tao_bandpassfilter_29.label = u'HST/WFC3/IR F0.98M'
    tao_bandpassfilter_29.filter_id = u'WFC3/f098m.IR.dati'
    tao_bandpassfilter_29.description = u'<p>Hubble Space Telescope, WFC3/IR, F0.98M</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/WFC3_f098m.IR.dati.html">HST/WFC3/IR F0.98M</a>.</p>'
    tao_bandpassfilter_29.group = u''
    tao_bandpassfilter_29.order = 0L
    tao_bandpassfilter_29 = save_or_locate(tao_bandpassfilter_29)

    tao_bandpassfilter_30 = BandPassFilter()
    tao_bandpassfilter_30.label = u'HST/WFC3/IR F105W'
    tao_bandpassfilter_30.filter_id = u'WFC3/f105w.IR.dati'
    tao_bandpassfilter_30.description = u'<p>Hubble Space Telescope, WFC3/IR, F105W</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/WFC3_f105w.IR.dati.html">HST/WFC3/IR F105W</a>.</p>'
    tao_bandpassfilter_30.group = u''
    tao_bandpassfilter_30.order = 0L
    tao_bandpassfilter_30 = save_or_locate(tao_bandpassfilter_30)

    tao_bandpassfilter_31 = BandPassFilter()
    tao_bandpassfilter_31.label = u'HST/WFC3/IR F125W'
    tao_bandpassfilter_31.filter_id = u'WFC3/f125w.IR.dati'
    tao_bandpassfilter_31.description = u'<p>Hubble Space Telescope, WFC3/IR, F125W</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/WFC3_f125w.IR.dati.html">HST/WFC3/IR F125W</a>.</p>'
    tao_bandpassfilter_31.group = u''
    tao_bandpassfilter_31.order = 0L
    tao_bandpassfilter_31 = save_or_locate(tao_bandpassfilter_31)

    tao_bandpassfilter_32 = BandPassFilter()
    tao_bandpassfilter_32.label = u'HST/WFC3/IR F160W'
    tao_bandpassfilter_32.filter_id = u'WFC3/f160w.IR.dati'
    tao_bandpassfilter_32.description = u'<p>Hubble Space Telescope, WFC3/IR, F160W</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/WFC3_f160w.IR.dati.html">HST/WFC3/IR F160W</a>.</p>'
    tao_bandpassfilter_32.group = u''
    tao_bandpassfilter_32.order = 0L
    tao_bandpassfilter_32 = save_or_locate(tao_bandpassfilter_32)

    tao_bandpassfilter_33 = BandPassFilter()
    tao_bandpassfilter_33.label = u'HST/WFC3/IR/UVIS1 F265W'
    tao_bandpassfilter_33.filter_id = u'WFC3/f275w.UVIS1.dati'
    tao_bandpassfilter_33.description = u'<p>Hubble Space Telescope, WFC3/IR/UVIS1, F275W</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/WFC3_f275w.UVIS1.dati.html">HST/WFC3/IR/UVIS1 F265W</a>.</p>'
    tao_bandpassfilter_33.group = u''
    tao_bandpassfilter_33.order = 0L
    tao_bandpassfilter_33 = save_or_locate(tao_bandpassfilter_33)

    tao_bandpassfilter_34 = BandPassFilter()
    tao_bandpassfilter_34.label = u'HST/WFC3/IR/UVIS1 F336W'
    tao_bandpassfilter_34.filter_id = u'WFC3/f336w.UVIS1.dati'
    tao_bandpassfilter_34.description = u'<p>Hubble Space Telescope, WFC3/IR/UVIS1, F336W</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/WFC3_f336w.UVIS1.dati.html">HST/WFC3/IR/UVIS1 F336W</a>.</p>'
    tao_bandpassfilter_34.group = u''
    tao_bandpassfilter_34.order = 0L
    tao_bandpassfilter_34 = save_or_locate(tao_bandpassfilter_34)

    tao_bandpassfilter_35 = BandPassFilter()
    tao_bandpassfilter_35.label = u'HST/WFC3/IR/UVIS2 F265W'
    tao_bandpassfilter_35.filter_id = u'WFC3/f275w.UVIS2.dati'
    tao_bandpassfilter_35.description = u'<p>Hubble Space Telescope, WFC3/IR/UVIS2, F275W</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/WFC3_f275w.UVIS2.dati.html">HST/WFC3/IR/UVIS2 F265W</a>.</p>'
    tao_bandpassfilter_35.group = u''
    tao_bandpassfilter_35.order = 0L
    tao_bandpassfilter_35 = save_or_locate(tao_bandpassfilter_35)

    tao_bandpassfilter_36 = BandPassFilter()
    tao_bandpassfilter_36.label = u'HST/WFC3/IR/UVIS2 F336W'
    tao_bandpassfilter_36.filter_id = u'WFC3/f336w.UVIS2.dati'
    tao_bandpassfilter_36.description = u'<p>Hubble Space Telescope, WFC3/IR/UVIS2, F336W</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/WFC3_f336w.UVIS2.dati.html">HST/WFC3/IR/UVIS2 F336W</a>.</p>'
    tao_bandpassfilter_36.group = u''
    tao_bandpassfilter_36.order = 0L
    tao_bandpassfilter_36 = save_or_locate(tao_bandpassfilter_36)

    tao_bandpassfilter_37 = BandPassFilter()
    tao_bandpassfilter_37.label = u'Johnson B'
    tao_bandpassfilter_37.filter_id = u'Johnson/Johnson_B.dati'
    tao_bandpassfilter_37.description = u'<p>Johnson B band</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/Johnson_Johnson_B.dati.html">Johnson B</a>.</p>'
    tao_bandpassfilter_37.group = u''
    tao_bandpassfilter_37.order = 0L
    tao_bandpassfilter_37 = save_or_locate(tao_bandpassfilter_37)

    tao_bandpassfilter_38 = BandPassFilter()
    tao_bandpassfilter_38.label = u'Johnson H'
    tao_bandpassfilter_38.filter_id = u'Johnson/h.dat'
    tao_bandpassfilter_38.description = u'<p>Johnson H band</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/Johnson_h.dat.html">Johnson H</a>.</p>'
    tao_bandpassfilter_38.group = u''
    tao_bandpassfilter_38.order = 0L
    tao_bandpassfilter_38 = save_or_locate(tao_bandpassfilter_38)

    tao_bandpassfilter_39 = BandPassFilter()
    tao_bandpassfilter_39.label = u'Johnson I'
    tao_bandpassfilter_39.filter_id = u'Johnson/Ifilter.dati'
    tao_bandpassfilter_39.description = u'<p>Johnson I band</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/Johnson_Ifilter.dati.html">Johnson I</a>.</p>'
    tao_bandpassfilter_39.group = u''
    tao_bandpassfilter_39.order = 0L
    tao_bandpassfilter_39 = save_or_locate(tao_bandpassfilter_39)

    tao_bandpassfilter_40 = BandPassFilter()
    tao_bandpassfilter_40.label = u'Johnson J'
    tao_bandpassfilter_40.filter_id = u'Johnson/j.dat'
    tao_bandpassfilter_40.description = u'<p>Johnson J band</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/Johnson_j.dat.html">Johnson J</a>.</p>'
    tao_bandpassfilter_40.group = u''
    tao_bandpassfilter_40.order = 0L
    tao_bandpassfilter_40 = save_or_locate(tao_bandpassfilter_40)

    tao_bandpassfilter_41 = BandPassFilter()
    tao_bandpassfilter_41.label = u'Johnson K'
    tao_bandpassfilter_41.filter_id = u'Johnson/k.dat'
    tao_bandpassfilter_41.description = u'<p>Johnson K band</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/Johnson_k.dat.html">Johnson K</a>.</p>'
    tao_bandpassfilter_41.group = u''
    tao_bandpassfilter_41.order = 0L
    tao_bandpassfilter_41 = save_or_locate(tao_bandpassfilter_41)

    tao_bandpassfilter_42 = BandPassFilter()
    tao_bandpassfilter_42.label = u'Johnson R'
    tao_bandpassfilter_42.filter_id = u'Johnson/Rfilter.dati'
    tao_bandpassfilter_42.description = u'<p>Johnson R band</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/Johnson_Rfilter.dati.html">Johnson R</a>.</p>'
    tao_bandpassfilter_42.group = u''
    tao_bandpassfilter_42.order = 0L
    tao_bandpassfilter_42 = save_or_locate(tao_bandpassfilter_42)

    tao_bandpassfilter_43 = BandPassFilter()
    tao_bandpassfilter_43.label = u'Johnson U'
    tao_bandpassfilter_43.filter_id = u'Johnson/Johnson_U.dati'
    tao_bandpassfilter_43.description = u'<p>Johnson U band</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/Johnson_Johnson_U.dati.html">Johnson U</a>.</p>'
    tao_bandpassfilter_43.group = u''
    tao_bandpassfilter_43.order = 0L
    tao_bandpassfilter_43 = save_or_locate(tao_bandpassfilter_43)

    tao_bandpassfilter_44 = BandPassFilter()
    tao_bandpassfilter_44.label = u'Johnson V'
    tao_bandpassfilter_44.filter_id = u'Johnson/Johnson_V.dati'
    tao_bandpassfilter_44.description = u'<p>Johnson V band</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/Johnson_Johnson_V.dati.html">Johnson V</a>.</p>'
    tao_bandpassfilter_44.group = u''
    tao_bandpassfilter_44.order = 0L
    tao_bandpassfilter_44 = save_or_locate(tao_bandpassfilter_44)

    tao_bandpassfilter_45 = BandPassFilter()
    tao_bandpassfilter_45.label = u'Keck/DEIMOS/DEEP B'
    tao_bandpassfilter_45.filter_id = u'DEEP/deep_B.dati'
    tao_bandpassfilter_45.description = u'<p>Keck/DEIMOS/DEEP, B band</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/DEEP_deep_B.dati.html">Keck/DEIMOS/DEEP B</a>.</p>'
    tao_bandpassfilter_45.group = u''
    tao_bandpassfilter_45.order = 0L
    tao_bandpassfilter_45 = save_or_locate(tao_bandpassfilter_45)

    tao_bandpassfilter_46 = BandPassFilter()
    tao_bandpassfilter_46.label = u'Keck/DEIMOS/DEEP I'
    tao_bandpassfilter_46.filter_id = u'DEEP/deep_I.dati'
    tao_bandpassfilter_46.description = u'<p>Keck/DEIMOS/DEEP, I band</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/DEEP_deep_I.dati.html">Keck/DEIMOS/DEEP I</a>.</p>'
    tao_bandpassfilter_46.group = u''
    tao_bandpassfilter_46.order = 0L
    tao_bandpassfilter_46 = save_or_locate(tao_bandpassfilter_46)

    tao_bandpassfilter_47 = BandPassFilter()
    tao_bandpassfilter_47.label = u'Keck/DEIMOS/DEEP R'
    tao_bandpassfilter_47.filter_id = u'DEEP/deep_R.dati'
    tao_bandpassfilter_47.description = u'<p>Keck/DEIMOS/DEEP, R band</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/DEEP_deep_R.dati.html">Keck/DEIMOS/DEEP R</a>.</p>'
    tao_bandpassfilter_47.group = u''
    tao_bandpassfilter_47.order = 0L
    tao_bandpassfilter_47 = save_or_locate(tao_bandpassfilter_47)

    tao_bandpassfilter_48 = BandPassFilter()
    tao_bandpassfilter_48.label = u'LBC USPEC'
    tao_bandpassfilter_48.filter_id = u'LBC/LBCBLUE_USPEC_airm12.dati'
    tao_bandpassfilter_48.description = u'<p>Large Binocular Camera, USPEC</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/LBC_LBCBLUE_USPEC_airm12.dati.html">LBC USPEC</a>.</p>'
    tao_bandpassfilter_48.group = u''
    tao_bandpassfilter_48.order = 0L
    tao_bandpassfilter_48 = save_or_locate(tao_bandpassfilter_48)

    tao_bandpassfilter_49 = BandPassFilter()
    tao_bandpassfilter_49.label = u'Mosaic U'
    tao_bandpassfilter_49.filter_id = u'MOSAIC/U_ctio_mosaic_tot.dati'
    tao_bandpassfilter_49.description = u'<p>Cerro Tololo Inter-American Observatory (CTIO) Mosaic II, U band</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/MOSAIC_U_ctio_mosaic_tot.dati.html">Mosaic U</a>.</p>'
    tao_bandpassfilter_49.group = u''
    tao_bandpassfilter_49.order = 0L
    tao_bandpassfilter_49 = save_or_locate(tao_bandpassfilter_49)

    tao_bandpassfilter_50 = BandPassFilter()
    tao_bandpassfilter_50.label = u'MUSYC/ECDFS B'
    tao_bandpassfilter_50.filter_id = u'MUSYC/ecdfs.B.filt.dati'
    tao_bandpassfilter_50.description = u'<p>MUSYC survey, Extended Chandra Deep Field South, B band</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/MUSYC_ecdfs.B.filt.dati.html">MUSYC/ECDFS B</a>.</p>'
    tao_bandpassfilter_50.group = u''
    tao_bandpassfilter_50.order = 0L
    tao_bandpassfilter_50 = save_or_locate(tao_bandpassfilter_50)

    tao_bandpassfilter_51 = BandPassFilter()
    tao_bandpassfilter_51.label = u'MUSYC/ECDFS H'
    tao_bandpassfilter_51.filter_id = u'MUSYC/ecdfs.H.filt.dati'
    tao_bandpassfilter_51.description = u'<p>MUSYC survey, Extended Chandra Deep Field South, H band</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/MUSYC_ecdfs.H.filt.dati.html">MUSYC/ECDFS H</a>.</p>'
    tao_bandpassfilter_51.group = u''
    tao_bandpassfilter_51.order = 0L
    tao_bandpassfilter_51 = save_or_locate(tao_bandpassfilter_51)

    tao_bandpassfilter_52 = BandPassFilter()
    tao_bandpassfilter_52.label = u'MUSYC/ECDFS I'
    tao_bandpassfilter_52.filter_id = u'MUSYC/ecdfs.I.filt.dati'
    tao_bandpassfilter_52.description = u'<p>MUSYC survey, Extended Chandra Deep Field South, I band</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/MUSYC_ecdfs.I.filt.dati.html">MUSYC/ECDFS I</a>.</p>'
    tao_bandpassfilter_52.group = u''
    tao_bandpassfilter_52.order = 0L
    tao_bandpassfilter_52 = save_or_locate(tao_bandpassfilter_52)

    tao_bandpassfilter_53 = BandPassFilter()
    tao_bandpassfilter_53.label = u'MUSYC/ECDFS J'
    tao_bandpassfilter_53.filter_id = u'MUSYC/ecdfs.J.filt.dati'
    tao_bandpassfilter_53.description = u'<p>MUSYC survey, Extended Chandra Deep Field South, J band</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/MUSYC_ecdfs.J.filt.dati.html">MUSYC/ECDFS J</a>.</p>'
    tao_bandpassfilter_53.group = u''
    tao_bandpassfilter_53.order = 0L
    tao_bandpassfilter_53 = save_or_locate(tao_bandpassfilter_53)

    tao_bandpassfilter_54 = BandPassFilter()
    tao_bandpassfilter_54.label = u'MUSYC/ECDFS K'
    tao_bandpassfilter_54.filter_id = u'MUSYC/ecdfs.K.filt.dati'
    tao_bandpassfilter_54.description = u'<p>MUSYC survey, Extended Chandra Deep Field South, K band</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/MUSYC_ecdfs.K.filt.dati.html">MUSYC/ECDFS K</a>.</p>'
    tao_bandpassfilter_54.group = u''
    tao_bandpassfilter_54.order = 0L
    tao_bandpassfilter_54 = save_or_locate(tao_bandpassfilter_54)

    tao_bandpassfilter_55 = BandPassFilter()
    tao_bandpassfilter_55.label = u'MUSYC/ECDFS R'
    tao_bandpassfilter_55.filter_id = u'MUSYC/ecdfs.R.filt.dati'
    tao_bandpassfilter_55.description = u'<p>MUSYC survey, Extended Chandra Deep Field South, R band</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/MUSYC_ecdfs.R.filt.dati.html">MUSYC/ECDFS R</a>.</p>'
    tao_bandpassfilter_55.group = u''
    tao_bandpassfilter_55.order = 0L
    tao_bandpassfilter_55 = save_or_locate(tao_bandpassfilter_55)

    tao_bandpassfilter_56 = BandPassFilter()
    tao_bandpassfilter_56.label = u'MUSYC/ECDFS U'
    tao_bandpassfilter_56.filter_id = u'MUSYC/ecdfs.U.filt.dati'
    tao_bandpassfilter_56.description = u'<p>MUSYC survey, Extended Chandra Deep Field South, U band</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/MUSYC_ecdfs.U.filt.dati.html">MUSYC/ECDFS U</a>.</p>'
    tao_bandpassfilter_56.group = u''
    tao_bandpassfilter_56.order = 0L
    tao_bandpassfilter_56 = save_or_locate(tao_bandpassfilter_56)

    tao_bandpassfilter_57 = BandPassFilter()
    tao_bandpassfilter_57.label = u'MUSYC/ECDFS V'
    tao_bandpassfilter_57.filter_id = u'MUSYC/ecdfs.V.filt.dati'
    tao_bandpassfilter_57.description = u'<p>MUSYC survey, Extended Chandra Deep Field South, V band</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/MUSYC_ecdfs.V.filt.dati.html">MUSYC/ECDFS V</a>.</p>'
    tao_bandpassfilter_57.group = u''
    tao_bandpassfilter_57.order = 0L
    tao_bandpassfilter_57 = save_or_locate(tao_bandpassfilter_57)

    tao_bandpassfilter_58 = BandPassFilter()
    tao_bandpassfilter_58.label = u'MUSYC/ECDFS z'
    tao_bandpassfilter_58.filter_id = u'MUSYC/ecdfs.z.filt.dati'
    tao_bandpassfilter_58.description = u'<p>MUSYC survey, Extended Chandra Deep Field South, z band</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/MUSYC_ecdfs.z.filt.dati.html">MUSYC/ECDFS z</a>.</p>'
    tao_bandpassfilter_58.group = u''
    tao_bandpassfilter_58.order = 0L
    tao_bandpassfilter_58 = save_or_locate(tao_bandpassfilter_58)

    tao_bandpassfilter_59 = BandPassFilter()
    tao_bandpassfilter_59.label = u'NEWFIRM H'
    tao_bandpassfilter_59.filter_id = u'NEWFIRM/newfirmH.dati'
    tao_bandpassfilter_59.description = u'<p>NOAO Extremely Wide-Field Infrared Imager (NEWFIRM), H band</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/NEWFIRM_newfirmH.dati.html">NEWFIRM H</a>.</p>'
    tao_bandpassfilter_59.group = u''
    tao_bandpassfilter_59.order = 0L
    tao_bandpassfilter_59 = save_or_locate(tao_bandpassfilter_59)

    tao_bandpassfilter_60 = BandPassFilter()
    tao_bandpassfilter_60.label = u'NEWFIRM J'
    tao_bandpassfilter_60.filter_id = u'NEWFIRM/newfirmJ.dati'
    tao_bandpassfilter_60.description = u'<p>NOAO Extremely Wide-Field Infrared Imager (NEWFIRM), J band</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/NEWFIRM_newfirmJ.dati.html">NEWFIRM J</a>.</p>'
    tao_bandpassfilter_60.group = u''
    tao_bandpassfilter_60.order = 0L
    tao_bandpassfilter_60 = save_or_locate(tao_bandpassfilter_60)

    tao_bandpassfilter_61 = BandPassFilter()
    tao_bandpassfilter_61.label = u'NEWFIRM K'
    tao_bandpassfilter_61.filter_id = u'NEWFIRM/newfirmK.dati'
    tao_bandpassfilter_61.description = u'<p>NOAO Extremely Wide-Field Infrared Imager (NEWFIRM), K band</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/NEWFIRM_newfirmK.dati.html">NEWFIRM K</a>.</p>'
    tao_bandpassfilter_61.group = u''
    tao_bandpassfilter_61.order = 0L
    tao_bandpassfilter_61 = save_or_locate(tao_bandpassfilter_61)

    tao_bandpassfilter_62 = BandPassFilter()
    tao_bandpassfilter_62.label = u'SCUBA 850'
    tao_bandpassfilter_62.filter_id = u'SCUBA/SCUBA_850.dati'
    tao_bandpassfilter_62.description = u'<p>SCUBA 850 micron</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/SCUBA_SCUBA_850.dati.html">SCUBA 850</a>.</p>'
    tao_bandpassfilter_62.group = u''
    tao_bandpassfilter_62.order = 0L
    tao_bandpassfilter_62 = save_or_locate(tao_bandpassfilter_62)

    tao_bandpassfilter_63 = BandPassFilter()
    tao_bandpassfilter_63.label = u'SDSS g'
    tao_bandpassfilter_63.filter_id = u'SDSS/sdss_g.dati'
    tao_bandpassfilter_63.description = u'<p>Sloan Digital Sky Survey (SDSS) g</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/SDSS_sdss_g.dati.html">SDSS g</a>.</p>'
    tao_bandpassfilter_63.group = u''
    tao_bandpassfilter_63.order = 0L
    tao_bandpassfilter_63 = save_or_locate(tao_bandpassfilter_63)

    tao_bandpassfilter_64 = BandPassFilter()
    tao_bandpassfilter_64.label = u'SDSS i'
    tao_bandpassfilter_64.filter_id = u'SDSS/sdss_i.dati'
    tao_bandpassfilter_64.description = u'<p>Sloan Digital Sky Survey (SDSS) i</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/SDSS_sdss_i.dati.html">SDSS i</a>.</p>'
    tao_bandpassfilter_64.group = u''
    tao_bandpassfilter_64.order = 0L
    tao_bandpassfilter_64 = save_or_locate(tao_bandpassfilter_64)

    tao_bandpassfilter_65 = BandPassFilter()
    tao_bandpassfilter_65.label = u'SDSS r'
    tao_bandpassfilter_65.filter_id = u'SDSS/sdss_r.dati'
    tao_bandpassfilter_65.description = u'<p>Sloan Digital Sky Survey (SDSS) r</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/SDSS_sdss_r.dati.html">SDSS r</a>.</p>'
    tao_bandpassfilter_65.group = u''
    tao_bandpassfilter_65.order = 0L
    tao_bandpassfilter_65 = save_or_locate(tao_bandpassfilter_65)

    tao_bandpassfilter_66 = BandPassFilter()
    tao_bandpassfilter_66.label = u'SDSS u'
    tao_bandpassfilter_66.filter_id = u'SDSS/sdss_u.dati'
    tao_bandpassfilter_66.description = u'<p>Sloan Digital Sky Survey (SDSS) u</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/SDSS_sdss_u.dati.html">SDSS u</a>.</p>'
    tao_bandpassfilter_66.group = u''
    tao_bandpassfilter_66.order = 0L
    tao_bandpassfilter_66 = save_or_locate(tao_bandpassfilter_66)

    tao_bandpassfilter_67 = BandPassFilter()
    tao_bandpassfilter_67.label = u'SDSS z'
    tao_bandpassfilter_67.filter_id = u'SDSS/sdss_z.dati'
    tao_bandpassfilter_67.description = u'<p>Sloan Digital Sky Survey (SDSS) z</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/SDSS_sdss_z.dati.html">SDSS z</a>.</p>'
    tao_bandpassfilter_67.group = u''
    tao_bandpassfilter_67.order = 0L
    tao_bandpassfilter_67 = save_or_locate(tao_bandpassfilter_67)

    tao_bandpassfilter_68 = BandPassFilter()
    tao_bandpassfilter_68.label = u'Subaru/SuprimeCAM B'
    tao_bandpassfilter_68.filter_id = u'SuprimeCAM/B_subaru.dati'
    tao_bandpassfilter_68.description = u'<p>Subaru/SuprimeCAM, B band</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/SuprimeCAM_B_subaru.dati.html">Subaru/SuprimeCAM B</a>.</p>'
    tao_bandpassfilter_68.group = u''
    tao_bandpassfilter_68.order = 0L
    tao_bandpassfilter_68 = save_or_locate(tao_bandpassfilter_68)

    tao_bandpassfilter_69 = BandPassFilter()
    tao_bandpassfilter_69.label = u"Subaru/SuprimeCAM i'"
    tao_bandpassfilter_69.filter_id = u'SuprimeCAM/i_subaru.dati'
    tao_bandpassfilter_69.description = u'<p>Subaru/SuprimeCAM, i\' band</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/SuprimeCAM_i_subaru.dati.html">Subaru/SuprimeCAM i\'</a>.</p>'
    tao_bandpassfilter_69.group = u''
    tao_bandpassfilter_69.order = 0L
    tao_bandpassfilter_69 = save_or_locate(tao_bandpassfilter_69)

    tao_bandpassfilter_70 = BandPassFilter()
    tao_bandpassfilter_70.label = u"Subaru/SuprimeCAM R'"
    tao_bandpassfilter_70.filter_id = u'SuprimeCAM/r_subaru.dati'
    tao_bandpassfilter_70.description = u'<p>Subaru/SuprimeCAM, R\' band</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/SuprimeCAM_r_subaru.dati.html">Subaru/SuprimeCAM R\'</a>.</p>'
    tao_bandpassfilter_70.group = u''
    tao_bandpassfilter_70.order = 0L
    tao_bandpassfilter_70 = save_or_locate(tao_bandpassfilter_70)

    tao_bandpassfilter_71 = BandPassFilter()
    tao_bandpassfilter_71.label = u'Subaru/SuprimeCAM V'
    tao_bandpassfilter_71.filter_id = u'SuprimeCAM/V_subaru.dati'
    tao_bandpassfilter_71.description = u'<p>Subaru/SuprimeCAM, V band</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/SuprimeCAM_V_subaru.dati.html">Subaru/SuprimeCAM V</a>.</p>'
    tao_bandpassfilter_71.group = u''
    tao_bandpassfilter_71.order = 0L
    tao_bandpassfilter_71 = save_or_locate(tao_bandpassfilter_71)

    tao_bandpassfilter_72 = BandPassFilter()
    tao_bandpassfilter_72.label = u"Subaru/SuprimeCAM z'"
    tao_bandpassfilter_72.filter_id = u'SuprimeCAM/z_subaru.dati'
    tao_bandpassfilter_72.description = u'<p>Subaru/SuprimeCAM, z\' band</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/SuprimeCAM_z_subaru.dati.html">Subaru/SuprimeCAM z\'</a>.</p>'
    tao_bandpassfilter_72.group = u''
    tao_bandpassfilter_72.order = 0L
    tao_bandpassfilter_72 = save_or_locate(tao_bandpassfilter_72)

    tao_bandpassfilter_73 = BandPassFilter()
    tao_bandpassfilter_73.label = u'UKIRT H'
    tao_bandpassfilter_73.filter_id = u'UKIRT/H_filter.dati'
    tao_bandpassfilter_73.description = u'<p>UKIRT Infrared Deep Sky Survey, H band</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/UKIRT_H_filter.dati.html">UKIRT H</a>.</p>'
    tao_bandpassfilter_73.group = u''
    tao_bandpassfilter_73.order = 0L
    tao_bandpassfilter_73 = save_or_locate(tao_bandpassfilter_73)

    tao_bandpassfilter_74 = BandPassFilter()
    tao_bandpassfilter_74.label = u'UKIRT J'
    tao_bandpassfilter_74.filter_id = u'UKIRT/J_filter.dati'
    tao_bandpassfilter_74.description = u'<p>UKIRT Infrared Deep Sky Survey, J band</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/UKIRT_J_filter.dati.html">UKIRT J</a>.</p>'
    tao_bandpassfilter_74.group = u''
    tao_bandpassfilter_74.order = 0L
    tao_bandpassfilter_74 = save_or_locate(tao_bandpassfilter_74)

    tao_bandpassfilter_75 = BandPassFilter()
    tao_bandpassfilter_75.label = u'UKIRT K'
    tao_bandpassfilter_75.filter_id = u'UKIRT/K_filter.dati'
    tao_bandpassfilter_75.description = u'<p>UKIRT Infrared Deep Sky Survey, K band</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/UKIRT_K_filter.dati.html">UKIRT K</a>.</p>'
    tao_bandpassfilter_75.group = u''
    tao_bandpassfilter_75.order = 0L
    tao_bandpassfilter_75 = save_or_locate(tao_bandpassfilter_75)

    tao_bandpassfilter_76 = BandPassFilter()
    tao_bandpassfilter_76.label = u'VLT/Hawk-I H'
    tao_bandpassfilter_76.filter_id = u'Hawk-I/HawkI_Hband.dati'
    tao_bandpassfilter_76.description = u'<p>VLT/Hawk-I, H band</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/Hawk-I_HawkI_Hband.dati.html">VLT/Hawk-I H</a>.</p>'
    tao_bandpassfilter_76.group = u''
    tao_bandpassfilter_76.order = 0L
    tao_bandpassfilter_76 = save_or_locate(tao_bandpassfilter_76)

    tao_bandpassfilter_77 = BandPassFilter()
    tao_bandpassfilter_77.label = u'VLT/Hawk-I J'
    tao_bandpassfilter_77.filter_id = u'Hawk-I/HawkI_Jband.dati'
    tao_bandpassfilter_77.description = u'<p>VLT/Hawk-I, J band</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/Hawk-I_HawkI_Jband.dati.html">VLT/Hawk-I J</a>.</p>'
    tao_bandpassfilter_77.group = u''
    tao_bandpassfilter_77.order = 0L
    tao_bandpassfilter_77 = save_or_locate(tao_bandpassfilter_77)

    tao_bandpassfilter_78 = BandPassFilter()
    tao_bandpassfilter_78.label = u'VLT/Hawk-I K'
    tao_bandpassfilter_78.filter_id = u'Hawk-I/HawkI_Kband.dati'
    tao_bandpassfilter_78.description = u'<p>VLT/Hawk-I, K band</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/Hawk-I_HawkI_Kband.dati.html">VLT/Hawk-I K</a>.</p>'
    tao_bandpassfilter_78.group = u''
    tao_bandpassfilter_78.order = 0L
    tao_bandpassfilter_78 = save_or_locate(tao_bandpassfilter_78)

    tao_bandpassfilter_79 = BandPassFilter()
    tao_bandpassfilter_79.label = u'VLT/Hawk-I Y'
    tao_bandpassfilter_79.filter_id = u'Hawk-I/HawkI_Yband.dati'
    tao_bandpassfilter_79.description = u'<p>VLT/Hawk-I, Y band</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/Hawk-I_HawkI_Yband.dati.html">VLT/Hawk-I Y</a>.</p>'
    tao_bandpassfilter_79.group = u''
    tao_bandpassfilter_79.order = 0L
    tao_bandpassfilter_79 = save_or_locate(tao_bandpassfilter_79)

    tao_bandpassfilter_80 = BandPassFilter()
    tao_bandpassfilter_80.label = u'VLT/VIMOS R'
    tao_bandpassfilter_80.filter_id = u'VIMOS/R_vimos_inband.dati'
    tao_bandpassfilter_80.description = u'<p>VLT/VIMOS, R band</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/VIMOS_R_vimos_inband.dati.html">VLT/VIMOS R</a>.</p>'
    tao_bandpassfilter_80.group = u''
    tao_bandpassfilter_80.order = 0L
    tao_bandpassfilter_80 = save_or_locate(tao_bandpassfilter_80)

    tao_bandpassfilter_81 = BandPassFilter()
    tao_bandpassfilter_81.label = u'VLT/VIMOS U'
    tao_bandpassfilter_81.filter_id = u'VIMOS/U_vimos.dati'
    tao_bandpassfilter_81.description = u'<p>VLT/VIMOS, U band</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/VIMOS_U_vimos.dati.html">VLT/VIMOS U</a>.</p>'
    tao_bandpassfilter_81.group = u''
    tao_bandpassfilter_81.order = 0L
    tao_bandpassfilter_81 = save_or_locate(tao_bandpassfilter_81)

    tao_bandpassfilter_82 = BandPassFilter()
    tao_bandpassfilter_82.label = u'VLT/VISTA H'
    tao_bandpassfilter_82.filter_id = u'VISTA/VISTA_Hband.dati'
    tao_bandpassfilter_82.description = u'<p>VLT/VISTA, H band</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/VISTA_VISTA_Hband.dati.html">VLT/VISTA H</a>.</p>'
    tao_bandpassfilter_82.group = u''
    tao_bandpassfilter_82.order = 0L
    tao_bandpassfilter_82 = save_or_locate(tao_bandpassfilter_82)

    tao_bandpassfilter_83 = BandPassFilter()
    tao_bandpassfilter_83.label = u'VLT/VISTA J'
    tao_bandpassfilter_83.filter_id = u'VISTA/VISTA_Jband.dati'
    tao_bandpassfilter_83.description = u'<p>VLT/VISTA, J band</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/VISTA_VISTA_Jband.dati.html">VLT/VISTA J</a>.</p>'
    tao_bandpassfilter_83.group = u''
    tao_bandpassfilter_83.order = 0L
    tao_bandpassfilter_83 = save_or_locate(tao_bandpassfilter_83)

    tao_bandpassfilter_84 = BandPassFilter()
    tao_bandpassfilter_84.label = u'VLT/VISTA K'
    tao_bandpassfilter_84.filter_id = u'VISTA/VISTA_Kband.dati'
    tao_bandpassfilter_84.description = u'<p>VLT/VISTA, K band</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/VISTA_VISTA_Kband.dati.html">VLT/VISTA K</a>.</p>'
    tao_bandpassfilter_84.group = u''
    tao_bandpassfilter_84.order = 0L
    tao_bandpassfilter_84 = save_or_locate(tao_bandpassfilter_84)

    tao_bandpassfilter_85 = BandPassFilter()
    tao_bandpassfilter_85.label = u'VLT/VISTA Y'
    tao_bandpassfilter_85.filter_id = u'VISTA/VISTA_Yband.dati'
    tao_bandpassfilter_85.description = u'<p>VLT/VISTA, Y band</p>\n<p>Additional Details: <a href="../static/docs/bpfilters/VISTA_VISTA_Yband.dati.html">VLT/VISTA Y</a>.</p>'
    tao_bandpassfilter_85.group = u''
    tao_bandpassfilter_85.order = 0L
    tao_bandpassfilter_85 = save_or_locate(tao_bandpassfilter_85)

    #Processing model: DustModel

    from tao.models import DustModel

    tao_dustmodel_1 = DustModel()
    tao_dustmodel_1.name = u'Tonini et al. 2012'
    tao_dustmodel_1.label = u'Tonini et al. 2012'
    tao_dustmodel_1.details = u'Paper: <a href="http://google.com.au">Tonini et al. 2012</a>'
    tao_dustmodel_1 = save_or_locate(tao_dustmodel_1)

    #Processing model: GlobalParameter

    from tao.models import GlobalParameter

    tao_globalparameter_1 = GlobalParameter()
    tao_globalparameter_1.parameter_name = u'approve.html'
    tao_globalparameter_1.parameter_value = u'<p>Hello {{ title }} {{ first_name }} {{ last_name }}.</p>\r\n\r\n<p>Welcome to ASVO TAO. Your account has been activated and you may sign-in at the URL below.</p>\r\n\r\n<p><a href="{{ login_url }}">{{ login_url }}</a></p>\r\n'
    tao_globalparameter_1.description = u'Template for approve email, html version.U'
    tao_globalparameter_1 = save_or_locate(tao_globalparameter_1)

    tao_globalparameter_2 = GlobalParameter()
    tao_globalparameter_2.parameter_name = u'approve.txt'
    tao_globalparameter_2.parameter_value = u'Hello {{ title }} {{ first_name }} {{ last_name }}.\r\n\r\nWelcome to ASVO TAO Staging. Your account has been activated and you may sign-in.\r\n\r\n{{ login_url }}'
    tao_globalparameter_2.description = u'Template for approve email, text version'
    tao_globalparameter_2 = save_or_locate(tao_globalparameter_2)

    tao_globalparameter_3 = GlobalParameter()
    tao_globalparameter_3.parameter_name = u'registration.html'
    tao_globalparameter_3.parameter_value = u'<p>A new user has registered on TAO Staging.</p>\r\n\r\n<p>Go to this url to view the currently pending requests: <a href="{{ pending_requests_url }}">{{ pending_requests_url }}</a></p>'
    tao_globalparameter_3.description = u'Template for registration email, html version.'
    tao_globalparameter_3 = save_or_locate(tao_globalparameter_3)

    tao_globalparameter_4 = GlobalParameter()
    tao_globalparameter_4.parameter_name = u'registration.txt'
    tao_globalparameter_4.parameter_value = u'A new user has registered on TAO Staging.\r\n\r\nVisit {{ pending_requests_url }} to approve or reject.\r\n'
    tao_globalparameter_4.description = u'Template for registration email, text version.'
    tao_globalparameter_4 = save_or_locate(tao_globalparameter_4)

    tao_globalparameter_5 = GlobalParameter()
    tao_globalparameter_5.parameter_name = u'reject.html'
    tao_globalparameter_5.parameter_value = u'Hello {{ title }} {{ first_name }} {{ last_name }}.\r\n\r\nYou have been rejected from using the ASVO-TAO Staging system.\r\n\r\nReason:\r\n{{ reason }}'
    tao_globalparameter_5.description = u'Template for reject email, html version.'
    tao_globalparameter_5 = save_or_locate(tao_globalparameter_5)

    tao_globalparameter_6 = GlobalParameter()
    tao_globalparameter_6.parameter_name = u'reject.txt'
    tao_globalparameter_6.parameter_value = u'Hello {{ title }} {{ first_name }} {{ last_name }}.\r\n\r\nYou have been rejected from using the ASVO-TAO Staging system.\r\n\r\nReason:\r\n{{ reason }}'
    tao_globalparameter_6.description = u'Template for reject email, text version.'
    tao_globalparameter_6 = save_or_locate(tao_globalparameter_6)

    tao_globalparameter_7 = GlobalParameter()
    tao_globalparameter_7.parameter_name = u'maximum-random-light-cones'
    tao_globalparameter_7.parameter_value = u'10'
    tao_globalparameter_7.description = u'Maximum number of random light-cones'
    tao_globalparameter_7 = save_or_locate(tao_globalparameter_7)

    tao_globalparameter_8 = GlobalParameter()
    tao_globalparameter_8.parameter_name = u'job-status.html'
    tao_globalparameter_8.parameter_value = u'<p>Dear {{ user.username }},</p>\r\n\r\n<p>Your <a href="http://tao.asvo.org.au/taostaging/jobs/{{ job.id }}">TAO Staging Job {{ job.id }}</a> has successfully completed.</p>'
    tao_globalparameter_8.description = u'Template for job status update, html version. Use {{ user }} and {{ job }} template variables'
    tao_globalparameter_8 = save_or_locate(tao_globalparameter_8)

    tao_globalparameter_9 = GlobalParameter()
    tao_globalparameter_9.parameter_name = u'job-status.txt'
    tao_globalparameter_9.parameter_value = u'Dear {{ user.username }},\r\n\r\nYour TAO Staging Job {{ job.id }} has completed.\r\n\r\nPlease view your job at: http://tao.asvo.org.au/taostaging/jobs/{{ job.id }}'
    tao_globalparameter_9.description = u'Template for job status update, text version. Use {{ user }} and {{ job }} template variables'
    tao_globalparameter_9 = save_or_locate(tao_globalparameter_9)

    tao_globalparameter_10 = GlobalParameter()
    tao_globalparameter_10.parameter_name = u'support-template.html'
    tao_globalparameter_10.parameter_value = u'<p><strong>Staging User:</strong> {{ user.username }}</p>\r\n\r\n{{ message }}'
    tao_globalparameter_10.description = u'Template for support emails, html version. Use {{ user }} and {{ message }} template variables'
    tao_globalparameter_10 = save_or_locate(tao_globalparameter_10)

    tao_globalparameter_11 = GlobalParameter()
    tao_globalparameter_11.parameter_name = u'support-template.txt'
    tao_globalparameter_11.parameter_value = u'Staging User: {{ user.username }}\r\n\r\n{{ message }}'
    tao_globalparameter_11.description = u'Template for support emails, text version. Use {{ user }}, {{ subject }} & {{ message }} template variables'
    tao_globalparameter_11 = save_or_locate(tao_globalparameter_11)

    tao_globalparameter_12 = GlobalParameter()
    tao_globalparameter_12.parameter_name = u'support-recipients'
    tao_globalparameter_12.parameter_value = u'alistair@intersect.org.au, dcroton@astro.swin.edu.au'
    tao_globalparameter_12.description = u'List of recipients to send support emails'
    tao_globalparameter_12 = save_or_locate(tao_globalparameter_12)

    tao_globalparameter_13 = GlobalParameter()
    tao_globalparameter_13.parameter_name = u'INITIAL_JOB_STATUS'
    tao_globalparameter_13.parameter_value = u'SUBMITTED'
    tao_globalparameter_13.description = u'Status assigned to jobs when created in New Catalogue. Use one of HELD or SUBMITTED.'
    tao_globalparameter_13 = save_or_locate(tao_globalparameter_13)

    #Processing model: WorkflowCommand

    from tao.models import WorkflowCommand

    tao_workflowcommand_1 = WorkflowCommand()
    tao_workflowcommand_1.issued = datetime.datetime(2013, 7, 12, 1, 54, 40, tzinfo=pytz.UTC)
    tao_workflowcommand_1.command = u'Job_Stop'
    tao_workflowcommand_1.parameters = u''
    tao_workflowcommand_1.executed = None
    tao_workflowcommand_1.execution_status = u'SUBMITTED'
    tao_workflowcommand_1.execution_comment = u''
    tao_workflowcommand_1 = save_or_locate(tao_workflowcommand_1)

    tao_workflowcommand_2 = WorkflowCommand()
    tao_workflowcommand_2.issued = datetime.datetime(2013, 7, 12, 1, 57, 35, tzinfo=pytz.UTC)
    tao_workflowcommand_2.command = u'Job_Output_Delete'
    tao_workflowcommand_2.parameters = u'Amr'
    tao_workflowcommand_2.executed = None
    tao_workflowcommand_2.execution_status = u'COMPLETED'
    tao_workflowcommand_2.execution_comment = u''
    tao_workflowcommand_2 = save_or_locate(tao_workflowcommand_2)

    tao_workflowcommand_3 = WorkflowCommand()
    tao_workflowcommand_3.job_id = None
    tao_workflowcommand_3.issued = datetime.datetime(2013, 7, 17, 0, 36, 2, tzinfo=pytz.UTC)
    tao_workflowcommand_3.command = u'Job_Stop_All'
    tao_workflowcommand_3.parameters = u''
    tao_workflowcommand_3.executed = None
    tao_workflowcommand_3.execution_status = u'COMPLETED'
    tao_workflowcommand_3.execution_comment = u''
    tao_workflowcommand_3 = save_or_locate(tao_workflowcommand_3)

    #Processing model: TaoUser

    from tao.models import TaoUser

    tao_taouser_1 = TaoUser()
    tao_taouser_1.password = u'pbkdf2_sha256$10000$6RjuCdHl4QHV$Mugd1gfyo4crtqcAaYeOKYmtWs/0k6FIh5Rm2/YjiuE='
    tao_taouser_1.last_login = datetime.datetime(2013, 7, 15, 2, 36, 48, tzinfo=pytz.UTC)
    tao_taouser_1.is_superuser = True
    tao_taouser_1.username = u'staging'
    tao_taouser_1.first_name = u'stage'
    tao_taouser_1.last_name = u'user'
    tao_taouser_1.email = u'akgrant@gmail.com'
    tao_taouser_1.is_staff = True
    tao_taouser_1.is_active = True
    tao_taouser_1.date_joined = datetime.datetime(2013, 7, 1, 15, 39, 56, tzinfo=pytz.UTC)
    tao_taouser_1.institution = None
    tao_taouser_1.scientific_interests = None
    tao_taouser_1.title = None
    tao_taouser_1.rejected = False
    tao_taouser_1.aaf_shared_token = u''
    tao_taouser_1.account_registration_status = u'NA'
    tao_taouser_1.account_registration_reason = u''
    tao_taouser_1.account_registration_date = None
    tao_taouser_1 = save_or_locate(tao_taouser_1)

    tao_taouser_2 = TaoUser()
    tao_taouser_2.password = u'pbkdf2_sha256$10000$qqTtklsDljw8$qELd0yaDbu1gi8KOXRY11BSWTxMsBp82CHMaYsjjbxs='
    tao_taouser_2.last_login = datetime.datetime(2013, 7, 22, 7, 45, 40, tzinfo=pytz.UTC)
    tao_taouser_2.is_superuser = True
    tao_taouser_2.username = u'alistair'
    tao_taouser_2.first_name = u'Alistair'
    tao_taouser_2.last_name = u'Grant'
    tao_taouser_2.email = u'alistair@intersect.org.au'
    tao_taouser_2.is_staff = True
    tao_taouser_2.is_active = True
    tao_taouser_2.date_joined = datetime.datetime(2013, 7, 7, 17, 35, 38, tzinfo=pytz.UTC)
    tao_taouser_2.institution = u'Intersect'
    tao_taouser_2.scientific_interests = u'TAO'
    tao_taouser_2.title = u'Mr'
    tao_taouser_2.rejected = False
    tao_taouser_2.aaf_shared_token = u''
    tao_taouser_2.account_registration_status = u'NA'
    tao_taouser_2.account_registration_reason = u''
    tao_taouser_2.account_registration_date = None
    tao_taouser_2 = save_or_locate(tao_taouser_2)

    tao_taouser_3 = TaoUser()
    tao_taouser_3.password = u'pbkdf2_sha256$10000$jISvjDy7zaJH$tck2IVF97AzbKdOulpNVYvLlqGUV1CQ2+MPJbk4MyQQ='
    tao_taouser_3.last_login = datetime.datetime(2013, 7, 16, 6, 50, 41, tzinfo=pytz.UTC)
    tao_taouser_3.is_superuser = True
    tao_taouser_3.username = u'Amr'
    tao_taouser_3.first_name = u'Amr'
    tao_taouser_3.last_name = u'Hassan'
    tao_taouser_3.email = u'ahassan@swin.edu.au'
    tao_taouser_3.is_staff = True
    tao_taouser_3.is_active = True
    tao_taouser_3.date_joined = datetime.datetime(2013, 7, 8, 6, 5, 35, tzinfo=pytz.UTC)
    tao_taouser_3.institution = u'Swinburne'
    tao_taouser_3.scientific_interests = u''
    tao_taouser_3.title = u'Dr'
    tao_taouser_3.rejected = False
    tao_taouser_3.aaf_shared_token = u''
    tao_taouser_3.account_registration_status = u'NA'
    tao_taouser_3.account_registration_reason = u''
    tao_taouser_3.account_registration_date = None
    tao_taouser_3 = save_or_locate(tao_taouser_3)

    tao_taouser_4 = TaoUser()
    tao_taouser_4.password = u'pbkdf2_sha256$10000$xBwj3VM7mZgp$HO1da/pYlAA1lpDQ97h+RWij55LMOJQudcOp59cpLis='
    tao_taouser_4.last_login = datetime.datetime(2013, 7, 17, 6, 21, 40, tzinfo=pytz.UTC)
    tao_taouser_4.is_superuser = False
    tao_taouser_4.username = u'max'
    tao_taouser_4.first_name = u'Max'
    tao_taouser_4.last_name = u'Bern'
    tao_taouser_4.email = u'maxbernyk@gmail.com'
    tao_taouser_4.is_staff = False
    tao_taouser_4.is_active = True
    tao_taouser_4.date_joined = datetime.datetime(2013, 7, 12, 9, 41, 33, tzinfo=pytz.UTC)
    tao_taouser_4.institution = u'Swinburne'
    tao_taouser_4.scientific_interests = u''
    tao_taouser_4.title = u'Mr'
    tao_taouser_4.rejected = False
    tao_taouser_4.aaf_shared_token = u''
    tao_taouser_4.account_registration_status = u'NA'
    tao_taouser_4.account_registration_reason = u''
    tao_taouser_4.account_registration_date = None
    tao_taouser_4 = save_or_locate(tao_taouser_4)

    tao_taouser_5 = TaoUser()
    tao_taouser_5.password = u'pbkdf2_sha256$10000$EBmBJv7REWDs$opb83MxnHMA1LipM8kX57FFeWiUKPMVDQdRLKgPUrlg='
    tao_taouser_5.last_login = datetime.datetime(2013, 7, 15, 0, 9, 9, tzinfo=pytz.UTC)
    tao_taouser_5.is_superuser = False
    tao_taouser_5.username = u'lotophage'
    tao_taouser_5.first_name = u'Ilya'
    tao_taouser_5.last_name = u'Anisimoff'
    tao_taouser_5.email = u'ilya@intersect.org.au'
    tao_taouser_5.is_staff = False
    tao_taouser_5.is_active = True
    tao_taouser_5.date_joined = datetime.datetime(2013, 7, 15, 0, 9, 9, tzinfo=pytz.UTC)
    tao_taouser_5.institution = u'Intersect'
    tao_taouser_5.scientific_interests = u''
    tao_taouser_5.title = u'Mr'
    tao_taouser_5.rejected = False
    tao_taouser_5.aaf_shared_token = u''
    tao_taouser_5.account_registration_status = u'NA'
    tao_taouser_5.account_registration_reason = u''
    tao_taouser_5.account_registration_date = None
    tao_taouser_5 = save_or_locate(tao_taouser_5)

    tao_taouser_6 = TaoUser()
    tao_taouser_6.password = u'pbkdf2_sha256$10000$otOWdCjSspRH$9qPXvfIKHrsT3j7mHcSUoji1YGnuPbM6nZTzyIVWmpI='
    tao_taouser_6.last_login = datetime.datetime(2013, 7, 17, 1, 46, 32, tzinfo=pytz.UTC)
    tao_taouser_6.is_superuser = True
    tao_taouser_6.username = u'darrencroton'
    tao_taouser_6.first_name = u'Darren'
    tao_taouser_6.last_name = u'Croton'
    tao_taouser_6.email = u'dcroton@astro.swin.edu.au'
    tao_taouser_6.is_staff = True
    tao_taouser_6.is_active = True
    tao_taouser_6.date_joined = datetime.datetime(2013, 7, 17, 1, 46, 32, tzinfo=pytz.UTC)
    tao_taouser_6.institution = u'Swinburne University'
    tao_taouser_6.scientific_interests = u'Galaxies, cosmology, simulations, models'
    tao_taouser_6.title = u'Prof'
    tao_taouser_6.rejected = False
    tao_taouser_6.aaf_shared_token = u''
    tao_taouser_6.account_registration_status = u'NA'
    tao_taouser_6.account_registration_reason = u''
    tao_taouser_6.account_registration_date = None
    tao_taouser_6 = save_or_locate(tao_taouser_6)

    #Processing model: DataSet

    from tao.models import DataSet

    tao_dataset_1 = DataSet()
    tao_dataset_1.simulation = tao_simulation_2
    tao_dataset_1.galaxy_model = tao_galaxymodel_1
    tao_dataset_1.database = u'millennium_full_hdf5_dist'
    tao_dataset_1.version = Decimal('1.00')
    tao_dataset_1.import_date = datetime.date(2013, 7, 21)
    tao_dataset_1.available = True
    tao_dataset_1.default_filter_min = 0.31
    tao_dataset_1.default_filter_max = None
    tao_dataset_1 = save_or_locate(tao_dataset_1)

    tao_dataset_2 = DataSet()
    tao_dataset_2.simulation = tao_simulation_3
    tao_dataset_2.galaxy_model = tao_galaxymodel_1
    tao_dataset_2.database = u'millennium_mini_hdf5_dist'
    tao_dataset_2.version = Decimal('1.00')
    tao_dataset_2.import_date = datetime.date(2013, 7, 21)
    tao_dataset_2.available = True
    tao_dataset_2.default_filter_min = 0.1
    tao_dataset_2.default_filter_max = None
    tao_dataset_2 = save_or_locate(tao_dataset_2)

    tao_dataset_3 = DataSet()
    tao_dataset_3.simulation = tao_simulation_1
    tao_dataset_3.galaxy_model = tao_galaxymodel_1
    tao_dataset_3.database = u'bolshoi_full_dist'
    tao_dataset_3.version = Decimal('1.00')
    tao_dataset_3.import_date = datetime.date(2013, 7, 21)
    tao_dataset_3.available = True
    tao_dataset_3.default_filter_min = 0.31
    tao_dataset_3.default_filter_max = None
    tao_dataset_3 = save_or_locate(tao_dataset_3)

    #Processing model: DataSetProperty

    from tao.models import DataSetProperty

    tao_datasetproperty_1 = DataSetProperty()
    tao_datasetproperty_1.name = u'stellarmass'
    tao_datasetproperty_1.units = u'10+10solMass/h'
    tao_datasetproperty_1.label = u'Total Stellar Mass'
    tao_datasetproperty_1.dataset = tao_dataset_1
    tao_datasetproperty_1.data_type = 1L
    tao_datasetproperty_1.is_computed = False
    tao_datasetproperty_1.is_filter = True
    tao_datasetproperty_1.is_output = True
    tao_datasetproperty_1.description = u'Total galaxy stellar mass'
    tao_datasetproperty_1.group = u'Galaxy Masses'
    tao_datasetproperty_1.order = 1L
    tao_datasetproperty_1 = save_or_locate(tao_datasetproperty_1)

    tao_datasetproperty_2 = DataSetProperty()
    tao_datasetproperty_2.name = u'stellarmass'
    tao_datasetproperty_2.units = u'10+10solMass/h'
    tao_datasetproperty_2.label = u'Total Stellar Mass'
    tao_datasetproperty_2.dataset = tao_dataset_2
    tao_datasetproperty_2.data_type = 1L
    tao_datasetproperty_2.is_computed = False
    tao_datasetproperty_2.is_filter = True
    tao_datasetproperty_2.is_output = True
    tao_datasetproperty_2.description = u'Total galaxy stellar mass'
    tao_datasetproperty_2.group = u'Galaxy Masses'
    tao_datasetproperty_2.order = 1L
    tao_datasetproperty_2 = save_or_locate(tao_datasetproperty_2)

    tao_datasetproperty_3 = DataSetProperty()
    tao_datasetproperty_3.name = u'stellarmass'
    tao_datasetproperty_3.units = u'10+10solMass/h'
    tao_datasetproperty_3.label = u'Total Stellar Mass'
    tao_datasetproperty_3.dataset = tao_dataset_3
    tao_datasetproperty_3.data_type = 1L
    tao_datasetproperty_3.is_computed = False
    tao_datasetproperty_3.is_filter = True
    tao_datasetproperty_3.is_output = True
    tao_datasetproperty_3.description = u'Total galaxy stellar mass'
    tao_datasetproperty_3.group = u'Galaxy Masses'
    tao_datasetproperty_3.order = 1L
    tao_datasetproperty_3 = save_or_locate(tao_datasetproperty_3)

    tao_datasetproperty_4 = DataSetProperty()
    tao_datasetproperty_4.name = u'bulgemass'
    tao_datasetproperty_4.units = u'10+10solMass/h'
    tao_datasetproperty_4.label = u'Bulge Stellar Mass'
    tao_datasetproperty_4.dataset = tao_dataset_1
    tao_datasetproperty_4.data_type = 1L
    tao_datasetproperty_4.is_computed = False
    tao_datasetproperty_4.is_filter = True
    tao_datasetproperty_4.is_output = True
    tao_datasetproperty_4.description = u'Bulge stellar mass only'
    tao_datasetproperty_4.group = u'Galaxy Masses'
    tao_datasetproperty_4.order = 2L
    tao_datasetproperty_4 = save_or_locate(tao_datasetproperty_4)

    tao_datasetproperty_5 = DataSetProperty()
    tao_datasetproperty_5.name = u'bulgemass'
    tao_datasetproperty_5.units = u'10+10solMass/h'
    tao_datasetproperty_5.label = u'Bulge Stellar Mass'
    tao_datasetproperty_5.dataset = tao_dataset_2
    tao_datasetproperty_5.data_type = 1L
    tao_datasetproperty_5.is_computed = False
    tao_datasetproperty_5.is_filter = True
    tao_datasetproperty_5.is_output = True
    tao_datasetproperty_5.description = u'Bulge stellar mass only'
    tao_datasetproperty_5.group = u'Galaxy Masses'
    tao_datasetproperty_5.order = 2L
    tao_datasetproperty_5 = save_or_locate(tao_datasetproperty_5)

    tao_datasetproperty_6 = DataSetProperty()
    tao_datasetproperty_6.name = u'bulgemass'
    tao_datasetproperty_6.units = u'10+10solMass/h'
    tao_datasetproperty_6.label = u'Bulge Stellar Mass'
    tao_datasetproperty_6.dataset = tao_dataset_3
    tao_datasetproperty_6.data_type = 1L
    tao_datasetproperty_6.is_computed = False
    tao_datasetproperty_6.is_filter = True
    tao_datasetproperty_6.is_output = True
    tao_datasetproperty_6.description = u'Bulge stellar mass only'
    tao_datasetproperty_6.group = u'Galaxy Masses'
    tao_datasetproperty_6.order = 2L
    tao_datasetproperty_6 = save_or_locate(tao_datasetproperty_6)

    tao_datasetproperty_7 = DataSetProperty()
    tao_datasetproperty_7.name = u'blackholemass'
    tao_datasetproperty_7.units = u'10+10solMass/h'
    tao_datasetproperty_7.label = u'Black Hole Mass'
    tao_datasetproperty_7.dataset = tao_dataset_1
    tao_datasetproperty_7.data_type = 1L
    tao_datasetproperty_7.is_computed = False
    tao_datasetproperty_7.is_filter = True
    tao_datasetproperty_7.is_output = True
    tao_datasetproperty_7.description = u'Supermassive black hole mass'
    tao_datasetproperty_7.group = u'Galaxy Masses'
    tao_datasetproperty_7.order = 3L
    tao_datasetproperty_7 = save_or_locate(tao_datasetproperty_7)

    tao_datasetproperty_8 = DataSetProperty()
    tao_datasetproperty_8.name = u'blackholemass'
    tao_datasetproperty_8.units = u'10+10solMass/h'
    tao_datasetproperty_8.label = u'Black Hole Mass'
    tao_datasetproperty_8.dataset = tao_dataset_2
    tao_datasetproperty_8.data_type = 1L
    tao_datasetproperty_8.is_computed = False
    tao_datasetproperty_8.is_filter = True
    tao_datasetproperty_8.is_output = True
    tao_datasetproperty_8.description = u'Supermassive black hole mass'
    tao_datasetproperty_8.group = u'Galaxy Masses'
    tao_datasetproperty_8.order = 3L
    tao_datasetproperty_8 = save_or_locate(tao_datasetproperty_8)

    tao_datasetproperty_9 = DataSetProperty()
    tao_datasetproperty_9.name = u'blackholemass'
    tao_datasetproperty_9.units = u'10+10solMass/h'
    tao_datasetproperty_9.label = u'Black Hole Mass'
    tao_datasetproperty_9.dataset = tao_dataset_3
    tao_datasetproperty_9.data_type = 1L
    tao_datasetproperty_9.is_computed = False
    tao_datasetproperty_9.is_filter = True
    tao_datasetproperty_9.is_output = True
    tao_datasetproperty_9.description = u'Supermassive black hole mass'
    tao_datasetproperty_9.group = u'Galaxy Masses'
    tao_datasetproperty_9.order = 3L
    tao_datasetproperty_9 = save_or_locate(tao_datasetproperty_9)

    tao_datasetproperty_10 = DataSetProperty()
    tao_datasetproperty_10.name = u'coldgas'
    tao_datasetproperty_10.units = u'10+10solMass/h'
    tao_datasetproperty_10.label = u'Cold Gas Mass'
    tao_datasetproperty_10.dataset = tao_dataset_1
    tao_datasetproperty_10.data_type = 1L
    tao_datasetproperty_10.is_computed = False
    tao_datasetproperty_10.is_filter = True
    tao_datasetproperty_10.is_output = True
    tao_datasetproperty_10.description = u'Mass of cold gas in the galaxy'
    tao_datasetproperty_10.group = u'Galaxy Masses'
    tao_datasetproperty_10.order = 4L
    tao_datasetproperty_10 = save_or_locate(tao_datasetproperty_10)

    tao_datasetproperty_11 = DataSetProperty()
    tao_datasetproperty_11.name = u'coldgas'
    tao_datasetproperty_11.units = u'10+10solMass/h'
    tao_datasetproperty_11.label = u'Cold Gas Mass'
    tao_datasetproperty_11.dataset = tao_dataset_2
    tao_datasetproperty_11.data_type = 1L
    tao_datasetproperty_11.is_computed = False
    tao_datasetproperty_11.is_filter = True
    tao_datasetproperty_11.is_output = True
    tao_datasetproperty_11.description = u'Mass of cold gas in the galaxy'
    tao_datasetproperty_11.group = u'Galaxy Masses'
    tao_datasetproperty_11.order = 4L
    tao_datasetproperty_11 = save_or_locate(tao_datasetproperty_11)

    tao_datasetproperty_12 = DataSetProperty()
    tao_datasetproperty_12.name = u'coldgas'
    tao_datasetproperty_12.units = u'10+10solMass/h'
    tao_datasetproperty_12.label = u'Cold Gas Mass'
    tao_datasetproperty_12.dataset = tao_dataset_3
    tao_datasetproperty_12.data_type = 1L
    tao_datasetproperty_12.is_computed = False
    tao_datasetproperty_12.is_filter = True
    tao_datasetproperty_12.is_output = True
    tao_datasetproperty_12.description = u'Mass of cold gas in the galaxy'
    tao_datasetproperty_12.group = u'Galaxy Masses'
    tao_datasetproperty_12.order = 4L
    tao_datasetproperty_12 = save_or_locate(tao_datasetproperty_12)

    tao_datasetproperty_13 = DataSetProperty()
    tao_datasetproperty_13.name = u'hotgas'
    tao_datasetproperty_13.units = u'10+10solMass/h'
    tao_datasetproperty_13.label = u'Hot Gas Mass'
    tao_datasetproperty_13.dataset = tao_dataset_1
    tao_datasetproperty_13.data_type = 1L
    tao_datasetproperty_13.is_computed = False
    tao_datasetproperty_13.is_filter = True
    tao_datasetproperty_13.is_output = True
    tao_datasetproperty_13.description = u'Mass of hot halo gas'
    tao_datasetproperty_13.group = u'Galaxy Masses'
    tao_datasetproperty_13.order = 5L
    tao_datasetproperty_13 = save_or_locate(tao_datasetproperty_13)

    tao_datasetproperty_14 = DataSetProperty()
    tao_datasetproperty_14.name = u'hotgas'
    tao_datasetproperty_14.units = u'10+10solMass/h'
    tao_datasetproperty_14.label = u'Hot Gas Mass'
    tao_datasetproperty_14.dataset = tao_dataset_2
    tao_datasetproperty_14.data_type = 1L
    tao_datasetproperty_14.is_computed = False
    tao_datasetproperty_14.is_filter = True
    tao_datasetproperty_14.is_output = True
    tao_datasetproperty_14.description = u'Mass of hot halo gas'
    tao_datasetproperty_14.group = u'Galaxy Masses'
    tao_datasetproperty_14.order = 5L
    tao_datasetproperty_14 = save_or_locate(tao_datasetproperty_14)

    tao_datasetproperty_15 = DataSetProperty()
    tao_datasetproperty_15.name = u'hotgas'
    tao_datasetproperty_15.units = u'10+10solMass/h'
    tao_datasetproperty_15.label = u'Hot Gas Mass'
    tao_datasetproperty_15.dataset = tao_dataset_3
    tao_datasetproperty_15.data_type = 1L
    tao_datasetproperty_15.is_computed = False
    tao_datasetproperty_15.is_filter = True
    tao_datasetproperty_15.is_output = True
    tao_datasetproperty_15.description = u'Mass of hot halo gas'
    tao_datasetproperty_15.group = u'Galaxy Masses'
    tao_datasetproperty_15.order = 5L
    tao_datasetproperty_15 = save_or_locate(tao_datasetproperty_15)

    tao_datasetproperty_16 = DataSetProperty()
    tao_datasetproperty_16.name = u'ejectedmass'
    tao_datasetproperty_16.units = u'10+10solMass/h'
    tao_datasetproperty_16.label = u'Ejected Gas Mass'
    tao_datasetproperty_16.dataset = tao_dataset_1
    tao_datasetproperty_16.data_type = 1L
    tao_datasetproperty_16.is_computed = False
    tao_datasetproperty_16.is_filter = True
    tao_datasetproperty_16.is_output = True
    tao_datasetproperty_16.description = u'Gas mass ejected from the halo'
    tao_datasetproperty_16.group = u'Galaxy Masses'
    tao_datasetproperty_16.order = 6L
    tao_datasetproperty_16 = save_or_locate(tao_datasetproperty_16)

    tao_datasetproperty_17 = DataSetProperty()
    tao_datasetproperty_17.name = u'ejectedmass'
    tao_datasetproperty_17.units = u'10+10solMass/h'
    tao_datasetproperty_17.label = u'Ejected Gas Mass'
    tao_datasetproperty_17.dataset = tao_dataset_2
    tao_datasetproperty_17.data_type = 1L
    tao_datasetproperty_17.is_computed = False
    tao_datasetproperty_17.is_filter = True
    tao_datasetproperty_17.is_output = True
    tao_datasetproperty_17.description = u'Gas mass ejected from the halo'
    tao_datasetproperty_17.group = u'Galaxy Masses'
    tao_datasetproperty_17.order = 6L
    tao_datasetproperty_17 = save_or_locate(tao_datasetproperty_17)

    tao_datasetproperty_18 = DataSetProperty()
    tao_datasetproperty_18.name = u'ejectedmass'
    tao_datasetproperty_18.units = u'10+10solMass/h'
    tao_datasetproperty_18.label = u'Ejected Gas Mass'
    tao_datasetproperty_18.dataset = tao_dataset_3
    tao_datasetproperty_18.data_type = 1L
    tao_datasetproperty_18.is_computed = False
    tao_datasetproperty_18.is_filter = True
    tao_datasetproperty_18.is_output = True
    tao_datasetproperty_18.description = u'Gas mass ejected from the halo'
    tao_datasetproperty_18.group = u'Galaxy Masses'
    tao_datasetproperty_18.order = 6L
    tao_datasetproperty_18 = save_or_locate(tao_datasetproperty_18)

    tao_datasetproperty_19 = DataSetProperty()
    tao_datasetproperty_19.name = u'ics'
    tao_datasetproperty_19.units = u'10+10solMass/h'
    tao_datasetproperty_19.label = u'Intracluster Stars Mass'
    tao_datasetproperty_19.dataset = tao_dataset_1
    tao_datasetproperty_19.data_type = 1L
    tao_datasetproperty_19.is_computed = False
    tao_datasetproperty_19.is_filter = True
    tao_datasetproperty_19.is_output = True
    tao_datasetproperty_19.description = u'Stellar mass in the intracluster stars'
    tao_datasetproperty_19.group = u'Galaxy Masses'
    tao_datasetproperty_19.order = 7L
    tao_datasetproperty_19 = save_or_locate(tao_datasetproperty_19)

    tao_datasetproperty_20 = DataSetProperty()
    tao_datasetproperty_20.name = u'ics'
    tao_datasetproperty_20.units = u'10+10solMass/h'
    tao_datasetproperty_20.label = u'Intracluster Stars Mass'
    tao_datasetproperty_20.dataset = tao_dataset_2
    tao_datasetproperty_20.data_type = 1L
    tao_datasetproperty_20.is_computed = False
    tao_datasetproperty_20.is_filter = True
    tao_datasetproperty_20.is_output = True
    tao_datasetproperty_20.description = u'Stellar mass in the intracluster stars'
    tao_datasetproperty_20.group = u'Galaxy Masses'
    tao_datasetproperty_20.order = 7L
    tao_datasetproperty_20 = save_or_locate(tao_datasetproperty_20)

    tao_datasetproperty_21 = DataSetProperty()
    tao_datasetproperty_21.name = u'ics'
    tao_datasetproperty_21.units = u'10+10solMass/h'
    tao_datasetproperty_21.label = u'Intracluster Stars Mass'
    tao_datasetproperty_21.dataset = tao_dataset_3
    tao_datasetproperty_21.data_type = 1L
    tao_datasetproperty_21.is_computed = False
    tao_datasetproperty_21.is_filter = True
    tao_datasetproperty_21.is_output = True
    tao_datasetproperty_21.description = u'Stellar mass in the intracluster stars'
    tao_datasetproperty_21.group = u'Galaxy Masses'
    tao_datasetproperty_21.order = 7L
    tao_datasetproperty_21 = save_or_locate(tao_datasetproperty_21)

    tao_datasetproperty_22 = DataSetProperty()
    tao_datasetproperty_22.name = u'metalsstellarmass'
    tao_datasetproperty_22.units = u'10+10solMass/h'
    tao_datasetproperty_22.label = u'Metals Total Stellar Mass'
    tao_datasetproperty_22.dataset = tao_dataset_1
    tao_datasetproperty_22.data_type = 1L
    tao_datasetproperty_22.is_computed = False
    tao_datasetproperty_22.is_filter = True
    tao_datasetproperty_22.is_output = True
    tao_datasetproperty_22.description = u'Mass of metals in the total stellar mass'
    tao_datasetproperty_22.group = u'Galaxy Masses'
    tao_datasetproperty_22.order = 8L
    tao_datasetproperty_22 = save_or_locate(tao_datasetproperty_22)

    tao_datasetproperty_23 = DataSetProperty()
    tao_datasetproperty_23.name = u'metalsstellarmass'
    tao_datasetproperty_23.units = u'10+10solMass/h'
    tao_datasetproperty_23.label = u'Metals Total Stellar Mass'
    tao_datasetproperty_23.dataset = tao_dataset_2
    tao_datasetproperty_23.data_type = 1L
    tao_datasetproperty_23.is_computed = False
    tao_datasetproperty_23.is_filter = True
    tao_datasetproperty_23.is_output = True
    tao_datasetproperty_23.description = u'Mass of metals in the total stellar mass'
    tao_datasetproperty_23.group = u'Galaxy Masses'
    tao_datasetproperty_23.order = 8L
    tao_datasetproperty_23 = save_or_locate(tao_datasetproperty_23)

    tao_datasetproperty_24 = DataSetProperty()
    tao_datasetproperty_24.name = u'metalsstellarmass'
    tao_datasetproperty_24.units = u'10+10solMass/h'
    tao_datasetproperty_24.label = u'Metals Total Stellar Mass'
    tao_datasetproperty_24.dataset = tao_dataset_3
    tao_datasetproperty_24.data_type = 1L
    tao_datasetproperty_24.is_computed = False
    tao_datasetproperty_24.is_filter = True
    tao_datasetproperty_24.is_output = True
    tao_datasetproperty_24.description = u'Mass of metals in the total stellar mass'
    tao_datasetproperty_24.group = u'Galaxy Masses'
    tao_datasetproperty_24.order = 8L
    tao_datasetproperty_24 = save_or_locate(tao_datasetproperty_24)

    tao_datasetproperty_25 = DataSetProperty()
    tao_datasetproperty_25.name = u'metalsbulgemass'
    tao_datasetproperty_25.units = u'10+10solMass/h'
    tao_datasetproperty_25.label = u'Metals Bulge Mass'
    tao_datasetproperty_25.dataset = tao_dataset_1
    tao_datasetproperty_25.data_type = 1L
    tao_datasetproperty_25.is_computed = False
    tao_datasetproperty_25.is_filter = True
    tao_datasetproperty_25.is_output = True
    tao_datasetproperty_25.description = u'Mass of metals in the bulge'
    tao_datasetproperty_25.group = u'Galaxy Masses'
    tao_datasetproperty_25.order = 9L
    tao_datasetproperty_25 = save_or_locate(tao_datasetproperty_25)

    tao_datasetproperty_26 = DataSetProperty()
    tao_datasetproperty_26.name = u'metalsbulgemass'
    tao_datasetproperty_26.units = u'10+10solMass/h'
    tao_datasetproperty_26.label = u'Metals Bulge Mass'
    tao_datasetproperty_26.dataset = tao_dataset_2
    tao_datasetproperty_26.data_type = 1L
    tao_datasetproperty_26.is_computed = False
    tao_datasetproperty_26.is_filter = True
    tao_datasetproperty_26.is_output = True
    tao_datasetproperty_26.description = u'Mass of metals in the bulge'
    tao_datasetproperty_26.group = u'Galaxy Masses'
    tao_datasetproperty_26.order = 9L
    tao_datasetproperty_26 = save_or_locate(tao_datasetproperty_26)

    tao_datasetproperty_27 = DataSetProperty()
    tao_datasetproperty_27.name = u'metalsbulgemass'
    tao_datasetproperty_27.units = u'10+10solMass/h'
    tao_datasetproperty_27.label = u'Metals Bulge Mass'
    tao_datasetproperty_27.dataset = tao_dataset_3
    tao_datasetproperty_27.data_type = 1L
    tao_datasetproperty_27.is_computed = False
    tao_datasetproperty_27.is_filter = True
    tao_datasetproperty_27.is_output = True
    tao_datasetproperty_27.description = u'Mass of metals in the bulge'
    tao_datasetproperty_27.group = u'Galaxy Masses'
    tao_datasetproperty_27.order = 9L
    tao_datasetproperty_27 = save_or_locate(tao_datasetproperty_27)

    tao_datasetproperty_28 = DataSetProperty()
    tao_datasetproperty_28.name = u'metalscoldgas'
    tao_datasetproperty_28.units = u'10+10solMass/h'
    tao_datasetproperty_28.label = u'Metals Cold Gas Mass'
    tao_datasetproperty_28.dataset = tao_dataset_1
    tao_datasetproperty_28.data_type = 1L
    tao_datasetproperty_28.is_computed = False
    tao_datasetproperty_28.is_filter = True
    tao_datasetproperty_28.is_output = True
    tao_datasetproperty_28.description = u'Mass of metals in the cold gas'
    tao_datasetproperty_28.group = u'Galaxy Masses'
    tao_datasetproperty_28.order = 10L
    tao_datasetproperty_28 = save_or_locate(tao_datasetproperty_28)

    tao_datasetproperty_29 = DataSetProperty()
    tao_datasetproperty_29.name = u'metalscoldgas'
    tao_datasetproperty_29.units = u'10+10solMass/h'
    tao_datasetproperty_29.label = u'Metals Cold Gas Mass'
    tao_datasetproperty_29.dataset = tao_dataset_2
    tao_datasetproperty_29.data_type = 1L
    tao_datasetproperty_29.is_computed = False
    tao_datasetproperty_29.is_filter = True
    tao_datasetproperty_29.is_output = True
    tao_datasetproperty_29.description = u'Mass of metals in the cold gas'
    tao_datasetproperty_29.group = u'Galaxy Masses'
    tao_datasetproperty_29.order = 10L
    tao_datasetproperty_29 = save_or_locate(tao_datasetproperty_29)

    tao_datasetproperty_30 = DataSetProperty()
    tao_datasetproperty_30.name = u'metalscoldgas'
    tao_datasetproperty_30.units = u'10+10solMass/h'
    tao_datasetproperty_30.label = u'Metals Cold Gas Mass'
    tao_datasetproperty_30.dataset = tao_dataset_3
    tao_datasetproperty_30.data_type = 1L
    tao_datasetproperty_30.is_computed = False
    tao_datasetproperty_30.is_filter = True
    tao_datasetproperty_30.is_output = True
    tao_datasetproperty_30.description = u'Mass of metals in the cold gas'
    tao_datasetproperty_30.group = u'Galaxy Masses'
    tao_datasetproperty_30.order = 10L
    tao_datasetproperty_30 = save_or_locate(tao_datasetproperty_30)

    tao_datasetproperty_31 = DataSetProperty()
    tao_datasetproperty_31.name = u'metalshotgas'
    tao_datasetproperty_31.units = u'10+10solMass/h'
    tao_datasetproperty_31.label = u'Metals Hot Gas Mass'
    tao_datasetproperty_31.dataset = tao_dataset_1
    tao_datasetproperty_31.data_type = 1L
    tao_datasetproperty_31.is_computed = False
    tao_datasetproperty_31.is_filter = True
    tao_datasetproperty_31.is_output = True
    tao_datasetproperty_31.description = u'Mass of metals in the hot gas'
    tao_datasetproperty_31.group = u'Galaxy Masses'
    tao_datasetproperty_31.order = 11L
    tao_datasetproperty_31 = save_or_locate(tao_datasetproperty_31)

    tao_datasetproperty_32 = DataSetProperty()
    tao_datasetproperty_32.name = u'metalshotgas'
    tao_datasetproperty_32.units = u'10+10solMass/h'
    tao_datasetproperty_32.label = u'Metals Hot Gas Mass'
    tao_datasetproperty_32.dataset = tao_dataset_2
    tao_datasetproperty_32.data_type = 1L
    tao_datasetproperty_32.is_computed = False
    tao_datasetproperty_32.is_filter = True
    tao_datasetproperty_32.is_output = True
    tao_datasetproperty_32.description = u'Mass of metals in the hot gas'
    tao_datasetproperty_32.group = u'Galaxy Masses'
    tao_datasetproperty_32.order = 11L
    tao_datasetproperty_32 = save_or_locate(tao_datasetproperty_32)

    tao_datasetproperty_33 = DataSetProperty()
    tao_datasetproperty_33.name = u'metalshotgas'
    tao_datasetproperty_33.units = u'10+10solMass/h'
    tao_datasetproperty_33.label = u'Metals Hot Gas Mass'
    tao_datasetproperty_33.dataset = tao_dataset_3
    tao_datasetproperty_33.data_type = 1L
    tao_datasetproperty_33.is_computed = False
    tao_datasetproperty_33.is_filter = True
    tao_datasetproperty_33.is_output = True
    tao_datasetproperty_33.description = u'Mass of metals in the hot gas'
    tao_datasetproperty_33.group = u'Galaxy Masses'
    tao_datasetproperty_33.order = 11L
    tao_datasetproperty_33 = save_or_locate(tao_datasetproperty_33)

    tao_datasetproperty_34 = DataSetProperty()
    tao_datasetproperty_34.name = u'metalsejectedmass'
    tao_datasetproperty_34.units = u'10+10solMass/h'
    tao_datasetproperty_34.label = u'Metals Ejected Gas Mass'
    tao_datasetproperty_34.dataset = tao_dataset_1
    tao_datasetproperty_34.data_type = 1L
    tao_datasetproperty_34.is_computed = False
    tao_datasetproperty_34.is_filter = True
    tao_datasetproperty_34.is_output = True
    tao_datasetproperty_34.description = u'Mass of metals in the ejected gas'
    tao_datasetproperty_34.group = u'Galaxy Masses'
    tao_datasetproperty_34.order = 12L
    tao_datasetproperty_34 = save_or_locate(tao_datasetproperty_34)

    tao_datasetproperty_35 = DataSetProperty()
    tao_datasetproperty_35.name = u'metalsejectedmass'
    tao_datasetproperty_35.units = u'10+10solMass/h'
    tao_datasetproperty_35.label = u'Metals Ejected Gas Mass'
    tao_datasetproperty_35.dataset = tao_dataset_2
    tao_datasetproperty_35.data_type = 1L
    tao_datasetproperty_35.is_computed = False
    tao_datasetproperty_35.is_filter = True
    tao_datasetproperty_35.is_output = True
    tao_datasetproperty_35.description = u'Mass of metals in the ejected gas'
    tao_datasetproperty_35.group = u'Galaxy Masses'
    tao_datasetproperty_35.order = 12L
    tao_datasetproperty_35 = save_or_locate(tao_datasetproperty_35)

    tao_datasetproperty_36 = DataSetProperty()
    tao_datasetproperty_36.name = u'metalsejectedmass'
    tao_datasetproperty_36.units = u'10+10solMass/h'
    tao_datasetproperty_36.label = u'Metals Ejected Gas Mass'
    tao_datasetproperty_36.dataset = tao_dataset_3
    tao_datasetproperty_36.data_type = 1L
    tao_datasetproperty_36.is_computed = False
    tao_datasetproperty_36.is_filter = True
    tao_datasetproperty_36.is_output = True
    tao_datasetproperty_36.description = u'Mass of metals in the ejected gas'
    tao_datasetproperty_36.group = u'Galaxy Masses'
    tao_datasetproperty_36.order = 12L
    tao_datasetproperty_36 = save_or_locate(tao_datasetproperty_36)

    tao_datasetproperty_37 = DataSetProperty()
    tao_datasetproperty_37.name = u'metalsics'
    tao_datasetproperty_37.units = u'10+10solMass/h'
    tao_datasetproperty_37.label = u'Metals Intracluster Stars Mass'
    tao_datasetproperty_37.dataset = tao_dataset_1
    tao_datasetproperty_37.data_type = 1L
    tao_datasetproperty_37.is_computed = False
    tao_datasetproperty_37.is_filter = True
    tao_datasetproperty_37.is_output = True
    tao_datasetproperty_37.description = u'Mass of metals in the intracluster stars'
    tao_datasetproperty_37.group = u'Galaxy Masses'
    tao_datasetproperty_37.order = 13L
    tao_datasetproperty_37 = save_or_locate(tao_datasetproperty_37)

    tao_datasetproperty_38 = DataSetProperty()
    tao_datasetproperty_38.name = u'metalsics'
    tao_datasetproperty_38.units = u'10+10solMass/h'
    tao_datasetproperty_38.label = u'Metals Intracluster Stars Mass'
    tao_datasetproperty_38.dataset = tao_dataset_2
    tao_datasetproperty_38.data_type = 1L
    tao_datasetproperty_38.is_computed = False
    tao_datasetproperty_38.is_filter = True
    tao_datasetproperty_38.is_output = True
    tao_datasetproperty_38.description = u'Mass of metals in the intracluster stars'
    tao_datasetproperty_38.group = u'Galaxy Masses'
    tao_datasetproperty_38.order = 13L
    tao_datasetproperty_38 = save_or_locate(tao_datasetproperty_38)

    tao_datasetproperty_39 = DataSetProperty()
    tao_datasetproperty_39.name = u'metalsics'
    tao_datasetproperty_39.units = u'10+10solMass/h'
    tao_datasetproperty_39.label = u'Metals Intracluster Stars Mass'
    tao_datasetproperty_39.dataset = tao_dataset_3
    tao_datasetproperty_39.data_type = 1L
    tao_datasetproperty_39.is_computed = False
    tao_datasetproperty_39.is_filter = True
    tao_datasetproperty_39.is_output = True
    tao_datasetproperty_39.description = u'Mass of metals in the intracluster stars'
    tao_datasetproperty_39.group = u'Galaxy Masses'
    tao_datasetproperty_39.order = 13L
    tao_datasetproperty_39 = save_or_locate(tao_datasetproperty_39)

    tao_datasetproperty_40 = DataSetProperty()
    tao_datasetproperty_40.name = u'objecttype'
    tao_datasetproperty_40.units = u''
    tao_datasetproperty_40.label = u'Galaxy Classification'
    tao_datasetproperty_40.dataset = tao_dataset_1
    tao_datasetproperty_40.data_type = 0L
    tao_datasetproperty_40.is_computed = False
    tao_datasetproperty_40.is_filter = False
    tao_datasetproperty_40.is_output = True
    tao_datasetproperty_40.description = u'Galaxy classification: 0=central, 1=Satellite'
    tao_datasetproperty_40.group = u'Galaxy Properties'
    tao_datasetproperty_40.order = 1L
    tao_datasetproperty_40 = save_or_locate(tao_datasetproperty_40)

    tao_datasetproperty_41 = DataSetProperty()
    tao_datasetproperty_41.name = u'objecttype'
    tao_datasetproperty_41.units = u''
    tao_datasetproperty_41.label = u'Galaxy Classification'
    tao_datasetproperty_41.dataset = tao_dataset_2
    tao_datasetproperty_41.data_type = 0L
    tao_datasetproperty_41.is_computed = False
    tao_datasetproperty_41.is_filter = False
    tao_datasetproperty_41.is_output = True
    tao_datasetproperty_41.description = u'Galaxy classification: 0=central, 1=Satellite'
    tao_datasetproperty_41.group = u'Galaxy Properties'
    tao_datasetproperty_41.order = 1L
    tao_datasetproperty_41 = save_or_locate(tao_datasetproperty_41)

    tao_datasetproperty_42 = DataSetProperty()
    tao_datasetproperty_42.name = u'objecttype'
    tao_datasetproperty_42.units = u''
    tao_datasetproperty_42.label = u'Galaxy Classification'
    tao_datasetproperty_42.dataset = tao_dataset_3
    tao_datasetproperty_42.data_type = 0L
    tao_datasetproperty_42.is_computed = False
    tao_datasetproperty_42.is_filter = False
    tao_datasetproperty_42.is_output = True
    tao_datasetproperty_42.description = u'Galaxy classification: 0=central, 1=Satellite'
    tao_datasetproperty_42.group = u'Galaxy Properties'
    tao_datasetproperty_42.order = 1L
    tao_datasetproperty_42 = save_or_locate(tao_datasetproperty_42)

    tao_datasetproperty_43 = DataSetProperty()
    tao_datasetproperty_43.name = u'diskscaleradius'
    tao_datasetproperty_43.units = u'10+6pc/h'
    tao_datasetproperty_43.label = u'Disk Scale Radius'
    tao_datasetproperty_43.dataset = tao_dataset_1
    tao_datasetproperty_43.data_type = 1L
    tao_datasetproperty_43.is_computed = False
    tao_datasetproperty_43.is_filter = True
    tao_datasetproperty_43.is_output = True
    tao_datasetproperty_43.description = u'Stellar disk scale radius'
    tao_datasetproperty_43.group = u'Galaxy Properties'
    tao_datasetproperty_43.order = 2L
    tao_datasetproperty_43 = save_or_locate(tao_datasetproperty_43)

    tao_datasetproperty_44 = DataSetProperty()
    tao_datasetproperty_44.name = u'diskscaleradius'
    tao_datasetproperty_44.units = u'10+6pc/h'
    tao_datasetproperty_44.label = u'Disk Scale Radius'
    tao_datasetproperty_44.dataset = tao_dataset_2
    tao_datasetproperty_44.data_type = 1L
    tao_datasetproperty_44.is_computed = False
    tao_datasetproperty_44.is_filter = True
    tao_datasetproperty_44.is_output = True
    tao_datasetproperty_44.description = u'Stellar disk scale radius'
    tao_datasetproperty_44.group = u'Galaxy Properties'
    tao_datasetproperty_44.order = 2L
    tao_datasetproperty_44 = save_or_locate(tao_datasetproperty_44)

    tao_datasetproperty_45 = DataSetProperty()
    tao_datasetproperty_45.name = u'diskscaleradius'
    tao_datasetproperty_45.units = u'10+6pc/h'
    tao_datasetproperty_45.label = u'Disk Scale Radius'
    tao_datasetproperty_45.dataset = tao_dataset_3
    tao_datasetproperty_45.data_type = 1L
    tao_datasetproperty_45.is_computed = False
    tao_datasetproperty_45.is_filter = True
    tao_datasetproperty_45.is_output = True
    tao_datasetproperty_45.description = u'Stellar disk scale radius'
    tao_datasetproperty_45.group = u'Galaxy Properties'
    tao_datasetproperty_45.order = 2L
    tao_datasetproperty_45 = save_or_locate(tao_datasetproperty_45)

    tao_datasetproperty_46 = DataSetProperty()
    tao_datasetproperty_46.name = u'sfr'
    tao_datasetproperty_46.units = u'solMass/yr'
    tao_datasetproperty_46.label = u'Total Star Formation Rate'
    tao_datasetproperty_46.dataset = tao_dataset_1
    tao_datasetproperty_46.data_type = 1L
    tao_datasetproperty_46.is_computed = False
    tao_datasetproperty_46.is_filter = True
    tao_datasetproperty_46.is_output = True
    tao_datasetproperty_46.description = u'Total star formation rate in the galaxy'
    tao_datasetproperty_46.group = u'Galaxy Properties'
    tao_datasetproperty_46.order = 3L
    tao_datasetproperty_46 = save_or_locate(tao_datasetproperty_46)

    tao_datasetproperty_47 = DataSetProperty()
    tao_datasetproperty_47.name = u'sfr'
    tao_datasetproperty_47.units = u'solMass/yr'
    tao_datasetproperty_47.label = u'Total Star Formation Rate'
    tao_datasetproperty_47.dataset = tao_dataset_2
    tao_datasetproperty_47.data_type = 1L
    tao_datasetproperty_47.is_computed = False
    tao_datasetproperty_47.is_filter = True
    tao_datasetproperty_47.is_output = True
    tao_datasetproperty_47.description = u'Total star formation rate in the galaxy'
    tao_datasetproperty_47.group = u'Galaxy Properties'
    tao_datasetproperty_47.order = 3L
    tao_datasetproperty_47 = save_or_locate(tao_datasetproperty_47)

    tao_datasetproperty_48 = DataSetProperty()
    tao_datasetproperty_48.name = u'sfr'
    tao_datasetproperty_48.units = u'solMass/yr'
    tao_datasetproperty_48.label = u'Total Star Formation Rate'
    tao_datasetproperty_48.dataset = tao_dataset_3
    tao_datasetproperty_48.data_type = 1L
    tao_datasetproperty_48.is_computed = False
    tao_datasetproperty_48.is_filter = True
    tao_datasetproperty_48.is_output = True
    tao_datasetproperty_48.description = u'Total star formation rate in the galaxy'
    tao_datasetproperty_48.group = u'Galaxy Properties'
    tao_datasetproperty_48.order = 3L
    tao_datasetproperty_48 = save_or_locate(tao_datasetproperty_48)

    tao_datasetproperty_49 = DataSetProperty()
    tao_datasetproperty_49.name = u'sfrbulge'
    tao_datasetproperty_49.units = u'solMass/yr'
    tao_datasetproperty_49.label = u'Bulge Star Formation Rate'
    tao_datasetproperty_49.dataset = tao_dataset_1
    tao_datasetproperty_49.data_type = 1L
    tao_datasetproperty_49.is_computed = False
    tao_datasetproperty_49.is_filter = True
    tao_datasetproperty_49.is_output = True
    tao_datasetproperty_49.description = u'Star formation rate in the bulge only'
    tao_datasetproperty_49.group = u'Galaxy Properties'
    tao_datasetproperty_49.order = 4L
    tao_datasetproperty_49 = save_or_locate(tao_datasetproperty_49)

    tao_datasetproperty_50 = DataSetProperty()
    tao_datasetproperty_50.name = u'sfrbulge'
    tao_datasetproperty_50.units = u'solMass/yr'
    tao_datasetproperty_50.label = u'Bulge Star Formation Rate'
    tao_datasetproperty_50.dataset = tao_dataset_2
    tao_datasetproperty_50.data_type = 1L
    tao_datasetproperty_50.is_computed = False
    tao_datasetproperty_50.is_filter = True
    tao_datasetproperty_50.is_output = True
    tao_datasetproperty_50.description = u'Star formation rate in the bulge only'
    tao_datasetproperty_50.group = u'Galaxy Properties'
    tao_datasetproperty_50.order = 4L
    tao_datasetproperty_50 = save_or_locate(tao_datasetproperty_50)

    tao_datasetproperty_51 = DataSetProperty()
    tao_datasetproperty_51.name = u'sfrbulge'
    tao_datasetproperty_51.units = u'solMass/yr'
    tao_datasetproperty_51.label = u'Bulge Star Formation Rate'
    tao_datasetproperty_51.dataset = tao_dataset_3
    tao_datasetproperty_51.data_type = 1L
    tao_datasetproperty_51.is_computed = False
    tao_datasetproperty_51.is_filter = True
    tao_datasetproperty_51.is_output = True
    tao_datasetproperty_51.description = u'Star formation rate in the bulge only'
    tao_datasetproperty_51.group = u'Galaxy Properties'
    tao_datasetproperty_51.order = 4L
    tao_datasetproperty_51 = save_or_locate(tao_datasetproperty_51)

    tao_datasetproperty_52 = DataSetProperty()
    tao_datasetproperty_52.name = u'sfrics'
    tao_datasetproperty_52.units = u'solMass/yr'
    tao_datasetproperty_52.label = u'Intracluster Stars Star Formation Rate'
    tao_datasetproperty_52.dataset = tao_dataset_1
    tao_datasetproperty_52.data_type = 1L
    tao_datasetproperty_52.is_computed = False
    tao_datasetproperty_52.is_filter = True
    tao_datasetproperty_52.is_output = True
    tao_datasetproperty_52.description = u'Star formation rate in the intracluster stars'
    tao_datasetproperty_52.group = u'Galaxy Properties'
    tao_datasetproperty_52.order = 5L
    tao_datasetproperty_52 = save_or_locate(tao_datasetproperty_52)

    tao_datasetproperty_53 = DataSetProperty()
    tao_datasetproperty_53.name = u'sfrics'
    tao_datasetproperty_53.units = u'solMass/yr'
    tao_datasetproperty_53.label = u'Intracluster Stars Star Formation Rate'
    tao_datasetproperty_53.dataset = tao_dataset_2
    tao_datasetproperty_53.data_type = 1L
    tao_datasetproperty_53.is_computed = False
    tao_datasetproperty_53.is_filter = True
    tao_datasetproperty_53.is_output = True
    tao_datasetproperty_53.description = u'Star formation rate in the intracluster stars'
    tao_datasetproperty_53.group = u'Galaxy Properties'
    tao_datasetproperty_53.order = 5L
    tao_datasetproperty_53 = save_or_locate(tao_datasetproperty_53)

    tao_datasetproperty_54 = DataSetProperty()
    tao_datasetproperty_54.name = u'sfrics'
    tao_datasetproperty_54.units = u'solMass/yr'
    tao_datasetproperty_54.label = u'Intracluster Stars Star Formation Rate'
    tao_datasetproperty_54.dataset = tao_dataset_3
    tao_datasetproperty_54.data_type = 1L
    tao_datasetproperty_54.is_computed = False
    tao_datasetproperty_54.is_filter = True
    tao_datasetproperty_54.is_output = True
    tao_datasetproperty_54.description = u'Star formation rate in the intracluster stars'
    tao_datasetproperty_54.group = u'Galaxy Properties'
    tao_datasetproperty_54.order = 5L
    tao_datasetproperty_54 = save_or_locate(tao_datasetproperty_54)

    tao_datasetproperty_55 = DataSetProperty()
    tao_datasetproperty_55.name = u'cooling'
    tao_datasetproperty_55.units = u'log(10-7J/s)'
    tao_datasetproperty_55.label = u'Hot Gas Cooling Rate'
    tao_datasetproperty_55.dataset = tao_dataset_1
    tao_datasetproperty_55.data_type = 1L
    tao_datasetproperty_55.is_computed = False
    tao_datasetproperty_55.is_filter = True
    tao_datasetproperty_55.is_output = True
    tao_datasetproperty_55.description = u'Cooling rate of hot halo gas'
    tao_datasetproperty_55.group = u'Galaxy Properties'
    tao_datasetproperty_55.order = 6L
    tao_datasetproperty_55 = save_or_locate(tao_datasetproperty_55)

    tao_datasetproperty_56 = DataSetProperty()
    tao_datasetproperty_56.name = u'cooling'
    tao_datasetproperty_56.units = u'log(10-7J/s)'
    tao_datasetproperty_56.label = u'Hot Gas Cooling Rate'
    tao_datasetproperty_56.dataset = tao_dataset_2
    tao_datasetproperty_56.data_type = 1L
    tao_datasetproperty_56.is_computed = False
    tao_datasetproperty_56.is_filter = True
    tao_datasetproperty_56.is_output = True
    tao_datasetproperty_56.description = u'Cooling rate of hot halo gas'
    tao_datasetproperty_56.group = u'Galaxy Properties'
    tao_datasetproperty_56.order = 6L
    tao_datasetproperty_56 = save_or_locate(tao_datasetproperty_56)

    tao_datasetproperty_57 = DataSetProperty()
    tao_datasetproperty_57.name = u'cooling'
    tao_datasetproperty_57.units = u'log(10-7J/s)'
    tao_datasetproperty_57.label = u'Hot Gas Cooling Rate'
    tao_datasetproperty_57.dataset = tao_dataset_3
    tao_datasetproperty_57.data_type = 1L
    tao_datasetproperty_57.is_computed = False
    tao_datasetproperty_57.is_filter = True
    tao_datasetproperty_57.is_output = True
    tao_datasetproperty_57.description = u'Cooling rate of hot halo gas'
    tao_datasetproperty_57.group = u'Galaxy Properties'
    tao_datasetproperty_57.order = 6L
    tao_datasetproperty_57 = save_or_locate(tao_datasetproperty_57)

    tao_datasetproperty_58 = DataSetProperty()
    tao_datasetproperty_58.name = u'heating'
    tao_datasetproperty_58.units = u'log(10-7J/s)'
    tao_datasetproperty_58.label = u'AGN Heating Rate'
    tao_datasetproperty_58.dataset = tao_dataset_1
    tao_datasetproperty_58.data_type = 1L
    tao_datasetproperty_58.is_computed = False
    tao_datasetproperty_58.is_filter = True
    tao_datasetproperty_58.is_output = True
    tao_datasetproperty_58.description = u'AGN radio-mode heating rate'
    tao_datasetproperty_58.group = u'Galaxy Properties'
    tao_datasetproperty_58.order = 7L
    tao_datasetproperty_58 = save_or_locate(tao_datasetproperty_58)

    tao_datasetproperty_59 = DataSetProperty()
    tao_datasetproperty_59.name = u'heating'
    tao_datasetproperty_59.units = u'log(10-7J/s)'
    tao_datasetproperty_59.label = u'AGN Heating Rate'
    tao_datasetproperty_59.dataset = tao_dataset_2
    tao_datasetproperty_59.data_type = 1L
    tao_datasetproperty_59.is_computed = False
    tao_datasetproperty_59.is_filter = True
    tao_datasetproperty_59.is_output = True
    tao_datasetproperty_59.description = u'AGN radio-mode heating rate'
    tao_datasetproperty_59.group = u'Galaxy Properties'
    tao_datasetproperty_59.order = 7L
    tao_datasetproperty_59 = save_or_locate(tao_datasetproperty_59)

    tao_datasetproperty_60 = DataSetProperty()
    tao_datasetproperty_60.name = u'heating'
    tao_datasetproperty_60.units = u'log(10-7J/s)'
    tao_datasetproperty_60.label = u'AGN Heating Rate'
    tao_datasetproperty_60.dataset = tao_dataset_3
    tao_datasetproperty_60.data_type = 1L
    tao_datasetproperty_60.is_computed = False
    tao_datasetproperty_60.is_filter = True
    tao_datasetproperty_60.is_output = True
    tao_datasetproperty_60.description = u'AGN radio-mode heating rate'
    tao_datasetproperty_60.group = u'Galaxy Properties'
    tao_datasetproperty_60.order = 7L
    tao_datasetproperty_60 = save_or_locate(tao_datasetproperty_60)

    tao_datasetproperty_61 = DataSetProperty()
    tao_datasetproperty_61.name = u'mvir'
    tao_datasetproperty_61.units = u'10+10Mpc/h'
    tao_datasetproperty_61.label = u'Mvir'
    tao_datasetproperty_61.dataset = tao_dataset_1
    tao_datasetproperty_61.data_type = 1L
    tao_datasetproperty_61.is_computed = False
    tao_datasetproperty_61.is_filter = True
    tao_datasetproperty_61.is_output = True
    tao_datasetproperty_61.description = u'Dark matter (sub)halo virial mass'
    tao_datasetproperty_61.group = u'Halo Properties'
    tao_datasetproperty_61.order = 1L
    tao_datasetproperty_61 = save_or_locate(tao_datasetproperty_61)

    tao_datasetproperty_62 = DataSetProperty()
    tao_datasetproperty_62.name = u'mvir'
    tao_datasetproperty_62.units = u'10+10Mpc/h'
    tao_datasetproperty_62.label = u'Mvir'
    tao_datasetproperty_62.dataset = tao_dataset_2
    tao_datasetproperty_62.data_type = 1L
    tao_datasetproperty_62.is_computed = False
    tao_datasetproperty_62.is_filter = True
    tao_datasetproperty_62.is_output = True
    tao_datasetproperty_62.description = u'Dark matter (sub)halo virial mass'
    tao_datasetproperty_62.group = u'Halo Properties'
    tao_datasetproperty_62.order = 1L
    tao_datasetproperty_62 = save_or_locate(tao_datasetproperty_62)

    tao_datasetproperty_63 = DataSetProperty()
    tao_datasetproperty_63.name = u'mvir'
    tao_datasetproperty_63.units = u'10+10Mpc/h'
    tao_datasetproperty_63.label = u'Mvir'
    tao_datasetproperty_63.dataset = tao_dataset_3
    tao_datasetproperty_63.data_type = 1L
    tao_datasetproperty_63.is_computed = False
    tao_datasetproperty_63.is_filter = True
    tao_datasetproperty_63.is_output = True
    tao_datasetproperty_63.description = u'Dark matter (sub)halo virial mass'
    tao_datasetproperty_63.group = u'Halo Properties'
    tao_datasetproperty_63.order = 1L
    tao_datasetproperty_63 = save_or_locate(tao_datasetproperty_63)

    tao_datasetproperty_64 = DataSetProperty()
    tao_datasetproperty_64.name = u'rvir'
    tao_datasetproperty_64.units = u'10+6pc/h'
    tao_datasetproperty_64.label = u'Rvir'
    tao_datasetproperty_64.dataset = tao_dataset_1
    tao_datasetproperty_64.data_type = 1L
    tao_datasetproperty_64.is_computed = False
    tao_datasetproperty_64.is_filter = True
    tao_datasetproperty_64.is_output = True
    tao_datasetproperty_64.description = u'Dark matter (sub)halo virial radius'
    tao_datasetproperty_64.group = u'Halo Properties'
    tao_datasetproperty_64.order = 2L
    tao_datasetproperty_64 = save_or_locate(tao_datasetproperty_64)

    tao_datasetproperty_65 = DataSetProperty()
    tao_datasetproperty_65.name = u'rvir'
    tao_datasetproperty_65.units = u'10+6pc/h'
    tao_datasetproperty_65.label = u'Rvir'
    tao_datasetproperty_65.dataset = tao_dataset_2
    tao_datasetproperty_65.data_type = 1L
    tao_datasetproperty_65.is_computed = False
    tao_datasetproperty_65.is_filter = True
    tao_datasetproperty_65.is_output = True
    tao_datasetproperty_65.description = u'Dark matter (sub)halo virial radius'
    tao_datasetproperty_65.group = u'Halo Properties'
    tao_datasetproperty_65.order = 2L
    tao_datasetproperty_65 = save_or_locate(tao_datasetproperty_65)

    tao_datasetproperty_66 = DataSetProperty()
    tao_datasetproperty_66.name = u'rvir'
    tao_datasetproperty_66.units = u'10+6pc/h'
    tao_datasetproperty_66.label = u'Rvir'
    tao_datasetproperty_66.dataset = tao_dataset_3
    tao_datasetproperty_66.data_type = 1L
    tao_datasetproperty_66.is_computed = False
    tao_datasetproperty_66.is_filter = True
    tao_datasetproperty_66.is_output = True
    tao_datasetproperty_66.description = u'Dark matter (sub)halo virial radius'
    tao_datasetproperty_66.group = u'Halo Properties'
    tao_datasetproperty_66.order = 2L
    tao_datasetproperty_66 = save_or_locate(tao_datasetproperty_66)

    tao_datasetproperty_67 = DataSetProperty()
    tao_datasetproperty_67.name = u'vvir'
    tao_datasetproperty_67.units = u'km/s'
    tao_datasetproperty_67.label = u'Vvir'
    tao_datasetproperty_67.dataset = tao_dataset_1
    tao_datasetproperty_67.data_type = 1L
    tao_datasetproperty_67.is_computed = False
    tao_datasetproperty_67.is_filter = True
    tao_datasetproperty_67.is_output = True
    tao_datasetproperty_67.description = u'Dark matter (sub)halo virial velocity'
    tao_datasetproperty_67.group = u'Halo Properties'
    tao_datasetproperty_67.order = 3L
    tao_datasetproperty_67 = save_or_locate(tao_datasetproperty_67)

    tao_datasetproperty_68 = DataSetProperty()
    tao_datasetproperty_68.name = u'vvir'
    tao_datasetproperty_68.units = u'km/s'
    tao_datasetproperty_68.label = u'Vvir'
    tao_datasetproperty_68.dataset = tao_dataset_2
    tao_datasetproperty_68.data_type = 1L
    tao_datasetproperty_68.is_computed = False
    tao_datasetproperty_68.is_filter = True
    tao_datasetproperty_68.is_output = True
    tao_datasetproperty_68.description = u'Dark matter (sub)halo virial velocity'
    tao_datasetproperty_68.group = u'Halo Properties'
    tao_datasetproperty_68.order = 3L
    tao_datasetproperty_68 = save_or_locate(tao_datasetproperty_68)

    tao_datasetproperty_69 = DataSetProperty()
    tao_datasetproperty_69.name = u'vvir'
    tao_datasetproperty_69.units = u'km/s'
    tao_datasetproperty_69.label = u'Vvir'
    tao_datasetproperty_69.dataset = tao_dataset_3
    tao_datasetproperty_69.data_type = 1L
    tao_datasetproperty_69.is_computed = False
    tao_datasetproperty_69.is_filter = True
    tao_datasetproperty_69.is_output = True
    tao_datasetproperty_69.description = u'Dark matter (sub)halo virial velocity'
    tao_datasetproperty_69.group = u'Halo Properties'
    tao_datasetproperty_69.order = 3L
    tao_datasetproperty_69 = save_or_locate(tao_datasetproperty_69)

    tao_datasetproperty_70 = DataSetProperty()
    tao_datasetproperty_70.name = u'vmax'
    tao_datasetproperty_70.units = u'km/s'
    tao_datasetproperty_70.label = u'Vmax'
    tao_datasetproperty_70.dataset = tao_dataset_1
    tao_datasetproperty_70.data_type = 1L
    tao_datasetproperty_70.is_computed = False
    tao_datasetproperty_70.is_filter = True
    tao_datasetproperty_70.is_output = True
    tao_datasetproperty_70.description = u'Dark matter (sub)halo maximum circular velocity'
    tao_datasetproperty_70.group = u'Halo Properties'
    tao_datasetproperty_70.order = 4L
    tao_datasetproperty_70 = save_or_locate(tao_datasetproperty_70)

    tao_datasetproperty_71 = DataSetProperty()
    tao_datasetproperty_71.name = u'vmax'
    tao_datasetproperty_71.units = u'km/s'
    tao_datasetproperty_71.label = u'Vmax'
    tao_datasetproperty_71.dataset = tao_dataset_2
    tao_datasetproperty_71.data_type = 1L
    tao_datasetproperty_71.is_computed = False
    tao_datasetproperty_71.is_filter = True
    tao_datasetproperty_71.is_output = True
    tao_datasetproperty_71.description = u'Dark matter (sub)halo maximum circular velocity'
    tao_datasetproperty_71.group = u'Halo Properties'
    tao_datasetproperty_71.order = 4L
    tao_datasetproperty_71 = save_or_locate(tao_datasetproperty_71)

    tao_datasetproperty_72 = DataSetProperty()
    tao_datasetproperty_72.name = u'vmax'
    tao_datasetproperty_72.units = u'km/s'
    tao_datasetproperty_72.label = u'Vmax'
    tao_datasetproperty_72.dataset = tao_dataset_3
    tao_datasetproperty_72.data_type = 1L
    tao_datasetproperty_72.is_computed = False
    tao_datasetproperty_72.is_filter = True
    tao_datasetproperty_72.is_output = True
    tao_datasetproperty_72.description = u'Dark matter (sub)halo maximum circular velocity'
    tao_datasetproperty_72.group = u'Halo Properties'
    tao_datasetproperty_72.order = 4L
    tao_datasetproperty_72 = save_or_locate(tao_datasetproperty_72)

    tao_datasetproperty_73 = DataSetProperty()
    tao_datasetproperty_73.name = u'veldisp'
    tao_datasetproperty_73.units = u'km/s'
    tao_datasetproperty_73.label = u'Velocity Dispersion'
    tao_datasetproperty_73.dataset = tao_dataset_1
    tao_datasetproperty_73.data_type = 1L
    tao_datasetproperty_73.is_computed = False
    tao_datasetproperty_73.is_filter = True
    tao_datasetproperty_73.is_output = True
    tao_datasetproperty_73.description = u'Dark matter halo velocity dispersion'
    tao_datasetproperty_73.group = u'Halo Properties'
    tao_datasetproperty_73.order = 5L
    tao_datasetproperty_73 = save_or_locate(tao_datasetproperty_73)

    tao_datasetproperty_74 = DataSetProperty()
    tao_datasetproperty_74.name = u'veldisp'
    tao_datasetproperty_74.units = u'km/s'
    tao_datasetproperty_74.label = u'Velocity Dispersion'
    tao_datasetproperty_74.dataset = tao_dataset_2
    tao_datasetproperty_74.data_type = 1L
    tao_datasetproperty_74.is_computed = False
    tao_datasetproperty_74.is_filter = True
    tao_datasetproperty_74.is_output = True
    tao_datasetproperty_74.description = u'Dark matter halo velocity dispersion'
    tao_datasetproperty_74.group = u'Halo Properties'
    tao_datasetproperty_74.order = 5L
    tao_datasetproperty_74 = save_or_locate(tao_datasetproperty_74)

    tao_datasetproperty_75 = DataSetProperty()
    tao_datasetproperty_75.name = u'veldisp'
    tao_datasetproperty_75.units = u'km/s'
    tao_datasetproperty_75.label = u'Velocity Dispersion'
    tao_datasetproperty_75.dataset = tao_dataset_3
    tao_datasetproperty_75.data_type = 1L
    tao_datasetproperty_75.is_computed = False
    tao_datasetproperty_75.is_filter = True
    tao_datasetproperty_75.is_output = True
    tao_datasetproperty_75.description = u'Dark matter halo velocity dispersion'
    tao_datasetproperty_75.group = u'Halo Properties'
    tao_datasetproperty_75.order = 5L
    tao_datasetproperty_75 = save_or_locate(tao_datasetproperty_75)

    tao_datasetproperty_76 = DataSetProperty()
    tao_datasetproperty_76.name = u'spinx'
    tao_datasetproperty_76.units = u''
    tao_datasetproperty_76.label = u'x Spin'
    tao_datasetproperty_76.dataset = tao_dataset_1
    tao_datasetproperty_76.data_type = 1L
    tao_datasetproperty_76.is_computed = False
    tao_datasetproperty_76.is_filter = True
    tao_datasetproperty_76.is_output = True
    tao_datasetproperty_76.description = u'X component of the (sub)halo spin'
    tao_datasetproperty_76.group = u'Halo Properties'
    tao_datasetproperty_76.order = 6L
    tao_datasetproperty_76 = save_or_locate(tao_datasetproperty_76)

    tao_datasetproperty_77 = DataSetProperty()
    tao_datasetproperty_77.name = u'spinx'
    tao_datasetproperty_77.units = u''
    tao_datasetproperty_77.label = u'x Spin'
    tao_datasetproperty_77.dataset = tao_dataset_2
    tao_datasetproperty_77.data_type = 1L
    tao_datasetproperty_77.is_computed = False
    tao_datasetproperty_77.is_filter = True
    tao_datasetproperty_77.is_output = True
    tao_datasetproperty_77.description = u'X component of the (sub)halo spin'
    tao_datasetproperty_77.group = u'Halo Properties'
    tao_datasetproperty_77.order = 6L
    tao_datasetproperty_77 = save_or_locate(tao_datasetproperty_77)

    tao_datasetproperty_78 = DataSetProperty()
    tao_datasetproperty_78.name = u'spinx'
    tao_datasetproperty_78.units = u''
    tao_datasetproperty_78.label = u'x Spin'
    tao_datasetproperty_78.dataset = tao_dataset_3
    tao_datasetproperty_78.data_type = 1L
    tao_datasetproperty_78.is_computed = False
    tao_datasetproperty_78.is_filter = True
    tao_datasetproperty_78.is_output = True
    tao_datasetproperty_78.description = u'X component of the (sub)halo spin'
    tao_datasetproperty_78.group = u'Halo Properties'
    tao_datasetproperty_78.order = 6L
    tao_datasetproperty_78 = save_or_locate(tao_datasetproperty_78)

    tao_datasetproperty_79 = DataSetProperty()
    tao_datasetproperty_79.name = u'spiny'
    tao_datasetproperty_79.units = u''
    tao_datasetproperty_79.label = u'y Spin'
    tao_datasetproperty_79.dataset = tao_dataset_1
    tao_datasetproperty_79.data_type = 1L
    tao_datasetproperty_79.is_computed = False
    tao_datasetproperty_79.is_filter = True
    tao_datasetproperty_79.is_output = True
    tao_datasetproperty_79.description = u'Y component of the (sub)halo spin'
    tao_datasetproperty_79.group = u'Halo Properties'
    tao_datasetproperty_79.order = 7L
    tao_datasetproperty_79 = save_or_locate(tao_datasetproperty_79)

    tao_datasetproperty_80 = DataSetProperty()
    tao_datasetproperty_80.name = u'spiny'
    tao_datasetproperty_80.units = u''
    tao_datasetproperty_80.label = u'y Spin'
    tao_datasetproperty_80.dataset = tao_dataset_2
    tao_datasetproperty_80.data_type = 1L
    tao_datasetproperty_80.is_computed = False
    tao_datasetproperty_80.is_filter = True
    tao_datasetproperty_80.is_output = True
    tao_datasetproperty_80.description = u'Y component of the (sub)halo spin'
    tao_datasetproperty_80.group = u'Halo Properties'
    tao_datasetproperty_80.order = 7L
    tao_datasetproperty_80 = save_or_locate(tao_datasetproperty_80)

    tao_datasetproperty_81 = DataSetProperty()
    tao_datasetproperty_81.name = u'spiny'
    tao_datasetproperty_81.units = u''
    tao_datasetproperty_81.label = u'y Spin'
    tao_datasetproperty_81.dataset = tao_dataset_3
    tao_datasetproperty_81.data_type = 1L
    tao_datasetproperty_81.is_computed = False
    tao_datasetproperty_81.is_filter = True
    tao_datasetproperty_81.is_output = True
    tao_datasetproperty_81.description = u'Y component of the (sub)halo spin'
    tao_datasetproperty_81.group = u'Halo Properties'
    tao_datasetproperty_81.order = 7L
    tao_datasetproperty_81 = save_or_locate(tao_datasetproperty_81)

    tao_datasetproperty_82 = DataSetProperty()
    tao_datasetproperty_82.name = u'spinz'
    tao_datasetproperty_82.units = u''
    tao_datasetproperty_82.label = u'z Spin'
    tao_datasetproperty_82.dataset = tao_dataset_1
    tao_datasetproperty_82.data_type = 1L
    tao_datasetproperty_82.is_computed = False
    tao_datasetproperty_82.is_filter = True
    tao_datasetproperty_82.is_output = True
    tao_datasetproperty_82.description = u'Z component of the (sub)halo spin'
    tao_datasetproperty_82.group = u'Halo Properties'
    tao_datasetproperty_82.order = 8L
    tao_datasetproperty_82 = save_or_locate(tao_datasetproperty_82)

    tao_datasetproperty_83 = DataSetProperty()
    tao_datasetproperty_83.name = u'spinz'
    tao_datasetproperty_83.units = u''
    tao_datasetproperty_83.label = u'z Spin'
    tao_datasetproperty_83.dataset = tao_dataset_2
    tao_datasetproperty_83.data_type = 1L
    tao_datasetproperty_83.is_computed = False
    tao_datasetproperty_83.is_filter = True
    tao_datasetproperty_83.is_output = True
    tao_datasetproperty_83.description = u'Z component of the (sub)halo spin'
    tao_datasetproperty_83.group = u'Halo Properties'
    tao_datasetproperty_83.order = 8L
    tao_datasetproperty_83 = save_or_locate(tao_datasetproperty_83)

    tao_datasetproperty_84 = DataSetProperty()
    tao_datasetproperty_84.name = u'spinz'
    tao_datasetproperty_84.units = u''
    tao_datasetproperty_84.label = u'z Spin'
    tao_datasetproperty_84.dataset = tao_dataset_3
    tao_datasetproperty_84.data_type = 1L
    tao_datasetproperty_84.is_computed = False
    tao_datasetproperty_84.is_filter = True
    tao_datasetproperty_84.is_output = True
    tao_datasetproperty_84.description = u'Z component of the (sub)halo spin'
    tao_datasetproperty_84.group = u'Halo Properties'
    tao_datasetproperty_84.order = 8L
    tao_datasetproperty_84 = save_or_locate(tao_datasetproperty_84)

    tao_datasetproperty_85 = DataSetProperty()
    tao_datasetproperty_85.name = u'len'
    tao_datasetproperty_85.units = u''
    tao_datasetproperty_85.label = u'Total particles'
    tao_datasetproperty_85.dataset = tao_dataset_1
    tao_datasetproperty_85.data_type = 0L
    tao_datasetproperty_85.is_computed = False
    tao_datasetproperty_85.is_filter = True
    tao_datasetproperty_85.is_output = True
    tao_datasetproperty_85.description = u'Total simulation particles in the dark matter halo'
    tao_datasetproperty_85.group = u'Halo Properties'
    tao_datasetproperty_85.order = 9L
    tao_datasetproperty_85 = save_or_locate(tao_datasetproperty_85)

    tao_datasetproperty_86 = DataSetProperty()
    tao_datasetproperty_86.name = u'len'
    tao_datasetproperty_86.units = u''
    tao_datasetproperty_86.label = u'Total particles'
    tao_datasetproperty_86.dataset = tao_dataset_2
    tao_datasetproperty_86.data_type = 0L
    tao_datasetproperty_86.is_computed = False
    tao_datasetproperty_86.is_filter = True
    tao_datasetproperty_86.is_output = True
    tao_datasetproperty_86.description = u'Total simulation particles in the dark matter halo'
    tao_datasetproperty_86.group = u'Halo Properties'
    tao_datasetproperty_86.order = 9L
    tao_datasetproperty_86 = save_or_locate(tao_datasetproperty_86)

    tao_datasetproperty_87 = DataSetProperty()
    tao_datasetproperty_87.name = u'len'
    tao_datasetproperty_87.units = u''
    tao_datasetproperty_87.label = u'Total particles'
    tao_datasetproperty_87.dataset = tao_dataset_3
    tao_datasetproperty_87.data_type = 0L
    tao_datasetproperty_87.is_computed = False
    tao_datasetproperty_87.is_filter = True
    tao_datasetproperty_87.is_output = True
    tao_datasetproperty_87.description = u'Total simulation particles in the dark matter halo'
    tao_datasetproperty_87.group = u'Halo Properties'
    tao_datasetproperty_87.order = 9L
    tao_datasetproperty_87 = save_or_locate(tao_datasetproperty_87)

    tao_datasetproperty_88 = DataSetProperty()
    tao_datasetproperty_88.name = u'centralmvir'
    tao_datasetproperty_88.units = u'10+10solMass/h'
    tao_datasetproperty_88.label = u'Central Galaxy Mvir'
    tao_datasetproperty_88.dataset = tao_dataset_1
    tao_datasetproperty_88.data_type = 1L
    tao_datasetproperty_88.is_computed = False
    tao_datasetproperty_88.is_filter = True
    tao_datasetproperty_88.is_output = True
    tao_datasetproperty_88.description = u'Dark matter FOF halo (central galaxy) virial mass'
    tao_datasetproperty_88.group = u'Halo Properties'
    tao_datasetproperty_88.order = 10L
    tao_datasetproperty_88 = save_or_locate(tao_datasetproperty_88)

    tao_datasetproperty_89 = DataSetProperty()
    tao_datasetproperty_89.name = u'centralmvir'
    tao_datasetproperty_89.units = u'10+10solMass/h'
    tao_datasetproperty_89.label = u'Central Galaxy Mvir'
    tao_datasetproperty_89.dataset = tao_dataset_2
    tao_datasetproperty_89.data_type = 1L
    tao_datasetproperty_89.is_computed = False
    tao_datasetproperty_89.is_filter = True
    tao_datasetproperty_89.is_output = True
    tao_datasetproperty_89.description = u'Dark matter FOF halo (central galaxy) virial mass'
    tao_datasetproperty_89.group = u'Halo Properties'
    tao_datasetproperty_89.order = 10L
    tao_datasetproperty_89 = save_or_locate(tao_datasetproperty_89)

    tao_datasetproperty_90 = DataSetProperty()
    tao_datasetproperty_90.name = u'centralmvir'
    tao_datasetproperty_90.units = u'10+10solMass/h'
    tao_datasetproperty_90.label = u'Central Galaxy Mvir'
    tao_datasetproperty_90.dataset = tao_dataset_3
    tao_datasetproperty_90.data_type = 1L
    tao_datasetproperty_90.is_computed = False
    tao_datasetproperty_90.is_filter = True
    tao_datasetproperty_90.is_output = True
    tao_datasetproperty_90.description = u'Dark matter FOF halo (central galaxy) virial mass'
    tao_datasetproperty_90.group = u'Halo Properties'
    tao_datasetproperty_90.order = 10L
    tao_datasetproperty_90 = save_or_locate(tao_datasetproperty_90)

    tao_datasetproperty_91 = DataSetProperty()
    tao_datasetproperty_91.name = u'posx'
    tao_datasetproperty_91.units = u'10+6pc/h'
    tao_datasetproperty_91.label = u'x (original)'
    tao_datasetproperty_91.dataset = tao_dataset_1
    tao_datasetproperty_91.data_type = 1L
    tao_datasetproperty_91.is_computed = False
    tao_datasetproperty_91.is_filter = False
    tao_datasetproperty_91.is_output = False
    tao_datasetproperty_91.description = u'Original x coordinate in the simulation box'
    tao_datasetproperty_91.group = u'Internal'
    tao_datasetproperty_91.order = 1L
    tao_datasetproperty_91 = save_or_locate(tao_datasetproperty_91)

    tao_datasetproperty_92 = DataSetProperty()
    tao_datasetproperty_92.name = u'posx'
    tao_datasetproperty_92.units = u'10+6pc/h'
    tao_datasetproperty_92.label = u'x (original)'
    tao_datasetproperty_92.dataset = tao_dataset_2
    tao_datasetproperty_92.data_type = 1L
    tao_datasetproperty_92.is_computed = False
    tao_datasetproperty_92.is_filter = False
    tao_datasetproperty_92.is_output = False
    tao_datasetproperty_92.description = u'Original x coordinate in the simulation box'
    tao_datasetproperty_92.group = u'Internal'
    tao_datasetproperty_92.order = 1L
    tao_datasetproperty_92 = save_or_locate(tao_datasetproperty_92)

    tao_datasetproperty_93 = DataSetProperty()
    tao_datasetproperty_93.name = u'posx'
    tao_datasetproperty_93.units = u'10+6pc/h'
    tao_datasetproperty_93.label = u'x (original)'
    tao_datasetproperty_93.dataset = tao_dataset_3
    tao_datasetproperty_93.data_type = 1L
    tao_datasetproperty_93.is_computed = False
    tao_datasetproperty_93.is_filter = False
    tao_datasetproperty_93.is_output = False
    tao_datasetproperty_93.description = u'Original x coordinate in the simulation box'
    tao_datasetproperty_93.group = u'Internal'
    tao_datasetproperty_93.order = 1L
    tao_datasetproperty_93 = save_or_locate(tao_datasetproperty_93)

    tao_datasetproperty_94 = DataSetProperty()
    tao_datasetproperty_94.name = u'posy'
    tao_datasetproperty_94.units = u'10+6pc/h'
    tao_datasetproperty_94.label = u'y (original)'
    tao_datasetproperty_94.dataset = tao_dataset_1
    tao_datasetproperty_94.data_type = 1L
    tao_datasetproperty_94.is_computed = False
    tao_datasetproperty_94.is_filter = False
    tao_datasetproperty_94.is_output = False
    tao_datasetproperty_94.description = u'Original y coordinate in the simulation box'
    tao_datasetproperty_94.group = u'Internal'
    tao_datasetproperty_94.order = 2L
    tao_datasetproperty_94 = save_or_locate(tao_datasetproperty_94)

    tao_datasetproperty_95 = DataSetProperty()
    tao_datasetproperty_95.name = u'posy'
    tao_datasetproperty_95.units = u'10+6pc/h'
    tao_datasetproperty_95.label = u'y (original)'
    tao_datasetproperty_95.dataset = tao_dataset_2
    tao_datasetproperty_95.data_type = 1L
    tao_datasetproperty_95.is_computed = False
    tao_datasetproperty_95.is_filter = False
    tao_datasetproperty_95.is_output = False
    tao_datasetproperty_95.description = u'Original y coordinate in the simulation box'
    tao_datasetproperty_95.group = u'Internal'
    tao_datasetproperty_95.order = 2L
    tao_datasetproperty_95 = save_or_locate(tao_datasetproperty_95)

    tao_datasetproperty_96 = DataSetProperty()
    tao_datasetproperty_96.name = u'posy'
    tao_datasetproperty_96.units = u'10+6pc/h'
    tao_datasetproperty_96.label = u'y (original)'
    tao_datasetproperty_96.dataset = tao_dataset_3
    tao_datasetproperty_96.data_type = 1L
    tao_datasetproperty_96.is_computed = False
    tao_datasetproperty_96.is_filter = False
    tao_datasetproperty_96.is_output = False
    tao_datasetproperty_96.description = u'Original y coordinate in the simulation box'
    tao_datasetproperty_96.group = u'Internal'
    tao_datasetproperty_96.order = 2L
    tao_datasetproperty_96 = save_or_locate(tao_datasetproperty_96)

    tao_datasetproperty_97 = DataSetProperty()
    tao_datasetproperty_97.name = u'posz'
    tao_datasetproperty_97.units = u'10+6pc/h'
    tao_datasetproperty_97.label = u'z (original)'
    tao_datasetproperty_97.dataset = tao_dataset_1
    tao_datasetproperty_97.data_type = 1L
    tao_datasetproperty_97.is_computed = False
    tao_datasetproperty_97.is_filter = False
    tao_datasetproperty_97.is_output = False
    tao_datasetproperty_97.description = u'Original z coordinate in the simulation box'
    tao_datasetproperty_97.group = u'Internal'
    tao_datasetproperty_97.order = 3L
    tao_datasetproperty_97 = save_or_locate(tao_datasetproperty_97)

    tao_datasetproperty_98 = DataSetProperty()
    tao_datasetproperty_98.name = u'posz'
    tao_datasetproperty_98.units = u'10+6pc/h'
    tao_datasetproperty_98.label = u'z (original)'
    tao_datasetproperty_98.dataset = tao_dataset_2
    tao_datasetproperty_98.data_type = 1L
    tao_datasetproperty_98.is_computed = False
    tao_datasetproperty_98.is_filter = False
    tao_datasetproperty_98.is_output = False
    tao_datasetproperty_98.description = u'Original z coordinate in the simulation box'
    tao_datasetproperty_98.group = u'Internal'
    tao_datasetproperty_98.order = 3L
    tao_datasetproperty_98 = save_or_locate(tao_datasetproperty_98)

    tao_datasetproperty_99 = DataSetProperty()
    tao_datasetproperty_99.name = u'posz'
    tao_datasetproperty_99.units = u'10+6pc/h'
    tao_datasetproperty_99.label = u'z (original)'
    tao_datasetproperty_99.dataset = tao_dataset_3
    tao_datasetproperty_99.data_type = 1L
    tao_datasetproperty_99.is_computed = False
    tao_datasetproperty_99.is_filter = False
    tao_datasetproperty_99.is_output = False
    tao_datasetproperty_99.description = u'Original z coordinate in the simulation box'
    tao_datasetproperty_99.group = u'Internal'
    tao_datasetproperty_99.order = 3L
    tao_datasetproperty_99 = save_or_locate(tao_datasetproperty_99)

    tao_datasetproperty_100 = DataSetProperty()
    tao_datasetproperty_100.name = u'descendant'
    tao_datasetproperty_100.units = u''
    tao_datasetproperty_100.label = u'Descendant'
    tao_datasetproperty_100.dataset = tao_dataset_1
    tao_datasetproperty_100.data_type = 0L
    tao_datasetproperty_100.is_computed = False
    tao_datasetproperty_100.is_filter = False
    tao_datasetproperty_100.is_output = False
    tao_datasetproperty_100.description = u''
    tao_datasetproperty_100.group = u'Internal'
    tao_datasetproperty_100.order = 4L
    tao_datasetproperty_100 = save_or_locate(tao_datasetproperty_100)

    tao_datasetproperty_101 = DataSetProperty()
    tao_datasetproperty_101.name = u'descendant'
    tao_datasetproperty_101.units = u''
    tao_datasetproperty_101.label = u'Descendant'
    tao_datasetproperty_101.dataset = tao_dataset_2
    tao_datasetproperty_101.data_type = 0L
    tao_datasetproperty_101.is_computed = False
    tao_datasetproperty_101.is_filter = False
    tao_datasetproperty_101.is_output = False
    tao_datasetproperty_101.description = u''
    tao_datasetproperty_101.group = u'Internal'
    tao_datasetproperty_101.order = 4L
    tao_datasetproperty_101 = save_or_locate(tao_datasetproperty_101)

    tao_datasetproperty_102 = DataSetProperty()
    tao_datasetproperty_102.name = u'descendant'
    tao_datasetproperty_102.units = u''
    tao_datasetproperty_102.label = u'Descendant'
    tao_datasetproperty_102.dataset = tao_dataset_3
    tao_datasetproperty_102.data_type = 0L
    tao_datasetproperty_102.is_computed = False
    tao_datasetproperty_102.is_filter = False
    tao_datasetproperty_102.is_output = False
    tao_datasetproperty_102.description = u''
    tao_datasetproperty_102.group = u'Internal'
    tao_datasetproperty_102.order = 4L
    tao_datasetproperty_102 = save_or_locate(tao_datasetproperty_102)

    tao_datasetproperty_103 = DataSetProperty()
    tao_datasetproperty_103.name = u'fofhaloindex'
    tao_datasetproperty_103.units = u''
    tao_datasetproperty_103.label = u'FOF Halo Index'
    tao_datasetproperty_103.dataset = tao_dataset_1
    tao_datasetproperty_103.data_type = 0L
    tao_datasetproperty_103.is_computed = False
    tao_datasetproperty_103.is_filter = False
    tao_datasetproperty_103.is_output = False
    tao_datasetproperty_103.description = u''
    tao_datasetproperty_103.group = u'Internal'
    tao_datasetproperty_103.order = 5L
    tao_datasetproperty_103 = save_or_locate(tao_datasetproperty_103)

    tao_datasetproperty_104 = DataSetProperty()
    tao_datasetproperty_104.name = u'fofhaloindex'
    tao_datasetproperty_104.units = u''
    tao_datasetproperty_104.label = u'FOF Halo Index'
    tao_datasetproperty_104.dataset = tao_dataset_2
    tao_datasetproperty_104.data_type = 0L
    tao_datasetproperty_104.is_computed = False
    tao_datasetproperty_104.is_filter = False
    tao_datasetproperty_104.is_output = False
    tao_datasetproperty_104.description = u''
    tao_datasetproperty_104.group = u'Internal'
    tao_datasetproperty_104.order = 5L
    tao_datasetproperty_104 = save_or_locate(tao_datasetproperty_104)

    tao_datasetproperty_105 = DataSetProperty()
    tao_datasetproperty_105.name = u'fofhaloindex'
    tao_datasetproperty_105.units = u''
    tao_datasetproperty_105.label = u'FOF Halo Index'
    tao_datasetproperty_105.dataset = tao_dataset_3
    tao_datasetproperty_105.data_type = 0L
    tao_datasetproperty_105.is_computed = False
    tao_datasetproperty_105.is_filter = False
    tao_datasetproperty_105.is_output = False
    tao_datasetproperty_105.description = u''
    tao_datasetproperty_105.group = u'Internal'
    tao_datasetproperty_105.order = 5L
    tao_datasetproperty_105 = save_or_locate(tao_datasetproperty_105)

    tao_datasetproperty_106 = DataSetProperty()
    tao_datasetproperty_106.name = u'globalgalaxyid'
    tao_datasetproperty_106.units = u''
    tao_datasetproperty_106.label = u'Galaxy Index'
    tao_datasetproperty_106.dataset = tao_dataset_1
    tao_datasetproperty_106.data_type = 2L
    tao_datasetproperty_106.is_computed = False
    tao_datasetproperty_106.is_filter = False
    tao_datasetproperty_106.is_output = False
    tao_datasetproperty_106.description = u''
    tao_datasetproperty_106.group = u'Internal'
    tao_datasetproperty_106.order = 6L
    tao_datasetproperty_106 = save_or_locate(tao_datasetproperty_106)

    tao_datasetproperty_107 = DataSetProperty()
    tao_datasetproperty_107.name = u'globalgalaxyid'
    tao_datasetproperty_107.units = u''
    tao_datasetproperty_107.label = u'Galaxy Index'
    tao_datasetproperty_107.dataset = tao_dataset_2
    tao_datasetproperty_107.data_type = 2L
    tao_datasetproperty_107.is_computed = False
    tao_datasetproperty_107.is_filter = False
    tao_datasetproperty_107.is_output = False
    tao_datasetproperty_107.description = u''
    tao_datasetproperty_107.group = u'Internal'
    tao_datasetproperty_107.order = 6L
    tao_datasetproperty_107 = save_or_locate(tao_datasetproperty_107)

    tao_datasetproperty_108 = DataSetProperty()
    tao_datasetproperty_108.name = u'globalgalaxyid'
    tao_datasetproperty_108.units = u''
    tao_datasetproperty_108.label = u'Galaxy Index'
    tao_datasetproperty_108.dataset = tao_dataset_3
    tao_datasetproperty_108.data_type = 2L
    tao_datasetproperty_108.is_computed = False
    tao_datasetproperty_108.is_filter = False
    tao_datasetproperty_108.is_output = False
    tao_datasetproperty_108.description = u''
    tao_datasetproperty_108.group = u'Internal'
    tao_datasetproperty_108.order = 6L
    tao_datasetproperty_108 = save_or_locate(tao_datasetproperty_108)

    tao_datasetproperty_109 = DataSetProperty()
    tao_datasetproperty_109.name = u'globaldescendant'
    tao_datasetproperty_109.units = u''
    tao_datasetproperty_109.label = u'Global Descendant'
    tao_datasetproperty_109.dataset = tao_dataset_1
    tao_datasetproperty_109.data_type = 2L
    tao_datasetproperty_109.is_computed = False
    tao_datasetproperty_109.is_filter = False
    tao_datasetproperty_109.is_output = False
    tao_datasetproperty_109.description = u''
    tao_datasetproperty_109.group = u'Internal'
    tao_datasetproperty_109.order = 7L
    tao_datasetproperty_109 = save_or_locate(tao_datasetproperty_109)

    tao_datasetproperty_110 = DataSetProperty()
    tao_datasetproperty_110.name = u'globaldescendant'
    tao_datasetproperty_110.units = u''
    tao_datasetproperty_110.label = u'Global Descendant'
    tao_datasetproperty_110.dataset = tao_dataset_2
    tao_datasetproperty_110.data_type = 2L
    tao_datasetproperty_110.is_computed = False
    tao_datasetproperty_110.is_filter = False
    tao_datasetproperty_110.is_output = False
    tao_datasetproperty_110.description = u''
    tao_datasetproperty_110.group = u'Internal'
    tao_datasetproperty_110.order = 7L
    tao_datasetproperty_110 = save_or_locate(tao_datasetproperty_110)

    tao_datasetproperty_111 = DataSetProperty()
    tao_datasetproperty_111.name = u'globaldescendant'
    tao_datasetproperty_111.units = u''
    tao_datasetproperty_111.label = u'Global Descendant'
    tao_datasetproperty_111.dataset = tao_dataset_3
    tao_datasetproperty_111.data_type = 2L
    tao_datasetproperty_111.is_computed = False
    tao_datasetproperty_111.is_filter = False
    tao_datasetproperty_111.is_output = False
    tao_datasetproperty_111.description = u''
    tao_datasetproperty_111.group = u'Internal'
    tao_datasetproperty_111.order = 7L
    tao_datasetproperty_111 = save_or_locate(tao_datasetproperty_111)

    tao_datasetproperty_112 = DataSetProperty()
    tao_datasetproperty_112.name = u'treeindex'
    tao_datasetproperty_112.units = u''
    tao_datasetproperty_112.label = u'Tree Index'
    tao_datasetproperty_112.dataset = tao_dataset_1
    tao_datasetproperty_112.data_type = 0L
    tao_datasetproperty_112.is_computed = False
    tao_datasetproperty_112.is_filter = False
    tao_datasetproperty_112.is_output = False
    tao_datasetproperty_112.description = u''
    tao_datasetproperty_112.group = u'Internal'
    tao_datasetproperty_112.order = 8L
    tao_datasetproperty_112 = save_or_locate(tao_datasetproperty_112)

    tao_datasetproperty_113 = DataSetProperty()
    tao_datasetproperty_113.name = u'treeindex'
    tao_datasetproperty_113.units = u''
    tao_datasetproperty_113.label = u'Tree Index'
    tao_datasetproperty_113.dataset = tao_dataset_2
    tao_datasetproperty_113.data_type = 0L
    tao_datasetproperty_113.is_computed = False
    tao_datasetproperty_113.is_filter = False
    tao_datasetproperty_113.is_output = False
    tao_datasetproperty_113.description = u''
    tao_datasetproperty_113.group = u'Internal'
    tao_datasetproperty_113.order = 8L
    tao_datasetproperty_113 = save_or_locate(tao_datasetproperty_113)

    tao_datasetproperty_114 = DataSetProperty()
    tao_datasetproperty_114.name = u'treeindex'
    tao_datasetproperty_114.units = u''
    tao_datasetproperty_114.label = u'Tree Index'
    tao_datasetproperty_114.dataset = tao_dataset_3
    tao_datasetproperty_114.data_type = 0L
    tao_datasetproperty_114.is_computed = False
    tao_datasetproperty_114.is_filter = False
    tao_datasetproperty_114.is_output = False
    tao_datasetproperty_114.description = u''
    tao_datasetproperty_114.group = u'Internal'
    tao_datasetproperty_114.order = 8L
    tao_datasetproperty_114 = save_or_locate(tao_datasetproperty_114)

    tao_datasetproperty_115 = DataSetProperty()
    tao_datasetproperty_115.name = u'ra'
    tao_datasetproperty_115.units = u'rad'
    tao_datasetproperty_115.label = u'Right Angle'
    tao_datasetproperty_115.dataset = tao_dataset_1
    tao_datasetproperty_115.data_type = 1L
    tao_datasetproperty_115.is_computed = False
    tao_datasetproperty_115.is_filter = True
    tao_datasetproperty_115.is_output = True
    tao_datasetproperty_115.description = u'Right Angle in the selected box/cone'
    tao_datasetproperty_115.group = u'Positions & Velocities'
    tao_datasetproperty_115.order = 1L
    tao_datasetproperty_115 = save_or_locate(tao_datasetproperty_115)

    tao_datasetproperty_116 = DataSetProperty()
    tao_datasetproperty_116.name = u'ra'
    tao_datasetproperty_116.units = u'rad'
    tao_datasetproperty_116.label = u'Right Angle'
    tao_datasetproperty_116.dataset = tao_dataset_2
    tao_datasetproperty_116.data_type = 1L
    tao_datasetproperty_116.is_computed = False
    tao_datasetproperty_116.is_filter = True
    tao_datasetproperty_116.is_output = True
    tao_datasetproperty_116.description = u'Right Angle in the selected box/cone'
    tao_datasetproperty_116.group = u'Positions & Velocities'
    tao_datasetproperty_116.order = 1L
    tao_datasetproperty_116 = save_or_locate(tao_datasetproperty_116)

    tao_datasetproperty_117 = DataSetProperty()
    tao_datasetproperty_117.name = u'ra'
    tao_datasetproperty_117.units = u'rad'
    tao_datasetproperty_117.label = u'Right Angle'
    tao_datasetproperty_117.dataset = tao_dataset_3
    tao_datasetproperty_117.data_type = 1L
    tao_datasetproperty_117.is_computed = False
    tao_datasetproperty_117.is_filter = True
    tao_datasetproperty_117.is_output = True
    tao_datasetproperty_117.description = u'Right Angle in the selected box/cone'
    tao_datasetproperty_117.group = u'Positions & Velocities'
    tao_datasetproperty_117.order = 1L
    tao_datasetproperty_117 = save_or_locate(tao_datasetproperty_117)

    tao_datasetproperty_118 = DataSetProperty()
    tao_datasetproperty_118.name = u'dec'
    tao_datasetproperty_118.units = u'rad'
    tao_datasetproperty_118.label = u'Declination'
    tao_datasetproperty_118.dataset = tao_dataset_1
    tao_datasetproperty_118.data_type = 1L
    tao_datasetproperty_118.is_computed = False
    tao_datasetproperty_118.is_filter = True
    tao_datasetproperty_118.is_output = True
    tao_datasetproperty_118.description = u'Declination in the selected box/cone'
    tao_datasetproperty_118.group = u'Positions & Velocities'
    tao_datasetproperty_118.order = 2L
    tao_datasetproperty_118 = save_or_locate(tao_datasetproperty_118)

    tao_datasetproperty_119 = DataSetProperty()
    tao_datasetproperty_119.name = u'dec'
    tao_datasetproperty_119.units = u'rad'
    tao_datasetproperty_119.label = u'Declination'
    tao_datasetproperty_119.dataset = tao_dataset_2
    tao_datasetproperty_119.data_type = 1L
    tao_datasetproperty_119.is_computed = False
    tao_datasetproperty_119.is_filter = True
    tao_datasetproperty_119.is_output = True
    tao_datasetproperty_119.description = u'Declination in the selected box/cone'
    tao_datasetproperty_119.group = u'Positions & Velocities'
    tao_datasetproperty_119.order = 2L
    tao_datasetproperty_119 = save_or_locate(tao_datasetproperty_119)

    tao_datasetproperty_120 = DataSetProperty()
    tao_datasetproperty_120.name = u'dec'
    tao_datasetproperty_120.units = u'rad'
    tao_datasetproperty_120.label = u'Declination'
    tao_datasetproperty_120.dataset = tao_dataset_3
    tao_datasetproperty_120.data_type = 1L
    tao_datasetproperty_120.is_computed = False
    tao_datasetproperty_120.is_filter = True
    tao_datasetproperty_120.is_output = True
    tao_datasetproperty_120.description = u'Declination in the selected box/cone'
    tao_datasetproperty_120.group = u'Positions & Velocities'
    tao_datasetproperty_120.order = 2L
    tao_datasetproperty_120 = save_or_locate(tao_datasetproperty_120)

    tao_datasetproperty_121 = DataSetProperty()
    tao_datasetproperty_121.name = u'redshift_apparent'
    tao_datasetproperty_121.units = u''
    tao_datasetproperty_121.label = u'Redshift (Apparent)'
    tao_datasetproperty_121.dataset = tao_dataset_1
    tao_datasetproperty_121.data_type = 1L
    tao_datasetproperty_121.is_computed = False
    tao_datasetproperty_121.is_filter = True
    tao_datasetproperty_121.is_output = True
    tao_datasetproperty_121.description = u'Redshift (Apparent) in the selected box/cone'
    tao_datasetproperty_121.group = u'Positions & Velocities'
    tao_datasetproperty_121.order = 3L
    tao_datasetproperty_121 = save_or_locate(tao_datasetproperty_121)

    tao_datasetproperty_122 = DataSetProperty()
    tao_datasetproperty_122.name = u'redshift_apparent'
    tao_datasetproperty_122.units = u''
    tao_datasetproperty_122.label = u'Redshift (Apparent)'
    tao_datasetproperty_122.dataset = tao_dataset_2
    tao_datasetproperty_122.data_type = 1L
    tao_datasetproperty_122.is_computed = False
    tao_datasetproperty_122.is_filter = True
    tao_datasetproperty_122.is_output = True
    tao_datasetproperty_122.description = u'Redshift (Apparent) in the selected box/cone'
    tao_datasetproperty_122.group = u'Positions & Velocities'
    tao_datasetproperty_122.order = 3L
    tao_datasetproperty_122 = save_or_locate(tao_datasetproperty_122)

    tao_datasetproperty_123 = DataSetProperty()
    tao_datasetproperty_123.name = u'redshift_apparent'
    tao_datasetproperty_123.units = u''
    tao_datasetproperty_123.label = u'Redshift (Apparent)'
    tao_datasetproperty_123.dataset = tao_dataset_3
    tao_datasetproperty_123.data_type = 1L
    tao_datasetproperty_123.is_computed = False
    tao_datasetproperty_123.is_filter = True
    tao_datasetproperty_123.is_output = True
    tao_datasetproperty_123.description = u'Redshift (Apparent) in the selected box/cone'
    tao_datasetproperty_123.group = u'Positions & Velocities'
    tao_datasetproperty_123.order = 3L
    tao_datasetproperty_123 = save_or_locate(tao_datasetproperty_123)

    tao_datasetproperty_124 = DataSetProperty()
    tao_datasetproperty_124.name = u'pos_x'
    tao_datasetproperty_124.units = u'10+6pc/h'
    tao_datasetproperty_124.label = u'x'
    tao_datasetproperty_124.dataset = tao_dataset_1
    tao_datasetproperty_124.data_type = 1L
    tao_datasetproperty_124.is_computed = False
    tao_datasetproperty_124.is_filter = True
    tao_datasetproperty_124.is_output = True
    tao_datasetproperty_124.description = u'X coordinate in the selected box/cone'
    tao_datasetproperty_124.group = u'Positions & Velocities'
    tao_datasetproperty_124.order = 4L
    tao_datasetproperty_124 = save_or_locate(tao_datasetproperty_124)

    tao_datasetproperty_125 = DataSetProperty()
    tao_datasetproperty_125.name = u'pos_x'
    tao_datasetproperty_125.units = u'10+6pc/h'
    tao_datasetproperty_125.label = u'x'
    tao_datasetproperty_125.dataset = tao_dataset_2
    tao_datasetproperty_125.data_type = 1L
    tao_datasetproperty_125.is_computed = False
    tao_datasetproperty_125.is_filter = True
    tao_datasetproperty_125.is_output = True
    tao_datasetproperty_125.description = u'X coordinate in the selected box/cone'
    tao_datasetproperty_125.group = u'Positions & Velocities'
    tao_datasetproperty_125.order = 4L
    tao_datasetproperty_125 = save_or_locate(tao_datasetproperty_125)

    tao_datasetproperty_126 = DataSetProperty()
    tao_datasetproperty_126.name = u'pos_x'
    tao_datasetproperty_126.units = u'10+6pc/h'
    tao_datasetproperty_126.label = u'x'
    tao_datasetproperty_126.dataset = tao_dataset_3
    tao_datasetproperty_126.data_type = 1L
    tao_datasetproperty_126.is_computed = False
    tao_datasetproperty_126.is_filter = True
    tao_datasetproperty_126.is_output = True
    tao_datasetproperty_126.description = u'X coordinate in the selected box/cone'
    tao_datasetproperty_126.group = u'Positions & Velocities'
    tao_datasetproperty_126.order = 4L
    tao_datasetproperty_126 = save_or_locate(tao_datasetproperty_126)

    tao_datasetproperty_127 = DataSetProperty()
    tao_datasetproperty_127.name = u'pos_y'
    tao_datasetproperty_127.units = u'10+6pc/h'
    tao_datasetproperty_127.label = u'y'
    tao_datasetproperty_127.dataset = tao_dataset_1
    tao_datasetproperty_127.data_type = 1L
    tao_datasetproperty_127.is_computed = False
    tao_datasetproperty_127.is_filter = True
    tao_datasetproperty_127.is_output = True
    tao_datasetproperty_127.description = u'Y coordinate in the selected box/cone'
    tao_datasetproperty_127.group = u'Positions & Velocities'
    tao_datasetproperty_127.order = 5L
    tao_datasetproperty_127 = save_or_locate(tao_datasetproperty_127)

    tao_datasetproperty_128 = DataSetProperty()
    tao_datasetproperty_128.name = u'pos_y'
    tao_datasetproperty_128.units = u'10+6pc/h'
    tao_datasetproperty_128.label = u'y'
    tao_datasetproperty_128.dataset = tao_dataset_2
    tao_datasetproperty_128.data_type = 1L
    tao_datasetproperty_128.is_computed = False
    tao_datasetproperty_128.is_filter = True
    tao_datasetproperty_128.is_output = True
    tao_datasetproperty_128.description = u'Y coordinate in the selected box/cone'
    tao_datasetproperty_128.group = u'Positions & Velocities'
    tao_datasetproperty_128.order = 5L
    tao_datasetproperty_128 = save_or_locate(tao_datasetproperty_128)

    tao_datasetproperty_129 = DataSetProperty()
    tao_datasetproperty_129.name = u'pos_y'
    tao_datasetproperty_129.units = u'10+6pc/h'
    tao_datasetproperty_129.label = u'y'
    tao_datasetproperty_129.dataset = tao_dataset_3
    tao_datasetproperty_129.data_type = 1L
    tao_datasetproperty_129.is_computed = False
    tao_datasetproperty_129.is_filter = True
    tao_datasetproperty_129.is_output = True
    tao_datasetproperty_129.description = u'Y coordinate in the selected box/cone'
    tao_datasetproperty_129.group = u'Positions & Velocities'
    tao_datasetproperty_129.order = 5L
    tao_datasetproperty_129 = save_or_locate(tao_datasetproperty_129)

    tao_datasetproperty_130 = DataSetProperty()
    tao_datasetproperty_130.name = u'pos_z'
    tao_datasetproperty_130.units = u'10+6pc/h'
    tao_datasetproperty_130.label = u'z'
    tao_datasetproperty_130.dataset = tao_dataset_1
    tao_datasetproperty_130.data_type = 1L
    tao_datasetproperty_130.is_computed = False
    tao_datasetproperty_130.is_filter = True
    tao_datasetproperty_130.is_output = True
    tao_datasetproperty_130.description = u'Z coordinate in the selected box/cone'
    tao_datasetproperty_130.group = u'Positions & Velocities'
    tao_datasetproperty_130.order = 6L
    tao_datasetproperty_130 = save_or_locate(tao_datasetproperty_130)

    tao_datasetproperty_131 = DataSetProperty()
    tao_datasetproperty_131.name = u'pos_z'
    tao_datasetproperty_131.units = u'10+6pc/h'
    tao_datasetproperty_131.label = u'z'
    tao_datasetproperty_131.dataset = tao_dataset_2
    tao_datasetproperty_131.data_type = 1L
    tao_datasetproperty_131.is_computed = False
    tao_datasetproperty_131.is_filter = True
    tao_datasetproperty_131.is_output = True
    tao_datasetproperty_131.description = u'Z coordinate in the selected box/cone'
    tao_datasetproperty_131.group = u'Positions & Velocities'
    tao_datasetproperty_131.order = 6L
    tao_datasetproperty_131 = save_or_locate(tao_datasetproperty_131)

    tao_datasetproperty_132 = DataSetProperty()
    tao_datasetproperty_132.name = u'pos_z'
    tao_datasetproperty_132.units = u'10+6pc/h'
    tao_datasetproperty_132.label = u'z'
    tao_datasetproperty_132.dataset = tao_dataset_3
    tao_datasetproperty_132.data_type = 1L
    tao_datasetproperty_132.is_computed = False
    tao_datasetproperty_132.is_filter = True
    tao_datasetproperty_132.is_output = True
    tao_datasetproperty_132.description = u'Z coordinate in the selected box/cone'
    tao_datasetproperty_132.group = u'Positions & Velocities'
    tao_datasetproperty_132.order = 6L
    tao_datasetproperty_132 = save_or_locate(tao_datasetproperty_132)

    tao_datasetproperty_133 = DataSetProperty()
    tao_datasetproperty_133.name = u'velx'
    tao_datasetproperty_133.units = u'km/s'
    tao_datasetproperty_133.label = u'x Velocity'
    tao_datasetproperty_133.dataset = tao_dataset_1
    tao_datasetproperty_133.data_type = 1L
    tao_datasetproperty_133.is_computed = False
    tao_datasetproperty_133.is_filter = True
    tao_datasetproperty_133.is_output = True
    tao_datasetproperty_133.description = u'X component of the galaxy/halo velocity'
    tao_datasetproperty_133.group = u'Positions & Velocities'
    tao_datasetproperty_133.order = 7L
    tao_datasetproperty_133 = save_or_locate(tao_datasetproperty_133)

    tao_datasetproperty_134 = DataSetProperty()
    tao_datasetproperty_134.name = u'velx'
    tao_datasetproperty_134.units = u'km/s'
    tao_datasetproperty_134.label = u'x Velocity'
    tao_datasetproperty_134.dataset = tao_dataset_2
    tao_datasetproperty_134.data_type = 1L
    tao_datasetproperty_134.is_computed = False
    tao_datasetproperty_134.is_filter = True
    tao_datasetproperty_134.is_output = True
    tao_datasetproperty_134.description = u'X component of the galaxy/halo velocity'
    tao_datasetproperty_134.group = u'Positions & Velocities'
    tao_datasetproperty_134.order = 7L
    tao_datasetproperty_134 = save_or_locate(tao_datasetproperty_134)

    tao_datasetproperty_135 = DataSetProperty()
    tao_datasetproperty_135.name = u'velx'
    tao_datasetproperty_135.units = u'km/s'
    tao_datasetproperty_135.label = u'x Velocity'
    tao_datasetproperty_135.dataset = tao_dataset_3
    tao_datasetproperty_135.data_type = 1L
    tao_datasetproperty_135.is_computed = False
    tao_datasetproperty_135.is_filter = True
    tao_datasetproperty_135.is_output = True
    tao_datasetproperty_135.description = u'X component of the galaxy/halo velocity'
    tao_datasetproperty_135.group = u'Positions & Velocities'
    tao_datasetproperty_135.order = 7L
    tao_datasetproperty_135 = save_or_locate(tao_datasetproperty_135)

    tao_datasetproperty_136 = DataSetProperty()
    tao_datasetproperty_136.name = u'vely'
    tao_datasetproperty_136.units = u'km/s'
    tao_datasetproperty_136.label = u'y Velocity'
    tao_datasetproperty_136.dataset = tao_dataset_1
    tao_datasetproperty_136.data_type = 1L
    tao_datasetproperty_136.is_computed = False
    tao_datasetproperty_136.is_filter = True
    tao_datasetproperty_136.is_output = True
    tao_datasetproperty_136.description = u'Y component of the galaxy/halo velocity'
    tao_datasetproperty_136.group = u'Positions & Velocities'
    tao_datasetproperty_136.order = 8L
    tao_datasetproperty_136 = save_or_locate(tao_datasetproperty_136)

    tao_datasetproperty_137 = DataSetProperty()
    tao_datasetproperty_137.name = u'vely'
    tao_datasetproperty_137.units = u'km/s'
    tao_datasetproperty_137.label = u'y Velocity'
    tao_datasetproperty_137.dataset = tao_dataset_2
    tao_datasetproperty_137.data_type = 1L
    tao_datasetproperty_137.is_computed = False
    tao_datasetproperty_137.is_filter = True
    tao_datasetproperty_137.is_output = True
    tao_datasetproperty_137.description = u'Y component of the galaxy/halo velocity'
    tao_datasetproperty_137.group = u'Positions & Velocities'
    tao_datasetproperty_137.order = 8L
    tao_datasetproperty_137 = save_or_locate(tao_datasetproperty_137)

    tao_datasetproperty_138 = DataSetProperty()
    tao_datasetproperty_138.name = u'vely'
    tao_datasetproperty_138.units = u'km/s'
    tao_datasetproperty_138.label = u'y Velocity'
    tao_datasetproperty_138.dataset = tao_dataset_3
    tao_datasetproperty_138.data_type = 1L
    tao_datasetproperty_138.is_computed = False
    tao_datasetproperty_138.is_filter = True
    tao_datasetproperty_138.is_output = True
    tao_datasetproperty_138.description = u'Y component of the galaxy/halo velocity'
    tao_datasetproperty_138.group = u'Positions & Velocities'
    tao_datasetproperty_138.order = 8L
    tao_datasetproperty_138 = save_or_locate(tao_datasetproperty_138)

    tao_datasetproperty_139 = DataSetProperty()
    tao_datasetproperty_139.name = u'velz'
    tao_datasetproperty_139.units = u'km/s'
    tao_datasetproperty_139.label = u'z Velocity'
    tao_datasetproperty_139.dataset = tao_dataset_1
    tao_datasetproperty_139.data_type = 1L
    tao_datasetproperty_139.is_computed = False
    tao_datasetproperty_139.is_filter = True
    tao_datasetproperty_139.is_output = True
    tao_datasetproperty_139.description = u'Z component of the galaxy/halo velocity'
    tao_datasetproperty_139.group = u'Positions & Velocities'
    tao_datasetproperty_139.order = 9L
    tao_datasetproperty_139 = save_or_locate(tao_datasetproperty_139)

    tao_datasetproperty_140 = DataSetProperty()
    tao_datasetproperty_140.name = u'velz'
    tao_datasetproperty_140.units = u'km/s'
    tao_datasetproperty_140.label = u'z Velocity'
    tao_datasetproperty_140.dataset = tao_dataset_2
    tao_datasetproperty_140.data_type = 1L
    tao_datasetproperty_140.is_computed = False
    tao_datasetproperty_140.is_filter = True
    tao_datasetproperty_140.is_output = True
    tao_datasetproperty_140.description = u'Z component of the galaxy/halo velocity'
    tao_datasetproperty_140.group = u'Positions & Velocities'
    tao_datasetproperty_140.order = 9L
    tao_datasetproperty_140 = save_or_locate(tao_datasetproperty_140)

    tao_datasetproperty_141 = DataSetProperty()
    tao_datasetproperty_141.name = u'velz'
    tao_datasetproperty_141.units = u'km/s'
    tao_datasetproperty_141.label = u'z Velocity'
    tao_datasetproperty_141.dataset = tao_dataset_3
    tao_datasetproperty_141.data_type = 1L
    tao_datasetproperty_141.is_computed = False
    tao_datasetproperty_141.is_filter = True
    tao_datasetproperty_141.is_output = True
    tao_datasetproperty_141.description = u'Z component of the galaxy/halo velocity'
    tao_datasetproperty_141.group = u'Positions & Velocities'
    tao_datasetproperty_141.order = 9L
    tao_datasetproperty_141 = save_or_locate(tao_datasetproperty_141)

    tao_datasetproperty_142 = DataSetProperty()
    tao_datasetproperty_142.name = u'snapnum'
    tao_datasetproperty_142.units = u''
    tao_datasetproperty_142.label = u'Snapshot Number'
    tao_datasetproperty_142.dataset = tao_dataset_1
    tao_datasetproperty_142.data_type = 0L
    tao_datasetproperty_142.is_computed = False
    tao_datasetproperty_142.is_filter = False
    tao_datasetproperty_142.is_output = True
    tao_datasetproperty_142.description = u'Simulation snapshot number'
    tao_datasetproperty_142.group = u'Simulation'
    tao_datasetproperty_142.order = 1L
    tao_datasetproperty_142 = save_or_locate(tao_datasetproperty_142)

    tao_datasetproperty_143 = DataSetProperty()
    tao_datasetproperty_143.name = u'snapnum'
    tao_datasetproperty_143.units = u''
    tao_datasetproperty_143.label = u'Snapshot Number'
    tao_datasetproperty_143.dataset = tao_dataset_2
    tao_datasetproperty_143.data_type = 0L
    tao_datasetproperty_143.is_computed = False
    tao_datasetproperty_143.is_filter = False
    tao_datasetproperty_143.is_output = True
    tao_datasetproperty_143.description = u'Simulation snapshot number'
    tao_datasetproperty_143.group = u'Simulation'
    tao_datasetproperty_143.order = 1L
    tao_datasetproperty_143 = save_or_locate(tao_datasetproperty_143)

    tao_datasetproperty_144 = DataSetProperty()
    tao_datasetproperty_144.name = u'snapnum'
    tao_datasetproperty_144.units = u''
    tao_datasetproperty_144.label = u'Snapshot Number'
    tao_datasetproperty_144.dataset = tao_dataset_3
    tao_datasetproperty_144.data_type = 0L
    tao_datasetproperty_144.is_computed = False
    tao_datasetproperty_144.is_filter = False
    tao_datasetproperty_144.is_output = True
    tao_datasetproperty_144.description = u'Simulation snapshot number'
    tao_datasetproperty_144.group = u'Simulation'
    tao_datasetproperty_144.order = 1L
    tao_datasetproperty_144 = save_or_locate(tao_datasetproperty_144)

    tao_datasetproperty_145 = DataSetProperty()
    tao_datasetproperty_145.name = u'globalindex'
    tao_datasetproperty_145.units = u''
    tao_datasetproperty_145.label = u'Galaxy ID'
    tao_datasetproperty_145.dataset = tao_dataset_1
    tao_datasetproperty_145.data_type = 2L
    tao_datasetproperty_145.is_computed = False
    tao_datasetproperty_145.is_filter = False
    tao_datasetproperty_145.is_output = True
    tao_datasetproperty_145.description = u'Galaxy ID'
    tao_datasetproperty_145.group = u'Simulation'
    tao_datasetproperty_145.order = 2L
    tao_datasetproperty_145 = save_or_locate(tao_datasetproperty_145)

    tao_datasetproperty_146 = DataSetProperty()
    tao_datasetproperty_146.name = u'globalindex'
    tao_datasetproperty_146.units = u''
    tao_datasetproperty_146.label = u'Galaxy ID'
    tao_datasetproperty_146.dataset = tao_dataset_2
    tao_datasetproperty_146.data_type = 2L
    tao_datasetproperty_146.is_computed = False
    tao_datasetproperty_146.is_filter = False
    tao_datasetproperty_146.is_output = True
    tao_datasetproperty_146.description = u'Galaxy ID'
    tao_datasetproperty_146.group = u'Simulation'
    tao_datasetproperty_146.order = 2L
    tao_datasetproperty_146 = save_or_locate(tao_datasetproperty_146)

    tao_datasetproperty_147 = DataSetProperty()
    tao_datasetproperty_147.name = u'globalindex'
    tao_datasetproperty_147.units = u''
    tao_datasetproperty_147.label = u'Galaxy ID'
    tao_datasetproperty_147.dataset = tao_dataset_3
    tao_datasetproperty_147.data_type = 2L
    tao_datasetproperty_147.is_computed = False
    tao_datasetproperty_147.is_filter = False
    tao_datasetproperty_147.is_output = True
    tao_datasetproperty_147.description = u'Galaxy ID'
    tao_datasetproperty_147.group = u'Simulation'
    tao_datasetproperty_147.order = 2L
    tao_datasetproperty_147 = save_or_locate(tao_datasetproperty_147)

    tao_datasetproperty_148 = DataSetProperty()
    tao_datasetproperty_148.name = u'haloindex'
    tao_datasetproperty_148.units = u''
    tao_datasetproperty_148.label = u'Halo ID'
    tao_datasetproperty_148.dataset = tao_dataset_1
    tao_datasetproperty_148.data_type = 0L
    tao_datasetproperty_148.is_computed = False
    tao_datasetproperty_148.is_filter = False
    tao_datasetproperty_148.is_output = True
    tao_datasetproperty_148.description = u'(sub)Halo ID'
    tao_datasetproperty_148.group = u'Simulation'
    tao_datasetproperty_148.order = 3L
    tao_datasetproperty_148 = save_or_locate(tao_datasetproperty_148)

    tao_datasetproperty_149 = DataSetProperty()
    tao_datasetproperty_149.name = u'haloindex'
    tao_datasetproperty_149.units = u''
    tao_datasetproperty_149.label = u'Halo ID'
    tao_datasetproperty_149.dataset = tao_dataset_2
    tao_datasetproperty_149.data_type = 0L
    tao_datasetproperty_149.is_computed = False
    tao_datasetproperty_149.is_filter = False
    tao_datasetproperty_149.is_output = True
    tao_datasetproperty_149.description = u'(sub)Halo ID'
    tao_datasetproperty_149.group = u'Simulation'
    tao_datasetproperty_149.order = 3L
    tao_datasetproperty_149 = save_or_locate(tao_datasetproperty_149)

    tao_datasetproperty_150 = DataSetProperty()
    tao_datasetproperty_150.name = u'haloindex'
    tao_datasetproperty_150.units = u''
    tao_datasetproperty_150.label = u'Halo ID'
    tao_datasetproperty_150.dataset = tao_dataset_3
    tao_datasetproperty_150.data_type = 0L
    tao_datasetproperty_150.is_computed = False
    tao_datasetproperty_150.is_filter = False
    tao_datasetproperty_150.is_output = True
    tao_datasetproperty_150.description = u'(sub)Halo ID'
    tao_datasetproperty_150.group = u'Simulation'
    tao_datasetproperty_150.order = 3L
    tao_datasetproperty_150 = save_or_locate(tao_datasetproperty_150)

    tao_datasetproperty_151 = DataSetProperty()
    tao_datasetproperty_151.name = u'centralgal'
    tao_datasetproperty_151.units = u''
    tao_datasetproperty_151.label = u'Central Galaxy ID'
    tao_datasetproperty_151.dataset = tao_dataset_1
    tao_datasetproperty_151.data_type = 0L
    tao_datasetproperty_151.is_computed = False
    tao_datasetproperty_151.is_filter = False
    tao_datasetproperty_151.is_output = True
    tao_datasetproperty_151.description = u'Central galaxy ID'
    tao_datasetproperty_151.group = u'Simulation'
    tao_datasetproperty_151.order = 4L
    tao_datasetproperty_151 = save_or_locate(tao_datasetproperty_151)

    tao_datasetproperty_152 = DataSetProperty()
    tao_datasetproperty_152.name = u'centralgal'
    tao_datasetproperty_152.units = u''
    tao_datasetproperty_152.label = u'Central Galaxy ID'
    tao_datasetproperty_152.dataset = tao_dataset_2
    tao_datasetproperty_152.data_type = 0L
    tao_datasetproperty_152.is_computed = False
    tao_datasetproperty_152.is_filter = False
    tao_datasetproperty_152.is_output = True
    tao_datasetproperty_152.description = u'Central galaxy ID'
    tao_datasetproperty_152.group = u'Simulation'
    tao_datasetproperty_152.order = 4L
    tao_datasetproperty_152 = save_or_locate(tao_datasetproperty_152)

    tao_datasetproperty_153 = DataSetProperty()
    tao_datasetproperty_153.name = u'centralgal'
    tao_datasetproperty_153.units = u''
    tao_datasetproperty_153.label = u'Central Galaxy ID'
    tao_datasetproperty_153.dataset = tao_dataset_3
    tao_datasetproperty_153.data_type = 0L
    tao_datasetproperty_153.is_computed = False
    tao_datasetproperty_153.is_filter = False
    tao_datasetproperty_153.is_output = True
    tao_datasetproperty_153.description = u'Central galaxy ID'
    tao_datasetproperty_153.group = u'Simulation'
    tao_datasetproperty_153.order = 4L
    tao_datasetproperty_153 = save_or_locate(tao_datasetproperty_153)

    #Processing model: Snapshot

    from tao.models import Snapshot

    tao_snapshot_1 = Snapshot()
    tao_snapshot_1.dataset = tao_dataset_1
    tao_snapshot_1.redshift = Decimal('0E-10')
    tao_snapshot_1 = save_or_locate(tao_snapshot_1)

    tao_snapshot_2 = Snapshot()
    tao_snapshot_2.dataset = tao_dataset_1
    tao_snapshot_2.redshift = Decimal('0.0199325417')
    tao_snapshot_2 = save_or_locate(tao_snapshot_2)

    tao_snapshot_3 = Snapshot()
    tao_snapshot_3.dataset = tao_dataset_1
    tao_snapshot_3.redshift = Decimal('0.0414030615')
    tao_snapshot_3 = save_or_locate(tao_snapshot_3)

    tao_snapshot_4 = Snapshot()
    tao_snapshot_4.dataset = tao_dataset_1
    tao_snapshot_4.redshift = Decimal('0.0644933969')
    tao_snapshot_4 = save_or_locate(tao_snapshot_4)

    tao_snapshot_5 = Snapshot()
    tao_snapshot_5.dataset = tao_dataset_1
    tao_snapshot_5.redshift = Decimal('0.0892878345')
    tao_snapshot_5 = save_or_locate(tao_snapshot_5)

    tao_snapshot_6 = Snapshot()
    tao_snapshot_6.dataset = tao_dataset_1
    tao_snapshot_6.redshift = Decimal('0.1158833723')
    tao_snapshot_6 = save_or_locate(tao_snapshot_6)

    tao_snapshot_7 = Snapshot()
    tao_snapshot_7.dataset = tao_dataset_1
    tao_snapshot_7.redshift = Decimal('0.1443834234')
    tao_snapshot_7 = save_or_locate(tao_snapshot_7)

    tao_snapshot_8 = Snapshot()
    tao_snapshot_8.dataset = tao_dataset_1
    tao_snapshot_8.redshift = Decimal('0.1748976077')
    tao_snapshot_8 = save_or_locate(tao_snapshot_8)

    tao_snapshot_9 = Snapshot()
    tao_snapshot_9.dataset = tao_dataset_1
    tao_snapshot_9.redshift = Decimal('0.2075486280')
    tao_snapshot_9 = save_or_locate(tao_snapshot_9)

    tao_snapshot_10 = Snapshot()
    tao_snapshot_10.dataset = tao_dataset_1
    tao_snapshot_10.redshift = Decimal('0.2424690843')
    tao_snapshot_10 = save_or_locate(tao_snapshot_10)

    tao_snapshot_11 = Snapshot()
    tao_snapshot_11.dataset = tao_dataset_1
    tao_snapshot_11.redshift = Decimal('0.2798017843')
    tao_snapshot_11 = save_or_locate(tao_snapshot_11)

    tao_snapshot_12 = Snapshot()
    tao_snapshot_12.dataset = tao_dataset_1
    tao_snapshot_12.redshift = Decimal('0.3197034362')
    tao_snapshot_12 = save_or_locate(tao_snapshot_12)

    tao_snapshot_13 = Snapshot()
    tao_snapshot_13.dataset = tao_dataset_1
    tao_snapshot_13.redshift = Decimal('0.3623402826')
    tao_snapshot_13 = save_or_locate(tao_snapshot_13)

    tao_snapshot_14 = Snapshot()
    tao_snapshot_14.dataset = tao_dataset_1
    tao_snapshot_14.redshift = Decimal('0.4078994422')
    tao_snapshot_14 = save_or_locate(tao_snapshot_14)

    tao_snapshot_15 = Snapshot()
    tao_snapshot_15.dataset = tao_dataset_1
    tao_snapshot_15.redshift = Decimal('0.4565772474')
    tao_snapshot_15 = save_or_locate(tao_snapshot_15)

    tao_snapshot_16 = Snapshot()
    tao_snapshot_16.dataset = tao_dataset_1
    tao_snapshot_16.redshift = Decimal('0.5085914282')
    tao_snapshot_16 = save_or_locate(tao_snapshot_16)

    tao_snapshot_17 = Snapshot()
    tao_snapshot_17.dataset = tao_dataset_1
    tao_snapshot_17.redshift = Decimal('0.5641766018')
    tao_snapshot_17 = save_or_locate(tao_snapshot_17)

    tao_snapshot_18 = Snapshot()
    tao_snapshot_18.dataset = tao_dataset_1
    tao_snapshot_18.redshift = Decimal('0.6235901149')
    tao_snapshot_18 = save_or_locate(tao_snapshot_18)

    tao_snapshot_19 = Snapshot()
    tao_snapshot_19.dataset = tao_dataset_1
    tao_snapshot_19.redshift = Decimal('0.6871088016')
    tao_snapshot_19 = save_or_locate(tao_snapshot_19)

    tao_snapshot_20 = Snapshot()
    tao_snapshot_20.dataset = tao_dataset_1
    tao_snapshot_20.redshift = Decimal('0.7550356360')
    tao_snapshot_20 = save_or_locate(tao_snapshot_20)

    tao_snapshot_21 = Snapshot()
    tao_snapshot_21.dataset = tao_dataset_1
    tao_snapshot_21.redshift = Decimal('0.8276991461')
    tao_snapshot_21 = save_or_locate(tao_snapshot_21)

    tao_snapshot_22 = Snapshot()
    tao_snapshot_22.dataset = tao_dataset_1
    tao_snapshot_22.redshift = Decimal('0.9054623890')
    tao_snapshot_22 = save_or_locate(tao_snapshot_22)

    tao_snapshot_23 = Snapshot()
    tao_snapshot_23.dataset = tao_dataset_1
    tao_snapshot_23.redshift = Decimal('0.9887081153')
    tao_snapshot_23 = save_or_locate(tao_snapshot_23)

    tao_snapshot_24 = Snapshot()
    tao_snapshot_24.dataset = tao_dataset_1
    tao_snapshot_24.redshift = Decimal('1.0778745836')
    tao_snapshot_24 = save_or_locate(tao_snapshot_24)

    tao_snapshot_25 = Snapshot()
    tao_snapshot_25.dataset = tao_dataset_1
    tao_snapshot_25.redshift = Decimal('1.1734169374')
    tao_snapshot_25 = save_or_locate(tao_snapshot_25)

    tao_snapshot_26 = Snapshot()
    tao_snapshot_26.dataset = tao_dataset_1
    tao_snapshot_26.redshift = Decimal('1.2758462165')
    tao_snapshot_26 = save_or_locate(tao_snapshot_26)

    tao_snapshot_27 = Snapshot()
    tao_snapshot_27.dataset = tao_dataset_1
    tao_snapshot_27.redshift = Decimal('1.3857181369')
    tao_snapshot_27 = save_or_locate(tao_snapshot_27)

    tao_snapshot_28 = Snapshot()
    tao_snapshot_28.dataset = tao_dataset_1
    tao_snapshot_28.redshift = Decimal('1.5036365321')
    tao_snapshot_28 = save_or_locate(tao_snapshot_28)

    tao_snapshot_29 = Snapshot()
    tao_snapshot_29.dataset = tao_dataset_1
    tao_snapshot_29.redshift = Decimal('1.6302707338')
    tao_snapshot_29 = save_or_locate(tao_snapshot_29)

    tao_snapshot_30 = Snapshot()
    tao_snapshot_30.dataset = tao_dataset_1
    tao_snapshot_30.redshift = Decimal('1.7663359051')
    tao_snapshot_30 = save_or_locate(tao_snapshot_30)

    tao_snapshot_31 = Snapshot()
    tao_snapshot_31.dataset = tao_dataset_1
    tao_snapshot_31.redshift = Decimal('1.9126326704')
    tao_snapshot_31 = save_or_locate(tao_snapshot_31)

    tao_snapshot_32 = Snapshot()
    tao_snapshot_32.dataset = tao_dataset_1
    tao_snapshot_32.redshift = Decimal('2.0700273232')
    tao_snapshot_32 = save_or_locate(tao_snapshot_32)

    tao_snapshot_33 = Snapshot()
    tao_snapshot_33.dataset = tao_dataset_1
    tao_snapshot_33.redshift = Decimal('2.2394854401')
    tao_snapshot_33 = save_or_locate(tao_snapshot_33)

    tao_snapshot_34 = Snapshot()
    tao_snapshot_34.dataset = tao_dataset_1
    tao_snapshot_34.redshift = Decimal('2.4220441238')
    tao_snapshot_34 = save_or_locate(tao_snapshot_34)

    tao_snapshot_35 = Snapshot()
    tao_snapshot_35.dataset = tao_dataset_1
    tao_snapshot_35.redshift = Decimal('2.6188615062')
    tao_snapshot_35 = save_or_locate(tao_snapshot_35)

    tao_snapshot_36 = Snapshot()
    tao_snapshot_36.dataset = tao_dataset_1
    tao_snapshot_36.redshift = Decimal('2.8311827627')
    tao_snapshot_36 = save_or_locate(tao_snapshot_36)

    tao_snapshot_37 = Snapshot()
    tao_snapshot_37.dataset = tao_dataset_1
    tao_snapshot_37.redshift = Decimal('3.0604190352')
    tao_snapshot_37 = save_or_locate(tao_snapshot_37)

    tao_snapshot_38 = Snapshot()
    tao_snapshot_38.dataset = tao_dataset_1
    tao_snapshot_38.redshift = Decimal('3.3080979317')
    tao_snapshot_38 = save_or_locate(tao_snapshot_38)

    tao_snapshot_39 = Snapshot()
    tao_snapshot_39.dataset = tao_dataset_1
    tao_snapshot_39.redshift = Decimal('3.5759051140')
    tao_snapshot_39 = save_or_locate(tao_snapshot_39)

    tao_snapshot_40 = Snapshot()
    tao_snapshot_40.dataset = tao_dataset_1
    tao_snapshot_40.redshift = Decimal('3.8656828256')
    tao_snapshot_40 = save_or_locate(tao_snapshot_40)

    tao_snapshot_41 = Snapshot()
    tao_snapshot_41.dataset = tao_dataset_1
    tao_snapshot_41.redshift = Decimal('4.1794685865')
    tao_snapshot_41 = save_or_locate(tao_snapshot_41)

    tao_snapshot_42 = Snapshot()
    tao_snapshot_42.dataset = tao_dataset_1
    tao_snapshot_42.redshift = Decimal('4.5195557862')
    tao_snapshot_42 = save_or_locate(tao_snapshot_42)

    tao_snapshot_43 = Snapshot()
    tao_snapshot_43.dataset = tao_dataset_1
    tao_snapshot_43.redshift = Decimal('4.8884492180')
    tao_snapshot_43 = save_or_locate(tao_snapshot_43)

    tao_snapshot_44 = Snapshot()
    tao_snapshot_44.dataset = tao_dataset_1
    tao_snapshot_44.redshift = Decimal('5.2888335472')
    tao_snapshot_44 = save_or_locate(tao_snapshot_44)

    tao_snapshot_45 = Snapshot()
    tao_snapshot_45.dataset = tao_dataset_1
    tao_snapshot_45.redshift = Decimal('5.7238643393')
    tao_snapshot_45 = save_or_locate(tao_snapshot_45)

    tao_snapshot_46 = Snapshot()
    tao_snapshot_46.dataset = tao_dataset_1
    tao_snapshot_46.redshift = Decimal('6.1968333933')
    tao_snapshot_46 = save_or_locate(tao_snapshot_46)

    tao_snapshot_47 = Snapshot()
    tao_snapshot_47.dataset = tao_dataset_1
    tao_snapshot_47.redshift = Decimal('6.7115866590')
    tao_snapshot_47 = save_or_locate(tao_snapshot_47)

    tao_snapshot_48 = Snapshot()
    tao_snapshot_48.dataset = tao_dataset_1
    tao_snapshot_48.redshift = Decimal('7.2721880765')
    tao_snapshot_48 = save_or_locate(tao_snapshot_48)

    tao_snapshot_49 = Snapshot()
    tao_snapshot_49.dataset = tao_dataset_1
    tao_snapshot_49.redshift = Decimal('7.8832036386')
    tao_snapshot_49 = save_or_locate(tao_snapshot_49)

    tao_snapshot_50 = Snapshot()
    tao_snapshot_50.dataset = tao_dataset_1
    tao_snapshot_50.redshift = Decimal('8.5499126183')
    tao_snapshot_50 = save_or_locate(tao_snapshot_50)

    tao_snapshot_51 = Snapshot()
    tao_snapshot_51.dataset = tao_dataset_1
    tao_snapshot_51.redshift = Decimal('9.2779148166')
    tao_snapshot_51 = save_or_locate(tao_snapshot_51)

    tao_snapshot_52 = Snapshot()
    tao_snapshot_52.dataset = tao_dataset_1
    tao_snapshot_52.redshift = Decimal('10.0734613425')
    tao_snapshot_52 = save_or_locate(tao_snapshot_52)

    tao_snapshot_53 = Snapshot()
    tao_snapshot_53.dataset = tao_dataset_1
    tao_snapshot_53.redshift = Decimal('10.9438638400')
    tao_snapshot_53 = save_or_locate(tao_snapshot_53)

    tao_snapshot_54 = Snapshot()
    tao_snapshot_54.dataset = tao_dataset_1
    tao_snapshot_54.redshift = Decimal('11.8965695125')
    tao_snapshot_54 = save_or_locate(tao_snapshot_54)

    tao_snapshot_55 = Snapshot()
    tao_snapshot_55.dataset = tao_dataset_1
    tao_snapshot_55.redshift = Decimal('12.9407795684')
    tao_snapshot_55 = save_or_locate(tao_snapshot_55)

    tao_snapshot_56 = Snapshot()
    tao_snapshot_56.dataset = tao_dataset_1
    tao_snapshot_56.redshift = Decimal('14.0859142818')
    tao_snapshot_56 = save_or_locate(tao_snapshot_56)

    tao_snapshot_57 = Snapshot()
    tao_snapshot_57.dataset = tao_dataset_1
    tao_snapshot_57.redshift = Decimal('15.3430738053')
    tao_snapshot_57 = save_or_locate(tao_snapshot_57)

    tao_snapshot_58 = Snapshot()
    tao_snapshot_58.dataset = tao_dataset_1
    tao_snapshot_58.redshift = Decimal('16.7245254258')
    tao_snapshot_58 = save_or_locate(tao_snapshot_58)

    tao_snapshot_59 = Snapshot()
    tao_snapshot_59.dataset = tao_dataset_1
    tao_snapshot_59.redshift = Decimal('18.2437217358')
    tao_snapshot_59 = save_or_locate(tao_snapshot_59)

    tao_snapshot_60 = Snapshot()
    tao_snapshot_60.dataset = tao_dataset_1
    tao_snapshot_60.redshift = Decimal('19.9156888582')
    tao_snapshot_60 = save_or_locate(tao_snapshot_60)

    tao_snapshot_61 = Snapshot()
    tao_snapshot_61.dataset = tao_dataset_1
    tao_snapshot_61.redshift = Decimal('30.0000620001')
    tao_snapshot_61 = save_or_locate(tao_snapshot_61)

    tao_snapshot_62 = Snapshot()
    tao_snapshot_62.dataset = tao_dataset_1
    tao_snapshot_62.redshift = Decimal('49.9995920033')
    tao_snapshot_62 = save_or_locate(tao_snapshot_62)

    tao_snapshot_63 = Snapshot()
    tao_snapshot_63.dataset = tao_dataset_1
    tao_snapshot_63.redshift = Decimal('79.9978940548')
    tao_snapshot_63 = save_or_locate(tao_snapshot_63)

    tao_snapshot_64 = Snapshot()
    tao_snapshot_64.dataset = tao_dataset_1
    tao_snapshot_64.redshift = Decimal('127.0000000000')
    tao_snapshot_64 = save_or_locate(tao_snapshot_64)

    tao_snapshot_65 = Snapshot()
    tao_snapshot_65.dataset = tao_dataset_2
    tao_snapshot_65.redshift = Decimal('0E-10')
    tao_snapshot_65 = save_or_locate(tao_snapshot_65)

    tao_snapshot_66 = Snapshot()
    tao_snapshot_66.dataset = tao_dataset_2
    tao_snapshot_66.redshift = Decimal('0.0199325417')
    tao_snapshot_66 = save_or_locate(tao_snapshot_66)

    tao_snapshot_67 = Snapshot()
    tao_snapshot_67.dataset = tao_dataset_2
    tao_snapshot_67.redshift = Decimal('0.0414030615')
    tao_snapshot_67 = save_or_locate(tao_snapshot_67)

    tao_snapshot_68 = Snapshot()
    tao_snapshot_68.dataset = tao_dataset_2
    tao_snapshot_68.redshift = Decimal('0.0644933969')
    tao_snapshot_68 = save_or_locate(tao_snapshot_68)

    tao_snapshot_69 = Snapshot()
    tao_snapshot_69.dataset = tao_dataset_2
    tao_snapshot_69.redshift = Decimal('0.0892878345')
    tao_snapshot_69 = save_or_locate(tao_snapshot_69)

    tao_snapshot_70 = Snapshot()
    tao_snapshot_70.dataset = tao_dataset_2
    tao_snapshot_70.redshift = Decimal('0.1158833723')
    tao_snapshot_70 = save_or_locate(tao_snapshot_70)

    tao_snapshot_71 = Snapshot()
    tao_snapshot_71.dataset = tao_dataset_2
    tao_snapshot_71.redshift = Decimal('0.1443834234')
    tao_snapshot_71 = save_or_locate(tao_snapshot_71)

    tao_snapshot_72 = Snapshot()
    tao_snapshot_72.dataset = tao_dataset_2
    tao_snapshot_72.redshift = Decimal('0.1748976077')
    tao_snapshot_72 = save_or_locate(tao_snapshot_72)

    tao_snapshot_73 = Snapshot()
    tao_snapshot_73.dataset = tao_dataset_2
    tao_snapshot_73.redshift = Decimal('0.2075486280')
    tao_snapshot_73 = save_or_locate(tao_snapshot_73)

    tao_snapshot_74 = Snapshot()
    tao_snapshot_74.dataset = tao_dataset_2
    tao_snapshot_74.redshift = Decimal('0.2424690843')
    tao_snapshot_74 = save_or_locate(tao_snapshot_74)

    tao_snapshot_75 = Snapshot()
    tao_snapshot_75.dataset = tao_dataset_2
    tao_snapshot_75.redshift = Decimal('0.2798017843')
    tao_snapshot_75 = save_or_locate(tao_snapshot_75)

    tao_snapshot_76 = Snapshot()
    tao_snapshot_76.dataset = tao_dataset_2
    tao_snapshot_76.redshift = Decimal('0.3197034362')
    tao_snapshot_76 = save_or_locate(tao_snapshot_76)

    tao_snapshot_77 = Snapshot()
    tao_snapshot_77.dataset = tao_dataset_2
    tao_snapshot_77.redshift = Decimal('0.3623402826')
    tao_snapshot_77 = save_or_locate(tao_snapshot_77)

    tao_snapshot_78 = Snapshot()
    tao_snapshot_78.dataset = tao_dataset_2
    tao_snapshot_78.redshift = Decimal('0.4078994422')
    tao_snapshot_78 = save_or_locate(tao_snapshot_78)

    tao_snapshot_79 = Snapshot()
    tao_snapshot_79.dataset = tao_dataset_2
    tao_snapshot_79.redshift = Decimal('0.4565772474')
    tao_snapshot_79 = save_or_locate(tao_snapshot_79)

    tao_snapshot_80 = Snapshot()
    tao_snapshot_80.dataset = tao_dataset_2
    tao_snapshot_80.redshift = Decimal('0.5085914282')
    tao_snapshot_80 = save_or_locate(tao_snapshot_80)

    tao_snapshot_81 = Snapshot()
    tao_snapshot_81.dataset = tao_dataset_2
    tao_snapshot_81.redshift = Decimal('0.5641766018')
    tao_snapshot_81 = save_or_locate(tao_snapshot_81)

    tao_snapshot_82 = Snapshot()
    tao_snapshot_82.dataset = tao_dataset_2
    tao_snapshot_82.redshift = Decimal('0.6235901149')
    tao_snapshot_82 = save_or_locate(tao_snapshot_82)

    tao_snapshot_83 = Snapshot()
    tao_snapshot_83.dataset = tao_dataset_2
    tao_snapshot_83.redshift = Decimal('0.6871088016')
    tao_snapshot_83 = save_or_locate(tao_snapshot_83)

    tao_snapshot_84 = Snapshot()
    tao_snapshot_84.dataset = tao_dataset_2
    tao_snapshot_84.redshift = Decimal('0.7550356360')
    tao_snapshot_84 = save_or_locate(tao_snapshot_84)

    tao_snapshot_85 = Snapshot()
    tao_snapshot_85.dataset = tao_dataset_2
    tao_snapshot_85.redshift = Decimal('0.8276991461')
    tao_snapshot_85 = save_or_locate(tao_snapshot_85)

    tao_snapshot_86 = Snapshot()
    tao_snapshot_86.dataset = tao_dataset_2
    tao_snapshot_86.redshift = Decimal('0.9054623890')
    tao_snapshot_86 = save_or_locate(tao_snapshot_86)

    tao_snapshot_87 = Snapshot()
    tao_snapshot_87.dataset = tao_dataset_2
    tao_snapshot_87.redshift = Decimal('0.9887081153')
    tao_snapshot_87 = save_or_locate(tao_snapshot_87)

    tao_snapshot_88 = Snapshot()
    tao_snapshot_88.dataset = tao_dataset_2
    tao_snapshot_88.redshift = Decimal('1.0778745836')
    tao_snapshot_88 = save_or_locate(tao_snapshot_88)

    tao_snapshot_89 = Snapshot()
    tao_snapshot_89.dataset = tao_dataset_2
    tao_snapshot_89.redshift = Decimal('1.1734169374')
    tao_snapshot_89 = save_or_locate(tao_snapshot_89)

    tao_snapshot_90 = Snapshot()
    tao_snapshot_90.dataset = tao_dataset_2
    tao_snapshot_90.redshift = Decimal('1.2758462165')
    tao_snapshot_90 = save_or_locate(tao_snapshot_90)

    tao_snapshot_91 = Snapshot()
    tao_snapshot_91.dataset = tao_dataset_2
    tao_snapshot_91.redshift = Decimal('1.3857181369')
    tao_snapshot_91 = save_or_locate(tao_snapshot_91)

    tao_snapshot_92 = Snapshot()
    tao_snapshot_92.dataset = tao_dataset_2
    tao_snapshot_92.redshift = Decimal('1.5036365321')
    tao_snapshot_92 = save_or_locate(tao_snapshot_92)

    tao_snapshot_93 = Snapshot()
    tao_snapshot_93.dataset = tao_dataset_2
    tao_snapshot_93.redshift = Decimal('1.6302707338')
    tao_snapshot_93 = save_or_locate(tao_snapshot_93)

    tao_snapshot_94 = Snapshot()
    tao_snapshot_94.dataset = tao_dataset_2
    tao_snapshot_94.redshift = Decimal('1.7663359051')
    tao_snapshot_94 = save_or_locate(tao_snapshot_94)

    tao_snapshot_95 = Snapshot()
    tao_snapshot_95.dataset = tao_dataset_2
    tao_snapshot_95.redshift = Decimal('1.9126326704')
    tao_snapshot_95 = save_or_locate(tao_snapshot_95)

    tao_snapshot_96 = Snapshot()
    tao_snapshot_96.dataset = tao_dataset_2
    tao_snapshot_96.redshift = Decimal('2.0700273232')
    tao_snapshot_96 = save_or_locate(tao_snapshot_96)

    tao_snapshot_97 = Snapshot()
    tao_snapshot_97.dataset = tao_dataset_2
    tao_snapshot_97.redshift = Decimal('2.2394854401')
    tao_snapshot_97 = save_or_locate(tao_snapshot_97)

    tao_snapshot_98 = Snapshot()
    tao_snapshot_98.dataset = tao_dataset_2
    tao_snapshot_98.redshift = Decimal('2.4220441238')
    tao_snapshot_98 = save_or_locate(tao_snapshot_98)

    tao_snapshot_99 = Snapshot()
    tao_snapshot_99.dataset = tao_dataset_2
    tao_snapshot_99.redshift = Decimal('2.6188615062')
    tao_snapshot_99 = save_or_locate(tao_snapshot_99)

    tao_snapshot_100 = Snapshot()
    tao_snapshot_100.dataset = tao_dataset_2
    tao_snapshot_100.redshift = Decimal('2.8311827627')
    tao_snapshot_100 = save_or_locate(tao_snapshot_100)

    tao_snapshot_101 = Snapshot()
    tao_snapshot_101.dataset = tao_dataset_2
    tao_snapshot_101.redshift = Decimal('3.0604190352')
    tao_snapshot_101 = save_or_locate(tao_snapshot_101)

    tao_snapshot_102 = Snapshot()
    tao_snapshot_102.dataset = tao_dataset_2
    tao_snapshot_102.redshift = Decimal('3.3080979317')
    tao_snapshot_102 = save_or_locate(tao_snapshot_102)

    tao_snapshot_103 = Snapshot()
    tao_snapshot_103.dataset = tao_dataset_2
    tao_snapshot_103.redshift = Decimal('3.5759051140')
    tao_snapshot_103 = save_or_locate(tao_snapshot_103)

    tao_snapshot_104 = Snapshot()
    tao_snapshot_104.dataset = tao_dataset_2
    tao_snapshot_104.redshift = Decimal('3.8656828256')
    tao_snapshot_104 = save_or_locate(tao_snapshot_104)

    tao_snapshot_105 = Snapshot()
    tao_snapshot_105.dataset = tao_dataset_2
    tao_snapshot_105.redshift = Decimal('4.1794685865')
    tao_snapshot_105 = save_or_locate(tao_snapshot_105)

    tao_snapshot_106 = Snapshot()
    tao_snapshot_106.dataset = tao_dataset_2
    tao_snapshot_106.redshift = Decimal('4.5195557862')
    tao_snapshot_106 = save_or_locate(tao_snapshot_106)

    tao_snapshot_107 = Snapshot()
    tao_snapshot_107.dataset = tao_dataset_2
    tao_snapshot_107.redshift = Decimal('4.8884492180')
    tao_snapshot_107 = save_or_locate(tao_snapshot_107)

    tao_snapshot_108 = Snapshot()
    tao_snapshot_108.dataset = tao_dataset_2
    tao_snapshot_108.redshift = Decimal('5.2888335472')
    tao_snapshot_108 = save_or_locate(tao_snapshot_108)

    tao_snapshot_109 = Snapshot()
    tao_snapshot_109.dataset = tao_dataset_2
    tao_snapshot_109.redshift = Decimal('5.7238643393')
    tao_snapshot_109 = save_or_locate(tao_snapshot_109)

    tao_snapshot_110 = Snapshot()
    tao_snapshot_110.dataset = tao_dataset_2
    tao_snapshot_110.redshift = Decimal('6.1968333933')
    tao_snapshot_110 = save_or_locate(tao_snapshot_110)

    tao_snapshot_111 = Snapshot()
    tao_snapshot_111.dataset = tao_dataset_2
    tao_snapshot_111.redshift = Decimal('6.7115866590')
    tao_snapshot_111 = save_or_locate(tao_snapshot_111)

    tao_snapshot_112 = Snapshot()
    tao_snapshot_112.dataset = tao_dataset_2
    tao_snapshot_112.redshift = Decimal('7.2721880765')
    tao_snapshot_112 = save_or_locate(tao_snapshot_112)

    tao_snapshot_113 = Snapshot()
    tao_snapshot_113.dataset = tao_dataset_2
    tao_snapshot_113.redshift = Decimal('7.8832036386')
    tao_snapshot_113 = save_or_locate(tao_snapshot_113)

    tao_snapshot_114 = Snapshot()
    tao_snapshot_114.dataset = tao_dataset_2
    tao_snapshot_114.redshift = Decimal('8.5499126183')
    tao_snapshot_114 = save_or_locate(tao_snapshot_114)

    tao_snapshot_115 = Snapshot()
    tao_snapshot_115.dataset = tao_dataset_2
    tao_snapshot_115.redshift = Decimal('9.2779148166')
    tao_snapshot_115 = save_or_locate(tao_snapshot_115)

    tao_snapshot_116 = Snapshot()
    tao_snapshot_116.dataset = tao_dataset_2
    tao_snapshot_116.redshift = Decimal('10.0734613425')
    tao_snapshot_116 = save_or_locate(tao_snapshot_116)

    tao_snapshot_117 = Snapshot()
    tao_snapshot_117.dataset = tao_dataset_2
    tao_snapshot_117.redshift = Decimal('10.9438638400')
    tao_snapshot_117 = save_or_locate(tao_snapshot_117)

    tao_snapshot_118 = Snapshot()
    tao_snapshot_118.dataset = tao_dataset_2
    tao_snapshot_118.redshift = Decimal('11.8965695125')
    tao_snapshot_118 = save_or_locate(tao_snapshot_118)

    tao_snapshot_119 = Snapshot()
    tao_snapshot_119.dataset = tao_dataset_2
    tao_snapshot_119.redshift = Decimal('12.9407795684')
    tao_snapshot_119 = save_or_locate(tao_snapshot_119)

    tao_snapshot_120 = Snapshot()
    tao_snapshot_120.dataset = tao_dataset_2
    tao_snapshot_120.redshift = Decimal('14.0859142818')
    tao_snapshot_120 = save_or_locate(tao_snapshot_120)

    tao_snapshot_121 = Snapshot()
    tao_snapshot_121.dataset = tao_dataset_2
    tao_snapshot_121.redshift = Decimal('15.3430738053')
    tao_snapshot_121 = save_or_locate(tao_snapshot_121)

    tao_snapshot_122 = Snapshot()
    tao_snapshot_122.dataset = tao_dataset_2
    tao_snapshot_122.redshift = Decimal('16.7245254258')
    tao_snapshot_122 = save_or_locate(tao_snapshot_122)

    tao_snapshot_123 = Snapshot()
    tao_snapshot_123.dataset = tao_dataset_2
    tao_snapshot_123.redshift = Decimal('18.2437217358')
    tao_snapshot_123 = save_or_locate(tao_snapshot_123)

    tao_snapshot_124 = Snapshot()
    tao_snapshot_124.dataset = tao_dataset_2
    tao_snapshot_124.redshift = Decimal('19.9156888582')
    tao_snapshot_124 = save_or_locate(tao_snapshot_124)

    tao_snapshot_125 = Snapshot()
    tao_snapshot_125.dataset = tao_dataset_2
    tao_snapshot_125.redshift = Decimal('30.0000620001')
    tao_snapshot_125 = save_or_locate(tao_snapshot_125)

    tao_snapshot_126 = Snapshot()
    tao_snapshot_126.dataset = tao_dataset_2
    tao_snapshot_126.redshift = Decimal('49.9995920033')
    tao_snapshot_126 = save_or_locate(tao_snapshot_126)

    tao_snapshot_127 = Snapshot()
    tao_snapshot_127.dataset = tao_dataset_2
    tao_snapshot_127.redshift = Decimal('79.9978940548')
    tao_snapshot_127 = save_or_locate(tao_snapshot_127)

    tao_snapshot_128 = Snapshot()
    tao_snapshot_128.dataset = tao_dataset_2
    tao_snapshot_128.redshift = Decimal('127.0000000000')
    tao_snapshot_128 = save_or_locate(tao_snapshot_128)

    tao_snapshot_129 = Snapshot()
    tao_snapshot_129.dataset = tao_dataset_3
    tao_snapshot_129.redshift = Decimal('0E-10')
    tao_snapshot_129 = save_or_locate(tao_snapshot_129)

    tao_snapshot_130 = Snapshot()
    tao_snapshot_130.dataset = tao_dataset_3
    tao_snapshot_130.redshift = Decimal('0.0027073097')
    tao_snapshot_130 = save_or_locate(tao_snapshot_130)

    tao_snapshot_131 = Snapshot()
    tao_snapshot_131.dataset = tao_dataset_3
    tao_snapshot_131.redshift = Decimal('0.0057326763')
    tao_snapshot_131 = save_or_locate(tao_snapshot_131)

    tao_snapshot_132 = Snapshot()
    tao_snapshot_132.dataset = tao_dataset_3
    tao_snapshot_132.redshift = Decimal('0.0087763543')
    tao_snapshot_132 = save_or_locate(tao_snapshot_132)

    tao_snapshot_133 = Snapshot()
    tao_snapshot_133.dataset = tao_dataset_3
    tao_snapshot_133.redshift = Decimal('0.0118385106')
    tao_snapshot_133 = save_or_locate(tao_snapshot_133)

    tao_snapshot_134 = Snapshot()
    tao_snapshot_134.dataset = tao_dataset_3
    tao_snapshot_134.redshift = Decimal('0.0149193139')
    tao_snapshot_134 = save_or_locate(tao_snapshot_134)

    tao_snapshot_135 = Snapshot()
    tao_snapshot_135.dataset = tao_dataset_3
    tao_snapshot_135.redshift = Decimal('0.0180189352')
    tao_snapshot_135 = save_or_locate(tao_snapshot_135)

    tao_snapshot_136 = Snapshot()
    tao_snapshot_136.dataset = tao_dataset_3
    tao_snapshot_136.redshift = Decimal('0.0211375472')
    tao_snapshot_136 = save_or_locate(tao_snapshot_136)

    tao_snapshot_137 = Snapshot()
    tao_snapshot_137.dataset = tao_dataset_3
    tao_snapshot_137.redshift = Decimal('0.0242753252')
    tao_snapshot_137 = save_or_locate(tao_snapshot_137)

    tao_snapshot_138 = Snapshot()
    tao_snapshot_138.dataset = tao_dataset_3
    tao_snapshot_138.redshift = Decimal('0.0274324463')
    tao_snapshot_138 = save_or_locate(tao_snapshot_138)

    tao_snapshot_139 = Snapshot()
    tao_snapshot_139.dataset = tao_dataset_3
    tao_snapshot_139.redshift = Decimal('0.0306090900')
    tao_snapshot_139 = save_or_locate(tao_snapshot_139)

    tao_snapshot_140 = Snapshot()
    tao_snapshot_140.dataset = tao_dataset_3
    tao_snapshot_140.redshift = Decimal('0.0338054378')
    tao_snapshot_140 = save_or_locate(tao_snapshot_140)

    tao_snapshot_141 = Snapshot()
    tao_snapshot_141.dataset = tao_dataset_3
    tao_snapshot_141.redshift = Decimal('0.0370216738')
    tao_snapshot_141 = save_or_locate(tao_snapshot_141)

    tao_snapshot_142 = Snapshot()
    tao_snapshot_142.dataset = tao_dataset_3
    tao_snapshot_142.redshift = Decimal('0.0402579840')
    tao_snapshot_142 = save_or_locate(tao_snapshot_142)

    tao_snapshot_143 = Snapshot()
    tao_snapshot_143.dataset = tao_dataset_3
    tao_snapshot_143.redshift = Decimal('0.0435145570')
    tao_snapshot_143 = save_or_locate(tao_snapshot_143)

    tao_snapshot_144 = Snapshot()
    tao_snapshot_144.dataset = tao_dataset_3
    tao_snapshot_144.redshift = Decimal('0.0500892576')
    tao_snapshot_144 = save_or_locate(tao_snapshot_144)

    tao_snapshot_145 = Snapshot()
    tao_snapshot_145.dataset = tao_dataset_3
    tao_snapshot_145.redshift = Decimal('0.0534077741')
    tao_snapshot_145 = save_or_locate(tao_snapshot_145)

    tao_snapshot_146 = Snapshot()
    tao_snapshot_146.dataset = tao_dataset_3
    tao_snapshot_146.redshift = Decimal('0.0567473317')
    tao_snapshot_146 = save_or_locate(tao_snapshot_146)

    tao_snapshot_147 = Snapshot()
    tao_snapshot_147.dataset = tao_dataset_3
    tao_snapshot_147.redshift = Decimal('0.0601081310')
    tao_snapshot_147 = save_or_locate(tao_snapshot_147)

    tao_snapshot_148 = Snapshot()
    tao_snapshot_148.dataset = tao_dataset_3
    tao_snapshot_148.redshift = Decimal('0.0668942708')
    tao_snapshot_148 = save_or_locate(tao_snapshot_148)

    tao_snapshot_149 = Snapshot()
    tao_snapshot_149.dataset = tao_dataset_3
    tao_snapshot_149.redshift = Decimal('0.0703200257')
    tao_snapshot_149 = save_or_locate(tao_snapshot_149)

    tao_snapshot_150 = Snapshot()
    tao_snapshot_150.dataset = tao_dataset_3
    tao_snapshot_150.redshift = Decimal('0.0737678514')
    tao_snapshot_150 = save_or_locate(tao_snapshot_150)

    tao_snapshot_151 = Snapshot()
    tao_snapshot_151.dataset = tao_dataset_3
    tao_snapshot_151.redshift = Decimal('0.0772379619')
    tao_snapshot_151 = save_or_locate(tao_snapshot_151)

    tao_snapshot_152 = Snapshot()
    tao_snapshot_152.dataset = tao_dataset_3
    tao_snapshot_152.redshift = Decimal('0.0807305739')
    tao_snapshot_152 = save_or_locate(tao_snapshot_152)

    tao_snapshot_153 = Snapshot()
    tao_snapshot_153.dataset = tao_dataset_3
    tao_snapshot_153.redshift = Decimal('0.0842459070')
    tao_snapshot_153 = save_or_locate(tao_snapshot_153)

    tao_snapshot_154 = Snapshot()
    tao_snapshot_154.dataset = tao_dataset_3
    tao_snapshot_154.redshift = Decimal('0.0877841836')
    tao_snapshot_154 = save_or_locate(tao_snapshot_154)

    tao_snapshot_155 = Snapshot()
    tao_snapshot_155.dataset = tao_dataset_3
    tao_snapshot_155.redshift = Decimal('0.0913456292')
    tao_snapshot_155 = save_or_locate(tao_snapshot_155)

    tao_snapshot_156 = Snapshot()
    tao_snapshot_156.dataset = tao_dataset_3
    tao_snapshot_156.redshift = Decimal('0.0949304719')
    tao_snapshot_156 = save_or_locate(tao_snapshot_156)

    tao_snapshot_157 = Snapshot()
    tao_snapshot_157.dataset = tao_dataset_3
    tao_snapshot_157.redshift = Decimal('0.0985389432')
    tao_snapshot_157 = save_or_locate(tao_snapshot_157)

    tao_snapshot_158 = Snapshot()
    tao_snapshot_158.dataset = tao_dataset_3
    tao_snapshot_158.redshift = Decimal('0.1021712774')
    tao_snapshot_158 = save_or_locate(tao_snapshot_158)

    tao_snapshot_159 = Snapshot()
    tao_snapshot_159.dataset = tao_dataset_3
    tao_snapshot_159.redshift = Decimal('0.1058277120')
    tao_snapshot_159 = save_or_locate(tao_snapshot_159)

    tao_snapshot_160 = Snapshot()
    tao_snapshot_160.dataset = tao_dataset_3
    tao_snapshot_160.redshift = Decimal('0.1095084877')
    tao_snapshot_160 = save_or_locate(tao_snapshot_160)

    tao_snapshot_161 = Snapshot()
    tao_snapshot_161.dataset = tao_dataset_3
    tao_snapshot_161.redshift = Decimal('0.1132138484')
    tao_snapshot_161 = save_or_locate(tao_snapshot_161)

    tao_snapshot_162 = Snapshot()
    tao_snapshot_162.dataset = tao_dataset_3
    tao_snapshot_162.redshift = Decimal('0.1169440411')
    tao_snapshot_162 = save_or_locate(tao_snapshot_162)

    tao_snapshot_163 = Snapshot()
    tao_snapshot_163.dataset = tao_dataset_3
    tao_snapshot_163.redshift = Decimal('0.1206993164')
    tao_snapshot_163 = save_or_locate(tao_snapshot_163)

    tao_snapshot_164 = Snapshot()
    tao_snapshot_164.dataset = tao_dataset_3
    tao_snapshot_164.redshift = Decimal('0.1244799280')
    tao_snapshot_164 = save_or_locate(tao_snapshot_164)

    tao_snapshot_165 = Snapshot()
    tao_snapshot_165.dataset = tao_dataset_3
    tao_snapshot_165.redshift = Decimal('0.1282861334')
    tao_snapshot_165 = save_or_locate(tao_snapshot_165)

    tao_snapshot_166 = Snapshot()
    tao_snapshot_166.dataset = tao_dataset_3
    tao_snapshot_166.redshift = Decimal('0.1321181931')
    tao_snapshot_166 = save_or_locate(tao_snapshot_166)

    tao_snapshot_167 = Snapshot()
    tao_snapshot_167.dataset = tao_dataset_3
    tao_snapshot_167.redshift = Decimal('0.1359763717')
    tao_snapshot_167 = save_or_locate(tao_snapshot_167)

    tao_snapshot_168 = Snapshot()
    tao_snapshot_168.dataset = tao_dataset_3
    tao_snapshot_168.redshift = Decimal('0.1398609370')
    tao_snapshot_168 = save_or_locate(tao_snapshot_168)

    tao_snapshot_169 = Snapshot()
    tao_snapshot_169.dataset = tao_dataset_3
    tao_snapshot_169.redshift = Decimal('0.1437721606')
    tao_snapshot_169 = save_or_locate(tao_snapshot_169)

    tao_snapshot_170 = Snapshot()
    tao_snapshot_170.dataset = tao_dataset_3
    tao_snapshot_170.redshift = Decimal('0.1477103179')
    tao_snapshot_170 = save_or_locate(tao_snapshot_170)

    tao_snapshot_171 = Snapshot()
    tao_snapshot_171.dataset = tao_dataset_3
    tao_snapshot_171.redshift = Decimal('0.1516756881')
    tao_snapshot_171 = save_or_locate(tao_snapshot_171)

    tao_snapshot_172 = Snapshot()
    tao_snapshot_172.dataset = tao_dataset_3
    tao_snapshot_172.redshift = Decimal('0.1556685543')
    tao_snapshot_172 = save_or_locate(tao_snapshot_172)

    tao_snapshot_173 = Snapshot()
    tao_snapshot_173.dataset = tao_dataset_3
    tao_snapshot_173.redshift = Decimal('0.1596892033')
    tao_snapshot_173 = save_or_locate(tao_snapshot_173)

    tao_snapshot_174 = Snapshot()
    tao_snapshot_174.dataset = tao_dataset_3
    tao_snapshot_174.redshift = Decimal('0.1637379262')
    tao_snapshot_174 = save_or_locate(tao_snapshot_174)

    tao_snapshot_175 = Snapshot()
    tao_snapshot_175.dataset = tao_dataset_3
    tao_snapshot_175.redshift = Decimal('0.1678150181')
    tao_snapshot_175 = save_or_locate(tao_snapshot_175)

    tao_snapshot_176 = Snapshot()
    tao_snapshot_176.dataset = tao_dataset_3
    tao_snapshot_176.redshift = Decimal('0.1719207782')
    tao_snapshot_176 = save_or_locate(tao_snapshot_176)

    tao_snapshot_177 = Snapshot()
    tao_snapshot_177.dataset = tao_dataset_3
    tao_snapshot_177.redshift = Decimal('0.1760555098')
    tao_snapshot_177 = save_or_locate(tao_snapshot_177)

    tao_snapshot_178 = Snapshot()
    tao_snapshot_178.dataset = tao_dataset_3
    tao_snapshot_178.redshift = Decimal('0.1802195208')
    tao_snapshot_178 = save_or_locate(tao_snapshot_178)

    tao_snapshot_179 = Snapshot()
    tao_snapshot_179.dataset = tao_dataset_3
    tao_snapshot_179.redshift = Decimal('0.1844131233')
    tao_snapshot_179 = save_or_locate(tao_snapshot_179)

    tao_snapshot_180 = Snapshot()
    tao_snapshot_180.dataset = tao_dataset_3
    tao_snapshot_180.redshift = Decimal('0.1886366338')
    tao_snapshot_180 = save_or_locate(tao_snapshot_180)

    tao_snapshot_181 = Snapshot()
    tao_snapshot_181.dataset = tao_dataset_3
    tao_snapshot_181.redshift = Decimal('0.1928903734')
    tao_snapshot_181 = save_or_locate(tao_snapshot_181)

    tao_snapshot_182 = Snapshot()
    tao_snapshot_182.dataset = tao_dataset_3
    tao_snapshot_182.redshift = Decimal('0.1971746678')
    tao_snapshot_182 = save_or_locate(tao_snapshot_182)

    tao_snapshot_183 = Snapshot()
    tao_snapshot_183.dataset = tao_dataset_3
    tao_snapshot_183.redshift = Decimal('0.2014898474')
    tao_snapshot_183 = save_or_locate(tao_snapshot_183)

    tao_snapshot_184 = Snapshot()
    tao_snapshot_184.dataset = tao_dataset_3
    tao_snapshot_184.redshift = Decimal('0.2058362474')
    tao_snapshot_184 = save_or_locate(tao_snapshot_184)

    tao_snapshot_185 = Snapshot()
    tao_snapshot_185.dataset = tao_dataset_3
    tao_snapshot_185.redshift = Decimal('0.2102142079')
    tao_snapshot_185 = save_or_locate(tao_snapshot_185)

    tao_snapshot_186 = Snapshot()
    tao_snapshot_186.dataset = tao_dataset_3
    tao_snapshot_186.redshift = Decimal('0.2146240738')
    tao_snapshot_186 = save_or_locate(tao_snapshot_186)

    tao_snapshot_187 = Snapshot()
    tao_snapshot_187.dataset = tao_dataset_3
    tao_snapshot_187.redshift = Decimal('0.2190661953')
    tao_snapshot_187 = save_or_locate(tao_snapshot_187)

    tao_snapshot_188 = Snapshot()
    tao_snapshot_188.dataset = tao_dataset_3
    tao_snapshot_188.redshift = Decimal('0.2235409274')
    tao_snapshot_188 = save_or_locate(tao_snapshot_188)

    tao_snapshot_189 = Snapshot()
    tao_snapshot_189.dataset = tao_dataset_3
    tao_snapshot_189.redshift = Decimal('0.2280486307')
    tao_snapshot_189 = save_or_locate(tao_snapshot_189)

    tao_snapshot_190 = Snapshot()
    tao_snapshot_190.dataset = tao_dataset_3
    tao_snapshot_190.redshift = Decimal('0.2325896709')
    tao_snapshot_190 = save_or_locate(tao_snapshot_190)

    tao_snapshot_191 = Snapshot()
    tao_snapshot_191.dataset = tao_dataset_3
    tao_snapshot_191.redshift = Decimal('0.2371644192')
    tao_snapshot_191 = save_or_locate(tao_snapshot_191)

    tao_snapshot_192 = Snapshot()
    tao_snapshot_192.dataset = tao_dataset_3
    tao_snapshot_192.redshift = Decimal('0.2464165524')
    tao_snapshot_192 = save_or_locate(tao_snapshot_192)

    tao_snapshot_193 = Snapshot()
    tao_snapshot_193.dataset = tao_dataset_3
    tao_snapshot_193.redshift = Decimal('0.2558081125')
    tao_snapshot_193 = save_or_locate(tao_snapshot_193)

    tao_snapshot_194 = Snapshot()
    tao_snapshot_194.dataset = tao_dataset_3
    tao_snapshot_194.redshift = Decimal('0.2653422751')
    tao_snapshot_194 = save_or_locate(tao_snapshot_194)

    tao_snapshot_195 = Snapshot()
    tao_snapshot_195.dataset = tao_dataset_3
    tao_snapshot_195.redshift = Decimal('0.2750223129')
    tao_snapshot_195 = save_or_locate(tao_snapshot_195)

    tao_snapshot_196 = Snapshot()
    tao_snapshot_196.dataset = tao_dataset_3
    tao_snapshot_196.redshift = Decimal('0.2848515996')
    tao_snapshot_196 = save_or_locate(tao_snapshot_196)

    tao_snapshot_197 = Snapshot()
    tao_snapshot_197.dataset = tao_dataset_3
    tao_snapshot_197.redshift = Decimal('0.2948336139')
    tao_snapshot_197 = save_or_locate(tao_snapshot_197)

    tao_snapshot_198 = Snapshot()
    tao_snapshot_198.dataset = tao_dataset_3
    tao_snapshot_198.redshift = Decimal('0.3049719431')
    tao_snapshot_198 = save_or_locate(tao_snapshot_198)

    tao_snapshot_199 = Snapshot()
    tao_snapshot_199.dataset = tao_dataset_3
    tao_snapshot_199.redshift = Decimal('0.3152702880')
    tao_snapshot_199 = save_or_locate(tao_snapshot_199)

    tao_snapshot_200 = Snapshot()
    tao_snapshot_200.dataset = tao_dataset_3
    tao_snapshot_200.redshift = Decimal('0.3257324672')
    tao_snapshot_200 = save_or_locate(tao_snapshot_200)

    tao_snapshot_201 = Snapshot()
    tao_snapshot_201.dataset = tao_dataset_3
    tao_snapshot_201.redshift = Decimal('0.3363624215')
    tao_snapshot_201 = save_or_locate(tao_snapshot_201)

    tao_snapshot_202 = Snapshot()
    tao_snapshot_202.dataset = tao_dataset_3
    tao_snapshot_202.redshift = Decimal('0.3471642193')
    tao_snapshot_202 = save_or_locate(tao_snapshot_202)

    tao_snapshot_203 = Snapshot()
    tao_snapshot_203.dataset = tao_dataset_3
    tao_snapshot_203.redshift = Decimal('0.3581420617')
    tao_snapshot_203 = save_or_locate(tao_snapshot_203)

    tao_snapshot_204 = Snapshot()
    tao_snapshot_204.dataset = tao_dataset_3
    tao_snapshot_204.redshift = Decimal('0.3693002876')
    tao_snapshot_204 = save_or_locate(tao_snapshot_204)

    tao_snapshot_205 = Snapshot()
    tao_snapshot_205.dataset = tao_dataset_3
    tao_snapshot_205.redshift = Decimal('0.3806433798')
    tao_snapshot_205 = save_or_locate(tao_snapshot_205)

    tao_snapshot_206 = Snapshot()
    tao_snapshot_206.dataset = tao_dataset_3
    tao_snapshot_206.redshift = Decimal('0.3921759710')
    tao_snapshot_206 = save_or_locate(tao_snapshot_206)

    tao_snapshot_207 = Snapshot()
    tao_snapshot_207.dataset = tao_dataset_3
    tao_snapshot_207.redshift = Decimal('0.4039028499')
    tao_snapshot_207 = save_or_locate(tao_snapshot_207)

    tao_snapshot_208 = Snapshot()
    tao_snapshot_208.dataset = tao_dataset_3
    tao_snapshot_208.redshift = Decimal('0.4158289679')
    tao_snapshot_208 = save_or_locate(tao_snapshot_208)

    tao_snapshot_209 = Snapshot()
    tao_snapshot_209.dataset = tao_dataset_3
    tao_snapshot_209.redshift = Decimal('0.4279594460')
    tao_snapshot_209 = save_or_locate(tao_snapshot_209)

    tao_snapshot_210 = Snapshot()
    tao_snapshot_210.dataset = tao_dataset_3
    tao_snapshot_210.redshift = Decimal('0.4402995823')
    tao_snapshot_210 = save_or_locate(tao_snapshot_210)

    tao_snapshot_211 = Snapshot()
    tao_snapshot_211.dataset = tao_dataset_3
    tao_snapshot_211.redshift = Decimal('0.4528548598')
    tao_snapshot_211 = save_or_locate(tao_snapshot_211)

    tao_snapshot_212 = Snapshot()
    tao_snapshot_212.dataset = tao_dataset_3
    tao_snapshot_212.redshift = Decimal('0.4656309541')
    tao_snapshot_212 = save_or_locate(tao_snapshot_212)

    tao_snapshot_213 = Snapshot()
    tao_snapshot_213.dataset = tao_dataset_3
    tao_snapshot_213.redshift = Decimal('0.4786337424')
    tao_snapshot_213 = save_or_locate(tao_snapshot_213)

    tao_snapshot_214 = Snapshot()
    tao_snapshot_214.dataset = tao_dataset_3
    tao_snapshot_214.redshift = Decimal('0.4918693122')
    tao_snapshot_214 = save_or_locate(tao_snapshot_214)

    tao_snapshot_215 = Snapshot()
    tao_snapshot_215.dataset = tao_dataset_3
    tao_snapshot_215.redshift = Decimal('0.5053439711')
    tao_snapshot_215 = save_or_locate(tao_snapshot_215)

    tao_snapshot_216 = Snapshot()
    tao_snapshot_216.dataset = tao_dataset_3
    tao_snapshot_216.redshift = Decimal('0.5190642564')
    tao_snapshot_216 = save_or_locate(tao_snapshot_216)

    tao_snapshot_217 = Snapshot()
    tao_snapshot_217.dataset = tao_dataset_3
    tao_snapshot_217.redshift = Decimal('0.5330369462')
    tao_snapshot_217 = save_or_locate(tao_snapshot_217)

    tao_snapshot_218 = Snapshot()
    tao_snapshot_218.dataset = tao_dataset_3
    tao_snapshot_218.redshift = Decimal('0.5472690701')
    tao_snapshot_218 = save_or_locate(tao_snapshot_218)

    tao_snapshot_219 = Snapshot()
    tao_snapshot_219.dataset = tao_dataset_3
    tao_snapshot_219.redshift = Decimal('0.5617679213')
    tao_snapshot_219 = save_or_locate(tao_snapshot_219)

    tao_snapshot_220 = Snapshot()
    tao_snapshot_220.dataset = tao_dataset_3
    tao_snapshot_220.redshift = Decimal('0.5765410689')
    tao_snapshot_220 = save_or_locate(tao_snapshot_220)

    tao_snapshot_221 = Snapshot()
    tao_snapshot_221.dataset = tao_dataset_3
    tao_snapshot_221.redshift = Decimal('0.5915963712')
    tao_snapshot_221 = save_or_locate(tao_snapshot_221)

    tao_snapshot_222 = Snapshot()
    tao_snapshot_222.dataset = tao_dataset_3
    tao_snapshot_222.redshift = Decimal('0.6069419894')
    tao_snapshot_222 = save_or_locate(tao_snapshot_222)

    tao_snapshot_223 = Snapshot()
    tao_snapshot_223.dataset = tao_dataset_3
    tao_snapshot_223.redshift = Decimal('0.6225864027')
    tao_snapshot_223 = save_or_locate(tao_snapshot_223)

    tao_snapshot_224 = Snapshot()
    tao_snapshot_224.dataset = tao_dataset_3
    tao_snapshot_224.redshift = Decimal('0.6385384237')
    tao_snapshot_224 = save_or_locate(tao_snapshot_224)

    tao_snapshot_225 = Snapshot()
    tao_snapshot_225.dataset = tao_dataset_3
    tao_snapshot_225.redshift = Decimal('0.6548072150')
    tao_snapshot_225 = save_or_locate(tao_snapshot_225)

    tao_snapshot_226 = Snapshot()
    tao_snapshot_226.dataset = tao_dataset_3
    tao_snapshot_226.redshift = Decimal('0.6714023065')
    tao_snapshot_226 = save_or_locate(tao_snapshot_226)

    tao_snapshot_227 = Snapshot()
    tao_snapshot_227.dataset = tao_dataset_3
    tao_snapshot_227.redshift = Decimal('0.6883336147')
    tao_snapshot_227 = save_or_locate(tao_snapshot_227)

    tao_snapshot_228 = Snapshot()
    tao_snapshot_228.dataset = tao_dataset_3
    tao_snapshot_228.redshift = Decimal('0.7056114617')
    tao_snapshot_228 = save_or_locate(tao_snapshot_228)

    tao_snapshot_229 = Snapshot()
    tao_snapshot_229.dataset = tao_dataset_3
    tao_snapshot_229.redshift = Decimal('0.7232465966')
    tao_snapshot_229 = save_or_locate(tao_snapshot_229)

    tao_snapshot_230 = Snapshot()
    tao_snapshot_230.dataset = tao_dataset_3
    tao_snapshot_230.redshift = Decimal('0.7412502177')
    tao_snapshot_230 = save_or_locate(tao_snapshot_230)

    tao_snapshot_231 = Snapshot()
    tao_snapshot_231.dataset = tao_dataset_3
    tao_snapshot_231.redshift = Decimal('0.7596339961')
    tao_snapshot_231 = save_or_locate(tao_snapshot_231)

    tao_snapshot_232 = Snapshot()
    tao_snapshot_232.dataset = tao_dataset_3
    tao_snapshot_232.redshift = Decimal('0.7784101014')
    tao_snapshot_232 = save_or_locate(tao_snapshot_232)

    tao_snapshot_233 = Snapshot()
    tao_snapshot_233.dataset = tao_dataset_3
    tao_snapshot_233.redshift = Decimal('0.7975912278')
    tao_snapshot_233 = save_or_locate(tao_snapshot_233)

    tao_snapshot_234 = Snapshot()
    tao_snapshot_234.dataset = tao_dataset_3
    tao_snapshot_234.redshift = Decimal('0.8171906233')
    tao_snapshot_234 = save_or_locate(tao_snapshot_234)

    tao_snapshot_235 = Snapshot()
    tao_snapshot_235.dataset = tao_dataset_3
    tao_snapshot_235.redshift = Decimal('0.8372221202')
    tao_snapshot_235 = save_or_locate(tao_snapshot_235)

    tao_snapshot_236 = Snapshot()
    tao_snapshot_236.dataset = tao_dataset_3
    tao_snapshot_236.redshift = Decimal('0.8577001672')
    tao_snapshot_236 = save_or_locate(tao_snapshot_236)

    tao_snapshot_237 = Snapshot()
    tao_snapshot_237.dataset = tao_dataset_3
    tao_snapshot_237.redshift = Decimal('0.8786398647')
    tao_snapshot_237 = save_or_locate(tao_snapshot_237)

    tao_snapshot_238 = Snapshot()
    tao_snapshot_238.dataset = tao_dataset_3
    tao_snapshot_238.redshift = Decimal('0.8928639031')
    tao_snapshot_238 = save_or_locate(tao_snapshot_238)

    tao_snapshot_239 = Snapshot()
    tao_snapshot_239.dataset = tao_dataset_3
    tao_snapshot_239.redshift = Decimal('0.9146084626')
    tao_snapshot_239 = save_or_locate(tao_snapshot_239)

    tao_snapshot_240 = Snapshot()
    tao_snapshot_240.dataset = tao_dataset_3
    tao_snapshot_240.redshift = Decimal('0.9368584156')
    tao_snapshot_240 = save_or_locate(tao_snapshot_240)

    tao_snapshot_241 = Snapshot()
    tao_snapshot_241.dataset = tao_dataset_3
    tao_snapshot_241.redshift = Decimal('0.9596315893')
    tao_snapshot_241 = save_or_locate(tao_snapshot_241)

    tao_snapshot_242 = Snapshot()
    tao_snapshot_242.dataset = tao_dataset_3
    tao_snapshot_242.redshift = Decimal('0.9829466587')
    tao_snapshot_242 = save_or_locate(tao_snapshot_242)

    tao_snapshot_243 = Snapshot()
    tao_snapshot_243.dataset = tao_dataset_3
    tao_snapshot_243.redshift = Decimal('1.0068231989')
    tao_snapshot_243 = save_or_locate(tao_snapshot_243)

    tao_snapshot_244 = Snapshot()
    tao_snapshot_244.dataset = tao_dataset_3
    tao_snapshot_244.redshift = Decimal('1.0563438207')
    tao_snapshot_244 = save_or_locate(tao_snapshot_244)

    tao_snapshot_245 = Snapshot()
    tao_snapshot_245.dataset = tao_dataset_3
    tao_snapshot_245.redshift = Decimal('1.0820320633')
    tao_snapshot_245 = save_or_locate(tao_snapshot_245)

    tao_snapshot_246 = Snapshot()
    tao_snapshot_246.dataset = tao_dataset_3
    tao_snapshot_246.redshift = Decimal('1.1083702298')
    tao_snapshot_246 = save_or_locate(tao_snapshot_246)

    tao_snapshot_247 = Snapshot()
    tao_snapshot_247.dataset = tao_dataset_3
    tao_snapshot_247.redshift = Decimal('1.1353833013')
    tao_snapshot_247 = save_or_locate(tao_snapshot_247)

    tao_snapshot_248 = Snapshot()
    tao_snapshot_248.dataset = tao_dataset_3
    tao_snapshot_248.redshift = Decimal('1.1630975557')
    tao_snapshot_248 = save_or_locate(tao_snapshot_248)

    tao_snapshot_249 = Snapshot()
    tao_snapshot_249.dataset = tao_dataset_3
    tao_snapshot_249.redshift = Decimal('1.1915406531')
    tao_snapshot_249 = save_or_locate(tao_snapshot_249)

    tao_snapshot_250 = Snapshot()
    tao_snapshot_250.dataset = tao_dataset_3
    tao_snapshot_250.redshift = Decimal('1.2207417277')
    tao_snapshot_250 = save_or_locate(tao_snapshot_250)

    tao_snapshot_251 = Snapshot()
    tao_snapshot_251.dataset = tao_dataset_3
    tao_snapshot_251.redshift = Decimal('1.2507314877')
    tao_snapshot_251 = save_or_locate(tao_snapshot_251)

    tao_snapshot_252 = Snapshot()
    tao_snapshot_252.dataset = tao_dataset_3
    tao_snapshot_252.redshift = Decimal('1.2815423226')
    tao_snapshot_252 = save_or_locate(tao_snapshot_252)

    tao_snapshot_253 = Snapshot()
    tao_snapshot_253.dataset = tao_dataset_3
    tao_snapshot_253.redshift = Decimal('1.3132084201')
    tao_snapshot_253 = save_or_locate(tao_snapshot_253)

    tao_snapshot_254 = Snapshot()
    tao_snapshot_254.dataset = tao_dataset_3
    tao_snapshot_254.redshift = Decimal('1.3457658926')
    tao_snapshot_254 = save_or_locate(tao_snapshot_254)

    tao_snapshot_255 = Snapshot()
    tao_snapshot_255.dataset = tao_dataset_3
    tao_snapshot_255.redshift = Decimal('1.3792529146')
    tao_snapshot_255 = save_or_locate(tao_snapshot_255)

    tao_snapshot_256 = Snapshot()
    tao_snapshot_256.dataset = tao_dataset_3
    tao_snapshot_256.redshift = Decimal('1.4137098721')
    tao_snapshot_256 = save_or_locate(tao_snapshot_256)

    tao_snapshot_257 = Snapshot()
    tao_snapshot_257.dataset = tao_dataset_3
    tao_snapshot_257.redshift = Decimal('1.4491795249')
    tao_snapshot_257 = save_or_locate(tao_snapshot_257)

    tao_snapshot_258 = Snapshot()
    tao_snapshot_258.dataset = tao_dataset_3
    tao_snapshot_258.redshift = Decimal('1.4857071837')
    tao_snapshot_258 = save_or_locate(tao_snapshot_258)

    tao_snapshot_259 = Snapshot()
    tao_snapshot_259.dataset = tao_dataset_3
    tao_snapshot_259.redshift = Decimal('1.5233409034')
    tao_snapshot_259 = save_or_locate(tao_snapshot_259)

    tao_snapshot_260 = Snapshot()
    tao_snapshot_260.dataset = tao_dataset_3
    tao_snapshot_260.redshift = Decimal('1.5621316936')
    tao_snapshot_260 = save_or_locate(tao_snapshot_260)

    tao_snapshot_261 = Snapshot()
    tao_snapshot_261.dataset = tao_dataset_3
    tao_snapshot_261.redshift = Decimal('1.6021337497')
    tao_snapshot_261 = save_or_locate(tao_snapshot_261)

    tao_snapshot_262 = Snapshot()
    tao_snapshot_262.dataset = tao_dataset_3
    tao_snapshot_262.redshift = Decimal('1.6434047053')
    tao_snapshot_262 = save_or_locate(tao_snapshot_262)

    tao_snapshot_263 = Snapshot()
    tao_snapshot_263.dataset = tao_dataset_3
    tao_snapshot_263.redshift = Decimal('1.6860059092')
    tao_snapshot_263 = save_or_locate(tao_snapshot_263)

    tao_snapshot_264 = Snapshot()
    tao_snapshot_264.dataset = tao_dataset_3
    tao_snapshot_264.redshift = Decimal('1.7300027300')
    tao_snapshot_264 = save_or_locate(tao_snapshot_264)

    tao_snapshot_265 = Snapshot()
    tao_snapshot_265.dataset = tao_dataset_3
    tao_snapshot_265.redshift = Decimal('1.7754648904')
    tao_snapshot_265 = save_or_locate(tao_snapshot_265)

    tao_snapshot_266 = Snapshot()
    tao_snapshot_266.dataset = tao_dataset_3
    tao_snapshot_266.redshift = Decimal('1.8224668360')
    tao_snapshot_266 = save_or_locate(tao_snapshot_266)

    tao_snapshot_267 = Snapshot()
    tao_snapshot_267.dataset = tao_dataset_3
    tao_snapshot_267.redshift = Decimal('1.8710881424')
    tao_snapshot_267 = save_or_locate(tao_snapshot_267)

    tao_snapshot_268 = Snapshot()
    tao_snapshot_268.dataset = tao_dataset_3
    tao_snapshot_268.redshift = Decimal('1.9214139644')
    tao_snapshot_268 = save_or_locate(tao_snapshot_268)

    tao_snapshot_269 = Snapshot()
    tao_snapshot_269.dataset = tao_dataset_3
    tao_snapshot_269.redshift = Decimal('1.9735355338')
    tao_snapshot_269 = save_or_locate(tao_snapshot_269)

    tao_snapshot_270 = Snapshot()
    tao_snapshot_270.dataset = tao_dataset_3
    tao_snapshot_270.redshift = Decimal('2.0275507115')
    tao_snapshot_270 = save_or_locate(tao_snapshot_270)

    tao_snapshot_271 = Snapshot()
    tao_snapshot_271.dataset = tao_dataset_3
    tao_snapshot_271.redshift = Decimal('2.0835646007')
    tao_snapshot_271 = save_or_locate(tao_snapshot_271)

    tao_snapshot_272 = Snapshot()
    tao_snapshot_272.dataset = tao_dataset_3
    tao_snapshot_272.redshift = Decimal('2.1416902293')
    tao_snapshot_272 = save_or_locate(tao_snapshot_272)

    tao_snapshot_273 = Snapshot()
    tao_snapshot_273.dataset = tao_dataset_3
    tao_snapshot_273.redshift = Decimal('2.2020493116')
    tao_snapshot_273 = save_or_locate(tao_snapshot_273)

    tao_snapshot_274 = Snapshot()
    tao_snapshot_274.dataset = tao_dataset_3
    tao_snapshot_274.redshift = Decimal('2.2647730983')
    tao_snapshot_274 = save_or_locate(tao_snapshot_274)

    tao_snapshot_275 = Snapshot()
    tao_snapshot_275.dataset = tao_dataset_3
    tao_snapshot_275.redshift = Decimal('2.3978933062')
    tao_snapshot_275 = save_or_locate(tao_snapshot_275)

    tao_snapshot_276 = Snapshot()
    tao_snapshot_276.dataset = tao_dataset_3
    tao_snapshot_276.redshift = Decimal('2.4686090878')
    tao_snapshot_276 = save_or_locate(tao_snapshot_276)

    tao_snapshot_277 = Snapshot()
    tao_snapshot_277.dataset = tao_dataset_3
    tao_snapshot_277.redshift = Decimal('2.5423308537')
    tao_snapshot_277 = save_or_locate(tao_snapshot_277)

    tao_snapshot_278 = Snapshot()
    tao_snapshot_278.dataset = tao_dataset_3
    tao_snapshot_278.redshift = Decimal('2.6192544336')
    tao_snapshot_278 = save_or_locate(tao_snapshot_278)

    tao_snapshot_279 = Snapshot()
    tao_snapshot_279.dataset = tao_dataset_3
    tao_snapshot_279.redshift = Decimal('2.6995930448')
    tao_snapshot_279 = save_or_locate(tao_snapshot_279)

    tao_snapshot_280 = Snapshot()
    tao_snapshot_280.dataset = tao_dataset_3
    tao_snapshot_280.redshift = Decimal('2.7835792660')
    tao_snapshot_280 = save_or_locate(tao_snapshot_280)

    tao_snapshot_281 = Snapshot()
    tao_snapshot_281.dataset = tao_dataset_3
    tao_snapshot_281.redshift = Decimal('2.8714672861')
    tao_snapshot_281 = save_or_locate(tao_snapshot_281)

    tao_snapshot_282 = Snapshot()
    tao_snapshot_282.dataset = tao_dataset_3
    tao_snapshot_282.redshift = Decimal('2.9635354736')
    tao_snapshot_282 = save_or_locate(tao_snapshot_282)

    tao_snapshot_283 = Snapshot()
    tao_snapshot_283.dataset = tao_dataset_3
    tao_snapshot_283.redshift = Decimal('3.0600893220')
    tao_snapshot_283 = save_or_locate(tao_snapshot_283)

    tao_snapshot_284 = Snapshot()
    tao_snapshot_284.dataset = tao_dataset_3
    tao_snapshot_284.redshift = Decimal('3.2680324370')
    tao_snapshot_284 = save_or_locate(tao_snapshot_284)

    tao_snapshot_285 = Snapshot()
    tao_snapshot_285.dataset = tao_dataset_3
    tao_snapshot_285.redshift = Decimal('3.3802014893')
    tao_snapshot_285 = save_or_locate(tao_snapshot_285)

    tao_snapshot_286 = Snapshot()
    tao_snapshot_286.dataset = tao_dataset_3
    tao_snapshot_286.redshift = Decimal('3.4984255511')
    tao_snapshot_286 = save_or_locate(tao_snapshot_286)

    tao_snapshot_287 = Snapshot()
    tao_snapshot_287.dataset = tao_dataset_3
    tao_snapshot_287.redshift = Decimal('3.6232085067')
    tao_snapshot_287 = save_or_locate(tao_snapshot_287)

    tao_snapshot_288 = Snapshot()
    tao_snapshot_288.dataset = tao_dataset_3
    tao_snapshot_288.redshift = Decimal('3.7551117451')
    tao_snapshot_288 = save_or_locate(tao_snapshot_288)

    tao_snapshot_289 = Snapshot()
    tao_snapshot_289.dataset = tao_dataset_3
    tao_snapshot_289.redshift = Decimal('3.8947626040')
    tao_snapshot_289 = save_or_locate(tao_snapshot_289)

    tao_snapshot_290 = Snapshot()
    tao_snapshot_290.dataset = tao_dataset_3
    tao_snapshot_290.redshift = Decimal('3.9431537321')
    tao_snapshot_290 = save_or_locate(tao_snapshot_290)

    tao_snapshot_291 = Snapshot()
    tao_snapshot_291.dataset = tao_dataset_3
    tao_snapshot_291.redshift = Decimal('4.0428643470')
    tao_snapshot_291 = save_or_locate(tao_snapshot_291)

    tao_snapshot_292 = Snapshot()
    tao_snapshot_292.dataset = tao_dataset_3
    tao_snapshot_292.redshift = Decimal('4.2002080083')
    tao_snapshot_292 = save_or_locate(tao_snapshot_292)

    tao_snapshot_293 = Snapshot()
    tao_snapshot_293.dataset = tao_dataset_3
    tao_snapshot_293.redshift = Decimal('4.3676865271')
    tao_snapshot_293 = save_or_locate(tao_snapshot_293)

    tao_snapshot_294 = Snapshot()
    tao_snapshot_294.dataset = tao_dataset_3
    tao_snapshot_294.redshift = Decimal('4.5463117027')
    tao_snapshot_294 = save_or_locate(tao_snapshot_294)

    tao_snapshot_295 = Snapshot()
    tao_snapshot_295.dataset = tao_dataset_3
    tao_snapshot_295.redshift = Decimal('4.7372346529')
    tao_snapshot_295 = save_or_locate(tao_snapshot_295)

    tao_snapshot_296 = Snapshot()
    tao_snapshot_296.dataset = tao_dataset_3
    tao_snapshot_296.redshift = Decimal('4.9417706476')
    tao_snapshot_296 = save_or_locate(tao_snapshot_296)

    tao_snapshot_297 = Snapshot()
    tao_snapshot_297.dataset = tao_dataset_3
    tao_snapshot_297.redshift = Decimal('5.1614294516')
    tao_snapshot_297 = save_or_locate(tao_snapshot_297)

    tao_snapshot_298 = Snapshot()
    tao_snapshot_298.dataset = tao_dataset_3
    tao_snapshot_298.redshift = Decimal('5.3979526552')
    tao_snapshot_298 = save_or_locate(tao_snapshot_298)

    tao_snapshot_299 = Snapshot()
    tao_snapshot_299.dataset = tao_dataset_3
    tao_snapshot_299.redshift = Decimal('5.6533599468')
    tao_snapshot_299 = save_or_locate(tao_snapshot_299)

    tao_snapshot_300 = Snapshot()
    tao_snapshot_300.dataset = tao_dataset_3
    tao_snapshot_300.redshift = Decimal('5.9300069300')
    tao_snapshot_300 = save_or_locate(tao_snapshot_300)

    tao_snapshot_301 = Snapshot()
    tao_snapshot_301.dataset = tao_dataset_3
    tao_snapshot_301.redshift = Decimal('6.2306579899')
    tao_snapshot_301 = save_or_locate(tao_snapshot_301)

    tao_snapshot_302 = Snapshot()
    tao_snapshot_302.dataset = tao_dataset_3
    tao_snapshot_302.redshift = Decimal('6.5585789872')
    tao_snapshot_302 = save_or_locate(tao_snapshot_302)

    tao_snapshot_303 = Snapshot()
    tao_snapshot_303.dataset = tao_dataset_3
    tao_snapshot_303.redshift = Decimal('7.3125519534')
    tao_snapshot_303 = save_or_locate(tao_snapshot_303)

    tao_snapshot_304 = Snapshot()
    tao_snapshot_304.dataset = tao_dataset_3
    tao_snapshot_304.redshift = Decimal('7.7489063867')
    tao_snapshot_304 = save_or_locate(tao_snapshot_304)

    tao_snapshot_305 = Snapshot()
    tao_snapshot_305.dataset = tao_dataset_3
    tao_snapshot_305.redshift = Decimal('8.2336103416')
    tao_snapshot_305 = save_or_locate(tao_snapshot_305)

    tao_snapshot_306 = Snapshot()
    tao_snapshot_306.dataset = tao_dataset_3
    tao_snapshot_306.redshift = Decimal('8.7751710655')
    tao_snapshot_306 = save_or_locate(tao_snapshot_306)

    tao_snapshot_307 = Snapshot()
    tao_snapshot_307.dataset = tao_dataset_3
    tao_snapshot_307.redshift = Decimal('9.3842159917')
    tao_snapshot_307 = save_or_locate(tao_snapshot_307)

    tao_snapshot_308 = Snapshot()
    tao_snapshot_308.dataset = tao_dataset_3
    tao_snapshot_308.redshift = Decimal('11.7713920817')
    tao_snapshot_308 = save_or_locate(tao_snapshot_308)

    tao_snapshot_309 = Snapshot()
    tao_snapshot_309.dataset = tao_dataset_3
    tao_snapshot_309.redshift = Decimal('14.0829562594')
    tao_snapshot_309 = save_or_locate(tao_snapshot_309)

    #Processing model: Job

    from tao.models import Job

    tao_job_1 = Job()
    tao_job_1.user = tao_taouser_1
    tao_job_1.created_time = datetime.datetime(2013, 7, 8, 2, 36, 29, tzinfo=pytz.UTC)
    tao_job_1.description = u' '
    tao_job_1.status = u'COMPLETED'
    tao_job_1.parameters = u'<?xml version=\'1.0\' encoding=\'utf-8\'?>\r\n<tao timestamp="2013-07-08T12:36:29+10:00" xmlns="http://tao.asvo.org.au/schema/module-parameters-v1">\r\n  <username>staging</username>\r\n  <workflow name="alpha-light-cone-image">\r\n    <schema-version>2.0</schema-version>\r\n    <light-cone id="1">\r\n      <module-version>1</module-version>\r\n      <geometry>box</geometry>\r\n      <simulation>Millennium</simulation>\r\n      <galaxy-model>SAGE</galaxy-model>\r\n      <redshift>0E-10</redshift>\r\n      <query-box-size units="Mpc">500.000</query-box-size>\r\n      <output-fields>\r\n        <item description="Galaxy total stellar mass" label="Total Stellar Mass" units="10^10 M\u2609/h">stellarmass</item>\r\n        <item description="Supermassive black hole mass" label="Black Hole Mass" units="10^10 M\u2609/h">blackholemass</item>\r\n      </output-fields>\r\n    </light-cone>\r\n    <csv id="5">\r\n      <fields>\r\n        <item label="Total Stellar Mass" units="10^10 M\u2609/h">stellarmass</item>\r\n        <item label="Black Hole Mass" units="10^10 M\u2609/h">blackholemass</item>\r\n      </fields>\r\n      <parents>\r\n        <item>1</item>\r\n      </parents>\r\n      <module-version>1</module-version>\r\n      <filename>tao.output.csv</filename>\r\n    </csv>\r\n    <record-filter>\r\n      <module-version>1</module-version>\r\n      <filter>\r\n        <filter-attribute>stellarmass</filter-attribute>\r\n        <filter-min units="10^10 M\u2609/h">0.31</filter-min>\r\n        <filter-max units="10^10 M\u2609/h">None</filter-max>\r\n      </filter>\r\n    </record-filter>\r\n  </workflow>\r\n  <signature>base64encodedsignature</signature>\r\n</tao>\r\n'
    tao_job_1.output_path = u'stagingjobs/staging/2/output'
    tao_job_1.database = u'millennium_full_hdf5_dist'
    tao_job_1.error_message = u''
    tao_job_1 = save_or_locate(tao_job_1)

    tao_job_2 = Job()
    tao_job_2.user = tao_taouser_3
    tao_job_2.created_time = datetime.datetime(2013, 7, 16, 6, 7, 46, tzinfo=pytz.UTC)
    tao_job_2.description = u' '
    tao_job_2.status = u'QUEUED'
    tao_job_2.parameters = u'<?xml version=\'1.0\' encoding=\'utf-8\'?>\r\n<tao timestamp="2013-07-01T15:39:42+10:00" xmlns="http://tao.asvo.org.au/schema/module-parameters-v1">\r\n  <username>amr</username>\r\n  <workflow name="alpha-light-cone-image">\r\n    <schema-version>2.0</schema-version>\r\n    <light-cone id="1">\r\n      <module-version>1</module-version>\r\n      <geometry>light-cone</geometry>\r\n      <simulation>Millennium</simulation>\r\n      <galaxy-model>SAGE</galaxy-model>\r\n      <box-repetition>unique</box-repetition>\r\n      <num-cones>1</num-cones>\r\n      <redshift-min>0.01</redshift-min>\r\n      <redshift-max>0.4</redshift-max>\r\n      <ra-min units="deg">0.0</ra-min>\r\n      <ra-max units="deg">12</ra-max>\r\n      <dec-min units="deg">0.0</dec-min>\r\n      <dec-max units="deg">5</dec-max>\r\n      <output-fields>\r\n        <item description="Galaxy total stellar mass" label="Total Stellar Mass" units="10^10 M\u2609/h">stellarmass</item>\r\n        <item description="0=Central, 1=Satellite" label="Galaxy Type">objecttype</item>\r\n        <item description="Stellar disk scale radius" label="Disk Scale Radius" units="Mpc/h">diskscaleradius</item>\r\n        <item description="Total star formation rate in the galaxy" label="Sfr" units="M\u2609/yr">sfr</item>\r\n        <item description="Dark matter (sub)halo virial mass" label="Mvir" units="10^10 Mpc/h">mvir</item>\r\n        <item description="Central galaxy dark matter halo Mvir" label="Central Galaxy Mvir" units="10^10 M\u2609/h">centralmvir</item>\r\n        <item description="Dark matter halo velocity dispersion" label="Velocity Dispersion" units="km/s">veldisp</item>\r\n        <item description="Total simulation particles in the dark matter halo" label="Total particles">len</item>\r\n        <item description="X coordinate in the selected box/cone" label="x" units="Mpc/h">pos_x</item>\r\n        <item description="Y coordinate in the selected box/cone" label="y" units="Mpc/h">pos_y</item>\r\n        <item description="Z coordinate in the selected box/cone" label="z" units="Mpc/h">pos_z</item>\r\n        <item description="X component of the galaxy/halo velocity" label="x Velocity" units="km/s">velx</item>\r\n        <item description="Y componentt of the galaxy/halo velocity" label="y Velocity" units="km/s">vely</item>\r\n        <item description="Z componentt of the galaxy/halo velocity" label="z Velocity" units="km/s">velz</item>\r\n        <item description="" label="Central Galaxy ID">centralgal</item>\r\n        <item description="" label="FOF Halo Index">fofhaloindex</item>\r\n        <item description="Simulation snapshot number" label="Snapshot Number">snapnum</item>\r\n<item description="" label="Galaxy Index">globalgalaxyid</item>\r\n      </output-fields>\r\n    </light-cone>\r\n    <votable id="5">\r\n      <fields>\r\n<item label="Galaxy Index">globalgalaxyid</item>\r\n        <item label="Total Stellar Mass" units="10^10 M\u2609/h">stellarmass</item>\r\n        <item label="Galaxy Type">objecttype</item>\r\n        <item label="Disk Scale Radius" units="Mpc/h">diskscaleradius</item>\r\n        <item label="Sfr" units="M\u2609/yr">sfr</item>\r\n        <item label="Mvir" units="10^10 Mpc/h">mvir</item>\r\n        <item label="Central Galaxy Mvir" units="10^10 M\u2609/h">centralmvir</item>\r\n        <item label="Velocity Dispersion" units="km/s">veldisp</item>\r\n        <item label="Total particles">len</item>\r\n        <item label="x" units="Mpc/h">pos_x</item>\r\n        <item label="y" units="Mpc/h">pos_y</item>\r\n        <item label="z" units="Mpc/h">pos_z</item>\r\n        <item label="x Velocity" units="km/s">velx</item>\r\n        <item label="y Velocity" units="km/s">vely</item>\r\n        <item label="z Velocity" units="km/s">velz</item>\r\n        <item label="Central Galaxy ID">centralgal</item>\r\n        <item label="FOF Halo Index">fofhaloindex</item>\r\n        <item label="Snapshot Number">snapnum</item>\r\n        <item label="SDSS g (Apparent)">SDSS/sdss_g.dati_apparent</item>\r\n        <item label="SDSS g (Absolute)">SDSS/sdss_g.dati_absolute</item>\r\n        <item label="SDSS i (Apparent)">SDSS/sdss_i.dati_apparent</item>\r\n        <item label="SDSS i (Absolute)">SDSS/sdss_i.dati_absolute</item>\r\n        <item label="SDSS r (Apparent)">SDSS/sdss_r.dati_apparent</item>\r\n        <item label="SDSS r (Absolute)">SDSS/sdss_r.dati_absolute</item>\r\n        <item label="SDSS u (Apparent)">SDSS/sdss_u.dati_apparent</item>\r\n        <item label="SDSS u (Absolute)">SDSS/sdss_u.dati_absolute</item>\r\n        <item label="SDSS z (Apparent)">SDSS/sdss_z.dati_apparent</item>\r\n        <item label="SDSS z (Absolute)">SDSS/sdss_z.dati_absolute</item>\r\n        <item label="UKIRT H (Apparent)">UKIRT/H_filter.dati_apparent</item>\r\n        <item label="UKIRT H (Absolute)">UKIRT/H_filter.dati_absolute</item>\r\n        <item label="UKIRT J (Apparent)">UKIRT/J_filter.dati_apparent</item>\r\n        <item label="UKIRT J (Absolute)">UKIRT/J_filter.dati_absolute</item>\r\n        <item label="UKIRT K (Apparent)">UKIRT/K_filter.dati_apparent</item>\r\n        <item label="UKIRT K (Absolute)">UKIRT/K_filter.dati_absolute</item>\r\n      </fields>\r\n      <parents>\r\n        <item>4</item>\r\n      </parents>\r\n      <module-version>1</module-version>\r\n      <filename>tao.output.xml</filename>\r\n    </votable>\r\n    <sed id="2">\r\n      <module-version>1</module-version>\r\n      <parents>\r\n        <item>1</item>\r\n      </parents>\r\n      <single-stellar-population-model>ssp.ssz</single-stellar-population-model>\r\n    </sed>\r\n    <filter id="4">\r\n      <module-version>1</module-version>\r\n      <parents>\r\n        <item>3</item>\r\n      </parents>\r\n      <bandpass-filters>\r\n        <item description="&lt;p&gt;Sloan Digital Sky Survey (SDSS) g&lt;/p&gt;&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/SDSS_sdss_g.dati.html&quot;&gt;SDSS g&lt;/a&gt;.&lt;/p&gt;" label="SDSS g" selected="apparent,absolute">SDSS/sdss_g.dati</item>\r\n        <item description="&lt;p&gt;Sloan Digital Sky Survey (SDSS) i&lt;/p&gt;&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/SDSS_sdss_i.dati.html&quot;&gt;SDSS i&lt;/a&gt;.&lt;/p&gt;" label="SDSS i" selected="apparent,absolute">SDSS/sdss_i.dati</item>\r\n        <item description="&lt;p&gt;Sloan Digital Sky Survey (SDSS) r&lt;/p&gt;&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/SDSS_sdss_r.dati.html&quot;&gt;SDSS r&lt;/a&gt;.&lt;/p&gt;" label="SDSS r" selected="apparent,absolute">SDSS/sdss_r.dati</item>\r\n        <item description="&lt;p&gt;Sloan Digital Sky Survey (SDSS) u&lt;/p&gt;&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/SDSS_sdss_u.dati.html&quot;&gt;SDSS u&lt;/a&gt;.&lt;/p&gt;" label="SDSS u" selected="apparent,absolute">SDSS/sdss_u.dati</item>\r\n        <item description="&lt;p&gt;Sloan Digital Sky Survey (SDSS) z&lt;/p&gt;&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/SDSS_sdss_z.dati.html&quot;&gt;SDSS z&lt;/a&gt;.&lt;/p&gt;" label="SDSS z" selected="apparent,absolute">SDSS/sdss_z.dati</item>\r\n        <item description="&lt;p&gt;UKIRT Infrared Deep Sky Survey, H band&lt;/p&gt;&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/UKIRT_H_filter.dati.html&quot;&gt;UKIRT H&lt;/a&gt;.&lt;/p&gt;" label="UKIRT H" selected="apparent,absolute">UKIRT/H_filter.dati</item>\r\n        <item description="&lt;p&gt;UKIRT Infrared Deep Sky Survey, J band&lt;/p&gt;&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/UKIRT_J_filter.dati.html&quot;&gt;UKIRT J&lt;/a&gt;.&lt;/p&gt;" label="UKIRT J" selected="apparent,absolute">UKIRT/J_filter.dati</item>\r\n        <item description="&lt;p&gt;UKIRT Infrared Deep Sky Survey, K band&lt;/p&gt;&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/UKIRT_K_filter.dati.html&quot;&gt;UKIRT K&lt;/a&gt;.&lt;/p&gt;" label="UKIRT K" selected="apparent,absolute">UKIRT/K_filter.dati</item>\r\n      </bandpass-filters>\r\n    </filter>\r\n    <dust id="3">\r\n      <module-version>1</module-version>\r\n      <parents>\r\n        <item>2</item>\r\n      </parents>\r\n      <model>Tonini et al. 2012</model>\r\n    </dust>\r\n    <record-filter>\r\n      <module-version>1</module-version>\r\n      <filter>\r\n        <filter-attribute>stellarmass</filter-attribute>\r\n        <filter-min units="10^10 M\u2609/h">0.1</filter-min>\r\n        <filter-max units="10^10 M\u2609/h">None</filter-max>\r\n      </filter>\r\n    </record-filter>\r\n  </workflow>\r\n  <signature>base64encodedsignature</signature>\r\n</tao>'
    tao_job_2.output_path = u'stagingjobs/Amr/3/output'
    tao_job_2.database = u'millennium_full_hdf5_dist'
    tao_job_2.error_message = u''
    tao_job_2 = save_or_locate(tao_job_2)

    tao_job_3 = Job()
    tao_job_3.user = tao_taouser_3
    tao_job_3.created_time = datetime.datetime(2013, 7, 16, 6, 51, 16, tzinfo=pytz.UTC)
    tao_job_3.description = u'bolshoi Test'
    tao_job_3.status = u'IN_PROGRESS'
    tao_job_3.parameters = u'<?xml version=\'1.0\' encoding=\'utf-8\'?>\r\n<tao timestamp="2013-06-27T18:01:13+10:00" xmlns="http://tao.asvo.org.au/schema/module-parameters-v1">\r\n  <username>darrencroton</username>\r\n  <workflow name="alpha-light-cone-image">\r\n    <schema-version>2.0</schema-version>\r\n    <light-cone id="1">\r\n      <module-version>1</module-version>\r\n      <geometry>light-cone</geometry>\r\n      <simulation>Bolshoi</simulation>\r\n      <galaxy-model>SAGE</galaxy-model>\r\n      <box-repetition>random</box-repetition>\r\n      <num-cones>1</num-cones>\r\n      <redshift-min>0</redshift-min>\r\n      <redshift-max>0.1</redshift-max>\r\n      <ra-min units="deg">0.0</ra-min>\r\n      <ra-max units="deg">60</ra-max>\r\n      <dec-min units="deg">0.0</dec-min>\r\n      <dec-max units="deg">60</dec-max>\r\n      <output-fields>\r\n        <item description="Galaxy total stellar mass" label="Total Stellar Mass" units="10^10 M\u2609/h">stellarmass</item>\r\n        <item description="Galaxy bulge stellar mass" label="Bulge Stellar Mass" units="10^10 M\u2609/h">bulgemass</item>\r\n        <item description="Supermassive black hole mass" label="Black Hole Mass" units="10^10 M\u2609/h">blackholemass</item>\r\n        <item description="Mass of cold gas in the galaxy" label="Cold Gas Mass" units="10^10 M\u2609/h">coldgas</item>\r\n        <item description="Mass of hot halo gas" label="Hot Gas Mass" units="10^10 M\u2609/h">hotgas</item>\r\n        <item description="Gas mass ejected from halo" label="Ejected Gas Mass" units="10^10 M\u2609/h">ejectedmass</item>\r\n        <item description="Stellar mass in intracluster stars" label="ICS Mass" units="10^10 M\u2609/h">ics</item>\r\n        <item description="Mass of metals in the total stellar mass" label="Metals Total Stellar Mass" units="10^10 M\u2609/h">metalsstellarmass</item>\r\n        <item description="Mass of metals in the bulge" label="Metals Bulge Mass" units="10^10 M\u2609/h">metalsbulgemass</item>\r\n        <item description="Mass of metals in the cold gas" label="Metals Cold Gas Mass" units="10^10 M\u2609/h">metalscoldgas</item>\r\n        <item description="Mass of metals in the hot gas" label="Metals Hot Gas Mass" units="10^10 M\u2609/h">metalshotgas</item>\r\n        <item description="Mass of metals in the ejected gas" label="Metals Ejected Gas Mass" units="10^10 M\u2609/h">metalsejectedmass</item>\r\n        <item description="Mass of metals in the ICS" label="Metals ICS Mass" units="10^10 M\u2609/h">metalsics</item>\r\n        <item description="0=Central, 1=Satellite" label="Galaxy Type">objecttype</item>\r\n        <item description="Stellar disk scale radius" label="Disk Scale Radius" units="Mpc/h">diskscaleradius</item>\r\n        <item description="Total star formation rate in the galaxy" label="Sfr" units="M\u2609/yr">sfr</item>\r\n        <item description="Bulge star formation rate" label="Sfr Bulge" units="M\u2609/yr">sfrbulge</item>\r\n        <item description="ICS star formation rate" label="Sfr ICS" units="M\u2609/yr">sfrics</item>\r\n        <item description="Cooling rate of hot halo gas" label="Cooling Rate" units="log(erg/s)">cooling</item>\r\n        <item description="AGN heating rate" label="AGN Heating Rate" units="log(erg/s)">heating</item>\r\n        <item description="Dark matter (sub)halo virial mass" label="Mvir" units="10^10 Mpc/h">mvir</item>\r\n        <item description="Central galaxy dark matter halo Mvir" label="Central Galaxy Mvir" units="10^10 M\u2609/h">centralmvir</item>\r\n        <item description="Dark matter (sub)halo virial radius" label="Rvir" units="Mpc/h">rvir</item>\r\n        <item description="Dark matter (sub)halo virial velocity" label="Vvir" units="km/s">vvir</item>\r\n        <item description="Dark matter (sub)halo maximum circular velocity" label="Vmax" units="km/s">vmax</item>\r\n        <item description="Dark matter halo velocity dispersion" label="Velocity Dispersion" units="km/s">veldisp</item>\r\n        <item description="X component of the (sub)halo spin" label="x Spin">spinx</item>\r\n        <item description="Y component of the (sub)halo spin" label="y Spin">spiny</item>\r\n        <item description="Z component of the (sub)halo spin" label="z Spin">spinz</item>\r\n        <item description="Total simulation particles in the dark matter halo" label="Total particles">len</item>\r\n        <item description="X coordinate in the selected box/cone" label="x" units="Mpc/h">pos_x</item>\r\n        <item description="Y coordinate in the selected box/cone" label="y" units="Mpc/h">pos_y</item>\r\n        <item description="Z coordinate in the selected box/cone" label="z" units="Mpc/h">pos_z</item>\r\n        <item description="X component of the galaxy/halo velocity" label="x Velocity" units="km/s">velx</item>\r\n        <item description="Y componentt of the galaxy/halo velocity" label="y Velocity" units="km/s">vely</item>\r\n        <item description="Z componentt of the galaxy/halo velocity" label="z Velocity" units="km/s">velz</item>\r\n        <item description="" label="Central Galaxy ID">centralgal</item>\r\n        <item description="" label="Descendant">descendant</item>\r\n        <item description="" label="FOF Halo Index">fofhaloindex</item>\r\n        <item description="" label="Galaxy Index">globalgalaxyid</item>\r\n        <item description="" label="Global Descendant">globaldescendant</item>\r\n        <item description="" label="Global Index">globalindex</item>\r\n        <item description="" label="Halo Index">haloindex</item>\r\n        <item description="" label="Tree Index">treeindex</item>\r\n        <item description="Original x coordinate in the simulation box" label="x (original)" units="Mpc/h">posx</item>\r\n        <item description="Original y coordinate in the simulation box" label="y (original)" units="Mpc/h">posy</item>\r\n        <item description="Original z coordinate in the simulation box" label="z (original)" units="Mpc/h">posz</item>\r\n        <item description="Simulation snapshot number" label="Snapshot Number">snapnum</item>\r\n      </output-fields>\r\n    </light-cone>\r\n    <csv id="5">\r\n      <fields>\r\n        <item label="Total Stellar Mass" units="10^10 M\u2609/h">stellarmass</item>\r\n        <item label="Bulge Stellar Mass" units="10^10 M\u2609/h">bulgemass</item>\r\n        <item label="Black Hole Mass" units="10^10 M\u2609/h">blackholemass</item>\r\n        <item label="Cold Gas Mass" units="10^10 M\u2609/h">coldgas</item>\r\n        <item label="Hot Gas Mass" units="10^10 M\u2609/h">hotgas</item>\r\n        <item label="Ejected Gas Mass" units="10^10 M\u2609/h">ejectedmass</item>\r\n        <item label="ICS Mass" units="10^10 M\u2609/h">ics</item>\r\n        <item label="Metals Total Stellar Mass" units="10^10 M\u2609/h">metalsstellarmass</item>\r\n        <item label="Metals Bulge Mass" units="10^10 M\u2609/h">metalsbulgemass</item>\r\n        <item label="Metals Cold Gas Mass" units="10^10 M\u2609/h">metalscoldgas</item>\r\n        <item label="Metals Hot Gas Mass" units="10^10 M\u2609/h">metalshotgas</item>\r\n        <item label="Metals Ejected Gas Mass" units="10^10 M\u2609/h">metalsejectedmass</item>\r\n        <item label="Metals ICS Mass" units="10^10 M\u2609/h">metalsics</item>\r\n        <item label="Galaxy Type">objecttype</item>\r\n        <item label="Disk Scale Radius" units="Mpc/h">diskscaleradius</item>\r\n        <item label="Sfr" units="M\u2609/yr">sfr</item>\r\n        <item label="Sfr Bulge" units="M\u2609/yr">sfrbulge</item>\r\n        <item label="Sfr ICS" units="M\u2609/yr">sfrics</item>\r\n        <item label="Cooling Rate" units="log(erg/s)">cooling</item>\r\n        <item label="AGN Heating Rate" units="log(erg/s)">heating</item>\r\n        <item label="Mvir" units="10^10 Mpc/h">mvir</item>\r\n        <item label="Central Galaxy Mvir" units="10^10 M\u2609/h">centralmvir</item>\r\n        <item label="Rvir" units="Mpc/h">rvir</item>\r\n        <item label="Vvir" units="km/s">vvir</item>\r\n        <item label="Vmax" units="km/s">vmax</item>\r\n        <item label="Velocity Dispersion" units="km/s">veldisp</item>\r\n        <item label="x Spin">spinx</item>\r\n        <item label="y Spin">spiny</item>\r\n        <item label="z Spin">spinz</item>\r\n        <item label="Total particles">len</item>\r\n        <item label="x" units="Mpc/h">pos_x</item>\r\n        <item label="y" units="Mpc/h">pos_y</item>\r\n        <item label="z" units="Mpc/h">pos_z</item>\r\n        <item label="x Velocity" units="km/s">velx</item>\r\n        <item label="y Velocity" units="km/s">vely</item>\r\n        <item label="z Velocity" units="km/s">velz</item>\r\n        <item label="Central Galaxy ID">centralgal</item>\r\n        <item label="Descendant">descendant</item>\r\n        <item label="FOF Halo Index">fofhaloindex</item>\r\n        <item label="Galaxy Index">globalgalaxyid</item>\r\n        <item label="Global Descendant">globaldescendant</item>\r\n        <item label="Global Index">globalindex</item>\r\n        <item label="Halo Index">haloindex</item>\r\n        <item label="Tree Index">treeindex</item>\r\n        <item label="x (original)" units="Mpc/h">posx</item>\r\n        <item label="y (original)" units="Mpc/h">posy</item>\r\n        <item label="z (original)" units="Mpc/h">posz</item>\r\n        <item label="Snapshot Number">snapnum</item>\r\n        <item label="Johnson B (Apparent)">Johnson/Johnson_B.dati_apparent</item>\r\n        <item label="Johnson B (Absolute)">Johnson/Johnson_B.dati_absolute</item>\r\n        <item label="Johnson H (Apparent)">Johnson/h.dat_apparent</item>\r\n        <item label="Johnson H (Absolute)">Johnson/h.dat_absolute</item>\r\n        <item label="Johnson I (Apparent)">Johnson/Ifilter.dati_apparent</item>\r\n        <item label="Johnson I (Absolute)">Johnson/Ifilter.dati_absolute</item>\r\n        <item label="Johnson J (Apparent)">Johnson/j.dat_apparent</item>\r\n        <item label="Johnson J (Absolute)">Johnson/j.dat_absolute</item>\r\n        <item label="Johnson K (Apparent)">Johnson/k.dat_apparent</item>\r\n        <item label="Johnson K (Absolute)">Johnson/k.dat_absolute</item>\r\n        <item label="Johnson R (Apparent)">Johnson/Rfilter.dati_apparent</item>\r\n        <item label="Johnson R (Absolute)">Johnson/Rfilter.dati_absolute</item>\r\n        <item label="Johnson U (Apparent)">Johnson/Johnson_U.dati_apparent</item>\r\n        <item label="Johnson U (Absolute)">Johnson/Johnson_U.dati_absolute</item>\r\n        <item label="Johnson V (Apparent)">Johnson/Johnson_V.dati_apparent</item>\r\n        <item label="Johnson V (Absolute)">Johnson/Johnson_V.dati_absolute</item>\r\n        <item label="Keck/DEIMOS/DEEP B (Apparent)">DEEP/deep_B.dati_apparent</item>\r\n        <item label="Keck/DEIMOS/DEEP B (Absolute)">DEEP/deep_B.dati_absolute</item>\r\n        <item label="Keck/DEIMOS/DEEP I (Apparent)">DEEP/deep_I.dati_apparent</item>\r\n        <item label="Keck/DEIMOS/DEEP I (Absolute)">DEEP/deep_I.dati_absolute</item>\r\n        <item label="Keck/DEIMOS/DEEP R (Apparent)">DEEP/deep_R.dati_apparent</item>\r\n        <item label="Keck/DEIMOS/DEEP R (Absolute)">DEEP/deep_R.dati_absolute</item>\r\n        <item label="SDSS g (Apparent)">SDSS/sdss_g.dati_apparent</item>\r\n        <item label="SDSS g (Absolute)">SDSS/sdss_g.dati_absolute</item>\r\n        <item label="SDSS i (Apparent)">SDSS/sdss_i.dati_apparent</item>\r\n        <item label="SDSS i (Absolute)">SDSS/sdss_i.dati_absolute</item>\r\n        <item label="SDSS r (Apparent)">SDSS/sdss_r.dati_apparent</item>\r\n        <item label="SDSS r (Absolute)">SDSS/sdss_r.dati_absolute</item>\r\n        <item label="SDSS u (Apparent)">SDSS/sdss_u.dati_apparent</item>\r\n        <item label="SDSS u (Absolute)">SDSS/sdss_u.dati_absolute</item>\r\n        <item label="SDSS z (Apparent)">SDSS/sdss_z.dati_apparent</item>\r\n        <item label="SDSS z (Absolute)">SDSS/sdss_z.dati_absolute</item>\r\n      </fields>\r\n      <parents>\r\n        <item>4</item>\r\n      </parents>\r\n      <module-version>1</module-version>\r\n      <filename>tao.output.csv</filename>\r\n    </csv>\r\n    <sed id="2">\r\n      <module-version>1</module-version>\r\n      <parents>\r\n        <item>1</item>\r\n      </parents>\r\n      <single-stellar-population-model>ssp.ssz</single-stellar-population-model>\r\n    </sed>\r\n    <filter id="4">\r\n      <module-version>1</module-version>\r\n      <parents>\r\n        <item>3</item>\r\n      </parents>\r\n      <bandpass-filters>\r\n        <item description="&lt;p&gt;Johnson B band&lt;/p&gt;&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/Johnson_Johnson_B.dati.html&quot;&gt;Johnson B&lt;/a&gt;.&lt;/p&gt;" label="Johnson B" selected="apparent,absolute">Johnson/Johnson_B.dati</item>\r\n        <item description="&lt;p&gt;Johnson H band&lt;/p&gt;&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/Johnson_h.dat.html&quot;&gt;Johnson H&lt;/a&gt;.&lt;/p&gt;" label="Johnson H" selected="apparent,absolute">Johnson/h.dat</item>\r\n        <item description="&lt;p&gt;Johnson I band&lt;/p&gt;&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/Johnson_Ifilter.dati.html&quot;&gt;Johnson I&lt;/a&gt;.&lt;/p&gt;" label="Johnson I" selected="apparent,absolute">Johnson/Ifilter.dati</item>\r\n        <item description="&lt;p&gt;Johnson J band&lt;/p&gt;&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/Johnson_j.dat.html&quot;&gt;Johnson J&lt;/a&gt;.&lt;/p&gt;" label="Johnson J" selected="apparent,absolute">Johnson/j.dat</item>\r\n        <item description="&lt;p&gt;Johnson K band&lt;/p&gt;&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/Johnson_k.dat.html&quot;&gt;Johnson K&lt;/a&gt;.&lt;/p&gt;" label="Johnson K" selected="apparent,absolute">Johnson/k.dat</item>\r\n        <item description="&lt;p&gt;Johnson R band&lt;/p&gt;&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/Johnson_Rfilter.dati.html&quot;&gt;Johnson R&lt;/a&gt;.&lt;/p&gt;" label="Johnson R" selected="apparent,absolute">Johnson/Rfilter.dati</item>\r\n        <item description="&lt;p&gt;Johnson U band&lt;/p&gt;&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/Johnson_Johnson_U.dati.html&quot;&gt;Johnson U&lt;/a&gt;.&lt;/p&gt;" label="Johnson U" selected="apparent,absolute">Johnson/Johnson_U.dati</item>\r\n        <item description="&lt;p&gt;Johnson V band&lt;/p&gt;&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/Johnson_Johnson_V.dati.html&quot;&gt;Johnson V&lt;/a&gt;.&lt;/p&gt;" label="Johnson V" selected="apparent,absolute">Johnson/Johnson_V.dati</item>\r\n        <item description="&lt;p&gt;Keck/DEIMOS/DEEP, B band&lt;/p&gt;&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/DEEP_deep_B.dati.html&quot;&gt;Keck/DEIMOS/DEEP B&lt;/a&gt;.&lt;/p&gt;" label="Keck/DEIMOS/DEEP B" selected="apparent,absolute">DEEP/deep_B.dati</item>\r\n        <item description="&lt;p&gt;Keck/DEIMOS/DEEP, I band&lt;/p&gt;&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/DEEP_deep_I.dati.html&quot;&gt;Keck/DEIMOS/DEEP I&lt;/a&gt;.&lt;/p&gt;" label="Keck/DEIMOS/DEEP I" selected="apparent,absolute">DEEP/deep_I.dati</item>\r\n        <item description="&lt;p&gt;Keck/DEIMOS/DEEP, R band&lt;/p&gt;&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/DEEP_deep_R.dati.html&quot;&gt;Keck/DEIMOS/DEEP R&lt;/a&gt;.&lt;/p&gt;" label="Keck/DEIMOS/DEEP R" selected="apparent,absolute">DEEP/deep_R.dati</item>\r\n        <item description="&lt;p&gt;Sloan Digital Sky Survey (SDSS) g&lt;/p&gt;&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/SDSS_sdss_g.dati.html&quot;&gt;SDSS g&lt;/a&gt;.&lt;/p&gt;" label="SDSS g" selected="apparent,absolute">SDSS/sdss_g.dati</item>\r\n        <item description="&lt;p&gt;Sloan Digital Sky Survey (SDSS) i&lt;/p&gt;&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/SDSS_sdss_i.dati.html&quot;&gt;SDSS i&lt;/a&gt;.&lt;/p&gt;" label="SDSS i" selected="apparent,absolute">SDSS/sdss_i.dati</item>\r\n        <item description="&lt;p&gt;Sloan Digital Sky Survey (SDSS) r&lt;/p&gt;&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/SDSS_sdss_r.dati.html&quot;&gt;SDSS r&lt;/a&gt;.&lt;/p&gt;" label="SDSS r" selected="apparent,absolute">SDSS/sdss_r.dati</item>\r\n        <item description="&lt;p&gt;Sloan Digital Sky Survey (SDSS) u&lt;/p&gt;&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/SDSS_sdss_u.dati.html&quot;&gt;SDSS u&lt;/a&gt;.&lt;/p&gt;" label="SDSS u" selected="apparent,absolute">SDSS/sdss_u.dati</item>\r\n        <item description="&lt;p&gt;Sloan Digital Sky Survey (SDSS) z&lt;/p&gt;&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/SDSS_sdss_z.dati.html&quot;&gt;SDSS z&lt;/a&gt;.&lt;/p&gt;" label="SDSS z" selected="apparent,absolute">SDSS/sdss_z.dati</item>\r\n      </bandpass-filters>\r\n    </filter>\r\n    <dust id="3">\r\n      <module-version>1</module-version>\r\n      <parents>\r\n        <item>2</item>\r\n      </parents>\r\n      <model>Tonini et al. 2012</model>\r\n    </dust>\r\n    <record-filter>\r\n      <module-version>1</module-version>\r\n      <filter>\r\n        <filter-attribute>mvir</filter-attribute>\r\n        <filter-min units="10^10 Mpc/h">10.0</filter-min>\r\n        <filter-max units="10^10 Mpc/h">None</filter-max>\r\n      </filter>\r\n    </record-filter>\r\n  </workflow>\r\n  <signature>base64encodedsignature</signature>\r\n</tao>'
    tao_job_3.output_path = u''
    tao_job_3.database = u'bolshoi_full_dist'
    tao_job_3.error_message = u''
    tao_job_3 = save_or_locate(tao_job_3)

    tao_job_4 = Job()
    tao_job_4.user = tao_taouser_2
    tao_job_4.created_time = datetime.datetime(2013, 7, 16, 11, 30, 38, tzinfo=pytz.UTC)
    tao_job_4.description = u'Testing units in results.'
    tao_job_4.status = u'COMPLETED'
    tao_job_4.parameters = u'<?xml version=\'1.0\' encoding=\'utf-8\'?>\r\n<tao timestamp="2013-07-16T21:30:38+10:00" xmlns="http://tao.asvo.org.au/schema/module-parameters-v1">\r\n  <username>alistair</username>\r\n  <workflow name="alpha-light-cone-image">\r\n    <schema-version>2.0</schema-version>\r\n    <light-cone id="1">\r\n      <module-version>1</module-version>\r\n      <geometry>box</geometry>\r\n      <simulation>Mini-Millennium</simulation>\r\n      <galaxy-model>SAGE</galaxy-model>\r\n      <redshift>0E-10</redshift>\r\n      <query-box-size units="Mpc">62.500</query-box-size>\r\n      <output-fields>\r\n        <item description="Galaxy total stellar mass" label="Total Stellar Mass" units="10^10 M\u2609/h">stellarmass</item>\r\n        <item description="Galaxy bulge stellar mass" label="Bulge Stellar Mass" units="10^10 M\u2609/h">bulgemass</item>\r\n        <item description="Supermassive black hole mass" label="Black Hole Mass" units="10^10 M\u2609/h">blackholemass</item>\r\n        <item description="Mass of cold gas in the galaxy" label="Cold Gas Mass" units="10^10 M\u2609/h">coldgas</item>\r\n        <item description="Mass of hot halo gas" label="Hot Gas Mass" units="10^10 M\u2609/h">hotgas</item>\r\n        <item description="Gas mass ejected from halo" label="Ejected Gas Mass" units="10^10 M\u2609/h">ejectedmass</item>\r\n        <item description="Stellar mass in intracluster stars" label="ICS Mass" units="10^10 M\u2609/h">ics</item>\r\n        <item description="Mass of metals in the total stellar mass" label="Metals Total Stellar Mass" units="10^10 M\u2609/h">metalsstellarmass</item>\r\n        <item description="Mass of metals in the bulge" label="Metals Bulge Mass" units="10^10 M\u2609/h">metalsbulgemass</item>\r\n        <item description="Mass of metals in the cold gas" label="Metals Cold Gas Mass" units="10^10 M\u2609/h">metalscoldgas</item>\r\n        <item description="Mass of metals in the hot gas" label="Metals Hot Gas Mass" units="10^10 M\u2609/h">metalshotgas</item>\r\n        <item description="Mass of metals in the ejected gas" label="Metals Ejected Gas Mass" units="10^10 M\u2609/h">metalsejectedmass</item>\r\n        <item description="Mass of metals in the ICS" label="Metals ICS Mass" units="10^10 M\u2609/h">metalsics</item>\r\n        <item description="0=Central, 1=Satellite" label="Galaxy Type">objecttype</item>\r\n        <item description="Stellar disk scale radius" label="Disk Scale Radius" units="Mpc/h">diskscaleradius</item>\r\n        <item description="Total star formation rate in the galaxy" label="Sfr" units="M\u2609/yr">sfr</item>\r\n        <item description="Bulge star formation rate" label="Sfr Bulge" units="M\u2609/yr">sfrbulge</item>\r\n        <item description="ICS star formation rate" label="Sfr ICS" units="M\u2609/yr">sfrics</item>\r\n        <item description="Cooling rate of hot halo gas" label="Cooling Rate" units="log(erg/s)">cooling</item>\r\n        <item description="AGN heating rate" label="AGN Heating Rate" units="log(erg/s)">heating</item>\r\n        <item description="Dark matter (sub)halo virial mass" label="Mvir" units="10^10 Mpc/h">mvir</item>\r\n        <item description="Central galaxy dark matter halo Mvir" label="Central Galaxy Mvir" units="10^10 M\u2609/h">centralmvir</item>\r\n        <item description="Dark matter (sub)halo virial radius" label="Rvir" units="Mpc/h">rvir</item>\r\n        <item description="Dark matter (sub)halo virial velocity" label="Vvir" units="km/s">vvir</item>\r\n        <item description="Dark matter (sub)halo maximum circular velocity" label="Vmax" units="km/s">vmax</item>\r\n        <item description="Dark matter halo velocity dispersion" label="Velocity Dispersion" units="km/s">veldisp</item>\r\n        <item description="X component of the (sub)halo spin" label="x Spin">spinx</item>\r\n        <item description="Y component of the (sub)halo spin" label="y Spin">spiny</item>\r\n        <item description="Z component of the (sub)halo spin" label="z Spin">spinz</item>\r\n        <item description="Total simulation particles in the dark matter halo" label="Total particles">len</item>\r\n        <item description="X coordinate in the selected box/cone" label="x" units="Mpc/h">pos_x</item>\r\n        <item description="Y coordinate in the selected box/cone" label="y" units="Mpc/h">pos_y</item>\r\n        <item description="Z coordinate in the selected box/cone" label="z" units="Mpc/h">pos_z</item>\r\n        <item description="X component of the galaxy/halo velocity" label="x Velocity" units="km/s">velx</item>\r\n        <item description="Y componentt of the galaxy/halo velocity" label="y Velocity" units="km/s">vely</item>\r\n        <item description="Z componentt of the galaxy/halo velocity" label="z Velocity" units="km/s">velz</item>\r\n        <item description="" label="Central Galaxy ID">centralgal</item>\r\n        <item description="" label="Descendant">descendant</item>\r\n        <item description="" label="FOF Halo Index">fofhaloindex</item>\r\n        <item description="" label="Galaxy Index">globalgalaxyid</item>\r\n        <item description="" label="Global Descendant">globaldescendant</item>\r\n        <item description="" label="Global Index">globalindex</item>\r\n        <item description="" label="Halo Index">haloindex</item>\r\n        <item description="" label="Tree Index">treeindex</item>\r\n        <item description="Original x coordinate in the simulation box" label="x (original)" units="Mpc/h">posx</item>\r\n        <item description="Original y coordinate in the simulation box" label="y (original)" units="Mpc/h">posy</item>\r\n        <item description="Original z coordinate in the simulation box" label="z (original)" units="Mpc/h">posz</item>\r\n        <item description="Simulation snapshot number" label="Snapshot Number">snapnum</item>\r\n      </output-fields>\r\n    </light-cone>\r\n    <votable id="5">\r\n      <fields>\r\n        <item label="Total Stellar Mass" units="10^10 M\u2609/h">stellarmass</item>\r\n        <item label="Bulge Stellar Mass" units="10^10 M\u2609/h">bulgemass</item>\r\n        <item label="Black Hole Mass" units="10^10 M\u2609/h">blackholemass</item>\r\n        <item label="Cold Gas Mass" units="10^10 M\u2609/h">coldgas</item>\r\n        <item label="Hot Gas Mass" units="10^10 M\u2609/h">hotgas</item>\r\n        <item label="Ejected Gas Mass" units="10^10 M\u2609/h">ejectedmass</item>\r\n        <item label="ICS Mass" units="10^10 M\u2609/h">ics</item>\r\n        <item label="Metals Total Stellar Mass" units="10^10 M\u2609/h">metalsstellarmass</item>\r\n        <item label="Metals Bulge Mass" units="10^10 M\u2609/h">metalsbulgemass</item>\r\n        <item label="Metals Cold Gas Mass" units="10^10 M\u2609/h">metalscoldgas</item>\r\n        <item label="Metals Hot Gas Mass" units="10^10 M\u2609/h">metalshotgas</item>\r\n        <item label="Metals Ejected Gas Mass" units="10^10 M\u2609/h">metalsejectedmass</item>\r\n        <item label="Metals ICS Mass" units="10^10 M\u2609/h">metalsics</item>\r\n        <item label="Galaxy Type">objecttype</item>\r\n        <item label="Disk Scale Radius" units="Mpc/h">diskscaleradius</item>\r\n        <item label="Sfr" units="M\u2609/yr">sfr</item>\r\n        <item label="Sfr Bulge" units="M\u2609/yr">sfrbulge</item>\r\n        <item label="Sfr ICS" units="M\u2609/yr">sfrics</item>\r\n        <item label="Cooling Rate" units="log(erg/s)">cooling</item>\r\n        <item label="AGN Heating Rate" units="log(erg/s)">heating</item>\r\n        <item label="Mvir" units="10^10 Mpc/h">mvir</item>\r\n        <item label="Central Galaxy Mvir" units="10^10 M\u2609/h">centralmvir</item>\r\n        <item label="Rvir" units="Mpc/h">rvir</item>\r\n        <item label="Vvir" units="km/s">vvir</item>\r\n        <item label="Vmax" units="km/s">vmax</item>\r\n        <item label="Velocity Dispersion" units="km/s">veldisp</item>\r\n        <item label="x Spin">spinx</item>\r\n        <item label="y Spin">spiny</item>\r\n        <item label="z Spin">spinz</item>\r\n        <item label="Total particles">len</item>\r\n        <item label="x" units="Mpc/h">pos_x</item>\r\n        <item label="y" units="Mpc/h">pos_y</item>\r\n        <item label="z" units="Mpc/h">pos_z</item>\r\n        <item label="x Velocity" units="km/s">velx</item>\r\n        <item label="y Velocity" units="km/s">vely</item>\r\n        <item label="z Velocity" units="km/s">velz</item>\r\n        <item label="Central Galaxy ID">centralgal</item>\r\n        <item label="Descendant">descendant</item>\r\n        <item label="FOF Halo Index">fofhaloindex</item>\r\n        <item label="Galaxy Index">globalgalaxyid</item>\r\n        <item label="Global Descendant">globaldescendant</item>\r\n        <item label="Global Index">globalindex</item>\r\n        <item label="Halo Index">haloindex</item>\r\n        <item label="Tree Index">treeindex</item>\r\n        <item label="x (original)" units="Mpc/h">posx</item>\r\n        <item label="y (original)" units="Mpc/h">posy</item>\r\n        <item label="z (original)" units="Mpc/h">posz</item>\r\n        <item label="Snapshot Number">snapnum</item>\r\n      </fields>\r\n      <parents>\r\n        <item>1</item>\r\n      </parents>\r\n      <module-version>1</module-version>\r\n      <filename>tao.output.votable</filename>\r\n    </votable>\r\n    <record-filter>\r\n      <module-version>1</module-version>\r\n      <filter>\r\n        <filter-attribute>stellarmass</filter-attribute>\r\n        <filter-min units="10^10 M\u2609/h">1.0</filter-min>\r\n        <filter-max units="10^10 M\u2609/h">None</filter-max>\r\n      </filter>\r\n    </record-filter>\r\n  </workflow>\r\n  <signature>base64encodedsignature</signature>\r\n</tao>\r\n'
    tao_job_4.output_path = u'stagingjobs/alistair/5/output'
    tao_job_4.database = u'millennium_mini_hdf5_dist'
    tao_job_4.error_message = u''
    tao_job_4 = save_or_locate(tao_job_4)

    tao_job_5 = Job()
    tao_job_5.user = tao_taouser_2
    tao_job_5.created_time = datetime.datetime(2013, 7, 16, 11, 42, 57, tzinfo=pytz.UTC)
    tao_job_5.description = u'Testing updated units in results.'
    tao_job_5.status = u'COMPLETED'
    tao_job_5.parameters = u'<?xml version=\'1.0\' encoding=\'utf-8\'?>\r\n<tao timestamp="2013-07-16T21:30:38+10:00" xmlns="http://tao.asvo.org.au/schema/module-parameters-v1">\r\n  <username>alistair</username>\r\n  <workflow name="alpha-light-cone-image">\r\n    <schema-version>2.0</schema-version>\r\n    <light-cone id="1">\r\n      <module-version>1</module-version>\r\n      <geometry>box</geometry>\r\n      <simulation>Mini-Millennium</simulation>\r\n      <galaxy-model>SAGE</galaxy-model>\r\n      <redshift>0E-10</redshift>\r\n      <query-box-size units="Mpc">62.500</query-box-size>\r\n      <output-fields>\r\n        <item description="Galaxy total stellar mass" label="Total Stellar Mass" units="10^10 M\u2609/h">stellarmass</item>\r\n        <item description="Galaxy bulge stellar mass" label="Bulge Stellar Mass" units="10^10 M\u2609/h">bulgemass</item>\r\n        <item description="Supermassive black hole mass" label="Black Hole Mass" units="10^10 M\u2609/h">blackholemass</item>\r\n        <item description="Mass of cold gas in the galaxy" label="Cold Gas Mass" units="10^10 M\u2609/h">coldgas</item>\r\n        <item description="Mass of hot halo gas" label="Hot Gas Mass" units="10^10 M\u2609/h">hotgas</item>\r\n        <item description="Gas mass ejected from halo" label="Ejected Gas Mass" units="10^10 M\u2609/h">ejectedmass</item>\r\n        <item description="Stellar mass in intracluster stars" label="ICS Mass" units="10^10 M\u2609/h">ics</item>\r\n        <item description="Mass of metals in the total stellar mass" label="Metals Total Stellar Mass" units="10^10 M\u2609/h">metalsstellarmass</item>\r\n        <item description="Mass of metals in the bulge" label="Metals Bulge Mass" units="10^10 M\u2609/h">metalsbulgemass</item>\r\n        <item description="Mass of metals in the cold gas" label="Metals Cold Gas Mass" units="10^10 M\u2609/h">metalscoldgas</item>\r\n        <item description="Mass of metals in the hot gas" label="Metals Hot Gas Mass" units="10^10 M\u2609/h">metalshotgas</item>\r\n        <item description="Mass of metals in the ejected gas" label="Metals Ejected Gas Mass" units="10^10 M\u2609/h">metalsejectedmass</item>\r\n        <item description="Mass of metals in the ICS" label="Metals ICS Mass" units="10^10 M\u2609/h">metalsics</item>\r\n        <item description="0=Central, 1=Satellite" label="Galaxy Type">objecttype</item>\r\n        <item description="Stellar disk scale radius" label="Disk Scale Radius" units="Mpc/h">diskscaleradius</item>\r\n        <item description="Total star formation rate in the galaxy" label="Sfr" units="M\u2609/yr">sfr</item>\r\n        <item description="Bulge star formation rate" label="Sfr Bulge" units="M\u2609/yr">sfrbulge</item>\r\n        <item description="ICS star formation rate" label="Sfr ICS" units="M\u2609/yr">sfrics</item>\r\n        <item description="Cooling rate of hot halo gas" label="Cooling Rate" units="log(erg/s)">cooling</item>\r\n        <item description="AGN heating rate" label="AGN Heating Rate" units="log(erg/s)">heating</item>\r\n        <item description="Dark matter (sub)halo virial mass" label="Mvir" units="10^10 Mpc/h">mvir</item>\r\n        <item description="Central galaxy dark matter halo Mvir" label="Central Galaxy Mvir" units="10^10 M\u2609/h">centralmvir</item>\r\n        <item description="Dark matter (sub)halo virial radius" label="Rvir" units="Mpc/h">rvir</item>\r\n        <item description="Dark matter (sub)halo virial velocity" label="Vvir" units="km/s">vvir</item>\r\n        <item description="Dark matter (sub)halo maximum circular velocity" label="Vmax" units="km/s">vmax</item>\r\n        <item description="Dark matter halo velocity dispersion" label="Velocity Dispersion" units="km/s">veldisp</item>\r\n        <item description="X component of the (sub)halo spin" label="x Spin">spinx</item>\r\n        <item description="Y component of the (sub)halo spin" label="y Spin">spiny</item>\r\n        <item description="Z component of the (sub)halo spin" label="z Spin">spinz</item>\r\n        <item description="Total simulation particles in the dark matter halo" label="Total particles">len</item>\r\n        <item description="X coordinate in the selected box/cone" label="x" units="Mpc/h">pos_x</item>\r\n        <item description="Y coordinate in the selected box/cone" label="y" units="Mpc/h">pos_y</item>\r\n        <item description="Z coordinate in the selected box/cone" label="z" units="Mpc/h">pos_z</item>\r\n        <item description="X component of the galaxy/halo velocity" label="x Velocity" units="km/s">velx</item>\r\n        <item description="Y componentt of the galaxy/halo velocity" label="y Velocity" units="km/s">vely</item>\r\n        <item description="Z componentt of the galaxy/halo velocity" label="z Velocity" units="km/s">velz</item>\r\n        <item description="" label="Central Galaxy ID">centralgal</item>\r\n        <item description="" label="Descendant">descendant</item>\r\n        <item description="" label="FOF Halo Index">fofhaloindex</item>\r\n        <item description="" label="Galaxy Index">globalgalaxyid</item>\r\n        <item description="" label="Global Descendant">globaldescendant</item>\r\n        <item description="" label="Global Index">globalindex</item>\r\n        <item description="" label="Halo Index">haloindex</item>\r\n        <item description="" label="Tree Index">treeindex</item>\r\n        <item description="Original x coordinate in the simulation box" label="x (original)" units="Mpc/h">posx</item>\r\n        <item description="Original y coordinate in the simulation box" label="y (original)" units="Mpc/h">posy</item>\r\n        <item description="Original z coordinate in the simulation box" label="z (original)" units="Mpc/h">posz</item>\r\n        <item description="Simulation snapshot number" label="Snapshot Number">snapnum</item>\r\n      </output-fields>\r\n    </light-cone>\r\n    <votable id="5">\r\n      <fields>\r\n        <item label="Total Stellar Mass" units="10^10 M\u2609/h">stellarmass</item>\r\n        <item label="Bulge Stellar Mass" units="10^10 M\u2609/h">bulgemass</item>\r\n        <item label="Black Hole Mass" units="10^10 M\u2609/h">blackholemass</item>\r\n        <item label="Cold Gas Mass" units="10^10 M\u2609/h">coldgas</item>\r\n        <item label="Hot Gas Mass" units="10^10 M\u2609/h">hotgas</item>\r\n        <item label="Ejected Gas Mass" units="10^10 M\u2609/h">ejectedmass</item>\r\n        <item label="ICS Mass" units="10^10 M\u2609/h">ics</item>\r\n        <item label="Metals Total Stellar Mass" units="10^10 M\u2609/h">metalsstellarmass</item>\r\n        <item label="Metals Bulge Mass" units="10^10 M\u2609/h">metalsbulgemass</item>\r\n        <item label="Metals Cold Gas Mass" units="10^10 M\u2609/h">metalscoldgas</item>\r\n        <item label="Metals Hot Gas Mass" units="10^10 M\u2609/h">metalshotgas</item>\r\n        <item label="Metals Ejected Gas Mass" units="10^10 M\u2609/h">metalsejectedmass</item>\r\n        <item label="Metals ICS Mass" units="10^10 M\u2609/h">metalsics</item>\r\n        <item label="Galaxy Type">objecttype</item>\r\n        <item label="Disk Scale Radius" units="Mpc/h">diskscaleradius</item>\r\n        <item label="Sfr" units="M\u2609/yr">sfr</item>\r\n        <item label="Sfr Bulge" units="M\u2609/yr">sfrbulge</item>\r\n        <item label="Sfr ICS" units="M\u2609/yr">sfrics</item>\r\n        <item label="Cooling Rate" units="log(erg/s)">cooling</item>\r\n        <item label="AGN Heating Rate" units="log(erg/s)">heating</item>\r\n        <item label="Mvir" units="10^10 Mpc/h">mvir</item>\r\n        <item label="Central Galaxy Mvir" units="10^10 M\u2609/h">centralmvir</item>\r\n        <item label="Rvir" units="Mpc/h">rvir</item>\r\n        <item label="Vvir" units="km/s">vvir</item>\r\n        <item label="Vmax" units="km/s">vmax</item>\r\n        <item label="Velocity Dispersion" units="km/s">veldisp</item>\r\n        <item label="x Spin">spinx</item>\r\n        <item label="y Spin">spiny</item>\r\n        <item label="z Spin">spinz</item>\r\n        <item label="Total particles">len</item>\r\n        <item label="x" units="Mpc/h">pos_x</item>\r\n        <item label="y" units="Mpc/h">pos_y</item>\r\n        <item label="z" units="Mpc/h">pos_z</item>\r\n        <item label="x Velocity" units="km/s">velx</item>\r\n        <item label="y Velocity" units="km/s">vely</item>\r\n        <item label="z Velocity" units="km/s">velz</item>\r\n        <item label="Central Galaxy ID">centralgal</item>\r\n        <item label="Descendant">descendant</item>\r\n        <item label="FOF Halo Index">fofhaloindex</item>\r\n        <item label="Galaxy Index">globalgalaxyid</item>\r\n        <item label="Global Descendant">globaldescendant</item>\r\n        <item label="Global Index">globalindex</item>\r\n        <item label="Halo Index">haloindex</item>\r\n        <item label="Tree Index">treeindex</item>\r\n        <item label="x (original)" units="Mpc/h">posx</item>\r\n        <item label="y (original)" units="Mpc/h">posy</item>\r\n        <item label="z (original)" units="Mpc/h">posz</item>\r\n        <item label="Snapshot Number">snapnum</item>\r\n      </fields>\r\n      <parents>\r\n        <item>1</item>\r\n      </parents>\r\n      <module-version>1</module-version>\r\n      <filename>tao.output.votable</filename>\r\n    </votable>\r\n    <record-filter>\r\n      <module-version>1</module-version>\r\n      <filter>\r\n        <filter-attribute>stellarmass</filter-attribute>\r\n        <filter-min units="10^10 M\u2609/h">1.0</filter-min>\r\n        <filter-max units="10^10 M\u2609/h">None</filter-max>\r\n      </filter>\r\n    </record-filter>\r\n  </workflow>\r\n  <signature>base64encodedsignature</signature>\r\n</tao>\r\n'
    tao_job_5.output_path = u'stagingjobs/alistair/6/output'
    tao_job_5.database = u'millennium_mini_hdf5_dist'
    tao_job_5.error_message = u''
    tao_job_5 = save_or_locate(tao_job_5)

    tao_job_6 = Job()
    tao_job_6.user = tao_taouser_2
    tao_job_6.created_time = datetime.datetime(2013, 7, 16, 11, 52, 34, tzinfo=pytz.UTC)
    tao_job_6.description = u''
    tao_job_6.status = u'COMPLETED'
    tao_job_6.parameters = u'<?xml version=\'1.0\' encoding=\'utf-8\'?>\n<tao timestamp="2013-07-16T21:52:34+10:00" xmlns="http://tao.asvo.org.au/schema/module-parameters-v1">\n  <username>alistair</username>\n  <workflow name="alpha-light-cone-image">\n    <schema-version>2.0</schema-version>\n    <light-cone id="1">\n      <module-version>1</module-version>\n      <geometry>box</geometry>\n      <simulation>Mini-Millennium</simulation>\n      <galaxy-model>SAGE</galaxy-model>\n      <redshift>0E-10</redshift>\n      <query-box-size units="Mpc">62.500</query-box-size>\n      <output-fields>\n        <item description="Galaxy total stellar mass" label="Total Stellar Mass" units="10+10solMass/h">stellarmass</item>\n        <item description="Galaxy bulge stellar mass" label="Bulge Stellar Mass" units="10+10solMass/h">bulgemass</item>\n        <item description="Supermassive black hole mass" label="Black Hole Mass" units="10+10solMass/h">blackholemass</item>\n        <item description="Mass of cold gas in the galaxy" label="Cold Gas Mass" units="10+10solMass/h">coldgas</item>\n        <item description="Mass of hot halo gas" label="Hot Gas Mass" units="10+10solMass/h">hotgas</item>\n        <item description="Gas mass ejected from halo" label="Ejected Gas Mass" units="10+10solMass/h">ejectedmass</item>\n        <item description="Stellar mass in intracluster stars" label="ICS Mass" units="10+10solMass/h">ics</item>\n        <item description="Mass of metals in the total stellar mass" label="Metals Total Stellar Mass" units="10+10solMass/h">metalsstellarmass</item>\n        <item description="Mass of metals in the bulge" label="Metals Bulge Mass" units="10+10solMass/h">metalsbulgemass</item>\n        <item description="Mass of metals in the cold gas" label="Metals Cold Gas Mass" units="10+10solMass/h">metalscoldgas</item>\n        <item description="Mass of metals in the hot gas" label="Metals Hot Gas Mass" units="10+10solMass/h">metalshotgas</item>\n        <item description="Mass of metals in the ejected gas" label="Metals Ejected Gas Mass" units="10+10solMass/h">metalsejectedmass</item>\n        <item description="Mass of metals in the ICS" label="Metals ICS Mass" units="10+10solMass/h">metalsics</item>\n        <item description="0=Central, 1=Satellite" label="Galaxy Type">objecttype</item>\n        <item description="Stellar disk scale radius" label="Disk Scale Radius" units="10+6pc/h">diskscaleradius</item>\n        <item description="Total star formation rate in the galaxy" label="Sfr" units="solMass/yr">sfr</item>\n        <item description="Bulge star formation rate" label="Sfr Bulge" units="solMass/yr">sfrbulge</item>\n        <item description="ICS star formation rate" label="Sfr ICS" units="solMass/yr">sfrics</item>\n        <item description="Cooling rate of hot halo gas" label="Cooling Rate" units="[erg/s]">cooling</item>\n        <item description="AGN heating rate" label="AGN Heating Rate" units="[erg/s]">heating</item>\n        <item description="Dark matter (sub)halo virial mass" label="Mvir" units="10+10Mpc/h">mvir</item>\n        <item description="Central galaxy dark matter halo Mvir" label="Central Galaxy Mvir" units="10+10solMass/h">centralmvir</item>\n        <item description="Dark matter (sub)halo virial radius" label="Rvir" units="10+6pc/h">rvir</item>\n        <item description="Dark matter (sub)halo virial velocity" label="Vvir" units="km/s">vvir</item>\n        <item description="Dark matter (sub)halo maximum circular velocity" label="Vmax" units="km/s">vmax</item>\n        <item description="Dark matter halo velocity dispersion" label="Velocity Dispersion" units="km/s">veldisp</item>\n        <item description="X component of the (sub)halo spin" label="x Spin">spinx</item>\n        <item description="Y component of the (sub)halo spin" label="y Spin">spiny</item>\n        <item description="Z component of the (sub)halo spin" label="z Spin">spinz</item>\n        <item description="Total simulation particles in the dark matter halo" label="Total particles">len</item>\n        <item description="X coordinate in the selected box/cone" label="x" units="10+6pc/h">pos_x</item>\n        <item description="Y coordinate in the selected box/cone" label="y" units="10+6pc/h">pos_y</item>\n        <item description="Z coordinate in the selected box/cone" label="z" units="10+6pc/h">pos_z</item>\n        <item description="X component of the galaxy/halo velocity" label="x Velocity" units="km/s">velx</item>\n        <item description="Y componentt of the galaxy/halo velocity" label="y Velocity" units="km/s">vely</item>\n        <item description="Z componentt of the galaxy/halo velocity" label="z Velocity" units="km/s">velz</item>\n        <item description="" label="Central Galaxy ID">centralgal</item>\n        <item description="" label="Descendant">descendant</item>\n        <item description="" label="FOF Halo Index">fofhaloindex</item>\n        <item description="" label="Galaxy Index">globalgalaxyid</item>\n        <item description="" label="Global Descendant">globaldescendant</item>\n        <item description="" label="Global Index">globalindex</item>\n        <item description="" label="Halo Index">haloindex</item>\n        <item description="" label="Tree Index">treeindex</item>\n        <item description="Original x coordinate in the simulation box" label="x (original)" units="10+6pc/h">posx</item>\n        <item description="Original y coordinate in the simulation box" label="y (original)" units="10+6pc/h">posy</item>\n        <item description="Original z coordinate in the simulation box" label="z (original)" units="10+6pc/h">posz</item>\n        <item description="Simulation snapshot number" label="Snapshot Number">snapnum</item>\n      </output-fields>\n    </light-cone>\n    <csv id="5">\n      <fields>\n        <item label="Total Stellar Mass" units="10+10solMass/h">stellarmass</item>\n        <item label="Bulge Stellar Mass" units="10+10solMass/h">bulgemass</item>\n        <item label="Black Hole Mass" units="10+10solMass/h">blackholemass</item>\n        <item label="Cold Gas Mass" units="10+10solMass/h">coldgas</item>\n        <item label="Hot Gas Mass" units="10+10solMass/h">hotgas</item>\n        <item label="Ejected Gas Mass" units="10+10solMass/h">ejectedmass</item>\n        <item label="ICS Mass" units="10+10solMass/h">ics</item>\n        <item label="Metals Total Stellar Mass" units="10+10solMass/h">metalsstellarmass</item>\n        <item label="Metals Bulge Mass" units="10+10solMass/h">metalsbulgemass</item>\n        <item label="Metals Cold Gas Mass" units="10+10solMass/h">metalscoldgas</item>\n        <item label="Metals Hot Gas Mass" units="10+10solMass/h">metalshotgas</item>\n        <item label="Metals Ejected Gas Mass" units="10+10solMass/h">metalsejectedmass</item>\n        <item label="Metals ICS Mass" units="10+10solMass/h">metalsics</item>\n        <item label="Galaxy Type">objecttype</item>\n        <item label="Disk Scale Radius" units="10+6pc/h">diskscaleradius</item>\n        <item label="Sfr" units="solMass/yr">sfr</item>\n        <item label="Sfr Bulge" units="solMass/yr">sfrbulge</item>\n        <item label="Sfr ICS" units="solMass/yr">sfrics</item>\n        <item label="Cooling Rate" units="[erg/s]">cooling</item>\n        <item label="AGN Heating Rate" units="[erg/s]">heating</item>\n        <item label="Mvir" units="10+10Mpc/h">mvir</item>\n        <item label="Central Galaxy Mvir" units="10+10solMass/h">centralmvir</item>\n        <item label="Rvir" units="10+6pc/h">rvir</item>\n        <item label="Vvir" units="km/s">vvir</item>\n        <item label="Vmax" units="km/s">vmax</item>\n        <item label="Velocity Dispersion" units="km/s">veldisp</item>\n        <item label="x Spin">spinx</item>\n        <item label="y Spin">spiny</item>\n        <item label="z Spin">spinz</item>\n        <item label="Total particles">len</item>\n        <item label="x" units="10+6pc/h">pos_x</item>\n        <item label="y" units="10+6pc/h">pos_y</item>\n        <item label="z" units="10+6pc/h">pos_z</item>\n        <item label="x Velocity" units="km/s">velx</item>\n        <item label="y Velocity" units="km/s">vely</item>\n        <item label="z Velocity" units="km/s">velz</item>\n        <item label="Central Galaxy ID">centralgal</item>\n        <item label="Descendant">descendant</item>\n        <item label="FOF Halo Index">fofhaloindex</item>\n        <item label="Galaxy Index">globalgalaxyid</item>\n        <item label="Global Descendant">globaldescendant</item>\n        <item label="Global Index">globalindex</item>\n        <item label="Halo Index">haloindex</item>\n        <item label="Tree Index">treeindex</item>\n        <item label="x (original)" units="10+6pc/h">posx</item>\n        <item label="y (original)" units="10+6pc/h">posy</item>\n        <item label="z (original)" units="10+6pc/h">posz</item>\n        <item label="Snapshot Number">snapnum</item>\n      </fields>\n      <parents>\n        <item>1</item>\n      </parents>\n      <module-version>1</module-version>\n      <filename>tao.output.csv</filename>\n    </csv>\n    <record-filter>\n      <module-version>1</module-version>\n      <filter>\n        <filter-attribute>stellarmass</filter-attribute>\n        <filter-min units="10+10solMass/h">1.0</filter-min>\n        <filter-max units="10+10solMass/h">None</filter-max>\n      </filter>\n    </record-filter>\n  </workflow>\n  <signature>base64encodedsignature</signature>\n</tao>\n'
    tao_job_6.output_path = u'stagingjobs/alistair/7/output'
    tao_job_6.database = u'millennium_mini_hdf5_dist'
    tao_job_6.error_message = u''
    tao_job_6 = save_or_locate(tao_job_6)

    tao_job_7 = Job()
    tao_job_7.user = tao_taouser_2
    tao_job_7.created_time = datetime.datetime(2013, 7, 16, 11, 54, 44, tzinfo=pytz.UTC)
    tao_job_7.description = u''
    tao_job_7.status = u'COMPLETED'
    tao_job_7.parameters = u'<?xml version=\'1.0\' encoding=\'utf-8\'?>\n<tao timestamp="2013-07-16T21:54:43+10:00" xmlns="http://tao.asvo.org.au/schema/module-parameters-v1">\n  <username>alistair</username>\n  <workflow name="alpha-light-cone-image">\n    <schema-version>2.0</schema-version>\n    <light-cone id="1">\n      <module-version>1</module-version>\n      <geometry>box</geometry>\n      <simulation>Mini-Millennium</simulation>\n      <galaxy-model>SAGE</galaxy-model>\n      <redshift>0E-10</redshift>\n      <query-box-size units="Mpc">62.500</query-box-size>\n      <output-fields>\n        <item description="Galaxy total stellar mass" label="Total Stellar Mass" units="10+10solMass/h">stellarmass</item>\n        <item description="Galaxy bulge stellar mass" label="Bulge Stellar Mass" units="10+10solMass/h">bulgemass</item>\n        <item description="Supermassive black hole mass" label="Black Hole Mass" units="10+10solMass/h">blackholemass</item>\n        <item description="Mass of cold gas in the galaxy" label="Cold Gas Mass" units="10+10solMass/h">coldgas</item>\n        <item description="Mass of hot halo gas" label="Hot Gas Mass" units="10+10solMass/h">hotgas</item>\n        <item description="Gas mass ejected from halo" label="Ejected Gas Mass" units="10+10solMass/h">ejectedmass</item>\n        <item description="Stellar mass in intracluster stars" label="ICS Mass" units="10+10solMass/h">ics</item>\n        <item description="Mass of metals in the total stellar mass" label="Metals Total Stellar Mass" units="10+10solMass/h">metalsstellarmass</item>\n        <item description="Mass of metals in the bulge" label="Metals Bulge Mass" units="10+10solMass/h">metalsbulgemass</item>\n        <item description="Mass of metals in the cold gas" label="Metals Cold Gas Mass" units="10+10solMass/h">metalscoldgas</item>\n        <item description="Mass of metals in the hot gas" label="Metals Hot Gas Mass" units="10+10solMass/h">metalshotgas</item>\n        <item description="Mass of metals in the ejected gas" label="Metals Ejected Gas Mass" units="10+10solMass/h">metalsejectedmass</item>\n        <item description="Mass of metals in the ICS" label="Metals ICS Mass" units="10+10solMass/h">metalsics</item>\n        <item description="0=Central, 1=Satellite" label="Galaxy Type">objecttype</item>\n        <item description="Stellar disk scale radius" label="Disk Scale Radius" units="10+6pc/h">diskscaleradius</item>\n        <item description="Total star formation rate in the galaxy" label="Sfr" units="solMass/yr">sfr</item>\n        <item description="Bulge star formation rate" label="Sfr Bulge" units="solMass/yr">sfrbulge</item>\n        <item description="ICS star formation rate" label="Sfr ICS" units="solMass/yr">sfrics</item>\n        <item description="Cooling rate of hot halo gas" label="Cooling Rate" units="[erg/s]">cooling</item>\n        <item description="AGN heating rate" label="AGN Heating Rate" units="[erg/s]">heating</item>\n        <item description="Dark matter (sub)halo virial mass" label="Mvir" units="10+10Mpc/h">mvir</item>\n        <item description="Central galaxy dark matter halo Mvir" label="Central Galaxy Mvir" units="10+10solMass/h">centralmvir</item>\n        <item description="Dark matter (sub)halo virial radius" label="Rvir" units="10+6pc/h">rvir</item>\n        <item description="Dark matter (sub)halo virial velocity" label="Vvir" units="km/s">vvir</item>\n        <item description="Dark matter (sub)halo maximum circular velocity" label="Vmax" units="km/s">vmax</item>\n        <item description="Dark matter halo velocity dispersion" label="Velocity Dispersion" units="km/s">veldisp</item>\n        <item description="X component of the (sub)halo spin" label="x Spin">spinx</item>\n        <item description="Y component of the (sub)halo spin" label="y Spin">spiny</item>\n        <item description="Z component of the (sub)halo spin" label="z Spin">spinz</item>\n        <item description="Total simulation particles in the dark matter halo" label="Total particles">len</item>\n        <item description="X coordinate in the selected box/cone" label="x" units="10+6pc/h">pos_x</item>\n        <item description="Y coordinate in the selected box/cone" label="y" units="10+6pc/h">pos_y</item>\n        <item description="Z coordinate in the selected box/cone" label="z" units="10+6pc/h">pos_z</item>\n        <item description="X component of the galaxy/halo velocity" label="x Velocity" units="km/s">velx</item>\n        <item description="Y componentt of the galaxy/halo velocity" label="y Velocity" units="km/s">vely</item>\n        <item description="Z componentt of the galaxy/halo velocity" label="z Velocity" units="km/s">velz</item>\n        <item description="" label="Central Galaxy ID">centralgal</item>\n        <item description="" label="Descendant">descendant</item>\n        <item description="" label="FOF Halo Index">fofhaloindex</item>\n        <item description="" label="Galaxy Index">globalgalaxyid</item>\n        <item description="" label="Global Descendant">globaldescendant</item>\n        <item description="" label="Global Index">globalindex</item>\n        <item description="" label="Halo Index">haloindex</item>\n        <item description="" label="Tree Index">treeindex</item>\n        <item description="Original x coordinate in the simulation box" label="x (original)" units="10+6pc/h">posx</item>\n        <item description="Original y coordinate in the simulation box" label="y (original)" units="10+6pc/h">posy</item>\n        <item description="Original z coordinate in the simulation box" label="z (original)" units="10+6pc/h">posz</item>\n        <item description="Simulation snapshot number" label="Snapshot Number">snapnum</item>\n      </output-fields>\n    </light-cone>\n    <votable id="5">\n      <fields>\n        <item label="Total Stellar Mass" units="10+10solMass/h">stellarmass</item>\n        <item label="Bulge Stellar Mass" units="10+10solMass/h">bulgemass</item>\n        <item label="Black Hole Mass" units="10+10solMass/h">blackholemass</item>\n        <item label="Cold Gas Mass" units="10+10solMass/h">coldgas</item>\n        <item label="Hot Gas Mass" units="10+10solMass/h">hotgas</item>\n        <item label="Ejected Gas Mass" units="10+10solMass/h">ejectedmass</item>\n        <item label="ICS Mass" units="10+10solMass/h">ics</item>\n        <item label="Metals Total Stellar Mass" units="10+10solMass/h">metalsstellarmass</item>\n        <item label="Metals Bulge Mass" units="10+10solMass/h">metalsbulgemass</item>\n        <item label="Metals Cold Gas Mass" units="10+10solMass/h">metalscoldgas</item>\n        <item label="Metals Hot Gas Mass" units="10+10solMass/h">metalshotgas</item>\n        <item label="Metals Ejected Gas Mass" units="10+10solMass/h">metalsejectedmass</item>\n        <item label="Metals ICS Mass" units="10+10solMass/h">metalsics</item>\n        <item label="Galaxy Type">objecttype</item>\n        <item label="Disk Scale Radius" units="10+6pc/h">diskscaleradius</item>\n        <item label="Sfr" units="solMass/yr">sfr</item>\n        <item label="Sfr Bulge" units="solMass/yr">sfrbulge</item>\n        <item label="Sfr ICS" units="solMass/yr">sfrics</item>\n        <item label="Cooling Rate" units="[erg/s]">cooling</item>\n        <item label="AGN Heating Rate" units="[erg/s]">heating</item>\n        <item label="Mvir" units="10+10Mpc/h">mvir</item>\n        <item label="Central Galaxy Mvir" units="10+10solMass/h">centralmvir</item>\n        <item label="Rvir" units="10+6pc/h">rvir</item>\n        <item label="Vvir" units="km/s">vvir</item>\n        <item label="Vmax" units="km/s">vmax</item>\n        <item label="Velocity Dispersion" units="km/s">veldisp</item>\n        <item label="x Spin">spinx</item>\n        <item label="y Spin">spiny</item>\n        <item label="z Spin">spinz</item>\n        <item label="Total particles">len</item>\n        <item label="x" units="10+6pc/h">pos_x</item>\n        <item label="y" units="10+6pc/h">pos_y</item>\n        <item label="z" units="10+6pc/h">pos_z</item>\n        <item label="x Velocity" units="km/s">velx</item>\n        <item label="y Velocity" units="km/s">vely</item>\n        <item label="z Velocity" units="km/s">velz</item>\n        <item label="Central Galaxy ID">centralgal</item>\n        <item label="Descendant">descendant</item>\n        <item label="FOF Halo Index">fofhaloindex</item>\n        <item label="Galaxy Index">globalgalaxyid</item>\n        <item label="Global Descendant">globaldescendant</item>\n        <item label="Global Index">globalindex</item>\n        <item label="Halo Index">haloindex</item>\n        <item label="Tree Index">treeindex</item>\n        <item label="x (original)" units="10+6pc/h">posx</item>\n        <item label="y (original)" units="10+6pc/h">posy</item>\n        <item label="z (original)" units="10+6pc/h">posz</item>\n        <item label="Snapshot Number">snapnum</item>\n      </fields>\n      <parents>\n        <item>1</item>\n      </parents>\n      <module-version>1</module-version>\n      <filename>tao.output.xml</filename>\n    </votable>\n    <record-filter>\n      <module-version>1</module-version>\n      <filter>\n        <filter-attribute>stellarmass</filter-attribute>\n        <filter-min units="10+10solMass/h">1.0</filter-min>\n        <filter-max units="10+10solMass/h">None</filter-max>\n      </filter>\n    </record-filter>\n  </workflow>\n  <signature>base64encodedsignature</signature>\n</tao>\n'
    tao_job_7.output_path = u'stagingjobs/alistair/8/output'
    tao_job_7.database = u'millennium_mini_hdf5_dist'
    tao_job_7.error_message = u''
    tao_job_7 = save_or_locate(tao_job_7)

    tao_job_8 = Job()
    tao_job_8.user = tao_taouser_4
    tao_job_8.created_time = datetime.datetime(2013, 7, 17, 6, 17, 7, tzinfo=pytz.UTC)
    tao_job_8.description = u''
    tao_job_8.status = u'QUEUED'
    tao_job_8.parameters = u'<?xml version=\'1.0\' encoding=\'utf-8\'?>\n<tao timestamp="2013-07-17T16:17:07+10:00" xmlns="http://tao.asvo.org.au/schema/module-parameters-v1">\n  <username>max</username>\n  <workflow name="alpha-light-cone-image">\n    <schema-version>2.0</schema-version>\n    <light-cone id="1">\n      <module-version>1</module-version>\n      <geometry>box</geometry>\n      <simulation>Mini-Millennium</simulation>\n      <galaxy-model>SAGE</galaxy-model>\n      <redshift>0E-10</redshift>\n      <query-box-size units="Mpc">50</query-box-size>\n      <output-fields>\n        <item description="Galaxy total stellar mass" label="Total Stellar Mass" units="10+10solMass/h">stellarmass</item>\n        <item description="Total star formation rate in the galaxy" label="Sfr" units="solMass/yr">sfr</item>\n      </output-fields>\n    </light-cone>\n    <csv id="5">\n      <fields>\n        <item label="Total Stellar Mass" units="10+10solMass/h">stellarmass</item>\n        <item label="Sfr" units="solMass/yr">sfr</item>\n        <item label="Johnson B (Absolute)">Johnson/Johnson_B.dati_absolute</item>\n        <item label="Johnson I (Absolute)">Johnson/Ifilter.dati_absolute</item>\n        <item label="Johnson J (Absolute)">Johnson/j.dat_absolute</item>\n        <item label="Johnson K (Absolute)">Johnson/k.dat_absolute</item>\n        <item label="Johnson R (Absolute)">Johnson/Rfilter.dati_absolute</item>\n        <item label="Johnson U (Absolute)">Johnson/Johnson_U.dati_absolute</item>\n        <item label="Johnson V (Absolute)">Johnson/Johnson_V.dati_absolute</item>\n      </fields>\n      <parents>\n        <item>4</item>\n      </parents>\n      <module-version>1</module-version>\n      <filename>tao.output.csv</filename>\n    </csv>\n    <sed id="2">\n      <module-version>1</module-version>\n      <parents>\n        <item>1</item>\n      </parents>\n      <single-stellar-population-model>ssp.ssz</single-stellar-population-model>\n    </sed>\n    <filter id="4">\n      <module-version>1</module-version>\n      <parents>\n        <item>3</item>\n      </parents>\n      <bandpass-filters>\n        <item description="&lt;p&gt;Johnson B band&lt;/p&gt;&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/Johnson_Johnson_B.dati.html&quot;&gt;Johnson B&lt;/a&gt;.&lt;/p&gt;" label="Johnson B" selected="absolute">Johnson/Johnson_B.dati</item>\n        <item description="&lt;p&gt;Johnson I band&lt;/p&gt;&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/Johnson_Ifilter.dati.html&quot;&gt;Johnson I&lt;/a&gt;.&lt;/p&gt;" label="Johnson I" selected="absolute">Johnson/Ifilter.dati</item>\n        <item description="&lt;p&gt;Johnson J band&lt;/p&gt;&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/Johnson_j.dat.html&quot;&gt;Johnson J&lt;/a&gt;.&lt;/p&gt;" label="Johnson J" selected="absolute">Johnson/j.dat</item>\n        <item description="&lt;p&gt;Johnson K band&lt;/p&gt;&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/Johnson_k.dat.html&quot;&gt;Johnson K&lt;/a&gt;.&lt;/p&gt;" label="Johnson K" selected="absolute">Johnson/k.dat</item>\n        <item description="&lt;p&gt;Johnson R band&lt;/p&gt;&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/Johnson_Rfilter.dati.html&quot;&gt;Johnson R&lt;/a&gt;.&lt;/p&gt;" label="Johnson R" selected="absolute">Johnson/Rfilter.dati</item>\n        <item description="&lt;p&gt;Johnson U band&lt;/p&gt;&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/Johnson_Johnson_U.dati.html&quot;&gt;Johnson U&lt;/a&gt;.&lt;/p&gt;" label="Johnson U" selected="absolute">Johnson/Johnson_U.dati</item>\n        <item description="&lt;p&gt;Johnson V band&lt;/p&gt;&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/Johnson_Johnson_V.dati.html&quot;&gt;Johnson V&lt;/a&gt;.&lt;/p&gt;" label="Johnson V" selected="absolute">Johnson/Johnson_V.dati</item>\n      </bandpass-filters>\n    </filter>\n    <dust id="3">\n      <module-version>1</module-version>\n      <parents>\n        <item>2</item>\n      </parents>\n      <model>Tonini et al. 2012</model>\n    </dust>\n    <record-filter>\n      <module-version>1</module-version>\n      <filter>\n        <filter-attribute>stellarmass</filter-attribute>\n        <filter-min units="10+10solMass/h">0.01</filter-min>\n        <filter-max units="10+10solMass/h">None</filter-max>\n      </filter>\n    </record-filter>\n  </workflow>\n  <signature>base64encodedsignature</signature>\n</tao>\n'
    tao_job_8.output_path = u''
    tao_job_8.database = u'millennium_mini_hdf5_dist'
    tao_job_8.error_message = u''
    tao_job_8 = save_or_locate(tao_job_8)

    #Re-processing model: WorkflowCommand

    tao_workflowcommand_1.job_id = tao_job_2
    tao_workflowcommand_1.submitted_by = tao_taouser_3
    tao_workflowcommand_1 = save_or_locate(tao_workflowcommand_1)

    tao_workflowcommand_2.job_id = tao_job_2
    tao_workflowcommand_2.submitted_by = tao_taouser_3
    tao_workflowcommand_2 = save_or_locate(tao_workflowcommand_2)

    tao_workflowcommand_3.submitted_by = tao_taouser_3
    tao_workflowcommand_3 = save_or_locate(tao_workflowcommand_3)

    #Re-processing model: TaoUser







    #Re-processing model: DataSet

    tao_dataset_1.default_filter_field = tao_datasetproperty_2
    tao_dataset_1 = save_or_locate(tao_dataset_1)

    tao_dataset_2.default_filter_field = tao_datasetproperty_2
    tao_dataset_2 = save_or_locate(tao_dataset_2)

    tao_dataset_3.default_filter_field = tao_datasetproperty_3
    tao_dataset_3 = save_or_locate(tao_dataset_3)

    #Re-processing model: DataSetProperty

    #Re-processing model: Snapshot

    #Re-processing model: Job

