##import xml.etree.ElementTree as ET
import xmltodict
import pickle as PI
import os
#import numpy
##import pandas as PyTABLE

# TablesLI = ['studies',
            # 'baseline_groups',
            # 'participant_flow_groups'
            # ]
            
AttrsDI  = {}

ValuesDI = {'studies':[],
            'study_design':[],
            'baseline_groups':[],
            'participant_flow_groups':[],
            'outcomes':[],
            'out_groups':[],
            'eval_params':[],
            'results':[],
            'interventions':[],
            'conditions':[]
            }




AttrsDI['studies'] = ['nct_id', 'brief_title', 'lead_sponsor_agency', 'study_phase']
AttrsDI['baseline_groups'] = ['nct_id', 'baseline_group', 'title']

AttrsDI['participant_flow_groups'] =['nct_id', 'pfl_group', 'title']
AttrsDI['outcomes']  =  ['nct_id', 'outcome_index', 'type', 'title', 'time_frame', 'population']
                         
AttrsDI['out_groups']    = ['nct_id', 'outcome_index', 'group_index', 'group_id', 'group_title']
                        
AttrsDI['eval_params']   = ['nct_id', 'outcome_index', 'EV_title', 'population', 'parameter', 'dispersion']
AttrsDI['results']       = ['nct_id', 'outcome_index', 'EV_title',  'group_id', 'value', 'units']
AttrsDI['study_design']  = ['nct_id', 'allocation', 'intervention_model', 'primary_purpose', 'masking']
AttrsDI['interventions'] = ['nct_id', 'intervention_type', 'intervention_name', 'description']
AttrsDI['conditions']    = ['nct_id', 'curr_disease']

CurrDI = {'table':'',
          'source':'',
          'OrDI':{},
          'CS':{},
          'ClinResults':{},
          'out_inx':0,
          'curr_outcome':'',
          'intervention':''
          }
       
        
def Eval__disease():

    nct_id = CurrDI['table']
    CS     = CurrDI['CS']

    condition = CS['condition']
    if type(condition) == type([]):
        for dis_inx in range(len(condition)):
            curr_disease = condition[dis_inx]
            sl = [nct_id, curr_disease]
            ValuesDI['conditions'].append(sl)

    else:
        sl = [nct_id, condition]
        ValuesDI['conditions'].append(sl)


def Attrs__intervention():

    nct_id = CurrDI['table']
    CS     = CurrDI['CS']
    
    curr_intervention = CurrDI['intervention']
    
     
    intervention_type = ''
    if 'intervention_type' in curr_intervention:
        intervention_type = curr_intervention['intervention_type']
     
    intervention_name  = ''
    if 'intervention_name' in curr_intervention:
        intervention_name = curr_intervention['intervention_name']
        
    description = ''
    if description in curr_intervention:
        description = curr_intervention['description']
        
    sl = [nct_id, intervention_type, intervention_name, description]
    ValuesDI['interventions'].append(sl)



def Eval__study__drugs():

#    nct_id = CurrDI['table']
    CS     = CurrDI['CS']
    
    intervention = ''
    if 'intervention' not in CS:
        return 0
        
    intervention = CS['intervention']
    # print('type(intervention)')
    # print(type(intervention))
   
    if type(intervention) == type([]):
        
        for int_inx in range(len(intervention)):
            curr_intervention = intervention[int_inx]
            CurrDI['intervention'] = curr_intervention
            
            Attrs__intervention()
            
    else:
        CurrDI['intervention'] = intervention
            
        Attrs__intervention()
            
        

def Eval__analyzed_list():


    nct_id = CurrDI['table']
    out_inx = CurrDI['out_inx']
    curr_outcome = CurrDI['curr_outcome']
    EvalParam = curr_outcome['measure']
    EV_title  = CurrDI['EV_title']
            
    analyzed_list = EvalParam['analyzed_list']
    # print('\n\n analyzed_list\n')
    # print(analyzed_list)
    analyzed = analyzed_list['analyzed']
    units = ''
    if 'units' in analyzed:
        units = analyzed['units']
        
# <scope>Overall</scope>
    scope = ''
    if 'scope' in analyzed:
        scope = analyzed['scope']
        
    if 'count_list' in analyzed:
        count_list = analyzed['count_list']

        CountLI = count_list['count']
        # print("type(CountLI) : ")
        # print(type(CountLI))
        # print(CountLI)
        
        if type(CountLI) == type([]):
        # 'list'>
        # [OrderedDict([(u'@group_id', u'O1'),
                    # (u'@value', u'2765')]), 
         # OrderedDict([(u'@group_id', u'O2'), 
                    # (u'@value', u'2753')])]
            
            for ordi in CountLI:
                group_id = ordi['@group_id']
                value    = ordi['@value'] 
                sl = [nct_id, out_inx, EV_title, group_id, value, units]
                ValuesDI['results'].append(sl)
                
        else:
            ordi = CountLI
            group_id = ordi['@group_id']
            value    = ordi['@value'] 
            sl = [nct_id, out_inx, EV_title, group_id, value, units]
            ValuesDI['results'].append(sl)



def Eval__measure():

    nct_id = CurrDI['table']
    out_inx = CurrDI['out_inx']
    curr_outcome = CurrDI['curr_outcome']
    
    
    #<measure>
    if 'measure' in curr_outcome:
        EvalParam = curr_outcome['measure']
        EV_title = EvalParam['title']
        
        CurrDI['EV_title'] = EV_title
#                print(EV_title) 
#          <title>Overall Survival</title>
#        description = ''
#        if 'description' in EvalParam:
 #           description = EvalParam['description']

        population = ''
        if population in EvalParam:
            population = EvalParam['EvalParam']
            
        
        units = ''
#          <units>days</units>            
        if units in EvalParam:
            population = EvalParam['units']
        
#                print(units)
#          <param>Median</param>
        param = ''
        if 'param' in EvalParam:
            param = EvalParam['param']
                        
#          <dispersion>95% Confidence Interval</dispersion>
        dispersion = ''
        if 'dispersion' in EvalParam:
            dispersion = EvalParam['dispersion']
    
        sl = [nct_id, out_inx, EV_title, population, param, dispersion]
        ValuesDI['eval_params'].append(sl)
   
#          <analyzed_list>
        if 'analyzed_list' in EvalParam:
        
            Eval__analyzed_list()
            
   

def Eval__group():

    nct_id = CurrDI['table']
    out_inx = CurrDI['out_inx']
    curr_outcome = CurrDI['curr_outcome']
    
    if 'group_list' in curr_outcome:
        
        groups = curr_outcome['group_list']['group']

        if type(groups) == type([]):
            group_count = len(groups)
            for out_gr_inx in range(group_count):
                curr_out_group = groups[out_gr_inx]
        ##('@group_id', 'O1'), ('title', 'D-Cycloserine'), ('description'
                group_id    = curr_out_group['@group_id']
                group_title = curr_out_group['title']

              #  group_description = ''
              #  if 'description' in curr_out_group:
              #      group_description = curr_out_group['description']

                sl = [nct_id, out_inx, out_gr_inx, group_id, group_title] #, group_description]
                ValuesDI['out_groups'].append(sl)
            
        else:                         
            
            curr_out_group = groups
    ##('@group_id', 'O1'), ('title', 'D-Cycloserine'), ('description'
            group_id    = curr_out_group['@group_id']
            group_title = curr_out_group['title']

       #     group_description = ''
      #      if 'description' in curr_out_group:
       #         group_description = curr_out_group['description']

            sl = [nct_id, out_inx, '0', group_id, group_title] #, group_description]
            ValuesDI['out_groups'].append(sl)



def Eval__outcome():

    nct_id = CurrDI['table']
    out_inx = CurrDI['out_inx']

    curr_outcome = CurrDI['curr_outcome']
    outcome_type  = curr_outcome["type"]
    outcome_title = curr_outcome["title"]
    time_frame = ""
    if "time_frame" in curr_outcome:                
        time_frame    = curr_outcome["time_frame"]
    
    population    = ""
    if "population" in curr_outcome:
        population    = curr_outcome["population"]

    
    
    sl = [nct_id, out_inx, outcome_type, outcome_title, time_frame, population] ##, description]
    ValuesDI['outcomes'].append(sl)
    
    
    Eval__group()
    
    Eval__measure()
    


def Study_results():

##    nct_id = CurrDI['table']

    ClinResults = CurrDI['ClinResults']
    CurrDI['out_inx'] = 0

    outcome_list = ClinResults["outcome_list"]    
    outcome = outcome_list['outcome']

    
    if type(outcome) == type([]):

        for out_inx in range(len(outcome)):            
            
            curr_outcome = outcome[out_inx]
            
            CurrDI['curr_outcome'] = curr_outcome
            CurrDI['out_inx'] = out_inx
            
            Eval__outcome()                    


    else:  ## type(outcome) != type([]): - ord. dict     

        #out_inx = 0
        curr_outcome = outcome
        CurrDI['curr_outcome'] = curr_outcome
            
        Eval__outcome()
        
       
            
def PrintoutResults():

    ResultsLI = ValuesDI['results']
    
    for y in range(len(ResultsLI)):
        sl = ResultsLI[y]
        print(sl)
    


def Read__source():

    curr_fname = CurrDI['source']
##fname = 'StudiesWithResults\\NCT00014495.xml'
    fname = 'StudiesWithResults/'+ curr_fname
    fi = open(fname, 'r')
    line = fi.read()
    fi.close()

    OrDI = xmltodict.parse(line)##fd.read())
    CurrDI['OrDI'] = OrDI
    CurrDI['outcome'] = 0
    
    CurrDI['CS'] = OrDI['clinical_study']
    CurrDI['ClinResults'] = CurrDI['CS']['clinical_results']
    


def Get__range():

    FiLI = os.listdir('StudiesWithResults')
    
        
    for finx in range(1000):
        curr_fname = FiLI[finx]
        print(finx)
        print(curr_fname)
        CurrDI['source'] = curr_fname
        
        Get_DATA()
        
    print('Get__range:done')


def Study__id():

   
    CS = CurrDI['CS']
    
    id_info = CS['id_info']
    di = dict(id_info)
    ##print(di)
    nct_id  = id_info['nct_id']
    ##<nct_id>NCT00835341</nct_id>
    print('\n\n nct_id : '+nct_id)
    CurrDI['table'] = nct_id
    
    
    brief_title  = CS['brief_title']
    lead_sponsor = CS['sponsors']['lead_sponsor']
    lead_sponsor_agency = lead_sponsor['agency']
    
    study_phase = ''
    if 'phase' in CS:    
        study_phase = CS['phase']
    
    sl = [nct_id, brief_title, lead_sponsor_agency, study_phase]
    ValuesDI['studies'].append(sl)
    
    ####################################
    if 'study_design_info' in CS:
        study_design_info = CS['study_design_info']

        allocation = ''
        if 'allocation' in study_design_info:
            allocation  = study_design_info['allocation']
            
        intervention_model = ''
        if 'intervention_model' in study_design_info:
            intervention_model = study_design_info['intervention_model']
        
        primary_purpose = ''
        if 'primary_purpose' in study_design_info:
            primary_purpose = study_design_info['primary_purpose']
           
        
        masking = ''
        if 'masking' in study_design_info:
            masking = study_design_info['masking']
            
        sl = [nct_id, allocation, intervention_model, primary_purpose, masking]
        ValuesDI['study_design'].append(sl)
    

def DumpDI(di_name):

    fname = di_name + '.li'
    Obj_4_dump = dict(CurrDI[di_name])
    
    fi = open(fname, 'wb')
    PI.dump(Obj_4_dump, fi)
    fi.close()

    print('DumpDI '+fname+' : done')
    

def Get__baseline():
    
    nct_id = CurrDI['table']
    ClinResults = CurrDI['ClinResults']        
    or_di = ClinResults['baseline']
    
    
    #print('baseline : ')
    ##for k,v in participant_flow.items():
    ##	print(k)
    ##	print(v)
    ##	print('\n\n=========')

    if type(or_di['group_list']['group']) == type([]):
        groups = or_di['group_list']['group']
        count_groups = len(groups)
#        print('total: '+str(count_groups)+' baseline groups')
#        BaseLI = []
        for cpg_inx in range(count_groups):

            curr_group  = or_di['group_list']['group'][cpg_inx]['@group_id']
            curr_title  = or_di['group_list']['group'][cpg_inx]['title']
            
            description = ''
            if 'description' in or_di['group_list']['group'][cpg_inx]:
                description = or_di['group_list']['group'][cpg_inx]['description']

            
            sl = [nct_id, curr_group, curr_title] ##, description]
            ValuesDI['baseline_groups'].append(sl)
    
    else: ##if type(or_di['group_list']['group']) != type([]): - ord. dict
        curr_group  = or_di['group_list']['group']['@group_id']
        curr_title  = or_di['group_list']['group']['title']
        
        description = ''
        if 'description' in or_di['group_list']['group']:
            description = or_di['group_list']['group']['description']

            
        sl = [nct_id, curr_group, curr_title] ##, description]
        ValuesDI['baseline_groups'].append(sl)



def Get__participant_flow():

    ClinResults = CurrDI['ClinResults'] 
    participant_flow = ClinResults['participant_flow']
    #print('participant_flow : ')

    nct_id = CurrDI['table']
    
#    print('total: '+str(count_part_groups)+' participant groups')

    PflLI = []
    
    if type(participant_flow['group_list']['group']) == type([]):
        part_groups = participant_flow['group_list']['group']
        count_part_groups = len(part_groups)

        for cpg_inx in range(count_part_groups):

            curr_group      = participant_flow['group_list']['group'][cpg_inx]['@group_id']
            ####'P1'
            curr_group_title = participant_flow['group_list']['group'][cpg_inx]['title']
            
            description = ''
            if 'description' in  participant_flow['group_list']['group'][cpg_inx]:
                description = participant_flow['group_list']['group'][cpg_inx]['description']
            sl = [nct_id, curr_group, curr_group_title] ##, description]
            
            
            ValuesDI['participant_flow_groups'].append(sl)
    else:
        
        curr_group = participant_flow['group_list']['group']['@group_id']
   
        curr_group_title = participant_flow['group_list']['group']['title']
        description = ''
        if 'description' in  participant_flow['group_list']['group']:
            description = participant_flow['group_list']['group']['description']
    
        sl = [nct_id, curr_group, curr_group_title] ##, description]
            
            
        ValuesDI['participant_flow_groups'].append(sl)
 
    #PflDF = PyTABLE.DataFrame(PflLI, columns = AttrsLI)

def Get_DATA():
    
    Read__source()
    
    Study__id()
    
    Eval__study__drugs()
    
    Eval__disease()
    
    Get__participant_flow()
    Get__baseline()
    Study_results()
   

def Start():

##    Study__id()    
##    Get__participant_flow()
##    Get__baseline()
    Get__range()
    
 
 
##    PrintoutResults()
    
Start()
