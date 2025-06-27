# 🚀 Quick Start Guide

**Get up and running with YOLO in TouchDesigner in 5 minutes!**

## ⚡ Super Quick Setup (macOS/Windows)

### 1️⃣ Install Environment (2 minutes)
```bash
# Clone or download this project
# Open terminal in project folder

# Create environment
conda env create -f environment_optimized.yml
conda activate yolo11-TD

# Verify everything works
python verify_setup.py
```

### 2️⃣ TouchDesigner Setup (2 minutes)
1. **Open TouchDesigner Experimental 2025.30060**
2. **Create Script DAT** (DAT → Script DAT)
3. **Copy-paste** entire content from `Python/touchdesigner_yolo_script.py` into the Script DAT
4. **Set DAT Execute to "On"**
5. **Connect video source** (Camera DAT, Movie File DAT, etc.) to Script DAT input

### 3️⃣ Test It! (1 minute)
- **First run**: YOLO model will auto-download (~10-30 seconds)
- **See detections**: Bounding boxes should appear around objects
- **Adjust parameters**: Use the YOLO parameter page that appears

## 🎛️ Essential Parameters

| Parameter | What it does | Recommended |
|-----------|--------------|-------------|
| **Draw Bounding Box** | Show/hide detection boxes | ✅ On |
| **Detection Classes** | Filter objects (e.g., "person,car") | Leave empty for all |
| **Confidence Threshold** | Detection sensitivity | 0.25-0.4 |
| **Frame Skip** | Performance optimization | 0 (no skip) |

## 🎯 Common Use Cases

### 👤 **People Detection Only**
- Detection Classes: `person`
- Confidence: `0.3`

### 🚗 **Traffic Monitoring**  
- Detection Classes: `person,car,bicycle,motorcycle,bus,truck`
- Confidence: `0.4`

### 🏠 **Indoor Objects**
- Detection Classes: `person,chair,cup,bottle,laptop,cell phone`
- Confidence: `0.3`

## 🚨 Quick Troubleshooting

**❌ No detections appearing:**
- Check video input is connected
- Lower confidence threshold to 0.2
- Make sure "Draw Bounding Box" is ON

**🐢 Performance issues:**
- Set Frame Skip to 2-5
- Use specific classes only
- Lower video resolution

**💥 Script errors:**
- Run `python verify_setup.py`
- Check TouchDesigner console for errors
- Make sure you're using Experimental 2025.30060

## 📞 Need Help?

1. **Run verification**: `python verify_setup.py`
2. **Check README.md** for detailed troubleshooting
3. **Console errors**: Look at TouchDesigner's textport for error messages

---

**🎉 That's it! You should now have real-time object detection in TouchDesigner!**
