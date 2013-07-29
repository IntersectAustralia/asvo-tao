# coding: utf-8

import  workflow
import os, shlex, subprocess, time, logging,sys
import requests
import torque
import dbase
import settingReader # Read the XML settings
import logging
from daemon import Daemon
import signal
import emailreport
import logging, logging.handlers

def BackupLogFile():
        if os.path.exists('log/logfile.log'):
           LogFile=open('log/logfile.log')
           Contents=LogFile.read()
           LogFile.close()
           LogFileBackup=open('log/logfile.log.bak','a')
           LogFileBackup.write(Contents)
           LogFileBackup.close()
           os.remove('log/logfile.log')
def PrepareLogFile():
    LOG_FILENAME = 'log/logfile.log'
    TAOLoger = logging.getLogger() 
    TAOLoger.setLevel(logging.DEBUG)      
    handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=10485760, backupCount=5)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
    TAOLoger.addHandler(handler)




if __name__ == '__main__':
    
    PrepareLogFile()
    #logging.basicConfig(filename='log/logfile.log',level=logging.DEBUG,format='%(asctime)s %(message)s')
    ## Read Running Setting from XML File
    [Options]=settingReader.ParseParams("settings.xml")
    
    ## Define Working Directory and the Sleep time between each Run
    WorkDirectory=Options['WorkFlowSettings:WorkingDir']
    SleepTime=int(Options['WorkFlowSettings:SleepTime'])
    
    
    # Change location to the working directory.
    os.chdir(WorkDirectory)

    
    # Load any existing database information.
    dbaseObj=dbase.DBInterface(Options)
    TorqueObj=torque.TorqueInterface(Options,dbaseObj)
    workflowObj=workflow.WorkFlow(Options,dbaseObj,TorqueObj)
    
    
    
    
    
    
    
    logging.info('-----------------------------------------------------------------')
    logging.info('Workflow Starting')
    
    
    
    
     
    
    UIJobReference=510
    JobParams='''<?xml version='1.0' encoding='utf-8'?>
<tao timestamp="2013-07-01T15:39:42+10:00" xmlns="http://tao.asvo.org.au/schema/module-parameters-v1">
<username>amr</username>
<workflow name="alpha-light-cone-image">
  <schema-version>2.0</schema-version>
  <light-cone id="1">
    <module-version>1</module-version>
    <geometry>light-cone</geometry>
    <simulation>Millennium</simulation>
    <galaxy-model>SAGE</galaxy-model>
    <box-repetition>unique</box-repetition>
    <num-cones>1</num-cones>
    <redshift-min>0.01</redshift-min>
    <redshift-max>0.4</redshift-max>
    <ra-min units="deg">0.0</ra-min>
    <ra-max units="deg">12</ra-max>
    <dec-min units="deg">0.0</dec-min>
    <dec-max units="deg">5</dec-max>
    <output-fields>
      <item description="Galaxy total stellar mass" label="Total Stellar Mass" units="10^10 M/h">stellarmass</item>
      <item description="0=Central, 1=Satellite" label="Galaxy Type">objecttype</item>
      <item description="Stellar disk scale radius" label="Disk Scale Radius" units="Mpc/h">diskscaleradius</item>
      <item description="Total star formation rate in the galaxy" label="Sfr" units="M/yr">sfr</item>
      <item description="Dark matter (sub)halo virial mass" label="Mvir" units="10^10 Mpc/h">mvir</item>
      <item description="Central galaxy dark matter halo Mvir" label="Central Galaxy Mvir" units="10^10 M/h">centralmvir</item>
      <item description="Dark matter halo velocity dispersion" label="Velocity Dispersion" units="km/s">veldisp</item>
      <item description="Total simulation particles in the dark matter halo" label="Total particles">len</item>
      <item description="X coordinate in the selected box/cone" label="x" units="Mpc/h">pos_x</item>
      <item description="Y coordinate in the selected box/cone" label="y" units="Mpc/h">pos_y</item>
      <item description="Z coordinate in the selected box/cone" label="z" units="Mpc/h">pos_z</item>
      <item description="X component of the galaxy/halo velocity" label="x Velocity" units="km/s">velx</item>
      <item description="Y componentt of the galaxy/halo velocity" label="y Velocity" units="km/s">vely</item>
      <item description="Z componentt of the galaxy/halo velocity" label="z Velocity" units="km/s">velz</item>
      <item description="" label="Central Galaxy ID">centralgal</item>
      <item description="" label="FOF Halo Index">fofhaloindex</item>
      <item description="Simulation snapshot number" label="Snapshot Number">snapnum</item>
<item description="" label="Galaxy Index">globalgalaxyid</item>
    </output-fields>
  </light-cone>
  <votable id="5">
    <fields>
<item label="Galaxy Index">globalgalaxyid</item>
      <item label="Total Stellar Mass" units="10^10 M/h">stellarmass</item>
      <item label="Galaxy Type">objecttype</item>
      <item label="Disk Scale Radius" units="Mpc/h">diskscaleradius</item>
      <item label="Sfr" units="M/yr">sfr</item>
      <item label="Mvir" units="10^10 Mpc/h">mvir</item>
      <item label="Central Galaxy Mvir" units="10^10 M/h">centralmvir</item>
      <item label="Velocity Dispersion" units="km/s">veldisp</item>
      <item label="Total particles">len</item>
      <item label="x" units="Mpc/h">pos_x</item>
      <item label="y" units="Mpc/h">pos_y</item>
      <item label="z" units="Mpc/h">pos_z</item>
      <item label="x Velocity" units="km/s">velx</item>
      <item label="y Velocity" units="km/s">vely</item>
      <item label="z Velocity" units="km/s">velz</item>
      <item label="Central Galaxy ID">centralgal</item>
      <item label="FOF Halo Index">fofhaloindex</item>
      <item label="Snapshot Number">snapnum</item>
      <item label="SDSS g (Apparent)">SDSS/sdss_g.dati_apparent</item>
      <item label="SDSS g (Absolute)">SDSS/sdss_g.dati_absolute</item>
      <item label="SDSS i (Apparent)">SDSS/sdss_i.dati_apparent</item>
      <item label="SDSS i (Absolute)">SDSS/sdss_i.dati_absolute</item>
      <item label="SDSS r (Apparent)">SDSS/sdss_r.dati_apparent</item>
      <item label="SDSS r (Absolute)">SDSS/sdss_r.dati_absolute</item>
      <item label="SDSS u (Apparent)">SDSS/sdss_u.dati_apparent</item>
      <item label="SDSS u (Absolute)">SDSS/sdss_u.dati_absolute</item>
      <item label="SDSS z (Apparent)">SDSS/sdss_z.dati_apparent</item>
      <item label="SDSS z (Absolute)">SDSS/sdss_z.dati_absolute</item>
      <item label="UKIRT H (Apparent)">UKIRT/H_filter.dati_apparent</item>
      <item label="UKIRT H (Absolute)">UKIRT/H_filter.dati_absolute</item>
      <item label="UKIRT J (Apparent)">UKIRT/J_filter.dati_apparent</item>
      <item label="UKIRT J (Absolute)">UKIRT/J_filter.dati_absolute</item>
      <item label="UKIRT K (Apparent)">UKIRT/K_filter.dati_apparent</item>
      <item label="UKIRT K (Absolute)">UKIRT/K_filter.dati_absolute</item>
    </fields>
    <parents>
      <item>4</item>
    </parents>
    <module-version>1</module-version>
    <filename>tao.output.xml</filename>
  </votable>
  <sed id="2">
    <module-version>1</module-version>
    <parents>
      <item>1</item>
    </parents>
    <single-stellar-population-model>ssp.ssz</single-stellar-population-model>
  </sed>
   <filter id="4">
      <module-version>1</module-version>
      <parents>
        <item>3</item>
      </parents>
      <bandpass-filters>
        <item description="&lt;p&gt;Sloan Digital Sky Survey (SDSS) g&lt;/p&gt;&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/SDSS_sdss_g.dati.html&quot;&gt;SDSS g&lt;/a&gt;.&lt;/p&gt;" label="SDSS g" selected="apparent,absolute">SDSS/sdss_g.dati</item>
        <item description="&lt;p&gt;Sloan Digital Sky Survey (SDSS) i&lt;/p&gt;&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/SDSS_sdss_i.dati.html&quot;&gt;SDSS i&lt;/a&gt;.&lt;/p&gt;" label="SDSS i" selected="apparent,absolute">SDSS/sdss_i.dati</item>
        <item description="&lt;p&gt;Sloan Digital Sky Survey (SDSS) r&lt;/p&gt;&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/SDSS_sdss_r.dati.html&quot;&gt;SDSS r&lt;/a&gt;.&lt;/p&gt;" label="SDSS r" selected="apparent,absolute">SDSS/sdss_r.dati</item>
        <item description="&lt;p&gt;Sloan Digital Sky Survey (SDSS) u&lt;/p&gt;&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/SDSS_sdss_u.dati.html&quot;&gt;SDSS u&lt;/a&gt;.&lt;/p&gt;" label="SDSS u" selected="apparent,absolute">SDSS/sdss_u.dati</item>
        <item description="&lt;p&gt;Sloan Digital Sky Survey (SDSS) z&lt;/p&gt;&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/SDSS_sdss_z.dati.html&quot;&gt;SDSS z&lt;/a&gt;.&lt;/p&gt;" label="SDSS z" selected="apparent,absolute">SDSS/sdss_z.dati</item>
        <item description="&lt;p&gt;UKIRT Infrared Deep Sky Survey, H band&lt;/p&gt;&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/UKIRT_H_filter.dati.html&quot;&gt;UKIRT H&lt;/a&gt;.&lt;/p&gt;" label="UKIRT H" selected="apparent,absolute">UKIRT/H_filter.dati</item>
        <item description="&lt;p&gt;UKIRT Infrared Deep Sky Survey, J band&lt;/p&gt;&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/UKIRT_J_filter.dati.html&quot;&gt;UKIRT J&lt;/a&gt;.&lt;/p&gt;" label="UKIRT J" selected="apparent,absolute">UKIRT/J_filter.dati</item>
        <item description="&lt;p&gt;UKIRT Infrared Deep Sky Survey, K band&lt;/p&gt;&#10;&lt;p&gt;Additional Details: &lt;a href=&quot;../static/docs/bpfilters/UKIRT_K_filter.dati.html&quot;&gt;UKIRT K&lt;/a&gt;.&lt;/p&gt;" label="UKIRT K" selected="apparent,absolute">UKIRT/K_filter.dati</item>
      </bandpass-filters>
    </filter>
    <dust id="3">
      <module-version>1</module-version>
      <parents>
        <item>2</item>
      </parents>
      <model>Tonini et al. 2012</model>
    </dust>    
  <record-filter>
    <module-version>1</module-version>
    <filter>
      <filter-attribute>stellarmass</filter-attribute>
      <filter-min units="10^10 M/h">0.1</filter-min>
      <filter-max units="10^10 M/h">None</filter-max>
    </filter>
  </record-filter>
</workflow>
<signature>base64encodedsignature</signature>
</tao>'''
    JobDatabase='millennium_full_hdf5_dist'
    JobUserName='amr'
    workflowObj.ProcessNewJob(UIJobReference,JobParams,JobDatabase,JobUserName)
      
    while True:  
        workflowObj.ProcessJobs()
        logging.info("Sleeping for "+str(SleepTime)+" Seconds")
        logging.info('-----------------------------------------------------------------')
        time.sleep(SleepTime)
          
        
        
        
        
                
            
        
        

    

