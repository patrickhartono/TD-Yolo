#!/usr/bin/env python3
"""
Standalone YOLO Test Script
===========================

This script tests the core YOLO functionality outside of TouchDesigner
to ensure all components work correctly.

Run this to verify YOLO detection works with dummy data.
"""

import numpy as np
import cv2
from ultralytics import YOLO
import torch
import time

def test_yolo_detection():
    print("🧪 Testing YOLO Detection Pipeline")
    print("=" * 50)
    
    # 1. Test device detection
    print("\n1️⃣ Hardware Detection Test:")
    if torch.backends.mps.is_available():
        device = 'mps'
        print("✅ MPS (Apple Silicon) detected")
    elif torch.cuda.is_available():
        device = 'cuda'
        print(f"✅ CUDA detected - {torch.cuda.get_device_name(0)}")
    else:
        device = 'cpu'
        print("⚠️  CPU only (performance will be limited)")
    
    # 2. Test model loading
    print("\n2️⃣ Model Loading Test:")
    try:
        model = YOLO('yolo11n.pt')
        model.to(device)
        print(f"✅ YOLO model loaded successfully on {device}")
        print(f"   Model classes: {len(model.names)}")
    except Exception as e:
        print(f"❌ Model loading failed: {e}")
        return False
    
    # 3. Test image processing pipeline
    print("\n3️⃣ Image Processing Test:")
    try:
        # Create test image (similar to TouchDesigner input)
        # RGBA float [0-1] format like TouchDesigner provides
        rgba_float = np.random.rand(480, 640, 4).astype(np.float32)
        print(f"✅ Created test RGBA image: {rgba_float.shape}")
        
        # Convert to BGR uint8 (like in TD script)
        bgr = cv2.cvtColor(np.clip(rgba_float * 255, 0, 255).astype(np.uint8), cv2.COLOR_RGBA2BGR)
        print(f"✅ Converted to BGR: {bgr.shape}")
        
    except Exception as e:
        print(f"❌ Image processing failed: {e}")
        return False
    
    # 4. Test YOLO inference
    print("\n4️⃣ YOLO Inference Test:")
    try:
        start_time = time.time()
        
        with torch.no_grad():
            results = model.predict(
                source=bgr,
                conf=0.25,
                verbose=False,
                device=device,
                half=True if device == 'mps' else False,
                imgsz=640
            )
        
        inference_time = time.time() - start_time
        
        det = results[0]
        num_detections = len(det.boxes) if det.boxes is not None else 0
        
        print(f"✅ Inference completed in {inference_time:.3f}s")
        print(f"   Detections found: {num_detections}")
        print(f"   FPS estimate: ~{1/inference_time:.1f}")
        
    except Exception as e:
        print(f"❌ YOLO inference failed: {e}")
        return False
    
    # 5. Test bounding box rendering
    print("\n5️⃣ Bounding Box Rendering Test:")
    try:
        if num_detections > 0:
            rendered = det.plot()
            print(f"✅ Bounding boxes rendered: {rendered.shape}")
        else:
            print("✅ No detections to render (expected with random image)")
            rendered = bgr
        
        # Test final conversion back to RGBA
        rgba_output = cv2.cvtColor(rendered, cv2.COLOR_BGR2RGBA)
        rgba_output = cv2.flip(rgba_output, 0)
        print(f"✅ Final output format: {rgba_output.shape}")
        
    except Exception as e:
        print(f"❌ Rendering failed: {e}")
        return False
    
    # 6. Test class filtering
    print("\n6️⃣ Class Filtering Test:")
    try:
        # Test with specific classes
        person_class = None
        for idx, name in model.names.items():
            if name.lower() == 'person':
                person_class = [idx]
                break
        
        if person_class:
            results_filtered = model.predict(
                source=bgr,
                conf=0.25,
                classes=person_class,
                verbose=False,
                device=device
            )
            print("✅ Class filtering (person only) works")
        else:
            print("⚠️  'person' class not found in model")
            
    except Exception as e:
        print(f"❌ Class filtering failed: {e}")
        return False
    
    # 7. Performance benchmark
    print("\n7️⃣ Performance Benchmark:")
    try:
        num_runs = 10
        times = []
        
        for i in range(num_runs):
            start = time.time()
            with torch.no_grad():
                _ = model.predict(
                    source=bgr,
                    conf=0.25,
                    verbose=False,
                    device=device,
                    half=True if device == 'mps' else False
                )
            times.append(time.time() - start)
        
        avg_time = np.mean(times)
        avg_fps = 1 / avg_time
        
        print(f"✅ Average inference time: {avg_time:.3f}s")
        print(f"✅ Average FPS: {avg_fps:.1f}")
        print(f"✅ Performance rating: {'🚀 Excellent' if avg_fps > 30 else '⚡ Good' if avg_fps > 15 else '🐢 Limited'}")
        
    except Exception as e:
        print(f"❌ Performance benchmark failed: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 ALL TESTS PASSED!")
    print("🎮 Ready for TouchDesigner integration!")
    print("\n📋 Performance Summary:")
    print(f"   Device: {device.upper()}")
    print(f"   Average FPS: {avg_fps:.1f}")
    print(f"   Model: YOLO11n ({len(model.names)} classes)")
    
    return True

if __name__ == "__main__":
    success = test_yolo_detection()
    if not success:
        print("\n❌ Some tests failed. Check your installation.")
        exit(1)
    else:
        print("\n✅ All systems ready for TouchDesigner!")
        exit(0)
