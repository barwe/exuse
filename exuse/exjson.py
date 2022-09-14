import json

def load_json(fp: str):
    '''read json from a file'''
    with open(fp) as rd:
        return json.load(rd)


def dump_json(obj, fp: str, indent=4):
    '''save json to a file'''
    with open(fp, 'w') as wt:
        json.dump(obj, wt, indent=indent)
