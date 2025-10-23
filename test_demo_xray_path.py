"""
Test script to verify demo X-ray path resolution
Run this before starting Streamlit to ensure the demo image will be found
"""

from pathlib import Path
import os

def test_demo_xray_path():
    """Test that the demo X-ray can be found using different path methods"""
    
    print("=" * 80)
    print("DEMO X-RAY PATH RESOLUTION TEST")
    print("=" * 80)
    
    # Method 1: Current working directory
    cwd = Path.cwd()
    demo_cwd = cwd / "uploads" / "demo_xray.png"
    print(f"\n1. Current Working Directory Method:")
    print(f"   CWD: {cwd}")
    print(f"   Demo path: {demo_cwd}")
    print(f"   Exists: {demo_cwd.exists()} {'✅' if demo_cwd.exists() else '❌'}")
    
    # Method 2: Script directory (__file__)
    try:
        script_dir = Path(__file__).parent.resolve()
        demo_script = script_dir / "uploads" / "demo_xray.png"
        print(f"\n2. Script Directory Method (__file__):")
        print(f"   Script dir: {script_dir}")
        print(f"   Demo path: {demo_script}")
        print(f"   Exists: {demo_script.exists()} {'✅' if demo_script.exists() else '❌'}")
    except NameError:
        print(f"\n2. Script Directory Method: Not available (running interactively)")
    
    # Method 3: Absolute path
    abs_path = Path("c:/Users/madha/multi-agent-healthcare/uploads/demo_xray.png")
    print(f"\n3. Absolute Path Method:")
    print(f"   Demo path: {abs_path}")
    print(f"   Exists: {abs_path.exists()} {'✅' if abs_path.exists() else '❌'}")
    
    # Method 4: The get_demo_xray_path function logic
    try:
        test_script_dir = Path(__file__).parent.resolve()
    except (NameError, OSError):
        test_script_dir = Path.cwd()
    
    demo_final = test_script_dir / "uploads" / "demo_xray.png"
    print(f"\n4. Final Implementation (get_demo_xray_path logic):")
    print(f"   Base dir: {test_script_dir}")
    print(f"   Demo path: {demo_final}")
    print(f"   Exists: {demo_final.exists()} {'✅' if demo_final.exists() else '❌'}")
    
    # Check file details
    if demo_final.exists():
        file_size = demo_final.stat().st_size
        print(f"\n5. File Details:")
        print(f"   Size: {file_size:,} bytes ({file_size / 1024:.1f} KB)")
        print(f"   Absolute path: {demo_final.absolute()}")
        
        # Try to open it
        try:
            from PIL import Image
            img = Image.open(demo_final)
            print(f"   Image format: {img.format}")
            print(f"   Image size: {img.size}")
            print(f"   Image mode: {img.mode}")
            print(f"   ✅ Image is valid and loadable")
        except Exception as e:
            print(f"   ❌ Error loading image: {e}")
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    if demo_final.exists():
        print("✅ Demo X-ray is READY!")
        print(f"✅ Path: {demo_final}")
        print("✅ Streamlit should be able to load the demo image")
    else:
        print("❌ Demo X-ray NOT FOUND!")
        print(f"❌ Expected at: {demo_final}")
        print("❌ Please copy the image to the uploads folder")
    
    print("=" * 80)

if __name__ == "__main__":
    test_demo_xray_path()
