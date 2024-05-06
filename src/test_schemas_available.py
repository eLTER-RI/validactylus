import pytest
import urllib



from os import chdir, getcwd

chdir("c:/Users/offenthaler//fremd//fremd//CI//validactylus//src//")





schema_base_url = ("https://raw.githubusercontent.com/eLTER-RI/"
                   "elter-ci-schemas/main/schemas/")


from validactylus import *

rs = get_remote_schemas(schema_base_url, "data_mapping", "shared")

rs["schema_topic"]

register_schemas(rs["schema_topic"], rs["schema_shared"])



import csv

with open("test.csv") as csv_data:
    reader = csv.DictReader(csv_data, delimiter = ";")   
    print([idx for idx, row in enumerate(reader)])
    
    
    
    for row in reader:
        instance = json.dumps(row)
        print(instance)
    


help("json.dump")

        
a = [3]
b = [2]

a + b

v_results.append(3)
v_results
import         
        
    try:
        instance = (pd.read_csv(csv_url, sep = ";").head(1)
    except:
        raiseValueError("could not import \"{csv_url}\"")            
    
   ## convert each CSV line to JSON object: 
   instance = json.loads(instance.to_json(orient = "records"))        
   
   
   
   