import os
import xml.etree.ElementTree as ET
import numpy as np
import cv2
from PIL import Image, ImageEnhance
import random
import shutil

# need to modify
root_path = '/disk2/data/VOCdevkit/VOCdevkit/VOC2007'
txt_sub_path = 'ImageSets/Main/trainval.txt'
xml_sub_path = 'Annotations'
save_balanced_path = 'ImageSets/Main/trainvalbalanced.txt'
img_sub_path = 'JPEGImages'
image_postfix = '.jpg'

# On VOC, no modification is recommended
augmentation_jpg_path = 'augmentation'
augmentation_xml_path = 'augmentation'
shuffle_cls = True
int_after_label = False

classes = []
classes_num = {} # cls:num


def load_image_set_index(trainlist_path):
    """
    Load the indexes listed in this dataset's image set file.
    """
    print "load train list"
    assert os.path.exists(trainlist_path), \
        'Path does not exist: {}'.format(trainlist_path)
    with open(trainlist_path) as f:
        trainlist = [x.strip().split(" ")[0] for x in f.readlines()]

    return trainlist


def classify_images(trainlist):
    """
    classify images based on their groundtruth object labels
    """
    class_dict = {}
    print "trainlist length: {}".format(len(trainlist))
    obj_num = 0
    for image_index in trainlist:
        filename = os.path.join(root_path, xml_sub_path, image_index + '.xml')
        tree = ET.parse(filename)
        objs = tree.findall('object')
        num_objs = len(objs)
        assert num_objs != 0, "num of objs = 0 in {}".format(filename)
        old_cls = ''
        for obj in objs:
            print "trainlist: {}; obj: {}".format(image_index, obj)
            cls = obj.find('name').text.lower().strip()
            if cls == old_cls:
                continue
            if cls in class_dict:
                class_dict[cls].append(image_index)
            else:
                class_dict[cls]=[image_index]
                classes.append(cls)
            old_cls = cls
            obj_num = obj_num + 1
            # print "image_index:{}, class:{}".format(image_index,cls)
    print "obj_num:{}".format(obj_num)

    return class_dict


def img_transform(im):
    # convert cv2 image to PIL image
    PIL_image = Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
    # sample a type of image enhancement to implement
    color_transform_rand = random.random()
    if color_transform_rand < 0.25:
        # change contrast
        img_enhancement = ImageEnhance.Contrast(PIL_image)
    elif color_transform_rand < 0.5:
        # change brightness
        img_enhancement = ImageEnhance.Brightness(PIL_image)
    elif color_transform_rand < 0.75:
        # change color
        img_enhancement = ImageEnhance.Color(PIL_image)
    else:
        # change sharpness
        img_enhancement = ImageEnhance.Sharpness(PIL_image)

    enhance_factor = random.uniform(0.5, 1.5)
    new_image = img_enhancement.enhance(enhance_factor)
    #convert PIL image back to cv2 image
    cv2_image = cv2.cvtColor(np.array(new_image), cv2.COLOR_RGB2BGR)

    return cv2_image


def create_new_txt(class_dict):
    print "create new trainlist:"
    max_cls_num = 0
    for cls in class_dict:
        cur_cls_num = len(class_dict[cls])
        classes_num[cls]=cur_cls_num
        if cur_cls_num > max_cls_num:
            max_cls_num = cur_cls_num

    new_trainlist = []
    index = np.arange(len(classes))
    for i in range(max_cls_num):
        if shuffle_cls:
            np.random.shuffle(index)
        for j in index:
            print "class: {} num: {}".format(j, i)
            quotient = i / len(class_dict[classes[j]])
            remainder = i % len(class_dict[classes[j]])
            if not quotient:
                new_trainlist.append(class_dict[classes[j]][i])
            else:
                im = cv2.imread(os.path.join(root_path, img_sub_path, class_dict[classes[j]][remainder] + image_postfix))
                new_im = img_transform(im)
                cv2.imwrite(os.path.join(root_path, img_sub_path, augmentation_jpg_path, class_dict[classes[j]][remainder] + str(quotient+1) + image_postfix), new_im)
                new_trainlist.append(os.path.join(augmentation_jpg_path, class_dict[classes[j]][remainder] + str(quotient+1)))
                src_xml_path = os.path.join(root_path, xml_sub_path, class_dict[classes[j]][remainder] + '.xml')
                dst_xml_path = os.path.join(root_path, xml_sub_path, augmentation_xml_path, class_dict[classes[j]][remainder] + str(quotient+1) + '.xml')
                shutil.copyfile(src_xml_path, dst_xml_path)
                # new_trainlist.append(class_dict[classes[j]][i % len(class_dict[classes[j]])])
    return new_trainlist


def save_train_txt(new_trainlist, save_balanced_path):
        print "save to {}".format(save_balanced_path)
        with open(save_balanced_path,'w') as f:
            count = 0
            len_new_trainlist = len(new_trainlist)
            for image_index in new_trainlist:
                print "save {}th in total {}".format(count+1, len_new_trainlist)
                # print image_index
                # print type(image_index)
                f.write(str(image_index))
                if int_after_label:
                    f.write(" ")
                    f.write(str(count))
                f.write('\n')
                count = count + 1
        f.close()


if __name__ == '__main__':
    assert os.path.exists(os.path.join(root_path, img_sub_path, augmentation_jpg_path)), \
        'Path does not exist: {}'.format(os.path.join(root_path, img_sub_path, augmentation_jpg_path))
    assert os.path.exists(os.path.join(root_path, xml_sub_path, augmentation_xml_path)), \
        'Path does not exist: {}'.format(os.path.join(root_path, xml_sub_path, augmentation_xml_path))
    train_txt_path = os.path.join(root_path, txt_sub_path)
    print "txt_path:{}".format(train_txt_path)
    trainlist = load_image_set_index(train_txt_path)
    print trainlist[0], trainlist[1]
    class_dict = classify_images(trainlist)
    new_trainlist = create_new_txt(class_dict)
    save_train_txt(new_trainlist, os.path.join(root_path, save_balanced_path))