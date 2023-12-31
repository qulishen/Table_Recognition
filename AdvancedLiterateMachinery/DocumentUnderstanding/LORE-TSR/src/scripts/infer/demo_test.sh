python demo.py ctdet_small \
        --dataset table_small \
        --demo ../data/PTN/images/ \
        --demo_name demo_test \
        --debug 1 \
        --dataset_name PTN \
        --arch dla_34  \
        --K 3000 \
        --MK 5000 \
        --tsfm_layers 3\
        --stacking_layers 3 \
        --gpus 0\
        --wiz_2dpe \
        --wiz_detect \
        --wiz_stacking \
        --convert_onnx 0 \
        --vis_thresh_corner 0.3 \
        --vis_thresh 0.35 \
        --scores_thresh 0.35 \
        --nms \
        --demo_dir ../dir_of_visualization_ptn/ \
        --anno_path ../data/PTN/json/test.json \
        --load_model ../dir_of_ckpt/ckpt_ptn/model_best.pth \
        --load_processor ../dir_of_ckpt/ckpt_ptn/processor_best.pth