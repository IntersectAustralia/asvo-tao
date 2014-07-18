import h5py
import numpy
import sys
import time



if __name__ == '__main__':
    
    IndexInputFilePath='/lustre/projects/p014_swin/galacticus/small_output.h5'
    DataInputFilePath='/lustre/projects/p014_swin/galacticus_transfer/milliMillennium.hdf5'
    OutputFilePath='/lustre/projects/p014_swin/galacticus/small_output.converted.h5'

    
    print("Start Loading HDF5 File Done....")
    IndexInputFile=h5py.File(IndexInputFilePath,'r')
    DataInputFile=h5py.File(DataInputFilePath,'r')
    OutputFile=h5py.File(OutputFilePath,'w')
    
        
    
    Outputs=DataInputFile["Outputs"]
    Galaxies=IndexInputFile['galaxies'].value
    TotalRecCount=0
    for i in range(1,65):
        try:
            TotalRecCount=TotalRecCount+(len(Outputs["Output"+str(i)+"/nodeData"]['satelliteNode']))
        except:
            print "..."
    print str(TotalRecCount)
    
    
    
    
    DataTypeLists=[]
    for dset in Outputs["Output15/nodeData"]:
        print "FieldName: "+str(dset)    
        DataTypeLists+=[(str(dset),(str(Outputs["Output15/nodeData/"+str(dset)].dtype)))]
    
    DataTypeLists+=[('snapshot',numpy.int64)]    
    DataTypeLists+=[('MetalsColdGas',numpy.float64)]
    DataTypeLists+=[('sfr',numpy.float64)]  
    DataTypeLists+=[('treeid',numpy.int64)]
    DataTypeLists+=[('galaxyglobalindex',numpy.int64)] 
    DataTypeLists+=[('globaldescendant',numpy.int64)]  
    DataTypeLists+=[('descendant',numpy.int64)]  
    
    print str(len(Galaxies))
    
    TreeCountDS = numpy.zeros(shape=(len(IndexInputFile['tree_displs'])+1,1),dtype=numpy.int64)
    for RecordIndex in range(0,len(IndexInputFile['tree_displs'])-1):
        TreeCountDS[RecordIndex]=IndexInputFile['tree_displs'][RecordIndex+1]-IndexInputFile['tree_displs'][RecordIndex]
        print str(IndexInputFile['tree_displs'][RecordIndex+1])+":"+str(IndexInputFile['tree_displs'][RecordIndex])+"->"+str(TreeCountDS[RecordIndex])
    '''TreeCountDS=IndexInputFile['tree_counts']'''
    LastIndex=len(IndexInputFile['tree_displs'])-1
    TreeCountDS[LastIndex]=-IndexInputFile['tree_displs'][LastIndex]
    TotalRecordsCount=0
     
    for RecordIndex in range(0,len(TreeCountDS)):
        if TreeCountDS[RecordIndex]>0:
            TotalRecordsCount=TotalRecordsCount+TreeCountDS[RecordIndex]
            
    
    print "Total:"+str(TotalRecordsCount)+'/'+str(len(Galaxies))
    
    
    Datadict = numpy.zeros(shape=(TotalRecordsCount,),dtype=DataTypeLists)
    
    for RecordIndex in range(0,len(IndexInputFile['tree_displs'])):
        StartIndex=IndexInputFile['tree_displs'][RecordIndex]
        RecordsCount=TreeCountDS[RecordIndex]
        if RecordsCount>0:
            Datadict['treeid'][StartIndex:StartIndex+RecordsCount]=RecordIndex
    CacheData={}
    CacheIndex={}
    for RecordIndex in range(0,TotalRecordsCount):
        start = time.clock()
        Datadict['globaldescendant'][RecordIndex]=Galaxies['global descendant'][RecordIndex]
        Datadict['descendant'][RecordIndex]=Galaxies['descendant'][RecordIndex]
        Datadict['galaxyglobalindex'][RecordIndex]=Galaxies['gobal galaxy index'][RecordIndex]
        Datadict['snapshot'][RecordIndex]=Galaxies['snapshot'][RecordIndex]
        SnapshotID=Datadict['snapshot'][RecordIndex]+1
        GalGalaxyIndex=Galaxies['galaxy index'][RecordIndex]
        OutputName='Output'+str(SnapshotID)+'/nodeData'
        print str(RecordIndex)+"/"+str(TotalRecordsCount)+":"+str(SnapshotID)+"\t->"+OutputName
        
        ZoneData=Outputs[OutputName]
        FromChache=False
        if OutputName+"/nodeIndex" in CacheIndex:
            ZoneIndexDataDict=CacheIndex[OutputName+"/nodeIndex"]
            FromChache=True
        else:
            ZoneIndexDataArr=ZoneData['nodeIndex'].value
            ZoneIndexDataDict={}
            for i in range(0,len(ZoneIndexDataArr)):
                ZoneIndexDataDict[ZoneIndexDataArr[i]]=i
            CacheIndex[OutputName+"/nodeIndex"]=ZoneIndexDataDict
        
            
        #ZoneIndexData=ZoneData['nodeIndex'].value
        
        DataFieldIndex=ZoneIndexDataDict[GalGalaxyIndex]#numpy.where(ZoneIndexData==GalGalaxyIndex)[0][0]
        
        for dset in ZoneData:
            if dset in Datadict.dtype.fields: 
                if OutputName+"/"+dset not in CacheData:
                    CacheData[OutputName+"/"+dset]=ZoneData[str(dset)].value
                    print "****Data Not in Cache: "+ OutputName+"/"+dset
                #else:
                #    print "----Data  in Cache: "+ OutputName+"/"+dset
                #print CacheData[OutputName+"/"+dset]
                Datadict[str(dset)][RecordIndex]=CacheData[OutputName+"/"+dset][DataFieldIndex]
            #else:
            #    print "Field doesn\'t exist :"+str(dset)
        end = time.clock()
        print "\t\t"+str(SnapshotID)+":"+str(GalGalaxyIndex)+">>"+str(DataFieldIndex)+"\t: Time="+str(end - start)+"\t\t"+str(FromChache)
    
    Datadict['MetalsColdGas']=numpy.add(Datadict['diskAbundancesGasMetals'],Datadict['spheroidAbundancesGasMetals'])
    Datadict['sfr']=numpy.add(Datadict['interOutputDiskStarFormationRate'],Datadict['interOutputSpheroidStarFormationRate'])
    
    Datadict['sfr']=Datadict['sfr']/(10**9)
    Datadict['interOutputSpheroidStarFormationRate']=Datadict['interOutputSpheroidStarFormationRate']/(10**9)
    
    
   
    
        
    OutputFile.create_dataset("galaxies", data=Datadict)
    
        
        
    RedshiftData=[127, 79.9978940547546, 49.999592003264, 30.000062000124, 19.9156888582125, 18.2437217357837, 16.7245254258317, 15.3430738053213, 14.0859142818351,12.9407795683935, 11.8965695125097, 10.9438638399522, 10.0734613425465, 9.277914816642, 8.54991261829954, 7.88320363856021, 7.27218807646811,6.71158665895508, 6.19683339330695, 5.72386433931309, 5.28883354715367, 4.88844921801394, 4.51955578615033, 4.17946858652302, 3.86568282559933,3.57590511403156, 3.30809793168218, 3.06041903524444, 2.83118276274251, 2.61886150617016, 2.42204412383693, 2.23948544013269, 2.07002732324318,1.91263267041814, 1.76633590510361, 1.63027073376663, 1.50363653206282, 1.38571813694499, 1.27584621651946, 1.17341693743819, 1.07787458364588,0.988708115321206, 0.905462389030634, 0.827699146098959, 0.755035635998589, 0.687108801646618, 0.623590114933944, 0.564176601795049,0.508591428183505, 0.45657724738945, 0.407899442190241, 0.362340282631115, 0.319703436243807, 0.279801784299648, 0.242469084263011,0.207548627983249, 0.174897607673491, 0.144383423377236, 0.115883372333457, 0.0892878345066779, 0.0644933969474588, 0.0414030615167202,0.0199325416616944, 0]
    OutputFile.create_dataset("tree_counts", data=TreeCountDS)
    OutputFile.create_dataset("tree_displs", data=IndexInputFile['tree_displs'])
    OutputFile.create_dataset("snapshot_redshifts", data=RedshiftData)
    cosgroup=OutputFile.create_group("cosmology")
    cosgroup.create_dataset("hubble",  data=[73])
    cosgroup.create_dataset("omega_l",  data=[0.75])
    cosgroup.create_dataset("omega_m",  data=[0.25])
    IndexInputFile.close()
    DataInputFile.close()
    OutputFile.close()