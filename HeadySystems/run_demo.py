import os
import sys
import subprocess

def main():
    print("Starting Heady Demo...")

    # Path to admin_console.py
    base_dir = os.path.dirname(os.path.abspath(__file__))
    admin_console = os.path.join(base_dir, 'heady_project', 'src', 'admin_console.py')

    if not os.path.exists(admin_console):
        print(f"Error: {admin_console} not found.")
        return

    # Ensure we run from base_dir so paths resolve correctly
    os.chdir(base_dir)

    # Run build
    print("Running build...")
    try:
        subprocess.run([sys.executable, admin_console, '--action', 'builder_build'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        return

    # Run API
    print("Starting API Server...")
    try:
        subprocess.run([sys.executable, admin_console, '--action', 'serve_api'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Server failed: {e}")
        return

if __name__ == "__main__":
    main()
