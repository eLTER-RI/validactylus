import argparse
import jsonschema
import requests
import json
import urllib.parse
import referencing # for in-memory registration of schemas
import pandas as pd

## get centrally managed schemas here:
schema_base_url = "https://raw.githubusercontent.com/eLTER-RI/validiraptor/main/inst/app/www/schemas/"

## currently (Apr. 2024) available topic schemas:
## ['data_mapping', 'data_observation', 'event', 'license', 'mapping', 'method', 'reference', 'sample', 'station']


parser = argparse.ArgumentParser(description="validates an instance against an eLTER reporting schema")
parser.add_argument("url_instance", type = str, help = "URL (file or remote) to CSV instance to be validated")
parser.add_argument("name_topic", type = str, help = "name of a topic-specific schema")
parser.add_argument("name_shared", type = str, help = "name of a schema with definitions shared by topic schemas ['shared']")
args = vars(parser.parse_args()) ## vars converts result to dictionnary

## sanitize path arguments (only the name, e. g. "data_mapping" should be supplied, but anyway:
args = {k: urllib.parse.quote(v, safe = ":./_-") for k,v in args.items()}

def get_schema_jsons(r_topic, r_shared):
    '''extract schema jsons from server response'''
    return {"topic" : r_topic.json(), "shared" : r_shared.json()}

def register_schemas(r_topic, r_shared):
    '''registers schemas locally
    Using a Registry object to make both the schema_shared and schema_topic known locally,
    references from schema_topic to schema_shared can be resolved.   
    -- args: r_topic, r_shared: server responses from the remote schemas' host
    '''

    jsons = get_schema_jsons(r_topic, r_shared)
 
    schema_topic_resource = referencing.Resource(contents = jsons["topic"], specification = referencing.jsonschema.DRAFT202012)
    schema_shared_resource = referencing.Resource(contents = jsons["shared"], specification = referencing.jsonschema.DRAFT202012)

    return referencing.Registry().with_resources([
        ("https://example.com/data_mapping", schema_topic_resource),
        ("https://example.com/shared", schema_shared_resource)
    ])

def get_instance_from_csv(csv_url):
    '''reads CSV data from a URL, takes header from first and exemplary data
    from second line, converts to JSON-able dictionnairy.
    Example: {"SITE_CODE" : "foo-bar-baz", ...}
    '''
    try:
        instance = pd.read_csv(csv_url, sep = ";").head(1).to_json(orient = "records")
        instance = json.loads(instance)[0] ## first entry of json array only
    except:
        instance = False
    finally:
        return instance
     
r_topic = requests.get(f"{schema_base_url}{args['name_topic']}.json")
r_shared = requests.get(f"{schema_base_url}{args['name_shared']}.json")


assert r_topic.status_code == 200, f"Couldn't retrieve schema {args['name_topic']} from {schema_base_url}{args['name_topic']}.json"
assert r_shared.status_code == 200, f"Couldn't retrieve schema {args['name_shared']} from {schema_base_url}{args['name_shared']}.json"

instance = get_instance_from_csv(args['url_instance'])
assert instance, f"Instance could not be read from {args['url_instance']}"

registry = register_schemas(r_topic, r_shared)

## create a validator which uses a schema defined in the registry;
## this validator then accepts an instance to validate
v = jsonschema.Draft202012Validator(schema = get_schema_jsons(r_topic, r_shared)["topic"],
                                    registry = registry)

    
print(json.dumps([{"path" : ','.join(e.path), "message" : e.message} 
            for e in v.iter_errors(instance = instance)
            ])
      )




