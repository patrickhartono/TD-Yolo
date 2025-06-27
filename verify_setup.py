#!/usr/bin/env python3
"""
YOLO TouchDesigner Setup Verification Script
============================================

This script verifies that all dependencies are correctly installed
and hardware acceleration is working properly.

Run this after setting up your environment to ensure everything works.
"""

import sys
import os

def print_header(title):
    print(f"\n{'='*50}")
    print(f"🔍 {title}")
    print(f"{'='*50}")

def check_python_version():
    print_header("Python Version Check")
    version = sys.version_info
    print(f"Python Version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor == 11:
        print("✅ Python version is correct (3.11.x)")
        return True
    else:
        print("❌ Python version should be 3.11.x")
        print("   Please create environment with: conda create -n yolo11-TD python=3.11.10")
        return False

def check_torch_installation():
    print_header("PyTorch Installation Check")
    try:
        import torch
        print(f"✅ PyTorch installed: {torch.__version__}")
        
        # Check hardware acceleration
        print("\n🔧 Hardware Acceleration Status:")
        
        # Check MPS (Apple Silicon)
        if hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            print("✅ MPS (Metal Performance Shaders) available - Apple Silicon detected")
            print("   🚀 YOLO will use hardware acceleration on this Mac")
            return True, 'mps'
        
        # Check CUDA (NVIDIA GPU)
        elif torch.cuda.is_available():
            gpu_count = torch.cuda.device_count()
            gpu_name = torch.cuda.get_device_name(0) if gpu_count > 0 else "Unknown"
            print(f"✅ CUDA available - {gpu_count} GPU(s) detected")
            print(f"   GPU: {gpu_name}")
            print("   🚀 YOLO will use hardware acceleration on this GPU")
            return True, 'cuda'
        
        # CPU fallback
        else:
            print("⚠️  Only CPU available - no hardware acceleration")
            print("   Performance will be limited (~15-30 FPS)")
            print("   Consider using a Mac with Apple Silicon or PC with NVIDIA GPU")
            return True, 'cpu'
            
    except ImportError as e:
        print(f"❌ PyTorch not installed: {e}")
        print("   Install with: conda install pytorch torchvision torchaudio -c pytorch")
        return False, None

def check_opencv():
    print_header("OpenCV Check")
    try:
        import cv2
        print(f"✅ OpenCV installed: {cv2.__version__}")
        return True
    except ImportError:
        print("❌ OpenCV not installed")
        print("   Install with: pip install opencv-python")
        return False

def check_ultralytics():
    print_header("YOLO (Ultralytics) Check")
    try:
        from ultralytics import YOLO
        import ultralytics
        print(f"✅ Ultralytics installed: {ultralytics.__version__}")
        
        # Test model loading
        print("\n🧠 Testing YOLO model loading...")
        try:
            model = YOLO('yolo11n.pt')  # This will auto-download if needed
            print("✅ YOLO11n model loaded successfully")
            print(f"   Model classes: {len(model.names)} categories")
            return True
        except Exception as e:
            print(f"⚠️  YOLO model loading issue: {e}")
            print("   Model will auto-download on first use in TouchDesigner")
            return True  # Still consider it a pass
            
    except ImportError:
        print("❌ Ultralytics not installed")
        print("   Install with: pip install ultralytics")
        return False

def check_numpy():
    print_header("NumPy Check")
    try:
        import numpy as np
        print(f"✅ NumPy installed: {np.__version__}")
        
        # Test basic array operations
        test_array = np.random.rand(100, 100, 3)
        print(f"✅ NumPy working correctly (test array: {test_array.shape})")
        return True
    except ImportError:
        print("❌ NumPy not installed")
        print("   Install with: conda install numpy")
        return False

def check_optional_packages():
    print_header("Optional Packages Check")
    
    optional_packages = {
        'psutil': 'System monitoring',
        'matplotlib': 'Plotting and visualization', 
        'pandas': 'Data analysis',
        'numba': 'JIT compilation for performance'
    }
    
    for package, description in optional_packages.items():
        try:
            __import__(package)
            print(f"✅ {package} - {description}")
        except ImportError:
            print(f"⚠️  {package} not installed - {description}")

def test_yolo_inference():
    print_header("YOLO Inference Test")
    try:
        import torch
        import numpy as np
        from ultralytics import YOLO
        
        # Create dummy image (480x640x3 RGB)
        dummy_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        
        # Load model and run inference
        model = YOLO('yolo11n.pt')
        results = model.predict(source=dummy_image, verbose=False)
        
        print("✅ YOLO inference test successful")
        print(f"   Input shape: {dummy_image.shape}")
        print(f"   Detections: {len(results[0].boxes) if results[0].boxes is not None else 0}")
        return True
        
    except Exception as e:
        print(f"❌ YOLO inference test failed: {e}")
        return False

def generate_summary(results):
    print_header("VERIFICATION SUMMARY")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("🎉 ALL CHECKS PASSED!")
        print("   Your environment is ready for TouchDesigner YOLO integration")
        print("\n📋 Next steps:")
        print("   1. Open TouchDesigner Experimental 2025.30060")
        print("   2. Create a Script DAT")
        print("   3. Copy touchdesigner_yolo_script.py content into the DAT")
        print("   4. Connect your video source and start detecting!")
    else:
        print("❌ SOME CHECKS FAILED")
        print("   Please fix the issues above before using with TouchDesigner")
        
        failed_checks = [check for check, passed in results.items() if not passed]
        print(f"\n🔧 Failed checks: {', '.join(failed_checks)}")

def main():
    print("🧠 YOLO TouchDesigner Setup Verification")
    print("=========================================")
    print("Checking if your environment is ready for YOLO object detection...")
    
    # Run all checks
    results = {
        'Python Version': check_python_version(),
        'PyTorch': check_torch_installation()[0],
        'OpenCV': check_opencv(),
        'Ultralytics YOLO': check_ultralytics(),
        'NumPy': check_numpy(),
        'YOLO Inference': test_yolo_inference()
    }
    
    # Check optional packages (doesn't affect pass/fail)
    check_optional_packages()
    
    # Generate summary
    generate_summary(results)
    
    return all(results.values())

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
