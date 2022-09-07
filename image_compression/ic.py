from PIL import Image
from glob import glob
import os
from tqdm import tqdm

import shutil


import sys
from itertools import chain

from multiprocessing import Pool

# image_dir = "image_dir"
template_dir = 'template'
output_dir = 'output'
error_dir = 'error'


def clean_dir(dir_name):
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)
        os.makedirs(dir_name)
    else:
        os.makedirs(dir_name)


# image_file_list = glob(f"{image_dir}/*")
# image_file_list


def imagesize(filepath):
    """
    获得文件的磁盘大小
    :param filepath:
    :return:
    """
    return os.path.getsize(filepath) / 1024


def compress_image(image_path):
    raw_image = Image.open(image_path)
    temp_image_name = image_path.split(os.sep)[-1]
    template_image = os.path.join(template_dir, temp_image_name)
    output_image = os.path.join(output_dir, temp_image_name)
    error_image = os.path.join(error_dir, temp_image_name)

    target_size = 500  # kb

    try:

        if imagesize(image_path) < target_size:

            shutil.copyfile(image_path, output_image)
        else:
            width, height = raw_image.size
            raw_image.resize((int(width * 0.9), int(height * 0.9)),
                             Image.ANTIALIAS).save(template_image)
            while imagesize(template_image) > target_size:
                template_iamge2 = Image.open(template_image)
                width_2, height_2 = template_iamge2.size
                template_iamge2.resize(
                    (int(width_2 * 0.9), int(height_2 * 0.9)), Image.ANTIALIAS).save(template_image)

            shutil.copyfile(template_image, output_image)
    except Exception as e:
        shutil.copyfile(image_path, error_image)
        print(f'文件保存失败: {image_path}')
        # print(e)


if __name__ == '__main__':
    # 批量创建文件夹
    [clean_dir(i) for i in [template_dir, output_dir, error_dir]]

    image_dir = sys.argv[1]

    image_file_list = list(
        chain(*[glob(os.path.join(image_dir, i)) for i in ['*.png', '*.jpg', '*.jpeg']]))

    # for temp_image_path in tqdm(image_file_list):
    #     compress_image(temp_image_path)

    print(f'\n\n文件保存父目录: {os.getcwd()}\n'
          f'输出文件位置:{os.path.join(os.getcwd(), output_dir)}\n\n')

    # parallel
    P = Pool(processes=10)
    pbar = tqdm(total=len(image_file_list))

    res_temp = [P.apply_async(func=compress_image, args=(i,), callback=lambda _: pbar.update(1)) for i in
                image_file_list]

    _ = [res.get() for res in res_temp]
