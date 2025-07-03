
import os
import subprocess
import importlib.util
import sys

def package_installed(package_name):
    """Check if a package is installed."""
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False

def check_virtual_env():
    """Check if running in a virtual environment."""
    if os.environ.get("VIRTUAL_ENV") is None:
        print("❌ Error: You must run this script from within a virtual environment or run the batch file.")
        sys.exit(1)
    else:
        print("✅ Running in virtual environment.")

def install_requirements():
    """Install packages from requirements.txt."""
    if not os.path.exists("requirements.txt"):
        print("❌ Error: requirements.txt not found!")
        return False
    
    print("📋 Installing requirements.txt...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install",
            "-r", "requirements.txt",
            "--no-deps"
        ])
        print("✅ Requirements installed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def install_torch_cuda():
    """Install PyTorch with CUDA support if not already installed."""
    if not package_installed("torch"):
        print("🔥 Installing PyTorch + CUDA dependencies...")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install",
                "torch", "torchvision", "torchaudio",
                "--index-url", "https://download.pytorch.org/whl/cu118"
            ])
            print("✅ PyTorch with CUDA installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install PyTorch with CUDA: {e}")
            print("⚠️  Falling back to CPU-only version...")
            try:
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install",
                    "torch", "torchvision", "torchaudio"
                ])
                print("✅ PyTorch (CPU-only) installed successfully.")
            except subprocess.CalledProcessError as e2:
                print(f"❌ Failed to install PyTorch: {e2}")
                return False
    else:
        print("✅ PyTorch already installed.")
    
    return True

def check_cuda_availability():
    """Check if CUDA is available in the installed PyTorch."""
    try:
        import torch
        if torch.cuda.is_available():
            print(f"🚀 CUDA is available! Device count: {torch.cuda.device_count()}")
            for i in range(torch.cuda.device_count()):
                print(f"   📱 GPU {i}: {torch.cuda.get_device_name(i)}")
        else:
            print("⚠️  CUDA is not available. Training will use CPU.")
    except ImportError:
        print("⚠️  Could not import torch to check CUDA availability.")

def list_installed_packages():
    """List all installed packages."""
    print("📦 Listing installed packages:")
    try:
        subprocess.run([sys.executable, "-m", "pip", "list"], check=True)
    except subprocess.CalledProcessError:
        print("❌ Failed to list packages.")

def setup_environment():
    """Main setup function."""
    print("🚀 Starting dependency installation for training project...")
    
    check_virtual_env()
    
    if not install_requirements():
        print("❌ Setup failed during requirements installation.")
        return False
    
    if not install_torch_cuda():
        print("❌ Setup failed during PyTorch installation.")
        return False
    
    check_cuda_availability()
    
    list_installed_packages()
    
    print("🎉 Environment setup completed successfully!")
    return True

if __name__ == "__main__":
    success = setup_environment()
    if not success:
        sys.exit(1)  
    sys.exit(0)