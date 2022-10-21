import numpy as np
import matplotlib.pyplot as plt
import os


def model_accuracy(dataset_train, dataset_val, test_model, inference_config, modellib, utils):
    image_ids = np.random.choice(dataset_train.image_ids, 30)
    APs = []
    for image_id in image_ids:
        # Load image and ground truth data
        image, image_meta, gt_class_id, gt_bbox, gt_mask =\
            modellib.load_image_gt(dataset_train, inference_config,
                                   image_id, use_mini_mask=False)
        molded_images = np.expand_dims(
            modellib.mold_image(image, inference_config), 0)
        # Run object detection
        results = test_model.detect([image], verbose=0)
        r = results[0]
        # Compute AP
        AP, precisions, recalls, overlaps =\
            utils.compute_ap(gt_bbox, gt_class_id, gt_mask,
                             r["rois"], r["class_ids"], r["scores"], r['masks'])
        APs.append(AP)

    print("Model Accuracy: ", np.mean(APs))
