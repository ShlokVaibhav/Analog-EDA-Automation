import csv
import os
import re

def netlist_script_gen(library_sch, cell_sch, view_sch, TOP):

    il_file = open(TOP+'/netlist.il', "wt")
    il_file.write('; netlist generation \n')
    il_file.write('envSetVal(\"asimenv.startup\" \"projectDir\" \'string \"'+os.getcwd()+"/"+TOP+"\")\n")
    il_file.write("simulator(\"spectre\")\n")
    il_file.write("design(\""+library_sch+"\" " +"\""+cell_sch + "\" \""+view_sch+"\")\n")
    il_file.write("createNetlist( ?recreateAll t)\n")
    il_file.write("exit()\n")
    il_file.close()

def checker_import_script_gen(library_sch, cell_sch, view_sch, TOP):

    il_file = open(TOP+'/checker_import.il', "wt")
    il_file.write('; checker import \n')
    il_file.write("sessionNAme = maeOpenSetup(\""+library_sch+"\" " +"\""+cell_sch + "\" \""+view_sch+"\")\n")
    #il_file.write("getDirFiles(strcat(axlGetSetupDBDir(axlGetMainSetupDB(sessionNAme)) \n")
    il_file.write("maeImportOutputsFromFileInDocuments("+"\""+TOP+"_checker.csv\")\n")
    il_file.write("maeSaveSetup()\n")
    il_file.write("exit()\n")
    il_file.close()


def process_text_and_write_to_csv(text_file, csv_writer, y, z, test_name, cell_name, hierarchy):
    """
    Reads a text file, processes lines containing 'IO_AMP', and writes specific expressions to a CSV file.

    Args:
    text_file (str): Path to the input text file.
    csv_file (str): Path to the output CSV file.
    y (str): A string provided by the user to be used in the expressions.
    z (list): A list of strings to be used as the second parameter in the expressions.
    """
    with open(text_file, 'r') as file:
        lines = file.readlines()

        # Open the CSV file for writing
        for i in range(1):
           
            

            # Flag to start processing lines after finding instance
            processing = False

            for line in lines:
                line = line.strip()

                if f'subckt {cell_name}' in line:
                    processing = True # Start processing lines
                    continue

                if processing:
                    if f'ends {cell_name}' in line:
                        break # Stop processing when 'ends' is found

                    # Extract the first word
                    first_word = line.split()[0] if line.split() else ""
                    initial_label = hierarchy  +"_"+ first_word
                    #initial_label = initial_label[1:]
                    # Check if the first word starts with MP_ or MN_ and does not contain SW
                    if (first_word.startswith("MP_") or first_word.startswith("MN_")) and "SW" not in first_word:
                        sign_OP = ""
                        sign_N = "-"
                        if(first_word.startswith("MP_")):
                            sign_OP = "-"
                            sign_N = "+"
                    # Write N rows to the CSV file based on the list z
                        for item in z:
                            print(item)
                            csv_writer.writerow([
                            test_name, # Test
                            f"{initial_label}_{item}", # Name
                            "expr", # Type
                            f'{sign_OP}OP("{y}{first_word}", "{item}")', # Output
                            "point", # EvalType
                            "t", # Plot
                            "", # PlotTarget
                            "" # Save
                            ])
                        csv_writer.writerow([
                        test_name, # Test
                        f"{initial_label}_VDSAT_MARGIN", # Name
                        "expr", # Type
                        f'{sign_OP}OP("{y}{first_word}", "VDS"){sign_N}OP("{y}{first_word}", "VDSAT")', # Output
                        "point", # EvalType
                        "t", # Plot
                        "", # PlotTarget
                        "" # Save
                        ])
                        csv_writer.writerow([
                        test_name, # Test
                        f"{initial_label}_REGION", # Name
                        "expr", # Type
                        f'OP("{y}{first_word}", "REGION")', # Output
                        "point", # EvalType
                        "t", # Plot
                        "", # PlotTarget
                        "" # Save
                        ])   
        
    file.close()             


def gen_struct(I, li):
    li.append(I[0])
    if len(I)>1:
        for i in range(1, len(I)):
            temp = I[i] 
            temp[0] = I[0].split(' ')[0]+"__"+temp[0].split(' ')[0]+" "+temp[0].split(' ')[1]+" "+I[0].split(' ')[2]+"/"+temp[0].split(' ')[2]
            I[i] = temp
            gen_struct(temp,li)
    return li

def preprocess_list(I):
    I[0] = I[0]+' '+I[0].split(' ')[0]
    if len(I)>1:
        for i in range(1, len(I)):
            temp = I[i] 
            temp[0] = temp[0]+' '+temp[0].split(' ')[0]
            I[i] = temp
            preprocess_list(temp)
    return I

def remove_top(I):
    top = I[0].split(' ')[0]
    for i in range(1, len(I)):
        temp = I[i]
        I[i] = temp[(len(top)+2):]
        temp = I[i].split(' ')[2]
        I[i] = I[i].split(' ')[0]+' '+I[i].split(' ')[1]+' '+temp[len(top):]+'/'
    I.pop(0)
    print(I)

    return I


def postprocess_block(I):
    remove_top(I)
    return I

def walk_folder(structure, netlist_file, csv_file, test_name, specs):
    #os.remove(csv_file)
    with open(csv_file, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Test", "Name", "Type", "Output", "EvalType", "Plot", "PlotTarget", "Save"])   
        for elem in structure:  
            process_text_and_write_to_csv(netlist_file, csv_writer, elem.split(' ')[2] , specs, test_name, elem.split(' ')[1] , elem.split(' ')[0])
    csvfile.close()
                                                                

