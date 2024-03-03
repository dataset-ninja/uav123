**UAV123 Dataset** is a dataset for an object detection task. It is used in the drone inspection domain. 

The dataset consists of 113476 images with 109866 labeled objects belonging to 10 different classes including *person*, *car*, *group*, and other: *wakeboard*, *boat*, *uav*, *bike*, *building*, *truck*, and *bird*.

Images in the UAV123 dataset have bounding box annotations. There are 3610 (3% of the total) unlabeled images (i.e. without annotations). There are no pre-defined <i>train/val/test</i> splits in the dataset. Alternatively, the dataset could be split into 12 tracking perspectives: ***scale variation*** (100919 images), ***camera motion*** (75025 images), ***partial occlusion*** (73677 images), ***aspect ratio change*** (70737 images), ***viewpoint change*** (60143 images), ***similar object*** (43669 images), ***low resolution*** (39016 images), ***out of view*** (33421 images), ***illumination variation*** (32803 images), ***full occlusion*** (30736 images), ***fast motion*** (29387 images), and ***background clutter*** (17942 images). Additionally, images marked with its ***sequence*** and ***uav20l*** tag. The dataset was released in 2016 by the King Abdullah University of Science and Technology, Saudi Arabia.

<img src="https://github.com/dataset-ninja/uav123/raw/main/visualizations/poster.png">
