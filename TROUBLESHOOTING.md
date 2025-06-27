# 🔧 Troubleshooting Guide

## 🚨 Common Issues & Solutions

### 1. ❌ Environment Creation Fails

**Problem:** `conda env create -f environment_optimized.yml` fails

**Solutions:**
```bash
# Option 1: Update conda first
conda update conda
conda env create -f environment_optimized.yml

# Option 2: Manual installation
conda create -n yolo11-TD python=3.11.10 -y
conda activate yolo11-TD
pip install torch torchvision ultralytics opencv-python numpy

# Option 3: Use pip instead
python -m venv yolo11-TD
source yolo11-TD/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### 2. 🐍 TouchDesigner Python Path Issues

**Problem:** TouchDesigner can't find your conda environment

**Solutions:**
1. **Find your conda path:**
   ```bash
   conda activate yolo11-TD
   python -c "import sys; print(sys.executable)"
   ```

2. **Set in TouchDesigner:**
   - Edit → Preferences → Python
   - Set "Python 64-bit Module Path" to your conda environment path
   - Example: `/Users/yourname/miniconda3/envs/yolo11-TD`

3. **Alternative: Use system Python:**
   ```bash
   # Install to system Python instead
   pip install torch ultralytics opencv-python
   ```

### 3. 🚫 No Detections Appearing

**Problem:** Script runs but no bounding boxes show up

**Debug Steps:**
```python
# Add these debug lines to your script temporarily:
print(f"Input connected: {scriptOp.inputs[0] is not None}")
print(f"Frame shape: {frame.shape if frame is not None else 'None'}")
print(f"Detections found: {len(det.boxes) if det.boxes else 0}")
```

**Common Fixes:**
- Lower confidence threshold to 0.1
- Check video input is actually connected
- Make sure "Draw Bounding Box" parameter is ON
- Try different video source (webcam vs. file)

### 4. 🐢 Performance Issues

**Problem:** Low FPS, choppy performance

**Optimization Checklist:**
- ✅ Hardware acceleration working? Run `python verify_setup.py`
- ✅ Set Frame Skip to 2-5
- ✅ Use specific classes only: `person,car` instead of all classes
- ✅ Lower video resolution (720p instead of 4K)
- ✅ Increase confidence threshold to 0.5+

**Check hardware acceleration:**
```python
import torch
print(f"MPS available: {torch.backends.mps.is_available()}")  # Mac
print(f"CUDA available: {torch.cuda.is_available()}")        # Windows
```

### 5. 💥 Script Errors

**Problem:** Red errors in TouchDesigner console

**Common Error Messages:**

#### `ModuleNotFoundError: No module named 'ultralytics'`
```bash
# Make sure TD is using right Python:
conda activate yolo11-TD
pip install ultralytics
```

#### `RuntimeError: No such file or directory: 'yolo11n.pt'`
```bash
# Download model manually:
python -c "from ultralytics import YOLO; YOLO('yolo11n.pt')"
```

#### `TypeError: 'NoneType' object has no attribute 'numpyArray'`
```
# Video input not connected or wrong input type
# Connect Camera DAT, Movie File DAT, or other video source
```

### 6. 🍎 macOS Specific Issues

**Problem:** "Metal not available" or slow performance on Mac

**Solutions:**
```bash
# Check MPS support:
python -c "import torch; print(torch.backends.mps.is_available())"

# If False, reinstall PyTorch:
conda uninstall pytorch torchvision -y
conda install pytorch torchvision -c pytorch
```

**macOS Permission Issues:**
- System Preferences → Security → Camera (allow TouchDesigner)
- System Preferences → Security → Files and Folders

### 7. 🪟 Windows Specific Issues

**Problem:** CUDA not working or GPU not detected

**Solutions:**
```bash
# Check CUDA availability:
nvidia-smi
python -c "import torch; print(torch.cuda.is_available())"

# Reinstall with CUDA support:
conda install pytorch torchvision pytorch-cuda=12.1 -c pytorch -c nvidia
```

### 8. 🔄 Parameter Changes Not Working

**Problem:** Changing parameters doesn't affect detection

**Fixes:**
- Make sure Script DAT is set to "DAT Execute: On"
- Save and re-open TouchDesigner project
- Check parameter spelling matches exactly

### 9. 📊 Advanced Debugging

**Enable verbose logging:**
```python
# Add to top of script:
import logging
logging.basicConfig(level=logging.DEBUG)

# In detection code:
results = model.predict(source=bgr, verbose=True)  # Change to True
```

**Monitor performance:**
```python
import time
start_time = time.time()
# ... your detection code ...
print(f"Detection took: {time.time() - start_time:.3f}s")
```

## 🆘 Still Having Issues?

### Run Full Diagnosis:
```bash
python verify_setup.py
```

### Check System Requirements:
- TouchDesigner Experimental 2025.30060+
- Python 3.11.x
- 8GB+ RAM recommended
- Mac: Apple Silicon (M1/M2/M3/M4) or Windows: NVIDIA GPU

### Get More Help:
1. Check TouchDesigner textport for error messages
2. Run verification script for detailed diagnostics
3. Try QUICKSTART.md for simplified setup
4. Check if issue exists with simple test video

---

**💡 Pro Tip:** Always run `python verify_setup.py` first when troubleshooting!
