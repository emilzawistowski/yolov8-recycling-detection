import os
import shutil
import random

INPUT_DIR = "dataset"
OUTPUT_DIR = "yolo_dataset"
TRAIN_RATIO = 0.8
CLASS_NAMES = ["chair", "couch", "bed", "dining table", "bench"]

for split in ["train", "val"]:
    for subfolder in ["images", "labels"]:
        path = os.path.join(OUTPUT_DIR, subfolder, split)
        os.makedirs(path, exist_ok=True)

def create_yolo_bbox_file(label_path, class_id):
    content = f"{class_id} 0.5 0.5 1.0 1.0\n"
    with open(label_path, "w") as f:
        f.write(content)

for class_id, cls in enumerate(CLASS_NAMES):
    cls_input_dir = os.path.join(INPUT_DIR, cls)
    if not os.path.exists(cls_input_dir):
        print(f"Brak folderu dla klasy: {cls}")
        continue

    images = [f for f in os.listdir(cls_input_dir) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    random.shuffle(images)
    split_index = int(len(images) * TRAIN_RATIO)
    train_imgs = images[:split_index]
    val_imgs = images[split_index:]

    for split, split_imgs in zip(["train", "val"], [train_imgs, val_imgs]):
        for idx, img_name in enumerate(split_imgs, start=1):
            src_path = os.path.join(cls_input_dir, img_name)

            new_img_name = f"{cls.replace(' ', '_')}_{idx}.jpg"
            dst_image_path = os.path.join(OUTPUT_DIR, "images", split, new_img_name)
            shutil.copy(src_path, dst_image_path)

            txt_name = os.path.splitext(new_img_name)[0] + ".txt"
            dst_label_path = os.path.join(OUTPUT_DIR, "labels", split, txt_name)
            create_yolo_bbox_file(dst_label_path, class_id)

print("Dataset YOLO gotowy w folderze:", OUTPUT_DIR)
