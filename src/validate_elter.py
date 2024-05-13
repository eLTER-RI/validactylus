"""
# Intro

<img src = "../assets/validactylus.svg" width = 200>

Validactylus is a small Python **command line tool** to validate CSV data
against a ruleset laid down as a [JSON schema](https://json-schema.org/).

Its main function, called from the command line is `validate_elter()`.
It takes a CSV data file, fetches a topic-specific and a shared schema from an
eLTER schema store and validates the former, linewise, with the latter.

Validation errors -- if any -- are returned as a JSON array of error objects.

**Example**


Windows
```
py -m validate_elter path/to/data.csv, -r station, -rs shared
```

Linux
```
python validate_elter.py path/to/data.csv -r station, -rs shared
```

*(make sure to specify the full path to `validate_elter.py`)*

**Sample output** (truncated)

```
[{"line": 1, "path": "SITE_CODE", "message": "'qwer' does not match 
    '^https://deims.org/[a-zA-Z0-9]{8}-([a-zA-Z0-9]{4}-){3}[a-zA-Z0-9]{12}$'"},
    {"line": 1, "path": "LAT", "message": "'100' is not of type 'number'"},
```    






where `-r` is the topic-specific ruleset (here: for a station description)
and `rs` the shared rules (common to several topics, e. g. longitude).
The rulesets can be give as names ("station"), file names ("station.json") or
full URL (currently: 
"https://raw.githubusercontent.com/eLTER-RI/elter-ci-schemas/main/schemas/station.json").

"""

# render html docs with pdoc (from /src folder):
# python -m pdoc validate_elter.py --html -o ../docs --force

import argparse
import jsonschema
import requests
import re
import csv
import json
from urllib.parse import urljoin, quote
import referencing # for in-memory registration of schemas






def get_remote_schemas(url_schema_topic,
                       url_schema_shared):
    """
    Retrieve validation schemas from a remote schema store (e. g. a dedicated
    GitHub repo).
    Will raise an error if not both schemas can be retrieved
    with a server status of 200.
    
    Parameters
    ----------
    
    url_schema_topic : str
        full URL of topic-specific schema (e. g. site description)
        
    url_schema_shared : str
        full URL of shared schema (containing common 
                definitions shared by several topic-specific schemas)    
    """


    max_waiting = 5 ## s
    rs = {
        "schema_topic" : requests.get(url_schema_topic,
                                      timeout = max_waiting),
        "schema_shared" : requests.get(url_schema_shared,
                                        timeout =max_waiting)
    }
    
    if not all (v.status_code == 200 for k, v in rs.items()):
        raise ValueError("failed to retrieve" +\
                          f"\"{url_schema_topic}\" and/or " + \
                          f"\"{url_schema_shared}.json\""
                          )
            
            
#     # decode server byte response to UTF-8 and return schema as JSON:        
    rs = {k: json.loads(v.content.decode("UTF-8")) for k, v in rs.items()}
        
    return rs


def register_schemas(schema_topic, schema_shared,
                     spec = referencing.jsonschema.DRAFT202012):
    """
    Registers schemas (JSON objects of schemas written in JSONSchema)                       
                       locally in a Registry object.
    
    This is necessary to allow references from one schema to another,
    e. g. a topic-specific schema for site description referring to 
    common definitions (like latitude or site code format) stored in a
    shared schema.
    
    Parameters:
    -----------
    schema_topic : Dict
        topic-specific schema, `loads`'ed from remote JSON ressource
    schema_shared : Dict
        schema with shared definitions, `loads`'ed from remote JSON ressource
    """

    schema_topic_resource = (
        referencing.Resource(contents = schema_topic,
                             specification = spec)
        )
    schema_shared_resource = (
        referencing.Resource(contents = schema_shared,
                             specification = spec)
        )

    return referencing.Registry().with_resources([
        ("https://example.com/schema_topic", schema_topic_resource),
        ("https://example.com/schema_shared", schema_shared_resource)
    ])


def get_validator(schema_topic, registry):
    
    """
    Parameters
    ----------
    schema_topic : Dict
        topic-specific schema, `loads`'ed from JSON string
    registry : referencing.Registry
        a validator (package JSONschema) to ingest the CSV data
    
    Returns
    -------
    validator : jsonschema.Validator
        a validator which uses the schema "schema_topic" including references
        to a common schema "schema_shared" stored in the schema
        registry. This validator can be used to validate an instance (=data
        to be checked) like so: `validate_file(file_path, validator)`.  
               
    """
    validator = jsonschema.Draft202012Validator(
        schema = schemas["schema_topic"],
        registry = registry)
    return (validator)
    

def validate_file(file_path, validator):
    """
    
    
    Parameters
    ----------
    file_path : str
        full path to CSV file to be validated
    validator : jsonschema.validator
        a validator (package JSONschema) to ingest the CSV data

    Returns
    -------
    v_results : str
        A string describing a JSON array of error objects encountered during
        validation, each object consisting of CSV line number,
        invalid parameter and schema violation.

    """
    v_results = []
    with open(file_path) as csv_data:
        reader = csv.DictReader(csv_data, delimiter = args["delim"])
        i = 1
        for row in reader:
            instance = json.dumps(row)
            v_results.extend([{"line" : i,
                               "path" : ','.join(e.path),
                               "message" : e.message}
                      for e in validator.iter_errors(
                              instance = json.loads(instance))
                    ])
            i += 1
    v_results = json.dumps(v_results)            
    return (v_results)
    
    
if __name__ == "__main__":
    
    # get centrally managed schemas here:
    schema_base_url = ("https://raw.githubusercontent.com/eLTER-RI/"
                               "elter-ci-schemas/main/schemas/")

    # currently (Apr. 2024) available topic schemas:
    topic_choices = ['data_mapping', 'data_observation', 'event', 'license', 
                     'mapping', 'method', 'reference', 'sample', 'station']
        
    

    ## use JSONSchema version DRAFT202012:
    spec = referencing.jsonschema.DRAFT202012

    parser = argparse.ArgumentParser(prog = "elter_validate",
                                     description = "validate a CSV " +\
                        "using JSON schema",
                        epilog = "HTH")
    parser.add_argument("file_path", type = str, # positional (first) argument
                        help = ("path to CSV-file which to validate")
                        )
    
    parser.add_argument("-u", "--schema-base",  type = str,
                        default = schema_base_url,
                        help = "base url for remote schemas," + \
                            f" default: {schema_base_url}"
                        )
    
    parser.add_argument("-r", "--rules", type = str,
                        choices = topic_choices,
                        help = "name of a topic-specific schema")
    
    parser.add_argument("-rs", "--shared-rules", type = str,
                        default = "shared",
                        help = ("name of a schema with definitions shared by"
                                " topic schemas, default: \"shared\""))
    
    parser.add_argument("-delim", type = str, default = ";",
                        help = ("column separator, default: \";\" (semicolon"))

    # command line arguments to dictionary "args":
    args = vars(parser.parse_args()) 

    # sanitize url paths to schemas
    args = {k: quote(v, safe = ":./_-") if bool(re.search("rules", k)) else v 
            for k, v in args.items()}
   
    # expand schema name to full URL, whether supplied as foo, foo.json
    # or https://www.my_schemahost.org/schemas/foo.json:       
    def expand_path(fragment):
        return(urljoin(schema_base_url,
                  re.sub("(\\.json)+$", "", fragment) + ".json"))
    args = {k: expand_path(v) if bool(re.search("rules", k)) else v
           for k, v in args.items()}  
    
    


    schemas = get_remote_schemas(args["rules"], args["shared_rules"])
    registry = register_schemas(schemas["schema_topic"],
                                       schemas["schema_shared"],
                                       spec)

    validator = get_validator(schemas["schema_topic"], registry)
    result = validate_file(args["file_path"], validator)
    print(result)
    



        
         
    

