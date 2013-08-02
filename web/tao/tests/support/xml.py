from lxml import etree, objectify
from tao.xml_util import remove_comments
from tao.tests.support import stripped_joined_lines

def normalise_xml(xmlstring):
    try:
        as_object = etree.fromstring(xmlstring)
    except Exception, e:
        print xmlstring
        raise e
    as_object = remove_comments(as_object)
    normalised_string = etree.tostring(as_object, pretty_print=True)
    return normalised_string

def light_cone_xml(xml_parameters):
    if xml_parameters['catalogue_geometry'] == 'box':
        geometry_fragment = box_geometry_xml(xml_parameters)
    else:
        geometry_fragment = light_cone_geometry_xml(xml_parameters)
    xml_parameters.update({'geometry_fragment': geometry_fragment})
    if 'band_pass_filter_description' not in xml_parameters:
        xml_parameters.update({'band_pass_filter_description': ''})
    xml = stripped_joined_lines("""
            <?xml version="1.0" encoding="UTF-8"?>
            <!-- Using the XML namespace provides a version for future modifiability.  The timestamp allows
                 a researcher to know when this parameter file was generated.  -->
            <tao xmlns="http://tao.asvo.org.au/schema/module-parameters-v1" timestamp="2012-12-20T13:55:36+10:00">

                <!-- Username submitting the job -->
                <username>%(username)s</username>

                <!-- Workflow name identifies which workflow is to be executed.
                     This is currently a placeholder, the name is ignored. -->
                <workflow name="alpha-light-cone-image">

                    <!-- Global Configuration Parameters -->
                    <schema-version>2.0</schema-version>

                    <!-- Light-cone module parameters -->
                    %(geometry_fragment)s

                    <!-- File output module -->
                    <csv id="%(csv_dump_id)s">
                        <fields>
                            <item label="%(output_properties_1_label)s" units="%(output_properties_1_units)s" >%(output_properties_1_name)s</item>
                            <item label="%(output_properties_2_label)s" >%(output_properties_2_name)s</item>
                            <item label="%(output_properties_3_label)s" >%(output_properties_3_name)s</item>
                            <!-- <item label="bandpass (Absolute)">%(band_pass_filter_name)s_absolute</item> -->
                            <item label="bandpass (Apparent)">%(band_pass_filter_name)s_apparent</item>
                        </fields>

                        <!-- Module Version Number -->
                        <module-version>1</module-version>

                        <!-- Output file format -->
                        <filename>tao.output.csv</filename>

                        <parents>
                            <item>%(bandpass_filter_id)s</item>
                        </parents>

                    </csv>

                    <!-- Optional: Spectral Energy Distribution parameters -->
                    <sed id="%(sed_id)s">
                        <!-- Module Version Number -->
                        <module-version>1</module-version>

                        <parents>
                            <item>%(light_cone_id)s</item>
                        </parents>

                        <single-stellar-population-model>%(ssp_name)s</single-stellar-population-model>
                    </sed>

                    <filter id="%(bandpass_filter_id)s">
                        <module-version>1</module-version>
                        <parents>
                            <item>%(dust_id)s</item>
                        </parents>

                        <!-- Bandpass Filters) -->
                        <bandpass-filters>
                            <item description="%(band_pass_filter_description)s" label="%(band_pass_filter_label)s" selected="apparent">%(band_pass_filter_id)s</item>
                        </bandpass-filters>
                    </filter>

                    <dust id="%(dust_id)s">
                        <!-- Module Version Number -->
                        <module-version>1</module-version>
                        <parents>
                            <item>%(sed_id)s</item>
                        </parents>
                        <model>%(dust_model_name)s</model>
                    </dust>

                    <!-- Record Filter -->
                    <record-filter>
                        <!-- Module Version Number -->
                        <module-version>1</module-version>

                        <!-- Note that the units are for readability,
                             no unit conversion is supported.  The consumer of the
                             parameter file should check that the expected units are provided. -->
                        <filter>
                            <filter-attribute>%(filter)s</filter-attribute>
                            <filter-min units="Msun/h">%(filter_min)s</filter-min>
                            <filter-max units="Msun/h">%(filter_max)s</filter-max>
                        </filter>
                    </record-filter>

                    <!-- Image generation module parameters
                    <image-generator>
                        <!- Module Version Number ->
                        <module-version>1</module-version>

                        <!- Image size parameters ->
                        <image-width units="px">1024</image-width>
                        <image-height units="px">1024</image-height>

                        <!- Focal scale parameters ->
                        <focalx units="??">1024</focalx>
                        <focaly units="??">1024</focaly>

                        <!- Image offset parameters ->
                        <image-offsetx units="??">512</image-offsetx>
                        <image-offsety units="??">0</image-offsety>
                    </image-generator> -->

                </workflow>

                <!-- The signature is automatically generated and is intended to be used when running
                     old versions of the science modules (to remove the need for the UI to parse and check
                     every version. -->
                <signature>base64encodedsignature</signature>

            </tao>
        """) % xml_parameters
    return xml

def light_cone_geometry_xml(xml_parameters):
    return stripped_joined_lines("""
                    <light-cone id="%(light_cone_id)s">
                        <!-- Module Version Number -->
                        <module-version>1</module-version>

                        <!-- Is the query a light-cone or box? -->
                        <geometry>light-cone</geometry>

                        <!-- Selected Simuation -->
                        <simulation>%(dark_matter_simulation)s</simulation>

                        <!-- Selected Galaxy Model -->
                        <galaxy-model>%(galaxy_model)s</galaxy-model>

                        <!-- The number of light-cones to generate  -->
                        <box-repetition>%(light_cone_type)s</box-repetition>
                        <num-cones>%(number_of_light_cones)d</num-cones>

                        <!-- The min and max redshifts to filter by -->
                        <redshift-min>%(redshift_min).1f</redshift-min>
                        <redshift-max>%(redshift_max).1f</redshift-max>

                        <!-- RA/Dec range for limiting the light-cone -->
                        <ra-min units="deg">0.0</ra-min>
                        <ra-max units="deg">%(ra_opening_angle).3f</ra-max>
                        <dec-min units="deg">0.0</dec-min>
                        <dec-max units="deg">%(dec_opening_angle).3f</dec-max>

                        <!-- List of fields to be included in the output file -->
                        <output-fields>
                            <item description="%(output_properties_1_description)s" label="%(output_properties_1_label)s" units="%(output_properties_1_units)s">%(output_properties_1_name)s</item>
                            <item description="%(output_properties_2_description)s" label="%(output_properties_2_label)s">%(output_properties_2_name)s</item>
                        </output-fields>

                        <!-- RNG Seed -->
                        <!-- This will be added by the workflow after the job has been completed
                             to enable the job to be repeated.
                             The information stored may change, the intent is to store whatever is
                             required to re-run the job and obtain the same results.
                        <rng-seed>12345678901234567890</rng-seed> -->

                    </light-cone>
    """) % xml_parameters

def box_geometry_xml(xml_parameters):
    return stripped_joined_lines("""
                    <light-cone id="%(light_cone_id)s">
                        <!-- Module Version Number -->
                        <module-version>1</module-version>

                        <!-- Is the query a light-cone or box? -->
                        <geometry>box</geometry>

                        <!-- Selected Simuation -->
                        <simulation>%(dark_matter_simulation)s</simulation>

                        <!-- Selected Galaxy Model -->
                        <galaxy-model>%(galaxy_model)s</galaxy-model>

                        <redshift>%(redshift)s</redshift>
                        <query-box-size units="Mpc">%(box_size)f</query-box-size>

                        <!-- List of fields to be included in the output file -->
                        <output-fields>
                            <item label="%(output_properties_1_label)s" units="%(output_properties_1_units)s">%(output_properties_1_name)s</item>
                            <item label="%(output_properties_2_label)s">%(output_properties_2_name)s</item>
                        </output-fields>

                        <!-- RNG Seed -->
                        <!-- This will be added by the workflow after the job has been completed
                             to enable the job to be repeated.
                             The information stored may change, the intent is to store whatever is
                             required to re-run the job and obtain the same results.
                        <rng-seed>12345678901234567890</rng-seed> -->

                    </light-cone>
    """) % xml_parameters

def fits_output_format_xml(xml_parameters):
    if xml_parameters['catalogue_geometry'] == 'box':
        geometry_fragment = box_geometry_xml(xml_parameters)
    else:
        geometry_fragment = light_cone_geometry_xml(xml_parameters)
    xml_parameters.update({'geometry_fragment': geometry_fragment})
    if 'band_pass_filter_description' not in xml_parameters:
        xml_parameters.update({'band_pass_filter_description': ''})
    xml = stripped_joined_lines("""
            <?xml version="1.0" encoding="UTF-8"?>
            <!-- Using the XML namespace provides a version for future modifiability.  The timestamp allows
                 a researcher to know when this parameter file was generated.  -->
            <tao xmlns="http://tao.asvo.org.au/schema/module-parameters-v1" timestamp="2012-12-20T13:55:36+10:00">

                <!-- Username submitting the job -->
                <username>%(username)s</username>

                <!-- Workflow name identifies which workflow is to be executed.
                     This is currently a placeholder, the name is ignored. -->
                <workflow name="alpha-light-cone-image">

                    <!-- Global Configuration Parameters -->
                    <schema-version>2.0</schema-version>


                    <!-- File output module -->
                    <fits id="%(csv_dump_id)s">
                        <fields>
                            <item label="%(output_properties_1_label)s" units="%(output_properties_1_units)s">%(output_properties_1_name)s</item>
                            <item label="%(output_properties_2_label)s">%(output_properties_2_name)s</item>
                            <!-- <item label="bandpass (Absolute)">%(band_pass_filter_name)s_absolute</item> -->
                            <item label="bandpass (Apparent)">%(band_pass_filter_name)s_apparent</item>
                        </fields>

                        <!-- Module Version Number -->
                        <module-version>1</module-version>

                        <!-- Output file format -->
                        <filename>tao.output.csv</filename>

                        <parents>
                            <item>%(bandpass_filter_id)s</item>
                        </parents>

                    </fits>

                    <!-- Optional: Spectral Energy Distribution parameters -->
                    <sed id="%(sed_id)s">
                        <!-- Module Version Number -->
                        <module-version>1</module-version>

                        <parents>
                            <item>%(light_cone_id)s</item>
                        </parents>

                        <single-stellar-population-model>%(ssp_name)s</single-stellar-population-model>
                    </sed>

                    <filter id="%(bandpass_filter_id)s">
                        <module-version>1</module-version>
                        <parents>
                            <item>%(dust_id)s</item>
                        </parents>

                        <!-- Bandpass Filters) -->
                        <bandpass-filters>
                            <item description="%(band_pass_filter_description)s" label="%(band_pass_filter_label)s" selected="apparent">%(band_pass_filter_id)s</item>
                        </bandpass-filters>
                    </filter>

                    <dust id="%(dust_id)s">
                        <!-- Module Version Number -->
                        <module-version>1</module-version>
                        <parents>
                            <item>%(sed_id)s</item>
                        </parents>
                        <model>%(dust_model_name)s</model>
                    </dust>

                    <!-- Record Filter -->
                    <record-filter>
                        <!-- Module Version Number -->
                        <module-version>1</module-version>

                        <!-- Note that the units are for readability,
                             no unit conversion is supported.  The consumer of the
                             parameter file should check that the expected units are provided. -->
                        <filter>
                            <filter-attribute>%(filter)s</filter-attribute>
                            <filter-min units="Msun/h">%(filter_min)s</filter-min>
                            <filter-max units="Msun/h">%(filter_max)s</filter-max>
                        </filter>
                    </record-filter>

                    <!-- Image generation module parameters
                    <image-generator>
                        <!- Module Version Number ->
                        <module-version>1</module-version>

                        <!- Image size parameters ->
                        <image-width units="px">1024</image-width>
                        <image-height units="px">1024</image-height>

                        <!- Focal scale parameters ->
                        <focalx units="??">1024</focalx>
                        <focaly units="??">1024</focaly>

                        <!- Image offset parameters ->
                        <image-offsetx units="??">512</image-offsetx>
                        <image-offsety units="??">0</image-offsety>
                    </image-generator> -->

                </workflow>

                <!-- The signature is automatically generated and is intended to be used when running
                     old versions of the science modules (to remove the need for the UI to parse and check
                     every version. -->
                <signature>base64encodedsignature</signature>

            </tao>
        """) % xml_parameters
    return xml

class XmlDiffMixin(object):
    """
        This class provides xml diff capabilities
    """
    def assertXmlEqual(self, expected, actual):
        normalised_expected = normalise_xml(expected)
        normalised_actual = normalise_xml(actual)

        expected_lines = normalised_expected.split('\n')
        actual_lines = normalised_actual.split('\n')
        maxDiff = self.maxDiff
        self.maxDiff = None
        self.assertEqual(expected_lines, actual_lines)
        self.maxDiff = maxDiff

