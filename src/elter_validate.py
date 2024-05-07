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
    '''
    retrieve validation schemas (1. topic specific and 2. shared definitions)
    from host; raise error if not both schemas can be retrieved
    (i. e. if server status not 200 for either schema)
    '''


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
            
            
    # decode server byte response to UTF-8 and return schema as JSON:        
    rs = {k: json.loads(v.content.decode("UTF-8")) for k, v in rs.items()}
        
    return rs


def register_schemas(schema_topic, schema_shared,
                     spec = referencing.jsonschema.DRAFT202012):
    '''registers schemas locally
    Using a Registry object to make both the schema_shared and schema_topic
    known locally. This allows, i. a. to share references between schemas.
    -- args: schema_topic, schema_shared:
        JSON schemas (by default fetched from a remote host)
    '''

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
    
    parser.add_argument("-t", "--schema-topic", type = str,
                        choices = topic_choices,
                        help = "name of a topic-specific schema")
    
    parser.add_argument("-s", "--schema-shared", type = str,
                        default = "shared",
                        help = ("name of a schema with definitions shared by"
                                " topic schemas, default: \"shared\""))

    args = vars(parser.parse_args()) ## vars converts result to dictionnary

    # sanitize path arguments
    # (only the name, e. g. "data_mapping" should be supplied, but anyway:
    args = {k: quote(v, safe = ":./_-") for k,v in args.items()}
   
    # expand schema name to full URL, whether supplied as foo, foo.json
    # or https://www.my_schemahost.org/schemas/foo.json:       
    def expand_path(fragment):
        return(urljoin(schema_base_url,
                  re.sub("(\\.json)+$", "", fragment) + ".json"))
    args = {k: expand_path(v) if bool(re.search("schema_", k)) else v
           for k, v in args.items()} 


    print(args)

    the_schemas = get_remote_schemas(args["schema_topic"],
                                     args["schema_shared"])
    
   

    # create a validator which uses a schema defined in the registry;
    # this validator then accepts an instance to validate
    v = jsonschema.Draft202012Validator(
        schema = the_schemas["schema_topic"],
        registry = register_schemas(the_schemas["schema_topic"],
                                    the_schemas["schema_shared"])
    )


    v_results = []
    with open(args["file_path"]) as csv_data:
        reader = csv.DictReader(csv_data, delimiter = ";")
        i = 1
        for row in reader:
            instance = json.dumps(row)
            v_results.extend([{"line" : i,
                               "path" : ','.join(e.path),
                               "message" : e.message}
                      for e in v.iter_errors(instance = json.loads(instance))
                    ])
            i += 1
            
    print (json.dumps(v_results))
    
    



