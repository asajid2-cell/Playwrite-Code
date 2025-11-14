import genanki
import random

# Generate unique IDs
DECK_ID = random.randrange(1 << 30, 1 << 31)
MODEL_ID = random.randrange(1 << 30, 1 << 31)

# Define custom model with black/white styling
model = genanki.Model(
    MODEL_ID,
    'CNN CIFAR-10 Model',
    fields=[
        {'name': 'Question'},
        {'name': 'Answer'},
        {'name': 'Category'},
        {'name': 'Code'},
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '''
                <div class="card">
                    <div class="category-badge">{{Category}}</div>
                    <div class="question">{{Question}}</div>
                </div>
            ''',
            'afmt': '''
                <div class="card">
                    <div class="category-badge">{{Category}}</div>
                    <div class="question">{{Question}}</div>
                    <hr>
                    <div class="answer">{{Answer}}</div>
                    {{#Code}}
                    <div class="code-block">{{Code}}</div>
                    {{/Code}}
                </div>
            ''',
        },
    ],
    css='''
        .card {
            font-family: 'Courier New', Consolas, Monaco, monospace;
            font-size: 18px;
            text-align: center;
            color: #ffffff;
            background-color: #000000;
            padding: 20px;
            line-height: 1.6;
        }

        .category-badge {
            display: inline-block;
            background: #ffffff;
            color: #000000;
            padding: 6px 14px;
            border-radius: 0px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 20px;
            border: 2px solid #ffffff;
        }

        .question {
            font-size: 24px;
            font-weight: 600;
            margin: 25px 0;
            color: #ffffff;
            text-align: left;
        }

        hr {
            border: none;
            border-top: 2px solid #ffffff;
            margin: 30px 0;
        }

        .answer {
            text-align: left;
            font-size: 17px;
            padding: 20px;
            background-color: #0a0a0a;
            border-radius: 0px;
            margin: 20px 0;
            border: 1px solid #ffffff;
        }

        .answer strong {
            color: #ffffff;
            font-weight: 700;
            text-decoration: underline;
        }

        .answer ul, .answer ol {
            margin: 15px 0;
            padding-left: 30px;
        }

        .answer li {
            margin: 10px 0;
        }

        .code-block {
            background-color: #0a0a0a;
            color: #ffffff;
            padding: 18px;
            border-radius: 0px;
            font-family: 'Courier New', Consolas, Monaco, monospace;
            font-size: 14px;
            text-align: left;
            overflow-x: auto;
            margin-top: 20px;
            white-space: pre-wrap;
            word-wrap: break-word;
            border: 2px solid #ffffff;
        }
    '''
)

# Create deck
deck = genanki.Deck(
    DECK_ID,
    'Assignment 3: CNNs for CIFAR-10 Image Classification'
)

# Card content
cards = [
    # ===== CNN FUNDAMENTALS =====
    {
        'question': 'What is a Convolutional Neural Network (CNN)?',
        'answer': '''<strong>A CNN is a specialized neural network designed for processing grid-like data, particularly images.</strong>
<br><br>
<strong>Key characteristics:</strong>
<ul>
<li><strong>Spatial hierarchy:</strong> Learns hierarchical patterns from low-level (edges) to high-level (objects)</li>
<li><strong>Parameter sharing:</strong> Same filters applied across entire image</li>
<li><strong>Translation invariance:</strong> Detects features regardless of position</li>
<li><strong>Sparse connectivity:</strong> Each neuron connects only to local region</li>
</ul>
<br>
<strong>Inspired by:</strong> Animal visual cortex''',
        'category': 'CNN Fundamentals',
        'code': ''
    },
    {
        'question': 'Why do CNNs NOT flatten the image at the input?',
        'answer': '''<strong>Flattening destroys spatial structure!</strong>
<br><br>
<strong>Problems with flattening:</strong>
<ul>
<li><strong>Loss of spatial relationships:</strong> Adjacent pixels treated same as distant pixels</li>
<li><strong>No translation invariance:</strong> Must learn same feature at every position</li>
<li><strong>Huge parameter count:</strong> 32×32×3 → 3,072 inputs × 1,024 hidden = 3.1M parameters!</li>
<li><strong>Poor generalization:</strong> Too many parameters cause overfitting</li>
</ul>
<br>
<strong>CNNs preserve structure:</strong> [batch, channels, height, width] throughout network''',
        'category': 'CNN Fundamentals',
        'code': '''# WRONG - Flattening at input
x = x.view(x.size(0), -1)  # Destroys spatial structure!

# CORRECT - Preserve spatial structure
x = self.conv1(x)  # [batch, 3, 32, 32] → [batch, 64, 32, 32]'''
    },
    {
        'question': 'What is convolution and how does it work?',
        'answer': '''<strong>Convolution slides a small filter (kernel) over the input to produce a feature map.</strong>
<br><br>
<strong>Mathematical operation:</strong>
Output[i,j] = Σ Σ Input[i+m, j+n] × Kernel[m,n]
<br><br>
<strong>Process:</strong>
<ul>
<li>Small filter (e.g., 3×3) slides across input</li>
<li>Element-wise multiplication at each position</li>
<li>Sum results to produce one output value</li>
<li>Slide to next position (determined by stride)</li>
</ul>
<br>
<strong>Key benefit:</strong> Same filter detects patterns anywhere in image''',
        'category': 'Convolutional Layers',
        'code': '''nn.Conv2d(
    in_channels=3,
    out_channels=64,
    kernel_size=3,
    stride=1,
    padding=1
)'''
    },
    {
        'question': 'What are the key parameters of a convolutional layer?',
        'answer': '''<strong>Four main parameters control convolution behavior:</strong>
<br><br>
<strong>1. Kernel size (k):</strong> Size of sliding window (e.g., 3×3, 5×5)
<br><br>
<strong>2. Stride (s):</strong> How many pixels to slide
<ul>
<li>stride=1: overlapping windows</li>
<li>stride=2: downsample by factor of 2</li>
</ul>
<br>
<strong>3. Padding (p):</strong> Add zeros around border
<ul>
<li>padding=1 with 3×3 kernel maintains spatial size</li>
</ul>
<br>
<strong>4. Number of filters (out_channels):</strong> How many feature maps to produce
<ul>
<li>Common: 32, 64, 128, 256</li>
</ul>''',
        'category': 'Convolutional Layers',
        'code': '''# Example: maintain spatial size
nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1)
# 32×32 input → 32×32 output

# Example: downsample
nn.Conv2d(64, 128, kernel_size=3, stride=2, padding=1)
# 32×32 input → 16×16 output'''
    },
    {
        'question': 'What is the formula for calculating output size after convolution?',
        'answer': '''<strong>Output size formula:</strong>
<br><br>
output_size = ⌊(input_size + 2×padding - kernel_size) / stride⌋ + 1
<br><br>
<strong>Example 1: Maintain size</strong>
<ul>
<li>Input: 32×32</li>
<li>Kernel: 3×3, Padding: 1, Stride: 1</li>
<li>Output: ⌊(32 + 2×1 - 3) / 1⌋ + 1 = 32×32</li>
</ul>
<br>
<strong>Example 2: Downsample</strong>
<ul>
<li>Input: 32×32</li>
<li>Kernel: 3×3, Padding: 1, Stride: 2</li>
<li>Output: ⌊(32 + 2×1 - 3) / 2⌋ + 1 = 16×16</li>
</ul>''',
        'category': 'Convolutional Layers',
        'code': ''
    },
    {
        'question': 'How do you calculate the number of parameters in a Conv2d layer?',
        'answer': '''<strong>Formula:</strong>
<br>
Parameters = (kernel_h × kernel_w × in_channels + 1) × out_channels
<br><br>
<strong>Components:</strong>
<ul>
<li><strong>Weights:</strong> kernel_h × kernel_w × in_channels per filter</li>
<li><strong>Bias:</strong> +1 per filter</li>
<li><strong>Total filters:</strong> × out_channels</li>
</ul>
<br>
<strong>Example:</strong> Conv2d(3, 64, kernel_size=3)
<br>
= (3 × 3 × 3 + 1) × 64 = 1,792 parameters
<br><br>
<strong>Compare to FC:</strong> 3,072 × 1,024 = 3,145,728 parameters!
<br>
<strong>CNN is 1,754× more efficient!</strong>''',
        'category': 'Convolutional Layers',
        'code': '''def count_parameters(layer):
    return sum(p.numel() for p in layer.parameters())

conv = nn.Conv2d(3, 64, 3)
print(count_parameters(conv))  # 1,792

fc = nn.Linear(3072, 1024)
print(count_parameters(fc))    # 3,146,752'''
    },

    # ===== POOLING =====
    {
        'question': 'What is the purpose of pooling layers?',
        'answer': '''<strong>Pooling reduces spatial dimensions while preserving important information.</strong>
<br><br>
<strong>Four main purposes:</strong>
<ol>
<li><strong>Reduce spatial dimensions:</strong> Decrease computational cost and memory</li>
<li><strong>Increase receptive field:</strong> Each neuron "sees" more of the input</li>
<li><strong>Add translation invariance:</strong> Small shifts don't change output</li>
<li><strong>Reduce overfitting:</strong> Fewer parameters in subsequent layers</li>
</ol>
<br>
<strong>Typical progression:</strong>
<ul>
<li>32×32 → MaxPool(2) → 16×16</li>
<li>16×16 → MaxPool(2) → 8×8</li>
<li>8×8 → MaxPool(2) → 4×4</li>
</ul>''',
        'category': 'Pooling',
        'code': '''nn.MaxPool2d(kernel_size=2, stride=2)'''
    },
    {
        'question': 'What is the difference between MaxPool and AvgPool?',
        'answer': '''<strong>MaxPool vs AvgPool:</strong>
<br><br>
<strong>MaxPool2d:</strong>
<ul>
<li><strong>Operation:</strong> Takes maximum value in each window</li>
<li><strong>Preserves:</strong> Strongest activations (sharp features)</li>
<li><strong>Use case:</strong> Feature detection (edges, patterns)</li>
<li><strong>Most common</strong> in modern CNNs</li>
</ul>
<br>
<strong>AvgPool2d:</strong>
<ul>
<li><strong>Operation:</strong> Takes average value in each window</li>
<li><strong>Preserves:</strong> Overall intensity</li>
<li><strong>Use case:</strong> Smooth downsampling</li>
<li><strong>Less common</strong> nowadays</li>
</ul>
<br>
<strong>Global Average Pooling (GAP):</strong> Reduces each feature map to single value, replaces flatten + FC''',
        'category': 'Pooling',
        'code': '''# MaxPool
nn.MaxPool2d(2)  # Most common

# AvgPool
nn.AvgPool2d(2)  # Less common

# Global Average Pooling
nn.AdaptiveAvgPool2d(1)  # Before classifier'''
    },

    # ===== ACTIVATION FUNCTIONS =====
    {
        'question': 'Why do we need activation functions in neural networks?',
        'answer': '''<strong>Activation functions introduce non-linearity.</strong>
<br><br>
<strong>Without activations:</strong>
<br>
Linear → Linear → Linear ≡ Single Linear Layer
<br><br>
<strong>Problem:</strong> Stacking layers is useless without non-linearity!
<br><br>
<strong>With activations:</strong>
<ul>
<li>Network can learn complex, non-linear patterns</li>
<li>Each layer adds expressiveness</li>
<li>Can approximate any function (universal approximation)</li>
</ul>
<br>
<strong>Most common in CNNs:</strong> ReLU (Rectified Linear Unit)''',
        'category': 'Activation Functions',
        'code': '''# Bad - no activations (useless!)
x = self.fc1(x)
x = self.fc2(x)
x = self.fc3(x)

# Good - with activations
x = F.relu(self.fc1(x))
x = F.relu(self.fc2(x))
x = self.fc3(x)'''
    },
    {
        'question': 'What is ReLU and why is it used in CNNs?',
        'answer': '''<strong>ReLU (Rectified Linear Unit):</strong> ReLU(x) = max(0, x)
<br><br>
<strong>Advantages:</strong>
<ul>
<li><strong>Fast to compute:</strong> Simple max operation</li>
<li><strong>Helps with vanishing gradients:</strong> Gradient is 0 or 1</li>
<li><strong>Sparse activations:</strong> Many zeros, efficient representation</li>
<li><strong>Works well in practice:</strong> Default choice for CNNs</li>
</ul>
<br>
<strong>Disadvantages:</strong>
<ul>
<li><strong>"Dying ReLU":</strong> Neurons can get stuck at 0 forever</li>
<li><strong>Not zero-centered:</strong> All outputs ≥ 0</li>
</ul>
<br>
<strong>Variants:</strong> Leaky ReLU, PReLU, ELU (prevent dying neurons)''',
        'category': 'Activation Functions',
        'code': '''nn.ReLU(inplace=True)

# Typical usage in CNN
nn.Conv2d(64, 128, 3, padding=1),
nn.BatchNorm2d(128),
nn.ReLU(inplace=True),  # After BatchNorm'''
    },

    # ===== NORMALIZATION =====
    {
        'question': 'What is Batch Normalization and why is it important?',
        'answer': '''<strong>BatchNorm normalizes layer inputs to have mean=0, std=1.</strong>
<br><br>
<strong>Formula:</strong>
<br>
BatchNorm(x) = γ × (x - μ_batch) / √(σ²_batch + ε) + β
<br><br>
<strong>Where:</strong>
<ul>
<li>μ_batch, σ²_batch: mean and variance of current batch</li>
<li>γ, β: learned scale and shift parameters</li>
</ul>
<br>
<strong>Benefits:</strong>
<ul>
<li><strong>Faster convergence:</strong> Stabilized training dynamics</li>
<li><strong>Higher learning rates:</strong> Can train with larger LR</li>
<li><strong>Less sensitive to initialization</strong></li>
<li><strong>Acts as regularization</strong> (reduces overfitting)</li>
</ul>''',
        'category': 'Normalization',
        'code': '''# Typical ordering: Conv → BatchNorm → ReLU
nn.Conv2d(64, 128, 3, padding=1),
nn.BatchNorm2d(128),
nn.ReLU(inplace=True)'''
    },
    {
        'question': 'How does BatchNorm behave differently during training vs inference?',
        'answer': '''<strong>Training mode vs Evaluation mode:</strong>
<br><br>
<strong>During Training (model.train()):</strong>
<ul>
<li>Computes mean and variance from <strong>current batch</strong></li>
<li>Updates running statistics (exponential moving average)</li>
<li>Normalizes using batch statistics</li>
</ul>
<br>
<strong>During Inference (model.eval()):</strong>
<ul>
<li>Uses <strong>running statistics</strong> computed during training</li>
<li>No batch statistics (might have batch_size=1!)</li>
<li>Deterministic output</li>
</ul>
<br>
<strong>CRITICAL:</strong> Always call model.eval() before evaluation/testing!''',
        'category': 'Normalization',
        'code': '''# Training
model.train()
for inputs, targets in train_loader:
    outputs = model(inputs)  # Uses batch stats

# Evaluation
model.eval()  # IMPORTANT!
with torch.no_grad():
    for inputs, targets in test_loader:
        outputs = model(inputs)  # Uses running stats'''
    },

    # ===== REGULARIZATION =====
    {
        'question': 'What is Dropout and how does it prevent overfitting?',
        'answer': '''<strong>Dropout randomly drops (sets to 0) activations during training.</strong>
<br><br>
<strong>Mechanism:</strong>
<ul>
<li><strong>Training:</strong> Randomly set activations to 0 with probability p</li>
<li><strong>Inference:</strong> Use all activations, scaled by (1-p)</li>
</ul>
<br>
<strong>Why it works:</strong>
<ul>
<li><strong>Forces redundancy:</strong> Can't rely on single neuron</li>
<li><strong>Ensemble effect:</strong> Training many sub-networks</li>
<li><strong>Prevents co-adaptation:</strong> Neurons learn independent features</li>
</ul>
<br>
<strong>Typical values:</strong>
<ul>
<li>0.5 in fully connected layers (aggressive)</li>
<li>0.2-0.3 after convolutional layers (mild)</li>
</ul>''',
        'category': 'Regularization',
        'code': '''# Higher dropout in FC layers
nn.Dropout(0.5),
nn.Linear(256, 128),

# Lower dropout after conv layers
nn.Dropout2d(0.25),  # Drops entire feature maps
nn.Conv2d(64, 128, 3)'''
    },
    {
        'question': 'What is weight decay (L2 regularization)?',
        'answer': '''<strong>Weight decay penalizes large weights to encourage simpler models.</strong>
<br><br>
<strong>Formula:</strong>
<br>
Loss_total = Loss_original + λ × Σ(w²)
<br><br>
<strong>Effect:</strong>
<ul>
<li>Pushes weights toward zero</li>
<li>Prevents any single weight from becoming too large</li>
<li>Encourages distributed representations</li>
<li>Reduces overfitting</li>
</ul>
<br>
<strong>Typical values:</strong>
<ul>
<li>λ = 5e-4 (0.0005) - common default</li>
<li>Range: 1e-4 to 1e-3</li>
</ul>''',
        'category': 'Regularization',
        'code': '''optimizer = optim.AdamW(
    model.parameters(),
    lr=1e-3,
    weight_decay=5e-4  # L2 regularization
)'''
    },

    # ===== DATA AUGMENTATION =====
    {
        'question': 'What is data augmentation and why is it important?',
        'answer': '''<strong>Data augmentation creates variations of training data to improve generalization.</strong>
<br><br>
<strong>Benefits:</strong>
<ul>
<li><strong>Increases effective dataset size:</strong> More training examples</li>
<li><strong>Improves generalization:</strong> Model learns invariances</li>
<li><strong>Reduces overfitting:</strong> More diverse examples</li>
<li><strong>Better calibration:</strong> More robust predictions</li>
</ul>
<br>
<strong>For CIFAR-10, typically gain:</strong>
<ul>
<li>Basic augmentation (crop + flip): +2-5% accuracy</li>
<li>With color jitter: +1-2% additional</li>
<li>With random erasing: +0.5-1% additional</li>
</ul>
<br>
<strong>Total improvement:</strong> +5-10% accuracy possible!''',
        'category': 'Data Augmentation',
        'code': ''
    },
    {
        'question': 'What are the common data augmentations for CIFAR-10?',
        'answer': '''<strong>Four recommended augmentations for CIFAR-10:</strong>
<br><br>
<strong>1. RandomCrop(32, padding=4)</strong>
<ul>
<li>Pads to 36×36, then random crops to 32×32</li>
<li>Effect: Translation invariance</li>
</ul>
<br>
<strong>2. RandomHorizontalFlip()</strong>
<ul>
<li>50% chance to flip left-right</li>
<li>Effect: Mirror symmetry (car facing left = car facing right)</li>
</ul>
<br>
<strong>3. ColorJitter(0.2, 0.2, 0.2, 0.1)</strong>
<ul>
<li>Varies brightness, contrast, saturation, hue</li>
<li>Effect: Robustness to lighting conditions</li>
</ul>
<br>
<strong>4. RandomErasing(p=0.15)</strong>
<ul>
<li>Randomly masks rectangular regions</li>
<li>Effect: Occlusion robustness, prevents single-feature reliance</li>
</ul>''',
        'category': 'Data Augmentation',
        'code': '''train_transform = transforms.Compose([
    transforms.RandomCrop(32, padding=4),
    transforms.RandomHorizontalFlip(),
    transforms.ColorJitter(0.2, 0.2, 0.2, 0.1),
    transforms.ToTensor(),
    transforms.Normalize(mean, std),
    transforms.RandomErasing(p=0.15),
])'''
    },
    {
        'question': 'Should you augment the test set? Why or why not?',
        'answer': '''<strong>NO! NEVER augment the test set.</strong>
<br><br>
<strong>Reasons:</strong>
<ul>
<li><strong>Fair evaluation:</strong> Test should reflect real-world clean images</li>
<li><strong>Consistency:</strong> Everyone evaluates on same data</li>
<li><strong>Reproducibility:</strong> Random augmentations give different results each run</li>
<li><strong>Meaningful metrics:</strong> Want true performance, not boosted numbers</li>
</ul>
<br>
<strong>Test transform should only include:</strong>
<ul>
<li>ToTensor() - convert to tensor</li>
<li>Normalize() - same normalization as training</li>
</ul>
<br>
<strong>Training = augment heavily</strong>
<br>
<strong>Testing = clean data only</strong>''',
        'category': 'Data Augmentation',
        'code': '''# WRONG - augmenting test set
test_transform = transforms.Compose([
    transforms.RandomCrop(32, padding=4),  # NO!
    transforms.ToTensor(),
])

# CORRECT - clean test data
test_transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean, std),
])'''
    },

    # ===== TRAINING =====
    {
        'question': 'What loss function should you use for multi-class classification?',
        'answer': '''<strong>CrossEntropyLoss is the standard for multi-class classification.</strong>
<br><br>
<strong>What it does:</strong>
<ul>
<li>Combines LogSoftmax + Negative Log Likelihood</li>
<li>Expects raw logits (before softmax)</li>
<li>Outputs probability distribution via softmax</li>
<li>Penalizes wrong predictions more heavily</li>
</ul>
<br>
<strong>Formula:</strong>
<br>
Loss = -log(softmax(logits)[target_class])
<br><br>
<strong>With label smoothing (recommended):</strong>
<ul>
<li>Prevents overconfident predictions</li>
<li>Better calibration</li>
<li>Acts as regularization</li>
</ul>''',
        'category': 'Training',
        'code': '''# Basic
criterion = nn.CrossEntropyLoss()

# With label smoothing (better)
criterion = nn.CrossEntropyLoss(label_smoothing=0.05)

# Usage
loss = criterion(outputs, targets)
# outputs: raw logits [batch, 10]
# targets: class indices [batch]'''
    },
    {
        'question': 'Adam vs SGD: which optimizer should you use for CNNs?',
        'answer': '''<strong>Both have trade-offs. Choose based on your goals:</strong>
<br><br>
<strong>Adam / AdamW:</strong>
<ul>
<li><strong>Pros:</strong> Fast convergence, adaptive LR per parameter, works out-of-the-box</li>
<li><strong>Cons:</strong> Can generalize slightly worse than SGD</li>
<li><strong>Use when:</strong> Quick experiments, prototyping, limited tuning time</li>
<li><strong>LR:</strong> 1e-4 to 1e-3</li>
</ul>
<br>
<strong>SGD + Momentum:</strong>
<ul>
<li><strong>Pros:</strong> Better generalization, proven track record</li>
<li><strong>Cons:</strong> Requires careful LR tuning, slower convergence</li>
<li><strong>Use when:</strong> Final production model, have time to tune</li>
<li><strong>LR:</strong> 0.01 to 0.1</li>
</ul>
<br>
<strong>For Assignment 3:</strong> AdamW is recommended''',
        'category': 'Training',
        'code': '''# AdamW (recommended for A3)
optimizer = optim.AdamW(
    model.parameters(),
    lr=2e-3,
    weight_decay=5e-4
)

# SGD + Momentum (for production)
optimizer = optim.SGD(
    model.parameters(),
    lr=0.1,
    momentum=0.9,
    weight_decay=5e-4,
    nesterov=True
)'''
    },
    {
        'question': 'What are learning rate schedules and why use them?',
        'answer': '''<strong>LR schedules decrease learning rate during training for better convergence.</strong>
<br><br>
<strong>Why use schedules:</strong>
<ul>
<li><strong>Early training:</strong> High LR for fast exploration</li>
<li><strong>Late training:</strong> Low LR for fine-tuning</li>
<li><strong>Better final accuracy:</strong> Typically +1-2%</li>
</ul>
<br>
<strong>Three common schedules:</strong>
<br><br>
<strong>1. CosineAnnealingLR:</strong> Smooth cosine decrease
<br>
<strong>2. StepLR:</strong> Decrease by factor every N epochs
<br>
<strong>3. ReduceLROnPlateau:</strong> Decrease when validation stops improving
<br><br>
<strong>For Assignment 3:</strong> CosineAnnealing recommended''',
        'category': 'Training',
        'code': '''# Cosine (recommended)
scheduler = optim.lr_scheduler.CosineAnnealingLR(
    optimizer, T_max=50, eta_min=1e-6
)

# Step
scheduler = optim.lr_scheduler.StepLR(
    optimizer, step_size=30, gamma=0.1
)

# Adaptive
scheduler = optim.lr_scheduler.ReduceLROnPlateau(
    optimizer, mode='min', factor=0.5, patience=5
)

# Update after each epoch
scheduler.step()'''
    },
    {
        'question': 'What is gradient clipping and when should you use it?',
        'answer': '''<strong>Gradient clipping limits the magnitude of gradients to prevent instability.</strong>
<br><br>
<strong>How it works:</strong>
<ul>
<li>Compute gradient norm: ||g|| = √(Σ g_i²)</li>
<li>If ||g|| > threshold, scale down: g ← g × (threshold / ||g||)</li>
</ul>
<br>
<strong>When to use:</strong>
<ul>
<li>Training with high learning rates</li>
<li>When loss occasionally spikes to NaN</li>
<li>Recurrent networks (RNNs/LSTMs)</li>
<li>Very deep networks</li>
</ul>
<br>
<strong>Typical threshold:</strong> 0.5 to 2.0
<br><br>
<strong>For Assignment 3:</strong> Use max_norm=1.0''',
        'category': 'Training',
        'code': '''loss.backward()

# Clip gradients
torch.nn.utils.clip_grad_norm_(
    model.parameters(),
    max_norm=1.0
)

optimizer.step()'''
    },

    # ===== CIFAR-10 DATASET =====
    {
        'question': 'What are the key statistics of the CIFAR-10 dataset?',
        'answer': '''<strong>CIFAR-10 dataset statistics:</strong>
<br><br>
<strong>Size:</strong>
<ul>
<li>60,000 total images</li>
<li>50,000 training images</li>
<li>10,000 test images</li>
</ul>
<br>
<strong>Format:</strong>
<ul>
<li>32×32 pixels</li>
<li>3 channels (RGB)</li>
<li>10 balanced classes (6,000 each)</li>
</ul>
<br>
<strong>Classes:</strong>
<br>
airplane, automobile, bird, cat, deer, dog, frog, horse, ship, truck
<br><br>
<strong>Normalization values:</strong>
<br>
mean = (0.4914, 0.4822, 0.4465)
<br>
std = (0.2470, 0.2435, 0.2616)''',
        'category': 'CIFAR-10',
        'code': '''from torchvision import datasets

train_dataset = datasets.CIFAR10(
    root='./data',
    train=True,
    download=True,
    transform=train_transform
)

test_dataset = datasets.CIFAR10(
    root='./data',
    train=False,
    download=True,
    transform=test_transform
)'''
    },
    {
        'question': 'How should you split CIFAR-10 for training?',
        'answer': '''<strong>Standard split for Assignment 3:</strong>
<br><br>
<strong>Recommended:</strong>
<ul>
<li>45,000 training images (90% of train set)</li>
<li>5,000 validation images (10% of train set)</li>
<li>10,000 test images (official test set)</li>
</ul>
<br>
<strong>Why use validation set:</strong>
<ul>
<li>Monitor overfitting during training</li>
<li>Early stopping based on val accuracy</li>
<li>Save best model based on val performance</li>
<li>Tune hyperparameters</li>
</ul>
<br>
<strong>NEVER tune on test set!</strong> Use only for final evaluation.''',
        'category': 'CIFAR-10',
        'code': '''# Create validation split
val_size = 5000
indices = torch.randperm(len(train_dataset))
train_indices = indices[val_size:].tolist()  # 45,000
val_indices = indices[:val_size].tolist()    # 5,000

train_subset = Subset(train_dataset, train_indices)
val_subset = Subset(train_dataset, val_indices)'''
    },
    {
        'question': 'Why do we normalize CIFAR-10 images?',
        'answer': '''<strong>Normalization centers pixel values and standardizes scale.</strong>
<br><br>
<strong>Formula:</strong>
<br>
normalized = (x - mean) / std
<br><br>
<strong>Benefits:</strong>
<ul>
<li><strong>Zero-centered inputs:</strong> Speeds up convergence</li>
<li><strong>Prevents saturation:</strong> Activations stay in good range</li>
<li><strong>Consistent scale:</strong> All channels have similar importance</li>
<li><strong>Better gradients:</strong> More stable training</li>
</ul>
<br>
<strong>CIFAR-10 statistics:</strong>
<br>
Computed from all 50,000 training images
<br><br>
<strong>CRITICAL:</strong> Use same normalization for train AND test!''',
        'category': 'CIFAR-10',
        'code': '''# CIFAR-10 statistics
mean = (0.4914, 0.4822, 0.4465)
std = (0.2470, 0.2435, 0.2616)

normalize = transforms.Normalize(mean=mean, std=std)

# Apply to both train and test
train_transform = transforms.Compose([
    transforms.RandomCrop(32, padding=4),
    transforms.ToTensor(),
    normalize,  # Same normalization
])

test_transform = transforms.Compose([
    transforms.ToTensor(),
    normalize,  # Same normalization
])'''
    },

    # ===== EVALUATION =====
    {
        'question': 'What metrics should you track during CNN training?',
        'answer': '''<strong>Track both training and validation metrics:</strong>
<br><br>
<strong>Essential metrics:</strong>
<ol>
<li><strong>Training loss:</strong> Are we learning?</li>
<li><strong>Training accuracy:</strong> Performance on train set</li>
<li><strong>Validation loss:</strong> Generalization indicator</li>
<li><strong>Validation accuracy:</strong> True performance metric</li>
</ol>
<br>
<strong>Watch for patterns:</strong>
<ul>
<li><strong>Train loss ↓, Val loss ↓:</strong> Good! Keep training</li>
<li><strong>Train loss ↓, Val loss ↑:</strong> Overfitting! Add regularization</li>
<li><strong>Both high:</strong> Underfitting! Increase capacity or train longer</li>
</ul>
<br>
<strong>Additional metrics:</strong>
<ul>
<li>Learning rate (if using scheduler)</li>
<li>Time per epoch</li>
<li>Best epoch / best validation accuracy</li>
</ul>''',
        'category': 'Evaluation',
        'code': '''history = []
for epoch in range(num_epochs):
    train_loss, train_acc = train_epoch(...)
    val_loss, val_acc = evaluate(...)

    history.append({
        'epoch': epoch,
        'train_loss': train_loss,
        'train_acc': train_acc,
        'val_loss': val_loss,
        'val_acc': val_acc,
        'lr': optimizer.param_groups[0]['lr']
    })'''
    },
    {
        'question': 'How do you properly evaluate a model on the test set?',
        'answer': '''<strong>Proper evaluation procedure:</strong>
<br><br>
<strong>Steps:</strong>
<ol>
<li><strong>Set to eval mode:</strong> model.eval()</li>
<li><strong>Disable gradients:</strong> with torch.no_grad()</li>
<li><strong>Use test transform:</strong> No augmentation!</li>
<li><strong>Track predictions:</strong> Compute metrics</li>
</ol>
<br>
<strong>Why model.eval() is critical:</strong>
<ul>
<li>Switches BatchNorm to use running statistics</li>
<li>Disables Dropout (use all neurons)</li>
<li>Deterministic behavior</li>
</ul>
<br>
<strong>Why torch.no_grad() is important:</strong>
<ul>
<li>Saves memory (no gradient computation)</li>
<li>Faster evaluation</li>
<li>Prevents accidental gradient updates</li>
</ul>''',
        'category': 'Evaluation',
        'code': '''def evaluate(model, dataloader, criterion, device):
    model.eval()  # CRITICAL!
    running_loss = 0.0
    correct = 0
    total = 0

    with torch.no_grad():  # CRITICAL!
        for inputs, targets in dataloader:
            inputs = inputs.to(device)
            targets = targets.to(device)

            outputs = model(inputs)
            loss = criterion(outputs, targets)

            running_loss += loss.item() * inputs.size(0)
            predictions = outputs.argmax(dim=1)
            correct += (predictions == targets).sum().item()
            total += targets.size(0)

    return running_loss / total, correct / total'''
    },

    # ===== CNN vs FC =====
    {
        'question': 'Why do CNNs outperform fully connected networks on images?',
        'answer': '''<strong>CNNs have inductive biases that match image structure.</strong>
<br><br>
<strong>1. Spatial structure preservation:</strong>
<ul>
<li>FC: Flattens to [batch, 3072] - destroys spatial relationships</li>
<li>CNN: Keeps [batch, C, H, W] - preserves adjacency</li>
</ul>
<br>
<strong>2. Parameter efficiency:</strong>
<ul>
<li>FC first layer: 3,145,728 parameters</li>
<li>CNN first layer: 1,792 parameters</li>
<li><strong>1,754× fewer parameters!</strong></li>
</ul>
<br>
<strong>3. Translation invariance:</strong>
<ul>
<li>FC: Must learn cat at every position separately</li>
<li>CNN: Same filter detects cat anywhere</li>
</ul>
<br>
<strong>4. Hierarchical learning:</strong>
<ul>
<li>Layer 1: Edges → Layer 2: Shapes → Layer 3: Objects</li>
</ul>''',
        'category': 'CNN vs FC',
        'code': '''# FC Network
class FC_Net(nn.Module):
    def forward(self, x):
        x = x.view(x.size(0), -1)  # Flatten!
        x = F.relu(self.fc1(x))    # 3M parameters
        ...

# CNN
class CNN(nn.Module):
    def forward(self, x):
        # x: [batch, 3, 32, 32] - preserved!
        x = self.conv1(x)  # Only 1.7k parameters
        ...'''
    },
    {
        'question': 'What are typical accuracy results on CIFAR-10?',
        'answer': '''<strong>Expected test accuracy by model type:</strong>
<br><br>
<table border="1" style="border-collapse: collapse; width: 100%;">
<tr style="background: #1a1a1a;">
<th>Model</th>
<th>Test Accuracy</th>
</tr>
<tr>
<td>Random guessing</td>
<td>10%</td>
</tr>
<tr>
<td>3-layer FC network</td>
<td>55-60%</td>
</tr>
<tr>
<td>Simple CNN (no augmentation)</td>
<td>70-75%</td>
</tr>
<tr>
<td>CNN + basic augmentation</td>
<td>80-85%</td>
</tr>
<tr>
<td>CNN + full augmentation</td>
<td>85-90%</td>
</tr>
<tr>
<td>ResNet-18</td>
<td>92-95%</td>
</tr>
<tr>
<td>State-of-the-art</td>
<td>99%+</td>
</tr>
</table>
<br>
<strong>For Assignment 3:</strong> Target 80-85%+ for strong grade''',
        'category': 'CNN vs FC',
        'code': ''
    },

    # ===== ARCHITECTURE =====
    {
        'question': 'What is a typical CNN architecture for CIFAR-10?',
        'answer': '''<strong>Standard pattern: [Conv-BN-ReLU-Pool] blocks → GAP → FC</strong>
<br><br>
<strong>Example architecture:</strong>
<ul>
<li><strong>Block 1:</strong> 3→64 Conv, BN, ReLU, MaxPool → 32×32 to 16×16</li>
<li><strong>Block 2:</strong> 64→128 Conv, BN, ReLU, MaxPool → 16×16 to 8×8</li>
<li><strong>Block 3:</strong> 128→256 Conv, BN, ReLU, AdaptiveAvgPool → 8×8 to 1×1</li>
<li><strong>Classifier:</strong> Flatten, Dropout, FC(256→128), ReLU, FC(128→10)</li>
</ul>
<br>
<strong>Key principles:</strong>
<ul>
<li>Increasing channels: 3 → 64 → 128 → 256</li>
<li>Decreasing spatial size: 32 → 16 → 8 → 1</li>
<li>BN after Conv, before ReLU</li>
<li>Dropout for regularization</li>
</ul>''',
        'category': 'Architecture',
        'code': '''self.features = nn.Sequential(
    # Block 1
    nn.Conv2d(3, 64, 3, padding=1),
    nn.BatchNorm2d(64),
    nn.ReLU(inplace=True),
    nn.MaxPool2d(2),

    # Block 2
    nn.Conv2d(64, 128, 3, padding=1),
    nn.BatchNorm2d(128),
    nn.ReLU(inplace=True),
    nn.MaxPool2d(2),

    # Block 3
    nn.Conv2d(128, 256, 3, padding=1),
    nn.BatchNorm2d(256),
    nn.ReLU(inplace=True),
    nn.AdaptiveAvgPool2d(1),
)'''
    },
    {
        'question': 'What is the correct order of Conv-BatchNorm-ReLU?',
        'answer': '''<strong>Correct order: Conv → BatchNorm → ReLU</strong>
<br><br>
<strong>Why this order:</strong>
<ul>
<li><strong>Conv:</strong> Linear transformation</li>
<li><strong>BatchNorm:</strong> Normalize before activation (stabilizes)</li>
<li><strong>ReLU:</strong> Non-linearity after normalization</li>
</ul>
<br>
<strong>Wrong orders and why:</strong>
<ul>
<li><strong>BN → Conv → ReLU:</strong> BN expects output of Conv, not input</li>
<li><strong>Conv → ReLU → BN:</strong> ReLU zeroes negative values, reducing BN effectiveness</li>
<li><strong>ReLU → Conv → BN:</strong> Completely wrong, doesn't make sense</li>
</ul>
<br>
<strong>Remember:</strong> Process data, normalize, activate!''',
        'category': 'Architecture',
        'code': '''# CORRECT
nn.Conv2d(64, 128, 3, padding=1),
nn.BatchNorm2d(128),
nn.ReLU(inplace=True),

# WRONG
nn.BatchNorm2d(64),
nn.Conv2d(64, 128, 3, padding=1),  # NO!
nn.ReLU(inplace=True),'''
    },

    # ===== COMMON PITFALLS =====
    {
        'question': 'What are the most common mistakes when implementing CNNs?',
        'answer': '''<strong>Top 10 pitfalls to avoid:</strong>
<br><br>
<strong>1. Flattening at input</strong> - Destroys spatial structure
<br>
<strong>2. Augmenting test set</strong> - Unfair evaluation
<br>
<strong>3. Not calling model.eval()</strong> - BatchNorm/Dropout wrong mode
<br>
<strong>4. Wrong BatchNorm placement</strong> - Should be Conv→BN→ReLU
<br>
<strong>5. LR too high</strong> - Loss explodes to NaN
<br>
<strong>6. Not saving best model</strong> - Last epoch might not be best
<br>
<strong>7. Forgetting to normalize inputs</strong> - Slow/unstable training
<br>
<strong>8. Not setting seeds</strong> - Results not reproducible
<br>
<strong>9. Using same normalization for train/test</strong> - Must match!
<br>
<strong>10. Training too long without validation</strong> - Overfitting''',
        'category': 'Common Pitfalls',
        'code': ''
    },
    {
        'question': 'How do you fix training when loss becomes NaN?',
        'answer': '''<strong>Loss = NaN usually means gradients exploded.</strong>
<br><br>
<strong>Solutions to try (in order):</strong>
<br><br>
<strong>1. Lower learning rate:</strong>
<ul>
<li>Try 10× smaller (e.g., 1e-3 → 1e-4)</li>
</ul>
<br>
<strong>2. Add gradient clipping:</strong>
<ul>
<li>torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)</li>
</ul>
<br>
<strong>3. Check data normalization:</strong>
<ul>
<li>Ensure inputs are normalized to [-1, 1] or [0, 1]</li>
</ul>
<br>
<strong>4. Verify no bugs:</strong>
<ul>
<li>Check for division by zero</li>
<li>Ensure targets are in correct range [0, num_classes)</li>
<li>Check model initialization</li>
</ul>''',
        'category': 'Common Pitfalls',
        'code': '''# Solution 1: Lower LR
optimizer = optim.AdamW(
    model.parameters(),
    lr=1e-4,  # Instead of 1e-3
    weight_decay=5e-4
)

# Solution 2: Gradient clipping
loss.backward()
torch.nn.utils.clip_grad_norm_(
    model.parameters(),
    max_norm=1.0
)
optimizer.step()'''
    },

    # ===== REPRODUCIBILITY =====
    {
        'question': 'How do you ensure reproducible results in PyTorch?',
        'answer': '''<strong>Set ALL random seeds at start of training.</strong>
<br><br>
<strong>Must set seeds for:</strong>
<ol>
<li><strong>Python random:</strong> random.seed()</li>
<li><strong>NumPy:</strong> np.random.seed()</li>
<li><strong>PyTorch CPU:</strong> torch.manual_seed()</li>
<li><strong>PyTorch CUDA:</strong> torch.cuda.manual_seed_all()</li>
<li><strong>cuDNN:</strong> deterministic=True, benchmark=False</li>
</ol>
<br>
<strong>For Assignment 3:</strong> Use seed=328
<br><br>
<strong>Additional tips:</strong>
<ul>
<li>Document PyTorch version</li>
<li>Save model architecture code</li>
<li>Record hyperparameters</li>
<li>Use same hardware when possible</li>
</ul>''',
        'category': 'Reproducibility',
        'code': '''def set_seed(seed=328):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False

set_seed(328)'''
    },
]

# Add all cards to deck
for card_data in cards:
    note = genanki.Note(
        model=model,
        fields=[
            card_data['question'],
            card_data['answer'],
            card_data['category'],
            card_data.get('code', '')
        ]
    )
    deck.add_note(note)

# Generate the deck
output_file = 'CNN_CIFAR10_Image_Classification.apkg'
genanki.Package(deck).write_to_file(output_file)

print(f"Successfully generated Anki deck: {output_file}")
print(f"Total cards: {len(cards)}")
print("\nCards by category:")
categories = {}
for card in cards:
    cat = card['category']
    categories[cat] = categories.get(cat, 0) + 1

for cat, count in sorted(categories.items()):
    print(f"  {cat}: {count} cards")
