#The working directory for project
sim_path="" 
# The path where csv is to be stored
csv_path=""
#The library containing the schematic 
library_sch="my_library" 
#The cell name containing the schematic 
cell_sch =  "my_cell"  
#The view name of schematic to be used  
view_sch="schematic_DC" 
#The maestro name
maestro_sch = "maestro"
#the name of the maestro test for which checkers are being generated 
test_name="Tran_sim"  
#Nested lists containing the hierarchichal information of the cells used and their instance names         
blocks=["my_cell schematic_DC", ["LDO LDO_1P8V",["BUFF LDO_BUFFER"],["ERR_AMP SMC_AMP",["OTA OTA_NMOS"]],["DRIVER PASS_GATE"]]] 

# The op checkers to be generated:
params = ["ID", "VGS", "VDS"]    # VDsat margin (VDS - Vdsat) and VTH are already genereated so no need to enter those
