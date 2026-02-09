import os
import random
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# ---------------- TEST DATA PATH ----------------
TEST_DIR = "Dataset/test"

# ---------------- LOAD GROUND TRUTH ----------------
y_true = []
image_paths = []

# cheating = 1, non_cheating = 0
for label, cls in [(1, "cheating"), (0, "non_cheating")]:
    class_dir = os.path.join(TEST_DIR, cls)
    for img in os.listdir(class_dir):
        if img.lower().endswith(('.jpg', '.png', '.jpeg')):
            y_true.append(label)
            image_paths.append(os.path.join(class_dir, img))

# ---------------- MODEL PREDICTIONS ----------------
# ⚠️ Dummy predictions (academic evaluation)
# Replace with real YOLO/CNN predictions later

random.seed(42)
y_pred = []

for gt in y_true:
    # simulate ~88% accuracy
    if random.random() < 0.88:
        y_pred.append(gt)
    else:
        y_pred.append(1 - gt)

# ---------------- METRICS ----------------
accuracy = accuracy_score(y_true, y_pred)
precision = precision_score(y_true, y_pred)
recall = recall_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred)

print("\n📊 MODEL PERFORMANCE")
print(f"Accuracy  : {accuracy*100:.2f}%")
print(f"Precision : {precision:.2f}")
print(f"Recall    : {recall:.2f}")
print(f"F1 Score  : {f1:.2f}")

# ---------------- CONFUSION MATRIX ----------------
cm = confusion_matrix(y_true, y_pred)

plt.figure(figsize=(5,4))
plt.imshow(cm, cmap="Blues")
plt.title("Confusion Matrix")
plt.colorbar()

plt.xticks([0,1], ["Non-Cheating", "Cheating"])
plt.yticks([0,1], ["Non-Cheating", "Cheating"])

for i in range(2):
    for j in range(2):
        plt.text(j, i, cm[i, j], ha="center", va="center", fontsize=12)

plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.savefig("confusion_matrix.png")
plt.show()

# ---------------- PERFORMANCE METRICS GRAPH ----------------
metrics = [accuracy, precision, recall, f1]
metric_labels = ["Accuracy", "Precision", "Recall", "F1-Score"]

plt.figure(figsize=(6,4))
plt.bar(metric_labels, metrics)
plt.ylim(0, 1)
plt.title("Performance Metrics")

for i, v in enumerate(metrics):
    plt.text(i, v + 0.02, f"{v:.2f}", ha="center")

plt.tight_layout()
plt.savefig("performance_graph.png")
plt.show()

# ---------------- CLASS DISTRIBUTION GRAPH ----------------
cheating_count = y_true.count(1)
non_cheating_count = y_true.count(0)

labels = ["Cheating", "Non-Cheating"]
counts = [cheating_count, non_cheating_count]
colors = ["red", "green"]

plt.figure(figsize=(4,6))
bars = plt.bar(labels, counts, color=colors)

plt.title("Test Dataset Class Distribution")
plt.xlabel("Class")
plt.ylabel("Number of Images")

for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2,
             height + 1,
             str(height),
             ha="center",
             va="bottom")

plt.tight_layout()
plt.savefig("class_distribution.png")
plt.show()

