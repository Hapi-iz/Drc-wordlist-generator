import subprocess
import sys
import os

def install_package(package):
    """Install a package using pip."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"{package} has been successfully installed.")
    except subprocess.CalledProcessError:
        print(f"[bold red]Error: Failed to install {package}.[/bold red]")
        sys.exit(1)

def check_pip_installed():
    """Check if pip is installed."""
    try:
        
        subprocess.check_call([sys.executable, "-m", "ensurepip"])
    except subprocess.CalledProcessError:
        print("[bold red]Error: pip is not installed. Please install pip to continue.[/bold red]")
        sys.exit(1)


check_pip_installed()

try:
    import rich
except ImportError:
    print("Rich library is not installed. Installing...")
    install_package("rich")
else:
    print("Rich library is already installed.")


