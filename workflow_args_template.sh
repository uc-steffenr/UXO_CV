#! /bin/bash
# https://phoenixnap.com/kb/bash-associative-array

# DECLARE ASSOCIATIVE ARRAYS
declare -A general
declare -A preprocess
declare -A tune
declare -A train
declare -A val

optimizers=('SGD' 'Adam' 'AdamW')

# GENERAL ARGS
general['all_opts']=false
general['data']=
general['do_preprocess']=true
general['do_tune']=true
general['do_val']=true
general['imgsz']=
general['opt']=
general['project']=


# PREPROCESS ARGS
preprocess['database_name']=
preprocess['dataset_name']=
preprocess['offset']=''                 # NOTE: NEEDS TO HAVE 2 VALS IN STRING
preprocess['percent_train']=
preprocess['percent_val']=
preprocess['roboflow_version']=
preprocess['seed']=                     # optional
preprocess['shuffle_only']=false


# TUNE ARGS
tune['batch']=
tune['cos-lr']=false                    # optional
tune['epochs']=
tune['exist-ok']=true                   # optional
tune['evolve_population']=              # optional
tune['hyp']=                            # optional
tune['iterations']=
tune['name']=
tune['noplots']=false                   # optional
tune['nosave']=false                    # optional
tune['noval']=false                     # optional
tune['patience']=                       # optional
tune['resume_evolve']=                  # optional
tune['seed']=                           # optional
tune['weights']=


# TRAIN ARGS
train['batch']=
train['cos-lr']=false                   # optional
train['epochs']=
train['exist-ok']=true                  # optional
train['hyp']=
train['name']=
train['nosave']=false                   # optional
train['noval']=false                    # optional
train['noplots']=false                  # optional
train['noautoanchor']=false             # optional
train['patience']=                      # optional
train['resume']=                        # optional
train['seed']=                          # optional
train['weights']=


# VAL ARGS
val['batch']=
val['confidence_threshold']=            # optional
val['name']=
val['weights']=
val['augment']=false                    # optional
val['dnn']=false                        # optional
val['exist-ok']=true                    # optional
val['save-conf']=true                   # optional
val['save-hybrid']=true                 # optional
val['save-json']=true                   # optional
val['save-txt']=true                    # optional
val['verbose']=true                     # optional
