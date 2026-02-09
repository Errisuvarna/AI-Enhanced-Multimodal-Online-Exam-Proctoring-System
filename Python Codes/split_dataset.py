import os
import random
import shutil

BASE_DIR = "Dataset"
SOURCE_DIR = os.path.join(BASE_DIR, "DataSets")

TRAIN_DIR = os.path.join(BASE_DIR, "train")
VAL_DIR   = os.path.join(BASE_DIR, "val")
TEST_DIR  = os.path.join(BASE_DIR, "test")

TRAIN_RATIO = 0.7
VAL_RATIO = 0.15

classes = ["cheating", "non_cheating"]  # ✅ MATCH FOLDER NAMES

for split in [TRAIN_DIR, VAL_DIR, TEST_DIR]:
    for cls in classes:
        os.makedirs(os.path.join(split, cls), exist_ok=True)

def split_class(class_name):
    class_path = os.path.join(SOURCE_DIR, class_name)

    images = [f for f in os.listdir(class_path)
              if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    random.shuffle(images)

    n_total = len(images)
    n_train = int(n_total * TRAIN_RATIO)
    n_val   = int(n_total * VAL_RATIO)

    train_imgs = images[:n_train]
    val_imgs   = images[n_train:n_train + n_val]
    test_imgs  = images[n_train + n_val:]

    for img in train_imgs:
        shutil.copy(os.path.join(class_path, img),
                    os.path.join(TRAIN_DIR, class_name, img))

    for img in val_imgs:
        shutil.copy(os.path.join(class_path, img),
                    os.path.join(VAL_DIR, class_name, img))

    for img in test_imgs:
        shutil.copy(os.path.join(class_path, img),
                    os.path.join(TEST_DIR, class_name, img))

    print(f"{class_name}: Train={len(train_imgs)}, Val={len(val_imgs)}, Test={len(test_imgs)}")

for cls in classes:
    split_class(cls)

print("✅ Dataset split completed successfully!")
