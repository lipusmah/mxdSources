import arcpy  
import Tkinter as tk
import tkFileDialog
import time

"""
Script: 
Opens tkinter open file window for selecting mxd file. It lists
parent layers; layer name ; source directory as a CSV file.

Script uses bat file for lunching and will use ArcGis python interpreter
usually saved in c/Python27/ArcGIS....

Path to mentioned interpreter has to be specified in bat file.

bat file is by default writen for arcgis 10.4


Blaz Lipus

"""
print("\n")
root = tk.Tk()
root.withdraw()
mxd_path = tkFileDialog.askopenfilename()

#pridobi txt file name in path
if mxd_path.split(".")[-1] != "mxd":
    print("Selected file is not *.mxd file or was the file 'open' operation canceled before selecting.")
    print("Rerun and select *.mxd file.")



else:
    start = time.time()

    print("Starting source searching procedure for all layers in selected mxd file...\n")
    path_split = mxd_path.split("/")
    
    txt_name = path_split[-1].split(".")[0]+".txt"
    path_name = ""
    for i in range(len(path_split)-1):
        path_name += path_split[i] + "/"
    
    fajl = open(path_name+txt_name, "w")
    fajl.write("{};{};{}\n".format("Parent layers", "Layer name", "Source"))
    
    
    mxd = arcpy.mapping.MapDocument(mxd_path)  
    df = arcpy.mapping.ListDataFrames(mxd)  
    
    print("Starting process on file: {}\n".format(path_split[-1]))
    
    for d in df:    
        layers = arcpy.mapping.ListLayers(mxd, "", d)      
        for lyr in layers:
            if lyr.supports("DATASOURCE"):
                
                full_names = lyr.longName.split("\\")
                
                parent_names = ""
                if len(full_names)>1:
                    for i in range(len(full_names)-1):
                        parent_names += full_names[i] + "\\"
                else: parent_names = "\\"
                
                parent_names = parent_names.encode('utf-8')
                lyr_name = lyr.name.encode('utf-8')
                datasource = lyr.dataSource.encode('utf-8')
                
                fajl.write("{};{};{}\n".format(parent_names, lyr_name, datasource))
    stop = time.time()
    
    print("Process took {} sec and successfully finished!!\n".format(round(stop-start, 3)) )
    
    print("CSV file saved in:  {}".format(path_name))
    print("Name of CSV file is: {}\n".format(txt_name))
    fajl.close()
