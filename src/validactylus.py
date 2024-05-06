import logging
import argparse
import jsonschema
import requests
import json
import urllib.parse
import referencing # for in-memory registration of schemas
import pandas as pd

logger = logging.getLogger(__name__)


def get_instance_from_csv(csv_url):
    '''reads CSV data from a URL, takes header from first and exemplary data
    from second line, converts to JSON-able dictionnairy.
    Example: {"SITE_CODE" : "foo-bar-baz", ...}
    '''
    try:
        instance = (pd.read_csv(csv_url, sep = ";").head(1)
                    .to_json(orient = "records"))
        instance = json.loads(instance)[0] ## first entry of json array only
    except:
        instance = False
    finally:
        return instance



def get_remote_schemas(schema_base_url, name_topic, name_shared):
    '''
    retrieve validation schemas (1. topic specific and 2. shared definitions)
    from host; raise error if not both schemas can be retrieved
    (i. e. if server status not 200 for either schema)
    '''

    try:
        requests.get(schema_base_url)
    except (requests.exceptions.RequestException):
        raise ValueError(f"failed to contact host \"{schema_base_url}\" " +\
                         "for schemas")

    max_waiting = 5 ## s
    rs = {"schema_topic" : requests.get(f"{schema_base_url}/{name_topic}.json",
                           timeout = max_waiting),
          "schema_shared" : requests.get(f"{schema_base_url}/{name_shared}.json",
                            timeout =max_waiting)
    }
    
    if not all (v.status_code == 200 for k, v in rs.items()):
        raise ValueError(f"\"{name_topic}.json\" and/or " + \
                          f"\"{name_shared}.json\"" + \
                          f" not found at \"{schema_base_url}\"")
            
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

    ## get centrally managed schemas here:
    schema_base_url = ("https://raw.githubusercontent.com/eLTER-RI/"
                       "elter-ci-schemas/main/schemas/")
    ## use JSONSchema version DRAFT202012:
    spec = referencing.jsonschema.DRAFT202012


    ## currently (Apr. 2024) available topic schemas:
    ## ['data_mapping', 'data_observation', 'event', 'license', 'mapping', 
    ## 'method', 'reference', 'sample', 'station']


    parser = argparse.ArgumentParser()
    parser.add_argument("url_instance", type = str,
                        help = ("URL (file or remote) to CSV instance"
                                "to be validated")
                        )
    parser.add_argument("name_topic", type = str,
                        help = "name of a topic-specific schema")
    parser.add_argument("name_shared", type = str,
                        help = ("name of a schema with definitions shared by"
                                " topic schemas ['shared']"))

    args = vars(parser.parse_args()) ## vars converts result to dictionnary

    ## sanitize path arguments
    ## (only the name, e. g. "data_mapping" should be supplied, but anyway:
    args = {k: urllib.parse.quote(v, safe = ":./_-") for k,v in args.items()}
   

    instance = get_instance_from_csv(args['url_instance'])


    registry = register_schemas(r_topic, r_shared)
    ## create a validator which uses a schema defined in the registry;
    ## this validator then accepts an instance to validate
    v = jsonschema.Draft202012Validator(
        schema = get_schema_jsons(r_topic, r_shared)["topic"],
        registry = registry
    )


    print(json.dumps([{"path" : ','.join(e.path), "message" : e.message}
                      for e in v.iter_errors(instance = instance)
                      ])
          )




