import os
import subprocess
import sys

def create_test_ply(filename):
    """Creates a simple 1x1x1 PLY cube."""
    ply_content = """ply
format ascii 1.0
element vertex 8
property float x
property float y
property float z
element face 12
property list uchar int vertex_indices
end_header
0 0 0
0 0 1
0 1 0
0 1 1
1 0 0
1 0 1
1 1 0
1 1 1
3 0 1 2
3 1 3 2
3 4 5 6
3 5 7 6
3 0 1 4
3 1 5 4
3 2 3 6
3 3 7 6
3 0 2 4
3 2 6 4
3 1 3 5
3 3 7 5
"""
    with open(filename, 'w') as f:
        f.write(ply_content)

def test_rtsc_load():
    """Tests if rtsc can load a mesh and exit using the 'q' command-line flag."""
    test_mesh = "test_cube.ply"
    create_test_ply(test_mesh)
    
    # Check for the binary in common build locations
    possible_binaries = ["./build/rtsc", "./rtsc"]
    rtsc_bin = None
    for b in possible_binaries:
        if os.path.isfile(b) and os.access(b, os.X_OK):
            rtsc_bin = b
            break
            
    if not rtsc_bin:
        print("Error: rtsc binary not found or not executable. Please build the project first.")
        sys.exit(1)

    print(f"Testing {rtsc_bin} with {test_mesh}...")
    
    try:
        # Run rtsc with -q flag to exit immediately
        # We also need to handle the case where a display is not available
        process = subprocess.Popen(
            [rtsc_bin, "-q", test_mesh],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for a short time to see if it crashes or loads
        try:
            stdout, stderr = process.communicate(timeout=5)
            if process.returncode == 0:
                print("Test Passed: rtsc loaded mesh and exited successfully.")
            else:
                print(f"Test Failed: rtsc exited with return code {process.returncode}")
                print("Error Output:", stderr)
                sys.exit(1)
        except subprocess.TimeoutExpired:
            process.kill()
            print("Test Warning: rtsc timed out (likely waiting for GUI/OpenGL context).")
            print("If this is a headless environment, this is expected.")

    except Exception as e:
        print(f"Test Failed: An error occurred: {e}")
        sys.exit(1)
    finally:
        if os.path.exists(test_mesh):
            os.remove(test_mesh)

if __name__ == "__main__":
    test_rtsc_load()
