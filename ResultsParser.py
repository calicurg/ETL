import os
import shutil


ParamsDI = {'target_dir' : 'StudiesWithResults'}

def Eval__attrs():

    target_dir = ParamsDI['target_dir']
    FiLI = os.listdir(target_dir)
    print(FiLI[:5])
    
    finx = 0    
    curr_file_name =  FiLI[finx]   
    curr_file = target_dir + '/' + curr_file_name 

    fi = open(curr_file, 'r')
    line = fi.read()
    fi.close()

    start_cr =  '<clinical_results>'
    end_cr   =  '</clinical_results>'
    
    start_pos = line.find(start_cr)
    end_pos   = line.find(end_cr)

    cr_fragment = line[start_pos:end_pos]
    


    


def Get__stidues__with__results():

    all_xmls_dir = 'AllPublicXML'

    FoldersLI = os.listdir(all_xmls_dir)
    total_folders = len(FoldersLI)
    outline = 'total folders : ' + str(total_folders)
    print(outline)

    target_dir = ParamsDI['target_dir']
    
    primer =  'clinical_results'

    for folder_index in range(len(FoldersLI)):
        current_folder = FoldersLI[folder_index]
        curr_path = all_xmls_dir +'/'+current_folder

        FiLI = os.listdir(curr_path)
        ##print(len(FiLI))
    
        for finx in range(len(FiLI)):
            curr_file_name = FiLI[finx]
            curr_file = curr_path + '/' + curr_file_name
            fi = open(curr_file, 'r')
            try:
                line = fi.read()
                fi.close()
            except:
                print('reading error : '+curr_file_name)
                fi.close()
                continue            
            

            if primer in line:

                shutil.copy(curr_file, target_dir)
                
                pos  = line.find(primer)
                fr   = line[pos:pos+30]
                print(curr_file_name) 
##                print(fr)
##                print('\n\n========')
    

def Start():
    
    ## step 0. 
    ##Get__stidues__with__results()

    ## step 1.
    Eval__attrs()

Start()













