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
    tao_simulation_1.details = u'<p>Cosmology: WMAP5<br/>\r\nCosmological parameters: \u03a9m = 0.27, \u03a9\u039b = 0.73, \u03a9b = 0.0469, \u03c38 = 0.82, h = 0.70, n=0.95<br/>\r\nBox Size: 250 Mpc/h<br/>\r\nMass resolution: 1.35x10^8 Msun/h<br/>\r\nForce resolution: 1 kpc/h\r\n</p>\r\n<p>Paper: <a href="http://arxiv.org/abs/1002.3660" target="_blank">Klypin, Trujillo-Gomez & Primack 2011</a><br/>\r\nExternal link: <a href="http://hipacc.ucsc.edu/Bolshoi/" target="_blank">The Bolshoi cosmological simulation</a>\r\n</p>'
    tao_simulation_1.order = 3L
    tao_simulation_1 = save_or_locate(tao_simulation_1)

    tao_simulation_2 = Simulation()
    tao_simulation_2.name = u'Millennium'
    tao_simulation_2.box_size_units = u'Mpc/h'
    tao_simulation_2.box_size = Decimal('500.000')
    tao_simulation_2.details = u'<p>\r\nCosmology: WMAP-1<br/>\r\nCosmological parameters: \u03a9m = 0.25, \u03a9\u039b = 0.75, \u03a9b = 0.045, \u03c38 = 0.9, h = 0.73, n = 1<br/>\r\nBox size: 500 Mpc/h<br/>\r\nMass resolution: 8.6x10^8 Msun/h<br/>\r\nForce resolution: 5 kpc/h\r\n</p>\r\n<p>Paper: <a href="http://arxiv.org/abs/astro-ph/0504097" target="_blank"> Springel et al. 2005</a><br/>\r\nExternal link: <a href="http://www.mpa-garching.mpg.de/millennium/"" target="_blank">The German Astrophysical Virtual Observatory</a>\r\n</p>'
    tao_simulation_2.order = 0L
    tao_simulation_2 = save_or_locate(tao_simulation_2)

    tao_simulation_3 = Simulation()
    tao_simulation_3.name = u'Mini-Millennium'
    tao_simulation_3.box_size_units = u'Mpc/h'
    tao_simulation_3.box_size = Decimal('62.500')
    tao_simulation_3.details = u'<p>\r\nCosmology: WMAP-1<br/>\r\nCosmological parameters: \u03a9m = 0.25, \u03a9\u039b = 0.75, \u03a9b = 0.045, \u03c38 = 0.9, h = 0.73, n = 1<br/>\r\nBox size: 62.5 Mpc/h<br/>\r\nMass resolution: 8.6x10^8 Msun/h<br/>\r\nForce resolution: 5 kpc/h\r\n</p>\r\n<p>Paper: <a href="http://arxiv.org/abs/astro-ph/0504097" target="_blank"> Springel et al. 2005</a><br/>\r\nExternal link: <a href="http://www.mpa-garching.mpg.de/millennium/"" target="_blank">The German Astrophysical Virtual Observatory</a>\r\n</p>'
    tao_simulation_3.order = 0L
    tao_simulation_3 = save_or_locate(tao_simulation_3)

    #Processing model: GalaxyModel

    from tao.models import GalaxyModel

    tao_galaxymodel_1 = GalaxyModel()
    tao_galaxymodel_1.name = u'Galacticus'
    tao_galaxymodel_1.details = u'Galacticus is a new open source semi-analytic galaxy model from Andrew Benson.<br/>\r\nPaper: <a href="http://arxiv.org/abs/1008.1786" target="_blank">Benson 2010</a>'
    tao_galaxymodel_1 = save_or_locate(tao_galaxymodel_1)

    tao_galaxymodel_2 = GalaxyModel()
    tao_galaxymodel_2.name = u'SAGE'
    tao_galaxymodel_2.details = u'The "Semi-Analytic Galaxy Evolution" (SAGE) galaxy model is an updated version of the Croton et al. 2006 galaxy model. It is still under development, with a publication expected at the end of 2013.<br/>\r\nPaper: <a href="http://arxiv.org/abs/astro-ph/0602065" target="_blank">Croton et al. 2006</a>'
    tao_galaxymodel_2 = save_or_locate(tao_galaxymodel_2)

    #Processing model: StellarModel

    from tao.models import StellarModel

    tao_stellarmodel_1 = StellarModel()
    tao_stellarmodel_1.name = u'm05/ssp.ssz'
    tao_stellarmodel_1.label = u'Maraston (2005), Salpeter IMF'
    tao_stellarmodel_1.description = u'<p>External link: <a href="http://www.icg.port.ac.uk/~maraston/Claudia%27s_Stellar_Population_Model.html" target="_blank">Maraston stellar population models</a></p>\r\n<ul>\r\n<li>All magnitudes assume the simulation little h value from General Properties</li>\r\n<li>Magnitudes are calculated in the AB system</li>\r\n</ul>\r\n<p>Additional information is available from the <a href="../static/docs/user-manual/sed.html" target="_blank">SED Module documentation</a>.</p>'
    tao_stellarmodel_1.encoding = u'<single-stellar-population-model>m05/ssp.ssz</single-stellar-population-model>\r\n<wavelengths-file>m05/wavelengths.dat</wavelengths-file>\r\n<ages-file>m05/ages.dat</ages-file>\r\n<metallicities-file>m05/metallicities.dat</metallicities-file>'
    tao_stellarmodel_1 = save_or_locate(tao_stellarmodel_1)

    tao_stellarmodel_2 = StellarModel()
    tao_stellarmodel_2.name = u'm05/ssp.krz'
    tao_stellarmodel_2.label = u'Maraston (2005), Kroupa IMF'
    tao_stellarmodel_2.description = u'<p>External link: <a href="http://www.icg.port.ac.uk/~maraston/Claudia%27s_Stellar_Population_Model.html" target="_blank">Maraston stellar population models</a></p>\r\n<ul>\r\n<li>All magnitudes assume the simulation little h value from General Properties</li>\r\n<li>Magnitudes are calculated in the AB system</li>\r\n</ul>\r\n<p>Additional information is available from the <a href="../static/docs/user-manual/sed.html" target="_blank">SED Module documentation</a>.</p>'
    tao_stellarmodel_2.encoding = u'<single-stellar-population-model>m05/ssp.krz</single-stellar-population-model>\r\n<wavelengths-file>m05/wavelengths.dat</wavelengths-file>\r\n<ages-file>m05/ages.dat</ages-file>\r\n<metallicities-file>m05/metallicities.dat</metallicities-file>'
    tao_stellarmodel_2 = save_or_locate(tao_stellarmodel_2)

    tao_stellarmodel_3 = StellarModel()
    tao_stellarmodel_3.name = u'conroy/ssp_kroupa_no_mass_norm.dat'
    tao_stellarmodel_3.label = u'Conroy et al. (2009), Kroupa IMF'
    tao_stellarmodel_3.description = u'<p>External link: <a href="http://people.ucsc.edu/~conroy/FSPS.html" target="_blank">Flexible Stellar Population Synthesis (FSPS)</a></p>\r\n<ul>\r\n<li>All magnitudes assume the simulation little h value from General Properties</li>\r\n<li>Magnitudes are calculated in the AB system</li>\r\n</ul>\r\n<p>Additional information is available from the <a href="../static/docs/user-manual/sed.html" target="_blank">SED Module documentation</a>.</p>'
    tao_stellarmodel_3.encoding = u'<single-stellar-population-model>conroy/ssp_kroupa_no_mass_norm.dat</single-stellar-population-model>\r\n<wavelengths-file>conroy/wavelengths.dat</wavelengths-file>\r\n<ages-file>conroy/ages.dat</ages-file>\r\n<metallicities-file>conroy/metallicities.dat</metallicities-file>\r\n'
    tao_stellarmodel_3 = save_or_locate(tao_stellarmodel_3)

    tao_stellarmodel_4 = StellarModel()
    tao_stellarmodel_4.name = u'conroy/ssp_salpeter_no_mass_norm.dat'
    tao_stellarmodel_4.label = u'Conroy et al. (2009), Salpeter IMF'
    tao_stellarmodel_4.description = u'<p>External link: <a href="http://people.ucsc.edu/~conroy/FSPS.html" target="_blank">Flexible Stellar Population Synthesis (FSPS)</a></p>\r\n<ul>\r\n<li>All magnitudes assume the simulation little h value from General Properties</li>\r\n<li>Magnitudes are calculated in the AB system</li>\r\n</ul>\r\n<p>Additional information is available from the <a href="../static/docs/user-manual/sed.html" target="_blank">SED Module documentation</a>.</p>'
    tao_stellarmodel_4.encoding = u'<single-stellar-population-model>conroy/ssp_salpeter_no_mass_norm.dat</single-stellar-population-model>\r\n<wavelengths-file>conroy/wavelengths.dat</wavelengths-file>\r\n<ages-file>conroy/ages.dat</ages-file>\r\n<metallicities-file>conroy/metallicities.dat</metallicities-file>\r\n'
    tao_stellarmodel_4 = save_or_locate(tao_stellarmodel_4)

    tao_stellarmodel_5 = StellarModel()
    tao_stellarmodel_5.name = u'conroy/ssp_chabrier_no_mass_norm.dat'
    tao_stellarmodel_5.label = u'Conroy et al. (2009), Chabrier IMF'
    tao_stellarmodel_5.description = u'<p>External link: <a href="http://people.ucsc.edu/~conroy/FSPS.html" target="_blank">Flexible Stellar Population Synthesis (FSPS)</a></p>\r\n<ul>\r\n<li>All magnitudes assume the simulation little h value from General Properties</li>\r\n<li>Magnitudes are calculated in the AB system</li>\r\n</ul>\r\n<p>Additional information is available from the <a href="../static/docs/user-manual/sed.html" target="_blank">SED Module documentation</a>.</p>'
    tao_stellarmodel_5.encoding = u'<single-stellar-population-model>conroy/ssp_chabrier_no_mass_norm.dat</single-stellar-population-model>\r\n<wavelengths-file>conroy/wavelengths.dat</wavelengths-file>\r\n<ages-file>conroy/ages.dat</ages-file>\r\n<metallicities-file>conroy/metallicities.dat</metallicities-file>\r\n'
    tao_stellarmodel_5 = save_or_locate(tao_stellarmodel_5)

    tao_stellarmodel_6 = StellarModel()
    tao_stellarmodel_6.name = u'bc03/ssp_kroupa.dat'
    tao_stellarmodel_6.label = u'Bruzual & Charlot (2003), Kroupa IMF'
    tao_stellarmodel_6.description = u'<p>External link: <a href="http://www2.iap.fr/users/charlot/bc2003/" target="_blank">GALAXEV</a></p>\r\n<ul>\r\n<li>All magnitudes assume the simulation little h value from General Properties</li>\r\n<li>Magnitudes are calculated in the AB system</li>\r\n</ul>\r\n<p>Additional information is available from the <a href="../static/docs/user-manual/sed.html" target="_blank">SED Module documentation</a>.</p>'
    tao_stellarmodel_6.encoding = u'<single-stellar-population-model>bc03/ssp_kroupa.dat</single-stellar-population-model>\r\n<wavelengths-file>bc03/wavelengths.dat</wavelengths-file>\r\n<ages-file>bc03/ages.dat</ages-file>\r\n<metallicities-file>bc03/metallicities.dat</metallicities-file>\r\n'
    tao_stellarmodel_6 = save_or_locate(tao_stellarmodel_6)

    tao_stellarmodel_7 = StellarModel()
    tao_stellarmodel_7.name = u'bc03/ssp_salpeter.dat'
    tao_stellarmodel_7.label = u'Bruzual & Charlot (2003), Salpeter IMF'
    tao_stellarmodel_7.description = u'<p>External link: <a href="http://www2.iap.fr/users/charlot/bc2003/" target="_blank">GALAXEV</a></p>\r\n<ul>\r\n<li>All magnitudes assume the simulation little h value from General Properties</li>\r\n<li>Magnitudes are calculated in the AB system</li>\r\n</ul>\r\n<p>Additional information is available from the <a href="../static/docs/user-manual/sed.html" target="_blank">SED Module documentation</a>.</p>'
    tao_stellarmodel_7.encoding = u'<single-stellar-population-model>bc03/ssp_salpeter.dat</single-stellar-population-model>\r\n<wavelengths-file>bc03/wavelengths.dat</wavelengths-file>\r\n<ages-file>bc03/ages.dat</ages-file>\r\n<metallicities-file>bc03/metallicities.dat</metallicities-file>\r\n'
    tao_stellarmodel_7 = save_or_locate(tao_stellarmodel_7)

    tao_stellarmodel_8 = StellarModel()
    tao_stellarmodel_8.name = u'bc03/ssp_chabrier.dat'
    tao_stellarmodel_8.label = u'Bruzual & Charlot (2003), Chabrier IMF'
    tao_stellarmodel_8.description = u'<p>External link: <a href="http://www2.iap.fr/users/charlot/bc2003/" target="_blank">GALAXEV</a></p>\r\n<ul>\r\n<li>All magnitudes assume the simulation little h value from General Properties</li>\r\n<li>Magnitudes are calculated in the AB system</li>\r\n</ul>\r\n<p>Additional information is available from the <a href="../static/docs/user-manual/sed.html" target="_blank">SED Module documentation</a>.</p>'
    tao_stellarmodel_8.encoding = u'<single-stellar-population-model>bc03/ssp_kroupa.dat</single-stellar-population-model>\r\n<wavelengths-file>bc03/wavelengths.dat</wavelengths-file>\r\n<ages-file>bc03/ages.dat</ages-file>\r\n<metallicities-file>bc03/metallicities.dat</metallicities-file>\r\n'
    tao_stellarmodel_8 = save_or_locate(tao_stellarmodel_8)

    #Processing model: BandPassFilter

    from tao.models import BandPassFilter

    tao_bandpassfilter_1 = BandPassFilter()
    tao_bandpassfilter_1.label = u"CFHTLS Megacam g'"
    tao_bandpassfilter_1.filter_id = u'CFHTLS/gMega.dati'
    tao_bandpassfilter_1.description = u'Canada France Hawaii Telescope (CFHTLS/Megacam), g\' band\n<p>Additional Details: <a href="../static/docs/bpfilters/CFHTLS_gMega.dati.html">CFHTLS Megacam g\'</a>.</p>'
    tao_bandpassfilter_1.group = u''
    tao_bandpassfilter_1.order = 0L
    tao_bandpassfilter_1 = save_or_locate(tao_bandpassfilter_1)

    tao_bandpassfilter_2 = BandPassFilter()
    tao_bandpassfilter_2.label = u"CFHTLS Megacam i'"
    tao_bandpassfilter_2.filter_id = u'CFHTLS/i2Mega_new.dati'
    tao_bandpassfilter_2.description = u'Canada France Hawaii Telescope (CFHTLS/Megacam), i\' band\n<p>Additional Details: <a href="../static/docs/bpfilters/CFHTLS_i2Mega_new.dati.html">CFHTLS Megacam i\'</a>.</p>'
    tao_bandpassfilter_2.group = u''
    tao_bandpassfilter_2.order = 0L
    tao_bandpassfilter_2 = save_or_locate(tao_bandpassfilter_2)

    tao_bandpassfilter_3 = BandPassFilter()
    tao_bandpassfilter_3.label = u"CFHTLS Megacam r'"
    tao_bandpassfilter_3.filter_id = u'CFHTLS/rMega.dati'
    tao_bandpassfilter_3.description = u'Canada France Hawaii Telescope (CFHTLS/Megacam), r\' band\n<p>Additional Details: <a href="../static/docs/bpfilters/CFHTLS_rMega.dati.html">CFHTLS Megacam r\'</a>.</p>'
    tao_bandpassfilter_3.group = u''
    tao_bandpassfilter_3.order = 0L
    tao_bandpassfilter_3 = save_or_locate(tao_bandpassfilter_3)

    tao_bandpassfilter_4 = BandPassFilter()
    tao_bandpassfilter_4.label = u'CFHTLS Megacam u*'
    tao_bandpassfilter_4.filter_id = u'CFHTLS/uMega.dati'
    tao_bandpassfilter_4.description = u'Canada France Hawaii Telescope (CFHTLS/Megacam), u* band\n<p>Additional Details: <a href="../static/docs/bpfilters/CFHTLS_uMega.dati.html">CFHTLS Megacam u*</a>.</p>'
    tao_bandpassfilter_4.group = u''
    tao_bandpassfilter_4.order = 0L
    tao_bandpassfilter_4 = save_or_locate(tao_bandpassfilter_4)

    tao_bandpassfilter_5 = BandPassFilter()
    tao_bandpassfilter_5.label = u"CFHTLS Megacam z'"
    tao_bandpassfilter_5.filter_id = u'CFHTLS/zMega.dati'
    tao_bandpassfilter_5.description = u'Canada France Hawaii Telescope (CFHTLS/Megacam), z\' band\n<p>Additional Details: <a href="../static/docs/bpfilters/CFHTLS_zMega.dati.html">CFHTLS Megacam z\'</a>.</p>'
    tao_bandpassfilter_5.group = u''
    tao_bandpassfilter_5.order = 0L
    tao_bandpassfilter_5 = save_or_locate(tao_bandpassfilter_5)

    tao_bandpassfilter_6 = BandPassFilter()
    tao_bandpassfilter_6.label = u'GALEX FUV'
    tao_bandpassfilter_6.filter_id = u'GALEX/galex_FUV.dati'
    tao_bandpassfilter_6.description = u'Galaxy Evolution Explorer (GALEX), far-UV\n<p>Additional Details: <a href="../static/docs/bpfilters/GALEX_galex_FUV.dati.html">GALEX FUV</a>.</p>'
    tao_bandpassfilter_6.group = u''
    tao_bandpassfilter_6.order = 0L
    tao_bandpassfilter_6 = save_or_locate(tao_bandpassfilter_6)

    tao_bandpassfilter_7 = BandPassFilter()
    tao_bandpassfilter_7.label = u'GALEX NUV'
    tao_bandpassfilter_7.filter_id = u'GALEX/galex_NUV.dati'
    tao_bandpassfilter_7.description = u'Galaxy Evolution  Explorer (GALEX), near-UV\n<p>Additional Details: <a href="../static/docs/bpfilters/GALEX_galex_NUV.dati.html">GALEX NUV</a>.</p>'
    tao_bandpassfilter_7.group = u''
    tao_bandpassfilter_7.order = 0L
    tao_bandpassfilter_7 = save_or_locate(tao_bandpassfilter_7)

    tao_bandpassfilter_8 = BandPassFilter()
    tao_bandpassfilter_8.label = u'HST/ACS/WFC1 B'
    tao_bandpassfilter_8.filter_id = u'ACS/f435w.WFC1.dati'
    tao_bandpassfilter_8.description = u'Hubble Space Telescope Advanced Camera for Surveys, Wide Field Camera 1 (HST/ACS, WFC1), B band (F435W)\n<p>Additional Details: <a href="../static/docs/bpfilters/ACS_f435w.WFC1.dati.html">HST/ACS/WFC1 B</a>.</p>'
    tao_bandpassfilter_8.group = u''
    tao_bandpassfilter_8.order = 0L
    tao_bandpassfilter_8 = save_or_locate(tao_bandpassfilter_8)

    tao_bandpassfilter_9 = BandPassFilter()
    tao_bandpassfilter_9.label = u'HST/ACS/WFC1 i'
    tao_bandpassfilter_9.filter_id = u'ACS/f775w.WFC1.dati'
    tao_bandpassfilter_9.description = u'Hubble Space Telescope Advanced Camera for Surveys, Wide Field Camera 1 (HST/ACS, WFC1), i band (F775W)\n<p>Additional Details: <a href="../static/docs/bpfilters/ACS_f775w.WFC1.dati.html">HST/ACS/WFC1 i</a>.</p>'
    tao_bandpassfilter_9.group = u''
    tao_bandpassfilter_9.order = 0L
    tao_bandpassfilter_9 = save_or_locate(tao_bandpassfilter_9)

    tao_bandpassfilter_10 = BandPassFilter()
    tao_bandpassfilter_10.label = u'HST/ACS/WFC1 V'
    tao_bandpassfilter_10.filter_id = u'ACS/f606w.WFC1.dati'
    tao_bandpassfilter_10.description = u'Hubble Space Telescope Advanced Camera for Surveys, Wide Field Camera 1 (HST/ACS, WFC1), V band (F606W)\n<p>Additional Details: <a href="../static/docs/bpfilters/ACS_f606w.WFC1.dati.html">HST/ACS/WFC1 V</a>.</p>'
    tao_bandpassfilter_10.group = u''
    tao_bandpassfilter_10.order = 0L
    tao_bandpassfilter_10 = save_or_locate(tao_bandpassfilter_10)

    tao_bandpassfilter_11 = BandPassFilter()
    tao_bandpassfilter_11.label = u'HST/ACS/WFC1 z'
    tao_bandpassfilter_11.filter_id = u'ACS/f850lp.WFC1.dati'
    tao_bandpassfilter_11.description = u'Hubble Space Telescope Advanced Camera for Surveys, Wide Field Camera 1 (HST/ACS, WFC1), z band (F850LP)\n<p>Additional Details: <a href="../static/docs/bpfilters/ACS_f850lp.WFC1.dati.html">HST/ACS/WFC1 z</a>.</p>'
    tao_bandpassfilter_11.group = u''
    tao_bandpassfilter_11.order = 0L
    tao_bandpassfilter_11 = save_or_locate(tao_bandpassfilter_11)

    tao_bandpassfilter_12 = BandPassFilter()
    tao_bandpassfilter_12.label = u'HST/ACS/WFC2 B'
    tao_bandpassfilter_12.filter_id = u'ACS/f435w.WFC2.dati'
    tao_bandpassfilter_12.description = u'Hubble Space Telescope Advanced Camera for Surveys, Wide Field Camera 2 (HST/ACS, WFC2), B band (F435W)\n<p>Additional Details: <a href="../static/docs/bpfilters/ACS_f435w.WFC2.dati.html">HST/ACS/WFC2 B</a>.</p>'
    tao_bandpassfilter_12.group = u''
    tao_bandpassfilter_12.order = 0L
    tao_bandpassfilter_12 = save_or_locate(tao_bandpassfilter_12)

    tao_bandpassfilter_13 = BandPassFilter()
    tao_bandpassfilter_13.label = u'HST/ACS/WFC2 i'
    tao_bandpassfilter_13.filter_id = u'ACS/f775w.WFC2.dati'
    tao_bandpassfilter_13.description = u'Hubble Space Telescope Advanced Camera for Surveys, Wide Field Camera 2 (HST/ACS, WFC2), i band (F775W)\n<p>Additional Details: <a href="../static/docs/bpfilters/ACS_f775w.WFC2.dati.html">HST/ACS/WFC2 i</a>.</p>'
    tao_bandpassfilter_13.group = u''
    tao_bandpassfilter_13.order = 0L
    tao_bandpassfilter_13 = save_or_locate(tao_bandpassfilter_13)

    tao_bandpassfilter_14 = BandPassFilter()
    tao_bandpassfilter_14.label = u'HST/ACS/WFC2 V'
    tao_bandpassfilter_14.filter_id = u'ACS/f606w.WFC2.dati'
    tao_bandpassfilter_14.description = u'Hubble Space Telescope Advanced Camera for Surveys, Wide Field Camera 2 (HST/ACS, WFC2), V band (F606W)\n<p>Additional Details: <a href="../static/docs/bpfilters/ACS_f606w.WFC2.dati.html">HST/ACS/WFC2 V</a>.</p>'
    tao_bandpassfilter_14.group = u''
    tao_bandpassfilter_14.order = 0L
    tao_bandpassfilter_14 = save_or_locate(tao_bandpassfilter_14)

    tao_bandpassfilter_15 = BandPassFilter()
    tao_bandpassfilter_15.label = u'HST/ACS/WFC2 z'
    tao_bandpassfilter_15.filter_id = u'ACS/f850lp.WFC2.dati'
    tao_bandpassfilter_15.description = u'Hubble Space Telescope Advanced Camera for Surveys, Wide Field Camera 2 (HST/ACS, WFC2), z band (F850LP)\n<p>Additional Details: <a href="../static/docs/bpfilters/ACS_f850lp.WFC2.dati.html">HST/ACS/WFC2 z</a>.</p>'
    tao_bandpassfilter_15.group = u''
    tao_bandpassfilter_15.order = 0L
    tao_bandpassfilter_15 = save_or_locate(tao_bandpassfilter_15)

    tao_bandpassfilter_16 = BandPassFilter()
    tao_bandpassfilter_16.label = u'HST/Herschel/PACS 100'
    tao_bandpassfilter_16.filter_id = u'PACS/pacs100.dati'
    tao_bandpassfilter_16.description = u'Hubble Space Telescope, Herschel/PACS, 100 micron\n<p>Additional Details: <a href="../static/docs/bpfilters/PACS_pacs100.dati.html">HST/Herschel/PACS 100</a>.</p>'
    tao_bandpassfilter_16.group = u''
    tao_bandpassfilter_16.order = 0L
    tao_bandpassfilter_16 = save_or_locate(tao_bandpassfilter_16)

    tao_bandpassfilter_17 = BandPassFilter()
    tao_bandpassfilter_17.label = u'HST/Herschel/PACS 160'
    tao_bandpassfilter_17.filter_id = u'PACS/pacs160.dati'
    tao_bandpassfilter_17.description = u'Hubble Space Telescope, Herschel/PACS, 160 micron\n<p>Additional Details: <a href="../static/docs/bpfilters/PACS_pacs160.dati.html">HST/Herschel/PACS 160</a>.</p>'
    tao_bandpassfilter_17.group = u''
    tao_bandpassfilter_17.order = 0L
    tao_bandpassfilter_17 = save_or_locate(tao_bandpassfilter_17)

    tao_bandpassfilter_18 = BandPassFilter()
    tao_bandpassfilter_18.label = u'HST/Herschel/PACS 70'
    tao_bandpassfilter_18.filter_id = u'PACS/pacs70.dati'
    tao_bandpassfilter_18.description = u'Hubble Space Telescope, Herschel/PACS, 70 micron\n<p>Additional Details: <a href="../static/docs/bpfilters/PACS_pacs70.dati.html">HST/Herschel/PACS 70</a>.</p>'
    tao_bandpassfilter_18.group = u''
    tao_bandpassfilter_18.order = 0L
    tao_bandpassfilter_18 = save_or_locate(tao_bandpassfilter_18)

    tao_bandpassfilter_19 = BandPassFilter()
    tao_bandpassfilter_19.label = u'HST/Herschel/SPIRE 250'
    tao_bandpassfilter_19.filter_id = u'SPIRE/spire250.dati'
    tao_bandpassfilter_19.description = u'Hubble Space Telescope, Herschel/SPIRE, 250 micron\n<p>Additional Details: <a href="../static/docs/bpfilters/SPIRE_spire250.dati.html">HST/Herschel/SPIRE 250</a>.</p>'
    tao_bandpassfilter_19.group = u''
    tao_bandpassfilter_19.order = 0L
    tao_bandpassfilter_19 = save_or_locate(tao_bandpassfilter_19)

    tao_bandpassfilter_20 = BandPassFilter()
    tao_bandpassfilter_20.label = u'HST/Herschel/SPIRE 350'
    tao_bandpassfilter_20.filter_id = u'SPIRE/spire350.dati'
    tao_bandpassfilter_20.description = u'Hubble Space Telescope, Herschel/SPIRE, 350 micron\n<p>Additional Details: <a href="../static/docs/bpfilters/SPIRE_spire350.dati.html">HST/Herschel/SPIRE 350</a>.</p>'
    tao_bandpassfilter_20.group = u''
    tao_bandpassfilter_20.order = 0L
    tao_bandpassfilter_20 = save_or_locate(tao_bandpassfilter_20)

    tao_bandpassfilter_21 = BandPassFilter()
    tao_bandpassfilter_21.label = u'HST/Herschel/SPIRE 500'
    tao_bandpassfilter_21.filter_id = u'SPIRE/spire500.dati'
    tao_bandpassfilter_21.description = u'Hubble Space Telescope, Herschel/SPIRE, 500 micron\n<p>Additional Details: <a href="../static/docs/bpfilters/SPIRE_spire500.dati.html">HST/Herschel/SPIRE 500</a>.</p>'
    tao_bandpassfilter_21.group = u''
    tao_bandpassfilter_21.order = 0L
    tao_bandpassfilter_21 = save_or_locate(tao_bandpassfilter_21)

    tao_bandpassfilter_22 = BandPassFilter()
    tao_bandpassfilter_22.label = u'HST/Spitzer IRAC1'
    tao_bandpassfilter_22.filter_id = u'IRAC/irac_3.4.dati'
    tao_bandpassfilter_22.description = u'Hubble Space Telescope, Spitzer/IRAC, ch1 (3.4 micron)\n<p>Additional Details: <a href="../static/docs/bpfilters/IRAC_irac_3.4.dati.html">HST/Spitzer IRAC1</a>.</p>'
    tao_bandpassfilter_22.group = u''
    tao_bandpassfilter_22.order = 0L
    tao_bandpassfilter_22 = save_or_locate(tao_bandpassfilter_22)

    tao_bandpassfilter_23 = BandPassFilter()
    tao_bandpassfilter_23.label = u'HST/Spitzer IRAC2'
    tao_bandpassfilter_23.filter_id = u'IRAC/irac_4.5.dati'
    tao_bandpassfilter_23.description = u'Hubble Space Telescope, Spitzer/IRAC, ch2 (4.5 micron)\n<p>Additional Details: <a href="../static/docs/bpfilters/IRAC_irac_4.5.dati.html">HST/Spitzer IRAC2</a>.</p>'
    tao_bandpassfilter_23.group = u''
    tao_bandpassfilter_23.order = 0L
    tao_bandpassfilter_23 = save_or_locate(tao_bandpassfilter_23)

    tao_bandpassfilter_24 = BandPassFilter()
    tao_bandpassfilter_24.label = u'HST/Spitzer IRAC3'
    tao_bandpassfilter_24.filter_id = u'IRAC/irac_5.8.dati'
    tao_bandpassfilter_24.description = u'Hubble Space Telescope, Spitzer/IRAC, ch3 (5.8 micron)\n<p>Additional Details: <a href="../static/docs/bpfilters/IRAC_irac_5.8.dati.html">HST/Spitzer IRAC3</a>.</p>'
    tao_bandpassfilter_24.group = u''
    tao_bandpassfilter_24.order = 0L
    tao_bandpassfilter_24 = save_or_locate(tao_bandpassfilter_24)

    tao_bandpassfilter_25 = BandPassFilter()
    tao_bandpassfilter_25.label = u'HST/Spitzer IRAC4'
    tao_bandpassfilter_25.filter_id = u'IRAC/irac_8.0.dati'
    tao_bandpassfilter_25.description = u'Hubble Space Telescope, Spitzer/IRAC, ch4 (8.0 micron)\n<p>Additional Details: <a href="../static/docs/bpfilters/IRAC_irac_8.0.dati.html">HST/Spitzer IRAC4</a>.</p>'
    tao_bandpassfilter_25.group = u''
    tao_bandpassfilter_25.order = 0L
    tao_bandpassfilter_25 = save_or_locate(tao_bandpassfilter_25)

    tao_bandpassfilter_26 = BandPassFilter()
    tao_bandpassfilter_26.label = u'HST/Spitzer/MIPS 24'
    tao_bandpassfilter_26.filter_id = u'MIPS/mips_24.dati'
    tao_bandpassfilter_26.description = u'Hubble Space Telescope, Spitzer/MIPS, 24 micron\n<p>Additional Details: <a href="../static/docs/bpfilters/MIPS_mips_24.dati.html">HST/Spitzer/MIPS 24</a>.</p>'
    tao_bandpassfilter_26.group = u''
    tao_bandpassfilter_26.order = 0L
    tao_bandpassfilter_26 = save_or_locate(tao_bandpassfilter_26)

    tao_bandpassfilter_27 = BandPassFilter()
    tao_bandpassfilter_27.label = u'HST/WFC3/IR F0.98M'
    tao_bandpassfilter_27.filter_id = u'WFC3/f098m.IR.dati'
    tao_bandpassfilter_27.description = u'Hubble Space Telescope, WFC3/IR, F0.98M\n<p>Additional Details: <a href="../static/docs/bpfilters/WFC3_f098m.IR.dati.html">HST/WFC3/IR F0.98M</a>.</p>'
    tao_bandpassfilter_27.group = u''
    tao_bandpassfilter_27.order = 0L
    tao_bandpassfilter_27 = save_or_locate(tao_bandpassfilter_27)

    tao_bandpassfilter_28 = BandPassFilter()
    tao_bandpassfilter_28.label = u'HST/WFC3/IR F105W'
    tao_bandpassfilter_28.filter_id = u'WFC3/f105w.IR.dati'
    tao_bandpassfilter_28.description = u'Hubble Space Telescope, WFC3/IR, F105W\n<p>Additional Details: <a href="../static/docs/bpfilters/WFC3_f105w.IR.dati.html">HST/WFC3/IR F105W</a>.</p>'
    tao_bandpassfilter_28.group = u''
    tao_bandpassfilter_28.order = 0L
    tao_bandpassfilter_28 = save_or_locate(tao_bandpassfilter_28)

    tao_bandpassfilter_29 = BandPassFilter()
    tao_bandpassfilter_29.label = u'HST/WFC3/IR F125W'
    tao_bandpassfilter_29.filter_id = u'WFC3/f125w.IR.dati'
    tao_bandpassfilter_29.description = u'Hubble Space Telescope, WFC3/IR, F125W\n<p>Additional Details: <a href="../static/docs/bpfilters/WFC3_f125w.IR.dati.html">HST/WFC3/IR F125W</a>.</p>'
    tao_bandpassfilter_29.group = u''
    tao_bandpassfilter_29.order = 0L
    tao_bandpassfilter_29 = save_or_locate(tao_bandpassfilter_29)

    tao_bandpassfilter_30 = BandPassFilter()
    tao_bandpassfilter_30.label = u'HST/WFC3/IR F160W'
    tao_bandpassfilter_30.filter_id = u'WFC3/f160w.IR.dati'
    tao_bandpassfilter_30.description = u'Hubble Space Telescope, WFC3/IR, F160W\n<p>Additional Details: <a href="../static/docs/bpfilters/WFC3_f160w.IR.dati.html">HST/WFC3/IR F160W</a>.</p>'
    tao_bandpassfilter_30.group = u''
    tao_bandpassfilter_30.order = 0L
    tao_bandpassfilter_30 = save_or_locate(tao_bandpassfilter_30)

    tao_bandpassfilter_31 = BandPassFilter()
    tao_bandpassfilter_31.label = u'HST/WFC3/IR/UVIS1 F265W'
    tao_bandpassfilter_31.filter_id = u'WFC3/f275w.UVIS1.dati'
    tao_bandpassfilter_31.description = u'Hubble Space Telescope, WFC3/IR/UVIS1, F275W\n<p>Additional Details: <a href="../static/docs/bpfilters/WFC3_f275w.UVIS1.dati.html">HST/WFC3/IR/UVIS1 F265W</a>.</p>'
    tao_bandpassfilter_31.group = u''
    tao_bandpassfilter_31.order = 0L
    tao_bandpassfilter_31 = save_or_locate(tao_bandpassfilter_31)

    tao_bandpassfilter_32 = BandPassFilter()
    tao_bandpassfilter_32.label = u'HST/WFC3/IR/UVIS1 F336W'
    tao_bandpassfilter_32.filter_id = u'WFC3/f336w.UVIS1.dati'
    tao_bandpassfilter_32.description = u'Hubble Space Telescope, WFC3/IR/UVIS1, F336W\n<p>Additional Details: <a href="../static/docs/bpfilters/WFC3_f336w.UVIS1.dati.html">HST/WFC3/IR/UVIS1 F336W</a>.</p>'
    tao_bandpassfilter_32.group = u''
    tao_bandpassfilter_32.order = 0L
    tao_bandpassfilter_32 = save_or_locate(tao_bandpassfilter_32)

    tao_bandpassfilter_33 = BandPassFilter()
    tao_bandpassfilter_33.label = u'HST/WFC3/IR/UVIS2 F265W'
    tao_bandpassfilter_33.filter_id = u'WFC3/f275w.UVIS2.dati'
    tao_bandpassfilter_33.description = u'Hubble Space Telescope, WFC3/IR/UVIS2, F275W\n<p>Additional Details: <a href="../static/docs/bpfilters/WFC3_f275w.UVIS2.dati.html">HST/WFC3/IR/UVIS2 F265W</a>.</p>'
    tao_bandpassfilter_33.group = u''
    tao_bandpassfilter_33.order = 0L
    tao_bandpassfilter_33 = save_or_locate(tao_bandpassfilter_33)

    tao_bandpassfilter_34 = BandPassFilter()
    tao_bandpassfilter_34.label = u'HST/WFC3/IR/UVIS2 F336W'
    tao_bandpassfilter_34.filter_id = u'WFC3/f336w.UVIS2.dati'
    tao_bandpassfilter_34.description = u'Hubble Space Telescope, WFC3/IR/UVIS2, F336W\n<p>Additional Details: <a href="../static/docs/bpfilters/WFC3_f336w.UVIS2.dati.html">HST/WFC3/IR/UVIS2 F336W</a>.</p>'
    tao_bandpassfilter_34.group = u''
    tao_bandpassfilter_34.order = 0L
    tao_bandpassfilter_34 = save_or_locate(tao_bandpassfilter_34)

    tao_bandpassfilter_35 = BandPassFilter()
    tao_bandpassfilter_35.label = u'Johnson B'
    tao_bandpassfilter_35.filter_id = u'Johnson/Johnson_B.dati'
    tao_bandpassfilter_35.description = u'Johnson B band\n<p>Additional Details: <a href="../static/docs/bpfilters/Johnson_Johnson_B.dati.html">Johnson B</a>.</p>'
    tao_bandpassfilter_35.group = u''
    tao_bandpassfilter_35.order = 0L
    tao_bandpassfilter_35 = save_or_locate(tao_bandpassfilter_35)

    tao_bandpassfilter_36 = BandPassFilter()
    tao_bandpassfilter_36.label = u'Johnson H'
    tao_bandpassfilter_36.filter_id = u'Johnson/h.dat'
    tao_bandpassfilter_36.description = u'Johnson H band\n<p>Additional Details: <a href="../static/docs/bpfilters/Johnson_h.dat.html">Johnson H</a>.</p>'
    tao_bandpassfilter_36.group = u''
    tao_bandpassfilter_36.order = 0L
    tao_bandpassfilter_36 = save_or_locate(tao_bandpassfilter_36)

    tao_bandpassfilter_37 = BandPassFilter()
    tao_bandpassfilter_37.label = u'Johnson I'
    tao_bandpassfilter_37.filter_id = u'Johnson/Ifilter.dati'
    tao_bandpassfilter_37.description = u'Johnson I band\n<p>Additional Details: <a href="../static/docs/bpfilters/Johnson_Ifilter.dati.html">Johnson I</a>.</p>'
    tao_bandpassfilter_37.group = u''
    tao_bandpassfilter_37.order = 0L
    tao_bandpassfilter_37 = save_or_locate(tao_bandpassfilter_37)

    tao_bandpassfilter_38 = BandPassFilter()
    tao_bandpassfilter_38.label = u'Johnson J'
    tao_bandpassfilter_38.filter_id = u'Johnson/j.dat'
    tao_bandpassfilter_38.description = u'Johnson J band\n<p>Additional Details: <a href="../static/docs/bpfilters/Johnson_j.dat.html">Johnson J</a>.</p>'
    tao_bandpassfilter_38.group = u''
    tao_bandpassfilter_38.order = 0L
    tao_bandpassfilter_38 = save_or_locate(tao_bandpassfilter_38)

    tao_bandpassfilter_39 = BandPassFilter()
    tao_bandpassfilter_39.label = u'Johnson K'
    tao_bandpassfilter_39.filter_id = u'Johnson/k.dat'
    tao_bandpassfilter_39.description = u'Johnson K band\n<p>Additional Details: <a href="../static/docs/bpfilters/Johnson_k.dat.html">Johnson K</a>.</p>'
    tao_bandpassfilter_39.group = u''
    tao_bandpassfilter_39.order = 0L
    tao_bandpassfilter_39 = save_or_locate(tao_bandpassfilter_39)

    tao_bandpassfilter_40 = BandPassFilter()
    tao_bandpassfilter_40.label = u'Johnson R'
    tao_bandpassfilter_40.filter_id = u'Johnson/Rfilter.dati'
    tao_bandpassfilter_40.description = u'Johnson R band\n<p>Additional Details: <a href="../static/docs/bpfilters/Johnson_Rfilter.dati.html">Johnson R</a>.</p>'
    tao_bandpassfilter_40.group = u''
    tao_bandpassfilter_40.order = 0L
    tao_bandpassfilter_40 = save_or_locate(tao_bandpassfilter_40)

    tao_bandpassfilter_41 = BandPassFilter()
    tao_bandpassfilter_41.label = u'Johnson U'
    tao_bandpassfilter_41.filter_id = u'Johnson/Johnson_U.dati'
    tao_bandpassfilter_41.description = u'Johnson U band\n<p>Additional Details: <a href="../static/docs/bpfilters/Johnson_Johnson_U.dati.html">Johnson U</a>.</p>'
    tao_bandpassfilter_41.group = u''
    tao_bandpassfilter_41.order = 0L
    tao_bandpassfilter_41 = save_or_locate(tao_bandpassfilter_41)

    tao_bandpassfilter_42 = BandPassFilter()
    tao_bandpassfilter_42.label = u'Johnson V'
    tao_bandpassfilter_42.filter_id = u'Johnson/Johnson_V.dati'
    tao_bandpassfilter_42.description = u'Johnson V band\n<p>Additional Details: <a href="../static/docs/bpfilters/Johnson_Johnson_V.dati.html">Johnson V</a>.</p>'
    tao_bandpassfilter_42.group = u''
    tao_bandpassfilter_42.order = 0L
    tao_bandpassfilter_42 = save_or_locate(tao_bandpassfilter_42)

    tao_bandpassfilter_43 = BandPassFilter()
    tao_bandpassfilter_43.label = u'Keck/DEIMOS/DEEP B'
    tao_bandpassfilter_43.filter_id = u'DEEP/deep_B.dati'
    tao_bandpassfilter_43.description = u'Keck/DEIMOS/DEEP, B band\n<p>Additional Details: <a href="../static/docs/bpfilters/DEEP_deep_B.dati.html">Keck/DEIMOS/DEEP B</a>.</p>'
    tao_bandpassfilter_43.group = u''
    tao_bandpassfilter_43.order = 0L
    tao_bandpassfilter_43 = save_or_locate(tao_bandpassfilter_43)

    tao_bandpassfilter_44 = BandPassFilter()
    tao_bandpassfilter_44.label = u'Keck/DEIMOS/DEEP I'
    tao_bandpassfilter_44.filter_id = u'DEEP/deep_I.dati'
    tao_bandpassfilter_44.description = u'Keck/DEIMOS/DEEP, I band\n<p>Additional Details: <a href="../static/docs/bpfilters/DEEP_deep_I.dati.html">Keck/DEIMOS/DEEP I</a>.</p>'
    tao_bandpassfilter_44.group = u''
    tao_bandpassfilter_44.order = 0L
    tao_bandpassfilter_44 = save_or_locate(tao_bandpassfilter_44)

    tao_bandpassfilter_45 = BandPassFilter()
    tao_bandpassfilter_45.label = u'Keck/DEIMOS/DEEP R'
    tao_bandpassfilter_45.filter_id = u'DEEP/deep_R.dati'
    tao_bandpassfilter_45.description = u'Keck/DEIMOS/DEEP, R band\n<p>Additional Details: <a href="../static/docs/bpfilters/DEEP_deep_R.dati.html">Keck/DEIMOS/DEEP R</a>.</p>'
    tao_bandpassfilter_45.group = u''
    tao_bandpassfilter_45.order = 0L
    tao_bandpassfilter_45 = save_or_locate(tao_bandpassfilter_45)

    tao_bandpassfilter_46 = BandPassFilter()
    tao_bandpassfilter_46.label = u'LBC USPEC'
    tao_bandpassfilter_46.filter_id = u'LBC/LBCBLUE_USPEC_airm12.dati'
    tao_bandpassfilter_46.description = u'Large Binocular Camera, USPEC\n<p>Additional Details: <a href="../static/docs/bpfilters/LBC_LBCBLUE_USPEC_airm12.dati.html">LBC USPEC</a>.</p>'
    tao_bandpassfilter_46.group = u''
    tao_bandpassfilter_46.order = 0L
    tao_bandpassfilter_46 = save_or_locate(tao_bandpassfilter_46)

    tao_bandpassfilter_47 = BandPassFilter()
    tao_bandpassfilter_47.label = u'Mosaic U'
    tao_bandpassfilter_47.filter_id = u'MOSAIC/U_ctio_mosaic_tot.dati'
    tao_bandpassfilter_47.description = u'Cerro Tololo Inter-American Observatory (CTIO) Mosaic II, U band\n<p>Additional Details: <a href="../static/docs/bpfilters/MOSAIC_U_ctio_mosaic_tot.dati.html">Mosaic U</a>.</p>'
    tao_bandpassfilter_47.group = u''
    tao_bandpassfilter_47.order = 0L
    tao_bandpassfilter_47 = save_or_locate(tao_bandpassfilter_47)

    tao_bandpassfilter_48 = BandPassFilter()
    tao_bandpassfilter_48.label = u'MUSYC/ECDFS B'
    tao_bandpassfilter_48.filter_id = u'MUSYC/ecdfs.B.filt.dati'
    tao_bandpassfilter_48.description = u'MUSYC survey, Extended Chandra Deep Field South, B band\n<p>Additional Details: <a href="../static/docs/bpfilters/MUSYC_ecdfs.B.filt.dati.html">MUSYC/ECDFS B</a>.</p>'
    tao_bandpassfilter_48.group = u''
    tao_bandpassfilter_48.order = 0L
    tao_bandpassfilter_48 = save_or_locate(tao_bandpassfilter_48)

    tao_bandpassfilter_49 = BandPassFilter()
    tao_bandpassfilter_49.label = u'MUSYC/ECDFS H'
    tao_bandpassfilter_49.filter_id = u'MUSYC/ecdfs.H.filt.dati'
    tao_bandpassfilter_49.description = u'MUSYC survey, Extended Chandra Deep Field South, H band\n<p>Additional Details: <a href="../static/docs/bpfilters/MUSYC_ecdfs.H.filt.dati.html">MUSYC/ECDFS H</a>.</p>'
    tao_bandpassfilter_49.group = u''
    tao_bandpassfilter_49.order = 0L
    tao_bandpassfilter_49 = save_or_locate(tao_bandpassfilter_49)

    tao_bandpassfilter_50 = BandPassFilter()
    tao_bandpassfilter_50.label = u'MUSYC/ECDFS I'
    tao_bandpassfilter_50.filter_id = u'MUSYC/ecdfs.I.filt.dati'
    tao_bandpassfilter_50.description = u'MUSYC survey, Extended Chandra Deep Field South, I band\n<p>Additional Details: <a href="../static/docs/bpfilters/MUSYC_ecdfs.I.filt.dati.html">MUSYC/ECDFS I</a>.</p>'
    tao_bandpassfilter_50.group = u''
    tao_bandpassfilter_50.order = 0L
    tao_bandpassfilter_50 = save_or_locate(tao_bandpassfilter_50)

    tao_bandpassfilter_51 = BandPassFilter()
    tao_bandpassfilter_51.label = u'MUSYC/ECDFS J'
    tao_bandpassfilter_51.filter_id = u'MUSYC/ecdfs.J.filt.dati'
    tao_bandpassfilter_51.description = u'MUSYC survey, Extended Chandra Deep Field South, J band\n<p>Additional Details: <a href="../static/docs/bpfilters/MUSYC_ecdfs.J.filt.dati.html">MUSYC/ECDFS J</a>.</p>'
    tao_bandpassfilter_51.group = u''
    tao_bandpassfilter_51.order = 0L
    tao_bandpassfilter_51 = save_or_locate(tao_bandpassfilter_51)

    tao_bandpassfilter_52 = BandPassFilter()
    tao_bandpassfilter_52.label = u'MUSYC/ECDFS K'
    tao_bandpassfilter_52.filter_id = u'MUSYC/ecdfs.K.filt.dati'
    tao_bandpassfilter_52.description = u'MUSYC survey, Extended Chandra Deep Field South, K band\n<p>Additional Details: <a href="../static/docs/bpfilters/MUSYC_ecdfs.K.filt.dati.html">MUSYC/ECDFS K</a>.</p>'
    tao_bandpassfilter_52.group = u''
    tao_bandpassfilter_52.order = 0L
    tao_bandpassfilter_52 = save_or_locate(tao_bandpassfilter_52)

    tao_bandpassfilter_53 = BandPassFilter()
    tao_bandpassfilter_53.label = u'MUSYC/ECDFS R'
    tao_bandpassfilter_53.filter_id = u'MUSYC/ecdfs.R.filt.dati'
    tao_bandpassfilter_53.description = u'MUSYC survey, Extended Chandra Deep Field South, R band\n<p>Additional Details: <a href="../static/docs/bpfilters/MUSYC_ecdfs.R.filt.dati.html">MUSYC/ECDFS R</a>.</p>'
    tao_bandpassfilter_53.group = u''
    tao_bandpassfilter_53.order = 0L
    tao_bandpassfilter_53 = save_or_locate(tao_bandpassfilter_53)

    tao_bandpassfilter_54 = BandPassFilter()
    tao_bandpassfilter_54.label = u'MUSYC/ECDFS U'
    tao_bandpassfilter_54.filter_id = u'MUSYC/ecdfs.U.filt.dati'
    tao_bandpassfilter_54.description = u'MUSYC survey, Extended Chandra Deep Field South, U band\n<p>Additional Details: <a href="../static/docs/bpfilters/MUSYC_ecdfs.U.filt.dati.html">MUSYC/ECDFS U</a>.</p>'
    tao_bandpassfilter_54.group = u''
    tao_bandpassfilter_54.order = 0L
    tao_bandpassfilter_54 = save_or_locate(tao_bandpassfilter_54)

    tao_bandpassfilter_55 = BandPassFilter()
    tao_bandpassfilter_55.label = u'MUSYC/ECDFS V'
    tao_bandpassfilter_55.filter_id = u'MUSYC/ecdfs.V.filt.dati'
    tao_bandpassfilter_55.description = u'MUSYC survey, Extended Chandra Deep Field South, V band\n<p>Additional Details: <a href="../static/docs/bpfilters/MUSYC_ecdfs.V.filt.dati.html">MUSYC/ECDFS V</a>.</p>'
    tao_bandpassfilter_55.group = u''
    tao_bandpassfilter_55.order = 0L
    tao_bandpassfilter_55 = save_or_locate(tao_bandpassfilter_55)

    tao_bandpassfilter_56 = BandPassFilter()
    tao_bandpassfilter_56.label = u'MUSYC/ECDFS z'
    tao_bandpassfilter_56.filter_id = u'MUSYC/ecdfs.z.filt.dati'
    tao_bandpassfilter_56.description = u'MUSYC survey, Extended Chandra Deep Field South, z band\n<p>Additional Details: <a href="../static/docs/bpfilters/MUSYC_ecdfs.z.filt.dati.html">MUSYC/ECDFS z</a>.</p>'
    tao_bandpassfilter_56.group = u''
    tao_bandpassfilter_56.order = 0L
    tao_bandpassfilter_56 = save_or_locate(tao_bandpassfilter_56)

    tao_bandpassfilter_57 = BandPassFilter()
    tao_bandpassfilter_57.label = u'NEWFIRM H'
    tao_bandpassfilter_57.filter_id = u'NEWFIRM/newfirmH.dati'
    tao_bandpassfilter_57.description = u'NOAO Extremely Wide-Field Infrared Imager (NEWFIRM), H band\n<p>Additional Details: <a href="../static/docs/bpfilters/NEWFIRM_newfirmH.dati.html">NEWFIRM H</a>.</p>'
    tao_bandpassfilter_57.group = u''
    tao_bandpassfilter_57.order = 0L
    tao_bandpassfilter_57 = save_or_locate(tao_bandpassfilter_57)

    tao_bandpassfilter_58 = BandPassFilter()
    tao_bandpassfilter_58.label = u'NEWFIRM J'
    tao_bandpassfilter_58.filter_id = u'NEWFIRM/newfirmJ.dati'
    tao_bandpassfilter_58.description = u'NOAO Extremely Wide-Field Infrared Imager (NEWFIRM), J band\n<p>Additional Details: <a href="../static/docs/bpfilters/NEWFIRM_newfirmJ.dati.html">NEWFIRM J</a>.</p>'
    tao_bandpassfilter_58.group = u''
    tao_bandpassfilter_58.order = 0L
    tao_bandpassfilter_58 = save_or_locate(tao_bandpassfilter_58)

    tao_bandpassfilter_59 = BandPassFilter()
    tao_bandpassfilter_59.label = u'NEWFIRM K'
    tao_bandpassfilter_59.filter_id = u'NEWFIRM/newfirmK.dati'
    tao_bandpassfilter_59.description = u'NOAO Extremely Wide-Field Infrared Imager (NEWFIRM), K band\n<p>Additional Details: <a href="../static/docs/bpfilters/NEWFIRM_newfirmK.dati.html">NEWFIRM K</a>.</p>'
    tao_bandpassfilter_59.group = u''
    tao_bandpassfilter_59.order = 0L
    tao_bandpassfilter_59 = save_or_locate(tao_bandpassfilter_59)

    tao_bandpassfilter_60 = BandPassFilter()
    tao_bandpassfilter_60.label = u'SCUBA 850'
    tao_bandpassfilter_60.filter_id = u'SCUBA/SCUBA_850.dati'
    tao_bandpassfilter_60.description = u'SCUBA 850 micron\n<p>Additional Details: <a href="../static/docs/bpfilters/SCUBA_SCUBA_850.dati.html">SCUBA 850</a>.</p>'
    tao_bandpassfilter_60.group = u''
    tao_bandpassfilter_60.order = 0L
    tao_bandpassfilter_60 = save_or_locate(tao_bandpassfilter_60)

    tao_bandpassfilter_61 = BandPassFilter()
    tao_bandpassfilter_61.label = u'SDSS g'
    tao_bandpassfilter_61.filter_id = u'SDSS/sdss_g.dati'
    tao_bandpassfilter_61.description = u'Sloan Digital Sky Survey (SDSS) g\n<p>Additional Details: <a href="../static/docs/bpfilters/SDSS_sdss_g.dati.html">SDSS g</a>.</p>'
    tao_bandpassfilter_61.group = u''
    tao_bandpassfilter_61.order = 0L
    tao_bandpassfilter_61 = save_or_locate(tao_bandpassfilter_61)

    tao_bandpassfilter_62 = BandPassFilter()
    tao_bandpassfilter_62.label = u'SDSS i'
    tao_bandpassfilter_62.filter_id = u'SDSS/sdss_i.dati'
    tao_bandpassfilter_62.description = u'Sloan Digital Sky Survey (SDSS) i\n<p>Additional Details: <a href="../static/docs/bpfilters/SDSS_sdss_i.dati.html">SDSS i</a>.</p>'
    tao_bandpassfilter_62.group = u''
    tao_bandpassfilter_62.order = 0L
    tao_bandpassfilter_62 = save_or_locate(tao_bandpassfilter_62)

    tao_bandpassfilter_63 = BandPassFilter()
    tao_bandpassfilter_63.label = u'SDSS r'
    tao_bandpassfilter_63.filter_id = u'SDSS/sdss_r.dati'
    tao_bandpassfilter_63.description = u'Sloan Digital Sky Survey (SDSS) r\n<p>Additional Details: <a href="../static/docs/bpfilters/SDSS_sdss_r.dati.html">SDSS r</a>.</p>'
    tao_bandpassfilter_63.group = u''
    tao_bandpassfilter_63.order = 0L
    tao_bandpassfilter_63 = save_or_locate(tao_bandpassfilter_63)

    tao_bandpassfilter_64 = BandPassFilter()
    tao_bandpassfilter_64.label = u'SDSS u'
    tao_bandpassfilter_64.filter_id = u'SDSS/sdss_u.dati'
    tao_bandpassfilter_64.description = u'Sloan Digital Sky Survey (SDSS) u\n<p>Additional Details: <a href="../static/docs/bpfilters/SDSS_sdss_u.dati.html">SDSS u</a>.</p>'
    tao_bandpassfilter_64.group = u''
    tao_bandpassfilter_64.order = 0L
    tao_bandpassfilter_64 = save_or_locate(tao_bandpassfilter_64)

    tao_bandpassfilter_65 = BandPassFilter()
    tao_bandpassfilter_65.label = u'SDSS z'
    tao_bandpassfilter_65.filter_id = u'SDSS/sdss_z.dati'
    tao_bandpassfilter_65.description = u'Sloan Digital Sky Survey (SDSS) z\n<p>Additional Details: <a href="../static/docs/bpfilters/SDSS_sdss_z.dati.html">SDSS z</a>.</p>'
    tao_bandpassfilter_65.group = u''
    tao_bandpassfilter_65.order = 0L
    tao_bandpassfilter_65 = save_or_locate(tao_bandpassfilter_65)

    tao_bandpassfilter_66 = BandPassFilter()
    tao_bandpassfilter_66.label = u'Subaru/SuprimeCAM B'
    tao_bandpassfilter_66.filter_id = u'SuprimeCAM/B_subaru.dati'
    tao_bandpassfilter_66.description = u'Subaru/SuprimeCAM, B band\n<p>Additional Details: <a href="../static/docs/bpfilters/SuprimeCAM_B_subaru.dati.html">Subaru/SuprimeCAM B</a>.</p>'
    tao_bandpassfilter_66.group = u''
    tao_bandpassfilter_66.order = 0L
    tao_bandpassfilter_66 = save_or_locate(tao_bandpassfilter_66)

    tao_bandpassfilter_67 = BandPassFilter()
    tao_bandpassfilter_67.label = u"Subaru/SuprimeCAM i'"
    tao_bandpassfilter_67.filter_id = u'SuprimeCAM/i_subaru.dati'
    tao_bandpassfilter_67.description = u'Subaru/SuprimeCAM, i\' band\n<p>Additional Details: <a href="../static/docs/bpfilters/SuprimeCAM_i_subaru.dati.html">Subaru/SuprimeCAM i\'</a>.</p>'
    tao_bandpassfilter_67.group = u''
    tao_bandpassfilter_67.order = 0L
    tao_bandpassfilter_67 = save_or_locate(tao_bandpassfilter_67)

    tao_bandpassfilter_68 = BandPassFilter()
    tao_bandpassfilter_68.label = u"Subaru/SuprimeCAM R'"
    tao_bandpassfilter_68.filter_id = u'SuprimeCAM/r_subaru.dati'
    tao_bandpassfilter_68.description = u'Subaru/SuprimeCAM, R\' band\n<p>Additional Details: <a href="../static/docs/bpfilters/SuprimeCAM_r_subaru.dati.html">Subaru/SuprimeCAM R\'</a>.</p>'
    tao_bandpassfilter_68.group = u''
    tao_bandpassfilter_68.order = 0L
    tao_bandpassfilter_68 = save_or_locate(tao_bandpassfilter_68)

    tao_bandpassfilter_69 = BandPassFilter()
    tao_bandpassfilter_69.label = u'Subaru/SuprimeCAM V'
    tao_bandpassfilter_69.filter_id = u'SuprimeCAM/V_subaru.dati'
    tao_bandpassfilter_69.description = u'Subaru/SuprimeCAM, V band\n<p>Additional Details: <a href="../static/docs/bpfilters/SuprimeCAM_V_subaru.dati.html">Subaru/SuprimeCAM V</a>.</p>'
    tao_bandpassfilter_69.group = u''
    tao_bandpassfilter_69.order = 0L
    tao_bandpassfilter_69 = save_or_locate(tao_bandpassfilter_69)

    tao_bandpassfilter_70 = BandPassFilter()
    tao_bandpassfilter_70.label = u"Subaru/SuprimeCAM z'"
    tao_bandpassfilter_70.filter_id = u'SuprimeCAM/z_subaru.dati'
    tao_bandpassfilter_70.description = u'Subaru/SuprimeCAM, z\' band\n<p>Additional Details: <a href="../static/docs/bpfilters/SuprimeCAM_z_subaru.dati.html">Subaru/SuprimeCAM z\'</a>.</p>'
    tao_bandpassfilter_70.group = u''
    tao_bandpassfilter_70.order = 0L
    tao_bandpassfilter_70 = save_or_locate(tao_bandpassfilter_70)

    tao_bandpassfilter_71 = BandPassFilter()
    tao_bandpassfilter_71.label = u'TwoMASS H'
    tao_bandpassfilter_71.filter_id = u'2MASS/Hband_2mass.dati'
    tao_bandpassfilter_71.description = u'2 Micron All Sky Survey (2MASS) H\n<p>Additional Details: <a href="../static/docs/bpfilters/2MASS_Hband_2mass.dati.html">TwoMASS H</a>.</p>'
    tao_bandpassfilter_71.group = u''
    tao_bandpassfilter_71.order = 0L
    tao_bandpassfilter_71 = save_or_locate(tao_bandpassfilter_71)

    tao_bandpassfilter_72 = BandPassFilter()
    tao_bandpassfilter_72.label = u'TwoMASS J'
    tao_bandpassfilter_72.filter_id = u'2MASS/Jband_2mass.dati'
    tao_bandpassfilter_72.description = u'<p>2 Micron All Sky Survey (2MASS) J</p>\n<p>Source:  <a href="http://svo2.cab.inta-csic.es/theory/fps/index.php?id=2MASS/2MASS.J&&mode=browse&gname=2MASS&gname2=2MASS">SVO Filter Profile Service</a></p>\n<p>Additional Details: <a href="../static/docs/bpfilters/2MASS_Jband_2mass.dati.html">TwoMASS J</a>.</p>'
    tao_bandpassfilter_72.group = u''
    tao_bandpassfilter_72.order = 0L
    tao_bandpassfilter_72 = save_or_locate(tao_bandpassfilter_72)

    tao_bandpassfilter_73 = BandPassFilter()
    tao_bandpassfilter_73.label = u'TwoMASS Ks'
    tao_bandpassfilter_73.filter_id = u'2MASS/Ksband_2mass.dati'
    tao_bandpassfilter_73.description = u'2 Micron All Sky Survey (2MASS) Ks\n<p>Additional Details: <a href="../static/docs/bpfilters/2MASS_Ksband_2mass.dati.html">TwoMASS Ks</a>.</p>'
    tao_bandpassfilter_73.group = u''
    tao_bandpassfilter_73.order = 0L
    tao_bandpassfilter_73 = save_or_locate(tao_bandpassfilter_73)

    tao_bandpassfilter_74 = BandPassFilter()
    tao_bandpassfilter_74.label = u'UKIRT H'
    tao_bandpassfilter_74.filter_id = u'UKIRT/H_filter.dati'
    tao_bandpassfilter_74.description = u'UKIRT Infrared Deep Sky Survey, H band\n<p>Additional Details: <a href="../static/docs/bpfilters/UKIRT_H_filter.dati.html">UKIRT H</a>.</p>'
    tao_bandpassfilter_74.group = u''
    tao_bandpassfilter_74.order = 0L
    tao_bandpassfilter_74 = save_or_locate(tao_bandpassfilter_74)

    tao_bandpassfilter_75 = BandPassFilter()
    tao_bandpassfilter_75.label = u'UKIRT J'
    tao_bandpassfilter_75.filter_id = u'UKIRT/J_filter.dati'
    tao_bandpassfilter_75.description = u'UKIRT Infrared Deep Sky Survey, J band\n<p>Additional Details: <a href="../static/docs/bpfilters/UKIRT_J_filter.dati.html">UKIRT J</a>.</p>'
    tao_bandpassfilter_75.group = u''
    tao_bandpassfilter_75.order = 0L
    tao_bandpassfilter_75 = save_or_locate(tao_bandpassfilter_75)

    tao_bandpassfilter_76 = BandPassFilter()
    tao_bandpassfilter_76.label = u'UKIRT K'
    tao_bandpassfilter_76.filter_id = u'UKIRT/K_filter.dati'
    tao_bandpassfilter_76.description = u'UKIRT Infrared Deep Sky Survey, K band\n<p>Additional Details: <a href="../static/docs/bpfilters/UKIRT_K_filter.dati.html">UKIRT K</a>.</p>'
    tao_bandpassfilter_76.group = u''
    tao_bandpassfilter_76.order = 0L
    tao_bandpassfilter_76 = save_or_locate(tao_bandpassfilter_76)

    tao_bandpassfilter_77 = BandPassFilter()
    tao_bandpassfilter_77.label = u'UKIRT Y'
    tao_bandpassfilter_77.filter_id = u'UKIRT/Y_filter.dati'
    tao_bandpassfilter_77.description = u'<p>UKIRT Infrared Deep Sky Survey, Y band</p>\n<p>Source: <a href="http://svo2.cab.inta-csic.es/theory/fps/index.php?id=UKIRT/UKIDSS.Y&&mode=browse&gname=UKIRT&gname2=UKIDSS">SVO Filter Profile Service</a></p>\n<p>Additional Details: <a href="../static/docs/bpfilters/UKIRT_Y_filter.dati.html">UKIRT Y</a>.</p>'
    tao_bandpassfilter_77.group = u''
    tao_bandpassfilter_77.order = 0L
    tao_bandpassfilter_77 = save_or_locate(tao_bandpassfilter_77)

    tao_bandpassfilter_78 = BandPassFilter()
    tao_bandpassfilter_78.label = u'VLT/Hawk-I H'
    tao_bandpassfilter_78.filter_id = u'Hawk-I/HawkI_Hband.dati'
    tao_bandpassfilter_78.description = u'VLT/Hawk-I, H band\n<p>Additional Details: <a href="../static/docs/bpfilters/Hawk-I_HawkI_Hband.dati.html">VLT/Hawk-I H</a>.</p>'
    tao_bandpassfilter_78.group = u''
    tao_bandpassfilter_78.order = 0L
    tao_bandpassfilter_78 = save_or_locate(tao_bandpassfilter_78)

    tao_bandpassfilter_79 = BandPassFilter()
    tao_bandpassfilter_79.label = u'VLT/Hawk-I J'
    tao_bandpassfilter_79.filter_id = u'Hawk-I/HawkI_Jband.dati'
    tao_bandpassfilter_79.description = u'VLT/Hawk-I, J band\n<p>Additional Details: <a href="../static/docs/bpfilters/Hawk-I_HawkI_Jband.dati.html">VLT/Hawk-I J</a>.</p>'
    tao_bandpassfilter_79.group = u''
    tao_bandpassfilter_79.order = 0L
    tao_bandpassfilter_79 = save_or_locate(tao_bandpassfilter_79)

    tao_bandpassfilter_80 = BandPassFilter()
    tao_bandpassfilter_80.label = u'VLT/Hawk-I K'
    tao_bandpassfilter_80.filter_id = u'Hawk-I/HawkI_Kband.dati'
    tao_bandpassfilter_80.description = u'VLT/Hawk-I, K band\n<p>Additional Details: <a href="../static/docs/bpfilters/Hawk-I_HawkI_Kband.dati.html">VLT/Hawk-I K</a>.</p>'
    tao_bandpassfilter_80.group = u''
    tao_bandpassfilter_80.order = 0L
    tao_bandpassfilter_80 = save_or_locate(tao_bandpassfilter_80)

    tao_bandpassfilter_81 = BandPassFilter()
    tao_bandpassfilter_81.label = u'VLT/Hawk-I Y'
    tao_bandpassfilter_81.filter_id = u'Hawk-I/HawkI_Yband.dati'
    tao_bandpassfilter_81.description = u'VLT/Hawk-I, Y band\n<p>Additional Details: <a href="../static/docs/bpfilters/Hawk-I_HawkI_Yband.dati.html">VLT/Hawk-I Y</a>.</p>'
    tao_bandpassfilter_81.group = u''
    tao_bandpassfilter_81.order = 0L
    tao_bandpassfilter_81 = save_or_locate(tao_bandpassfilter_81)

    tao_bandpassfilter_82 = BandPassFilter()
    tao_bandpassfilter_82.label = u'VLT/VIMOS R'
    tao_bandpassfilter_82.filter_id = u'VIMOS/R_vimos_inband.dati'
    tao_bandpassfilter_82.description = u'VLT/VIMOS, R band\n<p>Additional Details: <a href="../static/docs/bpfilters/VIMOS_R_vimos_inband.dati.html">VLT/VIMOS R</a>.</p>'
    tao_bandpassfilter_82.group = u''
    tao_bandpassfilter_82.order = 0L
    tao_bandpassfilter_82 = save_or_locate(tao_bandpassfilter_82)

    tao_bandpassfilter_83 = BandPassFilter()
    tao_bandpassfilter_83.label = u'VLT/VIMOS U'
    tao_bandpassfilter_83.filter_id = u'VIMOS/U_vimos.dati'
    tao_bandpassfilter_83.description = u'VLT/VIMOS, U band\n<p>Additional Details: <a href="../static/docs/bpfilters/VIMOS_U_vimos.dati.html">VLT/VIMOS U</a>.</p>'
    tao_bandpassfilter_83.group = u''
    tao_bandpassfilter_83.order = 0L
    tao_bandpassfilter_83 = save_or_locate(tao_bandpassfilter_83)

    tao_bandpassfilter_84 = BandPassFilter()
    tao_bandpassfilter_84.label = u'VLT/VISTA H'
    tao_bandpassfilter_84.filter_id = u'VISTA/VISTA_Hband.dati'
    tao_bandpassfilter_84.description = u'VLT/VISTA, H band\n<p>Additional Details: <a href="../static/docs/bpfilters/VISTA_VISTA_Hband.dati.html">VLT/VISTA H</a>.</p>'
    tao_bandpassfilter_84.group = u''
    tao_bandpassfilter_84.order = 0L
    tao_bandpassfilter_84 = save_or_locate(tao_bandpassfilter_84)

    tao_bandpassfilter_85 = BandPassFilter()
    tao_bandpassfilter_85.label = u'VLT/VISTA J'
    tao_bandpassfilter_85.filter_id = u'VISTA/VISTA_Jband.dati'
    tao_bandpassfilter_85.description = u'VLT/VISTA, J band\n<p>Additional Details: <a href="../static/docs/bpfilters/VISTA_VISTA_Jband.dati.html">VLT/VISTA J</a>.</p>'
    tao_bandpassfilter_85.group = u''
    tao_bandpassfilter_85.order = 0L
    tao_bandpassfilter_85 = save_or_locate(tao_bandpassfilter_85)

    tao_bandpassfilter_86 = BandPassFilter()
    tao_bandpassfilter_86.label = u'VLT/VISTA K'
    tao_bandpassfilter_86.filter_id = u'VISTA/VISTA_Kband.dati'
    tao_bandpassfilter_86.description = u'VLT/VISTA, K band\n<p>Additional Details: <a href="../static/docs/bpfilters/VISTA_VISTA_Kband.dati.html">VLT/VISTA K</a>.</p>'
    tao_bandpassfilter_86.group = u''
    tao_bandpassfilter_86.order = 0L
    tao_bandpassfilter_86 = save_or_locate(tao_bandpassfilter_86)

    tao_bandpassfilter_87 = BandPassFilter()
    tao_bandpassfilter_87.label = u'VLT/VISTA Y'
    tao_bandpassfilter_87.filter_id = u'VISTA/VISTA_Yband.dati'
    tao_bandpassfilter_87.description = u'VLT/VISTA, Y band\n<p>Additional Details: <a href="../static/docs/bpfilters/VISTA_VISTA_Yband.dati.html">VLT/VISTA Y</a>.</p>'
    tao_bandpassfilter_87.group = u''
    tao_bandpassfilter_87.order = 0L
    tao_bandpassfilter_87 = save_or_locate(tao_bandpassfilter_87)

    #Processing model: DustModel

    from tao.models import DustModel

    tao_dustmodel_1 = DustModel()
    tao_dustmodel_1.name = u'Tonini et al. 2012'
    tao_dustmodel_1.label = u'Tonini et al. 2012'
    tao_dustmodel_1.details = u'This model uses the relationship between colour excess E(B-V) and instantaneous star formation rate to determine the dust content of a galaxy, which is then applied to the galaxy SED using a Calzetti extinction curve<br/>\r\n<p>External link: <a href="http://arxiv.org/abs/1209.1204" target="_blank">Tonini et al. 2012</a></p>'
    tao_dustmodel_1 = save_or_locate(tao_dustmodel_1)

    #Processing model: GlobalParameter

    from tao.models import GlobalParameter

    tao_globalparameter_1 = GlobalParameter()
    tao_globalparameter_1.parameter_name = u'approve.html'
    tao_globalparameter_1.parameter_value = u'<p>Dear {{ title }} {{ first_name }} {{ last_name }}.</p>\r\n\r\n<p>Welcome to Theoretical Astrophysical Observatory, a part of the All-Sky Virtual Obvservatory. Your account has been activated and you may sign-in at the URL below.</p>\r\n\r\n<p><a href="{{ login_url }}">{{ login_url }}</a></p>\r\n\r\n<p>If you have any questions or issues please use the Support form after logging in.</p>\r\n\r\n<p><a href="{{ login_url }}"><img src="http://www.asvo.org.au/wp-content/uploads/2013/01/asvo_logo_white-lo-res.jpg" /></a></p>'
    tao_globalparameter_1.description = u'Template for approval email, html version.'
    tao_globalparameter_1 = save_or_locate(tao_globalparameter_1)

    tao_globalparameter_2 = GlobalParameter()
    tao_globalparameter_2.parameter_name = u'approve.txt'
    tao_globalparameter_2.parameter_value = u'Dear {{ title }} {{ first_name }} {{ last_name }},\r\n\r\nWelcome to Theoretical Astrophysical Observatory, a part of the All-Sky Virtual Obvservatory. Your account has been activated and you may sign-in at the URL below.\r\n\r\n{{ login_url }}\r\n\r\nIf you have any questions or issues please use the Support form after logging in.'
    tao_globalparameter_2.description = u'Template for approval email, text version'
    tao_globalparameter_2 = save_or_locate(tao_globalparameter_2)

    tao_globalparameter_3 = GlobalParameter()
    tao_globalparameter_3.parameter_name = u'registration.html'
    tao_globalparameter_3.parameter_value = u'<p>A new user has registered on TAO.</p>\r\n\r\n<p>Please go to this url to view the currently pending requests: <a href="{{ pending_requests_url }}">{{ pending_requests_url }}</a>.</p>\r\n\r\n<p>User details:</p>\r\n\r\n<p>Name: {{user.title}} {{user.first_name}} {{user.last_name}}<br/>\r\nInstitution: {{user.institution}}<br/>\r\nScientific Interests: <br/>\r\n<pre>{{user.scientific_interests}}</pre>\r\n</p>'
    tao_globalparameter_3.description = u'Template for registration email, html version.\r\nValid macros:\r\n{{ user.title }}\r\n{{ user.first_name }}\r\n{{ user.last_name }}\r\n{{ user.institution }}\r\n{{ user.scientific_interests }}\r\n{{ pending_requests_url }}'
    tao_globalparameter_3 = save_or_locate(tao_globalparameter_3)

    tao_globalparameter_4 = GlobalParameter()
    tao_globalparameter_4.parameter_name = u'registration.txt'
    tao_globalparameter_4.parameter_value = u'A new user has registered on TAO\r\n\r\nPlease go to this url to view the currently pending requests: {{ pending_requests_url }}\r\n\r\nUser details:\r\n\r\nName: {{user.title}} {{user.first_name}} {{user.last_name}}\r\nInstitution: {{user.institution}}\r\nScientific Interests:\r\n{{user.scientific_interests}}'
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
    tao_globalparameter_8.parameter_value = u'<p>Dear {{ user.first_name }} {{ user.last_name }},</p>\r\n\r\n<p>Your <a href="http://tao.asvo.org.au/taostaging/jobs/{{ job.id }}">TAO Staging Catalogue {{ job.id }}</a> has successfully completed.</p>\r\n\r\n<p>Catalogue Description:</p>\r\n<div style="margin-left: 5%">{{ job.description|linebreaks }}</div>\r\n\r\n<p><img src="http://www.asvo.org.au/wp-content/uploads/2013/01/asvo_logo_white-lo-res.jpg" /></p>'
    tao_globalparameter_8.description = u'Template for job status update, html version. Use {{ user }} and {{ job }} template variables'
    tao_globalparameter_8 = save_or_locate(tao_globalparameter_8)

    tao_globalparameter_9 = GlobalParameter()
    tao_globalparameter_9.parameter_name = u'job-status.txt'
    tao_globalparameter_9.parameter_value = u'Dear {{ user.first_name }} {{ user.last_name }},\r\n\r\nYour TAO Staging Catalogue {{ job.id }} has completed.\r\n\r\nPlease view your catalogue at: http://tao.asvo.org.au/taostaging/jobs/{{ job.id }}\r\n\r\nDescription:\r\n\r\n{{ job.description|linebreaks }}'
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

    tao_globalparameter_14 = GlobalParameter()
    tao_globalparameter_14.parameter_name = u'output_formats'
    tao_globalparameter_14.parameter_value = u"[\r\n    {'value':'csv', 'text':'CSV (Text)', 'extension':'csv'},\r\n    {'value':'hdf5', 'text':'HDF5', 'extension':'hdf5'},\r\n    {'value': 'fits', 'text': 'FITS', 'extension': 'fits'},\r\n    {'value': 'votable', 'text': 'VOTable', 'extension': 'xml'},\r\n]\r\n"
    tao_globalparameter_14.description = u'Supported output formats.\r\n\r\nThis is a javascript array containing an object for each support format.  The object attributes are:\r\n\r\nvalue: The name of the format, e.g. "csv"\r\ntext: The label to display to the user, e.g. "CSV (Text)"\r\nextensions: The file extension to use, e.g. "csv"\r\n\r\nThe first entry is the default.\r\n'
    tao_globalparameter_14 = save_or_locate(tao_globalparameter_14)

    tao_globalparameter_15 = GlobalParameter()
    tao_globalparameter_15.parameter_name = u'default_disk_quota'
    tao_globalparameter_15.parameter_value = u'10000'
    tao_globalparameter_15.description = u"This will be the default quota applied unless over-ridden for an individual user. Values are interpreted as per user quota. If absent, disk quotas aren't enforced."
    tao_globalparameter_15 = save_or_locate(tao_globalparameter_15)

    tao_globalparameter_16 = GlobalParameter()
    tao_globalparameter_16.parameter_name = u'default_dataset'
    tao_globalparameter_16.parameter_value = u'4'
    tao_globalparameter_16.description = u'This contains the id (pk) of the default dataset. The selected Simulation and GalaxyModel are taken from the default dataset.'
    tao_globalparameter_16 = save_or_locate(tao_globalparameter_16)

    tao_globalparameter_17 = GlobalParameter()
    tao_globalparameter_17.parameter_name = u'job_too_large_warning'
    tao_globalparameter_17.parameter_value = u'<i><em>NOTE:</em> This job may not complete within the allowed time.</i>'
    tao_globalparameter_17.description = u'Warning text for the UI next to calculated job size. HTML is allowed, use with care.'
    tao_globalparameter_17 = save_or_locate(tao_globalparameter_17)

    #Processing model: SurveyPreset

    from tao.models import SurveyPreset

    tao_surveypreset_1 = SurveyPreset()
    tao_surveypreset_1.name = u'BC03 SSP testing'
    tao_surveypreset_1.parameters = u'<?xml version=\'1.0\' encoding=\'utf-8\'?>\r\n<tao timestamp="2013-09-11T15:07:50+10:00" xmlns="http://tao.asvo.org.au/schema/module-parameters-v1">\r\n  <username>alistair</username>\r\n  <workflow name="alpha-light-cone-image">\r\n    <schema-version>2.0</schema-version>\r\n    <light-cone id="1">\r\n      <module-version>1</module-version>\r\n      <geometry>box</geometry>\r\n      <simulation>Mini-Millennium</simulation>\r\n      <galaxy-model>SAGE</galaxy-model>\r\n      <redshift>2.0700273232</redshift>\r\n      <query-box-size units="Mpc">62.500</query-box-size>\r\n      <output-fields>\r\n        <item description="Total galaxy stellar mass" label="Total Stellar Mass" units="10+10solMass/h">stellarmass</item>\r\n        <item description="Bulge stellar mass only" label="Bulge Stellar Mass" units="10+10solMass/h">bulgemass</item>\r\n        <item description="Supermassive black hole mass" label="Black Hole Mass" units="10+10solMass/h">blackholemass</item>\r\n        <item description="Mass of cold gas in the galaxy" label="Cold Gas Mass" units="10+10solMass/h">coldgas</item>\r\n        <item description="Mass of hot halo gas" label="Hot Gas Mass" units="10+10solMass/h">hotgas</item>\r\n        <item description="Gas mass ejected from the halo" label="Ejected Gas Mass" units="10+10solMass/h">ejectedmass</item>\r\n        <item description="Stellar mass in the intracluster stars" label="Intracluster Stars Mass" units="10+10solMass/h">ics</item>\r\n        <item description="Mass of metals in the total stellar mass" label="Metals Total Stellar Mass" units="10+10solMass/h">metalsstellarmass</item>\r\n        <item description="Mass of metals in the bulge" label="Metals Bulge Mass" units="10+10solMass/h">metalsbulgemass</item>\r\n        <item description="Mass of metals in the cold gas" label="Metals Cold Gas Mass" units="10+10solMass/h">metalscoldgas</item>\r\n        <item description="Mass of metals in the hot gas" label="Metals Hot Gas Mass" units="10+10solMass/h">metalshotgas</item>\r\n        <item description="Mass of metals in the ejected gas" label="Metals Ejected Gas Mass" units="10+10solMass/h">metalsejectedmass</item>\r\n        <item description="Mass of metals in the intracluster stars" label="Metals Intracluster Stars Mass" units="10+10solMass/h">metalsics</item>\r\n        <item description="Galaxy classification: 0=central, 1=Satellite" label="Galaxy Classification">objecttype</item>\r\n        <item description="Stellar disk scale radius" label="Disk Scale Radius" units="10+6pc/h">diskscaleradius</item>\r\n        <item description="Total star formation rate in the galaxy" label="Total Star Formation Rate" units="solMass/yr">sfr</item>\r\n        <item description="Star formation rate in the bulge only" label="Bulge Star Formation Rate" units="solMass/yr">sfrbulge</item>\r\n        <item description="Star formation rate in the intracluster stars" label="Intracluster Stars Star Formation Rate" units="solMass/yr">sfrics</item>\r\n        <item description="Cooling rate of hot halo gas" label="Hot Gas Cooling Rate" units="log(10-7J/s)">cooling</item>\r\n        <item description="AGN radio-mode heating rate" label="AGN Heating Rate" units="log(10-7J/s)">heating</item>\r\n        <item description="Dark matter (sub)halo virial mass" label="Mvir" units="10+10solMass/h">mvir</item>\r\n        <item description="Dark matter (sub)halo virial radius" label="Rvir" units="10+6pc/h">rvir</item>\r\n        <item description="Dark matter (sub)halo virial velocity" label="Vvir" units="km/s">vvir</item>\r\n        <item description="Dark matter (sub)halo maximum circular velocity" label="Vmax" units="km/s">vmax</item>\r\n        <item description="Dark matter halo velocity dispersion" label="Velocity Dispersion" units="km/s">veldisp</item>\r\n        <item description="X component of the (sub)halo spin" label="x Spin">spinx</item>\r\n        <item description="Y component of the (sub)halo spin" label="y Spin">spiny</item>\r\n        <item description="Z component of the (sub)halo spin" label="z Spin">spinz</item>\r\n        <item description="Total simulation particles in the dark matter halo" label="Total particles">len</item>\r\n        <item description="Dark matter FOF halo (central galaxy) virial mass" label="Central Galaxy Mvir" units="10+10solMass/h">centralmvir</item>\r\n        <item description="X coordinate in the selected box/cone" label="x" units="10+6pc/h">pos_x</item>\r\n        <item description="Y coordinate in the selected box/cone" label="y" units="10+6pc/h">pos_y</item>\r\n        <item description="Z coordinate in the selected box/cone" label="z" units="10+6pc/h">pos_z</item>\r\n        <item description="X component of the galaxy/halo velocity" label="x Velocity" units="km/s">velx</item>\r\n        <item description="Y component of the galaxy/halo velocity" label="y Velocity" units="km/s">vely</item>\r\n        <item description="Z component of the galaxy/halo velocity" label="z Velocity" units="km/s">velz</item>\r\n        <item description="Simulation snapshot number" label="Snapshot Number">snapnum</item>\r\n        <item description="Galaxy ID" label="Galaxy ID">globalindex</item>\r\n        <item description="(sub)Halo ID" label="Halo ID">haloindex</item>\r\n        <item description="Central galaxy ID" label="Central Galaxy ID">centralgal</item>\r\n      </output-fields>\r\n    </light-cone>\r\n    <csv id="5">\r\n      <fields>\r\n        <item label="Total Stellar Mass" units="10+10solMass/h">stellarmass</item>\r\n        <item label="Bulge Stellar Mass" units="10+10solMass/h">bulgemass</item>\r\n        <item label="Black Hole Mass" units="10+10solMass/h">blackholemass</item>\r\n        <item label="Cold Gas Mass" units="10+10solMass/h">coldgas</item>\r\n        <item label="Hot Gas Mass" units="10+10solMass/h">hotgas</item>\r\n        <item label="Ejected Gas Mass" units="10+10solMass/h">ejectedmass</item>\r\n        <item label="Intracluster Stars Mass" units="10+10solMass/h">ics</item>\r\n        <item label="Metals Total Stellar Mass" units="10+10solMass/h">metalsstellarmass</item>\r\n        <item label="Metals Bulge Mass" units="10+10solMass/h">metalsbulgemass</item>\r\n        <item label="Metals Cold Gas Mass" units="10+10solMass/h">metalscoldgas</item>\r\n        <item label="Metals Hot Gas Mass" units="10+10solMass/h">metalshotgas</item>\r\n        <item label="Metals Ejected Gas Mass" units="10+10solMass/h">metalsejectedmass</item>\r\n        <item label="Metals Intracluster Stars Mass" units="10+10solMass/h">metalsics</item>\r\n        <item label="Galaxy Classification">objecttype</item>\r\n        <item label="Disk Scale Radius" units="10+6pc/h">diskscaleradius</item>\r\n        <item label="Total Star Formation Rate" units="solMass/yr">sfr</item>\r\n        <item label="Bulge Star Formation Rate" units="solMass/yr">sfrbulge</item>\r\n        <item label="Intracluster Stars Star Formation Rate" units="solMass/yr">sfrics</item>\r\n        <item label="Hot Gas Cooling Rate" units="log(10-7J/s)">cooling</item>\r\n        <item label="AGN Heating Rate" units="log(10-7J/s)">heating</item>\r\n        <item label="Mvir" units="10+10solMass/h">mvir</item>\r\n        <item label="Rvir" units="10+6pc/h">rvir</item>\r\n        <item label="Vvir" units="km/s">vvir</item>\r\n        <item label="Vmax" units="km/s">vmax</item>\r\n        <item label="Velocity Dispersion" units="km/s">veldisp</item>\r\n        <item label="x Spin">spinx</item>\r\n        <item label="y Spin">spiny</item>\r\n        <item label="z Spin">spinz</item>\r\n        <item label="Total particles">len</item>\r\n        <item label="Central Galaxy Mvir" units="10+10solMass/h">centralmvir</item>\r\n        <item label="x" units="10+6pc/h">pos_x</item>\r\n        <item label="y" units="10+6pc/h">pos_y</item>\r\n        <item label="z" units="10+6pc/h">pos_z</item>\r\n        <item label="x Velocity" units="km/s">velx</item>\r\n        <item label="y Velocity" units="km/s">vely</item>\r\n        <item label="z Velocity" units="km/s">velz</item>\r\n        <item label="Snapshot Number">snapnum</item>\r\n        <item label="Galaxy ID">globalindex</item>\r\n        <item label="Halo ID">haloindex</item>\r\n        <item label="Central Galaxy ID">centralgal</item>\r\n        <item label="CFHTLS Megacam g\' (Apparent)">CFHTLS/gMega.dati_apparent</item>\r\n        <item label="CFHTLS Megacam g\' (Absolute)">CFHTLS/gMega.dati_absolute</item>\r\n        <item label="CFHTLS Megacam i\' (Apparent)">CFHTLS/i2Mega_new.dati_apparent</item>\r\n        <item label="CFHTLS Megacam i\' (Absolute)">CFHTLS/i2Mega_new.dati_absolute</item>\r\n        <item label="CFHTLS Megacam r\' (Apparent)">CFHTLS/rMega.dati_apparent</item>\r\n        <item label="CFHTLS Megacam r\' (Absolute)">CFHTLS/rMega.dati_absolute</item>\r\n        <item label="CFHTLS Megacam u* (Apparent)">CFHTLS/uMega.dati_apparent</item>\r\n        <item label="CFHTLS Megacam u* (Absolute)">CFHTLS/uMega.dati_absolute</item>\r\n        <item label="CFHTLS Megacam z\' (Apparent)">CFHTLS/zMega.dati_apparent</item>\r\n        <item label="CFHTLS Megacam z\' (Absolute)">CFHTLS/zMega.dati_absolute</item>\r\n        <item label="GALEX FUV (Apparent)">GALEX/galex_FUV.dati_apparent</item>\r\n        <item label="GALEX FUV (Absolute)">GALEX/galex_FUV.dati_absolute</item>\r\n        <item label="GALEX NUV (Apparent)">GALEX/galex_NUV.dati_apparent</item>\r\n        <item label="GALEX NUV (Absolute)">GALEX/galex_NUV.dati_absolute</item>\r\n        <item label="HST/ACS/WFC1 B (Apparent)">ACS/f435w.WFC1.dati_apparent</item>\r\n        <item label="HST/ACS/WFC1 B (Absolute)">ACS/f435w.WFC1.dati_absolute</item>\r\n        <item label="HST/ACS/WFC1 i (Apparent)">ACS/f775w.WFC1.dati_apparent</item>\r\n        <item label="HST/ACS/WFC1 i (Absolute)">ACS/f775w.WFC1.dati_absolute</item>\r\n        <item label="HST/ACS/WFC1 V (Apparent)">ACS/f606w.WFC1.dati_apparent</item>\r\n        <item label="HST/ACS/WFC1 V (Absolute)">ACS/f606w.WFC1.dati_absolute</item>\r\n        <item label="HST/ACS/WFC1 z (Apparent)">ACS/f850lp.WFC1.dati_apparent</item>\r\n        <item label="HST/ACS/WFC1 z (Absolute)">ACS/f850lp.WFC1.dati_absolute</item>\r\n        <item label="HST/ACS/WFC2 B (Apparent)">ACS/f435w.WFC2.dati_apparent</item>\r\n        <item label="HST/ACS/WFC2 B (Absolute)">ACS/f435w.WFC2.dati_absolute</item>\r\n        <item label="HST/ACS/WFC2 i (Apparent)">ACS/f775w.WFC2.dati_apparent</item>\r\n        <item label="HST/ACS/WFC2 i (Absolute)">ACS/f775w.WFC2.dati_absolute</item>\r\n        <item label="HST/ACS/WFC2 V (Apparent)">ACS/f606w.WFC2.dati_apparent</item>\r\n        <item label="HST/ACS/WFC2 V (Absolute)">ACS/f606w.WFC2.dati_absolute</item>\r\n        <item label="HST/ACS/WFC2 z (Apparent)">ACS/f850lp.WFC2.dati_apparent</item>\r\n        <item label="HST/ACS/WFC2 z (Absolute)">ACS/f850lp.WFC2.dati_absolute</item>\r\n        <item label="HST/Herschel/PACS 100 (Apparent)">PACS/pacs100.dati_apparent</item>\r\n        <item label="HST/Herschel/PACS 100 (Absolute)">PACS/pacs100.dati_absolute</item>\r\n        <item label="HST/Herschel/PACS 160 (Apparent)">PACS/pacs160.dati_apparent</item>\r\n        <item label="HST/Herschel/PACS 160 (Absolute)">PACS/pacs160.dati_absolute</item>\r\n        <item label="HST/Herschel/PACS 70 (Apparent)">PACS/pacs70.dati_apparent</item>\r\n        <item label="HST/Herschel/PACS 70 (Absolute)">PACS/pacs70.dati_absolute</item>\r\n        <item label="HST/Herschel/SPIRE 250 (Apparent)">SPIRE/spire250.dati_apparent</item>\r\n        <item label="HST/Herschel/SPIRE 250 (Absolute)">SPIRE/spire250.dati_absolute</item>\r\n        <item label="HST/Herschel/SPIRE 350 (Apparent)">SPIRE/spire350.dati_apparent</item>\r\n        <item label="HST/Herschel/SPIRE 350 (Absolute)">SPIRE/spire350.dati_absolute</item>\r\n        <item label="HST/Herschel/SPIRE 500 (Apparent)">SPIRE/spire500.dati_apparent</item>\r\n        <item label="HST/Herschel/SPIRE 500 (Absolute)">SPIRE/spire500.dati_absolute</item>\r\n        <item label="HST/Spitzer IRAC1 (Apparent)">IRAC/irac_3.4.dati_apparent</item>\r\n        <item label="HST/Spitzer IRAC1 (Absolute)">IRAC/irac_3.4.dati_absolute</item>\r\n        <item label="HST/Spitzer IRAC2 (Apparent)">IRAC/irac_4.5.dati_apparent</item>\r\n        <item label="HST/Spitzer IRAC2 (Absolute)">IRAC/irac_4.5.dati_absolute</item>\r\n        <item label="HST/Spitzer IRAC3 (Apparent)">IRAC/irac_5.8.dati_apparent</item>\r\n        <item label="HST/Spitzer IRAC3 (Absolute)">IRAC/irac_5.8.dati_absolute</item>\r\n        <item label="HST/Spitzer IRAC4 (Apparent)">IRAC/irac_8.0.dati_apparent</item>\r\n        <item label="HST/Spitzer IRAC4 (Absolute)">IRAC/irac_8.0.dati_absolute</item>\r\n        <item label="HST/Spitzer/MIPS 24 (Apparent)">MIPS/mips_24.dati_apparent</item>\r\n        <item label="HST/Spitzer/MIPS 24 (Absolute)">MIPS/mips_24.dati_absolute</item>\r\n        <item label="HST/WFC3/IR F0.98M (Apparent)">WFC3/f098m.IR.dati_apparent</item>\r\n        <item label="HST/WFC3/IR F0.98M (Absolute)">WFC3/f098m.IR.dati_absolute</item>\r\n        <item label="HST/WFC3/IR F105W (Apparent)">WFC3/f105w.IR.dati_apparent</item>\r\n        <item label="HST/WFC3/IR F105W (Absolute)">WFC3/f105w.IR.dati_absolute</item>\r\n        <item label="HST/WFC3/IR F125W (Apparent)">WFC3/f125w.IR.dati_apparent</item>\r\n        <item label="HST/WFC3/IR F125W (Absolute)">WFC3/f125w.IR.dati_absolute</item>\r\n        <item label="HST/WFC3/IR F160W (Apparent)">WFC3/f160w.IR.dati_apparent</item>\r\n        <item label="HST/WFC3/IR F160W (Absolute)">WFC3/f160w.IR.dati_absolute</item>\r\n        <item label="HST/WFC3/IR/UVIS1 F265W (Apparent)">WFC3/f275w.UVIS1.dati_apparent</item>\r\n        <item label="HST/WFC3/IR/UVIS1 F265W (Absolute)">WFC3/f275w.UVIS1.dati_absolute</item>\r\n        <item label="HST/WFC3/IR/UVIS1 F336W (Apparent)">WFC3/f336w.UVIS1.dati_apparent</item>\r\n        <item label="HST/WFC3/IR/UVIS1 F336W (Absolute)">WFC3/f336w.UVIS1.dati_absolute</item>\r\n        <item label="HST/WFC3/IR/UVIS2 F265W (Apparent)">WFC3/f275w.UVIS2.dati_apparent</item>\r\n        <item label="HST/WFC3/IR/UVIS2 F265W (Absolute)">WFC3/f275w.UVIS2.dati_absolute</item>\r\n        <item label="HST/WFC3/IR/UVIS2 F336W (Apparent)">WFC3/f336w.UVIS2.dati_apparent</item>\r\n        <item label="HST/WFC3/IR/UVIS2 F336W (Absolute)">WFC3/f336w.UVIS2.dati_absolute</item>\r\n        <item label="Johnson B (Apparent)">Johnson/Johnson_B.dati_apparent</item>\r\n        <item label="Johnson B (Absolute)">Johnson/Johnson_B.dati_absolute</item>\r\n        <item label="Johnson H (Apparent)">Johnson/h.dat_apparent</item>\r\n        <item label="Johnson H (Absolute)">Johnson/h.dat_absolute</item>\r\n        <item label="Johnson I (Apparent)">Johnson/Ifilter.dati_apparent</item>\r\n        <item label="Johnson I (Absolute)">Johnson/Ifilter.dati_absolute</item>\r\n        <item label="Johnson J (Apparent)">Johnson/j.dat_apparent</item>\r\n        <item label="Johnson J (Absolute)">Johnson/j.dat_absolute</item>\r\n        <item label="Johnson K (Apparent)">Johnson/k.dat_apparent</item>\r\n        <item label="Johnson K (Absolute)">Johnson/k.dat_absolute</item>\r\n        <item label="Johnson R (Apparent)">Johnson/Rfilter.dati_apparent</item>\r\n        <item label="Johnson R (Absolute)">Johnson/Rfilter.dati_absolute</item>\r\n        <item label="Johnson U (Apparent)">Johnson/Johnson_U.dati_apparent</item>\r\n        <item label="Johnson U (Absolute)">Johnson/Johnson_U.dati_absolute</item>\r\n        <item label="Johnson V (Apparent)">Johnson/Johnson_V.dati_apparent</item>\r\n        <item label="Johnson V (Absolute)">Johnson/Johnson_V.dati_absolute</item>\r\n        <item label="Keck/DEIMOS/DEEP B (Apparent)">DEEP/deep_B.dati_apparent</item>\r\n        <item label="Keck/DEIMOS/DEEP B (Absolute)">DEEP/deep_B.dati_absolute</item>\r\n        <item label="Keck/DEIMOS/DEEP I (Apparent)">DEEP/deep_I.dati_apparent</item>\r\n        <item label="Keck/DEIMOS/DEEP I (Absolute)">DEEP/deep_I.dati_absolute</item>\r\n        <item label="Keck/DEIMOS/DEEP R (Apparent)">DEEP/deep_R.dati_apparent</item>\r\n        <item label="Keck/DEIMOS/DEEP R (Absolute)">DEEP/deep_R.dati_absolute</item>\r\n        <item label="LBC USPEC (Apparent)">LBC/LBCBLUE_USPEC_airm12.dati_apparent</item>\r\n        <item label="LBC USPEC (Absolute)">LBC/LBCBLUE_USPEC_airm12.dati_absolute</item>\r\n        <item label="Mosaic U (Apparent)">MOSAIC/U_ctio_mosaic_tot.dati_apparent</item>\r\n        <item label="Mosaic U (Absolute)">MOSAIC/U_ctio_mosaic_tot.dati_absolute</item>\r\n        <item label="MUSYC/ECDFS B (Apparent)">MUSYC/ecdfs.B.filt.dati_apparent</item>\r\n        <item label="MUSYC/ECDFS B (Absolute)">MUSYC/ecdfs.B.filt.dati_absolute</item>\r\n        <item label="MUSYC/ECDFS H (Apparent)">MUSYC/ecdfs.H.filt.dati_apparent</item>\r\n        <item label="MUSYC/ECDFS H (Absolute)">MUSYC/ecdfs.H.filt.dati_absolute</item>\r\n        <item label="MUSYC/ECDFS I (Apparent)">MUSYC/ecdfs.I.filt.dati_apparent</item>\r\n        <item label="MUSYC/ECDFS I (Absolute)">MUSYC/ecdfs.I.filt.dati_absolute</item>\r\n        <item label="MUSYC/ECDFS J (Apparent)">MUSYC/ecdfs.J.filt.dati_apparent</item>\r\n        <item label="MUSYC/ECDFS J (Absolute)">MUSYC/ecdfs.J.filt.dati_absolute</item>\r\n        <item label="MUSYC/ECDFS K (Apparent)">MUSYC/ecdfs.K.filt.dati_apparent</item>\r\n        <item label="MUSYC/ECDFS K (Absolute)">MUSYC/ecdfs.K.filt.dati_absolute</item>\r\n        <item label="MUSYC/ECDFS R (Apparent)">MUSYC/ecdfs.R.filt.dati_apparent</item>\r\n        <item label="MUSYC/ECDFS R (Absolute)">MUSYC/ecdfs.R.filt.dati_absolute</item>\r\n        <item label="MUSYC/ECDFS U (Apparent)">MUSYC/ecdfs.U.filt.dati_apparent</item>\r\n        <item label="MUSYC/ECDFS U (Absolute)">MUSYC/ecdfs.U.filt.dati_absolute</item>\r\n        <item label="MUSYC/ECDFS V (Apparent)">MUSYC/ecdfs.V.filt.dati_apparent</item>\r\n        <item label="MUSYC/ECDFS V (Absolute)">MUSYC/ecdfs.V.filt.dati_absolute</item>\r\n        <item label="MUSYC/ECDFS z (Apparent)">MUSYC/ecdfs.z.filt.dati_apparent</item>\r\n        <item label="MUSYC/ECDFS z (Absolute)">MUSYC/ecdfs.z.filt.dati_absolute</item>\r\n        <item label="NEWFIRM H (Apparent)">NEWFIRM/newfirmH.dati_apparent</item>\r\n        <item label="NEWFIRM H (Absolute)">NEWFIRM/newfirmH.dati_absolute</item>\r\n        <item label="NEWFIRM J (Apparent)">NEWFIRM/newfirmJ.dati_apparent</item>\r\n        <item label="NEWFIRM J (Absolute)">NEWFIRM/newfirmJ.dati_absolute</item>\r\n        <item label="NEWFIRM K (Apparent)">NEWFIRM/newfirmK.dati_apparent</item>\r\n        <item label="NEWFIRM K (Absolute)">NEWFIRM/newfirmK.dati_absolute</item>\r\n        <item label="SCUBA 850 (Apparent)">SCUBA/SCUBA_850.dati_apparent</item>\r\n        <item label="SCUBA 850 (Absolute)">SCUBA/SCUBA_850.dati_absolute</item>\r\n        <item label="SDSS g (Apparent)">SDSS/sdss_g.dati_apparent</item>\r\n        <item label="SDSS g (Absolute)">SDSS/sdss_g.dati_absolute</item>\r\n        <item label="SDSS i (Apparent)">SDSS/sdss_i.dati_apparent</item>\r\n        <item label="SDSS i (Absolute)">SDSS/sdss_i.dati_absolute</item>\r\n        <item label="SDSS r (Apparent)">SDSS/sdss_r.dati_apparent</item>\r\n        <item label="SDSS r (Absolute)">SDSS/sdss_r.dati_absolute</item>\r\n        <item label="SDSS u (Apparent)">SDSS/sdss_u.dati_apparent</item>\r\n        <item label="SDSS u (Absolute)">SDSS/sdss_u.dati_absolute</item>\r\n        <item label="SDSS z (Apparent)">SDSS/sdss_z.dati_apparent</item>\r\n        <item label="SDSS z (Absolute)">SDSS/sdss_z.dati_absolute</item>\r\n        <item label="Subaru/SuprimeCAM B (Apparent)">SuprimeCAM/B_subaru.dati_apparent</item>\r\n        <item label="Subaru/SuprimeCAM B (Absolute)">SuprimeCAM/B_subaru.dati_absolute</item>\r\n        <item label="Subaru/SuprimeCAM i\' (Apparent)">SuprimeCAM/i_subaru.dati_apparent</item>\r\n        <item label="Subaru/SuprimeCAM i\' (Absolute)">SuprimeCAM/i_subaru.dati_absolute</item>\r\n        <item label="Subaru/SuprimeCAM R\' (Apparent)">SuprimeCAM/r_subaru.dati_apparent</item>\r\n        <item label="Subaru/SuprimeCAM R\' (Absolute)">SuprimeCAM/r_subaru.dati_absolute</item>\r\n        <item label="Subaru/SuprimeCAM V (Apparent)">SuprimeCAM/V_subaru.dati_apparent</item>\r\n        <item label="Subaru/SuprimeCAM V (Absolute)">SuprimeCAM/V_subaru.dati_absolute</item>\r\n        <item label="Subaru/SuprimeCAM z\' (Apparent)">SuprimeCAM/z_subaru.dati_apparent</item>\r\n        <item label="Subaru/SuprimeCAM z\' (Absolute)">SuprimeCAM/z_subaru.dati_absolute</item>\r\n        <item label="TwoMASS H (Apparent)">2MASS/Hband_2mass.dati_apparent</item>\r\n        <item label="TwoMASS H (Absolute)">2MASS/Hband_2mass.dati_absolute</item>\r\n        <item label="TwoMASS J (Apparent)">2MASS/Jband_2mass.dati_apparent</item>\r\n        <item label="TwoMASS J (Absolute)">2MASS/Jband_2mass.dati_absolute</item>\r\n        <item label="TwoMASS Ks (Apparent)">2MASS/Ksband_2mass.dati_apparent</item>\r\n        <item label="TwoMASS Ks (Absolute)">2MASS/Ksband_2mass.dati_absolute</item>\r\n        <item label="UKIRT H (Apparent)">UKIRT/H_filter.dati_apparent</item>\r\n        <item label="UKIRT H (Absolute)">UKIRT/H_filter.dati_absolute</item>\r\n        <item label="UKIRT J (Apparent)">UKIRT/J_filter.dati_apparent</item>\r\n        <item label="UKIRT J (Absolute)">UKIRT/J_filter.dati_absolute</item>\r\n        <item label="UKIRT K (Apparent)">UKIRT/K_filter.dati_apparent</item>\r\n        <item label="UKIRT K (Absolute)">UKIRT/K_filter.dati_absolute</item>\r\n        <item label="UKIRT Y (Apparent)">UKIRT/Y_filter.dati_apparent</item>\r\n        <item label="UKIRT Y (Absolute)">UKIRT/Y_filter.dati_absolute</item>\r\n        <item label="VLT/Hawk-I H (Apparent)">Hawk-I/HawkI_Hband.dati_apparent</item>\r\n        <item label="VLT/Hawk-I H (Absolute)">Hawk-I/HawkI_Hband.dati_absolute</item>\r\n        <item label="VLT/Hawk-I J (Apparent)">Hawk-I/HawkI_Jband.dati_apparent</item>\r\n        <item label="VLT/Hawk-I J (Absolute)">Hawk-I/HawkI_Jband.dati_absolute</item>\r\n        <item label="VLT/Hawk-I K (Apparent)">Hawk-I/HawkI_Kband.dati_apparent</item>\r\n        <item label="VLT/Hawk-I K (Absolute)">Hawk-I/HawkI_Kband.dati_absolute</item>\r\n        <item label="VLT/Hawk-I Y (Apparent)">Hawk-I/HawkI_Yband.dati_apparent</item>\r\n        <item label="VLT/Hawk-I Y (Absolute)">Hawk-I/HawkI_Yband.dati_absolute</item>\r\n        <item label="VLT/VIMOS R (Apparent)">VIMOS/R_vimos_inband.dati_apparent</item>\r\n        <item label="VLT/VIMOS R (Absolute)">VIMOS/R_vimos_inband.dati_absolute</item>\r\n        <item label="VLT/VIMOS U (Apparent)">VIMOS/U_vimos.dati_apparent</item>\r\n        <item label="VLT/VIMOS U (Absolute)">VIMOS/U_vimos.dati_absolute</item>\r\n        <item label="VLT/VISTA H (Apparent)">VISTA/VISTA_Hband.dati_apparent</item>\r\n        <item label="VLT/VISTA H (Absolute)">VISTA/VISTA_Hband.dati_absolute</item>\r\n        <item label="VLT/VISTA J (Apparent)">VISTA/VISTA_Jband.dati_apparent</item>\r\n        <item label="VLT/VISTA J (Absolute)">VISTA/VISTA_Jband.dati_absolute</item>\r\n        <item label="VLT/VISTA K (Apparent)">VISTA/VISTA_Kband.dati_apparent</item>\r\n        <item label="VLT/VISTA K (Absolute)">VISTA/VISTA_Kband.dati_absolute</item>\r\n        <item label="VLT/VISTA Y (Apparent)">VISTA/VISTA_Yband.dati_apparent</item>\r\n        <item label="VLT/VISTA Y (Absolute)">VISTA/VISTA_Yband.dati_absolute</item>\r\n      </fields>\r\n      <parents>\r\n        <item>4</item>\r\n      </parents>\r\n      <module-version>1</module-version>\r\n      <filename>tao.output.csv</filename>\r\n    </csv>\r\n    <sed id="2"><module-version>1</module-version><parents><item>1</item></parents><single-stellar-population-model>bc03/ssp_kroupa.dat</single-stellar-population-model>\r\n<wavelengths-file>bc03/wavelengths.dat</wavelengths-file>\r\n<ages-file>bc03/ages.dat</ages-file>\r\n<metallicities-file>bc03/metallicities.dat</metallicities-file>\r\n</sed>\r\n    <filter id="4">\r\n      <module-version>1</module-version>\r\n      <parents>\r\n        <item>2</item>\r\n      </parents>\r\n      <bandpass-filters>\r\n        <item description="Canada France Hawaii Telescope (CFHTLS/Megacam), g\' band&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/CFHTLS_gMega.dati.html&quot;&gt;CFHTLS Megacam g\'&lt;/a&gt;.&lt;/p&gt;" label="CFHTLS Megacam g\'" selected="apparent,absolute">CFHTLS/gMega.dati</item>\r\n        <item description="Canada France Hawaii Telescope (CFHTLS/Megacam), i\' band&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/CFHTLS_i2Mega_new.dati.html&quot;&gt;CFHTLS Megacam i\'&lt;/a&gt;.&lt;/p&gt;" label="CFHTLS Megacam i\'" selected="apparent,absolute">CFHTLS/i2Mega_new.dati</item>\r\n        <item description="Canada France Hawaii Telescope (CFHTLS/Megacam), r\' band&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/CFHTLS_rMega.dati.html&quot;&gt;CFHTLS Megacam r\'&lt;/a&gt;.&lt;/p&gt;" label="CFHTLS Megacam r\'" selected="apparent,absolute">CFHTLS/rMega.dati</item>\r\n        <item description="Canada France Hawaii Telescope (CFHTLS/Megacam), u* band&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/CFHTLS_uMega.dati.html&quot;&gt;CFHTLS Megacam u*&lt;/a&gt;.&lt;/p&gt;" label="CFHTLS Megacam u*" selected="apparent,absolute">CFHTLS/uMega.dati</item>\r\n        <item description="Canada France Hawaii Telescope (CFHTLS/Megacam), z\' band&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/CFHTLS_zMega.dati.html&quot;&gt;CFHTLS Megacam z\'&lt;/a&gt;.&lt;/p&gt;" label="CFHTLS Megacam z\'" selected="apparent,absolute">CFHTLS/zMega.dati</item>\r\n        <item description="Galaxy Evolution Explorer (GALEX), far-UV&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/GALEX_galex_FUV.dati.html&quot;&gt;GALEX FUV&lt;/a&gt;.&lt;/p&gt;" label="GALEX FUV" selected="apparent,absolute">GALEX/galex_FUV.dati</item>\r\n        <item description="Galaxy Evolution  Explorer (GALEX), near-UV&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/GALEX_galex_NUV.dati.html&quot;&gt;GALEX NUV&lt;/a&gt;.&lt;/p&gt;" label="GALEX NUV" selected="apparent,absolute">GALEX/galex_NUV.dati</item>\r\n        <item description="Hubble Space Telescope Advanced Camera for Surveys, Wide Field Camera 1 (HST/ACS, WFC1), B band (F435W)&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/ACS_f435w.WFC1.dati.html&quot;&gt;HST/ACS/WFC1 B&lt;/a&gt;.&lt;/p&gt;" label="HST/ACS/WFC1 B" selected="apparent,absolute">ACS/f435w.WFC1.dati</item>\r\n        <item description="Hubble Space Telescope Advanced Camera for Surveys, Wide Field Camera 1 (HST/ACS, WFC1), i band (F775W)&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/ACS_f775w.WFC1.dati.html&quot;&gt;HST/ACS/WFC1 i&lt;/a&gt;.&lt;/p&gt;" label="HST/ACS/WFC1 i" selected="apparent,absolute">ACS/f775w.WFC1.dati</item>\r\n        <item description="Hubble Space Telescope Advanced Camera for Surveys, Wide Field Camera 1 (HST/ACS, WFC1), V band (F606W)&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/ACS_f606w.WFC1.dati.html&quot;&gt;HST/ACS/WFC1 V&lt;/a&gt;.&lt;/p&gt;" label="HST/ACS/WFC1 V" selected="apparent,absolute">ACS/f606w.WFC1.dati</item>\r\n        <item description="Hubble Space Telescope Advanced Camera for Surveys, Wide Field Camera 1 (HST/ACS, WFC1), z band (F850LP)&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/ACS_f850lp.WFC1.dati.html&quot;&gt;HST/ACS/WFC1 z&lt;/a&gt;.&lt;/p&gt;" label="HST/ACS/WFC1 z" selected="apparent,absolute">ACS/f850lp.WFC1.dati</item>\r\n        <item description="Hubble Space Telescope Advanced Camera for Surveys, Wide Field Camera 2 (HST/ACS, WFC2), B band (F435W)&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/ACS_f435w.WFC2.dati.html&quot;&gt;HST/ACS/WFC2 B&lt;/a&gt;.&lt;/p&gt;" label="HST/ACS/WFC2 B" selected="apparent,absolute">ACS/f435w.WFC2.dati</item>\r\n        <item description="Hubble Space Telescope Advanced Camera for Surveys, Wide Field Camera 2 (HST/ACS, WFC2), i band (F775W)&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/ACS_f775w.WFC2.dati.html&quot;&gt;HST/ACS/WFC2 i&lt;/a&gt;.&lt;/p&gt;" label="HST/ACS/WFC2 i" selected="apparent,absolute">ACS/f775w.WFC2.dati</item>\r\n        <item description="Hubble Space Telescope Advanced Camera for Surveys, Wide Field Camera 2 (HST/ACS, WFC2), V band (F606W)&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/ACS_f606w.WFC2.dati.html&quot;&gt;HST/ACS/WFC2 V&lt;/a&gt;.&lt;/p&gt;" label="HST/ACS/WFC2 V" selected="apparent,absolute">ACS/f606w.WFC2.dati</item>\r\n        <item description="Hubble Space Telescope Advanced Camera for Surveys, Wide Field Camera 2 (HST/ACS, WFC2), z band (F850LP)&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/ACS_f850lp.WFC2.dati.html&quot;&gt;HST/ACS/WFC2 z&lt;/a&gt;.&lt;/p&gt;" label="HST/ACS/WFC2 z" selected="apparent,absolute">ACS/f850lp.WFC2.dati</item>\r\n        <item description="Hubble Space Telescope, Herschel/PACS, 100 micron&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/PACS_pacs100.dati.html&quot;&gt;HST/Herschel/PACS 100&lt;/a&gt;.&lt;/p&gt;" label="HST/Herschel/PACS 100" selected="apparent,absolute">PACS/pacs100.dati</item>\r\n        <item description="Hubble Space Telescope, Herschel/PACS, 160 micron&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/PACS_pacs160.dati.html&quot;&gt;HST/Herschel/PACS 160&lt;/a&gt;.&lt;/p&gt;" label="HST/Herschel/PACS 160" selected="apparent,absolute">PACS/pacs160.dati</item>\r\n        <item description="Hubble Space Telescope, Herschel/PACS, 70 micron&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/PACS_pacs70.dati.html&quot;&gt;HST/Herschel/PACS 70&lt;/a&gt;.&lt;/p&gt;" label="HST/Herschel/PACS 70" selected="apparent,absolute">PACS/pacs70.dati</item>\r\n        <item description="Hubble Space Telescope, Herschel/SPIRE, 250 micron&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/SPIRE_spire250.dati.html&quot;&gt;HST/Herschel/SPIRE 250&lt;/a&gt;.&lt;/p&gt;" label="HST/Herschel/SPIRE 250" selected="apparent,absolute">SPIRE/spire250.dati</item>\r\n        <item description="Hubble Space Telescope, Herschel/SPIRE, 350 micron&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/SPIRE_spire350.dati.html&quot;&gt;HST/Herschel/SPIRE 350&lt;/a&gt;.&lt;/p&gt;" label="HST/Herschel/SPIRE 350" selected="apparent,absolute">SPIRE/spire350.dati</item>\r\n        <item description="Hubble Space Telescope, Herschel/SPIRE, 500 micron&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/SPIRE_spire500.dati.html&quot;&gt;HST/Herschel/SPIRE 500&lt;/a&gt;.&lt;/p&gt;" label="HST/Herschel/SPIRE 500" selected="apparent,absolute">SPIRE/spire500.dati</item>\r\n        <item description="Hubble Space Telescope, Spitzer/IRAC, ch1 (3.4 micron)&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/IRAC_irac_3.4.dati.html&quot;&gt;HST/Spitzer IRAC1&lt;/a&gt;.&lt;/p&gt;" label="HST/Spitzer IRAC1" selected="apparent,absolute">IRAC/irac_3.4.dati</item>\r\n        <item description="Hubble Space Telescope, Spitzer/IRAC, ch2 (4.5 micron)&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/IRAC_irac_4.5.dati.html&quot;&gt;HST/Spitzer IRAC2&lt;/a&gt;.&lt;/p&gt;" label="HST/Spitzer IRAC2" selected="apparent,absolute">IRAC/irac_4.5.dati</item>\r\n        <item description="Hubble Space Telescope, Spitzer/IRAC, ch3 (5.8 micron)&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/IRAC_irac_5.8.dati.html&quot;&gt;HST/Spitzer IRAC3&lt;/a&gt;.&lt;/p&gt;" label="HST/Spitzer IRAC3" selected="apparent,absolute">IRAC/irac_5.8.dati</item>\r\n        <item description="Hubble Space Telescope, Spitzer/IRAC, ch4 (8.0 micron)&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/IRAC_irac_8.0.dati.html&quot;&gt;HST/Spitzer IRAC4&lt;/a&gt;.&lt;/p&gt;" label="HST/Spitzer IRAC4" selected="apparent,absolute">IRAC/irac_8.0.dati</item>\r\n        <item description="Hubble Space Telescope, Spitzer/MIPS, 24 micron&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/MIPS_mips_24.dati.html&quot;&gt;HST/Spitzer/MIPS 24&lt;/a&gt;.&lt;/p&gt;" label="HST/Spitzer/MIPS 24" selected="apparent,absolute">MIPS/mips_24.dati</item>\r\n        <item description="Hubble Space Telescope, WFC3/IR, F0.98M&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/WFC3_f098m.IR.dati.html&quot;&gt;HST/WFC3/IR F0.98M&lt;/a&gt;.&lt;/p&gt;" label="HST/WFC3/IR F0.98M" selected="apparent,absolute">WFC3/f098m.IR.dati</item>\r\n        <item description="Hubble Space Telescope, WFC3/IR, F105W&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/WFC3_f105w.IR.dati.html&quot;&gt;HST/WFC3/IR F105W&lt;/a&gt;.&lt;/p&gt;" label="HST/WFC3/IR F105W" selected="apparent,absolute">WFC3/f105w.IR.dati</item>\r\n        <item description="Hubble Space Telescope, WFC3/IR, F125W&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/WFC3_f125w.IR.dati.html&quot;&gt;HST/WFC3/IR F125W&lt;/a&gt;.&lt;/p&gt;" label="HST/WFC3/IR F125W" selected="apparent,absolute">WFC3/f125w.IR.dati</item>\r\n        <item description="Hubble Space Telescope, WFC3/IR, F160W&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/WFC3_f160w.IR.dati.html&quot;&gt;HST/WFC3/IR F160W&lt;/a&gt;.&lt;/p&gt;" label="HST/WFC3/IR F160W" selected="apparent,absolute">WFC3/f160w.IR.dati</item>\r\n        <item description="Hubble Space Telescope, WFC3/IR/UVIS1, F275W&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/WFC3_f275w.UVIS1.dati.html&quot;&gt;HST/WFC3/IR/UVIS1 F265W&lt;/a&gt;.&lt;/p&gt;" label="HST/WFC3/IR/UVIS1 F265W" selected="apparent,absolute">WFC3/f275w.UVIS1.dati</item>\r\n        <item description="Hubble Space Telescope, WFC3/IR/UVIS1, F336W&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/WFC3_f336w.UVIS1.dati.html&quot;&gt;HST/WFC3/IR/UVIS1 F336W&lt;/a&gt;.&lt;/p&gt;" label="HST/WFC3/IR/UVIS1 F336W" selected="apparent,absolute">WFC3/f336w.UVIS1.dati</item>\r\n        <item description="Hubble Space Telescope, WFC3/IR/UVIS2, F275W&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/WFC3_f275w.UVIS2.dati.html&quot;&gt;HST/WFC3/IR/UVIS2 F265W&lt;/a&gt;.&lt;/p&gt;" label="HST/WFC3/IR/UVIS2 F265W" selected="apparent,absolute">WFC3/f275w.UVIS2.dati</item>\r\n        <item description="Hubble Space Telescope, WFC3/IR/UVIS2, F336W&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/WFC3_f336w.UVIS2.dati.html&quot;&gt;HST/WFC3/IR/UVIS2 F336W&lt;/a&gt;.&lt;/p&gt;" label="HST/WFC3/IR/UVIS2 F336W" selected="apparent,absolute">WFC3/f336w.UVIS2.dati</item>\r\n        <item description="Johnson B band&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/Johnson_Johnson_B.dati.html&quot;&gt;Johnson B&lt;/a&gt;.&lt;/p&gt;" label="Johnson B" selected="apparent,absolute">Johnson/Johnson_B.dati</item>\r\n        <item description="Johnson H band&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/Johnson_h.dat.html&quot;&gt;Johnson H&lt;/a&gt;.&lt;/p&gt;" label="Johnson H" selected="apparent,absolute">Johnson/h.dat</item>\r\n        <item description="Johnson I band&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/Johnson_Ifilter.dati.html&quot;&gt;Johnson I&lt;/a&gt;.&lt;/p&gt;" label="Johnson I" selected="apparent,absolute">Johnson/Ifilter.dati</item>\r\n        <item description="Johnson J band&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/Johnson_j.dat.html&quot;&gt;Johnson J&lt;/a&gt;.&lt;/p&gt;" label="Johnson J" selected="apparent,absolute">Johnson/j.dat</item>\r\n        <item description="Johnson K band&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/Johnson_k.dat.html&quot;&gt;Johnson K&lt;/a&gt;.&lt;/p&gt;" label="Johnson K" selected="apparent,absolute">Johnson/k.dat</item>\r\n        <item description="Johnson R band&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/Johnson_Rfilter.dati.html&quot;&gt;Johnson R&lt;/a&gt;.&lt;/p&gt;" label="Johnson R" selected="apparent,absolute">Johnson/Rfilter.dati</item>\r\n        <item description="Johnson U band&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/Johnson_Johnson_U.dati.html&quot;&gt;Johnson U&lt;/a&gt;.&lt;/p&gt;" label="Johnson U" selected="apparent,absolute">Johnson/Johnson_U.dati</item>\r\n        <item description="Johnson V band&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/Johnson_Johnson_V.dati.html&quot;&gt;Johnson V&lt;/a&gt;.&lt;/p&gt;" label="Johnson V" selected="apparent,absolute">Johnson/Johnson_V.dati</item>\r\n        <item description="Keck/DEIMOS/DEEP, B band&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/DEEP_deep_B.dati.html&quot;&gt;Keck/DEIMOS/DEEP B&lt;/a&gt;.&lt;/p&gt;" label="Keck/DEIMOS/DEEP B" selected="apparent,absolute">DEEP/deep_B.dati</item>\r\n        <item description="Keck/DEIMOS/DEEP, I band&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/DEEP_deep_I.dati.html&quot;&gt;Keck/DEIMOS/DEEP I&lt;/a&gt;.&lt;/p&gt;" label="Keck/DEIMOS/DEEP I" selected="apparent,absolute">DEEP/deep_I.dati</item>\r\n        <item description="Keck/DEIMOS/DEEP, R band&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/DEEP_deep_R.dati.html&quot;&gt;Keck/DEIMOS/DEEP R&lt;/a&gt;.&lt;/p&gt;" label="Keck/DEIMOS/DEEP R" selected="apparent,absolute">DEEP/deep_R.dati</item>\r\n        <item description="Large Binocular Camera, USPEC&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/LBC_LBCBLUE_USPEC_airm12.dati.html&quot;&gt;LBC USPEC&lt;/a&gt;.&lt;/p&gt;" label="LBC USPEC" selected="apparent,absolute">LBC/LBCBLUE_USPEC_airm12.dati</item>\r\n        <item description="Cerro Tololo Inter-American Observatory (CTIO) Mosaic II, U band&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/MOSAIC_U_ctio_mosaic_tot.dati.html&quot;&gt;Mosaic U&lt;/a&gt;.&lt;/p&gt;" label="Mosaic U" selected="apparent,absolute">MOSAIC/U_ctio_mosaic_tot.dati</item>\r\n        <item description="MUSYC survey, Extended Chandra Deep Field South, B band&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/MUSYC_ecdfs.B.filt.dati.html&quot;&gt;MUSYC/ECDFS B&lt;/a&gt;.&lt;/p&gt;" label="MUSYC/ECDFS B" selected="apparent,absolute">MUSYC/ecdfs.B.filt.dati</item>\r\n        <item description="MUSYC survey, Extended Chandra Deep Field South, H band&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/MUSYC_ecdfs.H.filt.dati.html&quot;&gt;MUSYC/ECDFS H&lt;/a&gt;.&lt;/p&gt;" label="MUSYC/ECDFS H" selected="apparent,absolute">MUSYC/ecdfs.H.filt.dati</item>\r\n        <item description="MUSYC survey, Extended Chandra Deep Field South, I band&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/MUSYC_ecdfs.I.filt.dati.html&quot;&gt;MUSYC/ECDFS I&lt;/a&gt;.&lt;/p&gt;" label="MUSYC/ECDFS I" selected="apparent,absolute">MUSYC/ecdfs.I.filt.dati</item>\r\n        <item description="MUSYC survey, Extended Chandra Deep Field South, J band&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/MUSYC_ecdfs.J.filt.dati.html&quot;&gt;MUSYC/ECDFS J&lt;/a&gt;.&lt;/p&gt;" label="MUSYC/ECDFS J" selected="apparent,absolute">MUSYC/ecdfs.J.filt.dati</item>\r\n        <item description="MUSYC survey, Extended Chandra Deep Field South, K band&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/MUSYC_ecdfs.K.filt.dati.html&quot;&gt;MUSYC/ECDFS K&lt;/a&gt;.&lt;/p&gt;" label="MUSYC/ECDFS K" selected="apparent,absolute">MUSYC/ecdfs.K.filt.dati</item>\r\n        <item description="MUSYC survey, Extended Chandra Deep Field South, R band&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/MUSYC_ecdfs.R.filt.dati.html&quot;&gt;MUSYC/ECDFS R&lt;/a&gt;.&lt;/p&gt;" label="MUSYC/ECDFS R" selected="apparent,absolute">MUSYC/ecdfs.R.filt.dati</item>\r\n        <item description="MUSYC survey, Extended Chandra Deep Field South, U band&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/MUSYC_ecdfs.U.filt.dati.html&quot;&gt;MUSYC/ECDFS U&lt;/a&gt;.&lt;/p&gt;" label="MUSYC/ECDFS U" selected="apparent,absolute">MUSYC/ecdfs.U.filt.dati</item>\r\n        <item description="MUSYC survey, Extended Chandra Deep Field South, V band&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/MUSYC_ecdfs.V.filt.dati.html&quot;&gt;MUSYC/ECDFS V&lt;/a&gt;.&lt;/p&gt;" label="MUSYC/ECDFS V" selected="apparent,absolute">MUSYC/ecdfs.V.filt.dati</item>\r\n        <item description="MUSYC survey, Extended Chandra Deep Field South, z band&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/MUSYC_ecdfs.z.filt.dati.html&quot;&gt;MUSYC/ECDFS z&lt;/a&gt;.&lt;/p&gt;" label="MUSYC/ECDFS z" selected="apparent,absolute">MUSYC/ecdfs.z.filt.dati</item>\r\n        <item description="NOAO Extremely Wide-Field Infrared Imager (NEWFIRM), H band&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/NEWFIRM_newfirmH.dati.html&quot;&gt;NEWFIRM H&lt;/a&gt;.&lt;/p&gt;" label="NEWFIRM H" selected="apparent,absolute">NEWFIRM/newfirmH.dati</item>\r\n        <item description="NOAO Extremely Wide-Field Infrared Imager (NEWFIRM), J band&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/NEWFIRM_newfirmJ.dati.html&quot;&gt;NEWFIRM J&lt;/a&gt;.&lt;/p&gt;" label="NEWFIRM J" selected="apparent,absolute">NEWFIRM/newfirmJ.dati</item>\r\n        <item description="NOAO Extremely Wide-Field Infrared Imager (NEWFIRM), K band&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/NEWFIRM_newfirmK.dati.html&quot;&gt;NEWFIRM K&lt;/a&gt;.&lt;/p&gt;" label="NEWFIRM K" selected="apparent,absolute">NEWFIRM/newfirmK.dati</item>\r\n        <item description="SCUBA 850 micron&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/SCUBA_SCUBA_850.dati.html&quot;&gt;SCUBA 850&lt;/a&gt;.&lt;/p&gt;" label="SCUBA 850" selected="apparent,absolute">SCUBA/SCUBA_850.dati</item>\r\n        <item description="Sloan Digital Sky Survey (SDSS) g&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/SDSS_sdss_g.dati.html&quot;&gt;SDSS g&lt;/a&gt;.&lt;/p&gt;" label="SDSS g" selected="apparent,absolute">SDSS/sdss_g.dati</item>\r\n        <item description="Sloan Digital Sky Survey (SDSS) i&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/SDSS_sdss_i.dati.html&quot;&gt;SDSS i&lt;/a&gt;.&lt;/p&gt;" label="SDSS i" selected="apparent,absolute">SDSS/sdss_i.dati</item>\r\n        <item description="Sloan Digital Sky Survey (SDSS) r&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/SDSS_sdss_r.dati.html&quot;&gt;SDSS r&lt;/a&gt;.&lt;/p&gt;" label="SDSS r" selected="apparent,absolute">SDSS/sdss_r.dati</item>\r\n        <item description="Sloan Digital Sky Survey (SDSS) u&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/SDSS_sdss_u.dati.html&quot;&gt;SDSS u&lt;/a&gt;.&lt;/p&gt;" label="SDSS u" selected="apparent,absolute">SDSS/sdss_u.dati</item>\r\n        <item description="Sloan Digital Sky Survey (SDSS) z&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/SDSS_sdss_z.dati.html&quot;&gt;SDSS z&lt;/a&gt;.&lt;/p&gt;" label="SDSS z" selected="apparent,absolute">SDSS/sdss_z.dati</item>\r\n        <item description="Subaru/SuprimeCAM, B band&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/SuprimeCAM_B_subaru.dati.html&quot;&gt;Subaru/SuprimeCAM B&lt;/a&gt;.&lt;/p&gt;" label="Subaru/SuprimeCAM B" selected="apparent,absolute">SuprimeCAM/B_subaru.dati</item>\r\n        <item description="Subaru/SuprimeCAM, i\' band&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/SuprimeCAM_i_subaru.dati.html&quot;&gt;Subaru/SuprimeCAM i\'&lt;/a&gt;.&lt;/p&gt;" label="Subaru/SuprimeCAM i\'" selected="apparent,absolute">SuprimeCAM/i_subaru.dati</item>\r\n        <item description="Subaru/SuprimeCAM, R\' band&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/SuprimeCAM_r_subaru.dati.html&quot;&gt;Subaru/SuprimeCAM R\'&lt;/a&gt;.&lt;/p&gt;" label="Subaru/SuprimeCAM R\'" selected="apparent,absolute">SuprimeCAM/r_subaru.dati</item>\r\n        <item description="Subaru/SuprimeCAM, V band&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/SuprimeCAM_V_subaru.dati.html&quot;&gt;Subaru/SuprimeCAM V&lt;/a&gt;.&lt;/p&gt;" label="Subaru/SuprimeCAM V" selected="apparent,absolute">SuprimeCAM/V_subaru.dati</item>\r\n        <item description="Subaru/SuprimeCAM, z\' band&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/SuprimeCAM_z_subaru.dati.html&quot;&gt;Subaru/SuprimeCAM z\'&lt;/a&gt;.&lt;/p&gt;" label="Subaru/SuprimeCAM z\'" selected="apparent,absolute">SuprimeCAM/z_subaru.dati</item>\r\n        <item description="2 Micron All Sky Survey (2MASS) H&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/2MASS_Hband_2mass.dati.html&quot;&gt;TwoMASS H&lt;/a&gt;.&lt;/p&gt;" label="TwoMASS H" selected="apparent,absolute">2MASS/Hband_2mass.dati</item>\r\n        <item description="&lt;p&gt;2 Micron All Sky Survey (2MASS) J&lt;/p&gt;&#10;&lt;p&gt;Source:  &lt;a href=&quot;http://svo2.cab.inta-csic.es/theory/fps/index.php?id=2MASS/2MASS.J&amp;&amp;mode=browse&amp;gname=2MASS&amp;gname2=2MASS&quot;&gt;SVO Filter Profile Service&lt;/a&gt;&lt;/p&gt;&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/2MASS_Jband_2mass.dati.html&quot;&gt;TwoMASS J&lt;/a&gt;.&lt;/p&gt;" label="TwoMASS J" selected="apparent,absolute">2MASS/Jband_2mass.dati</item>\r\n        <item description="2 Micron All Sky Survey (2MASS) Ks&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/2MASS_Ksband_2mass.dati.html&quot;&gt;TwoMASS Ks&lt;/a&gt;.&lt;/p&gt;" label="TwoMASS Ks" selected="apparent,absolute">2MASS/Ksband_2mass.dati</item>\r\n        <item description="UKIRT Infrared Deep Sky Survey, H band&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/UKIRT_H_filter.dati.html&quot;&gt;UKIRT H&lt;/a&gt;.&lt;/p&gt;" label="UKIRT H" selected="apparent,absolute">UKIRT/H_filter.dati</item>\r\n        <item description="UKIRT Infrared Deep Sky Survey, J band&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/UKIRT_J_filter.dati.html&quot;&gt;UKIRT J&lt;/a&gt;.&lt;/p&gt;" label="UKIRT J" selected="apparent,absolute">UKIRT/J_filter.dati</item>\r\n        <item description="UKIRT Infrared Deep Sky Survey, K band&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/UKIRT_K_filter.dati.html&quot;&gt;UKIRT K&lt;/a&gt;.&lt;/p&gt;" label="UKIRT K" selected="apparent,absolute">UKIRT/K_filter.dati</item>\r\n        <item description="&lt;p&gt;UKIRT Infrared Deep Sky Survey, Y band&lt;/p&gt;&#10;&lt;p&gt;Source: &lt;a href=&quot;http://svo2.cab.inta-csic.es/theory/fps/index.php?id=UKIRT/UKIDSS.Y&amp;&amp;mode=browse&amp;gname=UKIRT&amp;gname2=UKIDSS&quot;&gt;SVO Filter Profile Service&lt;/a&gt;&lt;/p&gt;&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/UKIRT_Y_filter.dati.html&quot;&gt;UKIRT Y&lt;/a&gt;.&lt;/p&gt;" label="UKIRT Y" selected="apparent,absolute">UKIRT/Y_filter.dati</item>\r\n        <item description="VLT/Hawk-I, H band&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/Hawk-I_HawkI_Hband.dati.html&quot;&gt;VLT/Hawk-I H&lt;/a&gt;.&lt;/p&gt;" label="VLT/Hawk-I H" selected="apparent,absolute">Hawk-I/HawkI_Hband.dati</item>\r\n        <item description="VLT/Hawk-I, J band&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/Hawk-I_HawkI_Jband.dati.html&quot;&gt;VLT/Hawk-I J&lt;/a&gt;.&lt;/p&gt;" label="VLT/Hawk-I J" selected="apparent,absolute">Hawk-I/HawkI_Jband.dati</item>\r\n        <item description="VLT/Hawk-I, K band&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/Hawk-I_HawkI_Kband.dati.html&quot;&gt;VLT/Hawk-I K&lt;/a&gt;.&lt;/p&gt;" label="VLT/Hawk-I K" selected="apparent,absolute">Hawk-I/HawkI_Kband.dati</item>\r\n        <item description="VLT/Hawk-I, Y band&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/Hawk-I_HawkI_Yband.dati.html&quot;&gt;VLT/Hawk-I Y&lt;/a&gt;.&lt;/p&gt;" label="VLT/Hawk-I Y" selected="apparent,absolute">Hawk-I/HawkI_Yband.dati</item>\r\n        <item description="VLT/VIMOS, R band&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/VIMOS_R_vimos_inband.dati.html&quot;&gt;VLT/VIMOS R&lt;/a&gt;.&lt;/p&gt;" label="VLT/VIMOS R" selected="apparent,absolute">VIMOS/R_vimos_inband.dati</item>\r\n        <item description="VLT/VIMOS, U band&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/VIMOS_U_vimos.dati.html&quot;&gt;VLT/VIMOS U&lt;/a&gt;.&lt;/p&gt;" label="VLT/VIMOS U" selected="apparent,absolute">VIMOS/U_vimos.dati</item>\r\n        <item description="VLT/VISTA, H band&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/VISTA_VISTA_Hband.dati.html&quot;&gt;VLT/VISTA H&lt;/a&gt;.&lt;/p&gt;" label="VLT/VISTA H" selected="apparent,absolute">VISTA/VISTA_Hband.dati</item>\r\n        <item description="VLT/VISTA, J band&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/VISTA_VISTA_Jband.dati.html&quot;&gt;VLT/VISTA J&lt;/a&gt;.&lt;/p&gt;" label="VLT/VISTA J" selected="apparent,absolute">VISTA/VISTA_Jband.dati</item>\r\n        <item description="VLT/VISTA, K band&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/VISTA_VISTA_Kband.dati.html&quot;&gt;VLT/VISTA K&lt;/a&gt;.&lt;/p&gt;" label="VLT/VISTA K" selected="apparent,absolute">VISTA/VISTA_Kband.dati</item>\r\n        <item description="VLT/VISTA, Y band&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/VISTA_VISTA_Yband.dati.html&quot;&gt;VLT/VISTA Y&lt;/a&gt;.&lt;/p&gt;" label="VLT/VISTA Y" selected="apparent,absolute">VISTA/VISTA_Yband.dati</item>\r\n      </bandpass-filters>\r\n    </filter>\r\n    <record-filter>\r\n      <module-version>1</module-version>\r\n      <filter>\r\n        <filter-attribute>stellarmass</filter-attribute>\r\n        <filter-min units="10+10solMass/h">0.31</filter-min>\r\n        <filter-max units="10+10solMass/h">None</filter-max>\r\n      </filter>\r\n    </record-filter>\r\n  </workflow>\r\n  <signature>base64encodedsignature</signature>\r\n</tao>\r\n'
    tao_surveypreset_1.description = u'<p>Mini-Millennium / SAGE, z=2, BC03 Kroupa IMF</p>\r\n\r\n<p>This is just a test for the Survey Presets and getting SSPs sorted out.</p>'
    tao_surveypreset_1 = save_or_locate(tao_surveypreset_1)

    #Processing model: DataSet

    from tao.models import DataSet

    tao_dataset_1 = DataSet()
    tao_dataset_1.simulation = tao_simulation_2
    tao_dataset_1.galaxy_model = tao_galaxymodel_2
    tao_dataset_1.database = u'millennium_full_hdf5_dist'
    tao_dataset_1.version = Decimal('1.00')
    tao_dataset_1.import_date = datetime.date(2013, 7, 30)
    tao_dataset_1.available = True
    tao_dataset_1.default_filter_min = 0.31
    tao_dataset_1.default_filter_max = None
    tao_dataset_1.max_job_box_count = 25L
    tao_dataset_1.job_size_p1 = 0.06555053
    tao_dataset_1.job_size_p2 = -0.10355211
    tao_dataset_1.job_size_p3 = 0.37135452
    tao_dataset_1 = save_or_locate(tao_dataset_1)

    tao_dataset_2 = DataSet()
    tao_dataset_2.simulation = tao_simulation_3
    tao_dataset_2.galaxy_model = tao_galaxymodel_2
    tao_dataset_2.database = u'millennium_mini_hdf5_dist'
    tao_dataset_2.version = Decimal('1.00')
    tao_dataset_2.import_date = datetime.date(2013, 7, 30)
    tao_dataset_2.available = True
    tao_dataset_2.default_filter_min = 0.1
    tao_dataset_2.default_filter_max = None
    tao_dataset_2.max_job_box_count = 25L
    tao_dataset_2.job_size_p1 = 0.06555053
    tao_dataset_2.job_size_p2 = -0.10355211
    tao_dataset_2.job_size_p3 = 0.37135452
    tao_dataset_2 = save_or_locate(tao_dataset_2)

    tao_dataset_3 = DataSet()
    tao_dataset_3.simulation = tao_simulation_1
    tao_dataset_3.galaxy_model = tao_galaxymodel_2
    tao_dataset_3.database = u'bolshoi_full_dist'
    tao_dataset_3.version = Decimal('1.00')
    tao_dataset_3.import_date = datetime.date(2013, 7, 30)
    tao_dataset_3.available = True
    tao_dataset_3.default_filter_min = 0.31
    tao_dataset_3.default_filter_max = None
    tao_dataset_3.max_job_box_count = 90L
    tao_dataset_3.job_size_p1 = 0.06555053
    tao_dataset_3.job_size_p2 = -0.10355211
    tao_dataset_3.job_size_p3 = 0.37135452
    tao_dataset_3 = save_or_locate(tao_dataset_3)

    tao_dataset_4 = DataSet()
    tao_dataset_4.simulation = tao_simulation_3
    tao_dataset_4.galaxy_model = tao_galaxymodel_1
    tao_dataset_4.database = u'millennium_mini_galacticus_3'
    tao_dataset_4.version = Decimal('1.00')
    tao_dataset_4.import_date = datetime.date(2013, 8, 26)
    tao_dataset_4.available = True
    tao_dataset_4.default_filter_min = 0.31
    tao_dataset_4.default_filter_max = None
    tao_dataset_4.max_job_box_count = 25L
    tao_dataset_4.job_size_p1 = 0.06555053
    tao_dataset_4.job_size_p2 = -0.10355211
    tao_dataset_4.job_size_p3 = 0.37135452
    tao_dataset_4 = save_or_locate(tao_dataset_4)

    #Processing model: DataSetProperty

    from tao.models import DataSetProperty

    tao_datasetproperty_1 = DataSetProperty()
    tao_datasetproperty_1.name = u'basicmass'
    tao_datasetproperty_1.units = u''
    tao_datasetproperty_1.label = u'basicMass'
    tao_datasetproperty_1.dataset = tao_dataset_4
    tao_datasetproperty_1.data_type = 4L
    tao_datasetproperty_1.is_computed = False
    tao_datasetproperty_1.is_filter = True
    tao_datasetproperty_1.is_output = True
    tao_datasetproperty_1.description = u''
    tao_datasetproperty_1.group = u''
    tao_datasetproperty_1.order = 0L
    tao_datasetproperty_1.is_index = False
    tao_datasetproperty_1.is_primary = False
    tao_datasetproperty_1.flags = 3L
    tao_datasetproperty_1 = save_or_locate(tao_datasetproperty_1)

    tao_datasetproperty_2 = DataSetProperty()
    tao_datasetproperty_2.name = u'basictimelastisolated'
    tao_datasetproperty_2.units = u''
    tao_datasetproperty_2.label = u'basicTimeLastIsolated'
    tao_datasetproperty_2.dataset = tao_dataset_4
    tao_datasetproperty_2.data_type = 4L
    tao_datasetproperty_2.is_computed = False
    tao_datasetproperty_2.is_filter = True
    tao_datasetproperty_2.is_output = True
    tao_datasetproperty_2.description = u''
    tao_datasetproperty_2.group = u''
    tao_datasetproperty_2.order = 0L
    tao_datasetproperty_2.is_index = False
    tao_datasetproperty_2.is_primary = False
    tao_datasetproperty_2.flags = 3L
    tao_datasetproperty_2 = save_or_locate(tao_datasetproperty_2)

    tao_datasetproperty_3 = DataSetProperty()
    tao_datasetproperty_3.name = u'blackholecount'
    tao_datasetproperty_3.units = u''
    tao_datasetproperty_3.label = u'blackHoleCount'
    tao_datasetproperty_3.dataset = tao_dataset_4
    tao_datasetproperty_3.data_type = 5L
    tao_datasetproperty_3.is_computed = False
    tao_datasetproperty_3.is_filter = True
    tao_datasetproperty_3.is_output = True
    tao_datasetproperty_3.description = u''
    tao_datasetproperty_3.group = u''
    tao_datasetproperty_3.order = 0L
    tao_datasetproperty_3.is_index = False
    tao_datasetproperty_3.is_primary = False
    tao_datasetproperty_3.flags = 3L
    tao_datasetproperty_3 = save_or_locate(tao_datasetproperty_3)

    tao_datasetproperty_4 = DataSetProperty()
    tao_datasetproperty_4.name = u'blackholemass'
    tao_datasetproperty_4.units = u'10+10solMass/h'
    tao_datasetproperty_4.label = u'blackHoleMass'
    tao_datasetproperty_4.dataset = tao_dataset_4
    tao_datasetproperty_4.data_type = 4L
    tao_datasetproperty_4.is_computed = False
    tao_datasetproperty_4.is_filter = True
    tao_datasetproperty_4.is_output = True
    tao_datasetproperty_4.description = u''
    tao_datasetproperty_4.group = u''
    tao_datasetproperty_4.order = 0L
    tao_datasetproperty_4.is_index = False
    tao_datasetproperty_4.is_primary = False
    tao_datasetproperty_4.flags = 3L
    tao_datasetproperty_4 = save_or_locate(tao_datasetproperty_4)

    tao_datasetproperty_5 = DataSetProperty()
    tao_datasetproperty_5.name = u'blackholespin'
    tao_datasetproperty_5.units = u''
    tao_datasetproperty_5.label = u'blackHoleSpin'
    tao_datasetproperty_5.dataset = tao_dataset_4
    tao_datasetproperty_5.data_type = 4L
    tao_datasetproperty_5.is_computed = False
    tao_datasetproperty_5.is_filter = True
    tao_datasetproperty_5.is_output = True
    tao_datasetproperty_5.description = u''
    tao_datasetproperty_5.group = u''
    tao_datasetproperty_5.order = 0L
    tao_datasetproperty_5.is_index = False
    tao_datasetproperty_5.is_primary = False
    tao_datasetproperty_5.flags = 3L
    tao_datasetproperty_5 = save_or_locate(tao_datasetproperty_5)

    tao_datasetproperty_6 = DataSetProperty()
    tao_datasetproperty_6.name = u'childnode'
    tao_datasetproperty_6.units = u''
    tao_datasetproperty_6.label = u'childNode'
    tao_datasetproperty_6.dataset = tao_dataset_4
    tao_datasetproperty_6.data_type = 5L
    tao_datasetproperty_6.is_computed = False
    tao_datasetproperty_6.is_filter = True
    tao_datasetproperty_6.is_output = True
    tao_datasetproperty_6.description = u''
    tao_datasetproperty_6.group = u''
    tao_datasetproperty_6.order = 0L
    tao_datasetproperty_6.is_index = False
    tao_datasetproperty_6.is_primary = False
    tao_datasetproperty_6.flags = 3L
    tao_datasetproperty_6 = save_or_locate(tao_datasetproperty_6)

    tao_datasetproperty_7 = DataSetProperty()
    tao_datasetproperty_7.name = u'coldgas'
    tao_datasetproperty_7.units = u''
    tao_datasetproperty_7.label = u'Cold Gas'
    tao_datasetproperty_7.dataset = tao_dataset_4
    tao_datasetproperty_7.data_type = 4L
    tao_datasetproperty_7.is_computed = False
    tao_datasetproperty_7.is_filter = True
    tao_datasetproperty_7.is_output = True
    tao_datasetproperty_7.description = u'Was diskmassgas'
    tao_datasetproperty_7.group = u''
    tao_datasetproperty_7.order = 0L
    tao_datasetproperty_7.is_index = False
    tao_datasetproperty_7.is_primary = False
    tao_datasetproperty_7.flags = 3L
    tao_datasetproperty_7 = save_or_locate(tao_datasetproperty_7)

    tao_datasetproperty_8 = DataSetProperty()
    tao_datasetproperty_8.name = u'darkmatterprofilescale'
    tao_datasetproperty_8.units = u''
    tao_datasetproperty_8.label = u'darkMatterProfileScale'
    tao_datasetproperty_8.dataset = tao_dataset_4
    tao_datasetproperty_8.data_type = 4L
    tao_datasetproperty_8.is_computed = False
    tao_datasetproperty_8.is_filter = True
    tao_datasetproperty_8.is_output = True
    tao_datasetproperty_8.description = u''
    tao_datasetproperty_8.group = u''
    tao_datasetproperty_8.order = 0L
    tao_datasetproperty_8.is_index = False
    tao_datasetproperty_8.is_primary = False
    tao_datasetproperty_8.flags = 3L
    tao_datasetproperty_8 = save_or_locate(tao_datasetproperty_8)

    tao_datasetproperty_9 = DataSetProperty()
    tao_datasetproperty_9.name = u'diskabundancesgasmetals'
    tao_datasetproperty_9.units = u''
    tao_datasetproperty_9.label = u'diskAbundancesGasMetals'
    tao_datasetproperty_9.dataset = tao_dataset_4
    tao_datasetproperty_9.data_type = 4L
    tao_datasetproperty_9.is_computed = False
    tao_datasetproperty_9.is_filter = True
    tao_datasetproperty_9.is_output = True
    tao_datasetproperty_9.description = u''
    tao_datasetproperty_9.group = u''
    tao_datasetproperty_9.order = 0L
    tao_datasetproperty_9.is_index = False
    tao_datasetproperty_9.is_primary = False
    tao_datasetproperty_9.flags = 3L
    tao_datasetproperty_9 = save_or_locate(tao_datasetproperty_9)

    tao_datasetproperty_10 = DataSetProperty()
    tao_datasetproperty_10.name = u'diskabundancesstellarmetals'
    tao_datasetproperty_10.units = u''
    tao_datasetproperty_10.label = u'diskAbundancesStellarMetals'
    tao_datasetproperty_10.dataset = tao_dataset_4
    tao_datasetproperty_10.data_type = 4L
    tao_datasetproperty_10.is_computed = False
    tao_datasetproperty_10.is_filter = True
    tao_datasetproperty_10.is_output = True
    tao_datasetproperty_10.description = u''
    tao_datasetproperty_10.group = u''
    tao_datasetproperty_10.order = 0L
    tao_datasetproperty_10.is_index = False
    tao_datasetproperty_10.is_primary = False
    tao_datasetproperty_10.flags = 3L
    tao_datasetproperty_10 = save_or_locate(tao_datasetproperty_10)

    tao_datasetproperty_11 = DataSetProperty()
    tao_datasetproperty_11.name = u'diskangularmomentum'
    tao_datasetproperty_11.units = u''
    tao_datasetproperty_11.label = u'diskAngularMomentum'
    tao_datasetproperty_11.dataset = tao_dataset_4
    tao_datasetproperty_11.data_type = 4L
    tao_datasetproperty_11.is_computed = False
    tao_datasetproperty_11.is_filter = True
    tao_datasetproperty_11.is_output = True
    tao_datasetproperty_11.description = u''
    tao_datasetproperty_11.group = u''
    tao_datasetproperty_11.order = 0L
    tao_datasetproperty_11.is_index = False
    tao_datasetproperty_11.is_primary = False
    tao_datasetproperty_11.flags = 3L
    tao_datasetproperty_11 = save_or_locate(tao_datasetproperty_11)

    tao_datasetproperty_12 = DataSetProperty()
    tao_datasetproperty_12.name = u'diskmassstellar'
    tao_datasetproperty_12.units = u''
    tao_datasetproperty_12.label = u'diskMassStellar'
    tao_datasetproperty_12.dataset = tao_dataset_4
    tao_datasetproperty_12.data_type = 4L
    tao_datasetproperty_12.is_computed = False
    tao_datasetproperty_12.is_filter = True
    tao_datasetproperty_12.is_output = True
    tao_datasetproperty_12.description = u''
    tao_datasetproperty_12.group = u''
    tao_datasetproperty_12.order = 0L
    tao_datasetproperty_12.is_index = False
    tao_datasetproperty_12.is_primary = False
    tao_datasetproperty_12.flags = 3L
    tao_datasetproperty_12 = save_or_locate(tao_datasetproperty_12)

    tao_datasetproperty_13 = DataSetProperty()
    tao_datasetproperty_13.name = u'diskradius'
    tao_datasetproperty_13.units = u''
    tao_datasetproperty_13.label = u'diskRadius'
    tao_datasetproperty_13.dataset = tao_dataset_4
    tao_datasetproperty_13.data_type = 4L
    tao_datasetproperty_13.is_computed = False
    tao_datasetproperty_13.is_filter = True
    tao_datasetproperty_13.is_output = True
    tao_datasetproperty_13.description = u''
    tao_datasetproperty_13.group = u''
    tao_datasetproperty_13.order = 0L
    tao_datasetproperty_13.is_index = False
    tao_datasetproperty_13.is_primary = False
    tao_datasetproperty_13.flags = 3L
    tao_datasetproperty_13 = save_or_locate(tao_datasetproperty_13)

    tao_datasetproperty_14 = DataSetProperty()
    tao_datasetproperty_14.name = u'diskvelocity'
    tao_datasetproperty_14.units = u''
    tao_datasetproperty_14.label = u'diskVelocity'
    tao_datasetproperty_14.dataset = tao_dataset_4
    tao_datasetproperty_14.data_type = 4L
    tao_datasetproperty_14.is_computed = False
    tao_datasetproperty_14.is_filter = True
    tao_datasetproperty_14.is_output = True
    tao_datasetproperty_14.description = u''
    tao_datasetproperty_14.group = u''
    tao_datasetproperty_14.order = 0L
    tao_datasetproperty_14.is_index = False
    tao_datasetproperty_14.is_primary = False
    tao_datasetproperty_14.flags = 3L
    tao_datasetproperty_14 = save_or_locate(tao_datasetproperty_14)

    tao_datasetproperty_15 = DataSetProperty()
    tao_datasetproperty_15.name = u'globalgalaxyid'
    tao_datasetproperty_15.units = u''
    tao_datasetproperty_15.label = u'GlobalGalaxyID'
    tao_datasetproperty_15.dataset = tao_dataset_4
    tao_datasetproperty_15.data_type = 5L
    tao_datasetproperty_15.is_computed = False
    tao_datasetproperty_15.is_filter = True
    tao_datasetproperty_15.is_output = True
    tao_datasetproperty_15.description = u''
    tao_datasetproperty_15.group = u''
    tao_datasetproperty_15.order = 0L
    tao_datasetproperty_15.is_index = False
    tao_datasetproperty_15.is_primary = False
    tao_datasetproperty_15.flags = 3L
    tao_datasetproperty_15 = save_or_locate(tao_datasetproperty_15)

    tao_datasetproperty_16 = DataSetProperty()
    tao_datasetproperty_16.name = u'globalindex'
    tao_datasetproperty_16.units = u''
    tao_datasetproperty_16.label = u'GlobalIndex'
    tao_datasetproperty_16.dataset = tao_dataset_4
    tao_datasetproperty_16.data_type = 5L
    tao_datasetproperty_16.is_computed = False
    tao_datasetproperty_16.is_filter = True
    tao_datasetproperty_16.is_output = True
    tao_datasetproperty_16.description = u''
    tao_datasetproperty_16.group = u''
    tao_datasetproperty_16.order = 0L
    tao_datasetproperty_16.is_index = False
    tao_datasetproperty_16.is_primary = False
    tao_datasetproperty_16.flags = 3L
    tao_datasetproperty_16 = save_or_locate(tao_datasetproperty_16)

    tao_datasetproperty_17 = DataSetProperty()
    tao_datasetproperty_17.name = u'hothaloabundancesmetals'
    tao_datasetproperty_17.units = u''
    tao_datasetproperty_17.label = u'hotHaloAbundancesMetals'
    tao_datasetproperty_17.dataset = tao_dataset_4
    tao_datasetproperty_17.data_type = 4L
    tao_datasetproperty_17.is_computed = False
    tao_datasetproperty_17.is_filter = True
    tao_datasetproperty_17.is_output = True
    tao_datasetproperty_17.description = u''
    tao_datasetproperty_17.group = u''
    tao_datasetproperty_17.order = 0L
    tao_datasetproperty_17.is_index = False
    tao_datasetproperty_17.is_primary = False
    tao_datasetproperty_17.flags = 3L
    tao_datasetproperty_17 = save_or_locate(tao_datasetproperty_17)

    tao_datasetproperty_18 = DataSetProperty()
    tao_datasetproperty_18.name = u'hothaloangularmomentum'
    tao_datasetproperty_18.units = u''
    tao_datasetproperty_18.label = u'hotHaloAngularMomentum'
    tao_datasetproperty_18.dataset = tao_dataset_4
    tao_datasetproperty_18.data_type = 4L
    tao_datasetproperty_18.is_computed = False
    tao_datasetproperty_18.is_filter = True
    tao_datasetproperty_18.is_output = True
    tao_datasetproperty_18.description = u''
    tao_datasetproperty_18.group = u''
    tao_datasetproperty_18.order = 0L
    tao_datasetproperty_18.is_index = False
    tao_datasetproperty_18.is_primary = False
    tao_datasetproperty_18.flags = 3L
    tao_datasetproperty_18 = save_or_locate(tao_datasetproperty_18)

    tao_datasetproperty_19 = DataSetProperty()
    tao_datasetproperty_19.name = u'hothalomass'
    tao_datasetproperty_19.units = u''
    tao_datasetproperty_19.label = u'hotHaloMass'
    tao_datasetproperty_19.dataset = tao_dataset_4
    tao_datasetproperty_19.data_type = 4L
    tao_datasetproperty_19.is_computed = False
    tao_datasetproperty_19.is_filter = True
    tao_datasetproperty_19.is_output = True
    tao_datasetproperty_19.description = u''
    tao_datasetproperty_19.group = u''
    tao_datasetproperty_19.order = 0L
    tao_datasetproperty_19.is_index = False
    tao_datasetproperty_19.is_primary = False
    tao_datasetproperty_19.flags = 3L
    tao_datasetproperty_19 = save_or_locate(tao_datasetproperty_19)

    tao_datasetproperty_20 = DataSetProperty()
    tao_datasetproperty_20.name = u'hothaloouterradius'
    tao_datasetproperty_20.units = u''
    tao_datasetproperty_20.label = u'hotHaloOuterRadius'
    tao_datasetproperty_20.dataset = tao_dataset_4
    tao_datasetproperty_20.data_type = 4L
    tao_datasetproperty_20.is_computed = False
    tao_datasetproperty_20.is_filter = True
    tao_datasetproperty_20.is_output = True
    tao_datasetproperty_20.description = u''
    tao_datasetproperty_20.group = u''
    tao_datasetproperty_20.order = 0L
    tao_datasetproperty_20.is_index = False
    tao_datasetproperty_20.is_primary = False
    tao_datasetproperty_20.flags = 3L
    tao_datasetproperty_20 = save_or_locate(tao_datasetproperty_20)

    tao_datasetproperty_21 = DataSetProperty()
    tao_datasetproperty_21.name = u'hothalooutflowedabundancesmetals'
    tao_datasetproperty_21.units = u''
    tao_datasetproperty_21.label = u'hotHaloOutflowedAbundancesMetals'
    tao_datasetproperty_21.dataset = tao_dataset_4
    tao_datasetproperty_21.data_type = 4L
    tao_datasetproperty_21.is_computed = False
    tao_datasetproperty_21.is_filter = True
    tao_datasetproperty_21.is_output = True
    tao_datasetproperty_21.description = u''
    tao_datasetproperty_21.group = u''
    tao_datasetproperty_21.order = 0L
    tao_datasetproperty_21.is_index = False
    tao_datasetproperty_21.is_primary = False
    tao_datasetproperty_21.flags = 3L
    tao_datasetproperty_21 = save_or_locate(tao_datasetproperty_21)

    tao_datasetproperty_22 = DataSetProperty()
    tao_datasetproperty_22.name = u'hothalooutflowedangularmomentum'
    tao_datasetproperty_22.units = u''
    tao_datasetproperty_22.label = u'hotHaloOutflowedAngularMomentum'
    tao_datasetproperty_22.dataset = tao_dataset_4
    tao_datasetproperty_22.data_type = 4L
    tao_datasetproperty_22.is_computed = False
    tao_datasetproperty_22.is_filter = True
    tao_datasetproperty_22.is_output = True
    tao_datasetproperty_22.description = u''
    tao_datasetproperty_22.group = u''
    tao_datasetproperty_22.order = 0L
    tao_datasetproperty_22.is_index = False
    tao_datasetproperty_22.is_primary = False
    tao_datasetproperty_22.flags = 3L
    tao_datasetproperty_22 = save_or_locate(tao_datasetproperty_22)

    tao_datasetproperty_23 = DataSetProperty()
    tao_datasetproperty_23.name = u'hothalooutflowedmass'
    tao_datasetproperty_23.units = u''
    tao_datasetproperty_23.label = u'hotHaloOutflowedMass'
    tao_datasetproperty_23.dataset = tao_dataset_4
    tao_datasetproperty_23.data_type = 4L
    tao_datasetproperty_23.is_computed = False
    tao_datasetproperty_23.is_filter = True
    tao_datasetproperty_23.is_output = True
    tao_datasetproperty_23.description = u''
    tao_datasetproperty_23.group = u''
    tao_datasetproperty_23.order = 0L
    tao_datasetproperty_23.is_index = False
    tao_datasetproperty_23.is_primary = False
    tao_datasetproperty_23.flags = 3L
    tao_datasetproperty_23 = save_or_locate(tao_datasetproperty_23)

    tao_datasetproperty_24 = DataSetProperty()
    tao_datasetproperty_24.name = u'hothalounaccretedmass'
    tao_datasetproperty_24.units = u''
    tao_datasetproperty_24.label = u'hotHaloUnaccretedMass'
    tao_datasetproperty_24.dataset = tao_dataset_4
    tao_datasetproperty_24.data_type = 4L
    tao_datasetproperty_24.is_computed = False
    tao_datasetproperty_24.is_filter = True
    tao_datasetproperty_24.is_output = True
    tao_datasetproperty_24.description = u''
    tao_datasetproperty_24.group = u''
    tao_datasetproperty_24.order = 0L
    tao_datasetproperty_24.is_index = False
    tao_datasetproperty_24.is_primary = False
    tao_datasetproperty_24.flags = 3L
    tao_datasetproperty_24 = save_or_locate(tao_datasetproperty_24)

    tao_datasetproperty_25 = DataSetProperty()
    tao_datasetproperty_25.name = u'indicesbranchtip'
    tao_datasetproperty_25.units = u''
    tao_datasetproperty_25.label = u'indicesBranchTip'
    tao_datasetproperty_25.dataset = tao_dataset_4
    tao_datasetproperty_25.data_type = 5L
    tao_datasetproperty_25.is_computed = False
    tao_datasetproperty_25.is_filter = True
    tao_datasetproperty_25.is_output = True
    tao_datasetproperty_25.description = u''
    tao_datasetproperty_25.group = u''
    tao_datasetproperty_25.order = 0L
    tao_datasetproperty_25.is_index = False
    tao_datasetproperty_25.is_primary = False
    tao_datasetproperty_25.flags = 3L
    tao_datasetproperty_25 = save_or_locate(tao_datasetproperty_25)

    tao_datasetproperty_26 = DataSetProperty()
    tao_datasetproperty_26.name = u'interoutputdiskstarformationrate'
    tao_datasetproperty_26.units = u''
    tao_datasetproperty_26.label = u'interOutputDiskStarFormationRate'
    tao_datasetproperty_26.dataset = tao_dataset_4
    tao_datasetproperty_26.data_type = 4L
    tao_datasetproperty_26.is_computed = False
    tao_datasetproperty_26.is_filter = True
    tao_datasetproperty_26.is_output = True
    tao_datasetproperty_26.description = u''
    tao_datasetproperty_26.group = u''
    tao_datasetproperty_26.order = 0L
    tao_datasetproperty_26.is_index = False
    tao_datasetproperty_26.is_primary = False
    tao_datasetproperty_26.flags = 3L
    tao_datasetproperty_26 = save_or_locate(tao_datasetproperty_26)

    tao_datasetproperty_27 = DataSetProperty()
    tao_datasetproperty_27.name = u'mergertreeindex'
    tao_datasetproperty_27.units = u''
    tao_datasetproperty_27.label = u'mergerTreeIndex'
    tao_datasetproperty_27.dataset = tao_dataset_4
    tao_datasetproperty_27.data_type = 5L
    tao_datasetproperty_27.is_computed = False
    tao_datasetproperty_27.is_filter = True
    tao_datasetproperty_27.is_output = True
    tao_datasetproperty_27.description = u''
    tao_datasetproperty_27.group = u''
    tao_datasetproperty_27.order = 0L
    tao_datasetproperty_27.is_index = False
    tao_datasetproperty_27.is_primary = False
    tao_datasetproperty_27.flags = 3L
    tao_datasetproperty_27 = save_or_locate(tao_datasetproperty_27)

    tao_datasetproperty_28 = DataSetProperty()
    tao_datasetproperty_28.name = u'metalscoldgas'
    tao_datasetproperty_28.units = u'10+10solMass/h'
    tao_datasetproperty_28.label = u'MetalsColdGas'
    tao_datasetproperty_28.dataset = tao_dataset_4
    tao_datasetproperty_28.data_type = 4L
    tao_datasetproperty_28.is_computed = False
    tao_datasetproperty_28.is_filter = True
    tao_datasetproperty_28.is_output = True
    tao_datasetproperty_28.description = u''
    tao_datasetproperty_28.group = u''
    tao_datasetproperty_28.order = 0L
    tao_datasetproperty_28.is_index = False
    tao_datasetproperty_28.is_primary = False
    tao_datasetproperty_28.flags = 3L
    tao_datasetproperty_28 = save_or_locate(tao_datasetproperty_28)

    tao_datasetproperty_29 = DataSetProperty()
    tao_datasetproperty_29.name = u'nodeisisolated'
    tao_datasetproperty_29.units = u''
    tao_datasetproperty_29.label = u'nodeIsIsolated'
    tao_datasetproperty_29.dataset = tao_dataset_4
    tao_datasetproperty_29.data_type = 5L
    tao_datasetproperty_29.is_computed = False
    tao_datasetproperty_29.is_filter = True
    tao_datasetproperty_29.is_output = True
    tao_datasetproperty_29.description = u''
    tao_datasetproperty_29.group = u''
    tao_datasetproperty_29.order = 0L
    tao_datasetproperty_29.is_index = False
    tao_datasetproperty_29.is_primary = False
    tao_datasetproperty_29.flags = 3L
    tao_datasetproperty_29 = save_or_locate(tao_datasetproperty_29)

    tao_datasetproperty_30 = DataSetProperty()
    tao_datasetproperty_30.name = u'parentnode'
    tao_datasetproperty_30.units = u''
    tao_datasetproperty_30.label = u'parentNode'
    tao_datasetproperty_30.dataset = tao_dataset_4
    tao_datasetproperty_30.data_type = 5L
    tao_datasetproperty_30.is_computed = False
    tao_datasetproperty_30.is_filter = True
    tao_datasetproperty_30.is_output = True
    tao_datasetproperty_30.description = u''
    tao_datasetproperty_30.group = u''
    tao_datasetproperty_30.order = 0L
    tao_datasetproperty_30.is_index = False
    tao_datasetproperty_30.is_primary = False
    tao_datasetproperty_30.flags = 3L
    tao_datasetproperty_30 = save_or_locate(tao_datasetproperty_30)

    tao_datasetproperty_31 = DataSetProperty()
    tao_datasetproperty_31.name = u'satelliteboundmass'
    tao_datasetproperty_31.units = u''
    tao_datasetproperty_31.label = u'satelliteBoundMass'
    tao_datasetproperty_31.dataset = tao_dataset_4
    tao_datasetproperty_31.data_type = 4L
    tao_datasetproperty_31.is_computed = False
    tao_datasetproperty_31.is_filter = True
    tao_datasetproperty_31.is_output = True
    tao_datasetproperty_31.description = u''
    tao_datasetproperty_31.group = u''
    tao_datasetproperty_31.order = 0L
    tao_datasetproperty_31.is_index = False
    tao_datasetproperty_31.is_primary = False
    tao_datasetproperty_31.flags = 3L
    tao_datasetproperty_31 = save_or_locate(tao_datasetproperty_31)

    tao_datasetproperty_32 = DataSetProperty()
    tao_datasetproperty_32.name = u'satellitemergetime'
    tao_datasetproperty_32.units = u''
    tao_datasetproperty_32.label = u'satelliteMergeTime'
    tao_datasetproperty_32.dataset = tao_dataset_4
    tao_datasetproperty_32.data_type = 4L
    tao_datasetproperty_32.is_computed = False
    tao_datasetproperty_32.is_filter = True
    tao_datasetproperty_32.is_output = True
    tao_datasetproperty_32.description = u''
    tao_datasetproperty_32.group = u''
    tao_datasetproperty_32.order = 0L
    tao_datasetproperty_32.is_index = False
    tao_datasetproperty_32.is_primary = False
    tao_datasetproperty_32.flags = 3L
    tao_datasetproperty_32 = save_or_locate(tao_datasetproperty_32)

    tao_datasetproperty_33 = DataSetProperty()
    tao_datasetproperty_33.name = u'satellitenode'
    tao_datasetproperty_33.units = u''
    tao_datasetproperty_33.label = u'satelliteNode'
    tao_datasetproperty_33.dataset = tao_dataset_4
    tao_datasetproperty_33.data_type = 5L
    tao_datasetproperty_33.is_computed = False
    tao_datasetproperty_33.is_filter = True
    tao_datasetproperty_33.is_output = True
    tao_datasetproperty_33.description = u''
    tao_datasetproperty_33.group = u''
    tao_datasetproperty_33.order = 0L
    tao_datasetproperty_33.is_index = False
    tao_datasetproperty_33.is_primary = False
    tao_datasetproperty_33.flags = 3L
    tao_datasetproperty_33 = save_or_locate(tao_datasetproperty_33)

    tao_datasetproperty_34 = DataSetProperty()
    tao_datasetproperty_34.name = u'sfr'
    tao_datasetproperty_34.units = u'solMass/yr'
    tao_datasetproperty_34.label = u'sfr'
    tao_datasetproperty_34.dataset = tao_dataset_4
    tao_datasetproperty_34.data_type = 4L
    tao_datasetproperty_34.is_computed = False
    tao_datasetproperty_34.is_filter = True
    tao_datasetproperty_34.is_output = True
    tao_datasetproperty_34.description = u''
    tao_datasetproperty_34.group = u''
    tao_datasetproperty_34.order = 0L
    tao_datasetproperty_34.is_index = False
    tao_datasetproperty_34.is_primary = False
    tao_datasetproperty_34.flags = 3L
    tao_datasetproperty_34 = save_or_locate(tao_datasetproperty_34)

    tao_datasetproperty_35 = DataSetProperty()
    tao_datasetproperty_35.name = u'sfrbulge'
    tao_datasetproperty_35.units = u''
    tao_datasetproperty_35.label = u'SFR Bulge'
    tao_datasetproperty_35.dataset = tao_dataset_4
    tao_datasetproperty_35.data_type = 4L
    tao_datasetproperty_35.is_computed = False
    tao_datasetproperty_35.is_filter = True
    tao_datasetproperty_35.is_output = True
    tao_datasetproperty_35.description = u'Was interoutputspheroidstarformationrate'
    tao_datasetproperty_35.group = u''
    tao_datasetproperty_35.order = 0L
    tao_datasetproperty_35.is_index = False
    tao_datasetproperty_35.is_primary = False
    tao_datasetproperty_35.flags = 3L
    tao_datasetproperty_35 = save_or_locate(tao_datasetproperty_35)

    tao_datasetproperty_36 = DataSetProperty()
    tao_datasetproperty_36.name = u'siblingnode'
    tao_datasetproperty_36.units = u''
    tao_datasetproperty_36.label = u'siblingNode'
    tao_datasetproperty_36.dataset = tao_dataset_4
    tao_datasetproperty_36.data_type = 5L
    tao_datasetproperty_36.is_computed = False
    tao_datasetproperty_36.is_filter = True
    tao_datasetproperty_36.is_output = True
    tao_datasetproperty_36.description = u''
    tao_datasetproperty_36.group = u''
    tao_datasetproperty_36.order = 0L
    tao_datasetproperty_36.is_index = False
    tao_datasetproperty_36.is_primary = False
    tao_datasetproperty_36.flags = 3L
    tao_datasetproperty_36 = save_or_locate(tao_datasetproperty_36)

    tao_datasetproperty_37 = DataSetProperty()
    tao_datasetproperty_37.name = u'snapnum'
    tao_datasetproperty_37.units = u''
    tao_datasetproperty_37.label = u'SnapNum'
    tao_datasetproperty_37.dataset = tao_dataset_4
    tao_datasetproperty_37.data_type = 0L
    tao_datasetproperty_37.is_computed = False
    tao_datasetproperty_37.is_filter = True
    tao_datasetproperty_37.is_output = True
    tao_datasetproperty_37.description = u''
    tao_datasetproperty_37.group = u''
    tao_datasetproperty_37.order = 0L
    tao_datasetproperty_37.is_index = False
    tao_datasetproperty_37.is_primary = False
    tao_datasetproperty_37.flags = 3L
    tao_datasetproperty_37 = save_or_locate(tao_datasetproperty_37)

    tao_datasetproperty_38 = DataSetProperty()
    tao_datasetproperty_38.name = u'spheroidabundancesgasmetals'
    tao_datasetproperty_38.units = u''
    tao_datasetproperty_38.label = u'spheroidAbundancesGasMetals'
    tao_datasetproperty_38.dataset = tao_dataset_4
    tao_datasetproperty_38.data_type = 4L
    tao_datasetproperty_38.is_computed = False
    tao_datasetproperty_38.is_filter = True
    tao_datasetproperty_38.is_output = True
    tao_datasetproperty_38.description = u''
    tao_datasetproperty_38.group = u''
    tao_datasetproperty_38.order = 0L
    tao_datasetproperty_38.is_index = False
    tao_datasetproperty_38.is_primary = False
    tao_datasetproperty_38.flags = 3L
    tao_datasetproperty_38 = save_or_locate(tao_datasetproperty_38)

    tao_datasetproperty_39 = DataSetProperty()
    tao_datasetproperty_39.name = u'spheroidabundancesstellarmetals'
    tao_datasetproperty_39.units = u''
    tao_datasetproperty_39.label = u'spheroidAbundancesStellarMetals'
    tao_datasetproperty_39.dataset = tao_dataset_4
    tao_datasetproperty_39.data_type = 4L
    tao_datasetproperty_39.is_computed = False
    tao_datasetproperty_39.is_filter = True
    tao_datasetproperty_39.is_output = True
    tao_datasetproperty_39.description = u''
    tao_datasetproperty_39.group = u''
    tao_datasetproperty_39.order = 0L
    tao_datasetproperty_39.is_index = False
    tao_datasetproperty_39.is_primary = False
    tao_datasetproperty_39.flags = 3L
    tao_datasetproperty_39 = save_or_locate(tao_datasetproperty_39)

    tao_datasetproperty_40 = DataSetProperty()
    tao_datasetproperty_40.name = u'spheroidangularmomentum'
    tao_datasetproperty_40.units = u''
    tao_datasetproperty_40.label = u'spheroidAngularMomentum'
    tao_datasetproperty_40.dataset = tao_dataset_4
    tao_datasetproperty_40.data_type = 4L
    tao_datasetproperty_40.is_computed = False
    tao_datasetproperty_40.is_filter = True
    tao_datasetproperty_40.is_output = True
    tao_datasetproperty_40.description = u''
    tao_datasetproperty_40.group = u''
    tao_datasetproperty_40.order = 0L
    tao_datasetproperty_40.is_index = False
    tao_datasetproperty_40.is_primary = False
    tao_datasetproperty_40.flags = 3L
    tao_datasetproperty_40 = save_or_locate(tao_datasetproperty_40)

    tao_datasetproperty_41 = DataSetProperty()
    tao_datasetproperty_41.name = u'spheroidmassgas'
    tao_datasetproperty_41.units = u''
    tao_datasetproperty_41.label = u'spheroidMassGas'
    tao_datasetproperty_41.dataset = tao_dataset_4
    tao_datasetproperty_41.data_type = 4L
    tao_datasetproperty_41.is_computed = False
    tao_datasetproperty_41.is_filter = True
    tao_datasetproperty_41.is_output = True
    tao_datasetproperty_41.description = u''
    tao_datasetproperty_41.group = u''
    tao_datasetproperty_41.order = 0L
    tao_datasetproperty_41.is_index = False
    tao_datasetproperty_41.is_primary = False
    tao_datasetproperty_41.flags = 3L
    tao_datasetproperty_41 = save_or_locate(tao_datasetproperty_41)

    tao_datasetproperty_42 = DataSetProperty()
    tao_datasetproperty_42.name = u'spheroidmassstellar'
    tao_datasetproperty_42.units = u''
    tao_datasetproperty_42.label = u'spheroidMassStellar'
    tao_datasetproperty_42.dataset = tao_dataset_4
    tao_datasetproperty_42.data_type = 4L
    tao_datasetproperty_42.is_computed = False
    tao_datasetproperty_42.is_filter = True
    tao_datasetproperty_42.is_output = True
    tao_datasetproperty_42.description = u''
    tao_datasetproperty_42.group = u''
    tao_datasetproperty_42.order = 0L
    tao_datasetproperty_42.is_index = False
    tao_datasetproperty_42.is_primary = False
    tao_datasetproperty_42.flags = 3L
    tao_datasetproperty_42 = save_or_locate(tao_datasetproperty_42)

    tao_datasetproperty_43 = DataSetProperty()
    tao_datasetproperty_43.name = u'spheroidradius'
    tao_datasetproperty_43.units = u''
    tao_datasetproperty_43.label = u'spheroidRadius'
    tao_datasetproperty_43.dataset = tao_dataset_4
    tao_datasetproperty_43.data_type = 4L
    tao_datasetproperty_43.is_computed = False
    tao_datasetproperty_43.is_filter = True
    tao_datasetproperty_43.is_output = True
    tao_datasetproperty_43.description = u''
    tao_datasetproperty_43.group = u''
    tao_datasetproperty_43.order = 0L
    tao_datasetproperty_43.is_index = False
    tao_datasetproperty_43.is_primary = False
    tao_datasetproperty_43.flags = 3L
    tao_datasetproperty_43 = save_or_locate(tao_datasetproperty_43)

    tao_datasetproperty_44 = DataSetProperty()
    tao_datasetproperty_44.name = u'spheroidvelocity'
    tao_datasetproperty_44.units = u''
    tao_datasetproperty_44.label = u'spheroidVelocity'
    tao_datasetproperty_44.dataset = tao_dataset_4
    tao_datasetproperty_44.data_type = 4L
    tao_datasetproperty_44.is_computed = False
    tao_datasetproperty_44.is_filter = True
    tao_datasetproperty_44.is_output = True
    tao_datasetproperty_44.description = u''
    tao_datasetproperty_44.group = u''
    tao_datasetproperty_44.order = 0L
    tao_datasetproperty_44.is_index = False
    tao_datasetproperty_44.is_primary = False
    tao_datasetproperty_44.flags = 3L
    tao_datasetproperty_44 = save_or_locate(tao_datasetproperty_44)

    tao_datasetproperty_45 = DataSetProperty()
    tao_datasetproperty_45.name = u'spinspin'
    tao_datasetproperty_45.units = u''
    tao_datasetproperty_45.label = u'spinSpin'
    tao_datasetproperty_45.dataset = tao_dataset_4
    tao_datasetproperty_45.data_type = 4L
    tao_datasetproperty_45.is_computed = False
    tao_datasetproperty_45.is_filter = True
    tao_datasetproperty_45.is_output = True
    tao_datasetproperty_45.description = u''
    tao_datasetproperty_45.group = u''
    tao_datasetproperty_45.order = 0L
    tao_datasetproperty_45.is_index = False
    tao_datasetproperty_45.is_primary = False
    tao_datasetproperty_45.flags = 3L
    tao_datasetproperty_45 = save_or_locate(tao_datasetproperty_45)

    tao_datasetproperty_46 = DataSetProperty()
    tao_datasetproperty_46.name = u'treeindex'
    tao_datasetproperty_46.units = u''
    tao_datasetproperty_46.label = u'TreeIndex'
    tao_datasetproperty_46.dataset = tao_dataset_4
    tao_datasetproperty_46.data_type = 5L
    tao_datasetproperty_46.is_computed = False
    tao_datasetproperty_46.is_filter = True
    tao_datasetproperty_46.is_output = True
    tao_datasetproperty_46.description = u''
    tao_datasetproperty_46.group = u''
    tao_datasetproperty_46.order = 0L
    tao_datasetproperty_46.is_index = False
    tao_datasetproperty_46.is_primary = False
    tao_datasetproperty_46.flags = 3L
    tao_datasetproperty_46 = save_or_locate(tao_datasetproperty_46)

    tao_datasetproperty_47 = DataSetProperty()
    tao_datasetproperty_47.name = u'velx'
    tao_datasetproperty_47.units = u'km/s'
    tao_datasetproperty_47.label = u'VelX'
    tao_datasetproperty_47.dataset = tao_dataset_4
    tao_datasetproperty_47.data_type = 4L
    tao_datasetproperty_47.is_computed = False
    tao_datasetproperty_47.is_filter = True
    tao_datasetproperty_47.is_output = True
    tao_datasetproperty_47.description = u''
    tao_datasetproperty_47.group = u''
    tao_datasetproperty_47.order = 0L
    tao_datasetproperty_47.is_index = False
    tao_datasetproperty_47.is_primary = False
    tao_datasetproperty_47.flags = 3L
    tao_datasetproperty_47 = save_or_locate(tao_datasetproperty_47)

    tao_datasetproperty_48 = DataSetProperty()
    tao_datasetproperty_48.name = u'vely'
    tao_datasetproperty_48.units = u'km/s'
    tao_datasetproperty_48.label = u'VelY'
    tao_datasetproperty_48.dataset = tao_dataset_4
    tao_datasetproperty_48.data_type = 4L
    tao_datasetproperty_48.is_computed = False
    tao_datasetproperty_48.is_filter = True
    tao_datasetproperty_48.is_output = True
    tao_datasetproperty_48.description = u''
    tao_datasetproperty_48.group = u''
    tao_datasetproperty_48.order = 0L
    tao_datasetproperty_48.is_index = False
    tao_datasetproperty_48.is_primary = False
    tao_datasetproperty_48.flags = 3L
    tao_datasetproperty_48 = save_or_locate(tao_datasetproperty_48)

    tao_datasetproperty_49 = DataSetProperty()
    tao_datasetproperty_49.name = u'velz'
    tao_datasetproperty_49.units = u'km/s'
    tao_datasetproperty_49.label = u'VelZ'
    tao_datasetproperty_49.dataset = tao_dataset_4
    tao_datasetproperty_49.data_type = 4L
    tao_datasetproperty_49.is_computed = False
    tao_datasetproperty_49.is_filter = True
    tao_datasetproperty_49.is_output = True
    tao_datasetproperty_49.description = u''
    tao_datasetproperty_49.group = u''
    tao_datasetproperty_49.order = 0L
    tao_datasetproperty_49.is_index = False
    tao_datasetproperty_49.is_primary = False
    tao_datasetproperty_49.flags = 3L
    tao_datasetproperty_49 = save_or_locate(tao_datasetproperty_49)

    tao_datasetproperty_50 = DataSetProperty()
    tao_datasetproperty_50.name = u'stellarmass'
    tao_datasetproperty_50.units = u'10+10solMass/h'
    tao_datasetproperty_50.label = u'Total Stellar Mass'
    tao_datasetproperty_50.dataset = tao_dataset_4
    tao_datasetproperty_50.data_type = 1L
    tao_datasetproperty_50.is_computed = False
    tao_datasetproperty_50.is_filter = True
    tao_datasetproperty_50.is_output = True
    tao_datasetproperty_50.description = u'Total galaxy stellar mass'
    tao_datasetproperty_50.group = u'Galaxy Masses'
    tao_datasetproperty_50.order = 1L
    tao_datasetproperty_50.is_index = False
    tao_datasetproperty_50.is_primary = False
    tao_datasetproperty_50.flags = 3L
    tao_datasetproperty_50 = save_or_locate(tao_datasetproperty_50)

    tao_datasetproperty_51 = DataSetProperty()
    tao_datasetproperty_51.name = u'stellarmass'
    tao_datasetproperty_51.units = u'10+10solMass/h'
    tao_datasetproperty_51.label = u'Total Stellar Mass'
    tao_datasetproperty_51.dataset = tao_dataset_1
    tao_datasetproperty_51.data_type = 1L
    tao_datasetproperty_51.is_computed = False
    tao_datasetproperty_51.is_filter = True
    tao_datasetproperty_51.is_output = True
    tao_datasetproperty_51.description = u'Total galaxy stellar mass'
    tao_datasetproperty_51.group = u'Galaxy Masses'
    tao_datasetproperty_51.order = 1L
    tao_datasetproperty_51.is_index = False
    tao_datasetproperty_51.is_primary = False
    tao_datasetproperty_51.flags = 3L
    tao_datasetproperty_51 = save_or_locate(tao_datasetproperty_51)

    tao_datasetproperty_52 = DataSetProperty()
    tao_datasetproperty_52.name = u'stellarmass'
    tao_datasetproperty_52.units = u'10+10solMass/h'
    tao_datasetproperty_52.label = u'Total Stellar Mass'
    tao_datasetproperty_52.dataset = tao_dataset_2
    tao_datasetproperty_52.data_type = 1L
    tao_datasetproperty_52.is_computed = False
    tao_datasetproperty_52.is_filter = True
    tao_datasetproperty_52.is_output = True
    tao_datasetproperty_52.description = u'Total galaxy stellar mass'
    tao_datasetproperty_52.group = u'Galaxy Masses'
    tao_datasetproperty_52.order = 1L
    tao_datasetproperty_52.is_index = False
    tao_datasetproperty_52.is_primary = False
    tao_datasetproperty_52.flags = 3L
    tao_datasetproperty_52 = save_or_locate(tao_datasetproperty_52)

    tao_datasetproperty_53 = DataSetProperty()
    tao_datasetproperty_53.name = u'stellarmass'
    tao_datasetproperty_53.units = u'10+10solMass/h'
    tao_datasetproperty_53.label = u'Total Stellar Mass'
    tao_datasetproperty_53.dataset = tao_dataset_3
    tao_datasetproperty_53.data_type = 1L
    tao_datasetproperty_53.is_computed = False
    tao_datasetproperty_53.is_filter = True
    tao_datasetproperty_53.is_output = True
    tao_datasetproperty_53.description = u'Total galaxy stellar mass'
    tao_datasetproperty_53.group = u'Galaxy Masses'
    tao_datasetproperty_53.order = 1L
    tao_datasetproperty_53.is_index = False
    tao_datasetproperty_53.is_primary = False
    tao_datasetproperty_53.flags = 3L
    tao_datasetproperty_53 = save_or_locate(tao_datasetproperty_53)

    tao_datasetproperty_54 = DataSetProperty()
    tao_datasetproperty_54.name = u'bulgemass'
    tao_datasetproperty_54.units = u'10+10solMass/h'
    tao_datasetproperty_54.label = u'Bulge Stellar Mass'
    tao_datasetproperty_54.dataset = tao_dataset_1
    tao_datasetproperty_54.data_type = 1L
    tao_datasetproperty_54.is_computed = False
    tao_datasetproperty_54.is_filter = True
    tao_datasetproperty_54.is_output = True
    tao_datasetproperty_54.description = u'Bulge stellar mass only'
    tao_datasetproperty_54.group = u'Galaxy Masses'
    tao_datasetproperty_54.order = 2L
    tao_datasetproperty_54.is_index = False
    tao_datasetproperty_54.is_primary = False
    tao_datasetproperty_54.flags = 3L
    tao_datasetproperty_54 = save_or_locate(tao_datasetproperty_54)

    tao_datasetproperty_55 = DataSetProperty()
    tao_datasetproperty_55.name = u'bulgemass'
    tao_datasetproperty_55.units = u'10+10solMass/h'
    tao_datasetproperty_55.label = u'Bulge Stellar Mass'
    tao_datasetproperty_55.dataset = tao_dataset_2
    tao_datasetproperty_55.data_type = 1L
    tao_datasetproperty_55.is_computed = False
    tao_datasetproperty_55.is_filter = True
    tao_datasetproperty_55.is_output = True
    tao_datasetproperty_55.description = u'Bulge stellar mass only'
    tao_datasetproperty_55.group = u'Galaxy Masses'
    tao_datasetproperty_55.order = 2L
    tao_datasetproperty_55.is_index = False
    tao_datasetproperty_55.is_primary = False
    tao_datasetproperty_55.flags = 3L
    tao_datasetproperty_55 = save_or_locate(tao_datasetproperty_55)

    tao_datasetproperty_56 = DataSetProperty()
    tao_datasetproperty_56.name = u'bulgemass'
    tao_datasetproperty_56.units = u'10+10solMass/h'
    tao_datasetproperty_56.label = u'Bulge Stellar Mass'
    tao_datasetproperty_56.dataset = tao_dataset_3
    tao_datasetproperty_56.data_type = 1L
    tao_datasetproperty_56.is_computed = False
    tao_datasetproperty_56.is_filter = True
    tao_datasetproperty_56.is_output = True
    tao_datasetproperty_56.description = u'Bulge stellar mass only'
    tao_datasetproperty_56.group = u'Galaxy Masses'
    tao_datasetproperty_56.order = 2L
    tao_datasetproperty_56.is_index = False
    tao_datasetproperty_56.is_primary = False
    tao_datasetproperty_56.flags = 3L
    tao_datasetproperty_56 = save_or_locate(tao_datasetproperty_56)

    tao_datasetproperty_57 = DataSetProperty()
    tao_datasetproperty_57.name = u'blackholemass'
    tao_datasetproperty_57.units = u'10+10solMass/h'
    tao_datasetproperty_57.label = u'Black Hole Mass'
    tao_datasetproperty_57.dataset = tao_dataset_1
    tao_datasetproperty_57.data_type = 1L
    tao_datasetproperty_57.is_computed = False
    tao_datasetproperty_57.is_filter = True
    tao_datasetproperty_57.is_output = True
    tao_datasetproperty_57.description = u'Supermassive black hole mass'
    tao_datasetproperty_57.group = u'Galaxy Masses'
    tao_datasetproperty_57.order = 3L
    tao_datasetproperty_57.is_index = False
    tao_datasetproperty_57.is_primary = False
    tao_datasetproperty_57.flags = 3L
    tao_datasetproperty_57 = save_or_locate(tao_datasetproperty_57)

    tao_datasetproperty_58 = DataSetProperty()
    tao_datasetproperty_58.name = u'blackholemass'
    tao_datasetproperty_58.units = u'10+10solMass/h'
    tao_datasetproperty_58.label = u'Black Hole Mass'
    tao_datasetproperty_58.dataset = tao_dataset_2
    tao_datasetproperty_58.data_type = 1L
    tao_datasetproperty_58.is_computed = False
    tao_datasetproperty_58.is_filter = True
    tao_datasetproperty_58.is_output = True
    tao_datasetproperty_58.description = u'Supermassive black hole mass'
    tao_datasetproperty_58.group = u'Galaxy Masses'
    tao_datasetproperty_58.order = 3L
    tao_datasetproperty_58.is_index = False
    tao_datasetproperty_58.is_primary = False
    tao_datasetproperty_58.flags = 3L
    tao_datasetproperty_58 = save_or_locate(tao_datasetproperty_58)

    tao_datasetproperty_59 = DataSetProperty()
    tao_datasetproperty_59.name = u'blackholemass'
    tao_datasetproperty_59.units = u'10+10solMass/h'
    tao_datasetproperty_59.label = u'Black Hole Mass'
    tao_datasetproperty_59.dataset = tao_dataset_3
    tao_datasetproperty_59.data_type = 1L
    tao_datasetproperty_59.is_computed = False
    tao_datasetproperty_59.is_filter = True
    tao_datasetproperty_59.is_output = True
    tao_datasetproperty_59.description = u'Supermassive black hole mass'
    tao_datasetproperty_59.group = u'Galaxy Masses'
    tao_datasetproperty_59.order = 3L
    tao_datasetproperty_59.is_index = False
    tao_datasetproperty_59.is_primary = False
    tao_datasetproperty_59.flags = 3L
    tao_datasetproperty_59 = save_or_locate(tao_datasetproperty_59)

    tao_datasetproperty_60 = DataSetProperty()
    tao_datasetproperty_60.name = u'coldgas'
    tao_datasetproperty_60.units = u'10+10solMass/h'
    tao_datasetproperty_60.label = u'Cold Gas Mass'
    tao_datasetproperty_60.dataset = tao_dataset_1
    tao_datasetproperty_60.data_type = 1L
    tao_datasetproperty_60.is_computed = False
    tao_datasetproperty_60.is_filter = True
    tao_datasetproperty_60.is_output = True
    tao_datasetproperty_60.description = u'Mass of cold gas in the galaxy'
    tao_datasetproperty_60.group = u'Galaxy Masses'
    tao_datasetproperty_60.order = 4L
    tao_datasetproperty_60.is_index = False
    tao_datasetproperty_60.is_primary = False
    tao_datasetproperty_60.flags = 3L
    tao_datasetproperty_60 = save_or_locate(tao_datasetproperty_60)

    tao_datasetproperty_61 = DataSetProperty()
    tao_datasetproperty_61.name = u'coldgas'
    tao_datasetproperty_61.units = u'10+10solMass/h'
    tao_datasetproperty_61.label = u'Cold Gas Mass'
    tao_datasetproperty_61.dataset = tao_dataset_2
    tao_datasetproperty_61.data_type = 1L
    tao_datasetproperty_61.is_computed = False
    tao_datasetproperty_61.is_filter = True
    tao_datasetproperty_61.is_output = True
    tao_datasetproperty_61.description = u'Mass of cold gas in the galaxy'
    tao_datasetproperty_61.group = u'Galaxy Masses'
    tao_datasetproperty_61.order = 4L
    tao_datasetproperty_61.is_index = False
    tao_datasetproperty_61.is_primary = False
    tao_datasetproperty_61.flags = 3L
    tao_datasetproperty_61 = save_or_locate(tao_datasetproperty_61)

    tao_datasetproperty_62 = DataSetProperty()
    tao_datasetproperty_62.name = u'coldgas'
    tao_datasetproperty_62.units = u'10+10solMass/h'
    tao_datasetproperty_62.label = u'Cold Gas Mass'
    tao_datasetproperty_62.dataset = tao_dataset_3
    tao_datasetproperty_62.data_type = 1L
    tao_datasetproperty_62.is_computed = False
    tao_datasetproperty_62.is_filter = True
    tao_datasetproperty_62.is_output = True
    tao_datasetproperty_62.description = u'Mass of cold gas in the galaxy'
    tao_datasetproperty_62.group = u'Galaxy Masses'
    tao_datasetproperty_62.order = 4L
    tao_datasetproperty_62.is_index = False
    tao_datasetproperty_62.is_primary = False
    tao_datasetproperty_62.flags = 3L
    tao_datasetproperty_62 = save_or_locate(tao_datasetproperty_62)

    tao_datasetproperty_63 = DataSetProperty()
    tao_datasetproperty_63.name = u'hotgas'
    tao_datasetproperty_63.units = u'10+10solMass/h'
    tao_datasetproperty_63.label = u'Hot Gas Mass'
    tao_datasetproperty_63.dataset = tao_dataset_1
    tao_datasetproperty_63.data_type = 1L
    tao_datasetproperty_63.is_computed = False
    tao_datasetproperty_63.is_filter = True
    tao_datasetproperty_63.is_output = True
    tao_datasetproperty_63.description = u'Mass of hot halo gas'
    tao_datasetproperty_63.group = u'Galaxy Masses'
    tao_datasetproperty_63.order = 5L
    tao_datasetproperty_63.is_index = False
    tao_datasetproperty_63.is_primary = False
    tao_datasetproperty_63.flags = 3L
    tao_datasetproperty_63 = save_or_locate(tao_datasetproperty_63)

    tao_datasetproperty_64 = DataSetProperty()
    tao_datasetproperty_64.name = u'hotgas'
    tao_datasetproperty_64.units = u'10+10solMass/h'
    tao_datasetproperty_64.label = u'Hot Gas Mass'
    tao_datasetproperty_64.dataset = tao_dataset_2
    tao_datasetproperty_64.data_type = 1L
    tao_datasetproperty_64.is_computed = False
    tao_datasetproperty_64.is_filter = True
    tao_datasetproperty_64.is_output = True
    tao_datasetproperty_64.description = u'Mass of hot halo gas'
    tao_datasetproperty_64.group = u'Galaxy Masses'
    tao_datasetproperty_64.order = 5L
    tao_datasetproperty_64.is_index = False
    tao_datasetproperty_64.is_primary = False
    tao_datasetproperty_64.flags = 3L
    tao_datasetproperty_64 = save_or_locate(tao_datasetproperty_64)

    tao_datasetproperty_65 = DataSetProperty()
    tao_datasetproperty_65.name = u'hotgas'
    tao_datasetproperty_65.units = u'10+10solMass/h'
    tao_datasetproperty_65.label = u'Hot Gas Mass'
    tao_datasetproperty_65.dataset = tao_dataset_3
    tao_datasetproperty_65.data_type = 1L
    tao_datasetproperty_65.is_computed = False
    tao_datasetproperty_65.is_filter = True
    tao_datasetproperty_65.is_output = True
    tao_datasetproperty_65.description = u'Mass of hot halo gas'
    tao_datasetproperty_65.group = u'Galaxy Masses'
    tao_datasetproperty_65.order = 5L
    tao_datasetproperty_65.is_index = False
    tao_datasetproperty_65.is_primary = False
    tao_datasetproperty_65.flags = 3L
    tao_datasetproperty_65 = save_or_locate(tao_datasetproperty_65)

    tao_datasetproperty_66 = DataSetProperty()
    tao_datasetproperty_66.name = u'ejectedmass'
    tao_datasetproperty_66.units = u'10+10solMass/h'
    tao_datasetproperty_66.label = u'Ejected Gas Mass'
    tao_datasetproperty_66.dataset = tao_dataset_1
    tao_datasetproperty_66.data_type = 1L
    tao_datasetproperty_66.is_computed = False
    tao_datasetproperty_66.is_filter = True
    tao_datasetproperty_66.is_output = True
    tao_datasetproperty_66.description = u'Gas mass ejected from the halo'
    tao_datasetproperty_66.group = u'Galaxy Masses'
    tao_datasetproperty_66.order = 6L
    tao_datasetproperty_66.is_index = False
    tao_datasetproperty_66.is_primary = False
    tao_datasetproperty_66.flags = 3L
    tao_datasetproperty_66 = save_or_locate(tao_datasetproperty_66)

    tao_datasetproperty_67 = DataSetProperty()
    tao_datasetproperty_67.name = u'ejectedmass'
    tao_datasetproperty_67.units = u'10+10solMass/h'
    tao_datasetproperty_67.label = u'Ejected Gas Mass'
    tao_datasetproperty_67.dataset = tao_dataset_2
    tao_datasetproperty_67.data_type = 1L
    tao_datasetproperty_67.is_computed = False
    tao_datasetproperty_67.is_filter = True
    tao_datasetproperty_67.is_output = True
    tao_datasetproperty_67.description = u'Gas mass ejected from the halo'
    tao_datasetproperty_67.group = u'Galaxy Masses'
    tao_datasetproperty_67.order = 6L
    tao_datasetproperty_67.is_index = False
    tao_datasetproperty_67.is_primary = False
    tao_datasetproperty_67.flags = 3L
    tao_datasetproperty_67 = save_or_locate(tao_datasetproperty_67)

    tao_datasetproperty_68 = DataSetProperty()
    tao_datasetproperty_68.name = u'ejectedmass'
    tao_datasetproperty_68.units = u'10+10solMass/h'
    tao_datasetproperty_68.label = u'Ejected Gas Mass'
    tao_datasetproperty_68.dataset = tao_dataset_3
    tao_datasetproperty_68.data_type = 1L
    tao_datasetproperty_68.is_computed = False
    tao_datasetproperty_68.is_filter = True
    tao_datasetproperty_68.is_output = True
    tao_datasetproperty_68.description = u'Gas mass ejected from the halo'
    tao_datasetproperty_68.group = u'Galaxy Masses'
    tao_datasetproperty_68.order = 6L
    tao_datasetproperty_68.is_index = False
    tao_datasetproperty_68.is_primary = False
    tao_datasetproperty_68.flags = 3L
    tao_datasetproperty_68 = save_or_locate(tao_datasetproperty_68)

    tao_datasetproperty_69 = DataSetProperty()
    tao_datasetproperty_69.name = u'ics'
    tao_datasetproperty_69.units = u'10+10solMass/h'
    tao_datasetproperty_69.label = u'Intracluster Stars Mass'
    tao_datasetproperty_69.dataset = tao_dataset_1
    tao_datasetproperty_69.data_type = 1L
    tao_datasetproperty_69.is_computed = False
    tao_datasetproperty_69.is_filter = True
    tao_datasetproperty_69.is_output = True
    tao_datasetproperty_69.description = u'Stellar mass in the intracluster stars'
    tao_datasetproperty_69.group = u'Galaxy Masses'
    tao_datasetproperty_69.order = 7L
    tao_datasetproperty_69.is_index = False
    tao_datasetproperty_69.is_primary = False
    tao_datasetproperty_69.flags = 3L
    tao_datasetproperty_69 = save_or_locate(tao_datasetproperty_69)

    tao_datasetproperty_70 = DataSetProperty()
    tao_datasetproperty_70.name = u'ics'
    tao_datasetproperty_70.units = u'10+10solMass/h'
    tao_datasetproperty_70.label = u'Intracluster Stars Mass'
    tao_datasetproperty_70.dataset = tao_dataset_2
    tao_datasetproperty_70.data_type = 1L
    tao_datasetproperty_70.is_computed = False
    tao_datasetproperty_70.is_filter = True
    tao_datasetproperty_70.is_output = True
    tao_datasetproperty_70.description = u'Stellar mass in the intracluster stars'
    tao_datasetproperty_70.group = u'Galaxy Masses'
    tao_datasetproperty_70.order = 7L
    tao_datasetproperty_70.is_index = False
    tao_datasetproperty_70.is_primary = False
    tao_datasetproperty_70.flags = 3L
    tao_datasetproperty_70 = save_or_locate(tao_datasetproperty_70)

    tao_datasetproperty_71 = DataSetProperty()
    tao_datasetproperty_71.name = u'ics'
    tao_datasetproperty_71.units = u'10+10solMass/h'
    tao_datasetproperty_71.label = u'Intracluster Stars Mass'
    tao_datasetproperty_71.dataset = tao_dataset_3
    tao_datasetproperty_71.data_type = 1L
    tao_datasetproperty_71.is_computed = False
    tao_datasetproperty_71.is_filter = True
    tao_datasetproperty_71.is_output = True
    tao_datasetproperty_71.description = u'Stellar mass in the intracluster stars'
    tao_datasetproperty_71.group = u'Galaxy Masses'
    tao_datasetproperty_71.order = 7L
    tao_datasetproperty_71.is_index = False
    tao_datasetproperty_71.is_primary = False
    tao_datasetproperty_71.flags = 3L
    tao_datasetproperty_71 = save_or_locate(tao_datasetproperty_71)

    tao_datasetproperty_72 = DataSetProperty()
    tao_datasetproperty_72.name = u'metalsstellarmass'
    tao_datasetproperty_72.units = u'10+10solMass/h'
    tao_datasetproperty_72.label = u'Metals Total Stellar Mass'
    tao_datasetproperty_72.dataset = tao_dataset_1
    tao_datasetproperty_72.data_type = 1L
    tao_datasetproperty_72.is_computed = False
    tao_datasetproperty_72.is_filter = True
    tao_datasetproperty_72.is_output = True
    tao_datasetproperty_72.description = u'Mass of metals in the total stellar mass'
    tao_datasetproperty_72.group = u'Galaxy Masses'
    tao_datasetproperty_72.order = 8L
    tao_datasetproperty_72.is_index = False
    tao_datasetproperty_72.is_primary = False
    tao_datasetproperty_72.flags = 3L
    tao_datasetproperty_72 = save_or_locate(tao_datasetproperty_72)

    tao_datasetproperty_73 = DataSetProperty()
    tao_datasetproperty_73.name = u'metalsstellarmass'
    tao_datasetproperty_73.units = u'10+10solMass/h'
    tao_datasetproperty_73.label = u'Metals Total Stellar Mass'
    tao_datasetproperty_73.dataset = tao_dataset_2
    tao_datasetproperty_73.data_type = 1L
    tao_datasetproperty_73.is_computed = False
    tao_datasetproperty_73.is_filter = True
    tao_datasetproperty_73.is_output = True
    tao_datasetproperty_73.description = u'Mass of metals in the total stellar mass'
    tao_datasetproperty_73.group = u'Galaxy Masses'
    tao_datasetproperty_73.order = 8L
    tao_datasetproperty_73.is_index = False
    tao_datasetproperty_73.is_primary = False
    tao_datasetproperty_73.flags = 3L
    tao_datasetproperty_73 = save_or_locate(tao_datasetproperty_73)

    tao_datasetproperty_74 = DataSetProperty()
    tao_datasetproperty_74.name = u'metalsstellarmass'
    tao_datasetproperty_74.units = u'10+10solMass/h'
    tao_datasetproperty_74.label = u'Metals Total Stellar Mass'
    tao_datasetproperty_74.dataset = tao_dataset_3
    tao_datasetproperty_74.data_type = 1L
    tao_datasetproperty_74.is_computed = False
    tao_datasetproperty_74.is_filter = True
    tao_datasetproperty_74.is_output = True
    tao_datasetproperty_74.description = u'Mass of metals in the total stellar mass'
    tao_datasetproperty_74.group = u'Galaxy Masses'
    tao_datasetproperty_74.order = 8L
    tao_datasetproperty_74.is_index = False
    tao_datasetproperty_74.is_primary = False
    tao_datasetproperty_74.flags = 3L
    tao_datasetproperty_74 = save_or_locate(tao_datasetproperty_74)

    tao_datasetproperty_75 = DataSetProperty()
    tao_datasetproperty_75.name = u'metalsbulgemass'
    tao_datasetproperty_75.units = u'10+10solMass/h'
    tao_datasetproperty_75.label = u'Metals Bulge Mass'
    tao_datasetproperty_75.dataset = tao_dataset_1
    tao_datasetproperty_75.data_type = 1L
    tao_datasetproperty_75.is_computed = False
    tao_datasetproperty_75.is_filter = True
    tao_datasetproperty_75.is_output = True
    tao_datasetproperty_75.description = u'Mass of metals in the bulge'
    tao_datasetproperty_75.group = u'Galaxy Masses'
    tao_datasetproperty_75.order = 9L
    tao_datasetproperty_75.is_index = False
    tao_datasetproperty_75.is_primary = False
    tao_datasetproperty_75.flags = 3L
    tao_datasetproperty_75 = save_or_locate(tao_datasetproperty_75)

    tao_datasetproperty_76 = DataSetProperty()
    tao_datasetproperty_76.name = u'metalsbulgemass'
    tao_datasetproperty_76.units = u'10+10solMass/h'
    tao_datasetproperty_76.label = u'Metals Bulge Mass'
    tao_datasetproperty_76.dataset = tao_dataset_2
    tao_datasetproperty_76.data_type = 1L
    tao_datasetproperty_76.is_computed = False
    tao_datasetproperty_76.is_filter = True
    tao_datasetproperty_76.is_output = True
    tao_datasetproperty_76.description = u'Mass of metals in the bulge'
    tao_datasetproperty_76.group = u'Galaxy Masses'
    tao_datasetproperty_76.order = 9L
    tao_datasetproperty_76.is_index = False
    tao_datasetproperty_76.is_primary = False
    tao_datasetproperty_76.flags = 3L
    tao_datasetproperty_76 = save_or_locate(tao_datasetproperty_76)

    tao_datasetproperty_77 = DataSetProperty()
    tao_datasetproperty_77.name = u'metalsbulgemass'
    tao_datasetproperty_77.units = u'10+10solMass/h'
    tao_datasetproperty_77.label = u'Metals Bulge Mass'
    tao_datasetproperty_77.dataset = tao_dataset_3
    tao_datasetproperty_77.data_type = 1L
    tao_datasetproperty_77.is_computed = False
    tao_datasetproperty_77.is_filter = True
    tao_datasetproperty_77.is_output = True
    tao_datasetproperty_77.description = u'Mass of metals in the bulge'
    tao_datasetproperty_77.group = u'Galaxy Masses'
    tao_datasetproperty_77.order = 9L
    tao_datasetproperty_77.is_index = False
    tao_datasetproperty_77.is_primary = False
    tao_datasetproperty_77.flags = 3L
    tao_datasetproperty_77 = save_or_locate(tao_datasetproperty_77)

    tao_datasetproperty_78 = DataSetProperty()
    tao_datasetproperty_78.name = u'metalscoldgas'
    tao_datasetproperty_78.units = u'10+10solMass/h'
    tao_datasetproperty_78.label = u'Metals Cold Gas Mass'
    tao_datasetproperty_78.dataset = tao_dataset_1
    tao_datasetproperty_78.data_type = 1L
    tao_datasetproperty_78.is_computed = False
    tao_datasetproperty_78.is_filter = True
    tao_datasetproperty_78.is_output = True
    tao_datasetproperty_78.description = u'Mass of metals in the cold gas'
    tao_datasetproperty_78.group = u'Galaxy Masses'
    tao_datasetproperty_78.order = 10L
    tao_datasetproperty_78.is_index = False
    tao_datasetproperty_78.is_primary = False
    tao_datasetproperty_78.flags = 3L
    tao_datasetproperty_78 = save_or_locate(tao_datasetproperty_78)

    tao_datasetproperty_79 = DataSetProperty()
    tao_datasetproperty_79.name = u'metalscoldgas'
    tao_datasetproperty_79.units = u'10+10solMass/h'
    tao_datasetproperty_79.label = u'Metals Cold Gas Mass'
    tao_datasetproperty_79.dataset = tao_dataset_2
    tao_datasetproperty_79.data_type = 1L
    tao_datasetproperty_79.is_computed = False
    tao_datasetproperty_79.is_filter = True
    tao_datasetproperty_79.is_output = True
    tao_datasetproperty_79.description = u'Mass of metals in the cold gas'
    tao_datasetproperty_79.group = u'Galaxy Masses'
    tao_datasetproperty_79.order = 10L
    tao_datasetproperty_79.is_index = False
    tao_datasetproperty_79.is_primary = False
    tao_datasetproperty_79.flags = 3L
    tao_datasetproperty_79 = save_or_locate(tao_datasetproperty_79)

    tao_datasetproperty_80 = DataSetProperty()
    tao_datasetproperty_80.name = u'metalscoldgas'
    tao_datasetproperty_80.units = u'10+10solMass/h'
    tao_datasetproperty_80.label = u'Metals Cold Gas Mass'
    tao_datasetproperty_80.dataset = tao_dataset_3
    tao_datasetproperty_80.data_type = 1L
    tao_datasetproperty_80.is_computed = False
    tao_datasetproperty_80.is_filter = True
    tao_datasetproperty_80.is_output = True
    tao_datasetproperty_80.description = u'Mass of metals in the cold gas'
    tao_datasetproperty_80.group = u'Galaxy Masses'
    tao_datasetproperty_80.order = 10L
    tao_datasetproperty_80.is_index = False
    tao_datasetproperty_80.is_primary = False
    tao_datasetproperty_80.flags = 3L
    tao_datasetproperty_80 = save_or_locate(tao_datasetproperty_80)

    tao_datasetproperty_81 = DataSetProperty()
    tao_datasetproperty_81.name = u'metalshotgas'
    tao_datasetproperty_81.units = u'10+10solMass/h'
    tao_datasetproperty_81.label = u'Metals Hot Gas Mass'
    tao_datasetproperty_81.dataset = tao_dataset_1
    tao_datasetproperty_81.data_type = 1L
    tao_datasetproperty_81.is_computed = False
    tao_datasetproperty_81.is_filter = True
    tao_datasetproperty_81.is_output = True
    tao_datasetproperty_81.description = u'Mass of metals in the hot gas'
    tao_datasetproperty_81.group = u'Galaxy Masses'
    tao_datasetproperty_81.order = 11L
    tao_datasetproperty_81.is_index = False
    tao_datasetproperty_81.is_primary = False
    tao_datasetproperty_81.flags = 3L
    tao_datasetproperty_81 = save_or_locate(tao_datasetproperty_81)

    tao_datasetproperty_82 = DataSetProperty()
    tao_datasetproperty_82.name = u'metalshotgas'
    tao_datasetproperty_82.units = u'10+10solMass/h'
    tao_datasetproperty_82.label = u'Metals Hot Gas Mass'
    tao_datasetproperty_82.dataset = tao_dataset_2
    tao_datasetproperty_82.data_type = 1L
    tao_datasetproperty_82.is_computed = False
    tao_datasetproperty_82.is_filter = True
    tao_datasetproperty_82.is_output = True
    tao_datasetproperty_82.description = u'Mass of metals in the hot gas'
    tao_datasetproperty_82.group = u'Galaxy Masses'
    tao_datasetproperty_82.order = 11L
    tao_datasetproperty_82.is_index = False
    tao_datasetproperty_82.is_primary = False
    tao_datasetproperty_82.flags = 3L
    tao_datasetproperty_82 = save_or_locate(tao_datasetproperty_82)

    tao_datasetproperty_83 = DataSetProperty()
    tao_datasetproperty_83.name = u'metalshotgas'
    tao_datasetproperty_83.units = u'10+10solMass/h'
    tao_datasetproperty_83.label = u'Metals Hot Gas Mass'
    tao_datasetproperty_83.dataset = tao_dataset_3
    tao_datasetproperty_83.data_type = 1L
    tao_datasetproperty_83.is_computed = False
    tao_datasetproperty_83.is_filter = True
    tao_datasetproperty_83.is_output = True
    tao_datasetproperty_83.description = u'Mass of metals in the hot gas'
    tao_datasetproperty_83.group = u'Galaxy Masses'
    tao_datasetproperty_83.order = 11L
    tao_datasetproperty_83.is_index = False
    tao_datasetproperty_83.is_primary = False
    tao_datasetproperty_83.flags = 3L
    tao_datasetproperty_83 = save_or_locate(tao_datasetproperty_83)

    tao_datasetproperty_84 = DataSetProperty()
    tao_datasetproperty_84.name = u'metalsejectedmass'
    tao_datasetproperty_84.units = u'10+10solMass/h'
    tao_datasetproperty_84.label = u'Metals Ejected Gas Mass'
    tao_datasetproperty_84.dataset = tao_dataset_1
    tao_datasetproperty_84.data_type = 1L
    tao_datasetproperty_84.is_computed = False
    tao_datasetproperty_84.is_filter = True
    tao_datasetproperty_84.is_output = True
    tao_datasetproperty_84.description = u'Mass of metals in the ejected gas'
    tao_datasetproperty_84.group = u'Galaxy Masses'
    tao_datasetproperty_84.order = 12L
    tao_datasetproperty_84.is_index = False
    tao_datasetproperty_84.is_primary = False
    tao_datasetproperty_84.flags = 3L
    tao_datasetproperty_84 = save_or_locate(tao_datasetproperty_84)

    tao_datasetproperty_85 = DataSetProperty()
    tao_datasetproperty_85.name = u'metalsejectedmass'
    tao_datasetproperty_85.units = u'10+10solMass/h'
    tao_datasetproperty_85.label = u'Metals Ejected Gas Mass'
    tao_datasetproperty_85.dataset = tao_dataset_2
    tao_datasetproperty_85.data_type = 1L
    tao_datasetproperty_85.is_computed = False
    tao_datasetproperty_85.is_filter = True
    tao_datasetproperty_85.is_output = True
    tao_datasetproperty_85.description = u'Mass of metals in the ejected gas'
    tao_datasetproperty_85.group = u'Galaxy Masses'
    tao_datasetproperty_85.order = 12L
    tao_datasetproperty_85.is_index = False
    tao_datasetproperty_85.is_primary = False
    tao_datasetproperty_85.flags = 3L
    tao_datasetproperty_85 = save_or_locate(tao_datasetproperty_85)

    tao_datasetproperty_86 = DataSetProperty()
    tao_datasetproperty_86.name = u'metalsejectedmass'
    tao_datasetproperty_86.units = u'10+10solMass/h'
    tao_datasetproperty_86.label = u'Metals Ejected Gas Mass'
    tao_datasetproperty_86.dataset = tao_dataset_3
    tao_datasetproperty_86.data_type = 1L
    tao_datasetproperty_86.is_computed = False
    tao_datasetproperty_86.is_filter = True
    tao_datasetproperty_86.is_output = True
    tao_datasetproperty_86.description = u'Mass of metals in the ejected gas'
    tao_datasetproperty_86.group = u'Galaxy Masses'
    tao_datasetproperty_86.order = 12L
    tao_datasetproperty_86.is_index = False
    tao_datasetproperty_86.is_primary = False
    tao_datasetproperty_86.flags = 3L
    tao_datasetproperty_86 = save_or_locate(tao_datasetproperty_86)

    tao_datasetproperty_87 = DataSetProperty()
    tao_datasetproperty_87.name = u'metalsics'
    tao_datasetproperty_87.units = u'10+10solMass/h'
    tao_datasetproperty_87.label = u'Metals Intracluster Stars Mass'
    tao_datasetproperty_87.dataset = tao_dataset_1
    tao_datasetproperty_87.data_type = 1L
    tao_datasetproperty_87.is_computed = False
    tao_datasetproperty_87.is_filter = True
    tao_datasetproperty_87.is_output = True
    tao_datasetproperty_87.description = u'Mass of metals in the intracluster stars'
    tao_datasetproperty_87.group = u'Galaxy Masses'
    tao_datasetproperty_87.order = 13L
    tao_datasetproperty_87.is_index = False
    tao_datasetproperty_87.is_primary = False
    tao_datasetproperty_87.flags = 3L
    tao_datasetproperty_87 = save_or_locate(tao_datasetproperty_87)

    tao_datasetproperty_88 = DataSetProperty()
    tao_datasetproperty_88.name = u'metalsics'
    tao_datasetproperty_88.units = u'10+10solMass/h'
    tao_datasetproperty_88.label = u'Metals Intracluster Stars Mass'
    tao_datasetproperty_88.dataset = tao_dataset_2
    tao_datasetproperty_88.data_type = 1L
    tao_datasetproperty_88.is_computed = False
    tao_datasetproperty_88.is_filter = True
    tao_datasetproperty_88.is_output = True
    tao_datasetproperty_88.description = u'Mass of metals in the intracluster stars'
    tao_datasetproperty_88.group = u'Galaxy Masses'
    tao_datasetproperty_88.order = 13L
    tao_datasetproperty_88.is_index = False
    tao_datasetproperty_88.is_primary = False
    tao_datasetproperty_88.flags = 3L
    tao_datasetproperty_88 = save_or_locate(tao_datasetproperty_88)

    tao_datasetproperty_89 = DataSetProperty()
    tao_datasetproperty_89.name = u'metalsics'
    tao_datasetproperty_89.units = u'10+10solMass/h'
    tao_datasetproperty_89.label = u'Metals Intracluster Stars Mass'
    tao_datasetproperty_89.dataset = tao_dataset_3
    tao_datasetproperty_89.data_type = 1L
    tao_datasetproperty_89.is_computed = False
    tao_datasetproperty_89.is_filter = True
    tao_datasetproperty_89.is_output = True
    tao_datasetproperty_89.description = u'Mass of metals in the intracluster stars'
    tao_datasetproperty_89.group = u'Galaxy Masses'
    tao_datasetproperty_89.order = 13L
    tao_datasetproperty_89.is_index = False
    tao_datasetproperty_89.is_primary = False
    tao_datasetproperty_89.flags = 3L
    tao_datasetproperty_89 = save_or_locate(tao_datasetproperty_89)

    tao_datasetproperty_90 = DataSetProperty()
    tao_datasetproperty_90.name = u'objecttype'
    tao_datasetproperty_90.units = u''
    tao_datasetproperty_90.label = u'Galaxy Classification'
    tao_datasetproperty_90.dataset = tao_dataset_1
    tao_datasetproperty_90.data_type = 0L
    tao_datasetproperty_90.is_computed = False
    tao_datasetproperty_90.is_filter = False
    tao_datasetproperty_90.is_output = True
    tao_datasetproperty_90.description = u'Galaxy classification: 0=central, 1=Satellite'
    tao_datasetproperty_90.group = u'Galaxy Properties'
    tao_datasetproperty_90.order = 1L
    tao_datasetproperty_90.is_index = False
    tao_datasetproperty_90.is_primary = False
    tao_datasetproperty_90.flags = 3L
    tao_datasetproperty_90 = save_or_locate(tao_datasetproperty_90)

    tao_datasetproperty_91 = DataSetProperty()
    tao_datasetproperty_91.name = u'objecttype'
    tao_datasetproperty_91.units = u''
    tao_datasetproperty_91.label = u'Galaxy Classification'
    tao_datasetproperty_91.dataset = tao_dataset_2
    tao_datasetproperty_91.data_type = 0L
    tao_datasetproperty_91.is_computed = False
    tao_datasetproperty_91.is_filter = False
    tao_datasetproperty_91.is_output = True
    tao_datasetproperty_91.description = u'Galaxy classification: 0=central, 1=Satellite'
    tao_datasetproperty_91.group = u'Galaxy Properties'
    tao_datasetproperty_91.order = 1L
    tao_datasetproperty_91.is_index = False
    tao_datasetproperty_91.is_primary = False
    tao_datasetproperty_91.flags = 3L
    tao_datasetproperty_91 = save_or_locate(tao_datasetproperty_91)

    tao_datasetproperty_92 = DataSetProperty()
    tao_datasetproperty_92.name = u'objecttype'
    tao_datasetproperty_92.units = u''
    tao_datasetproperty_92.label = u'Galaxy Classification'
    tao_datasetproperty_92.dataset = tao_dataset_3
    tao_datasetproperty_92.data_type = 0L
    tao_datasetproperty_92.is_computed = False
    tao_datasetproperty_92.is_filter = False
    tao_datasetproperty_92.is_output = True
    tao_datasetproperty_92.description = u'Galaxy classification: 0=central, 1=Satellite'
    tao_datasetproperty_92.group = u'Galaxy Properties'
    tao_datasetproperty_92.order = 1L
    tao_datasetproperty_92.is_index = False
    tao_datasetproperty_92.is_primary = False
    tao_datasetproperty_92.flags = 3L
    tao_datasetproperty_92 = save_or_locate(tao_datasetproperty_92)

    tao_datasetproperty_93 = DataSetProperty()
    tao_datasetproperty_93.name = u'diskscaleradius'
    tao_datasetproperty_93.units = u'10+6pc/h'
    tao_datasetproperty_93.label = u'Disk Scale Radius'
    tao_datasetproperty_93.dataset = tao_dataset_1
    tao_datasetproperty_93.data_type = 1L
    tao_datasetproperty_93.is_computed = False
    tao_datasetproperty_93.is_filter = True
    tao_datasetproperty_93.is_output = True
    tao_datasetproperty_93.description = u'Stellar disk scale radius'
    tao_datasetproperty_93.group = u'Galaxy Properties'
    tao_datasetproperty_93.order = 2L
    tao_datasetproperty_93.is_index = False
    tao_datasetproperty_93.is_primary = False
    tao_datasetproperty_93.flags = 3L
    tao_datasetproperty_93 = save_or_locate(tao_datasetproperty_93)

    tao_datasetproperty_94 = DataSetProperty()
    tao_datasetproperty_94.name = u'diskscaleradius'
    tao_datasetproperty_94.units = u'10+6pc/h'
    tao_datasetproperty_94.label = u'Disk Scale Radius'
    tao_datasetproperty_94.dataset = tao_dataset_2
    tao_datasetproperty_94.data_type = 1L
    tao_datasetproperty_94.is_computed = False
    tao_datasetproperty_94.is_filter = True
    tao_datasetproperty_94.is_output = True
    tao_datasetproperty_94.description = u'Stellar disk scale radius'
    tao_datasetproperty_94.group = u'Galaxy Properties'
    tao_datasetproperty_94.order = 2L
    tao_datasetproperty_94.is_index = False
    tao_datasetproperty_94.is_primary = False
    tao_datasetproperty_94.flags = 3L
    tao_datasetproperty_94 = save_or_locate(tao_datasetproperty_94)

    tao_datasetproperty_95 = DataSetProperty()
    tao_datasetproperty_95.name = u'diskscaleradius'
    tao_datasetproperty_95.units = u'10+6pc/h'
    tao_datasetproperty_95.label = u'Disk Scale Radius'
    tao_datasetproperty_95.dataset = tao_dataset_3
    tao_datasetproperty_95.data_type = 1L
    tao_datasetproperty_95.is_computed = False
    tao_datasetproperty_95.is_filter = True
    tao_datasetproperty_95.is_output = True
    tao_datasetproperty_95.description = u'Stellar disk scale radius'
    tao_datasetproperty_95.group = u'Galaxy Properties'
    tao_datasetproperty_95.order = 2L
    tao_datasetproperty_95.is_index = False
    tao_datasetproperty_95.is_primary = False
    tao_datasetproperty_95.flags = 3L
    tao_datasetproperty_95 = save_or_locate(tao_datasetproperty_95)

    tao_datasetproperty_96 = DataSetProperty()
    tao_datasetproperty_96.name = u'sfr'
    tao_datasetproperty_96.units = u'solMass/yr'
    tao_datasetproperty_96.label = u'Total Star Formation Rate'
    tao_datasetproperty_96.dataset = tao_dataset_1
    tao_datasetproperty_96.data_type = 1L
    tao_datasetproperty_96.is_computed = False
    tao_datasetproperty_96.is_filter = True
    tao_datasetproperty_96.is_output = True
    tao_datasetproperty_96.description = u'Total star formation rate in the galaxy'
    tao_datasetproperty_96.group = u'Galaxy Properties'
    tao_datasetproperty_96.order = 3L
    tao_datasetproperty_96.is_index = False
    tao_datasetproperty_96.is_primary = False
    tao_datasetproperty_96.flags = 3L
    tao_datasetproperty_96 = save_or_locate(tao_datasetproperty_96)

    tao_datasetproperty_97 = DataSetProperty()
    tao_datasetproperty_97.name = u'sfr'
    tao_datasetproperty_97.units = u'solMass/yr'
    tao_datasetproperty_97.label = u'Total Star Formation Rate'
    tao_datasetproperty_97.dataset = tao_dataset_2
    tao_datasetproperty_97.data_type = 1L
    tao_datasetproperty_97.is_computed = False
    tao_datasetproperty_97.is_filter = True
    tao_datasetproperty_97.is_output = True
    tao_datasetproperty_97.description = u'Total star formation rate in the galaxy'
    tao_datasetproperty_97.group = u'Galaxy Properties'
    tao_datasetproperty_97.order = 3L
    tao_datasetproperty_97.is_index = False
    tao_datasetproperty_97.is_primary = False
    tao_datasetproperty_97.flags = 3L
    tao_datasetproperty_97 = save_or_locate(tao_datasetproperty_97)

    tao_datasetproperty_98 = DataSetProperty()
    tao_datasetproperty_98.name = u'sfr'
    tao_datasetproperty_98.units = u'solMass/yr'
    tao_datasetproperty_98.label = u'Total Star Formation Rate'
    tao_datasetproperty_98.dataset = tao_dataset_3
    tao_datasetproperty_98.data_type = 1L
    tao_datasetproperty_98.is_computed = False
    tao_datasetproperty_98.is_filter = True
    tao_datasetproperty_98.is_output = True
    tao_datasetproperty_98.description = u'Total star formation rate in the galaxy'
    tao_datasetproperty_98.group = u'Galaxy Properties'
    tao_datasetproperty_98.order = 3L
    tao_datasetproperty_98.is_index = False
    tao_datasetproperty_98.is_primary = False
    tao_datasetproperty_98.flags = 3L
    tao_datasetproperty_98 = save_or_locate(tao_datasetproperty_98)

    tao_datasetproperty_99 = DataSetProperty()
    tao_datasetproperty_99.name = u'sfrbulge'
    tao_datasetproperty_99.units = u'solMass/yr'
    tao_datasetproperty_99.label = u'Bulge Star Formation Rate'
    tao_datasetproperty_99.dataset = tao_dataset_1
    tao_datasetproperty_99.data_type = 1L
    tao_datasetproperty_99.is_computed = False
    tao_datasetproperty_99.is_filter = True
    tao_datasetproperty_99.is_output = True
    tao_datasetproperty_99.description = u'Star formation rate in the bulge only'
    tao_datasetproperty_99.group = u'Galaxy Properties'
    tao_datasetproperty_99.order = 4L
    tao_datasetproperty_99.is_index = False
    tao_datasetproperty_99.is_primary = False
    tao_datasetproperty_99.flags = 3L
    tao_datasetproperty_99 = save_or_locate(tao_datasetproperty_99)

    tao_datasetproperty_100 = DataSetProperty()
    tao_datasetproperty_100.name = u'sfrbulge'
    tao_datasetproperty_100.units = u'solMass/yr'
    tao_datasetproperty_100.label = u'Bulge Star Formation Rate'
    tao_datasetproperty_100.dataset = tao_dataset_2
    tao_datasetproperty_100.data_type = 1L
    tao_datasetproperty_100.is_computed = False
    tao_datasetproperty_100.is_filter = True
    tao_datasetproperty_100.is_output = True
    tao_datasetproperty_100.description = u'Star formation rate in the bulge only'
    tao_datasetproperty_100.group = u'Galaxy Properties'
    tao_datasetproperty_100.order = 4L
    tao_datasetproperty_100.is_index = False
    tao_datasetproperty_100.is_primary = False
    tao_datasetproperty_100.flags = 3L
    tao_datasetproperty_100 = save_or_locate(tao_datasetproperty_100)

    tao_datasetproperty_101 = DataSetProperty()
    tao_datasetproperty_101.name = u'sfrbulge'
    tao_datasetproperty_101.units = u'solMass/yr'
    tao_datasetproperty_101.label = u'Bulge Star Formation Rate'
    tao_datasetproperty_101.dataset = tao_dataset_3
    tao_datasetproperty_101.data_type = 1L
    tao_datasetproperty_101.is_computed = False
    tao_datasetproperty_101.is_filter = True
    tao_datasetproperty_101.is_output = True
    tao_datasetproperty_101.description = u'Star formation rate in the bulge only'
    tao_datasetproperty_101.group = u'Galaxy Properties'
    tao_datasetproperty_101.order = 4L
    tao_datasetproperty_101.is_index = False
    tao_datasetproperty_101.is_primary = False
    tao_datasetproperty_101.flags = 3L
    tao_datasetproperty_101 = save_or_locate(tao_datasetproperty_101)

    tao_datasetproperty_102 = DataSetProperty()
    tao_datasetproperty_102.name = u'sfrics'
    tao_datasetproperty_102.units = u'solMass/yr'
    tao_datasetproperty_102.label = u'Intracluster Stars Star Formation Rate'
    tao_datasetproperty_102.dataset = tao_dataset_1
    tao_datasetproperty_102.data_type = 1L
    tao_datasetproperty_102.is_computed = False
    tao_datasetproperty_102.is_filter = True
    tao_datasetproperty_102.is_output = True
    tao_datasetproperty_102.description = u'Star formation rate in the intracluster stars'
    tao_datasetproperty_102.group = u'Galaxy Properties'
    tao_datasetproperty_102.order = 5L
    tao_datasetproperty_102.is_index = False
    tao_datasetproperty_102.is_primary = False
    tao_datasetproperty_102.flags = 3L
    tao_datasetproperty_102 = save_or_locate(tao_datasetproperty_102)

    tao_datasetproperty_103 = DataSetProperty()
    tao_datasetproperty_103.name = u'sfrics'
    tao_datasetproperty_103.units = u'solMass/yr'
    tao_datasetproperty_103.label = u'Intracluster Stars Star Formation Rate'
    tao_datasetproperty_103.dataset = tao_dataset_2
    tao_datasetproperty_103.data_type = 1L
    tao_datasetproperty_103.is_computed = False
    tao_datasetproperty_103.is_filter = True
    tao_datasetproperty_103.is_output = True
    tao_datasetproperty_103.description = u'Star formation rate in the intracluster stars'
    tao_datasetproperty_103.group = u'Galaxy Properties'
    tao_datasetproperty_103.order = 5L
    tao_datasetproperty_103.is_index = False
    tao_datasetproperty_103.is_primary = False
    tao_datasetproperty_103.flags = 3L
    tao_datasetproperty_103 = save_or_locate(tao_datasetproperty_103)

    tao_datasetproperty_104 = DataSetProperty()
    tao_datasetproperty_104.name = u'sfrics'
    tao_datasetproperty_104.units = u'solMass/yr'
    tao_datasetproperty_104.label = u'Intracluster Stars Star Formation Rate'
    tao_datasetproperty_104.dataset = tao_dataset_3
    tao_datasetproperty_104.data_type = 1L
    tao_datasetproperty_104.is_computed = False
    tao_datasetproperty_104.is_filter = True
    tao_datasetproperty_104.is_output = True
    tao_datasetproperty_104.description = u'Star formation rate in the intracluster stars'
    tao_datasetproperty_104.group = u'Galaxy Properties'
    tao_datasetproperty_104.order = 5L
    tao_datasetproperty_104.is_index = False
    tao_datasetproperty_104.is_primary = False
    tao_datasetproperty_104.flags = 3L
    tao_datasetproperty_104 = save_or_locate(tao_datasetproperty_104)

    tao_datasetproperty_105 = DataSetProperty()
    tao_datasetproperty_105.name = u'cooling'
    tao_datasetproperty_105.units = u'log(10-7J/s)'
    tao_datasetproperty_105.label = u'Hot Gas Cooling Rate'
    tao_datasetproperty_105.dataset = tao_dataset_1
    tao_datasetproperty_105.data_type = 1L
    tao_datasetproperty_105.is_computed = False
    tao_datasetproperty_105.is_filter = True
    tao_datasetproperty_105.is_output = True
    tao_datasetproperty_105.description = u'Cooling rate of hot halo gas'
    tao_datasetproperty_105.group = u'Galaxy Properties'
    tao_datasetproperty_105.order = 6L
    tao_datasetproperty_105.is_index = False
    tao_datasetproperty_105.is_primary = False
    tao_datasetproperty_105.flags = 3L
    tao_datasetproperty_105 = save_or_locate(tao_datasetproperty_105)

    tao_datasetproperty_106 = DataSetProperty()
    tao_datasetproperty_106.name = u'cooling'
    tao_datasetproperty_106.units = u'log(10-7J/s)'
    tao_datasetproperty_106.label = u'Hot Gas Cooling Rate'
    tao_datasetproperty_106.dataset = tao_dataset_2
    tao_datasetproperty_106.data_type = 1L
    tao_datasetproperty_106.is_computed = False
    tao_datasetproperty_106.is_filter = True
    tao_datasetproperty_106.is_output = True
    tao_datasetproperty_106.description = u'Cooling rate of hot halo gas'
    tao_datasetproperty_106.group = u'Galaxy Properties'
    tao_datasetproperty_106.order = 6L
    tao_datasetproperty_106.is_index = False
    tao_datasetproperty_106.is_primary = False
    tao_datasetproperty_106.flags = 3L
    tao_datasetproperty_106 = save_or_locate(tao_datasetproperty_106)

    tao_datasetproperty_107 = DataSetProperty()
    tao_datasetproperty_107.name = u'cooling'
    tao_datasetproperty_107.units = u'log(10-7J/s)'
    tao_datasetproperty_107.label = u'Hot Gas Cooling Rate'
    tao_datasetproperty_107.dataset = tao_dataset_3
    tao_datasetproperty_107.data_type = 1L
    tao_datasetproperty_107.is_computed = False
    tao_datasetproperty_107.is_filter = True
    tao_datasetproperty_107.is_output = True
    tao_datasetproperty_107.description = u'Cooling rate of hot halo gas'
    tao_datasetproperty_107.group = u'Galaxy Properties'
    tao_datasetproperty_107.order = 6L
    tao_datasetproperty_107.is_index = False
    tao_datasetproperty_107.is_primary = False
    tao_datasetproperty_107.flags = 3L
    tao_datasetproperty_107 = save_or_locate(tao_datasetproperty_107)

    tao_datasetproperty_108 = DataSetProperty()
    tao_datasetproperty_108.name = u'heating'
    tao_datasetproperty_108.units = u'log(10-7J/s)'
    tao_datasetproperty_108.label = u'AGN Heating Rate'
    tao_datasetproperty_108.dataset = tao_dataset_1
    tao_datasetproperty_108.data_type = 1L
    tao_datasetproperty_108.is_computed = False
    tao_datasetproperty_108.is_filter = True
    tao_datasetproperty_108.is_output = True
    tao_datasetproperty_108.description = u'AGN radio-mode heating rate'
    tao_datasetproperty_108.group = u'Galaxy Properties'
    tao_datasetproperty_108.order = 7L
    tao_datasetproperty_108.is_index = False
    tao_datasetproperty_108.is_primary = False
    tao_datasetproperty_108.flags = 3L
    tao_datasetproperty_108 = save_or_locate(tao_datasetproperty_108)

    tao_datasetproperty_109 = DataSetProperty()
    tao_datasetproperty_109.name = u'heating'
    tao_datasetproperty_109.units = u'log(10-7J/s)'
    tao_datasetproperty_109.label = u'AGN Heating Rate'
    tao_datasetproperty_109.dataset = tao_dataset_2
    tao_datasetproperty_109.data_type = 1L
    tao_datasetproperty_109.is_computed = False
    tao_datasetproperty_109.is_filter = True
    tao_datasetproperty_109.is_output = True
    tao_datasetproperty_109.description = u'AGN radio-mode heating rate'
    tao_datasetproperty_109.group = u'Galaxy Properties'
    tao_datasetproperty_109.order = 7L
    tao_datasetproperty_109.is_index = False
    tao_datasetproperty_109.is_primary = False
    tao_datasetproperty_109.flags = 3L
    tao_datasetproperty_109 = save_or_locate(tao_datasetproperty_109)

    tao_datasetproperty_110 = DataSetProperty()
    tao_datasetproperty_110.name = u'heating'
    tao_datasetproperty_110.units = u'log(10-7J/s)'
    tao_datasetproperty_110.label = u'AGN Heating Rate'
    tao_datasetproperty_110.dataset = tao_dataset_3
    tao_datasetproperty_110.data_type = 1L
    tao_datasetproperty_110.is_computed = False
    tao_datasetproperty_110.is_filter = True
    tao_datasetproperty_110.is_output = True
    tao_datasetproperty_110.description = u'AGN radio-mode heating rate'
    tao_datasetproperty_110.group = u'Galaxy Properties'
    tao_datasetproperty_110.order = 7L
    tao_datasetproperty_110.is_index = False
    tao_datasetproperty_110.is_primary = False
    tao_datasetproperty_110.flags = 3L
    tao_datasetproperty_110 = save_or_locate(tao_datasetproperty_110)

    tao_datasetproperty_111 = DataSetProperty()
    tao_datasetproperty_111.name = u'mvir'
    tao_datasetproperty_111.units = u'10+10solMass/h'
    tao_datasetproperty_111.label = u'Mvir'
    tao_datasetproperty_111.dataset = tao_dataset_1
    tao_datasetproperty_111.data_type = 1L
    tao_datasetproperty_111.is_computed = False
    tao_datasetproperty_111.is_filter = True
    tao_datasetproperty_111.is_output = True
    tao_datasetproperty_111.description = u'Dark matter (sub)halo virial mass'
    tao_datasetproperty_111.group = u'Halo Properties'
    tao_datasetproperty_111.order = 1L
    tao_datasetproperty_111.is_index = False
    tao_datasetproperty_111.is_primary = False
    tao_datasetproperty_111.flags = 3L
    tao_datasetproperty_111 = save_or_locate(tao_datasetproperty_111)

    tao_datasetproperty_112 = DataSetProperty()
    tao_datasetproperty_112.name = u'mvir'
    tao_datasetproperty_112.units = u'10+10solMass/h'
    tao_datasetproperty_112.label = u'Mvir'
    tao_datasetproperty_112.dataset = tao_dataset_2
    tao_datasetproperty_112.data_type = 1L
    tao_datasetproperty_112.is_computed = False
    tao_datasetproperty_112.is_filter = True
    tao_datasetproperty_112.is_output = True
    tao_datasetproperty_112.description = u'Dark matter (sub)halo virial mass'
    tao_datasetproperty_112.group = u'Halo Properties'
    tao_datasetproperty_112.order = 1L
    tao_datasetproperty_112.is_index = False
    tao_datasetproperty_112.is_primary = False
    tao_datasetproperty_112.flags = 3L
    tao_datasetproperty_112 = save_or_locate(tao_datasetproperty_112)

    tao_datasetproperty_113 = DataSetProperty()
    tao_datasetproperty_113.name = u'mvir'
    tao_datasetproperty_113.units = u'10+10solMass/h'
    tao_datasetproperty_113.label = u'Mvir'
    tao_datasetproperty_113.dataset = tao_dataset_3
    tao_datasetproperty_113.data_type = 1L
    tao_datasetproperty_113.is_computed = False
    tao_datasetproperty_113.is_filter = True
    tao_datasetproperty_113.is_output = True
    tao_datasetproperty_113.description = u'Dark matter (sub)halo virial mass'
    tao_datasetproperty_113.group = u'Halo Properties'
    tao_datasetproperty_113.order = 1L
    tao_datasetproperty_113.is_index = False
    tao_datasetproperty_113.is_primary = False
    tao_datasetproperty_113.flags = 3L
    tao_datasetproperty_113 = save_or_locate(tao_datasetproperty_113)

    tao_datasetproperty_114 = DataSetProperty()
    tao_datasetproperty_114.name = u'rvir'
    tao_datasetproperty_114.units = u'10+6pc/h'
    tao_datasetproperty_114.label = u'Rvir'
    tao_datasetproperty_114.dataset = tao_dataset_1
    tao_datasetproperty_114.data_type = 1L
    tao_datasetproperty_114.is_computed = False
    tao_datasetproperty_114.is_filter = True
    tao_datasetproperty_114.is_output = True
    tao_datasetproperty_114.description = u'Dark matter (sub)halo virial radius'
    tao_datasetproperty_114.group = u'Halo Properties'
    tao_datasetproperty_114.order = 2L
    tao_datasetproperty_114.is_index = False
    tao_datasetproperty_114.is_primary = False
    tao_datasetproperty_114.flags = 3L
    tao_datasetproperty_114 = save_or_locate(tao_datasetproperty_114)

    tao_datasetproperty_115 = DataSetProperty()
    tao_datasetproperty_115.name = u'rvir'
    tao_datasetproperty_115.units = u'10+6pc/h'
    tao_datasetproperty_115.label = u'Rvir'
    tao_datasetproperty_115.dataset = tao_dataset_2
    tao_datasetproperty_115.data_type = 1L
    tao_datasetproperty_115.is_computed = False
    tao_datasetproperty_115.is_filter = True
    tao_datasetproperty_115.is_output = True
    tao_datasetproperty_115.description = u'Dark matter (sub)halo virial radius'
    tao_datasetproperty_115.group = u'Halo Properties'
    tao_datasetproperty_115.order = 2L
    tao_datasetproperty_115.is_index = False
    tao_datasetproperty_115.is_primary = False
    tao_datasetproperty_115.flags = 3L
    tao_datasetproperty_115 = save_or_locate(tao_datasetproperty_115)

    tao_datasetproperty_116 = DataSetProperty()
    tao_datasetproperty_116.name = u'rvir'
    tao_datasetproperty_116.units = u'10+6pc/h'
    tao_datasetproperty_116.label = u'Rvir'
    tao_datasetproperty_116.dataset = tao_dataset_3
    tao_datasetproperty_116.data_type = 1L
    tao_datasetproperty_116.is_computed = False
    tao_datasetproperty_116.is_filter = True
    tao_datasetproperty_116.is_output = True
    tao_datasetproperty_116.description = u'Dark matter (sub)halo virial radius'
    tao_datasetproperty_116.group = u'Halo Properties'
    tao_datasetproperty_116.order = 2L
    tao_datasetproperty_116.is_index = False
    tao_datasetproperty_116.is_primary = False
    tao_datasetproperty_116.flags = 3L
    tao_datasetproperty_116 = save_or_locate(tao_datasetproperty_116)

    tao_datasetproperty_117 = DataSetProperty()
    tao_datasetproperty_117.name = u'vvir'
    tao_datasetproperty_117.units = u'km/s'
    tao_datasetproperty_117.label = u'Vvir'
    tao_datasetproperty_117.dataset = tao_dataset_1
    tao_datasetproperty_117.data_type = 1L
    tao_datasetproperty_117.is_computed = False
    tao_datasetproperty_117.is_filter = True
    tao_datasetproperty_117.is_output = True
    tao_datasetproperty_117.description = u'Dark matter (sub)halo virial velocity'
    tao_datasetproperty_117.group = u'Halo Properties'
    tao_datasetproperty_117.order = 3L
    tao_datasetproperty_117.is_index = False
    tao_datasetproperty_117.is_primary = False
    tao_datasetproperty_117.flags = 3L
    tao_datasetproperty_117 = save_or_locate(tao_datasetproperty_117)

    tao_datasetproperty_118 = DataSetProperty()
    tao_datasetproperty_118.name = u'vvir'
    tao_datasetproperty_118.units = u'km/s'
    tao_datasetproperty_118.label = u'Vvir'
    tao_datasetproperty_118.dataset = tao_dataset_2
    tao_datasetproperty_118.data_type = 1L
    tao_datasetproperty_118.is_computed = False
    tao_datasetproperty_118.is_filter = True
    tao_datasetproperty_118.is_output = True
    tao_datasetproperty_118.description = u'Dark matter (sub)halo virial velocity'
    tao_datasetproperty_118.group = u'Halo Properties'
    tao_datasetproperty_118.order = 3L
    tao_datasetproperty_118.is_index = False
    tao_datasetproperty_118.is_primary = False
    tao_datasetproperty_118.flags = 3L
    tao_datasetproperty_118 = save_or_locate(tao_datasetproperty_118)

    tao_datasetproperty_119 = DataSetProperty()
    tao_datasetproperty_119.name = u'vvir'
    tao_datasetproperty_119.units = u'km/s'
    tao_datasetproperty_119.label = u'Vvir'
    tao_datasetproperty_119.dataset = tao_dataset_3
    tao_datasetproperty_119.data_type = 1L
    tao_datasetproperty_119.is_computed = False
    tao_datasetproperty_119.is_filter = True
    tao_datasetproperty_119.is_output = True
    tao_datasetproperty_119.description = u'Dark matter (sub)halo virial velocity'
    tao_datasetproperty_119.group = u'Halo Properties'
    tao_datasetproperty_119.order = 3L
    tao_datasetproperty_119.is_index = False
    tao_datasetproperty_119.is_primary = False
    tao_datasetproperty_119.flags = 3L
    tao_datasetproperty_119 = save_or_locate(tao_datasetproperty_119)

    tao_datasetproperty_120 = DataSetProperty()
    tao_datasetproperty_120.name = u'vmax'
    tao_datasetproperty_120.units = u'km/s'
    tao_datasetproperty_120.label = u'Vmax'
    tao_datasetproperty_120.dataset = tao_dataset_1
    tao_datasetproperty_120.data_type = 1L
    tao_datasetproperty_120.is_computed = False
    tao_datasetproperty_120.is_filter = True
    tao_datasetproperty_120.is_output = True
    tao_datasetproperty_120.description = u'Dark matter (sub)halo maximum circular velocity'
    tao_datasetproperty_120.group = u'Halo Properties'
    tao_datasetproperty_120.order = 4L
    tao_datasetproperty_120.is_index = False
    tao_datasetproperty_120.is_primary = False
    tao_datasetproperty_120.flags = 3L
    tao_datasetproperty_120 = save_or_locate(tao_datasetproperty_120)

    tao_datasetproperty_121 = DataSetProperty()
    tao_datasetproperty_121.name = u'vmax'
    tao_datasetproperty_121.units = u'km/s'
    tao_datasetproperty_121.label = u'Vmax'
    tao_datasetproperty_121.dataset = tao_dataset_2
    tao_datasetproperty_121.data_type = 1L
    tao_datasetproperty_121.is_computed = False
    tao_datasetproperty_121.is_filter = True
    tao_datasetproperty_121.is_output = True
    tao_datasetproperty_121.description = u'Dark matter (sub)halo maximum circular velocity'
    tao_datasetproperty_121.group = u'Halo Properties'
    tao_datasetproperty_121.order = 4L
    tao_datasetproperty_121.is_index = False
    tao_datasetproperty_121.is_primary = False
    tao_datasetproperty_121.flags = 3L
    tao_datasetproperty_121 = save_or_locate(tao_datasetproperty_121)

    tao_datasetproperty_122 = DataSetProperty()
    tao_datasetproperty_122.name = u'vmax'
    tao_datasetproperty_122.units = u'km/s'
    tao_datasetproperty_122.label = u'Vmax'
    tao_datasetproperty_122.dataset = tao_dataset_3
    tao_datasetproperty_122.data_type = 1L
    tao_datasetproperty_122.is_computed = False
    tao_datasetproperty_122.is_filter = True
    tao_datasetproperty_122.is_output = True
    tao_datasetproperty_122.description = u'Dark matter (sub)halo maximum circular velocity'
    tao_datasetproperty_122.group = u'Halo Properties'
    tao_datasetproperty_122.order = 4L
    tao_datasetproperty_122.is_index = False
    tao_datasetproperty_122.is_primary = False
    tao_datasetproperty_122.flags = 3L
    tao_datasetproperty_122 = save_or_locate(tao_datasetproperty_122)

    tao_datasetproperty_123 = DataSetProperty()
    tao_datasetproperty_123.name = u'veldisp'
    tao_datasetproperty_123.units = u'km/s'
    tao_datasetproperty_123.label = u'Velocity Dispersion'
    tao_datasetproperty_123.dataset = tao_dataset_1
    tao_datasetproperty_123.data_type = 1L
    tao_datasetproperty_123.is_computed = False
    tao_datasetproperty_123.is_filter = True
    tao_datasetproperty_123.is_output = True
    tao_datasetproperty_123.description = u'Dark matter halo velocity dispersion'
    tao_datasetproperty_123.group = u'Halo Properties'
    tao_datasetproperty_123.order = 5L
    tao_datasetproperty_123.is_index = False
    tao_datasetproperty_123.is_primary = False
    tao_datasetproperty_123.flags = 3L
    tao_datasetproperty_123 = save_or_locate(tao_datasetproperty_123)

    tao_datasetproperty_124 = DataSetProperty()
    tao_datasetproperty_124.name = u'veldisp'
    tao_datasetproperty_124.units = u'km/s'
    tao_datasetproperty_124.label = u'Velocity Dispersion'
    tao_datasetproperty_124.dataset = tao_dataset_2
    tao_datasetproperty_124.data_type = 1L
    tao_datasetproperty_124.is_computed = False
    tao_datasetproperty_124.is_filter = True
    tao_datasetproperty_124.is_output = True
    tao_datasetproperty_124.description = u'Dark matter halo velocity dispersion'
    tao_datasetproperty_124.group = u'Halo Properties'
    tao_datasetproperty_124.order = 5L
    tao_datasetproperty_124.is_index = False
    tao_datasetproperty_124.is_primary = False
    tao_datasetproperty_124.flags = 3L
    tao_datasetproperty_124 = save_or_locate(tao_datasetproperty_124)

    tao_datasetproperty_125 = DataSetProperty()
    tao_datasetproperty_125.name = u'veldisp'
    tao_datasetproperty_125.units = u'km/s'
    tao_datasetproperty_125.label = u'Velocity Dispersion'
    tao_datasetproperty_125.dataset = tao_dataset_3
    tao_datasetproperty_125.data_type = 1L
    tao_datasetproperty_125.is_computed = False
    tao_datasetproperty_125.is_filter = True
    tao_datasetproperty_125.is_output = True
    tao_datasetproperty_125.description = u'Dark matter halo velocity dispersion'
    tao_datasetproperty_125.group = u'Halo Properties'
    tao_datasetproperty_125.order = 5L
    tao_datasetproperty_125.is_index = False
    tao_datasetproperty_125.is_primary = False
    tao_datasetproperty_125.flags = 3L
    tao_datasetproperty_125 = save_or_locate(tao_datasetproperty_125)

    tao_datasetproperty_126 = DataSetProperty()
    tao_datasetproperty_126.name = u'spinx'
    tao_datasetproperty_126.units = u''
    tao_datasetproperty_126.label = u'x Spin'
    tao_datasetproperty_126.dataset = tao_dataset_1
    tao_datasetproperty_126.data_type = 1L
    tao_datasetproperty_126.is_computed = False
    tao_datasetproperty_126.is_filter = True
    tao_datasetproperty_126.is_output = True
    tao_datasetproperty_126.description = u'X component of the (sub)halo spin'
    tao_datasetproperty_126.group = u'Halo Properties'
    tao_datasetproperty_126.order = 6L
    tao_datasetproperty_126.is_index = False
    tao_datasetproperty_126.is_primary = False
    tao_datasetproperty_126.flags = 3L
    tao_datasetproperty_126 = save_or_locate(tao_datasetproperty_126)

    tao_datasetproperty_127 = DataSetProperty()
    tao_datasetproperty_127.name = u'spinx'
    tao_datasetproperty_127.units = u''
    tao_datasetproperty_127.label = u'x Spin'
    tao_datasetproperty_127.dataset = tao_dataset_2
    tao_datasetproperty_127.data_type = 1L
    tao_datasetproperty_127.is_computed = False
    tao_datasetproperty_127.is_filter = True
    tao_datasetproperty_127.is_output = True
    tao_datasetproperty_127.description = u'X component of the (sub)halo spin'
    tao_datasetproperty_127.group = u'Halo Properties'
    tao_datasetproperty_127.order = 6L
    tao_datasetproperty_127.is_index = False
    tao_datasetproperty_127.is_primary = False
    tao_datasetproperty_127.flags = 3L
    tao_datasetproperty_127 = save_or_locate(tao_datasetproperty_127)

    tao_datasetproperty_128 = DataSetProperty()
    tao_datasetproperty_128.name = u'spinx'
    tao_datasetproperty_128.units = u''
    tao_datasetproperty_128.label = u'x Spin'
    tao_datasetproperty_128.dataset = tao_dataset_3
    tao_datasetproperty_128.data_type = 1L
    tao_datasetproperty_128.is_computed = False
    tao_datasetproperty_128.is_filter = True
    tao_datasetproperty_128.is_output = True
    tao_datasetproperty_128.description = u'X component of the (sub)halo spin'
    tao_datasetproperty_128.group = u'Halo Properties'
    tao_datasetproperty_128.order = 6L
    tao_datasetproperty_128.is_index = False
    tao_datasetproperty_128.is_primary = False
    tao_datasetproperty_128.flags = 3L
    tao_datasetproperty_128 = save_or_locate(tao_datasetproperty_128)

    tao_datasetproperty_129 = DataSetProperty()
    tao_datasetproperty_129.name = u'spiny'
    tao_datasetproperty_129.units = u''
    tao_datasetproperty_129.label = u'y Spin'
    tao_datasetproperty_129.dataset = tao_dataset_1
    tao_datasetproperty_129.data_type = 1L
    tao_datasetproperty_129.is_computed = False
    tao_datasetproperty_129.is_filter = True
    tao_datasetproperty_129.is_output = True
    tao_datasetproperty_129.description = u'Y component of the (sub)halo spin'
    tao_datasetproperty_129.group = u'Halo Properties'
    tao_datasetproperty_129.order = 7L
    tao_datasetproperty_129.is_index = False
    tao_datasetproperty_129.is_primary = False
    tao_datasetproperty_129.flags = 3L
    tao_datasetproperty_129 = save_or_locate(tao_datasetproperty_129)

    tao_datasetproperty_130 = DataSetProperty()
    tao_datasetproperty_130.name = u'spiny'
    tao_datasetproperty_130.units = u''
    tao_datasetproperty_130.label = u'y Spin'
    tao_datasetproperty_130.dataset = tao_dataset_2
    tao_datasetproperty_130.data_type = 1L
    tao_datasetproperty_130.is_computed = False
    tao_datasetproperty_130.is_filter = True
    tao_datasetproperty_130.is_output = True
    tao_datasetproperty_130.description = u'Y component of the (sub)halo spin'
    tao_datasetproperty_130.group = u'Halo Properties'
    tao_datasetproperty_130.order = 7L
    tao_datasetproperty_130.is_index = False
    tao_datasetproperty_130.is_primary = False
    tao_datasetproperty_130.flags = 3L
    tao_datasetproperty_130 = save_or_locate(tao_datasetproperty_130)

    tao_datasetproperty_131 = DataSetProperty()
    tao_datasetproperty_131.name = u'spiny'
    tao_datasetproperty_131.units = u''
    tao_datasetproperty_131.label = u'y Spin'
    tao_datasetproperty_131.dataset = tao_dataset_3
    tao_datasetproperty_131.data_type = 1L
    tao_datasetproperty_131.is_computed = False
    tao_datasetproperty_131.is_filter = True
    tao_datasetproperty_131.is_output = True
    tao_datasetproperty_131.description = u'Y component of the (sub)halo spin'
    tao_datasetproperty_131.group = u'Halo Properties'
    tao_datasetproperty_131.order = 7L
    tao_datasetproperty_131.is_index = False
    tao_datasetproperty_131.is_primary = False
    tao_datasetproperty_131.flags = 3L
    tao_datasetproperty_131 = save_or_locate(tao_datasetproperty_131)

    tao_datasetproperty_132 = DataSetProperty()
    tao_datasetproperty_132.name = u'spinz'
    tao_datasetproperty_132.units = u''
    tao_datasetproperty_132.label = u'z Spin'
    tao_datasetproperty_132.dataset = tao_dataset_1
    tao_datasetproperty_132.data_type = 1L
    tao_datasetproperty_132.is_computed = False
    tao_datasetproperty_132.is_filter = True
    tao_datasetproperty_132.is_output = True
    tao_datasetproperty_132.description = u'Z component of the (sub)halo spin'
    tao_datasetproperty_132.group = u'Halo Properties'
    tao_datasetproperty_132.order = 8L
    tao_datasetproperty_132.is_index = False
    tao_datasetproperty_132.is_primary = False
    tao_datasetproperty_132.flags = 3L
    tao_datasetproperty_132 = save_or_locate(tao_datasetproperty_132)

    tao_datasetproperty_133 = DataSetProperty()
    tao_datasetproperty_133.name = u'spinz'
    tao_datasetproperty_133.units = u''
    tao_datasetproperty_133.label = u'z Spin'
    tao_datasetproperty_133.dataset = tao_dataset_2
    tao_datasetproperty_133.data_type = 1L
    tao_datasetproperty_133.is_computed = False
    tao_datasetproperty_133.is_filter = True
    tao_datasetproperty_133.is_output = True
    tao_datasetproperty_133.description = u'Z component of the (sub)halo spin'
    tao_datasetproperty_133.group = u'Halo Properties'
    tao_datasetproperty_133.order = 8L
    tao_datasetproperty_133.is_index = False
    tao_datasetproperty_133.is_primary = False
    tao_datasetproperty_133.flags = 3L
    tao_datasetproperty_133 = save_or_locate(tao_datasetproperty_133)

    tao_datasetproperty_134 = DataSetProperty()
    tao_datasetproperty_134.name = u'spinz'
    tao_datasetproperty_134.units = u''
    tao_datasetproperty_134.label = u'z Spin'
    tao_datasetproperty_134.dataset = tao_dataset_3
    tao_datasetproperty_134.data_type = 1L
    tao_datasetproperty_134.is_computed = False
    tao_datasetproperty_134.is_filter = True
    tao_datasetproperty_134.is_output = True
    tao_datasetproperty_134.description = u'Z component of the (sub)halo spin'
    tao_datasetproperty_134.group = u'Halo Properties'
    tao_datasetproperty_134.order = 8L
    tao_datasetproperty_134.is_index = False
    tao_datasetproperty_134.is_primary = False
    tao_datasetproperty_134.flags = 3L
    tao_datasetproperty_134 = save_or_locate(tao_datasetproperty_134)

    tao_datasetproperty_135 = DataSetProperty()
    tao_datasetproperty_135.name = u'len'
    tao_datasetproperty_135.units = u''
    tao_datasetproperty_135.label = u'Total particles'
    tao_datasetproperty_135.dataset = tao_dataset_1
    tao_datasetproperty_135.data_type = 0L
    tao_datasetproperty_135.is_computed = False
    tao_datasetproperty_135.is_filter = True
    tao_datasetproperty_135.is_output = True
    tao_datasetproperty_135.description = u'Total simulation particles in the dark matter halo'
    tao_datasetproperty_135.group = u'Halo Properties'
    tao_datasetproperty_135.order = 9L
    tao_datasetproperty_135.is_index = False
    tao_datasetproperty_135.is_primary = False
    tao_datasetproperty_135.flags = 3L
    tao_datasetproperty_135 = save_or_locate(tao_datasetproperty_135)

    tao_datasetproperty_136 = DataSetProperty()
    tao_datasetproperty_136.name = u'len'
    tao_datasetproperty_136.units = u''
    tao_datasetproperty_136.label = u'Total particles'
    tao_datasetproperty_136.dataset = tao_dataset_2
    tao_datasetproperty_136.data_type = 0L
    tao_datasetproperty_136.is_computed = False
    tao_datasetproperty_136.is_filter = True
    tao_datasetproperty_136.is_output = True
    tao_datasetproperty_136.description = u'Total simulation particles in the dark matter halo'
    tao_datasetproperty_136.group = u'Halo Properties'
    tao_datasetproperty_136.order = 9L
    tao_datasetproperty_136.is_index = False
    tao_datasetproperty_136.is_primary = False
    tao_datasetproperty_136.flags = 3L
    tao_datasetproperty_136 = save_or_locate(tao_datasetproperty_136)

    tao_datasetproperty_137 = DataSetProperty()
    tao_datasetproperty_137.name = u'len'
    tao_datasetproperty_137.units = u''
    tao_datasetproperty_137.label = u'Total particles'
    tao_datasetproperty_137.dataset = tao_dataset_3
    tao_datasetproperty_137.data_type = 0L
    tao_datasetproperty_137.is_computed = False
    tao_datasetproperty_137.is_filter = True
    tao_datasetproperty_137.is_output = True
    tao_datasetproperty_137.description = u'Total simulation particles in the dark matter halo'
    tao_datasetproperty_137.group = u'Halo Properties'
    tao_datasetproperty_137.order = 9L
    tao_datasetproperty_137.is_index = False
    tao_datasetproperty_137.is_primary = False
    tao_datasetproperty_137.flags = 3L
    tao_datasetproperty_137 = save_or_locate(tao_datasetproperty_137)

    tao_datasetproperty_138 = DataSetProperty()
    tao_datasetproperty_138.name = u'centralmvir'
    tao_datasetproperty_138.units = u'10+10solMass/h'
    tao_datasetproperty_138.label = u'Central Galaxy Mvir'
    tao_datasetproperty_138.dataset = tao_dataset_1
    tao_datasetproperty_138.data_type = 1L
    tao_datasetproperty_138.is_computed = False
    tao_datasetproperty_138.is_filter = True
    tao_datasetproperty_138.is_output = True
    tao_datasetproperty_138.description = u'Dark matter FOF halo (central galaxy) virial mass'
    tao_datasetproperty_138.group = u'Halo Properties'
    tao_datasetproperty_138.order = 10L
    tao_datasetproperty_138.is_index = False
    tao_datasetproperty_138.is_primary = False
    tao_datasetproperty_138.flags = 3L
    tao_datasetproperty_138 = save_or_locate(tao_datasetproperty_138)

    tao_datasetproperty_139 = DataSetProperty()
    tao_datasetproperty_139.name = u'centralmvir'
    tao_datasetproperty_139.units = u'10+10solMass/h'
    tao_datasetproperty_139.label = u'Central Galaxy Mvir'
    tao_datasetproperty_139.dataset = tao_dataset_2
    tao_datasetproperty_139.data_type = 1L
    tao_datasetproperty_139.is_computed = False
    tao_datasetproperty_139.is_filter = True
    tao_datasetproperty_139.is_output = True
    tao_datasetproperty_139.description = u'Dark matter FOF halo (central galaxy) virial mass'
    tao_datasetproperty_139.group = u'Halo Properties'
    tao_datasetproperty_139.order = 10L
    tao_datasetproperty_139.is_index = False
    tao_datasetproperty_139.is_primary = False
    tao_datasetproperty_139.flags = 3L
    tao_datasetproperty_139 = save_or_locate(tao_datasetproperty_139)

    tao_datasetproperty_140 = DataSetProperty()
    tao_datasetproperty_140.name = u'centralmvir'
    tao_datasetproperty_140.units = u'10+10solMass/h'
    tao_datasetproperty_140.label = u'Central Galaxy Mvir'
    tao_datasetproperty_140.dataset = tao_dataset_3
    tao_datasetproperty_140.data_type = 1L
    tao_datasetproperty_140.is_computed = False
    tao_datasetproperty_140.is_filter = True
    tao_datasetproperty_140.is_output = True
    tao_datasetproperty_140.description = u'Dark matter FOF halo (central galaxy) virial mass'
    tao_datasetproperty_140.group = u'Halo Properties'
    tao_datasetproperty_140.order = 10L
    tao_datasetproperty_140.is_index = False
    tao_datasetproperty_140.is_primary = False
    tao_datasetproperty_140.flags = 3L
    tao_datasetproperty_140 = save_or_locate(tao_datasetproperty_140)

    tao_datasetproperty_141 = DataSetProperty()
    tao_datasetproperty_141.name = u'descendant'
    tao_datasetproperty_141.units = u''
    tao_datasetproperty_141.label = u'Descendant'
    tao_datasetproperty_141.dataset = tao_dataset_1
    tao_datasetproperty_141.data_type = 0L
    tao_datasetproperty_141.is_computed = False
    tao_datasetproperty_141.is_filter = False
    tao_datasetproperty_141.is_output = False
    tao_datasetproperty_141.description = u''
    tao_datasetproperty_141.group = u'Internal'
    tao_datasetproperty_141.order = 4L
    tao_datasetproperty_141.is_index = False
    tao_datasetproperty_141.is_primary = False
    tao_datasetproperty_141.flags = 3L
    tao_datasetproperty_141 = save_or_locate(tao_datasetproperty_141)

    tao_datasetproperty_142 = DataSetProperty()
    tao_datasetproperty_142.name = u'descendant'
    tao_datasetproperty_142.units = u''
    tao_datasetproperty_142.label = u'Descendant'
    tao_datasetproperty_142.dataset = tao_dataset_2
    tao_datasetproperty_142.data_type = 0L
    tao_datasetproperty_142.is_computed = False
    tao_datasetproperty_142.is_filter = False
    tao_datasetproperty_142.is_output = False
    tao_datasetproperty_142.description = u''
    tao_datasetproperty_142.group = u'Internal'
    tao_datasetproperty_142.order = 4L
    tao_datasetproperty_142.is_index = False
    tao_datasetproperty_142.is_primary = False
    tao_datasetproperty_142.flags = 3L
    tao_datasetproperty_142 = save_or_locate(tao_datasetproperty_142)

    tao_datasetproperty_143 = DataSetProperty()
    tao_datasetproperty_143.name = u'descendant'
    tao_datasetproperty_143.units = u''
    tao_datasetproperty_143.label = u'Descendant'
    tao_datasetproperty_143.dataset = tao_dataset_3
    tao_datasetproperty_143.data_type = 0L
    tao_datasetproperty_143.is_computed = False
    tao_datasetproperty_143.is_filter = False
    tao_datasetproperty_143.is_output = False
    tao_datasetproperty_143.description = u''
    tao_datasetproperty_143.group = u'Internal'
    tao_datasetproperty_143.order = 4L
    tao_datasetproperty_143.is_index = False
    tao_datasetproperty_143.is_primary = False
    tao_datasetproperty_143.flags = 3L
    tao_datasetproperty_143 = save_or_locate(tao_datasetproperty_143)

    tao_datasetproperty_144 = DataSetProperty()
    tao_datasetproperty_144.name = u'fofhaloindex'
    tao_datasetproperty_144.units = u''
    tao_datasetproperty_144.label = u'FOF Halo Index'
    tao_datasetproperty_144.dataset = tao_dataset_1
    tao_datasetproperty_144.data_type = 0L
    tao_datasetproperty_144.is_computed = False
    tao_datasetproperty_144.is_filter = False
    tao_datasetproperty_144.is_output = False
    tao_datasetproperty_144.description = u''
    tao_datasetproperty_144.group = u'Internal'
    tao_datasetproperty_144.order = 5L
    tao_datasetproperty_144.is_index = False
    tao_datasetproperty_144.is_primary = False
    tao_datasetproperty_144.flags = 3L
    tao_datasetproperty_144 = save_or_locate(tao_datasetproperty_144)

    tao_datasetproperty_145 = DataSetProperty()
    tao_datasetproperty_145.name = u'fofhaloindex'
    tao_datasetproperty_145.units = u''
    tao_datasetproperty_145.label = u'FOF Halo Index'
    tao_datasetproperty_145.dataset = tao_dataset_2
    tao_datasetproperty_145.data_type = 0L
    tao_datasetproperty_145.is_computed = False
    tao_datasetproperty_145.is_filter = False
    tao_datasetproperty_145.is_output = False
    tao_datasetproperty_145.description = u''
    tao_datasetproperty_145.group = u'Internal'
    tao_datasetproperty_145.order = 5L
    tao_datasetproperty_145.is_index = False
    tao_datasetproperty_145.is_primary = False
    tao_datasetproperty_145.flags = 3L
    tao_datasetproperty_145 = save_or_locate(tao_datasetproperty_145)

    tao_datasetproperty_146 = DataSetProperty()
    tao_datasetproperty_146.name = u'fofhaloindex'
    tao_datasetproperty_146.units = u''
    tao_datasetproperty_146.label = u'FOF Halo Index'
    tao_datasetproperty_146.dataset = tao_dataset_3
    tao_datasetproperty_146.data_type = 0L
    tao_datasetproperty_146.is_computed = False
    tao_datasetproperty_146.is_filter = False
    tao_datasetproperty_146.is_output = False
    tao_datasetproperty_146.description = u''
    tao_datasetproperty_146.group = u'Internal'
    tao_datasetproperty_146.order = 5L
    tao_datasetproperty_146.is_index = False
    tao_datasetproperty_146.is_primary = False
    tao_datasetproperty_146.flags = 3L
    tao_datasetproperty_146 = save_or_locate(tao_datasetproperty_146)

    tao_datasetproperty_147 = DataSetProperty()
    tao_datasetproperty_147.name = u'globalgalaxyid'
    tao_datasetproperty_147.units = u''
    tao_datasetproperty_147.label = u'Galaxy Index'
    tao_datasetproperty_147.dataset = tao_dataset_1
    tao_datasetproperty_147.data_type = 2L
    tao_datasetproperty_147.is_computed = False
    tao_datasetproperty_147.is_filter = False
    tao_datasetproperty_147.is_output = False
    tao_datasetproperty_147.description = u''
    tao_datasetproperty_147.group = u'Internal'
    tao_datasetproperty_147.order = 6L
    tao_datasetproperty_147.is_index = False
    tao_datasetproperty_147.is_primary = False
    tao_datasetproperty_147.flags = 3L
    tao_datasetproperty_147 = save_or_locate(tao_datasetproperty_147)

    tao_datasetproperty_148 = DataSetProperty()
    tao_datasetproperty_148.name = u'globalgalaxyid'
    tao_datasetproperty_148.units = u''
    tao_datasetproperty_148.label = u'Galaxy Index'
    tao_datasetproperty_148.dataset = tao_dataset_2
    tao_datasetproperty_148.data_type = 2L
    tao_datasetproperty_148.is_computed = False
    tao_datasetproperty_148.is_filter = False
    tao_datasetproperty_148.is_output = False
    tao_datasetproperty_148.description = u''
    tao_datasetproperty_148.group = u'Internal'
    tao_datasetproperty_148.order = 6L
    tao_datasetproperty_148.is_index = False
    tao_datasetproperty_148.is_primary = False
    tao_datasetproperty_148.flags = 3L
    tao_datasetproperty_148 = save_or_locate(tao_datasetproperty_148)

    tao_datasetproperty_149 = DataSetProperty()
    tao_datasetproperty_149.name = u'globalgalaxyid'
    tao_datasetproperty_149.units = u''
    tao_datasetproperty_149.label = u'Galaxy Index'
    tao_datasetproperty_149.dataset = tao_dataset_3
    tao_datasetproperty_149.data_type = 2L
    tao_datasetproperty_149.is_computed = False
    tao_datasetproperty_149.is_filter = False
    tao_datasetproperty_149.is_output = False
    tao_datasetproperty_149.description = u''
    tao_datasetproperty_149.group = u'Internal'
    tao_datasetproperty_149.order = 6L
    tao_datasetproperty_149.is_index = False
    tao_datasetproperty_149.is_primary = False
    tao_datasetproperty_149.flags = 3L
    tao_datasetproperty_149 = save_or_locate(tao_datasetproperty_149)

    tao_datasetproperty_150 = DataSetProperty()
    tao_datasetproperty_150.name = u'globaldescendant'
    tao_datasetproperty_150.units = u''
    tao_datasetproperty_150.label = u'Global Descendant'
    tao_datasetproperty_150.dataset = tao_dataset_1
    tao_datasetproperty_150.data_type = 2L
    tao_datasetproperty_150.is_computed = False
    tao_datasetproperty_150.is_filter = False
    tao_datasetproperty_150.is_output = False
    tao_datasetproperty_150.description = u''
    tao_datasetproperty_150.group = u'Internal'
    tao_datasetproperty_150.order = 7L
    tao_datasetproperty_150.is_index = False
    tao_datasetproperty_150.is_primary = False
    tao_datasetproperty_150.flags = 3L
    tao_datasetproperty_150 = save_or_locate(tao_datasetproperty_150)

    tao_datasetproperty_151 = DataSetProperty()
    tao_datasetproperty_151.name = u'globaldescendant'
    tao_datasetproperty_151.units = u''
    tao_datasetproperty_151.label = u'Global Descendant'
    tao_datasetproperty_151.dataset = tao_dataset_2
    tao_datasetproperty_151.data_type = 2L
    tao_datasetproperty_151.is_computed = False
    tao_datasetproperty_151.is_filter = False
    tao_datasetproperty_151.is_output = False
    tao_datasetproperty_151.description = u''
    tao_datasetproperty_151.group = u'Internal'
    tao_datasetproperty_151.order = 7L
    tao_datasetproperty_151.is_index = False
    tao_datasetproperty_151.is_primary = False
    tao_datasetproperty_151.flags = 3L
    tao_datasetproperty_151 = save_or_locate(tao_datasetproperty_151)

    tao_datasetproperty_152 = DataSetProperty()
    tao_datasetproperty_152.name = u'globaldescendant'
    tao_datasetproperty_152.units = u''
    tao_datasetproperty_152.label = u'Global Descendant'
    tao_datasetproperty_152.dataset = tao_dataset_3
    tao_datasetproperty_152.data_type = 2L
    tao_datasetproperty_152.is_computed = False
    tao_datasetproperty_152.is_filter = False
    tao_datasetproperty_152.is_output = False
    tao_datasetproperty_152.description = u''
    tao_datasetproperty_152.group = u'Internal'
    tao_datasetproperty_152.order = 7L
    tao_datasetproperty_152.is_index = False
    tao_datasetproperty_152.is_primary = False
    tao_datasetproperty_152.flags = 3L
    tao_datasetproperty_152 = save_or_locate(tao_datasetproperty_152)

    tao_datasetproperty_153 = DataSetProperty()
    tao_datasetproperty_153.name = u'treeindex'
    tao_datasetproperty_153.units = u''
    tao_datasetproperty_153.label = u'Tree Index'
    tao_datasetproperty_153.dataset = tao_dataset_1
    tao_datasetproperty_153.data_type = 0L
    tao_datasetproperty_153.is_computed = False
    tao_datasetproperty_153.is_filter = False
    tao_datasetproperty_153.is_output = False
    tao_datasetproperty_153.description = u''
    tao_datasetproperty_153.group = u'Internal'
    tao_datasetproperty_153.order = 8L
    tao_datasetproperty_153.is_index = False
    tao_datasetproperty_153.is_primary = False
    tao_datasetproperty_153.flags = 3L
    tao_datasetproperty_153 = save_or_locate(tao_datasetproperty_153)

    tao_datasetproperty_154 = DataSetProperty()
    tao_datasetproperty_154.name = u'treeindex'
    tao_datasetproperty_154.units = u''
    tao_datasetproperty_154.label = u'Tree Index'
    tao_datasetproperty_154.dataset = tao_dataset_2
    tao_datasetproperty_154.data_type = 0L
    tao_datasetproperty_154.is_computed = False
    tao_datasetproperty_154.is_filter = False
    tao_datasetproperty_154.is_output = False
    tao_datasetproperty_154.description = u''
    tao_datasetproperty_154.group = u'Internal'
    tao_datasetproperty_154.order = 8L
    tao_datasetproperty_154.is_index = False
    tao_datasetproperty_154.is_primary = False
    tao_datasetproperty_154.flags = 3L
    tao_datasetproperty_154 = save_or_locate(tao_datasetproperty_154)

    tao_datasetproperty_155 = DataSetProperty()
    tao_datasetproperty_155.name = u'treeindex'
    tao_datasetproperty_155.units = u''
    tao_datasetproperty_155.label = u'Tree Index'
    tao_datasetproperty_155.dataset = tao_dataset_3
    tao_datasetproperty_155.data_type = 0L
    tao_datasetproperty_155.is_computed = False
    tao_datasetproperty_155.is_filter = False
    tao_datasetproperty_155.is_output = False
    tao_datasetproperty_155.description = u''
    tao_datasetproperty_155.group = u'Internal'
    tao_datasetproperty_155.order = 8L
    tao_datasetproperty_155.is_index = False
    tao_datasetproperty_155.is_primary = False
    tao_datasetproperty_155.flags = 3L
    tao_datasetproperty_155 = save_or_locate(tao_datasetproperty_155)

    tao_datasetproperty_156 = DataSetProperty()
    tao_datasetproperty_156.name = u'ra'
    tao_datasetproperty_156.units = u'degrees'
    tao_datasetproperty_156.label = u'Right Ascension'
    tao_datasetproperty_156.dataset = tao_dataset_1
    tao_datasetproperty_156.data_type = 1L
    tao_datasetproperty_156.is_computed = True
    tao_datasetproperty_156.is_filter = True
    tao_datasetproperty_156.is_output = True
    tao_datasetproperty_156.description = u'Right Ascension in the selected box/cone'
    tao_datasetproperty_156.group = u'Positions & Velocities'
    tao_datasetproperty_156.order = 1L
    tao_datasetproperty_156.is_index = False
    tao_datasetproperty_156.is_primary = False
    tao_datasetproperty_156.flags = 1L
    tao_datasetproperty_156 = save_or_locate(tao_datasetproperty_156)

    tao_datasetproperty_157 = DataSetProperty()
    tao_datasetproperty_157.name = u'ra'
    tao_datasetproperty_157.units = u'degrees'
    tao_datasetproperty_157.label = u'Right Ascension'
    tao_datasetproperty_157.dataset = tao_dataset_2
    tao_datasetproperty_157.data_type = 1L
    tao_datasetproperty_157.is_computed = True
    tao_datasetproperty_157.is_filter = True
    tao_datasetproperty_157.is_output = True
    tao_datasetproperty_157.description = u'Right Ascension in the selected box/cone'
    tao_datasetproperty_157.group = u'Positions & Velocities'
    tao_datasetproperty_157.order = 1L
    tao_datasetproperty_157.is_index = False
    tao_datasetproperty_157.is_primary = False
    tao_datasetproperty_157.flags = 1L
    tao_datasetproperty_157 = save_or_locate(tao_datasetproperty_157)

    tao_datasetproperty_158 = DataSetProperty()
    tao_datasetproperty_158.name = u'ra'
    tao_datasetproperty_158.units = u'degrees'
    tao_datasetproperty_158.label = u'Right Ascension'
    tao_datasetproperty_158.dataset = tao_dataset_3
    tao_datasetproperty_158.data_type = 1L
    tao_datasetproperty_158.is_computed = True
    tao_datasetproperty_158.is_filter = True
    tao_datasetproperty_158.is_output = True
    tao_datasetproperty_158.description = u'Right Ascension in the selected box/cone'
    tao_datasetproperty_158.group = u'Positions & Velocities'
    tao_datasetproperty_158.order = 1L
    tao_datasetproperty_158.is_index = False
    tao_datasetproperty_158.is_primary = False
    tao_datasetproperty_158.flags = 1L
    tao_datasetproperty_158 = save_or_locate(tao_datasetproperty_158)

    tao_datasetproperty_159 = DataSetProperty()
    tao_datasetproperty_159.name = u'ra'
    tao_datasetproperty_159.units = u'degrees'
    tao_datasetproperty_159.label = u'Right Ascension'
    tao_datasetproperty_159.dataset = tao_dataset_4
    tao_datasetproperty_159.data_type = 1L
    tao_datasetproperty_159.is_computed = True
    tao_datasetproperty_159.is_filter = True
    tao_datasetproperty_159.is_output = True
    tao_datasetproperty_159.description = u'Right Ascension in the selected box/cone'
    tao_datasetproperty_159.group = u'Positions & Velocities'
    tao_datasetproperty_159.order = 1L
    tao_datasetproperty_159.is_index = False
    tao_datasetproperty_159.is_primary = False
    tao_datasetproperty_159.flags = 1L
    tao_datasetproperty_159 = save_or_locate(tao_datasetproperty_159)

    tao_datasetproperty_160 = DataSetProperty()
    tao_datasetproperty_160.name = u'dec'
    tao_datasetproperty_160.units = u'degrees'
    tao_datasetproperty_160.label = u'Declination'
    tao_datasetproperty_160.dataset = tao_dataset_1
    tao_datasetproperty_160.data_type = 1L
    tao_datasetproperty_160.is_computed = True
    tao_datasetproperty_160.is_filter = True
    tao_datasetproperty_160.is_output = True
    tao_datasetproperty_160.description = u'Declination in the selected box/cone'
    tao_datasetproperty_160.group = u'Positions & Velocities'
    tao_datasetproperty_160.order = 2L
    tao_datasetproperty_160.is_index = False
    tao_datasetproperty_160.is_primary = False
    tao_datasetproperty_160.flags = 1L
    tao_datasetproperty_160 = save_or_locate(tao_datasetproperty_160)

    tao_datasetproperty_161 = DataSetProperty()
    tao_datasetproperty_161.name = u'dec'
    tao_datasetproperty_161.units = u'degrees'
    tao_datasetproperty_161.label = u'Declination'
    tao_datasetproperty_161.dataset = tao_dataset_2
    tao_datasetproperty_161.data_type = 1L
    tao_datasetproperty_161.is_computed = True
    tao_datasetproperty_161.is_filter = True
    tao_datasetproperty_161.is_output = True
    tao_datasetproperty_161.description = u'Declination in the selected box/cone'
    tao_datasetproperty_161.group = u'Positions & Velocities'
    tao_datasetproperty_161.order = 2L
    tao_datasetproperty_161.is_index = False
    tao_datasetproperty_161.is_primary = False
    tao_datasetproperty_161.flags = 1L
    tao_datasetproperty_161 = save_or_locate(tao_datasetproperty_161)

    tao_datasetproperty_162 = DataSetProperty()
    tao_datasetproperty_162.name = u'dec'
    tao_datasetproperty_162.units = u'degrees'
    tao_datasetproperty_162.label = u'Declination'
    tao_datasetproperty_162.dataset = tao_dataset_3
    tao_datasetproperty_162.data_type = 1L
    tao_datasetproperty_162.is_computed = True
    tao_datasetproperty_162.is_filter = True
    tao_datasetproperty_162.is_output = True
    tao_datasetproperty_162.description = u'Declination in the selected box/cone'
    tao_datasetproperty_162.group = u'Positions & Velocities'
    tao_datasetproperty_162.order = 2L
    tao_datasetproperty_162.is_index = False
    tao_datasetproperty_162.is_primary = False
    tao_datasetproperty_162.flags = 1L
    tao_datasetproperty_162 = save_or_locate(tao_datasetproperty_162)

    tao_datasetproperty_163 = DataSetProperty()
    tao_datasetproperty_163.name = u'dec'
    tao_datasetproperty_163.units = u'degrees'
    tao_datasetproperty_163.label = u'Declination'
    tao_datasetproperty_163.dataset = tao_dataset_4
    tao_datasetproperty_163.data_type = 1L
    tao_datasetproperty_163.is_computed = True
    tao_datasetproperty_163.is_filter = True
    tao_datasetproperty_163.is_output = True
    tao_datasetproperty_163.description = u'Declination in the selected box/cone'
    tao_datasetproperty_163.group = u'Positions & Velocities'
    tao_datasetproperty_163.order = 2L
    tao_datasetproperty_163.is_index = False
    tao_datasetproperty_163.is_primary = False
    tao_datasetproperty_163.flags = 1L
    tao_datasetproperty_163 = save_or_locate(tao_datasetproperty_163)

    tao_datasetproperty_164 = DataSetProperty()
    tao_datasetproperty_164.name = u'redshift_cosmological'
    tao_datasetproperty_164.units = u''
    tao_datasetproperty_164.label = u'Redshift (Cosmological)'
    tao_datasetproperty_164.dataset = tao_dataset_1
    tao_datasetproperty_164.data_type = 1L
    tao_datasetproperty_164.is_computed = True
    tao_datasetproperty_164.is_filter = True
    tao_datasetproperty_164.is_output = True
    tao_datasetproperty_164.description = u'Redshift (Cosmological) in the selected box/cone'
    tao_datasetproperty_164.group = u'Positions & Velocities'
    tao_datasetproperty_164.order = 3L
    tao_datasetproperty_164.is_index = False
    tao_datasetproperty_164.is_primary = False
    tao_datasetproperty_164.flags = 1L
    tao_datasetproperty_164 = save_or_locate(tao_datasetproperty_164)

    tao_datasetproperty_165 = DataSetProperty()
    tao_datasetproperty_165.name = u'redshift_cosmological'
    tao_datasetproperty_165.units = u''
    tao_datasetproperty_165.label = u'Redshift (Cosmological)'
    tao_datasetproperty_165.dataset = tao_dataset_2
    tao_datasetproperty_165.data_type = 1L
    tao_datasetproperty_165.is_computed = True
    tao_datasetproperty_165.is_filter = True
    tao_datasetproperty_165.is_output = True
    tao_datasetproperty_165.description = u'Redshift (Cosmological) in the selected box/cone'
    tao_datasetproperty_165.group = u'Positions & Velocities'
    tao_datasetproperty_165.order = 3L
    tao_datasetproperty_165.is_index = False
    tao_datasetproperty_165.is_primary = False
    tao_datasetproperty_165.flags = 1L
    tao_datasetproperty_165 = save_or_locate(tao_datasetproperty_165)

    tao_datasetproperty_166 = DataSetProperty()
    tao_datasetproperty_166.name = u'redshift_cosmological'
    tao_datasetproperty_166.units = u''
    tao_datasetproperty_166.label = u'Redshift (Cosmological)'
    tao_datasetproperty_166.dataset = tao_dataset_3
    tao_datasetproperty_166.data_type = 1L
    tao_datasetproperty_166.is_computed = True
    tao_datasetproperty_166.is_filter = True
    tao_datasetproperty_166.is_output = True
    tao_datasetproperty_166.description = u'Redshift (Cosmological) in the selected box/cone'
    tao_datasetproperty_166.group = u'Positions & Velocities'
    tao_datasetproperty_166.order = 3L
    tao_datasetproperty_166.is_index = False
    tao_datasetproperty_166.is_primary = False
    tao_datasetproperty_166.flags = 1L
    tao_datasetproperty_166 = save_or_locate(tao_datasetproperty_166)

    tao_datasetproperty_167 = DataSetProperty()
    tao_datasetproperty_167.name = u'redshift_cosmological'
    tao_datasetproperty_167.units = u''
    tao_datasetproperty_167.label = u'Redshift (Cosmological)'
    tao_datasetproperty_167.dataset = tao_dataset_4
    tao_datasetproperty_167.data_type = 1L
    tao_datasetproperty_167.is_computed = True
    tao_datasetproperty_167.is_filter = True
    tao_datasetproperty_167.is_output = True
    tao_datasetproperty_167.description = u'Redshift (Cosmological) in the selected box/cone'
    tao_datasetproperty_167.group = u'Positions & Velocities'
    tao_datasetproperty_167.order = 3L
    tao_datasetproperty_167.is_index = False
    tao_datasetproperty_167.is_primary = False
    tao_datasetproperty_167.flags = 1L
    tao_datasetproperty_167 = save_or_locate(tao_datasetproperty_167)

    tao_datasetproperty_168 = DataSetProperty()
    tao_datasetproperty_168.name = u'redshift_observed'
    tao_datasetproperty_168.units = u''
    tao_datasetproperty_168.label = u'Redshift (Observed)'
    tao_datasetproperty_168.dataset = tao_dataset_1
    tao_datasetproperty_168.data_type = 1L
    tao_datasetproperty_168.is_computed = True
    tao_datasetproperty_168.is_filter = True
    tao_datasetproperty_168.is_output = True
    tao_datasetproperty_168.description = u'Redshift (Observed) = Redshift (Cosmological) + Peculiar Velocity'
    tao_datasetproperty_168.group = u'Positions & Velocities'
    tao_datasetproperty_168.order = 3L
    tao_datasetproperty_168.is_index = False
    tao_datasetproperty_168.is_primary = False
    tao_datasetproperty_168.flags = 1L
    tao_datasetproperty_168 = save_or_locate(tao_datasetproperty_168)

    tao_datasetproperty_169 = DataSetProperty()
    tao_datasetproperty_169.name = u'redshift_observed'
    tao_datasetproperty_169.units = u''
    tao_datasetproperty_169.label = u'Redshift (Observed)'
    tao_datasetproperty_169.dataset = tao_dataset_2
    tao_datasetproperty_169.data_type = 1L
    tao_datasetproperty_169.is_computed = True
    tao_datasetproperty_169.is_filter = True
    tao_datasetproperty_169.is_output = True
    tao_datasetproperty_169.description = u'Redshift (Observed) = Redshift (Cosmological) + Peculiar Velocity'
    tao_datasetproperty_169.group = u'Positions & Velocities'
    tao_datasetproperty_169.order = 3L
    tao_datasetproperty_169.is_index = False
    tao_datasetproperty_169.is_primary = False
    tao_datasetproperty_169.flags = 1L
    tao_datasetproperty_169 = save_or_locate(tao_datasetproperty_169)

    tao_datasetproperty_170 = DataSetProperty()
    tao_datasetproperty_170.name = u'redshift_observed'
    tao_datasetproperty_170.units = u''
    tao_datasetproperty_170.label = u'Redshift (Observed)'
    tao_datasetproperty_170.dataset = tao_dataset_3
    tao_datasetproperty_170.data_type = 1L
    tao_datasetproperty_170.is_computed = True
    tao_datasetproperty_170.is_filter = True
    tao_datasetproperty_170.is_output = True
    tao_datasetproperty_170.description = u'Redshift (Observed) = Redshift (Cosmological) + Peculiar Velocity'
    tao_datasetproperty_170.group = u'Positions & Velocities'
    tao_datasetproperty_170.order = 3L
    tao_datasetproperty_170.is_index = False
    tao_datasetproperty_170.is_primary = False
    tao_datasetproperty_170.flags = 1L
    tao_datasetproperty_170 = save_or_locate(tao_datasetproperty_170)

    tao_datasetproperty_171 = DataSetProperty()
    tao_datasetproperty_171.name = u'redshift_observed'
    tao_datasetproperty_171.units = u''
    tao_datasetproperty_171.label = u'Redshift (Observed)'
    tao_datasetproperty_171.dataset = tao_dataset_4
    tao_datasetproperty_171.data_type = 1L
    tao_datasetproperty_171.is_computed = True
    tao_datasetproperty_171.is_filter = True
    tao_datasetproperty_171.is_output = True
    tao_datasetproperty_171.description = u'Redshift (Observed) = Redshift (Cosmological) + Peculiar Velocity'
    tao_datasetproperty_171.group = u'Positions & Velocities'
    tao_datasetproperty_171.order = 3L
    tao_datasetproperty_171.is_index = False
    tao_datasetproperty_171.is_primary = False
    tao_datasetproperty_171.flags = 1L
    tao_datasetproperty_171 = save_or_locate(tao_datasetproperty_171)

    tao_datasetproperty_172 = DataSetProperty()
    tao_datasetproperty_172.name = u'distance'
    tao_datasetproperty_172.units = u'Mpc'
    tao_datasetproperty_172.label = u'Distance'
    tao_datasetproperty_172.dataset = tao_dataset_1
    tao_datasetproperty_172.data_type = 1L
    tao_datasetproperty_172.is_computed = True
    tao_datasetproperty_172.is_filter = True
    tao_datasetproperty_172.is_output = True
    tao_datasetproperty_172.description = u'Distance from the observer in the selected box/cone'
    tao_datasetproperty_172.group = u'Positions & Velocities'
    tao_datasetproperty_172.order = 4L
    tao_datasetproperty_172.is_index = False
    tao_datasetproperty_172.is_primary = False
    tao_datasetproperty_172.flags = 1L
    tao_datasetproperty_172 = save_or_locate(tao_datasetproperty_172)

    tao_datasetproperty_173 = DataSetProperty()
    tao_datasetproperty_173.name = u'distance'
    tao_datasetproperty_173.units = u'Mpc'
    tao_datasetproperty_173.label = u'Distance'
    tao_datasetproperty_173.dataset = tao_dataset_2
    tao_datasetproperty_173.data_type = 1L
    tao_datasetproperty_173.is_computed = True
    tao_datasetproperty_173.is_filter = True
    tao_datasetproperty_173.is_output = True
    tao_datasetproperty_173.description = u'Distance from the observer in the selected box/cone'
    tao_datasetproperty_173.group = u'Positions & Velocities'
    tao_datasetproperty_173.order = 4L
    tao_datasetproperty_173.is_index = False
    tao_datasetproperty_173.is_primary = False
    tao_datasetproperty_173.flags = 1L
    tao_datasetproperty_173 = save_or_locate(tao_datasetproperty_173)

    tao_datasetproperty_174 = DataSetProperty()
    tao_datasetproperty_174.name = u'distance'
    tao_datasetproperty_174.units = u'Mpc'
    tao_datasetproperty_174.label = u'Distance'
    tao_datasetproperty_174.dataset = tao_dataset_3
    tao_datasetproperty_174.data_type = 1L
    tao_datasetproperty_174.is_computed = True
    tao_datasetproperty_174.is_filter = True
    tao_datasetproperty_174.is_output = True
    tao_datasetproperty_174.description = u'Distance from the observer in the selected box/cone'
    tao_datasetproperty_174.group = u'Positions & Velocities'
    tao_datasetproperty_174.order = 4L
    tao_datasetproperty_174.is_index = False
    tao_datasetproperty_174.is_primary = False
    tao_datasetproperty_174.flags = 1L
    tao_datasetproperty_174 = save_or_locate(tao_datasetproperty_174)

    tao_datasetproperty_175 = DataSetProperty()
    tao_datasetproperty_175.name = u'distance'
    tao_datasetproperty_175.units = u'Mpc'
    tao_datasetproperty_175.label = u'Distance'
    tao_datasetproperty_175.dataset = tao_dataset_4
    tao_datasetproperty_175.data_type = 1L
    tao_datasetproperty_175.is_computed = True
    tao_datasetproperty_175.is_filter = True
    tao_datasetproperty_175.is_output = True
    tao_datasetproperty_175.description = u'Distance from the observer in the selected box/cone'
    tao_datasetproperty_175.group = u'Positions & Velocities'
    tao_datasetproperty_175.order = 4L
    tao_datasetproperty_175.is_index = False
    tao_datasetproperty_175.is_primary = False
    tao_datasetproperty_175.flags = 1L
    tao_datasetproperty_175 = save_or_locate(tao_datasetproperty_175)

    tao_datasetproperty_176 = DataSetProperty()
    tao_datasetproperty_176.name = u'posx'
    tao_datasetproperty_176.units = u'10+6pc/h'
    tao_datasetproperty_176.label = u'x'
    tao_datasetproperty_176.dataset = tao_dataset_1
    tao_datasetproperty_176.data_type = 1L
    tao_datasetproperty_176.is_computed = False
    tao_datasetproperty_176.is_filter = True
    tao_datasetproperty_176.is_output = True
    tao_datasetproperty_176.description = u'X coordinate in the selected box/cone'
    tao_datasetproperty_176.group = u'Positions & Velocities'
    tao_datasetproperty_176.order = 4L
    tao_datasetproperty_176.is_index = False
    tao_datasetproperty_176.is_primary = False
    tao_datasetproperty_176.flags = 3L
    tao_datasetproperty_176 = save_or_locate(tao_datasetproperty_176)

    tao_datasetproperty_177 = DataSetProperty()
    tao_datasetproperty_177.name = u'posx'
    tao_datasetproperty_177.units = u'10+6pc/h'
    tao_datasetproperty_177.label = u'x'
    tao_datasetproperty_177.dataset = tao_dataset_2
    tao_datasetproperty_177.data_type = 1L
    tao_datasetproperty_177.is_computed = False
    tao_datasetproperty_177.is_filter = True
    tao_datasetproperty_177.is_output = True
    tao_datasetproperty_177.description = u'X coordinate in the selected box/cone'
    tao_datasetproperty_177.group = u'Positions & Velocities'
    tao_datasetproperty_177.order = 4L
    tao_datasetproperty_177.is_index = False
    tao_datasetproperty_177.is_primary = False
    tao_datasetproperty_177.flags = 3L
    tao_datasetproperty_177 = save_or_locate(tao_datasetproperty_177)

    tao_datasetproperty_178 = DataSetProperty()
    tao_datasetproperty_178.name = u'posx'
    tao_datasetproperty_178.units = u'10+6pc/h'
    tao_datasetproperty_178.label = u'x'
    tao_datasetproperty_178.dataset = tao_dataset_3
    tao_datasetproperty_178.data_type = 1L
    tao_datasetproperty_178.is_computed = False
    tao_datasetproperty_178.is_filter = True
    tao_datasetproperty_178.is_output = True
    tao_datasetproperty_178.description = u'X coordinate in the selected box/cone'
    tao_datasetproperty_178.group = u'Positions & Velocities'
    tao_datasetproperty_178.order = 4L
    tao_datasetproperty_178.is_index = False
    tao_datasetproperty_178.is_primary = False
    tao_datasetproperty_178.flags = 3L
    tao_datasetproperty_178 = save_or_locate(tao_datasetproperty_178)

    tao_datasetproperty_179 = DataSetProperty()
    tao_datasetproperty_179.name = u'posx'
    tao_datasetproperty_179.units = u'10+6pc/h'
    tao_datasetproperty_179.label = u'x'
    tao_datasetproperty_179.dataset = tao_dataset_4
    tao_datasetproperty_179.data_type = 1L
    tao_datasetproperty_179.is_computed = False
    tao_datasetproperty_179.is_filter = True
    tao_datasetproperty_179.is_output = True
    tao_datasetproperty_179.description = u'X coordinate in the selected box/cone'
    tao_datasetproperty_179.group = u'Positions & Velocities'
    tao_datasetproperty_179.order = 4L
    tao_datasetproperty_179.is_index = False
    tao_datasetproperty_179.is_primary = False
    tao_datasetproperty_179.flags = 3L
    tao_datasetproperty_179 = save_or_locate(tao_datasetproperty_179)

    tao_datasetproperty_180 = DataSetProperty()
    tao_datasetproperty_180.name = u'posy'
    tao_datasetproperty_180.units = u'10+6pc/h'
    tao_datasetproperty_180.label = u'y'
    tao_datasetproperty_180.dataset = tao_dataset_1
    tao_datasetproperty_180.data_type = 1L
    tao_datasetproperty_180.is_computed = False
    tao_datasetproperty_180.is_filter = True
    tao_datasetproperty_180.is_output = True
    tao_datasetproperty_180.description = u'Y coordinate in the selected box/cone'
    tao_datasetproperty_180.group = u'Positions & Velocities'
    tao_datasetproperty_180.order = 5L
    tao_datasetproperty_180.is_index = False
    tao_datasetproperty_180.is_primary = False
    tao_datasetproperty_180.flags = 3L
    tao_datasetproperty_180 = save_or_locate(tao_datasetproperty_180)

    tao_datasetproperty_181 = DataSetProperty()
    tao_datasetproperty_181.name = u'posy'
    tao_datasetproperty_181.units = u'10+6pc/h'
    tao_datasetproperty_181.label = u'y'
    tao_datasetproperty_181.dataset = tao_dataset_2
    tao_datasetproperty_181.data_type = 1L
    tao_datasetproperty_181.is_computed = False
    tao_datasetproperty_181.is_filter = True
    tao_datasetproperty_181.is_output = True
    tao_datasetproperty_181.description = u'Y coordinate in the selected box/cone'
    tao_datasetproperty_181.group = u'Positions & Velocities'
    tao_datasetproperty_181.order = 5L
    tao_datasetproperty_181.is_index = False
    tao_datasetproperty_181.is_primary = False
    tao_datasetproperty_181.flags = 3L
    tao_datasetproperty_181 = save_or_locate(tao_datasetproperty_181)

    tao_datasetproperty_182 = DataSetProperty()
    tao_datasetproperty_182.name = u'posy'
    tao_datasetproperty_182.units = u'10+6pc/h'
    tao_datasetproperty_182.label = u'y'
    tao_datasetproperty_182.dataset = tao_dataset_3
    tao_datasetproperty_182.data_type = 1L
    tao_datasetproperty_182.is_computed = False
    tao_datasetproperty_182.is_filter = True
    tao_datasetproperty_182.is_output = True
    tao_datasetproperty_182.description = u'Y coordinate in the selected box/cone'
    tao_datasetproperty_182.group = u'Positions & Velocities'
    tao_datasetproperty_182.order = 5L
    tao_datasetproperty_182.is_index = False
    tao_datasetproperty_182.is_primary = False
    tao_datasetproperty_182.flags = 3L
    tao_datasetproperty_182 = save_or_locate(tao_datasetproperty_182)

    tao_datasetproperty_183 = DataSetProperty()
    tao_datasetproperty_183.name = u'posy'
    tao_datasetproperty_183.units = u'10+6pc/h'
    tao_datasetproperty_183.label = u'y'
    tao_datasetproperty_183.dataset = tao_dataset_4
    tao_datasetproperty_183.data_type = 1L
    tao_datasetproperty_183.is_computed = False
    tao_datasetproperty_183.is_filter = True
    tao_datasetproperty_183.is_output = True
    tao_datasetproperty_183.description = u'Y coordinate in the selected box/cone'
    tao_datasetproperty_183.group = u'Positions & Velocities'
    tao_datasetproperty_183.order = 5L
    tao_datasetproperty_183.is_index = False
    tao_datasetproperty_183.is_primary = False
    tao_datasetproperty_183.flags = 3L
    tao_datasetproperty_183 = save_or_locate(tao_datasetproperty_183)

    tao_datasetproperty_184 = DataSetProperty()
    tao_datasetproperty_184.name = u'posz'
    tao_datasetproperty_184.units = u'10+6pc/h'
    tao_datasetproperty_184.label = u'z'
    tao_datasetproperty_184.dataset = tao_dataset_1
    tao_datasetproperty_184.data_type = 1L
    tao_datasetproperty_184.is_computed = False
    tao_datasetproperty_184.is_filter = True
    tao_datasetproperty_184.is_output = True
    tao_datasetproperty_184.description = u'Z coordinate in the selected box/cone'
    tao_datasetproperty_184.group = u'Positions & Velocities'
    tao_datasetproperty_184.order = 6L
    tao_datasetproperty_184.is_index = False
    tao_datasetproperty_184.is_primary = False
    tao_datasetproperty_184.flags = 3L
    tao_datasetproperty_184 = save_or_locate(tao_datasetproperty_184)

    tao_datasetproperty_185 = DataSetProperty()
    tao_datasetproperty_185.name = u'posz'
    tao_datasetproperty_185.units = u'10+6pc/h'
    tao_datasetproperty_185.label = u'z'
    tao_datasetproperty_185.dataset = tao_dataset_2
    tao_datasetproperty_185.data_type = 1L
    tao_datasetproperty_185.is_computed = False
    tao_datasetproperty_185.is_filter = True
    tao_datasetproperty_185.is_output = True
    tao_datasetproperty_185.description = u'Z coordinate in the selected box/cone'
    tao_datasetproperty_185.group = u'Positions & Velocities'
    tao_datasetproperty_185.order = 6L
    tao_datasetproperty_185.is_index = False
    tao_datasetproperty_185.is_primary = False
    tao_datasetproperty_185.flags = 3L
    tao_datasetproperty_185 = save_or_locate(tao_datasetproperty_185)

    tao_datasetproperty_186 = DataSetProperty()
    tao_datasetproperty_186.name = u'posz'
    tao_datasetproperty_186.units = u'10+6pc/h'
    tao_datasetproperty_186.label = u'z'
    tao_datasetproperty_186.dataset = tao_dataset_3
    tao_datasetproperty_186.data_type = 1L
    tao_datasetproperty_186.is_computed = False
    tao_datasetproperty_186.is_filter = True
    tao_datasetproperty_186.is_output = True
    tao_datasetproperty_186.description = u'Z coordinate in the selected box/cone'
    tao_datasetproperty_186.group = u'Positions & Velocities'
    tao_datasetproperty_186.order = 6L
    tao_datasetproperty_186.is_index = False
    tao_datasetproperty_186.is_primary = False
    tao_datasetproperty_186.flags = 3L
    tao_datasetproperty_186 = save_or_locate(tao_datasetproperty_186)

    tao_datasetproperty_187 = DataSetProperty()
    tao_datasetproperty_187.name = u'posz'
    tao_datasetproperty_187.units = u'10+6pc/h'
    tao_datasetproperty_187.label = u'z'
    tao_datasetproperty_187.dataset = tao_dataset_4
    tao_datasetproperty_187.data_type = 1L
    tao_datasetproperty_187.is_computed = False
    tao_datasetproperty_187.is_filter = True
    tao_datasetproperty_187.is_output = True
    tao_datasetproperty_187.description = u'Z coordinate in the selected box/cone'
    tao_datasetproperty_187.group = u'Positions & Velocities'
    tao_datasetproperty_187.order = 6L
    tao_datasetproperty_187.is_index = False
    tao_datasetproperty_187.is_primary = False
    tao_datasetproperty_187.flags = 3L
    tao_datasetproperty_187 = save_or_locate(tao_datasetproperty_187)

    tao_datasetproperty_188 = DataSetProperty()
    tao_datasetproperty_188.name = u'velx'
    tao_datasetproperty_188.units = u'km/s'
    tao_datasetproperty_188.label = u'x Velocity'
    tao_datasetproperty_188.dataset = tao_dataset_1
    tao_datasetproperty_188.data_type = 1L
    tao_datasetproperty_188.is_computed = False
    tao_datasetproperty_188.is_filter = True
    tao_datasetproperty_188.is_output = True
    tao_datasetproperty_188.description = u'X component of the galaxy/halo velocity'
    tao_datasetproperty_188.group = u'Positions & Velocities'
    tao_datasetproperty_188.order = 7L
    tao_datasetproperty_188.is_index = False
    tao_datasetproperty_188.is_primary = False
    tao_datasetproperty_188.flags = 3L
    tao_datasetproperty_188 = save_or_locate(tao_datasetproperty_188)

    tao_datasetproperty_189 = DataSetProperty()
    tao_datasetproperty_189.name = u'velx'
    tao_datasetproperty_189.units = u'km/s'
    tao_datasetproperty_189.label = u'x Velocity'
    tao_datasetproperty_189.dataset = tao_dataset_2
    tao_datasetproperty_189.data_type = 1L
    tao_datasetproperty_189.is_computed = False
    tao_datasetproperty_189.is_filter = True
    tao_datasetproperty_189.is_output = True
    tao_datasetproperty_189.description = u'X component of the galaxy/halo velocity'
    tao_datasetproperty_189.group = u'Positions & Velocities'
    tao_datasetproperty_189.order = 7L
    tao_datasetproperty_189.is_index = False
    tao_datasetproperty_189.is_primary = False
    tao_datasetproperty_189.flags = 3L
    tao_datasetproperty_189 = save_or_locate(tao_datasetproperty_189)

    tao_datasetproperty_190 = DataSetProperty()
    tao_datasetproperty_190.name = u'velx'
    tao_datasetproperty_190.units = u'km/s'
    tao_datasetproperty_190.label = u'x Velocity'
    tao_datasetproperty_190.dataset = tao_dataset_3
    tao_datasetproperty_190.data_type = 1L
    tao_datasetproperty_190.is_computed = False
    tao_datasetproperty_190.is_filter = True
    tao_datasetproperty_190.is_output = True
    tao_datasetproperty_190.description = u'X component of the galaxy/halo velocity'
    tao_datasetproperty_190.group = u'Positions & Velocities'
    tao_datasetproperty_190.order = 7L
    tao_datasetproperty_190.is_index = False
    tao_datasetproperty_190.is_primary = False
    tao_datasetproperty_190.flags = 3L
    tao_datasetproperty_190 = save_or_locate(tao_datasetproperty_190)

    tao_datasetproperty_191 = DataSetProperty()
    tao_datasetproperty_191.name = u'vely'
    tao_datasetproperty_191.units = u'km/s'
    tao_datasetproperty_191.label = u'y Velocity'
    tao_datasetproperty_191.dataset = tao_dataset_1
    tao_datasetproperty_191.data_type = 1L
    tao_datasetproperty_191.is_computed = False
    tao_datasetproperty_191.is_filter = True
    tao_datasetproperty_191.is_output = True
    tao_datasetproperty_191.description = u'Y component of the galaxy/halo velocity'
    tao_datasetproperty_191.group = u'Positions & Velocities'
    tao_datasetproperty_191.order = 8L
    tao_datasetproperty_191.is_index = False
    tao_datasetproperty_191.is_primary = False
    tao_datasetproperty_191.flags = 3L
    tao_datasetproperty_191 = save_or_locate(tao_datasetproperty_191)

    tao_datasetproperty_192 = DataSetProperty()
    tao_datasetproperty_192.name = u'vely'
    tao_datasetproperty_192.units = u'km/s'
    tao_datasetproperty_192.label = u'y Velocity'
    tao_datasetproperty_192.dataset = tao_dataset_2
    tao_datasetproperty_192.data_type = 1L
    tao_datasetproperty_192.is_computed = False
    tao_datasetproperty_192.is_filter = True
    tao_datasetproperty_192.is_output = True
    tao_datasetproperty_192.description = u'Y component of the galaxy/halo velocity'
    tao_datasetproperty_192.group = u'Positions & Velocities'
    tao_datasetproperty_192.order = 8L
    tao_datasetproperty_192.is_index = False
    tao_datasetproperty_192.is_primary = False
    tao_datasetproperty_192.flags = 3L
    tao_datasetproperty_192 = save_or_locate(tao_datasetproperty_192)

    tao_datasetproperty_193 = DataSetProperty()
    tao_datasetproperty_193.name = u'vely'
    tao_datasetproperty_193.units = u'km/s'
    tao_datasetproperty_193.label = u'y Velocity'
    tao_datasetproperty_193.dataset = tao_dataset_3
    tao_datasetproperty_193.data_type = 1L
    tao_datasetproperty_193.is_computed = False
    tao_datasetproperty_193.is_filter = True
    tao_datasetproperty_193.is_output = True
    tao_datasetproperty_193.description = u'Y component of the galaxy/halo velocity'
    tao_datasetproperty_193.group = u'Positions & Velocities'
    tao_datasetproperty_193.order = 8L
    tao_datasetproperty_193.is_index = False
    tao_datasetproperty_193.is_primary = False
    tao_datasetproperty_193.flags = 3L
    tao_datasetproperty_193 = save_or_locate(tao_datasetproperty_193)

    tao_datasetproperty_194 = DataSetProperty()
    tao_datasetproperty_194.name = u'velz'
    tao_datasetproperty_194.units = u'km/s'
    tao_datasetproperty_194.label = u'z Velocity'
    tao_datasetproperty_194.dataset = tao_dataset_1
    tao_datasetproperty_194.data_type = 1L
    tao_datasetproperty_194.is_computed = False
    tao_datasetproperty_194.is_filter = True
    tao_datasetproperty_194.is_output = True
    tao_datasetproperty_194.description = u'Z component of the galaxy/halo velocity'
    tao_datasetproperty_194.group = u'Positions & Velocities'
    tao_datasetproperty_194.order = 9L
    tao_datasetproperty_194.is_index = False
    tao_datasetproperty_194.is_primary = False
    tao_datasetproperty_194.flags = 3L
    tao_datasetproperty_194 = save_or_locate(tao_datasetproperty_194)

    tao_datasetproperty_195 = DataSetProperty()
    tao_datasetproperty_195.name = u'velz'
    tao_datasetproperty_195.units = u'km/s'
    tao_datasetproperty_195.label = u'z Velocity'
    tao_datasetproperty_195.dataset = tao_dataset_2
    tao_datasetproperty_195.data_type = 1L
    tao_datasetproperty_195.is_computed = False
    tao_datasetproperty_195.is_filter = True
    tao_datasetproperty_195.is_output = True
    tao_datasetproperty_195.description = u'Z component of the galaxy/halo velocity'
    tao_datasetproperty_195.group = u'Positions & Velocities'
    tao_datasetproperty_195.order = 9L
    tao_datasetproperty_195.is_index = False
    tao_datasetproperty_195.is_primary = False
    tao_datasetproperty_195.flags = 3L
    tao_datasetproperty_195 = save_or_locate(tao_datasetproperty_195)

    tao_datasetproperty_196 = DataSetProperty()
    tao_datasetproperty_196.name = u'velz'
    tao_datasetproperty_196.units = u'km/s'
    tao_datasetproperty_196.label = u'z Velocity'
    tao_datasetproperty_196.dataset = tao_dataset_3
    tao_datasetproperty_196.data_type = 1L
    tao_datasetproperty_196.is_computed = False
    tao_datasetproperty_196.is_filter = True
    tao_datasetproperty_196.is_output = True
    tao_datasetproperty_196.description = u'Z component of the galaxy/halo velocity'
    tao_datasetproperty_196.group = u'Positions & Velocities'
    tao_datasetproperty_196.order = 9L
    tao_datasetproperty_196.is_index = False
    tao_datasetproperty_196.is_primary = False
    tao_datasetproperty_196.flags = 3L
    tao_datasetproperty_196 = save_or_locate(tao_datasetproperty_196)

    tao_datasetproperty_197 = DataSetProperty()
    tao_datasetproperty_197.name = u'snapnum'
    tao_datasetproperty_197.units = u''
    tao_datasetproperty_197.label = u'Snapshot Number'
    tao_datasetproperty_197.dataset = tao_dataset_1
    tao_datasetproperty_197.data_type = 0L
    tao_datasetproperty_197.is_computed = False
    tao_datasetproperty_197.is_filter = False
    tao_datasetproperty_197.is_output = True
    tao_datasetproperty_197.description = u'Simulation snapshot number'
    tao_datasetproperty_197.group = u'Simulation'
    tao_datasetproperty_197.order = 1L
    tao_datasetproperty_197.is_index = False
    tao_datasetproperty_197.is_primary = False
    tao_datasetproperty_197.flags = 3L
    tao_datasetproperty_197 = save_or_locate(tao_datasetproperty_197)

    tao_datasetproperty_198 = DataSetProperty()
    tao_datasetproperty_198.name = u'snapnum'
    tao_datasetproperty_198.units = u''
    tao_datasetproperty_198.label = u'Snapshot Number'
    tao_datasetproperty_198.dataset = tao_dataset_2
    tao_datasetproperty_198.data_type = 0L
    tao_datasetproperty_198.is_computed = False
    tao_datasetproperty_198.is_filter = False
    tao_datasetproperty_198.is_output = True
    tao_datasetproperty_198.description = u'Simulation snapshot number'
    tao_datasetproperty_198.group = u'Simulation'
    tao_datasetproperty_198.order = 1L
    tao_datasetproperty_198.is_index = False
    tao_datasetproperty_198.is_primary = False
    tao_datasetproperty_198.flags = 3L
    tao_datasetproperty_198 = save_or_locate(tao_datasetproperty_198)

    tao_datasetproperty_199 = DataSetProperty()
    tao_datasetproperty_199.name = u'snapnum'
    tao_datasetproperty_199.units = u''
    tao_datasetproperty_199.label = u'Snapshot Number'
    tao_datasetproperty_199.dataset = tao_dataset_3
    tao_datasetproperty_199.data_type = 0L
    tao_datasetproperty_199.is_computed = False
    tao_datasetproperty_199.is_filter = False
    tao_datasetproperty_199.is_output = True
    tao_datasetproperty_199.description = u'Simulation snapshot number'
    tao_datasetproperty_199.group = u'Simulation'
    tao_datasetproperty_199.order = 1L
    tao_datasetproperty_199.is_index = False
    tao_datasetproperty_199.is_primary = False
    tao_datasetproperty_199.flags = 3L
    tao_datasetproperty_199 = save_or_locate(tao_datasetproperty_199)

    tao_datasetproperty_200 = DataSetProperty()
    tao_datasetproperty_200.name = u'globalindex'
    tao_datasetproperty_200.units = u''
    tao_datasetproperty_200.label = u'Galaxy ID'
    tao_datasetproperty_200.dataset = tao_dataset_1
    tao_datasetproperty_200.data_type = 2L
    tao_datasetproperty_200.is_computed = False
    tao_datasetproperty_200.is_filter = False
    tao_datasetproperty_200.is_output = True
    tao_datasetproperty_200.description = u'Galaxy ID'
    tao_datasetproperty_200.group = u'Simulation'
    tao_datasetproperty_200.order = 2L
    tao_datasetproperty_200.is_index = False
    tao_datasetproperty_200.is_primary = False
    tao_datasetproperty_200.flags = 3L
    tao_datasetproperty_200 = save_or_locate(tao_datasetproperty_200)

    tao_datasetproperty_201 = DataSetProperty()
    tao_datasetproperty_201.name = u'globalindex'
    tao_datasetproperty_201.units = u''
    tao_datasetproperty_201.label = u'Galaxy ID'
    tao_datasetproperty_201.dataset = tao_dataset_2
    tao_datasetproperty_201.data_type = 2L
    tao_datasetproperty_201.is_computed = False
    tao_datasetproperty_201.is_filter = False
    tao_datasetproperty_201.is_output = True
    tao_datasetproperty_201.description = u'Galaxy ID'
    tao_datasetproperty_201.group = u'Simulation'
    tao_datasetproperty_201.order = 2L
    tao_datasetproperty_201.is_index = False
    tao_datasetproperty_201.is_primary = False
    tao_datasetproperty_201.flags = 3L
    tao_datasetproperty_201 = save_or_locate(tao_datasetproperty_201)

    tao_datasetproperty_202 = DataSetProperty()
    tao_datasetproperty_202.name = u'globalindex'
    tao_datasetproperty_202.units = u''
    tao_datasetproperty_202.label = u'Galaxy ID'
    tao_datasetproperty_202.dataset = tao_dataset_3
    tao_datasetproperty_202.data_type = 2L
    tao_datasetproperty_202.is_computed = False
    tao_datasetproperty_202.is_filter = False
    tao_datasetproperty_202.is_output = True
    tao_datasetproperty_202.description = u'Galaxy ID'
    tao_datasetproperty_202.group = u'Simulation'
    tao_datasetproperty_202.order = 2L
    tao_datasetproperty_202.is_index = False
    tao_datasetproperty_202.is_primary = False
    tao_datasetproperty_202.flags = 3L
    tao_datasetproperty_202 = save_or_locate(tao_datasetproperty_202)

    tao_datasetproperty_203 = DataSetProperty()
    tao_datasetproperty_203.name = u'haloindex'
    tao_datasetproperty_203.units = u''
    tao_datasetproperty_203.label = u'Halo ID'
    tao_datasetproperty_203.dataset = tao_dataset_1
    tao_datasetproperty_203.data_type = 0L
    tao_datasetproperty_203.is_computed = False
    tao_datasetproperty_203.is_filter = False
    tao_datasetproperty_203.is_output = True
    tao_datasetproperty_203.description = u'(sub)Halo ID'
    tao_datasetproperty_203.group = u'Simulation'
    tao_datasetproperty_203.order = 3L
    tao_datasetproperty_203.is_index = False
    tao_datasetproperty_203.is_primary = False
    tao_datasetproperty_203.flags = 3L
    tao_datasetproperty_203 = save_or_locate(tao_datasetproperty_203)

    tao_datasetproperty_204 = DataSetProperty()
    tao_datasetproperty_204.name = u'haloindex'
    tao_datasetproperty_204.units = u''
    tao_datasetproperty_204.label = u'Halo ID'
    tao_datasetproperty_204.dataset = tao_dataset_2
    tao_datasetproperty_204.data_type = 0L
    tao_datasetproperty_204.is_computed = False
    tao_datasetproperty_204.is_filter = False
    tao_datasetproperty_204.is_output = True
    tao_datasetproperty_204.description = u'(sub)Halo ID'
    tao_datasetproperty_204.group = u'Simulation'
    tao_datasetproperty_204.order = 3L
    tao_datasetproperty_204.is_index = False
    tao_datasetproperty_204.is_primary = False
    tao_datasetproperty_204.flags = 3L
    tao_datasetproperty_204 = save_or_locate(tao_datasetproperty_204)

    tao_datasetproperty_205 = DataSetProperty()
    tao_datasetproperty_205.name = u'haloindex'
    tao_datasetproperty_205.units = u''
    tao_datasetproperty_205.label = u'Halo ID'
    tao_datasetproperty_205.dataset = tao_dataset_3
    tao_datasetproperty_205.data_type = 0L
    tao_datasetproperty_205.is_computed = False
    tao_datasetproperty_205.is_filter = False
    tao_datasetproperty_205.is_output = True
    tao_datasetproperty_205.description = u'(sub)Halo ID'
    tao_datasetproperty_205.group = u'Simulation'
    tao_datasetproperty_205.order = 3L
    tao_datasetproperty_205.is_index = False
    tao_datasetproperty_205.is_primary = False
    tao_datasetproperty_205.flags = 3L
    tao_datasetproperty_205 = save_or_locate(tao_datasetproperty_205)

    tao_datasetproperty_206 = DataSetProperty()
    tao_datasetproperty_206.name = u'centralgal'
    tao_datasetproperty_206.units = u''
    tao_datasetproperty_206.label = u'Central Galaxy ID'
    tao_datasetproperty_206.dataset = tao_dataset_1
    tao_datasetproperty_206.data_type = 0L
    tao_datasetproperty_206.is_computed = False
    tao_datasetproperty_206.is_filter = False
    tao_datasetproperty_206.is_output = True
    tao_datasetproperty_206.description = u'Central galaxy ID'
    tao_datasetproperty_206.group = u'Simulation'
    tao_datasetproperty_206.order = 4L
    tao_datasetproperty_206.is_index = False
    tao_datasetproperty_206.is_primary = False
    tao_datasetproperty_206.flags = 3L
    tao_datasetproperty_206 = save_or_locate(tao_datasetproperty_206)

    tao_datasetproperty_207 = DataSetProperty()
    tao_datasetproperty_207.name = u'centralgal'
    tao_datasetproperty_207.units = u''
    tao_datasetproperty_207.label = u'Central Galaxy ID'
    tao_datasetproperty_207.dataset = tao_dataset_2
    tao_datasetproperty_207.data_type = 0L
    tao_datasetproperty_207.is_computed = False
    tao_datasetproperty_207.is_filter = False
    tao_datasetproperty_207.is_output = True
    tao_datasetproperty_207.description = u'Central galaxy ID'
    tao_datasetproperty_207.group = u'Simulation'
    tao_datasetproperty_207.order = 4L
    tao_datasetproperty_207.is_index = False
    tao_datasetproperty_207.is_primary = False
    tao_datasetproperty_207.flags = 3L
    tao_datasetproperty_207 = save_or_locate(tao_datasetproperty_207)

    tao_datasetproperty_208 = DataSetProperty()
    tao_datasetproperty_208.name = u'centralgal'
    tao_datasetproperty_208.units = u''
    tao_datasetproperty_208.label = u'Central Galaxy ID'
    tao_datasetproperty_208.dataset = tao_dataset_3
    tao_datasetproperty_208.data_type = 0L
    tao_datasetproperty_208.is_computed = False
    tao_datasetproperty_208.is_filter = False
    tao_datasetproperty_208.is_output = True
    tao_datasetproperty_208.description = u'Central galaxy ID'
    tao_datasetproperty_208.group = u'Simulation'
    tao_datasetproperty_208.order = 4L
    tao_datasetproperty_208.is_index = False
    tao_datasetproperty_208.is_primary = False
    tao_datasetproperty_208.flags = 3L
    tao_datasetproperty_208 = save_or_locate(tao_datasetproperty_208)

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

    tao_snapshot_310 = Snapshot()
    tao_snapshot_310.dataset = tao_dataset_4
    tao_snapshot_310.redshift = Decimal('0E-10')
    tao_snapshot_310 = save_or_locate(tao_snapshot_310)

    tao_snapshot_311 = Snapshot()
    tao_snapshot_311.dataset = tao_dataset_4
    tao_snapshot_311.redshift = Decimal('0.0199325417')
    tao_snapshot_311 = save_or_locate(tao_snapshot_311)

    tao_snapshot_312 = Snapshot()
    tao_snapshot_312.dataset = tao_dataset_4
    tao_snapshot_312.redshift = Decimal('0.0414030615')
    tao_snapshot_312 = save_or_locate(tao_snapshot_312)

    tao_snapshot_313 = Snapshot()
    tao_snapshot_313.dataset = tao_dataset_4
    tao_snapshot_313.redshift = Decimal('0.0644933969')
    tao_snapshot_313 = save_or_locate(tao_snapshot_313)

    tao_snapshot_314 = Snapshot()
    tao_snapshot_314.dataset = tao_dataset_4
    tao_snapshot_314.redshift = Decimal('0.0892878345')
    tao_snapshot_314 = save_or_locate(tao_snapshot_314)

    tao_snapshot_315 = Snapshot()
    tao_snapshot_315.dataset = tao_dataset_4
    tao_snapshot_315.redshift = Decimal('0.1158833723')
    tao_snapshot_315 = save_or_locate(tao_snapshot_315)

    tao_snapshot_316 = Snapshot()
    tao_snapshot_316.dataset = tao_dataset_4
    tao_snapshot_316.redshift = Decimal('0.1443834234')
    tao_snapshot_316 = save_or_locate(tao_snapshot_316)

    tao_snapshot_317 = Snapshot()
    tao_snapshot_317.dataset = tao_dataset_4
    tao_snapshot_317.redshift = Decimal('0.1748976077')
    tao_snapshot_317 = save_or_locate(tao_snapshot_317)

    tao_snapshot_318 = Snapshot()
    tao_snapshot_318.dataset = tao_dataset_4
    tao_snapshot_318.redshift = Decimal('0.2075486280')
    tao_snapshot_318 = save_or_locate(tao_snapshot_318)

    tao_snapshot_319 = Snapshot()
    tao_snapshot_319.dataset = tao_dataset_4
    tao_snapshot_319.redshift = Decimal('0.2424690843')
    tao_snapshot_319 = save_or_locate(tao_snapshot_319)

    tao_snapshot_320 = Snapshot()
    tao_snapshot_320.dataset = tao_dataset_4
    tao_snapshot_320.redshift = Decimal('0.2798017843')
    tao_snapshot_320 = save_or_locate(tao_snapshot_320)

    tao_snapshot_321 = Snapshot()
    tao_snapshot_321.dataset = tao_dataset_4
    tao_snapshot_321.redshift = Decimal('0.3197034362')
    tao_snapshot_321 = save_or_locate(tao_snapshot_321)

    tao_snapshot_322 = Snapshot()
    tao_snapshot_322.dataset = tao_dataset_4
    tao_snapshot_322.redshift = Decimal('0.3623402826')
    tao_snapshot_322 = save_or_locate(tao_snapshot_322)

    tao_snapshot_323 = Snapshot()
    tao_snapshot_323.dataset = tao_dataset_4
    tao_snapshot_323.redshift = Decimal('0.4078994422')
    tao_snapshot_323 = save_or_locate(tao_snapshot_323)

    tao_snapshot_324 = Snapshot()
    tao_snapshot_324.dataset = tao_dataset_4
    tao_snapshot_324.redshift = Decimal('0.4565772474')
    tao_snapshot_324 = save_or_locate(tao_snapshot_324)

    tao_snapshot_325 = Snapshot()
    tao_snapshot_325.dataset = tao_dataset_4
    tao_snapshot_325.redshift = Decimal('0.5085914282')
    tao_snapshot_325 = save_or_locate(tao_snapshot_325)

    tao_snapshot_326 = Snapshot()
    tao_snapshot_326.dataset = tao_dataset_4
    tao_snapshot_326.redshift = Decimal('0.5641766018')
    tao_snapshot_326 = save_or_locate(tao_snapshot_326)

    tao_snapshot_327 = Snapshot()
    tao_snapshot_327.dataset = tao_dataset_4
    tao_snapshot_327.redshift = Decimal('0.6235901149')
    tao_snapshot_327 = save_or_locate(tao_snapshot_327)

    tao_snapshot_328 = Snapshot()
    tao_snapshot_328.dataset = tao_dataset_4
    tao_snapshot_328.redshift = Decimal('0.6871088016')
    tao_snapshot_328 = save_or_locate(tao_snapshot_328)

    tao_snapshot_329 = Snapshot()
    tao_snapshot_329.dataset = tao_dataset_4
    tao_snapshot_329.redshift = Decimal('0.7550356360')
    tao_snapshot_329 = save_or_locate(tao_snapshot_329)

    tao_snapshot_330 = Snapshot()
    tao_snapshot_330.dataset = tao_dataset_4
    tao_snapshot_330.redshift = Decimal('0.8276991461')
    tao_snapshot_330 = save_or_locate(tao_snapshot_330)

    tao_snapshot_331 = Snapshot()
    tao_snapshot_331.dataset = tao_dataset_4
    tao_snapshot_331.redshift = Decimal('0.9054623890')
    tao_snapshot_331 = save_or_locate(tao_snapshot_331)

    tao_snapshot_332 = Snapshot()
    tao_snapshot_332.dataset = tao_dataset_4
    tao_snapshot_332.redshift = Decimal('0.9887081153')
    tao_snapshot_332 = save_or_locate(tao_snapshot_332)

    tao_snapshot_333 = Snapshot()
    tao_snapshot_333.dataset = tao_dataset_4
    tao_snapshot_333.redshift = Decimal('1.0778745836')
    tao_snapshot_333 = save_or_locate(tao_snapshot_333)

    tao_snapshot_334 = Snapshot()
    tao_snapshot_334.dataset = tao_dataset_4
    tao_snapshot_334.redshift = Decimal('1.1734169374')
    tao_snapshot_334 = save_or_locate(tao_snapshot_334)

    tao_snapshot_335 = Snapshot()
    tao_snapshot_335.dataset = tao_dataset_4
    tao_snapshot_335.redshift = Decimal('1.2758462165')
    tao_snapshot_335 = save_or_locate(tao_snapshot_335)

    tao_snapshot_336 = Snapshot()
    tao_snapshot_336.dataset = tao_dataset_4
    tao_snapshot_336.redshift = Decimal('1.3857181369')
    tao_snapshot_336 = save_or_locate(tao_snapshot_336)

    tao_snapshot_337 = Snapshot()
    tao_snapshot_337.dataset = tao_dataset_4
    tao_snapshot_337.redshift = Decimal('1.5036365321')
    tao_snapshot_337 = save_or_locate(tao_snapshot_337)

    tao_snapshot_338 = Snapshot()
    tao_snapshot_338.dataset = tao_dataset_4
    tao_snapshot_338.redshift = Decimal('1.6302707338')
    tao_snapshot_338 = save_or_locate(tao_snapshot_338)

    tao_snapshot_339 = Snapshot()
    tao_snapshot_339.dataset = tao_dataset_4
    tao_snapshot_339.redshift = Decimal('1.7663359051')
    tao_snapshot_339 = save_or_locate(tao_snapshot_339)

    tao_snapshot_340 = Snapshot()
    tao_snapshot_340.dataset = tao_dataset_4
    tao_snapshot_340.redshift = Decimal('1.9126326704')
    tao_snapshot_340 = save_or_locate(tao_snapshot_340)

    tao_snapshot_341 = Snapshot()
    tao_snapshot_341.dataset = tao_dataset_4
    tao_snapshot_341.redshift = Decimal('2.0700273232')
    tao_snapshot_341 = save_or_locate(tao_snapshot_341)

    tao_snapshot_342 = Snapshot()
    tao_snapshot_342.dataset = tao_dataset_4
    tao_snapshot_342.redshift = Decimal('2.2394854401')
    tao_snapshot_342 = save_or_locate(tao_snapshot_342)

    tao_snapshot_343 = Snapshot()
    tao_snapshot_343.dataset = tao_dataset_4
    tao_snapshot_343.redshift = Decimal('2.4220441238')
    tao_snapshot_343 = save_or_locate(tao_snapshot_343)

    tao_snapshot_344 = Snapshot()
    tao_snapshot_344.dataset = tao_dataset_4
    tao_snapshot_344.redshift = Decimal('2.6188615062')
    tao_snapshot_344 = save_or_locate(tao_snapshot_344)

    tao_snapshot_345 = Snapshot()
    tao_snapshot_345.dataset = tao_dataset_4
    tao_snapshot_345.redshift = Decimal('2.8311827627')
    tao_snapshot_345 = save_or_locate(tao_snapshot_345)

    tao_snapshot_346 = Snapshot()
    tao_snapshot_346.dataset = tao_dataset_4
    tao_snapshot_346.redshift = Decimal('3.0604190352')
    tao_snapshot_346 = save_or_locate(tao_snapshot_346)

    tao_snapshot_347 = Snapshot()
    tao_snapshot_347.dataset = tao_dataset_4
    tao_snapshot_347.redshift = Decimal('3.3080979317')
    tao_snapshot_347 = save_or_locate(tao_snapshot_347)

    tao_snapshot_348 = Snapshot()
    tao_snapshot_348.dataset = tao_dataset_4
    tao_snapshot_348.redshift = Decimal('3.5759051140')
    tao_snapshot_348 = save_or_locate(tao_snapshot_348)

    tao_snapshot_349 = Snapshot()
    tao_snapshot_349.dataset = tao_dataset_4
    tao_snapshot_349.redshift = Decimal('3.8656828256')
    tao_snapshot_349 = save_or_locate(tao_snapshot_349)

    tao_snapshot_350 = Snapshot()
    tao_snapshot_350.dataset = tao_dataset_4
    tao_snapshot_350.redshift = Decimal('4.1794685865')
    tao_snapshot_350 = save_or_locate(tao_snapshot_350)

    tao_snapshot_351 = Snapshot()
    tao_snapshot_351.dataset = tao_dataset_4
    tao_snapshot_351.redshift = Decimal('4.5195557862')
    tao_snapshot_351 = save_or_locate(tao_snapshot_351)

    tao_snapshot_352 = Snapshot()
    tao_snapshot_352.dataset = tao_dataset_4
    tao_snapshot_352.redshift = Decimal('4.8884492180')
    tao_snapshot_352 = save_or_locate(tao_snapshot_352)

    tao_snapshot_353 = Snapshot()
    tao_snapshot_353.dataset = tao_dataset_4
    tao_snapshot_353.redshift = Decimal('5.2888335472')
    tao_snapshot_353 = save_or_locate(tao_snapshot_353)

    tao_snapshot_354 = Snapshot()
    tao_snapshot_354.dataset = tao_dataset_4
    tao_snapshot_354.redshift = Decimal('5.7238643393')
    tao_snapshot_354 = save_or_locate(tao_snapshot_354)

    tao_snapshot_355 = Snapshot()
    tao_snapshot_355.dataset = tao_dataset_4
    tao_snapshot_355.redshift = Decimal('6.1968333933')
    tao_snapshot_355 = save_or_locate(tao_snapshot_355)

    tao_snapshot_356 = Snapshot()
    tao_snapshot_356.dataset = tao_dataset_4
    tao_snapshot_356.redshift = Decimal('6.7115866590')
    tao_snapshot_356 = save_or_locate(tao_snapshot_356)

    tao_snapshot_357 = Snapshot()
    tao_snapshot_357.dataset = tao_dataset_4
    tao_snapshot_357.redshift = Decimal('7.2721880765')
    tao_snapshot_357 = save_or_locate(tao_snapshot_357)

    tao_snapshot_358 = Snapshot()
    tao_snapshot_358.dataset = tao_dataset_4
    tao_snapshot_358.redshift = Decimal('7.8832036386')
    tao_snapshot_358 = save_or_locate(tao_snapshot_358)

    tao_snapshot_359 = Snapshot()
    tao_snapshot_359.dataset = tao_dataset_4
    tao_snapshot_359.redshift = Decimal('8.5499126183')
    tao_snapshot_359 = save_or_locate(tao_snapshot_359)

    tao_snapshot_360 = Snapshot()
    tao_snapshot_360.dataset = tao_dataset_4
    tao_snapshot_360.redshift = Decimal('9.2779148166')
    tao_snapshot_360 = save_or_locate(tao_snapshot_360)

    tao_snapshot_361 = Snapshot()
    tao_snapshot_361.dataset = tao_dataset_4
    tao_snapshot_361.redshift = Decimal('10.0734613425')
    tao_snapshot_361 = save_or_locate(tao_snapshot_361)

    tao_snapshot_362 = Snapshot()
    tao_snapshot_362.dataset = tao_dataset_4
    tao_snapshot_362.redshift = Decimal('10.9438638400')
    tao_snapshot_362 = save_or_locate(tao_snapshot_362)

    tao_snapshot_363 = Snapshot()
    tao_snapshot_363.dataset = tao_dataset_4
    tao_snapshot_363.redshift = Decimal('11.8965695125')
    tao_snapshot_363 = save_or_locate(tao_snapshot_363)

    tao_snapshot_364 = Snapshot()
    tao_snapshot_364.dataset = tao_dataset_4
    tao_snapshot_364.redshift = Decimal('12.9407795684')
    tao_snapshot_364 = save_or_locate(tao_snapshot_364)

    tao_snapshot_365 = Snapshot()
    tao_snapshot_365.dataset = tao_dataset_4
    tao_snapshot_365.redshift = Decimal('14.0859142818')
    tao_snapshot_365 = save_or_locate(tao_snapshot_365)

    tao_snapshot_366 = Snapshot()
    tao_snapshot_366.dataset = tao_dataset_4
    tao_snapshot_366.redshift = Decimal('15.3430738053')
    tao_snapshot_366 = save_or_locate(tao_snapshot_366)

    tao_snapshot_367 = Snapshot()
    tao_snapshot_367.dataset = tao_dataset_4
    tao_snapshot_367.redshift = Decimal('16.7245254258')
    tao_snapshot_367 = save_or_locate(tao_snapshot_367)

    tao_snapshot_368 = Snapshot()
    tao_snapshot_368.dataset = tao_dataset_4
    tao_snapshot_368.redshift = Decimal('18.2437217358')
    tao_snapshot_368 = save_or_locate(tao_snapshot_368)

    tao_snapshot_369 = Snapshot()
    tao_snapshot_369.dataset = tao_dataset_4
    tao_snapshot_369.redshift = Decimal('19.9156888582')
    tao_snapshot_369 = save_or_locate(tao_snapshot_369)

    tao_snapshot_370 = Snapshot()
    tao_snapshot_370.dataset = tao_dataset_4
    tao_snapshot_370.redshift = Decimal('30.0000620001')
    tao_snapshot_370 = save_or_locate(tao_snapshot_370)

    tao_snapshot_371 = Snapshot()
    tao_snapshot_371.dataset = tao_dataset_4
    tao_snapshot_371.redshift = Decimal('49.9995920033')
    tao_snapshot_371 = save_or_locate(tao_snapshot_371)

    tao_snapshot_372 = Snapshot()
    tao_snapshot_372.dataset = tao_dataset_4
    tao_snapshot_372.redshift = Decimal('79.9978940548')
    tao_snapshot_372 = save_or_locate(tao_snapshot_372)

    tao_snapshot_373 = Snapshot()
    tao_snapshot_373.dataset = tao_dataset_4
    tao_snapshot_373.redshift = Decimal('127.0000000000')
    tao_snapshot_373 = save_or_locate(tao_snapshot_373)


    #Re-processing model: DataSet

    tao_dataset_1.default_filter_field = tao_datasetproperty_51
    tao_dataset_1 = save_or_locate(tao_dataset_1)

    tao_dataset_2.default_filter_field = tao_datasetproperty_52
    tao_dataset_2 = save_or_locate(tao_dataset_2)

    tao_dataset_3.default_filter_field = tao_datasetproperty_53
    tao_dataset_3 = save_or_locate(tao_dataset_3)

    tao_dataset_4.default_filter_field = tao_datasetproperty_1
    tao_dataset_4 = save_or_locate(tao_dataset_4)

    #Re-processing model: DataSetProperty

    #Re-processing model: Snapshot

    #Re-processing model: Job

