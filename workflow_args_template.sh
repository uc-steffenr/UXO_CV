#! /bin/bash

# DECLARE ASSOCIATIVE ARRAYS
declare -A general
declare -A preprocess
declare -A tune
declare -A train
declare -A val
declare -A test

optimizers=('SGD' 'Adam' 'AdamW')

# GENERAL ARGS
general['all_opts']=false
general['data']=
general['do_preprocess']=true
general['do_tune']=true
general['do_train']=true
general['do_val']=true
general['do_test']=true
general['imgsz']=
general['opt']=
general['project']=
general['dataset_dir']=


# PREPROCESS ARGS
preprocess['dataset_name']=
preprocess['percent_train']=
preprocess['percent_val']=
preprocess['roboflow_name']=''          # can be multiple directories
preprocess['seed']=                     # optional


# TUNE ARGS
tune['batch']=
tune['cos-lr']=false                    # optional
tune['epochs']=
tune['exist-ok']=true                   # optional
tune['evolve_population']=              # optional
tune['hyp']=                            # optional
tune['iterations']=
tune['name']=tune_results
tune['noplots']=false                   # optional
tune['noautoanchor']=false              # optional
tune['nosave']=false                    # optional
tune['noval']=false                     # optional
tune['patience']=                       # optional
tune['resume_evolve']=                  # optional
tune['seed']=                           # optional
tune['weights']=yolov5n.pt


# TRAIN ARGS
train['batch']=
train['cos-lr']=false                   # optional
train['epochs']=
train['exist-ok']=true                  # optional
train['hyp']=
train['name']=train_results
train['nosave']=false                   # optional
train['noval']=false                    # optional
train['noplots']=false                  # optional
train['noautoanchor']=false             # optional
train['noautoanchor']=false             # optional
train['patience']=                      # optional
train['resume']=                        # optional
train['seed']=                          # optional
train['weights']=yolov5n.pt


# VAL ARGS
val['batch']=
val['confidence_threshold']=            # optional
val['name']=val_results
val['weights']=
val['augment']=false                    # optional
val['dnn']=false                        # optional
val['exist-ok']=true                    # optional
val['save-conf']=true                   # optional
val['save-hybrid']=true                 # optional
val['save-json']=true                   # optional
val['save-txt']=true                    # optional
val['verbose']=true                     # optional

# TEST ARGS
test['batch']=
test['confidence_threshold']=            # optional
test['name']=test_results
test['weights']=
test['augment']=false                    # optional
test['dnn']=false                        # optional
test['exist-ok']=true                    # optional
test['save-conf']=true                   # optional
test['save-hybrid']=true                 # optional
test['save-json']=true                   # optional
test['save-txt']=true                    # optional
test['verbose']=true                     # optional
