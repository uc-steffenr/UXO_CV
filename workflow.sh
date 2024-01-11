#! /bin/bash

source $1

# GENERAL
project_dir="${general['dataset_dir']}/${general['project']}"
general_args=" --project ${project_dir} --data ${general['dataset_dir']}/${general['data']}"
general_args+=" --imgsz ${general['imgsz']}"


# PREPROCESS
if ${general['do_preprocess']}; then
    preprocess_cmd="python preprocess.py"

    [[ -n ${general['seed']} ]] && preprocess_cmd+=" --seed ${preprocess['seed']}"
    [[ -n ${preprocess['percent_train']} ]] && preprocess_cmd+=" --percent_train ${preprocess['percent_train']}"
    [[ -n ${preprocess['percent_val']} ]] && preprocess_cmd+=" --percent_val ${preprocess['percent_val']}"
    [[ -n ${preprocess['roboflow_version']} ]] && preprocess_cmd+=" --roboflow_version ${preprocess['roboflow_version']}"
    [[ -n ${preprocess['database_name']} ]] && preprocess_cmd+=" --database_name ${preprocess['database_name']}"
    [[ -n ${preprocess['dataset_name']} ]] && preprocess_cmd+=" --dataset_name ${preprocess['dataset_name']}"
    [[ -n $"{preprocess['offset']}" ]] && preprocess_cmd+=" --offset ${preprocess['offset']}"
    ${preprocess['shuffle_only']} && preprocess_cmd+=" --shuffle_only"
    echo $preprocess_cmd

    eval $preprocess_cmd
fi


# TUNE
tune_cmd="python yolov5/train.py --evolve ${tune['iterations']}"
tune_cmd+=" --epochs ${tune['epochs']} --batch-size ${tune['batch']}"
tune_cmd+=" --weights ${general['dataset_dir']}/${tune['weights']}"
tune_cmd+=$general_args

[[ -n ${tune['hyp']} ]] && tune_cmd+=" --hyp ${tune['hyp']}"
[[ -n ${tune['seed']} ]] && tune_cmd+=" --seed ${tune['seed']}"
[[ -n ${tune['patience']} ]] && tune_cmd+=" --patience ${tune['patience']}"
[[ -n ${tune['resume_evolve']} ]] && tune_cmd+=" --resume_evolve ${tune['resume_evolve']}"
[[ -n ${tune['evolve_population']} ]] && tune_cmd+=" --evolve_population ${tune['evolve_population']}"

${tune['noplots']} && tune_cmd+=" --noplots"
${tune['nosave']} && tune_cmd+=" --nosave"
${tune['noval']} && tune_cmd+=" --noval"
${tune['exist-ok']} && tune_cmd+=" --exist-ok"
${tune['noautoanchor']} && tune_cmd+=" --noautoanchor"
${tune['cos-lr']} && tune_cmd+=" --cos-lr"

# echo $tune_cmd

# TRAIN
train_cmd="python yolov5/train.py"
train_cmd+=" --weights ${general['dataset_dir']}/${train['weights']} --epochs ${train['epochs']}"
train_cmd+=" --batch-size ${train['batch']}"
train_cmd+=$general_args

# [[ -n ${train['hyp']} ]] && train_cmd+=" --hyp ${train['hyp']}"
[[ -n ${train['seed']} ]] && train_cmd+=" --seed ${train['seed']}"
[[ -n ${train['patience']} ]] && train_cmd+=" --patience ${train['patience']}"
[[ -n ${train['resume']} ]] && train_cmd+=" --resume ${train['resume']}"

${train['nosave']} && train_cmd+=" --nosave"
${train['noval']} && train_cmd+=" --noval"
${train['noplots']} && train_cmd+=" --noplots"
${train['exist-ok']} && train_cmd+=" --exist-ok"
${train['noautoanchor']} && train_cmd+=" --noautoanchor"
${train['cos-lr']} && train_cmd+=" --cos-lr"

# echo $train_cmd


# VAL
# move weights dir to inner loop
val_cmd="python yolov5/val.py"
val_cmd+=" --batch-size ${val['batch']}" # --weights ${val['weights']}"
val_cmd+=$general_args

[[ -n ${val[confidence_threshold'']} ]] && val_cmd+=" --conf ${val['confidence_threshold']}"

${val['augment']} && val_cmd+=" --augment"
${val['dnn']} && val_cmd+=" --dnn"
${val['exist-ok']} && val_cmd+=" --exist-ok"
${val['save-conf']} && val_cmd+=" --save-conf"
${val['save-hybrid']} && val_cmd+=" --save-hybrid"
${val['save-json']} && val_cmd+=" --save-json"
${val['save-txt']} && val_cmd+=" --save-txt"
${val['verbose']} && val_cmd+=" --verbose"

# echo $val_cmd


# RUN SCRIPTS
if ${general['all_opts']}; then
    for opt in "${optimizers[@]}";
    do
        curr_tune_cmd=$tune_cmd" --name ${tune['name']}_${opt} --opt ${opt}"
        curr_train_cmd=$train_cmd" --name ${train['name']}_${opt} --opt ${opt}"
        curr_val_cmd=$val_cmd" --name ${val['name']}_${opt}"

        if ${general['do_tune']}; then
            echo $curr_tune_cmd
            eval $curr_tune_cmd
        fi

        if ${general['do_train']}; then
            if ${general['do_tune']}; then
                curr_train_cmd+=" --hyp ${project_dir}/${tune['name']}_${opt}/hyp_evolve.yaml"
            elif [[ -n ${train['hyp']} ]]; then
                curr_train_cmd+=" --hyp ${train['hyp']}"
            fi

            echo $curr_train_cmd
            eval $curr_train_cmd
        fi

        if ${general['do_val']}; then
            if ${general['do_train']}; then
                curr_val_cmd+=" --weights ${project_dir}/${train['name']}_${opt}/weights/best.pt"
            else
                curr_val_cmd+=" --weights ${val['weights']}"
            fi
            echo $curr_val_cmd
            eval $curr_val_cmd
        fi
    done
else
    tune_cmd+=" --name ${tune['name']} --opt ${general['opt']}"
    train_cmd+=" --name ${train['name']} --opt ${general['opt']}"
    val_cmd+=" --name ${val['name']}"

    if ${general['do_tune']}; then
        echo $tune_cmd
        eval $tune_cmd
    fi

    if ${general['do_train']}; then
            if ${general['do_tune']}; then
                curr_train_cmd+=" --hyp ${project_dir}/${tune['name']}/hyp_evolve.yaml"
            elif [[ -n ${train['hyp']} ]]; then
                curr_train_cmd+=" --hyp ${train['hyp']}"
            fi
        echo $train_cmd
        eval $train_cmd
    fi

    if ${general['do_val']}; then
            if ${general['do_train']}; then
                curr_val_cmd+=" --weights ${project_dir}/${train['name']}/weights/best.pt"
            else
                curr_val_cmd+=" --weights ${val['weights']}"
            fi
        echo $val_cmd
        eval $val_cmd
    fi
fi
