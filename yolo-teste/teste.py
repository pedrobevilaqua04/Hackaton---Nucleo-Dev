from ultralytics import YOLO

model = YOLO("yolo26n-seg.pt")

results = model("prato.jpg", save=True, conf=0.25)

print(results)