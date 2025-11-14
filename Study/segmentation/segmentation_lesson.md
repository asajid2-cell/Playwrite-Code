# Semantic and Instance Segmentation

## CMPUT 328 - Assignment 6 Study Guide

---

## Table of Contents

1. [Introduction to Image Segmentation](#1-introduction-to-image-segmentation)
2. [Semantic Segmentation](#2-semantic-segmentation)
3. [Fully Convolutional Networks (FCN)](#3-fully-convolutional-networks-fcn)
4. [Transposed Convolution (Upsampling)](#4-transposed-convolution-upsampling)
5. [U-Net Architecture](#5-u-net-architecture)
6. [Instance Segmentation](#6-instance-segmentation)
7. [Mask R-CNN](#7-mask-r-cnn)
8. [Training Strategies](#8-training-strategies)
9. [Loss Functions](#9-loss-functions)
10. [Evaluation Metrics](#10-evaluation-metrics)
11. [Data Preparation and Labels](#11-data-preparation-and-labels)
12. [Downsampling and Upsampling](#12-downsampling-and-upsampling)
13. [Skip Connections](#13-skip-connections)
14. [State-of-the-Art Models](#14-state-of-the-art-models)
15. [Implementation Guide](#15-implementation-guide)
16. [Common Pitfalls and Solutions](#16-common-pitfalls-and-solutions)

---

## 1. Introduction to Image Segmentation

### What is Image Segmentation?

Image segmentation is the task of partitioning an image into multiple segments or regions, where each pixel is assigned to a specific class or instance.

### Why Image Segmentation?

**Applications:**
- **Medical imaging**: Tumor detection, organ segmentation
- **Autonomous driving**: Road detection, pedestrian identification
- **Satellite imagery**: Land use classification, building detection
- **Agriculture**: Crop health monitoring, weed detection
- **Augmented reality**: Background removal, object tracking

### Types of Segmentation

**1. Semantic Segmentation:**
- Classifies each pixel into a category
- Does NOT distinguish between different instances of the same class
- Example: All "car" pixels labeled as "car", regardless of which car

**2. Instance Segmentation:**
- Semantic segmentation + Object detection
- Distinguishes between different instances
- Example: car₁, car₂, car₃ are labeled separately

**3. Panoptic Segmentation:**
- Combines semantic and instance segmentation
- Every pixel belongs to exactly one segment

---

## 2. Semantic Segmentation

### Definition

**Semantic segmentation** is classifying each pixel of an image into a category or class.

### How It Works

```
Input: RGB Image (H × W × 3)
Output: Label Map (H × W)
```

Each pixel in the output corresponds to a class label.

### Example

```
Input Image: Street scene
Classes: road, car, pedestrian, building, sky, tree
Output: Each pixel labeled with one of these classes
```

### Challenges

1. **High computational cost**: Processing every pixel
2. **Context understanding**: Need both local and global information
3. **Boundary precision**: Accurate segmentation at object edges
4. **Scale variation**: Objects appear at different sizes
5. **Occlusion**: Objects partially hidden by others

### Differences from Classification

| Aspect | Classification | Semantic Segmentation |
|--------|---------------|----------------------|
| Input | Image | Image |
| Output | Single label | Label per pixel |
| Spatial info | Lost (after pooling) | Preserved |
| Complexity | Lower | Higher |

---

## 3. Fully Convolutional Networks (FCN)

### Motivation

Traditional CNNs for classification:
- Use fully connected layers at the end
- Output fixed-size vector
- Lose spatial information

**Problem:** We need spatial output (same size as input)!

### FCN Architecture

**Key idea:** Replace fully connected layers with convolutional layers

```
Input Image (H × W × 3)
    ↓
[Conv + Pool] × N  ← Downsampling (encoder)
    ↓
[Conv Transpose] × M  ← Upsampling (decoder)
    ↓
Output Map (H × W × num_classes)
```

### Why Use Fully Convolutional Architecture?

**Advantages:**
1. **Accepts any input size**: No fixed-size requirement
2. **Preserves spatial information**: Output has spatial structure
3. **Efficient**: Shares computation across overlapping regions
4. **End-to-end training**: Learn features and segmentation together

### Converting FC to Conv

```python
# Traditional classification network
x = x.view(x.size(0), -1)  # Flatten: [batch, C*H*W]
x = self.fc(x)              # FC layer

# Fully convolutional network
# No flattening!
x = self.conv(x)  # [batch, channels, h, w] preserved
```

### Output Size Calculation

After multiple conv and pool operations:
```
Input: 32×32
After Conv (stride=1, padding=1): 32×32
After MaxPool (2): 16×16
After Conv (stride=1, padding=1): 16×16
After MaxPool (2): 8×8
```

**Problem:** Output is smaller than input!
**Solution:** Upsampling operations

---

## 4. Transposed Convolution (Upsampling)

### What is Transposed Convolution?

Also called **"deconvolution"** or **"upsampling"**:
- Increases spatial dimensions
- Learnable upsampling (unlike simple interpolation)
- Inverse operation of convolution (roughly)

### How It Works

**Regular convolution:**
- Slides filter over input
- Produces smaller or same-size output

**Transposed convolution:**
- Slides filter, but expands output
- Adds overlap and sums

### Mathematical Intuition

For a simple case:
```
Input = conv(output, kernel, stride)
Output = conv_transpose(input, kernel, stride)
```

### Example

```
Input: 2×2
Kernel: 3×3
Stride: 2
Output: 5×5  (larger!)
```

**Process:**
1. Insert zeros between input pixels (based on stride)
2. Apply regular convolution
3. Result is upsampled output

### In PyTorch

```python
nn.ConvTranspose2d(
    in_channels=64,
    out_channels=32,
    kernel_size=3,
    stride=2,
    padding=1,
    output_padding=1
)

# Input: [batch, 64, 16, 16]
# Output: [batch, 32, 32, 32]
```

### Output Size Formula

```
output_size = (input_size - 1) × stride - 2 × padding + kernel_size + output_padding
```

### Transposed Conv vs Bilinear Interpolation

| Aspect | Transposed Conv | Bilinear Interpolation |
|--------|----------------|----------------------|
| Learnable | Yes | No |
| Parameters | Many | None |
| Quality | Better (learned) | Fixed |
| Artifacts | Checkerboard possible | Smooth |

**Best practice:**
- Use bilinear interpolation + Conv for smoother results
- Or use transposed conv with careful initialization

---

## 5. U-Net Architecture

### What is U-Net?

**U-Net** is an important architecture for semantic segmentation, especially popular in medical imaging.

### Architecture Structure

```
       INPUT (572×572)
           ↓
    ┌──────────────┐
    │   Encoder    │ ← Contracting path (downsampling)
    │   (Down)     │
    └──────┬───────┘
           ↓
    ┌──────────────┐
    │  Bottleneck  │ ← Lowest resolution
    └──────┬───────┘
           ↓
    ┌──────────────┐
    │   Decoder    │ ← Expanding path (upsampling)
    │    (Up)      │   + Skip connections →
    └──────┬───────┘
           ↓
      OUTPUT (388×388)
```

### Key Features

**1. Encoder-Decoder Structure:**
- **Encoder**: Downsamples, captures context
- **Decoder**: Upsamples, enables precise localization

**2. Skip Connections:**
- Connects encoder to decoder at same resolution
- Preserves fine-grained details
- Helps gradient flow

**3. Symmetric:**
- Encoder and decoder are mirror images
- "U" shape gives the name

### U-Net Block Structure

**Encoder Block:**
```python
# Each encoder block
Conv(3×3) → BatchNorm → ReLU
Conv(3×3) → BatchNorm → ReLU
MaxPool(2×2)  ← Downsample
```

**Decoder Block:**
```python
# Each decoder block
ConvTranspose(2×2)  ← Upsample
Concatenate with skip connection
Conv(3×3) → BatchNorm → ReLU
Conv(3×3) → BatchNorm → ReLU
```

### Why U-Net Works

1. **Context + Localization**: Encoder captures what, decoder determines where
2. **Skip connections**: Preserve spatial information lost during downsampling
3. **Few parameters**: Works well even with small datasets
4. **Data augmentation friendly**: Can be trained with limited data

### U-Net vs FCN

| Feature | U-Net | FCN |
|---------|-------|-----|
| Skip connections | Yes (concat) | Yes (add) |
| Structure | Symmetric U | Asymmetric |
| Best for | Medical imaging, small data | General segmentation |
| Parameters | Moderate | Varies |

---

## 6. Instance Segmentation

### What is Instance Segmentation?

**Instance segmentation** = Semantic segmentation + Object detection

**Goal:** Detect and segment each object instance separately

### Difference from Semantic Segmentation

```
Semantic Segmentation:
- All cars labeled as "car"
- Cannot distinguish car₁ from car₂

Instance Segmentation:
- car₁, car₂, car₃ labeled separately
- Each instance has unique ID
```

### Challenges

1. **Varying number of instances**: Unknown how many objects in image
2. **Overlapping objects**: Objects may occlude each other
3. **Different scales**: Objects appear at different sizes
4. **Computational cost**: More complex than semantic segmentation

### Approaches

**1. Detect-then-Segment:**
- First detect bounding boxes
- Then segment within each box
- Example: Mask R-CNN

**2. Segment-then-Detect:**
- First generate segmentation proposals
- Then cluster into instances

**3. Bottom-up:**
- Segment all pixels
- Group pixels into instances
- Example: Associative embedding

---

## 7. Mask R-CNN

### Overview

**Mask R-CNN** extends Faster R-CNN by adding a branch for predicting segmentation masks on each Region of Interest (RoI).

### Architecture

```
Input Image
    ↓
┌─────────────────────┐
│  Backbone (ResNet)  │ ← Feature extraction
└─────────┬───────────┘
          ↓
┌─────────────────────┐
│  Region Proposal    │ ← Propose object locations
│  Network (RPN)      │
└─────────┬───────────┘
          ↓
┌─────────────────────┐
│   RoI Align         │ ← Extract features for each proposal
└─────────┬───────────┘
          ↓
    ┌────┴────┐
    ↓         ↓         ↓
┌────────┐ ┌────────┐ ┌────────┐
│  Box   │ │ Class  │ │  Mask  │ ← Three parallel heads
│Regress │ │Predict │ │ Predict│
└────────┘ └────────┘ └────────┘
```

### Key Components

**1. Backbone:**
- Usually ResNet-50 or ResNet-101
- Extracts features from input image
- Output: Feature maps

**2. Region Proposal Network (RPN):**
- Proposes candidate object bounding boxes
- Learned, not hand-crafted

**3. RoI Align:**
- Extracts features for each proposal
- Improves on RoI Pooling (no quantization)
- Preserves spatial alignment

**4. Three Heads:**
- **Classification**: What is the object?
- **Bounding box regression**: Where exactly is it?
- **Mask prediction**: What are its pixel-wise boundaries?

### Mask Head

```python
# Mask head architecture
# For each RoI:
Conv(3×3) × 4  ← Feature extraction
ConvTranspose(2×2)  ← Upsample
Conv(1×1)  ← num_classes masks

# Output: [num_classes, 28, 28]
# One binary mask per class
```

### RoI Align vs RoI Pool

**RoI Pool (Faster R-CNN):**
- Quantizes coordinates to integer
- Loses spatial precision
- Bad for segmentation

**RoI Align (Mask R-CNN):**
- Uses bilinear interpolation
- No quantization
- Preserves exact spatial locations
- **Critical for mask quality!**

### Training Mask R-CNN

**Multi-task loss:**
```
L_total = L_cls + L_box + L_mask

Where:
- L_cls: Classification loss (cross-entropy)
- L_box: Bounding box regression loss (smooth L1)
- L_mask: Mask loss (binary cross-entropy per pixel)
```

**Important:** Mask loss only computed for the true class (not all classes)

### Mask R-CNN Performance

**State-of-the-art results on COCO:**
- 37.1 AP (Average Precision) for instance segmentation
- 39.8 AP for object detection

---

## 8. Training Strategies

### Data Augmentation

**Essential augmentations for segmentation:**

1. **Random crop and resize**
```python
transforms.RandomResizedCrop(size, scale=(0.5, 2.0))
```

2. **Horizontal flip** (must flip both image and mask!)
```python
if random.random() > 0.5:
    image = transforms.functional.hflip(image)
    mask = transforms.functional.hflip(mask)
```

3. **Color jitter** (image only)
```python
transforms.ColorJitter(brightness=0.2, contrast=0.2)
```

4. **Random rotation** (both image and mask)
```python
angle = random.uniform(-10, 10)
image = transforms.functional.rotate(image, angle)
mask = transforms.functional.rotate(mask, angle)
```

**CRITICAL:** Always apply same geometric transformation to both image and mask!

### Training Pipeline

```python
for epoch in range(num_epochs):
    model.train()
    for images, masks in train_loader:
        images = images.to(device)
        masks = masks.to(device)

        # Forward pass
        outputs = model(images)

        # Compute loss
        loss = criterion(outputs, masks)

        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    # Validate
    validate(model, val_loader)
```

### Learning Rate Strategies

**1. Warm-up then decay:**
```python
# Start small, increase, then decay
epochs: 0-5: linear increase
epochs: 5-50: cosine decay
```

**2. Poly learning rate:**
```python
lr = base_lr × (1 - iter/max_iter)^power
```

**3. Step decay:**
```python
# Reduce by factor at milestones
milestones = [30, 60, 90]
gamma = 0.1
```

### Batch Size Considerations

- **Larger batch**: More stable, but needs more memory
- **Typical range**: 8-32 for segmentation (depends on image size)
- **Gradient accumulation**: Simulate larger batch with limited GPU

### Class Imbalance

**Problem:** Some classes appear much more than others (e.g., background vs rare object)

**Solutions:**
1. **Weighted loss**: Weight rare classes higher
2. **Focal loss**: Focus on hard examples
3. **Data sampling**: Oversample rare classes

---

## 9. Loss Functions

### Cross-Entropy Loss

**Standard for semantic segmentation:**
```python
criterion = nn.CrossEntropyLoss()
loss = criterion(outputs, targets)

# outputs: [batch, num_classes, H, W]
# targets: [batch, H, W] (class indices)
```

**Formula:**
```
L_CE = -Σ_pixels Σ_classes y_c × log(p_c)
```

### Weighted Cross-Entropy

**For class imbalance:**
```python
# Compute class weights (inverse frequency)
class_weights = torch.tensor([0.5, 2.0, 1.0, ...])
criterion = nn.CrossEntropyLoss(weight=class_weights)
```

### Dice Loss

**Popular in medical imaging:**
```python
def dice_loss(pred, target):
    smooth = 1.0
    pred_flat = pred.view(-1)
    target_flat = target.view(-1)
    intersection = (pred_flat * target_flat).sum()

    dice = (2. * intersection + smooth) / (
        pred_flat.sum() + target_flat.sum() + smooth
    )

    return 1 - dice
```

**Advantages:**
- Handles class imbalance well
- Directly optimizes overlap
- Works for binary and multi-class

### Focal Loss

**Focuses on hard examples:**
```python
def focal_loss(pred, target, alpha=0.25, gamma=2.0):
    ce_loss = F.cross_entropy(pred, target, reduction='none')
    p_t = torch.exp(-ce_loss)
    focal = alpha * (1 - p_t) ** gamma * ce_loss
    return focal.mean()
```

**Why it works:**
- Easy examples (p_t near 1) get down-weighted
- Hard examples (p_t near 0) dominate the loss
- Prevents easy background from overwhelming

### Combined Loss

**Often best to combine losses:**
```python
total_loss = ce_loss + dice_loss
# or
total_loss = alpha * ce_loss + beta * dice_loss
```

---

## 10. Evaluation Metrics

### Pixel Accuracy

**Simplest metric:**
```python
accuracy = correct_pixels / total_pixels
```

**Problem:** Not good for class imbalance
- If 90% background, predicting all background gives 90% accuracy!

### Mean IoU (Intersection over Union)

**Most common metric for segmentation:**

```
IoU = (Prediction ∩ Ground Truth) / (Prediction ∪ Ground Truth)
```

**Per class:**
```python
def compute_iou(pred, target, class_id):
    pred_mask = (pred == class_id)
    target_mask = (target == class_id)

    intersection = (pred_mask & target_mask).sum()
    union = (pred_mask | target_mask).sum()

    iou = intersection / (union + 1e-6)
    return iou
```

**Mean IoU:**
```python
mean_iou = mean([iou_class_1, iou_class_2, ..., iou_class_n])
```

### Dice Coefficient

**Alternative to IoU:**
```
Dice = 2 × |Prediction ∩ Ground Truth| / (|Prediction| + |Ground Truth|)
```

**Relationship to IoU:**
```
Dice = 2 × IoU / (1 + IoU)
```

### For Instance Segmentation

**Average Precision (AP):**
- Computed at different IoU thresholds
- AP50: IoU threshold = 0.5
- AP75: IoU threshold = 0.75
- AP: Average over thresholds 0.5 to 0.95

**COCO metrics:**
- AP: Primary metric
- AP50, AP75: At specific thresholds
- AP_S, AP_M, AP_L: For small, medium, large objects

---

## 11. Data Preparation and Labels

### Label Format for Semantic Segmentation

**Image-like format:**
```
Training image: RGB (H × W × 3)
Label image: Grayscale (H × W)

Each pixel value = class index
Example:
- 0: background
- 1: car
- 2: person
- 3: road
```

### Creating Label Images

```python
import numpy as np
from PIL import Image

# Create label image (same size as input)
label = np.zeros((H, W), dtype=np.uint8)

# Fill in labels (example: all pixels in certain region)
label[100:200, 100:200] = 1  # Class 1 (e.g., car)
label[50:150, 50:150] = 2    # Class 2 (e.g., person)

# Save as image
Image.fromarray(label).save('label.png')
```

### Dataset Structure

```
dataset/
├── images/
│   ├── train/
│   │   ├── img1.jpg
│   │   ├── img2.jpg
│   └── val/
│       ├── img3.jpg
└── labels/
    ├── train/
    │   ├── img1.png
    │   ├── img2.png
    └── val/
        ├── img3.png
```

### PyTorch Dataset

```python
class SegmentationDataset(Dataset):
    def __init__(self, image_dir, label_dir, transform=None):
        self.image_dir = image_dir
        self.label_dir = label_dir
        self.transform = transform
        self.images = os.listdir(image_dir)

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        img_path = os.path.join(self.image_dir, self.images[idx])
        label_path = os.path.join(self.label_dir, self.images[idx])

        image = Image.open(img_path).convert("RGB")
        label = Image.open(label_path)

        if self.transform:
            image, label = self.transform(image, label)

        return image, label
```

### Important Considerations

1. **Label images must be single-channel** (grayscale)
2. **No compression artifacts**: Save as PNG, not JPEG
3. **Same dimensions**: Label must match image size
4. **Class indices start from 0**
5. **Background typically class 0**

---

## 12. Downsampling and Upsampling

### Why Downsample?

**Computational efficiency:**
- Processing smaller feature maps is faster
- Reduces memory usage
- Enables deeper networks

**Larger receptive field:**
- Each pixel "sees" more of the image
- Captures more context

**Does NOT hurt segmentation accuracy when combined with upsampling!**

### Downsampling Methods

**1. Max Pooling:**
```python
nn.MaxPool2d(kernel_size=2, stride=2)
# 32×32 → 16×16
```
- Preserves strong activations
- No learnable parameters
- Information loss

**2. Strided Convolution:**
```python
nn.Conv2d(in_ch, out_ch, kernel_size=3, stride=2, padding=1)
# 32×32 → 16×16
```
- Learnable downsampling
- More parameters
- Better than pooling in some cases

### Upsampling Methods

**1. Transposed Convolution (see Section 4):**
```python
nn.ConvTranspose2d(in_ch, out_ch, kernel_size=3, stride=2, padding=1)
```
- Learnable
- Can produce checkerboard artifacts

**2. Bilinear Interpolation:**
```python
nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True)
```
- Fixed, not learnable
- Smooth results
- No artifacts

**3. Bilinear + Conv (Recommended):**
```python
nn.Sequential(
    nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True),
    nn.Conv2d(in_ch, out_ch, kernel_size=3, padding=1)
)
```
- Combines smoothness + learning
- Avoids checkerboard artifacts
- Often works better than transposed conv

### Downsampling-Upsampling Pipeline

```
Input: 256×256
    ↓ Conv + Pool
    128×128
    ↓ Conv + Pool
    64×64
    ↓ Conv + Pool
    32×32  ← Bottleneck (most compressed)
    ↓ Upsample + Conv
    64×64
    ↓ Upsample + Conv
    128×128
    ↓ Upsample + Conv
Output: 256×256
```

---

## 13. Skip Connections

### What are Skip Connections?

**Direct connections from encoder to decoder at same resolution:**

```
Encoder              Decoder

32×32 ─────────────→ 32×32 (concat or add)
  ↓                     ↑
16×16 ─────────────→ 16×16
  ↓                     ↑
 8×8  ─────────────→  8×8
  ↓                     ↑
 4×4  ←─ bottleneck
```

### Why Skip Connections?

**1. Preserve spatial details:**
- Downsampling loses fine-grained information
- Skip connections bring it back

**2. Better gradient flow:**
- Easier for gradients to flow during backprop
- Speeds up training

**3. Combine features:**
- Low-level features (edges) + High-level features (semantics)
- Best of both worlds

### Types of Skip Connections

**1. Concatenation (U-Net style):**
```python
# Encoder output: [batch, 64, 32, 32]
# Decoder output: [batch, 64, 32, 32]
# Concatenate along channel dimension
skip = torch.cat([encoder_out, decoder_out], dim=1)
# Result: [batch, 128, 32, 32]
```

**2. Addition (ResNet style):**
```python
# Both must have same channels
skip = encoder_out + decoder_out
# Result: [batch, 64, 32, 32]
```

### Implementation

```python
class UNetWithSkips(nn.Module):
    def forward(self, x):
        # Encoder
        e1 = self.enc1(x)      # 256×256
        e2 = self.enc2(e1)     # 128×128
        e3 = self.enc3(e2)     # 64×64
        e4 = self.enc4(e3)     # 32×32

        # Bottleneck
        b = self.bottleneck(e4)  # 16×16

        # Decoder with skip connections
        d4 = self.dec4(torch.cat([b, e4], dim=1))    # 32×32
        d3 = self.dec3(torch.cat([d4, e3], dim=1))   # 64×64
        d2 = self.dec2(torch.cat([d3, e2], dim=1))   # 128×128
        d1 = self.dec1(torch.cat([d2, e1], dim=1))   # 256×256

        return self.final(d1)
```

### Skip Connections: With vs Without

| Aspect | Without Skips | With Skips |
|--------|--------------|-----------|
| Boundary quality | Blurry | Sharp |
| Training speed | Slower | Faster |
| Gradient flow | Difficult | Easy |
| Fine details | Lost | Preserved |

**Rule of thumb:** Always use skip connections for segmentation!

---

## 14. State-of-the-Art Models

### DeepLab v3+

**Key innovations:**
1. **Atrous (dilated) convolution**: Enlarges receptive field without pooling
2. **Atrous Spatial Pyramid Pooling (ASPP)**: Multi-scale context
3. **Encoder-decoder with skip connections**

**Performance:** State-of-the-art on PASCAL VOC, Cityscapes

### PSPNet (Pyramid Scene Parsing Network)

**Key innovation:**
- **Pyramid pooling module**: Captures context at multiple scales
- Global average pooling at different scales
- Concatenate multi-scale features

### HRNet (High-Resolution Network)

**Key innovation:**
- Maintains high-resolution representations throughout
- Parallel multi-resolution branches
- Repeated multi-scale fusion

**Advantage:** Better for tasks requiring fine details

### Swin-UNETR

**Recent advancement:**
- Uses Swin Transformer as encoder
- U-Net style decoder
- State-of-the-art for medical imaging

### SAM (Segment Anything Model)

**Foundation model for segmentation:**
- Trained on 11 million images, 1 billion masks
- Zero-shot segmentation
- Interactive (user prompts)
- Can segment anything with minimal guidance

**Use cases:**
- Quick annotation
- Transfer learning
- General-purpose segmentation

---

## 15. Implementation Guide

### Complete U-Net Implementation

```python
import torch
import torch.nn as nn

class UNet(nn.Module):
    def __init__(self, in_channels=3, num_classes=21):
        super(UNet, self).__init__()

        # Encoder
        self.enc1 = self.conv_block(in_channels, 64)
        self.enc2 = self.conv_block(64, 128)
        self.enc3 = self.conv_block(128, 256)
        self.enc4 = self.conv_block(256, 512)

        self.pool = nn.MaxPool2d(2)

        # Bottleneck
        self.bottleneck = self.conv_block(512, 1024)

        # Decoder
        self.upconv4 = nn.ConvTranspose2d(1024, 512, 2, stride=2)
        self.dec4 = self.conv_block(1024, 512)

        self.upconv3 = nn.ConvTranspose2d(512, 256, 2, stride=2)
        self.dec3 = self.conv_block(512, 256)

        self.upconv2 = nn.ConvTranspose2d(256, 128, 2, stride=2)
        self.dec2 = self.conv_block(256, 128)

        self.upconv1 = nn.ConvTranspose2d(128, 64, 2, stride=2)
        self.dec1 = self.conv_block(128, 64)

        # Final layer
        self.final = nn.Conv2d(64, num_classes, 1)

    def conv_block(self, in_ch, out_ch):
        return nn.Sequential(
            nn.Conv2d(in_ch, out_ch, 3, padding=1),
            nn.BatchNorm2d(out_ch),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_ch, out_ch, 3, padding=1),
            nn.BatchNorm2d(out_ch),
            nn.ReLU(inplace=True)
        )

    def forward(self, x):
        # Encoder
        e1 = self.enc1(x)
        e2 = self.enc2(self.pool(e1))
        e3 = self.enc3(self.pool(e2))
        e4 = self.enc4(self.pool(e3))

        # Bottleneck
        b = self.bottleneck(self.pool(e4))

        # Decoder
        d4 = self.upconv4(b)
        d4 = torch.cat([d4, e4], dim=1)
        d4 = self.dec4(d4)

        d3 = self.upconv3(d4)
        d3 = torch.cat([d3, e3], dim=1)
        d3 = self.dec3(d3)

        d2 = self.upconv2(d3)
        d2 = torch.cat([d2, e2], dim=1)
        d2 = self.dec2(d2)

        d1 = self.upconv1(d2)
        d1 = torch.cat([d1, e1], dim=1)
        d1 = self.dec1(d1)

        return self.final(d1)
```

### Training Loop

```python
def train_epoch(model, dataloader, criterion, optimizer, device):
    model.train()
    total_loss = 0

    for images, masks in dataloader:
        images = images.to(device)
        masks = masks.to(device)

        # Forward
        outputs = model(images)
        loss = criterion(outputs, masks)

        # Backward
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    return total_loss / len(dataloader)

def evaluate(model, dataloader, device, num_classes):
    model.eval()
    total_iou = 0

    with torch.no_grad():
        for images, masks in dataloader:
            images = images.to(device)
            masks = masks.to(device)

            outputs = model(images)
            preds = outputs.argmax(dim=1)

            # Compute IoU
            iou = compute_mean_iou(preds, masks, num_classes)
            total_iou += iou

    return total_iou / len(dataloader)

def compute_mean_iou(pred, target, num_classes):
    ious = []
    for cls in range(num_classes):
        pred_cls = (pred == cls)
        target_cls = (target == cls)

        intersection = (pred_cls & target_cls).sum().float()
        union = (pred_cls | target_cls).sum().float()

        if union == 0:
            ious.append(float('nan'))
        else:
            ious.append((intersection / union).item())

    # Mean IoU (ignoring NaN for classes not in ground truth)
    ious = [iou for iou in ious if not np.isnan(iou)]
    return np.mean(ious) if ious else 0.0
```

### Complete Training Script

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader

# Model
model = UNet(in_channels=3, num_classes=21).to(device)

# Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=1e-4)
scheduler = optim.lr_scheduler.ReduceLROnPlateau(
    optimizer, mode='max', patience=5, factor=0.5
)

# Training
num_epochs = 50
best_iou = 0

for epoch in range(num_epochs):
    train_loss = train_epoch(model, train_loader, criterion, optimizer, device)
    val_iou = evaluate(model, val_loader, device, num_classes=21)

    # Update learning rate
    scheduler.step(val_iou)

    print(f"Epoch {epoch+1}/{num_epochs}")
    print(f"Train Loss: {train_loss:.4f}, Val IoU: {val_iou:.4f}")

    # Save best model
    if val_iou > best_iou:
        best_iou = val_iou
        torch.save(model.state_dict(), 'best_unet.pt')
        print(f"Saved best model with IoU: {best_iou:.4f}")
```

---

## 16. Common Pitfalls and Solutions

### Pitfall 1: Wrong Label Format

**Wrong:**
```python
# Labels as one-hot encoded (H, W, num_classes)
labels = torch.zeros(H, W, num_classes)
```

**Correct:**
```python
# Labels as class indices (H, W)
labels = torch.zeros(H, W, dtype=torch.long)
labels[...] = class_id  # 0 to num_classes-1
```

### Pitfall 2: Augmentation Mismatch

**Wrong:**
```python
# Augment image and mask separately
image = transform(image)  # Random crop/flip
mask = transform(mask)    # Different random crop/flip!
```

**Correct:**
```python
# Apply SAME transformation to both
seed = np.random.randint(2**32)
random.seed(seed)
torch.manual_seed(seed)
image = transform(image)

random.seed(seed)
torch.manual_seed(seed)
mask = transform(mask)
```

### Pitfall 3: Size Mismatch

**Problem:** Output size doesn't match input size

**Debug:**
```python
print(f"Input: {x.shape}")
x = model(x)
print(f"Output: {x.shape}")
```

**Solution:** Adjust padding/stride in upsampling layers

### Pitfall 4: Class Imbalance Ignored

**Wrong:**
```python
# Treat all classes equally
criterion = nn.CrossEntropyLoss()
```

**Correct:**
```python
# Weight rare classes higher
class_weights = compute_class_weights(train_dataset)
criterion = nn.CrossEntropyLoss(weight=class_weights)
```

### Pitfall 5: Not Using Skip Connections

**Wrong:**
```python
# Encoder-decoder without skips
x = encoder(x)
x = decoder(x)  # Blurry boundaries!
```

**Correct:**
```python
# With skip connections
e1, e2, e3, e4 = encoder(x)
x = decoder(e1, e2, e3, e4)  # Sharp boundaries!
```

### Pitfall 6: Wrong Evaluation Mode

**Wrong:**
```python
# Not setting eval mode
model.train()  # or not calling eval()
with torch.no_grad():
    outputs = model(images)
```

**Correct:**
```python
model.eval()  # CRITICAL!
with torch.no_grad():
    outputs = model(images)
```

### Pitfall 7: Memory Issues

**Problem:** Out of memory with high-resolution images

**Solutions:**
1. Reduce batch size
2. Use gradient checkpointing
3. Crop images into patches
4. Use mixed precision training

```python
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()

with autocast():
    outputs = model(images)
    loss = criterion(outputs, masks)

scaler.scale(loss).backward()
scaler.step(optimizer)
scaler.update()
```

### Pitfall 8: Ignoring Boundary Pixels

**Problem:** Predictions at image boundaries are poor

**Solution:** Use padding or valid convolutions carefully

### Pitfall 9: Oversmoothing

**Problem:** Predictions are blurry

**Causes:**
- Too many pooling layers
- No skip connections
- Over-regularization

**Solutions:**
- Add skip connections
- Use fewer pooling layers
- Reduce dropout

### Pitfall 10: Not Visualizing Predictions

**Always visualize during training:**
```python
def visualize_predictions(model, image, mask):
    model.eval()
    with torch.no_grad():
        pred = model(image.unsqueeze(0))
        pred = pred.argmax(dim=1).squeeze(0)

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    axes[0].imshow(image.permute(1, 2, 0))
    axes[0].set_title('Input')

    axes[1].imshow(mask)
    axes[1].set_title('Ground Truth')

    axes[2].imshow(pred.cpu())
    axes[2].set_title('Prediction')

    plt.show()
```

---

## Summary

### Key Takeaways

1. **Semantic segmentation** classifies each pixel into a class
2. **Instance segmentation** distinguishes individual object instances
3. **Fully convolutional networks** preserve spatial information
4. **U-Net** architecture with skip connections is highly effective
5. **Transposed convolution** or bilinear interpolation for upsampling
6. **Skip connections** preserve fine-grained details
7. **Mask R-CNN** extends Faster R-CNN for instance segmentation
8. **Data augmentation** must be applied to both image and mask
9. **Mean IoU** is the standard evaluation metric
10. **Class imbalance** requires weighted loss or focal loss

### Typical Results

| Task | Dataset | Metric | Good Result |
|------|---------|--------|-------------|
| Semantic Seg | PASCAL VOC | mIoU | 75-85% |
| Semantic Seg | Cityscapes | mIoU | 75-80% |
| Instance Seg | COCO | AP | 35-40% |

### Next Steps

- Implement U-Net from scratch
- Train on a small dataset (e.g., flower segmentation)
- Experiment with different loss functions
- Try skip connections vs no skip connections
- Visualize learned features
- Explore state-of-the-art models (DeepLab, PSPNet)

---

## References

- [U-Net: Convolutional Networks for Biomedical Image Segmentation](https://arxiv.org/abs/1505.04597)
- [Mask R-CNN](https://arxiv.org/abs/1703.06870)
- [Fully Convolutional Networks for Semantic Segmentation](https://arxiv.org/abs/1411.4038)
- [DeepLab: Semantic Image Segmentation](https://arxiv.org/abs/1606.00915)
- [Segment Anything Model (SAM)](https://arxiv.org/abs/2304.02643)
- [D2L.ai - Semantic Segmentation](https://d2l.ai/chapter_computer-vision/semantic-segmentation-and-dataset.html)
- [D2L.ai - Transposed Convolution](https://d2l.ai/chapter_computer-vision/transposed-conv.html)

---

**End of Lesson**
