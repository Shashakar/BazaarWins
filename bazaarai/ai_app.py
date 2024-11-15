import os
from torch.utils.data import DataLoader
from torchvision import datasets, transforms, models
import torch
import torch.nn as nn
import torch.optim as optim

transform = transforms.Compose([
    transforms.Resize((128, 128)),       # Resize images to a standard size
    transforms.RandomHorizontalFlip(),    # Randomly flip images horizontally
    transforms.ToTensor()                 # Convert images to PyTorch tensors
])

train_data = datasets.ImageFolder(os.path.join(".", "item_images"), transform=transform)
val_data = datasets.ImageFolder(os.path.join(".", "data"), transform=transform)


train_loader = DataLoader(train_data, batch_size=32, shuffle=True)
val_loader = DataLoader(val_data, batch_size=32, shuffle=False)

# Load a pretrained ResNet model with updated syntax
model = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)

# Freeze the feature layers to retain the pretrained weights
for param in model.parameters():
    param.requires_grad = False

# Replace the final layer with a new layer for your specific number of items
num_classes = len(train_data.classes)
model.fc = nn.Linear(model.fc.in_features, num_classes)

# Define loss function and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.fc.parameters(), lr=0.001)

# Training loop
num_epochs = 5
model.train()
for epoch in range(num_epochs):
    running_loss = 0.0
    for images, labels in train_loader:
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
    print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {running_loss/len(train_loader)}')

model.eval()
correct = 0
total = 0
with torch.no_grad():
    for images, labels in val_loader:
        outputs = model(images)
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

print(f'Validation Accuracy: {100 * correct / total}%')

torch.save(model.state_dict(), 'item_classifier.pth')