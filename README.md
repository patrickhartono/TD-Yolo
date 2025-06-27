# 🧠 YOLO Object Detection for TouchDesigner

A high-performance YOLO v11 implementation for TouchDesigner with automatic hardware acceleration support for Apple Silicon (MPS) and NVIDIA GPUs (CUDA).

> ⚠️ **Note**:
> ✅ **Supported platforms**: macOS (M1/M2/M3/M4) and Windows (NVIDIA GPU only)
> 🧪 **Tested with**: TouchDesigner **Experimental 2025.30060** only
> 🔗 Download here: [https://derivative.ca/download/experimental](https://derivative.ca/download/experimental)

## ✨ Features

* 💻 **macOS & Windows Support**: Fully optimized for Apple Silicon and NVIDIA GPUs
* ⚙️ **Automatic Hardware Detection**: Chooses the best available backend (MPS or CUDA)
* 🚀 **Real-time Performance**: Designed for live video analysis with frame skipping
* 🎯 **Class Filtering**: Detect specific classes or run full detection
* 🎛️ **TouchDesigner Integration**: Exposes YOLO as native parameters
* 🧠 **Efficient Memory Use**: Optimized for real-time stability

## ⚡ Hardware Acceleration

| 🖥️ Platform              | ⚙️ Acceleration                 | 🚀 Performance      | 📊 Tested         |
| ------------------------- | ------------------------------- | ------------------- | ----------------- |
| **macOS (Apple Silicon)** | Metal Performance Shaders (MPS) | 60–120+ FPS         | ✅ M4 Pro: 115 FPS |
| **Windows (NVIDIA GPU)**  | CUDA                            | 60+ FPS             | 🧪 Expected       |
| **CPU fallback (any)**    | Not supported (not recommended) | 15–30 FPS (limited) | ⚠️ Limited        |

## 📋 Requirements

* 🖥️ TouchDesigner Experimental 2025.30060
* 🐍 Python 3.11.10
* 📦 Conda or Miniconda

> 🚀 **Want to get started quickly?** See [QUICKSTART.md](QUICKSTART.md) for a 5-minute setup guide!

## ⚙️ Installation

### 1️⃣ Download Repository

```bash
# Option A: Git clone (if you have git)
git clone https://github.com/patrickhartono/TD-Yolo.git
cd TD-Yolo

# Option B: Download ZIP file
# Download from GitHub and extract to a folder
# Then navigate to the folder in terminal
cd /path/to/TD-Yolo
```

### 2️⃣ Create Python Environment

**Option A: Using Conda (recommended)**
```bash
conda env create -f environment_optimized.yml
conda activate yolo11-TD
```

**Option B: Using pip + venv**
```bash
# Create virtual environment
python -m venv yolo11-TD
source yolo11-TD/bin/activate  # macOS/Linux
# yolo11-TD\Scripts\activate     # Windows

# Install requirements
pip install -r requirements.txt
```

**Option C: Manual conda setup (if environment.yml fails)**
```bash
# Create new environment
conda create -n yolo11-TD python=3.11.10 -y
conda activate yolo11-TD

# Install PyTorch with hardware acceleration
# For macOS (Apple Silicon)
conda install pytorch torchvision torchaudio -c pytorch -y

# For Windows (NVIDIA GPU)
conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia -y

# Install other dependencies
conda install opencv numpy -c conda-forge -y
pip install ultralytics>=8.0.0
```

### 3️⃣ Verify Installation

```bash
# ✅ Quick verification script (recommended)
python verify_setup.py

# ✅ Performance test (optional)
python test_yolo_standalone.py

# ✅ Manual checks (optional)
python -c "import torch; print(f'MPS Available: {torch.backends.mps.is_available()}')"  # macOS
python -c "import torch; print(f'CUDA Available: {torch.cuda.is_available()}')"        # Windows
python -c "from ultralytics import YOLO; print('YOLO installation successful')"
```

## 📦 YOLO Model Auto-Download

> 🚀 **Automatic Setup**: YOLO models are downloaded automatically on first use
> 
> * 📁 **Model files**: `yolo11n.pt` (~6MB), `yolov8s-world.pt` (~40MB)
> * ⬇️ **Auto-download**: Happens automatically when script runs for the first time
> * 🏠 **Storage location**: Downloaded to Ultralytics cache directory (`~/.ultralytics/`)
> * 🚫 **Not in repository**: Model files are not included in this repository to keep it lightweight
> * ⏱️ **First run**: May take 10-60 seconds for initial model download (depends on internet speed)
> * 🌐 **No manual download needed**: Ultralytics handles everything automatically

### ✅ What happens on first run:
```
[YOLO] Downloading yolo11n.pt...
[YOLO] Model downloaded successfully
[YOLO] Using Metal Performance Shaders (MPS) for M4 Pro optimization
```

## 🎮 TouchDesigner Setup (Streamlined Version)

1. 🗂️ **Open the Project File**

   - Open the provided `.toe` file included in this repository (with `.td` format support for TouchDesigner 2025.30060)
   - This project is pre-configured to work with the `td.py` script using `manager21`

2. 🔌 **Automatic Webcam Connection**

   - No manual video input setup required
   - The project will automatically connect to your webcam on launch

3. 🎛️ **Configure Parameters (Optional)**

   The custom **YOLO** parameter page includes:

   - ✅ **Draw Bounding Box** – Toggle object detection overlays
   - 🧠 **Detection Classes** – Specify target objects (e.g., `"person,car,bicycle"`)
   - 🎯 **Confidence Threshold** – Adjust detection confidence (range: `0.0–1.0`)
   - ⏩ **Frame Skip** – Set number of frames to skip for better performance (`0 = all frames`)


## 🛠️ Usage Examples

### 🔍 Basic Object Detection

* Leave "Detection Classes" empty to detect all objects
* Set "Confidence Threshold" to 0.25 for balanced accuracy/performance
* Set "Frame Skip" to 0 for maximum quality

### 🚀 Performance Optimization

* Set "Frame Skip" to 2–5 for better performance on slower hardware
* Increase "Confidence Threshold" to 0.5+ to reduce false positives
* Disable "Draw Bounding Box" if you only need detection data

### 🎯 Specific Object Detection

Enter class names in "Detection Classes":

* `person` - Detect only people
* `person,car,bicycle` - Detect people, cars, and bicycles
* `bottle,cup,bowl` - Detect tableware objects

### 📚 Available YOLO Classes

Supports all 80 COCO dataset classes:

```
person, bicycle, car, motorcycle, airplane, bus, train, truck, boat, traffic light,
fire hydrant, stop sign, parking meter, bench, bird, cat, dog, horse, sheep, cow,
elephant, bear, zebra, giraffe, backpack, umbrella, handbag, tie, suitcase, frisbee,
skis, snowboard, sports ball, kite, baseball bat, baseball glove, skateboard, surfboard,
tennis racket, bottle, wine glass, cup, fork, knife, spoon, bowl, banana, apple,
sandwich, orange, broccoli, carrot, hot dog, pizza, donut, cake, chair, couch,
potted plant, bed, dining table, toilet, tv, laptop, mouse, remote, keyboard,
cell phone, microwave, oven, toaster, sink, refrigerator, book, clock, vase,
scissors, teddy bear, hair drier, toothbrush
```

## 🧯 Troubleshooting

> 🔧 **Having issues?** See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed solutions to common problems.

### 🚫 Installation Issues

**Environment creation fails:**
```bash
# Try manual installation
conda create -n yolo11-TD python=3.11.10 -y
conda activate yolo11-TD
pip install ultralytics opencv-python torch torchvision
```

**Import errors in TouchDesigner:**
* Make sure TouchDesigner is using the correct Python environment
* Check: Edit → Preferences → Python → Python 64-bit Module Path
* Should point to your conda environment: `/path/to/conda/envs/yolo11-TD/`

### 🚫 No Detection Output

* 🔌 Ensure video input is connected to the Script DAT
* 🧾 Check TouchDesigner console for error messages
* 📁 Verify the YOLO model file `yolo11n.pt` is accessible
* 🧪 Run `python verify_setup.py` to check your installation

### 🐢 Poor Performance

* ⏫ Increase Frame Skip value
* 🎯 Use specific class filtering
* 🔽 Lower video resolution
* ⚡ Check that hardware acceleration is active

### ⚠️ Hardware Acceleration Not Working

**macOS:**

```bash
python -c "import torch; print(torch.backends.mps.is_available())"
```

**Windows:**

```bash
nvidia-smi
python -c "import torch; print(torch.cuda.is_available())"
```

## 🧬 Technical Details

### 🧱 Architecture

* 🧠 **Model**: YOLO v11 Nano (`yolo11n.pt`)
* 🧪 **Framework**: Ultralytics YOLO (PyTorch backend)
* 🖼️ **Image Processing**: OpenCV
* 💾 **Memory**: Efficient numpy-based flow

### 🌍 Cross-Platform Note

* 🍎 Uses **MPS** on Apple Silicon
* 💠 Uses **CUDA** on Windows with NVIDIA GPU
* ❌ CPU fallback is not officially supported for production

### 🎛️ TouchDesigner Integration

* 🔗 Parameters sync with UI elements
* 💾 Settings persist between sessions
* 🔄 No script restart needed for parameter updates
* 🛡️ Error-handling included

## 🤝 Contributing

PRs and issues are welcome! 🙌

## 📄 License

MIT License — see LICENSE file

## 🙏 Acknowledgments

* [Ultralytics YOLO](https://github.com/ultralytics/ultralytics)
* [TouchDesigner](https://derivative.ca/)
* [PyTorch](https://pytorch.org/)
