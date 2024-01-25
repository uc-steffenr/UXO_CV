import torch

model = torch.hub.load('ultralytics/yolov5', 'custom', 'datasets/noise1.8-rot15/run1/train_results/weights/best.pt')
model.cpu()

im = 'datasets/noise1.8-rot15/test/images/full_database_2024_1_15_7703_eaaq_jpg.rf.6d8786f8e75ba765041065fb4ffa7044.jpg'

results = model(im)
results.print()

print(results.pandas().xyxy[0])
