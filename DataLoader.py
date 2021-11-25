import XmlReader
import numpy

import pyodbc
import pickle as PI
##import LightLinter as LL
###from tkinter import filedialog as TF

##TK   = LL.TK
##TKDI = LL.TKDI

Modes = ['strings_only', 
        'real_types'
        ]

CurrDI = XmlReader.CurrDI
CurrDI['mode'] = 'strings_only' 

ConnLI = ['DRIVER',
          'SERVER',
          'DATABASE',
          'UID',
          'PWD'
          ]

                 
ConnDI = {'DRIVER':'{SQL Server}',
          'SERVER':"WIN-DPISK0DDVO5\SQLEXPRESS",
          'DATABASE':'accs00',
          'UID':'ilya',
          'PWD':'0000'
          }
          
MaxLens  = {}
AttrsDI  = XmlReader.AttrsDI
ValuesDI = XmlReader.ValuesDI

CreateStatementsLI = []

NonLoadedLI = []

def WriteErrorsLog():

    fi = open('loading_errors.txt', 'w')
    for fr in NonLoadedLI:
        fr += '\n'
        fi.write(fr)
        
    fi.close()
    print('WriteErrorsLog : done')
    
    
def prepare__string__value(fragment):
    
    fragment = str(fragment)
    
    if "'" in fragment:
        fragment = fragment.replace("'", "")
    
    fragment = "'"+fragment+"'"
    
    return fragment 


def Prepare__valline(values_list):

    ## for CurrDI['mode'] = 'strings_only' 
    ValsLI = []
    
    for fragment in values_list:
    
        fr = prepare__string__value(fragment)
        
        ValsLI.append(fr)
     
    val_line = ', '.join(ValsLI)    
    return val_line
    

def Clean__all__tables():
    
    statement = "USE clin_results"
    Execute(statement)
    
    for table_name in  ValuesDI.keys():
        
        LINE = 'TRUNCATE TABLE '+table_name+';'
        Execute(LINE)
        
    print('Clean__all__tables : done')    

def InsertValues():

    ## for CurrDI['mode'] = 'strings_only' 

    statement = "USE clin_results"
    Execute(statement)
    
    counter = 0
    for table_name, Values_LOL in  ValuesDI.items():
        
        for values_list in Values_LOL:
    
            valline = Prepare__valline(values_list)
        
            line = "INSERT INTO " \
                +table_name \
                +" \n VALUES (\n" \
                + valline + "\n);\n"
            
            print(counter)
            
            Execute(line);
            
            counter += 1
            
                    
            


def CreateTables():
    
    statement = "USE clin_results"
    Execute(statement)
    
    for y in range( len(CreateStatementsLI)):
    
        sql_statement = CreateStatementsLI[y]
        
        Execute(sql_statement)
        
                    
def Execute(statement):

    cursor = CurrDI['cursor']
    cnxn   = CurrDI['con']
    #try:
    #print(statement)
    
    try:
        cursor.execute(statement)
        cnxn.commit()
    except: 
        NonLoadedLI.append(statement)    
        print('not done for :\n', statement)

def Get_conn_line():

    conn_line = ''
    LI = []
    for attr in ConnLI:
        value = ConnDI[attr]
        fr = attr+'='+value
        LI.append(fr)

    conn_line = ';'.join(LI)
    return conn_line


def Connect_mssql():

    conn_line = Get_conn_line()
    cnxn = pyodbc.connect(conn_line) 
    cursor = cnxn.cursor()  
    CurrDI['con'] = cnxn
    CurrDI['cursor'] = cursor    
    
    print('Connect_mssql: done')


def PrepareCreateStatements():

    ## for CurrDI['mode'] = 'strings_only' 

    for table_name, AttrsLI in AttrsDI.items():
        ls = 'CREATE TABLE ' + table_name +' (\n'
        
        sl = []
        LensLI = MaxLens[table_name]
        for attr_inx in range(len(AttrsLI)):
            attr = AttrsLI[attr_inx]
            col_length = LensLI[attr_inx]
            attr_line = attr + ' VARCHAR ('+str(col_length)+') \n'
            
            sl.append(attr_line)
            
        all_attrs_line = ', '.join(sl)
        ls += all_attrs_line
        ls += '\n);\n'
        CreateStatementsLI.append(ls)    


def PrintoutSQL_stqtements():

    for cr in CreateStatementsLI:
        print(cr)
    

def Adjust_max_len(max_len):
    
    if max_len < 10:
        return 10
    elif max_len < 20:
        return 20
       
    elif max_len < 50:
        return 50
        
    elif max_len < 100:
        return 100

    elif max_len < 200:
        return 200

    elif max_len < 300:
        return 300
        
    else:
        return 500
        
        
        
def Eval__max__lens():
    
        
    for table, attrs in AttrsDI.items():
        LOL = ValuesDI[table]
        Array = numpy.array(LOL)
        
        print('\n\n========')
        print(table)
        
        max_lens = []
        for column_index in range(len(attrs)):
            curr_column = Array[:, column_index]
            lens_li = [len(fr) for fr in curr_column]
            maxlen = max(lens_li)
            adjusted_maxlen = Adjust_max_len(maxlen)
            
            attr = attrs[column_index]
            print(attr)
            print(maxlen, adjusted_maxlen)
            max_lens.append(adjusted_maxlen)
            
        MaxLens[table] = max_lens


def Start(): 
           
    Eval__max__lens()            
    PrepareCreateStatements()
#    PrintoutSQL_stqtements()
    
    Connect_mssql()

#    CreateTables()
#    Clean__all__tables()
    
    InsertValues()
        
    WriteErrorsLog()
#Start()
            
