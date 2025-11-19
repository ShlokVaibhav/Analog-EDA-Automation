import csv
import os
from subprocess import call
import utils
import mae_var
import sys

li = []
block = utils.preprocess_list(mae_var.blocks)
li = utils.gen_struct(block, li)
li = utils.postprocess_block(li)    # generating the proper hierarchical names for the checkers

TOP = mae_var.cell_sch+'_'+mae_var.test_name    # all the skill scripts and netlisting will be happening here
csv_file = TOP+'_checker.csv'
call('rm -rf '+ TOP, shell=1)
call("mkdir " + TOP, shell=1)
call("cd "+TOP+"; rm -rf " + csv_file, shell=1)
call("cd "+TOP+"; touch " + csv_file, shell=1)      # The csv storing checkers

netlist_path = os.getcwd()+'/'+TOP+'/'
call("mkdir " + netlist_path, shell=1)
utils.netlist_script_gen(mae_var.library_sch, mae_var.cell_sch, mae_var.view_sch, TOP)

# https://community.cadence.com/cadence_technology_forums/f/custom-ic-skill/35153/generate-netlist-from-the-command-line
call("cd "+mae_var.sim_path+"; virtuoso -nograph -restore "+netlist_path+'netlist.il'+" -log "+ netlist_path+"/out2.log", shell=1)   # local virtuoso for netlist, command gathered from chatgpt


csv_file = TOP+"/"+csv_file
netlist_file =  netlist_path+mae_var.cell_sch+'/spectre/'+mae_var.view_sch+'/netlist/netlist'   # Assuming you are using spectre simulator
utils.walk_folder(li, netlist_file, csv_file, mae_var.test_name, mae_var.params)   ## Create the checkers csv file in TOP/
utils.checker_import_script_gen(mae_var.library_sch, mae_var.cell_sch, mae_var.maestro_sch, TOP)   # the script to automatically load the csv to maestro, currently under development

if(len(sys.argv)>1):
    load_in_maestro = sys.argv[1]
else:
    load_in_maestro = 1
    
if(load_in_maestro==1):
    call("rm -rf "+mae_var.csv_path+"/"+mae_var.cell_sch+"_"+mae_var.test_name+"_checkers.csv",shell=1)    
    call("cp "+csv_file+" "+mae_var.csv_path+"/"+mae_var.cell_sch+"_"+mae_var.test_name+"_checkers.csv",shell=1)    # copies the csv to the where you want
    #call("rm -rf "+mae_var.sim_path+"/cds/"+mae_var.library_sch+"/"+mae_var.cell_sch+"/"+mae_var.maestro_sch+"/documents/"+mae_var.cell_sch+"_"+mae_var.test_name+"_checkers.csv",shell=1)    
    #call("cp "+csv_file+" "+mae_var.sim_path+"/cds/"+mae_var.library_sch+"/"+mae_var.cell_sch+"/"+mae_var.maestro_sch+"/documents/"+mae_var.cell_sch+"_"+mae_var.test_name+"_checkers.csv",shell=1)
    #call("cd "+mae_var.sim_path+"; virtuoso -nograph -restore "+netlist_path+'/checker_import.il'+" -log "+ netlist_path+"/out_checker_import.log", shell=1)


