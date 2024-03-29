#! /bin/bash

# TODO: change `original_data` to benchmark and project to run number

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
general['data']=data.yaml
general['do_preprocess']=false
general['do_tune']=true
general['do_train']=false
general['do_val']=false
general['do_test']=false
general['imgsz']=640
general['opt']=SGD
general['project']=tmp
general['dataset_dir']=datasets/benchmark


# PREPROCESS ARGS
preprocess['dataset_name']=benchmark
preprocess['percent_train']=0.8
preprocess['percent_val']=0.1
preprocess['roboflow_name']='original'          # can be multiple directories
preprocess['seed']=12345                     # optional


# TUNE ARGS
tune['batch']=30
tune['cos-lr']=false                    # optional
tune['epochs']=15
tune['exist-ok']=true                   # optional
tune['evolve_population']=              # optional
tune['hyp']=                            # optional
tune['iterations']=10
tune['name']=tune_results
tune['noplots']=false                   # optional
tune['noautoanchor']=false              # optional
tune['nosave']=false                    # optional
tune['noval']=false                     # optional
tune['patience']=5                       # optional
tune['resume_evolve']= # ../datasets/benchmark/run1/tune_results/evolve_population.yaml                 # optional
tune['seed']=                           # optional
tune['weights']=yolov5n.pt


# TRAIN ARGS
train['batch']=30
train['cos-lr']=false                   # optional
train['epochs']=200
train['exist-ok']=true                  # optional
train['hyp']=datasets/benchmark/run1/tune_results/hyp_evolve.yaml
train['name']=train_results
train['nosave']=false                   # optional
train['noval']=false                    # optional
train['noplots']=false                  # optional
train['noautoanchor']=false             # optional
train['noautoanchor']=false             # optional
train['patience']=30                      # optional
train['resume']=                        # optional
train['seed']=                          # optional
train['weights']=yolov5n.pt


# VAL ARGS
val['batch']=30
val['confidence_threshold']=            # optional
val['name']=val_results
val['weights']=datasets/benchmark/run1/train_results/weights/best.pt
val['augment']=false                    # optional
val['dnn']=false                        # optional
val['exist-ok']=true                    # optional
val['save-conf']=true                   # optional
val['save-hybrid']=true                 # optional
val['save-json']=true                   # optional
val['save-txt']=true                    # optional
val['verbose']=true                     # optional

# TEST ARGS
test['batch']=30
test['confidence_threshold']=            # optional
test['name']=test_results
test['weights']=datasets/benchmark/run1/train_results/weights/best.pt
test['augment']=false                    # optional
test['dnn']=false                        # optional
test['exist-ok']=true                    # optional
test['save-conf']=true                   # optional
test['save-hybrid']=true                 # optional
test['save-json']=true                   # optional
test['save-txt']=true                    # optional
test['verbose']=true                     # optional
