The authors proposed a new aerial **UAV123 Dataset** for low altitude UAV target tracking, as well as, a photorealistic UAV simulator that can be coupled with tracking methods. Their benchmark provides the first evaluation of many state-of-the-art and popular trackers on 123 new and fully annotated HD video sequences captured from a low-altitude aerial perspective. 

## Motivation

Despite decades of advancements, visual tracking remains a persistently challenging problem. Evaluating tracking algorithms typically involves testing them on established video benchmarks. The effectiveness of a tracker is gauged against these benchmarks, making it crucial to ensure they encompass a comprehensive range of real-world scenarios and tracking challenges, such as fast motion, changes in illumination, scale variations, occlusions, and more. These benchmarks play a vital role in shaping future research directions and in the development of robust algorithms. However, a notable gap in these benchmarks is the absence of comprehensive annotated aerial datasets, which are essential for addressing challenges posed by unmanned aerial flight.

The integration of automated computer vision capabilities into unmanned aerial vehicles (UAVs), including tracking and object/activity recognition, has emerged as a significant research focus. This trend is fueled by the growing accessibility of low-cost commercial UAVs. Aerial tracking, beyond its traditional surveillance applications, has opened up new avenues in computer vision, ranging from search and rescue operations to wildlife monitoring, crowd management, navigation, obstacle avoidance, and extreme sports videography. Aerial tracking extends to a diverse array of objects, including humans, animals, cars, boats, and more, many of which are difficult or impossible to track persistently from the ground. Real-world aerial tracking scenarios present unique challenges, necessitating innovative approaches to tackle the tracking problem effectively.

## Dataset description

The authors' work entails evaluating trackers using over 100 newly annotated HD videos captured by a professional-grade UAV. This benchmark serves to complement existing benchmarks by addressing the aerial aspect of tracking comprehensively and offering a more diverse range of tracking challenges commonly encountered in low-altitude UAV footage. It stands as the first benchmark to systematically analyze the performance of state-of-the-art trackers on a comprehensive set of annotated aerial sequences featuring specific tracking challenges. The authors anticipate that this dataset, along with the tracker evaluation, will establish a foundational reference point for future advancements in UAV technology and improvements in target trackers. Visual tracking on UAVs holds significant promise, as the camera can dynamically adjust its orientation and position to optimize tracking performance based on visual feedback. This dynamic capability sets it apart from static tracking systems, which passively analyze dynamic scenes. Current benchmarks, which consist of pre-recorded scenes, fall short in quantifying how slower trackers may impact the UAV's ability to effectively track targets in real-time.

Video captured from low-altitude UAVs is inherently different from video in popular tracking datasets. Therefore, the authors propose a new dataset UAV123 with sequences from an aerial viewpoint, a subset of which is meant for long-term aerial tracking (***uav20l***).  The results highlight the effect of camera viewpoint change arising from UAV motion. The variation in bounding box size and aspect ratio with respect to the initial frame is significantly larger in UAV123. Furthermore, being mounted on the UAV, the camera is able to move with the target resulting in longer tracking sequences on average.

<img src="https://github.com/dataset-ninja/uav123/assets/120389559/bd454c2b-f1c4-4c7e-957a-fcd7d373ea74" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;"> Column 1 and 2: Proportional change of the target’s aspect ratio and bounding box size (area in pixels) with respect to the first frame and across three datasets: OTB100, TC128, and UAV123. Results are compiled over all sequences in each dataset as a histogram with log scale on the x-axis. Column 3: Histogram of sequence duration (in seconds) across the three datasets.</span>

The new UAV123 dataset contains a total of 123 video sequences and more than 110K frames making it the second largest object tracking dataset after [ALOV300++](https://www.crcv.ucf.edu/research/data-sets/alov/). The statistics of the authors dataset are compared to existing datasets. 

| Dataset     | UAV123 | UAV20L | VIVID | OTB50 | OTB100 | TC128 | VOT14 | VOT15 | ALOV300 |
|-------------|--------|--------|-------|-------|--------|-------|-------|-------|---------|
| Sequences   | 123    | 20     | 9     | 51    | 100    | 129   | 25    | 60    | 314     |
| Min frames  | 109    | 1717   | 1301  | 71    | 71     | 71    | 171   | 48    | 19      |
| Mean frames | 915    | 2934   | 1808  | 578   | 590    | 429   | 416   | 365   | 483     |
| Max frames  | 3085   | 5527   | 2571  | 3872  | 3872   | 3872  | 1217  | 1507  | 5975    |
| Total frames| 112578 | 58670  | 16274 | 29491 | 59040  | 55346 | 10389 | 21871 | 151657  |

<span style="font-size: smaller; font-style: italic;">Comparison of tracking datasets in the literature.</span>

The UAV123 dataset comprises three distinct subsets:

1) Set1 encompasses 103 sequences captured using a commercial-grade UAV (DJI S1000). These sequences feature various objects tracked at altitudes ranging from 5 to 25 meters. Video recordings were made at frame rates spanning from 30 to 96 FPS and resolutions from 720p to 4K, utilizing a Panasonic GH4 camera equipped with an Olympus M.Zuiko 12mm f2.0 lens mounted on a fully stabilized gimbal system (DJI Zenmuse Z15). All sequences are standardized at 720p and 30 FPS, with annotations provided in the form of upright bounding boxes at 30 FPS. The annotations were manually conducted at 10 FPS and subsequently interpolated linearly to 30 FPS.
2) Set2 comprises 12 sequences captured using a boardcam (lacking image stabilization) affixed to an inexpensive UAV tracking other UAVs. These sequences exhibit lower quality and resolution, often containing noticeable noise due to limitations in video transmission bandwidth. Annotation protocols mirror those of Set1.
3) Set3 features 8 synthetic sequences generated by the authors' proposed UAV simulator. In these sequences, targets traverse predetermined trajectories within various virtual environments rendered using the Unreal4 Game Engine, simulating the perspective of a flying UAV. Annotations are automatically generated at 30 FPS, with full object mask/segmentation also available.

**Note:** the authors did not provide the opportunity to divide the dataset according to the above criteria.

<img src="https://github.com/dataset-ninja/uav123/assets/120389559/fb2f9297-1189-43d6-b423-308ebc1b19bf" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;"> First frame of selected sequences from UAV123 dataset. The red bounding box indicates the ground truth annotation.</span>

The UAV123 dataset encompasses a diverse array of scenes, ranging from urban landscapes to roads, *building*, fields, beaches, and harbor/marina settings. It features a wide spectrum of targets, including *car*, *truck*, *boat*, individuals, *group*, and aerial vehicles (*uav*) engaged in various activities such as walking, cycling, wakeboarding, driving, swimming, and flying. As expected, these sequences present typical visual tracking challenges, such as long-term full and partial occlusion, scale variations, changes in illumination, shifts in viewpoint, background clutter, camera motion, and more.

| Attr | Description                                                                       |
|------|-----------------------------------------------------------------------------------|
| ARC  | ***Aspect Ratio Change***: the fraction of ground truth aspect ratio in the first frame and at least one subsequent frame is outside the range [0.5, 2]. |
| BC   | ***background clutter***: the background near the target has similar appearance as the target. |
| CM   | ***camera motion***: abrupt motion of the camera.                                       |
| FM   | ***fast motion***: motion of the ground truth bounding box is larger than 20 pixels between two consecutive frames. |
| FOC  | ***full occlusion***: the target is fully occluded.                                      |
| IV   | ***illumination variation***: the illumination of the target changes significantly.      |
| LR   | ***low resolution***: at least one ground truth bounding box has less than 400 pixels.    |
| OV   | ***out of view***: some portion of the target leaves the view.                           |
| POC  | ***partial occlusion***: the target is partially occluded.                               |
| SOB  | ***similar object***: there are objects of similar shape or same type near the target.   |
| SV   | ***scale variation***: the ratio of initial and at least one subsequent bounding box is outside the range [0.5, 2]. |
| VC   | ***viewpoint change***: viewpoint affects target appearance significantly.               |

<span style="font-size: smaller; font-style: italic;">Attributes used to characterize each sequence from a tracking perspective.</span>

In aerial surveillance scenarios, object tracking often demands long-term continuity, as the camera can dynamically pursue the target, unlike in static surveillance setups. In designing the dataset, fully annotated lengthy sequences captured in a single continuous shot were intentionally subdivided into subsequences to maintain a manageable level of difficulty. To accommodate long-term tracking, these subsequences were subsequently merged, and the 20 longest sequences were selected for inclusion in the dataset (***uav20l***).
