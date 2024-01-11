#! /bin/bash
# https://phoenixnap.com/kb/bash-associative-array

# DECLARE ASSOCIATIVE ARRAYS
declare -A general
declare -A preprocess
declare -A tune
declare -A train
declare -A val

optimizers=('SGD' 'Adam' 'AdamW')
# optimizers=('Adam' 'AdamW')


# GENERAL ARGS
general['all_opts']=false
general['data']=data.yaml # assuming data.yaml is in dataset_dir
general['do_preprocess']=false
general['do_tune']=true
general['do_train']=true
general['do_val']=true
general['imgsz']=640
general['opt']=Adam
general['project']=all_opts_test
general['dataset_dir']=datasets/full_dataset


# PREPROCESS ARGS
preprocess['database_name']=full_database
preprocess['dataset_name']=full_dataset
preprocess['offset']='1032 1032'                 # NOTE: NEEDS TO HAVE 2 VALS IN STRING
preprocess['percent_train']=0.8
preprocess['percent_val']=0.1
preprocess['roboflow_version']=roboflow_v4
preprocess['seed']=12345                     # optional
preprocess['shuffle_only']=false


# TUNE ARGS
tune['batch']=10
tune['cos-lr']=false                    # optional
tune['epochs']=15
tune['exist-ok']=true                   # optional
tune['evolve_population']=              # optional
tune['hyp']=                            # optional
tune['iterations']=2
tune['name']=tune_results_Adam
tune['noplots']=false                   # optional
tune['noautoanchor']=false              # optional
tune['nosave']=false                    # optional
tune['noval']=false                     # optional
tune['patience']=5                      # optional
tune['resume_evolve']=                  # optional
tune['seed']=                           # optional
tune['weights']=yolov5n.pt # assuming weights are in dataset_dir


# TRAIN ARGS
train['batch']=10
train['cos-lr']=false                   # optional
train['epochs']=100
train['exist-ok']=true                  # optional
train['hyp']=datasets/full_dataset/Adam_test/tune_results/hyp_evolve.yaml
# train['hyp']=hyp_evolve.yaml            # tricky one...
train['name']=train_results_Adam
train['nosave']=false                   # optional
train['noval']=false                    # optional
train['noplots']=false                  # optional
train['noautoanchor']=false             # optional
train['patience']=30                    # optional
train['resume']=                        # optional
train['seed']=                          # optional
train['weights']=yolov5n.pt # assuming weights are in dataset_dir


# VAL ARGS
val['batch']=15
val['confidence_threshold']=            # optional
val['name']=val_results_Adam
val['weights']=datasets/full_dataset/Adam_test/train_results/weights/best.pt
# val['weights']=best.pt                  # also tricky
val['augment']=false                    # optional
val['dnn']=false                        # optional
val['exist-ok']=true                    # optional
val['save-conf']=true                   # optional
val['save-hybrid']=true                 # optional
val['save-json']=true                   # optional
val['save-txt']=true                    # optional
val['verbose']=true                     # optional
