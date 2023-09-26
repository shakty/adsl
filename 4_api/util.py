import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

from etherscan import Etherscan

import json
import time
import os
import random
import math
import pathlib

## For handling exceptions
import sys, traceback

import scipy.stats as st

# print(pd.__version__)
# print(np.__version__)
# print(requests.__version__)
# print(plt.matplotlib.__version__)

## Loading keys.
#################

# MAIN_DIR = pathlib.Path(__file__).parent.absolute()
# print(MAIN_DIR)

from dotenv import dotenv_values
config = dotenv_values("../.env")

## API functions.
#################


## SNAPSHOT
###########

SNAPSHOT_ENDPOINT = "https://hub.snapshot.org/graphql"

snapshot = Client(
    transport=AIOHTTPTransport(url=SNAPSHOT_ENDPOINT)
)


def snapshot_rest(query, params=None):

    response = requests.post(SNAPSHOT_ENDPOINT,
                            headers={                      
                                'accept': 'application/json'
                            },
                            params={
                                'query': query
                            },
                            timeout=10)

    print(response)
    try:
        my_json = response.json()
        return my_json['data']
    except Exception as e:
        print("Response content with error")
        print(response.content)
        return []
    

## ETHERSCAN
############

def etherscan(params={}):

    ENDPOINT = 'https://api.etherscan.io/api'

    params['apikey'] = config['ETHERSCAN']

    response = requests.get(ENDPOINT,
                            headers={
                                'accept': 'application/json',
                                "User-Agent": ""
                            },
                            params=params,
                            timeout=10)

    print(response)
    return response.json()


eth = Etherscan(config['ETHERSCAN'])

## THE GRAPH
############

## Endpoints depends on subgraph of interest.
def get_thegraph_client(endpoint): 

    transport = AIOHTTPTransport(url=endpoint)
    client = Client(
        transport=transport
        #fetch_schema_from_transport=True
    )
    return client


## Utility functions.
#####################
   

def pd_read_json(file):
    ## Prevents Value too big Error.
    with open(file) as f:
        df = json.load(f)
    df = pd.DataFrame(df)
    return df

def pd_read_dir(dir, blacklist=None, whitelist=None, ext=('.json'), count_only=False):
    
    counter = 0
    dir_df = pd.DataFrame()

    for file in os.listdir(dir):
        if blacklist and file in blacklist:
            continue
        if whitelist and file not in whitelist:
            continue

        if file.endswith(ext):
            if count_only:
                counter += 1
            else:
                tmp_df = pd_read_json(dir + '/' + file)
                dir_df = pd.concat([dir_df, tmp_df])

    if count_only:
        return counter
    else:
        return dir_df


def get_query(filename, do_gql=False, query_dir="gql_queries/"):
    with open(query_dir + filename.replace(".gql", "") + ".gql") as f:
        query = f.read()
        if do_gql: query = gql(query)
    return query
    
## Alias gq.
gq = get_query


## Get all function.
####################

def _gql_all_set_default_throttle(throttle):
    # The first iteration is probably None
    if ('time' not in throttle) or (throttle['time'] is None):
        throttle['time'] = time.time()

    if ('req' not in throttle) or (throttle['req'] is None):
        throttle['req'] = 0

    if ('sec' not in throttle) or (throttle['sec'] is None):
        throttle['sec'] = 10

    if ('wait_max' not in throttle) or (throttle['wait_max'] is None):
        throttle['wait_max'] = throttle['sec'] + 2
    
    if ('wait_min' not in throttle) or (throttle['wait_min'] is None):
        throttle['wait_min'] = 1

    return throttle
 
async def gql_all(query, 
                  field, 
                  platform="tally", 
                  ## first and skip as in Snapshot. If platform is "tally"
                  ## they become ""
                  first=1000, 
                  skip=None, 
                  initial_list=None, 
                  counter = True, limit=None, 
                  save=None,
                  save_filename=None,
                  save_interval=10,
                  save_every=2000,
                  clear_on_save = False, 
                  append=True, 
                  rest=False, 
                  data_dir="data", 
                  save_counter = None, 
                  vars=None,
                  retry=False, 
                  max_retry=3, 
                  throttle={
                    "sec": 10,
                    "max": None,
                    "req": 0,
                    "time": None,
                    "sleep": 1
                  }):

    ## Boolean Flag to do Tally or Snapshot
    do_tally = True if platform.lower() == "tally" else False

    ## Result from server.
    res = None

    ## The returned value and the varible used to accumulate results.
    out = []

    def should_save(last=False):
        nonlocal save
        if not save: return False

        nonlocal save_every
        if save_every is not None:
            nonlocal out
            if last: return len(out) > 0
            return len(out) > save_every
        
        else:
            nonlocal my_counter, save_interval
            res = my_counter % save_interval == 0
            if last: res = not res
            return res
         
    ## Utility function to save intermediate and final results.
    def save_json():

        # Pandas has problem load pure json saves.
        # Hence we create a pandas Dataframe and save it.
        # nonlocal append
        # flag = "a" if append else "w"
        # with open("data/" + save, flag) as f:
        #     json.dump(out, f)
        #     print("Saved.")

        nonlocal out
        df = pd.DataFrame(out)

        # Introduced save_filename.
        filename = save_filename if save_filename is not None else save

        if clear_on_save:
            
            nonlocal save_counter
            
            sv = str(save_counter)
            sv = sv.zfill(5)
            save_counter += 1

            filename = filename.replace('.json', '_' + sv + '.json')
            
            out = []
            out_str = "Saved and cleared."
        else:
            # Removed when save_filename introduced.
            # filename = save
            out_str = "Saved."
        
        df.to_json(data_dir + "/" + filename, orient="records")
        print(out_str)


    def handleException(res):
        
        nonlocal n_retry

        exc_type, exc_value, exc_traceback = sys.exc_info()

        print("*** print_tb:")
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
        # print("*** print_exception:")
        # traceback.print_exception(exc_value, limit=2, file=sys.stdout)
        print("*** print_exc:")
        traceback.print_exc(limit=2, file=sys.stdout)
        print("*** format_exc, first and last line:")
        formatted_lines = traceback.format_exc().splitlines()
        print(formatted_lines[0])
        print(formatted_lines[-1])
        # print("*** format_exception:")
        # print(repr(traceback.format_exception(exc_value)))
        print("*** extract_tb:")
        print(repr(traceback.extract_tb(exc_traceback)))
        print("*** format_tb:")
        print(repr(traceback.format_tb(exc_traceback)))
        print("*** tb_lineno:", exc_traceback.tb_lineno)
        
        print("")

        if res is not None:
            print("Last res")
            print(res)
        else:
            print("No res yet")

        print("")
        if (not retry) or (n_retry == 0):
            print("**An error occurred, exiting early.**")
            if save and len(out) > 0: save_json()
            
            return False
        else:
            if retry:
                n_retry -= 1
                print("**An error occurred, n_retry: " + str(n_retry) + " **")
                return True
            else:
                return False   

    ## Load initial list.
    ## If no skip is provided, then skip is set to the length of
    ## the initial list, otherwise we use the user-specified value
    if initial_list:
        out = initial_list
        if skip is None:
            skip = len(out)
    elif skip is None:
        skip = 0

    ## Make a GQL query object, if necessary.
    if not rest and type(query) == str:
        query = gql(query)
        

    if save and (save_counter is None):
        save_counter = pd_read_dir(data_dir, count_only=True) + 1
        print("Save counter auto-detected:", save_counter)


    n_retry = max_retry
    my_counter = 0
    fetch = True

    # If throttle is enabled, we need to keep track of time.
    if ('max' in throttle) and (throttle['max'] is not None):
        throttle = _gql_all_set_default_throttle(throttle)


    while fetch:
        
        ## Throttle.
        if throttle['max'] is not None:

            # print(throttle)

            ## Is it time to check?
            elapsed = time.time() - throttle['time']
            if elapsed >= throttle['sec']:

                # Do we have too many requests?
                if throttle['req'] >= throttle['max']:

                    # Sleep for at most the one cycle of time-check.
                    wait_time = min(0.3  * (throttle['req'] - throttle['max']), 
                                    throttle['wait_max'])
                    if wait_time < throttle['wait_min']: wait_time = throttle['wait_min']

                    print("Throttling: " + str(throttle['req']) + " in " + str(elapsed))
                    time.sleep(wait_time)
                    
                    # Restart counting.
                    throttle['time'] = time.time()
                    throttle['req'] =  0

            
            throttle['req'] += 1



        # Re-init variables.
        res = None
        thrown = False
        my_counter += 1
        
        if limit and my_counter > limit:
            print('**Limit reached: ', limit)
            fetch = False
            continue

        if rest:

            ## TODO: for tally it needs to be adjusted.

            idx_bracket = query.find("{")
            q = "query " + query[idx_bracket:]
            # Building query manually.
            # q = query.replace("($first: Int!, $skip: Int!)", "")
            q = q.replace("$first", str(first))
            q = q.replace("$skip", str(skip))
            # print(q)

            ## Optional additional variables.
            if vars:
                for v in vars:
                    # where = v + ": $" + v
                    # replaced = v + ": " + str(vars[v])
                    q = q.replace("$" + v, '"' + str(vars[v]) + '"')

            # print(q)

            try:
                if do_tally:
                    res = tally_rest(q)
                else: 
                    res = snapshot_rest(q)
                
            except Exception as e:
                 fetch = handleException(res)
                 thrown = True
        else:
            
            if do_tally:
                ## TODO: check that variables are not overwritten.
                _vars = { "pagination": {"limit": first, "offset": skip} }
            else:
                _vars = {"first": first, "skip": skip}

            ## Optional additional variables.
            if vars:
                _vars = _vars | vars

            try:
                if do_tally:
                    res = await tally.execute_async(query,
                                                    variable_values=_vars)
                else:
                    res = await snapshot.execute_async(query,
                                                       variable_values=_vars)
                    
            except Exception as e:
                fetch = handleException(res)
                thrown = True

        ## If no error was raised we save results and increment.
        ## If an error was raised, we will either exit early or repeat
        ## the same iteration.
        if not thrown:
            n_retry = max_retry
            if not res[field]:
                print('**I am done fetching!**')
                fetch = False
            else:
                out.extend(res[field])
                skip += first
                if counter: print(my_counter, len(out))

                if should_save(): save_json()

    if should_save(): save_json()

    return out


def do_throttle(throttle):
    ## Throttle.
    if throttle['max'] is not None:

        # print(throttle)

        ## Is it time to check?
        elapsed = time.time() - throttle['time']
        if elapsed >= throttle['sec']:

            # Do we have too many requests?
            if throttle['req'] >= throttle['max']:

                # Sleep for at most the one cycle of time-check.
                wait_time = min(0.3  * (throttle['req'] - throttle['max']), 
                                throttle['wait_max'])
                if wait_time < throttle['wait_min']: wait_time = throttle['wait_min']

                print("Throttling: " + str(throttle['req']) + " in " + str(elapsed))
                time.sleep(wait_time)
                
                # Restart counting.
                throttle['time'] = time.time()
                throttle['req'] =  0

        
        throttle['req'] += 1

async def gql_all2(query, 
                  field,
                  client, 
                  initial_list=None, 
                  counter = True, limit=None, 
                  save=None,
                  save_filename=None,
                  save_interval=10,
                  save_every=2000,
                  clear_on_save = False, 
                  append=True, 
                  rest=False, 
                  data_dir="data", 
                  save_counter = None, 
                  vars=None,
                  retry=False, 
                  max_retry=3, 
                  throttle={
                    "sec": 10,
                    "max": None,
                    "req": 0,
                    "time": None,
                    "sleep": 1
                  }):

    ## Result from server.
    res = None

    ## The returned value and the varible used to accumulate results.
    out = []

    def should_save(last=False):
        nonlocal save
        if not save: return False

        nonlocal save_every
        if save_every is not None:
            nonlocal out
            if last: return len(out) > 0
            return len(out) > save_every
        
        else:
            nonlocal my_counter, save_interval
            res = my_counter % save_interval == 0
            if last: res = not res
            return res
         
    ## Utility function to save intermediate and final results.
    def save_json():

        # Pandas has problem load pure json saves.
        # Hence we create a pandas Dataframe and save it.
        # nonlocal append
        # flag = "a" if append else "w"
        # with open("data/" + save, flag) as f:
        #     json.dump(out, f)
        #     print("Saved.")

        nonlocal out
        df = pd.DataFrame(out)

        # Introduced save_filename.
        filename = save_filename if save_filename is not None else save

        if clear_on_save:
            
            nonlocal save_counter
            
            sv = str(save_counter)
            sv = sv.zfill(5)
            save_counter += 1

            filename = filename.replace('.json', '_' + sv + '.json')
            
            out = []
            out_str = "Saved and cleared."
        else:
            # Removed when save_filename introduced.
            # filename = save
            out_str = "Saved."
        
        df.to_json(data_dir + "/" + filename, orient="records")
        print(out_str)


    def handleException(res):
        
        nonlocal n_retry

        exc_type, exc_value, exc_traceback = sys.exc_info()

        print("*** print_tb:")
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
        # print("*** print_exception:")
        # traceback.print_exception(exc_value, limit=2, file=sys.stdout)
        print("*** print_exc:")
        traceback.print_exc(limit=2, file=sys.stdout)
        print("*** format_exc, first and last line:")
        formatted_lines = traceback.format_exc().splitlines()
        print(formatted_lines[0])
        print(formatted_lines[-1])
        # print("*** format_exception:")
        # print(repr(traceback.format_exception(exc_value)))
        print("*** extract_tb:")
        print(repr(traceback.extract_tb(exc_traceback)))
        print("*** format_tb:")
        print(repr(traceback.format_tb(exc_traceback)))
        print("*** tb_lineno:", exc_traceback.tb_lineno)
        
        print("")

        if res is not None:
            print("Last res")
            print(res)
        else:
            print("No res yet")

        print("")
        if (not retry) or (n_retry == 0):
            print("**An error occurred, exiting early.**")
            if save and len(out) > 0: save_json()
            
            return False
        else:
            if retry:
                n_retry -= 1
                print("**An error occurred, n_retry: " + str(n_retry) + " **")
                return True
            else:
                return False   

    ## Load initial list.
    ## If no skip is provided, then skip is set to the length of
    ## the initial list, otherwise we use the user-specified value
    if initial_list:
        out = initial_list
        skip = len(out)
    else:
        skip = 0

    first = 100

    ## Make a GQL query object, if necessary.
    if not rest and type(query) == str:
        query = gql(query)
        
    if save and (save_counter is None):
        save_counter = pd_read_dir(data_dir, count_only=True) + 1
        print("Save counter auto-detected:", save_counter)

    n_retry = max_retry
    my_counter = 0
    fetch = True

    # If throttle is enabled, we need to keep track of time.
    if ('max' in throttle) and (throttle['max'] is not None):
        throttle = _gql_all_set_default_throttle(throttle)


    while fetch:
        
        do_throttle(throttle)

        # Re-init variables.
        res = None
        thrown = False
        my_counter += 1
        
        if limit and my_counter > limit:
            print('**Limit reached: ', limit)
            fetch = False
            continue

        if rest:

            raise Exception("rest not supported for now")

            ## TODO: for tally it needs to be adjusted.

            # idx_bracket = query.find("{")
            # q = "query " + query[idx_bracket:]
            # # Building query manually.
            # # q = query.replace("($first: Int!, $skip: Int!)", "")
            # q = q.replace("$first", str(first))
            # q = q.replace("$skip", str(skip))
            # # print(q)

            # ## Optional additional variables.
            # if vars:
            #     for v in vars:
            #         # where = v + ": $" + v
            #         # replaced = v + ": " + str(vars[v])
            #         q = q.replace("$" + v, '"' + str(vars[v]) + '"')

            # # print(q)

            # try:
            #     if do_tally:
            #         res = tally_rest(q)
            #     else: 
            #         res = snapshot_rest(q)
                
            # except Exception as e:
            #      fetch = handleException(res)
            #      thrown = True
        else:
           
            try:
                res = await client.execute_async(query, variable_values=vars)
                    
            except Exception as e:
                fetch = handleException(res)
                thrown = True

        ## If no error was raised we save results and increment.
        ## If an error was raised, we will either exit early or repeat
        ## the same iteration.
        if not thrown:
            n_retry = max_retry
            if not res[field]:
                print('**I am done fetching!**')
                fetch = False
            else:
                out.extend(res[field])
                skip += first
                if counter: print(my_counter, len(out))

                if should_save(): save_json()

    if should_save(): save_json()

    return out



async def iter_gql_all2(iter, iter_var, opts):
    
    ## Temporary container, it will be dumped.
    res = []
    ## Kept and returned.
    empty_res = []

    ## Set defaults.

    if not 'data_dir' in opts:
        raise Exception("opts.data_dir is missing")

    if 'save_counter' in opts:
        save_counter = opts['save_counter']
    else:
        save_counter = pd_read_dir(opts['data_dir'], count_only=True) + 1
        print("save_counter", save_counter)

    if not 'vars' in opts: 
        opts['vars'] = {}

    opts['save'] = False

    if not 'save_filename' in opts:
        save_filename = iter_var + ".json"
    else:
        save_filename = opts['save_filename']

    for id in iter:
        
        opts['vars'][iter_var] = [ id ]

        one_res = await gql_all2(**opts)
            
        if len(one_res) > 0:
            res.extend(one_res)
        else:
            empty_res.extend([id])

        ## Save it...
        if len(res) > opts['save_every']:
            save_json3(res, opts['data_dir'], save_filename, save_counter)
            save_counter += 1
            res = []

    return empty_res

async def iter_gql_all(iter, iter_var, opts):
    
    ## Temporary container, it will be dumped.
    res = []
    ## Kept and returned.
    empty_res = []

    ## Set defaults.

    if not 'data_dir' in opts:
        raise Exception("opts.data_dir is missing")

    if 'save_counter' in opts:
        save_counter = opts['save_counter']
    else:
        save_counter = pd_read_dir(opts['data_dir'], count_only=True) + 1
        print("save_counter", save_counter)

    if not 'vars' in opts: 
        opts['vars'] = {}

    opts['save'] = False

    if not 'save_filename' in opts:
        save_filename = iter_var + ".json"
    else:
        save_filename = opts['save_filename']

    for id in iter:
        
        opts['vars'][iter_var] = [ id ]

        one_res = await gql_all(**opts)
            
        if len(one_res) > 0:
            res.extend(one_res)
        else:
            empty_res.extend([id])

        ## Save it...
        if len(res) > opts['save_every']:
            save_json3(res, opts['data_dir'], save_filename, save_counter)
            save_counter += 1
            res = []

    return empty_res


## Utility function to save intermediate and final results.
def save_json3(out, data_dir, file_template, save_counter):

    # Pandas has problem load pure json saves.
    # Hence we create a pandas Dataframe and save it.
    # nonlocal append
    # flag = "a" if append else "w"
    # with open("data/" + save, flag) as f:
    #     json.dump(out, f)
    #     print("Saved.")

        
    sv = str(save_counter)
    sv = sv.zfill(5)
    save_counter += 1

    filename = file_template.replace('.json', '_' + sv + '.json')
    
    out_str = "Saved " + sv

    df = pd.DataFrame(out)
    df.to_json(data_dir + "/" + filename, orient="records")

    print(out_str)

## TALLY.
#########

TALLY_ENDPOINT = "https://api.tally.xyz/query"

def tally_rest(query, params=None, timeout=10):

    response = requests.post(TALLY_ENDPOINT,
                            headers={                      
                                'accept': 'application/json',
                                'Api-key': config['TALLY_KEY']
                            },
                            params={
                                'query': query
                            },
                            timeout=timeout)

    print(response)
    try:
        my_json = response.json()
        return my_json['data']
    except Exception as e:
        print("Response content with error")
        print(response.content)
        return []


tally = Client(
    transport=AIOHTTPTransport(url=TALLY_ENDPOINT,
                               headers={
                                'Api-key': config['TALLY_KEY']
                               })
)

## DESS NODE
############

def dess(query, params=None, timeout=10):

    response = requests.post(config['DESS_NODE_URL'],
                            headers={                      
                                'accept': 'application/json',
                                'Api-key': config['TALLY_KEY']
                            },
                            params={
                                'query': query
                            },
                            timeout=timeout)

    print(response)
    try:
        my_json = response.json()
        return my_json['data']
    except Exception as e:
        print("Response content with error")
        print(response.content)
        return []
