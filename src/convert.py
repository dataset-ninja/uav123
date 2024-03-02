import os
import shutil

import supervisely as sly
from dataset_tools.convert import unpack_if_archive
from supervisely.io.fs import (
    file_exists,
    get_file_ext,
    get_file_name,
    get_file_name_with_ext,
)
from tqdm import tqdm

import src.settings as s


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    # Possible structure for bbox case. Feel free to modify as you needs.
    images_pathes = "/home/alex/DATASETS/TODO/Dataset_UAV123/UAV123/data_seq/UAV123"
    bboxes_pathes = "/home/alex/DATASETS/TODO/Dataset_UAV123/UAV123/anno/UAV123"
    uav20l_pathes = "/home/alex/DATASETS/TODO/Dataset_UAV123/UAV123/anno/UAV20L"
    att_pathes = "/home/alex/DATASETS/TODO/Dataset_UAV123/UAV123/anno/UAV123/att"
    ds_name = "ds"
    batch_size = 30

    def create_ann(image_path):
        labels = []
        tags = []

        seq_val = image_path.split("/")[-2]
        seq = sly.Tag(sequence_meta, value=seq_val)
        tags.append(seq)

        if subfolder in uav20l_folders:
            uav20l = sly.Tag(uav20_meta)
            tags.append(uav20l)

        curr_att_data = image_name_to_att.get(get_file_name_with_ext(image_path))
        if curr_att_data is not None:
            for idx, attrib in enumerate(curr_att_data):
                if attrib == "1":
                    att_meta = index_to_meta[idx]
                    att_tag = sly.Tag(att_meta)
                    tags.append(att_tag)

        obj_class = name_to_class[seq_val[:3]]

        image_np = sly.imaging.image.read(image_path)[:, :, 0]
        img_height = image_np.shape[0]
        img_wight = image_np.shape[1]

        curr_data = image_name_to_bbox.get(get_file_name_with_ext(image_path))
        if curr_data is not None:
            if curr_data[0] != "NaN":
                left = int(curr_data[0])
                right = left + int(curr_data[2])
                top = int(curr_data[1])
                bottom = top + int(curr_data[3])
                rectangle = sly.Rectangle(top=top, left=left, bottom=bottom, right=right)
                label = sly.Label(rectangle, obj_class)
                labels.append(label)

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels, img_tags=tags)

    bike = sly.ObjClass("bike", sly.Rectangle)
    bird = sly.ObjClass("bird", sly.Rectangle)
    boat = sly.ObjClass("boat", sly.Rectangle)
    building = sly.ObjClass("building", sly.Rectangle)
    car = sly.ObjClass("car", sly.Rectangle)
    group = sly.ObjClass("group", sly.Rectangle)
    person = sly.ObjClass("person", sly.Rectangle)
    truck = sly.ObjClass("truck", sly.Rectangle)
    uav = sly.ObjClass("uav", sly.Rectangle)
    wakeboard = sly.ObjClass("wakeboard", sly.Rectangle)

    name_to_class = {
        "bik": bike,
        "bir": bird,
        "boa": boat,
        "bui": building,
        "car": car,
        "gro": group,
        "per": person,
        "tru": truck,
        "uav": uav,
        "wak": wakeboard,
    }

    sequence_meta = sly.TagMeta("sequence", sly.TagValueType.ANY_STRING)
    uav20_meta = sly.TagMeta("uav20l", sly.TagValueType.NONE)

    iv_meta = sly.TagMeta("illumination variation", sly.TagValueType.NONE)
    sv_meta = sly.TagMeta("scale variation", sly.TagValueType.NONE)
    poc_meta = sly.TagMeta("partial occlusion", sly.TagValueType.NONE)
    foc_meta = sly.TagMeta("full occlusion", sly.TagValueType.NONE)
    ov_meta = sly.TagMeta("out of view", sly.TagValueType.NONE)
    fm_meta = sly.TagMeta("fast motion", sly.TagValueType.NONE)
    cm_meta = sly.TagMeta("camera motion", sly.TagValueType.NONE)
    bc_meta = sly.TagMeta("background clutter", sly.TagValueType.NONE)
    sob_meta = sly.TagMeta("similar object", sly.TagValueType.NONE)
    arc_meta = sly.TagMeta("aspect ratio change", sly.TagValueType.NONE)
    vc_meta = sly.TagMeta("viewpoint change", sly.TagValueType.NONE)
    lr_meta = sly.TagMeta("low resolution", sly.TagValueType.NONE)

    index_to_meta = {
        0: sv_meta,
        1: arc_meta,
        2: lr_meta,
        3: fm_meta,
        4: foc_meta,
        5: poc_meta,
        6: ov_meta,
        7: bc_meta,
        8: iv_meta,
        9: vc_meta,
        10: cm_meta,
        11: sob_meta,
    }

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(
        obj_classes=[bike, bird, boat, building, car, group, person, truck, uav, wakeboard],
        tag_metas=[
            sequence_meta,
            uav20_meta,
            iv_meta,
            sv_meta,
            poc_meta,
            foc_meta,
            ov_meta,
            fm_meta,
            cm_meta,
            bc_meta,
            sob_meta,
            arc_meta,
            vc_meta,
            lr_meta,
        ],
    )
    api.project.update_meta(project.id, meta.to_json())

    uav20l_folders = [
        get_file_name(data) for data in os.listdir(uav20l_pathes) if get_file_ext(data) == ".txt"
    ]

    dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

    folder_to_split = {
        "bird1": {"bird1_1": 1, "bird1_2": 775, "bird1_3": 1573},
        "car1": {
            "car1_1": 1,
            "car1_2": 751,
            "car1_3": 1627,
        },
        "car6": {"car6_1": 1, "car6_2": 487, "car6_3": 1807, "car6_4": 2953, "car6_5": 3925},
        "car8": {"car8_1": 1, "car8_2": 1357},
        "car16": {"car16_1": 1, "car16_2": 415},
        "group1": {"group1_1": 1, "group1_2": 1333, "group1_3": 2515, "group1_4": 3925},
        "group2": {"group2_1": 1, "group2_2": 907, "group2_3": 1771},
        "group3": {"group3_1": 1, "group3_2": 1567, "group3_3": 2827, "group3_4": 4369},
        "person2": {"person2_1": 1, "person2_2": 1189},
        "person4": {"person4_1": 1, "person4_2": 1501},
        "person5": {"person5_1": 1, "person5_2": 877},
        "person7": {"person7_1": 1, "person7_2": 1249},
        "person8": {"person8_1": 1, "person8_2": 1075},
        "person12": {"person12_1": 1, "person12_2": 601},
        "person14": {"person14_1": 1, "person14_2": 847, "person14_3": 1813},
        "person17": {"person17_1": 1, "person17_2": 1501},
        "person19": {"person19_1": 1, "person19_2": 1243, "person19_3": 2791},
        "truck4": {"truck4_1": 1, "truck4_2": 577},
        "uav1": {"uav1_1": 1, "uav1_2": 1555, "uav1_3": 2473},
    }

    for subfolder in os.listdir(images_pathes):
        curr_images_path = os.path.join(images_pathes, subfolder)
        images_names = os.listdir(curr_images_path)
        image_name_to_bbox = {}
        image_name_to_att = {}

        if subfolder in list(folder_to_split.keys()):
            curr_data = folder_to_split[subfolder]
            for key, val in curr_data.items():
                att_path = os.path.join(att_pathes, key + ".txt")
                with open(att_path) as f:
                    att_data = f.read().split("\n")[0].split(",")
                bboxes_path = os.path.join(bboxes_pathes, key + ".txt")
                with open(bboxes_path) as f:
                    content = f.read().split("\n")
                    for idx, row in enumerate(content):
                        if len(row) > 1:
                            index = str(idx + val)
                            image_name_to_bbox[index.zfill(6) + ".jpg"] = row.split(",")
                            image_name_to_att[index.zfill(6) + ".jpg"] = att_data

        else:
            att_path = os.path.join(att_pathes, subfolder + ".txt")
            with open(att_path) as f:
                att_data = f.read().split("\n")[0].split(",")
            bboxes_path = os.path.join(bboxes_pathes, subfolder + ".txt")
            with open(bboxes_path) as f:
                content = f.read().split("\n")
                for idx, row in enumerate(content):
                    if len(row) > 1:
                        index = str(idx + 1)
                        image_name_to_bbox[index.zfill(6) + ".jpg"] = row.split(",")
                        image_name_to_att[index.zfill(6) + ".jpg"] = att_data

        progress = sly.Progress("Create dataset {}".format(ds_name), len(images_names))

        for img_names_batch in sly.batched(images_names, batch_size=batch_size):
            img_pathes_batch = []
            curr_img_names_batch = []
            for im_name in img_names_batch:
                img_pathes_batch.append(os.path.join(curr_images_path, im_name))
                curr_img_names_batch.append(subfolder + "_" + im_name)

            img_infos = api.image.upload_paths(dataset.id, curr_img_names_batch, img_pathes_batch)
            img_ids = [im_info.id for im_info in img_infos]

            anns = [create_ann(image_path) for image_path in img_pathes_batch]
            api.annotation.upload_anns(img_ids, anns)

            progress.iters_done_report(len(img_names_batch))

    return project
