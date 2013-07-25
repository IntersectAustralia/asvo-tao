"""
========================
taoui_telescope.forms
========================
"""
from django import forms
from django.utils.translation import ugettext_lazy as _

from form_utils.forms import BetterForm
import form_utils.fields as bf_fields

from tao import datasets
from tao import models as tao_models
from tao.forms import FormsGraph
from tao.widgets import ChoiceFieldWithOtherAttrs, SelectWithOtherAttrs, TwoSidedSelectWidget
from tao.xml_util import module_xpath, module_xpath_iterate


####

class Form(BetterForm):
    EDIT_TEMPLATE = 'taoui_telescope/edit.html'
    MODULE_VERSION = 1
    SUMMARY_TEMPLATE = 'taoui_telescope/summary.html'
    LABEL = 'Telescope'


    def __init__(self, *args, **kwargs):
        self.ui_holder = args[0]
        super(Form, self).__init__(*args[1:], **kwargs)

        default_required = False
        self.fields['apply_telescope'] = forms.BooleanField(required=False, widget=forms.CheckboxInput(), label='Telescope Module')

        ### Image
        self.fields['image_name'] = forms.CharField(required=True, initial='sky.fits')
        self.fields['image_width'] = forms.IntegerField(required=True, initial=1024)
        self.fields['image_height'] = forms.IntegerField(required=True, initial=1024)

        image_type_choices = [('PUPIL_PHASE', 'Pupil Phase'), ('PUPIL_MTF', 'Pupil MTF'), ('PSF_MTF', 'PSF MTF'), ('PSF_FULLRES', 'PSF Full Resoltion'), ('PSF_FINALRES', 'PSF Final Resoltion'), ('SKY_NONOISE', 'Sky No Noise'), ('SKY', 'Sky'), ('GRID', 'Grid')]

        self.fields['image_type'] = forms.ChoiceField(required=True, choices=image_type_choices, initial='SKY')
        self.fields['grid_size'] = forms.IntegerField(required=True, initial=64)

        image_header_choices = [('INTERNAL', 'Internal'), ('FILE', 'File Name')]

        self.fields['image_header'] = forms.ChoiceField(required=True, choices=image_header_choices, initial='INTERNAL')

        ### Detector
        self.fields['gain'] = forms.FloatField(required=True, initial=1.0)
        self.fields['well_capacity'] = forms.IntegerField(required=True, initial=0, help_text="full well capacity in e- (0 = infinite)")
        self.fields['saturation_level'] = forms.IntegerField(required=True, initial=65535, help_text="saturation level (ADU)")
        self.fields['readout_noise'] = forms.FloatField(required=True, initial=1.0, help_text="read-out noise (e-)")
        self.fields['exposure_time'] = forms.FloatField(required=True, initial=300.0, help_text="total exposure time (s)")
        self.fields['mag_zeropoint'] = forms.FloatField(required=True, initial=26.0, help_text='magnitude zero-point ("ADU per second")')

        ### Sampling
        self.fields['pixel_size'] = forms.FloatField(required=True, initial=0.200, help_text="pixel size in arcsec.")
        self.fields['microscan_nstep'] = forms.IntegerField(required=True, initial=1, help_text="number of microscanning steps (1=no mscan)")

        ### PSF
        psf_type_choices = [('INTERNAL', 'Internal'), ('FILE', 'File Name')]

        self.fields['psf_type'] = forms.ChoiceField(required=True, choices=psf_type_choices, initial='INTERNAL')
        self.fields['psf_name'] = forms.CharField(required=True, initial='psf.fits', help_text="Name of the FITS image containing the PSF")

        seeing_type_choices = [('NONE', 'None'), ('LONG_EXPOSURE', 'Long Exposure'), ('SHORT_EXPOSURE', 'Short Exposure')]

        self.fields['seeing_type'] = forms.ChoiceField(required=True, choices=seeing_type_choices, initial='LONG_EXPOSURE')
        self.fields['seeing_fwhm'] = forms.FloatField(required=True, initial=0.7, help_text="FWHM of seeing in arcsec (incl. motion)")
        self.fields['aureole_radius'] = forms.IntegerField(required=True, initial=200, help_text="Range covered by aureole (pix) 0=no aureole")
        self.fields['aureole_sb'] = forms.FloatField(required=True, initial=16.0, help_text="SB (mag/arcsec2) at 1' from a 0-mag star")
        self.fields['psf_oversamp'] = forms.IntegerField(required=True, initial=5, help_text="Oversampling factor / final resolution")
        self.fields['psf_mapsize'] = forms.IntegerField(required=True, initial=1024, help_text="PSF mask size (pixels): must be a power of 2")

        trackerror_type_choices = [('NONE', 'None'), ('DRIFT', 'Drift'), ('JITTER', 'Jitter')]

        self.fields['trackerror_type'] = forms.ChoiceField(label='Track error type', required=True, choices=trackerror_type_choices, initial='NONE', help_text="Tracking error model: NONE, DRIFT or JITTER")
        self.fields['trackerror_maj'] = forms.FloatField(label='Track error major', required=True, initial=0.0, help_text="Tracking RMS error (major axis) (in arcsec)")
        self.fields['trackerror_min'] = forms.FloatField(label='Track error minor', required=True, initial=0.0, help_text="Tracking RMS error (minor axis) (in arcsec)")
        self.fields['trackerror_ang'] = forms.FloatField(label='Track error angle',required=True, initial=0.0, help_text="Tracking angle (in deg, CC/horizontal)")

        ### Pupil Features
        self.fields['m1_diameter'] = forms.FloatField(required=True, initial=3.6, help_text="Diameter of the primary mirror (in meters)")
        self.fields['m2_diameter'] = forms.FloatField(required=True, initial=1.0, help_text="Obstruction diam. from the 2nd mirror in m.")
        self.fields['arm_count'] = forms.FloatField(required=True, initial=4, help_text="Number of spider arms (0 = none)")
        self.fields['arm_thickness'] = forms.FloatField(required=True, initial=20.0, help_text="Thickness of the spider arms (in mm)")
        self.fields['arm_posangle'] = forms.FloatField(required=True, initial=0.0, help_text="Position angle of the spider pattern / AXIS1")
        self.fields['defoc_d80'] = forms.FloatField(required=True, initial=0.0, help_text="Defocusing d80% diameter (arcsec)")
        self.fields['spher_d80'] = forms.FloatField(required=True, initial=0.0, help_text="Spherical d80% diameter (arcsec)")
        self.fields['comax_d80'] = forms.FloatField(required=True, initial=0.0, help_text="Coma along X d80% diameter (arcsec)")
        self.fields['comay_d80'] = forms.FloatField(required=True, initial=0.0, help_text="Coma along Y d80% diameter (arcsec)")
        self.fields['ast00_d80'] = forms.FloatField(required=True, initial=0.0, help_text="0 deg. astigmatism d80% diameter (arcsec)")
        self.fields['ast45_d80'] = forms.FloatField(required=True, initial=0.0, help_text="45 deg. astigmatism d80% diameter (arcsec)")
        self.fields['tri00_d80'] = forms.FloatField(required=True, initial=0.0, help_text="0 deg. triangular d80% diameter (arcsec)")
        self.fields['tri30_d80'] = forms.FloatField(required=True, initial=0.0, help_text="30 deg. triangular d80% diameter (arcsec)")
        self.fields['qua00_d80'] = forms.FloatField(required=True, initial=0.0, help_text="0 deg. quadratic d80% diameter (arcsec)")
        self.fields['qua22_d80'] = forms.FloatField(required=True, initial=0.0, help_text="22.5 deg. quadratic d80% diameter (arcsec)")

        ### Signal
        self.fields['wavelength'] = forms.FloatField(required=True, initial=0.8, help_text="average wavelength analysed (microns)")
        self.fields['back_mag'] = forms.FloatField(required=True, initial=20.0, help_text="background surface brightness (mag/arcsec2)")

        ### Stellar Field
        self.fields['starcount_zp'] = forms.CharField(required=True, initial=3e4, help_text="nb of stars /deg2 brighter than MAG_LIMITS")
        self.fields['starcount_slope'] = forms.FloatField(required=True, initial=0.2, help_text="slope of differential star counts (dexp/mag)")

        self.fields['mag_range_start'] = forms.FloatField(required=True, initial=17.0, help_text="stellar magnitude range allowed")
        self.fields['mag_range_end'] = forms.FloatField(required=True, initial=26.0, help_text="stellar magnitude range allowed")

        ### Random Seeds
        self.fields['seed_motion'] = forms.FloatField(required=True, initial=0, help_text="rand. seed for PSF turbulent motion (0=time)")
        self.fields['seed_starpos'] = forms.FloatField(label='Seed star position', required=True, initial=0, help_text="random seed for star positions (0=time)")

        ### Miscellaneous
        verbose_type_choices = [('QUIET', 'Quiet'), ('NORMAL', 'Normal'), ('FULL', 'Full')]
        self.fields['verbose_type'] = forms.ChoiceField(required=True, choices=verbose_type_choices, initial='NORMAL')
        self.fields['nthreads'] = forms.FloatField(label='Number of threads', required=True, initial=0, help_text="Number of simultaneous threads for")



