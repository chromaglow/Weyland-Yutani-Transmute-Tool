#!/usr/bin/env python3
"""
FreeCAD Detection and Verification Test Script
Helps troubleshoot FreeCAD integration issues and verify installation integrity
"""

import sys
import os
from pathlib import Path
import winreg  # Windows registry access

def test_freecad_detection():
    """Test FreeCAD detection and provide troubleshooting information"""

    print("="*60)
    print("FREECAD DETECTION TEST")
    print("="*60)

    # Test 1: Direct import
    print("\n1. Testing direct FreeCAD import...")
    try:
        import FreeCAD
        print("✓ SUCCESS: FreeCAD imported directly")
        print(f"   FreeCAD version: {FreeCAD.Version()}")
        return True
    except ImportError as e:
        print(f"✗ FAILED: {e}")
        if "python311.dll" in str(e).lower():
            print("   → This is a Python version conflict!")
            print("   → FreeCAD 1.0 requires Python 3.11, but you have Python 3.13")
            print("   → Solution: Use FreeCAD's bundled Python or configure paths correctly")

    # Test 1.5: Try importing with FreeCAD's Python
    freecad_python = r"C:\Program Files\FreeCAD 1.0\bin\python.exe"
    if os.path.exists(freecad_python):
        print("\n1.5. Testing with FreeCAD's bundled Python 3.11...")
        try:
            # We'll test this by running a subprocess
            import subprocess
            result = subprocess.run([freecad_python, "-c", "import FreeCAD; print('SUCCESS:', FreeCAD.Version())"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("✓ SUCCESS: FreeCAD works with its bundled Python!")
                print(f"   Output: {result.stdout.strip()}")
                print("   → To use FreeCAD from your app, you need to configure the Python path")
                return True
            else:
                print(f"✗ FAILED: {result.stderr.strip()}")
        except Exception as e:
            print(f"✗ FAILED to test with FreeCAD Python: {e}")

    # Test 2: Check common paths
    print("\n2. Checking common FreeCAD installation paths...")

    common_paths = [
        r"C:\Program Files\FreeCAD\bin",
        r"C:\Program Files (x86)\FreeCAD\bin",
        r"C:\FreeCAD\bin",
        r"C:\Program Files\FreeCAD 1.0\bin",  # Found actual installation
        os.path.expanduser(r"~\AppData\Local\FreeCAD\bin"),
    ]

    found_paths = []
    for path in common_paths:
        if os.path.exists(path):
            print(f"✓ Found FreeCAD bin folder: {path}")
            found_paths.append(path)
        else:
            print(f"✗ Not found: {path}")

    # Test 3: Try to import from found paths
    print("\n3. Testing import from detected paths...")
    for path in found_paths:
        try:
            sys.path.insert(0, path)
            import FreeCAD
            print(f"✓ SUCCESS: FreeCAD imported from {path}")
            print(f"   FreeCAD version: {FreeCAD.Version()}")
            return True
        except ImportError as e:
            print(f"✗ FAILED to import from {path}: {e}")
            # Remove from path if it failed
            if path in sys.path:
                sys.path.remove(path)

    # Test 4: Check environment variables
    print("\n4. Checking environment variables...")
    freecad_root = os.environ.get('FREECAD_ROOT')
    if freecad_root:
        print(f"✓ FREECAD_ROOT environment variable: {freecad_root}")
        freecad_bin = os.path.join(freecad_root, 'bin')
        if os.path.exists(freecad_bin):
            print(f"✓ FreeCAD bin folder found at: {freecad_bin}")
            try:
                sys.path.insert(0, freecad_bin)
                import FreeCAD
                print("✓ SUCCESS: FreeCAD imported via FREECAD_ROOT")
                return True
            except ImportError as e:
                print(f"✗ FAILED: {e}")
    else:
        print("✗ FREECAD_ROOT environment variable not set")

    # Test 5: Check PATH
    print("\n5. Checking PATH environment variable...")
    path_env = os.environ.get('PATH', '')
    freecad_in_path = False
    for path_item in path_env.split(os.pathsep):
        if 'freecad' in path_item.lower() and os.path.exists(path_item):
            print(f"✓ FreeCAD found in PATH: {path_item}")
            freecad_in_path = True
            try:
                sys.path.insert(0, path_item)
                import FreeCAD
                print("✓ SUCCESS: FreeCAD imported from PATH")
                return True
            except ImportError as e:
                print(f"✗ FAILED: {e}")

    if not freecad_in_path:
        print("✗ No FreeCAD directories found in PATH")

    # Test 6: Comprehensive system search
    found_installations = find_freecad_installations()
    
    # Test 7: Windows registry check
    registry_paths = check_windows_registry()
    found_installations.extend(registry_paths)
    
    if found_installations:
        print(f"\n✓ Found {len(found_installations)} FreeCAD installation(s)")
        
        for install_path in found_installations:
            print(f"\n🔍 Analyzing installation: {install_path}")
            verification = verify_freecad_installation(install_path)
            
            if verification['can_import']:
                print(f"✅ This installation can be imported successfully!")
                return True
            else:
                print(f"❌ This installation has issues and cannot be imported")
                if verification['missing_required']:
                    print(f"   Missing required files: {verification['missing_required']}")
    
    # Test 8: Check user-added PATH entries specifically
    print("\n8. Checking user-added PATH entries for FreeCAD...")
    path_env = os.environ.get('PATH', '')
    user_freecad_paths = []
    
    for path_item in path_env.split(os.pathsep):
        path_item = path_item.strip()
        if path_item and 'freecad' in path_item.lower() and os.path.exists(path_item):
            user_freecad_paths.append(path_item)
            print(f"✓ Found FreeCAD in PATH: {path_item}")
            
            # Try to find the root installation from this bin path
            potential_root = os.path.dirname(path_item)  # Go up one level from bin
            if os.path.exists(potential_root):
                print(f"  → Potential installation root: {potential_root}")
                verification = verify_freecad_installation(potential_root)
                if verification['can_import']:
                    print("  ✅ This PATH entry leads to a working FreeCAD installation!")
                    return True
    
    if not user_freecad_paths:
        print("✗ No FreeCAD paths found in PATH environment variable")
    
    # Troubleshooting advice
    print("\n" + "="*60)
    print("TROUBLESHOOTING ADVICE")
    print("="*60)

    print("\nIf FreeCAD is installed but not detected:")
    print("1. PYTHON VERSION CONFLICT: FreeCAD 1.0 uses Python 3.11, but you have Python 3.13")
    print("   → SOLUTION: Configure your application to use FreeCAD's Python path")
    print("   → Add this to your Python script before importing FreeCAD:")
    print("     import sys")
    print("     sys.path.insert(0, r'C:\\Program Files\\FreeCAD 1.0\\bin')")
    print("   → Or set PYTHONPATH environment variable to include FreeCAD's bin folder")
    print("")
    print("2. Try running the application as Administrator")
    print("3. Check if FreeCAD is installed in a custom location")
    print("4. Add FreeCAD's bin folder to your system PATH:")
    print("   - Right-click 'This PC' > Properties > Advanced system settings")
    print("   - Click 'Environment Variables'")
    print("   - Edit 'Path' and add: C:\\Program Files\\FreeCAD 1.0\\bin")
    print("5. Set FREECAD_ROOT environment variable to: C:\\Program Files\\FreeCAD 1.0")
    print("6. Verify FreeCAD installation integrity - some files may be missing")
    print("7. Try reinstalling FreeCAD if core files are missing")

    print("\nCommon FreeCAD installation locations:")
    for path in common_paths:
        print(f"   {path}")

    return False
    
    # Troubleshooting advice
    print("\n" + "="*60)
    print("TROUBLESHOOTING ADVICE")
    print("="*60)

    print("\nIf FreeCAD is installed but not detected:")
    print("1. Try running the application as Administrator")
    print("2. Check if FreeCAD is installed in a custom location")
    print("3. Add FreeCAD's bin folder to your system PATH:")
    print("   - Right-click 'This PC' > Properties > Advanced system settings")
    print("   - Click 'Environment Variables'")
    print("   - Edit 'Path' and add: C:\\Program Files\\FreeCAD\\bin")
    print("4. Set FREECAD_ROOT environment variable to FreeCAD installation folder")

    print("\nCommon FreeCAD installation locations:")
    for path in common_paths:
        print(f"   {path}")

def check_windows_registry():
    """Check Windows registry for FreeCAD installation information"""
    
    print("\n7. Checking Windows registry for FreeCAD...")
    
    registry_paths = []
    
    try:
        # Check uninstall registry for FreeCAD
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall") as key:
            i = 0
            while True:
                try:
                    subkey = winreg.EnumKey(key, i)
                    with winreg.OpenKey(key, subkey) as sub_key:
                        try:
                            display_name = winreg.QueryValueEx(sub_key, "DisplayName")[0]
                            if "freecad" in display_name.lower():
                                try:
                                    install_location = winreg.QueryValueEx(sub_key, "InstallLocation")[0]
                                    if install_location:
                                        registry_paths.append(install_location)
                                        print(f"   ✓ Registry: {display_name} at {install_location}")
                                except FileNotFoundError:
                                    pass
                        except FileNotFoundError:
                            pass
                    i += 1
                except OSError:
                    break
                    
        # Check for FreeCAD in Program Files registry
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\FreeCAD") as key:
                try:
                    install_path = winreg.QueryValueEx(key, "")[0]
                    registry_paths.append(install_path)
                    print(f"   ✓ FreeCAD registry key: {install_path}")
                except FileNotFoundError:
                    pass
        except FileNotFoundError:
            pass
            
    except Exception as e:
        print(f"   ✗ Registry check failed: {e}")
    
    return registry_paths

def find_freecad_installations():
    """Search for FreeCAD installations on the system"""
    
    print("\n6. Searching for FreeCAD installations on your system...")
    
    found_installations = []
    
    # Search common drive letters
    drives = ['C:', 'D:', 'E:']
    
    for drive in drives:
        if not os.path.exists(drive):
            continue
            
        print(f"   Searching {drive} drive...")
        
        # Search for FreeCAD executables
        for root, dirs, files in os.walk(drive):
            # Don't search too deep to avoid performance issues
            if root.count(os.sep) - drive.count(os.sep) > 4:
                dirs[:] = []  # Don't recurse deeper
                continue
                
            if 'freecad' in root.lower():
                # Check if this looks like a FreeCAD installation
                if any('freecad.exe' in f.lower() for f in files):
                    found_installations.append(root)
                    print(f"   ✓ Found FreeCAD installation: {root}")
                    
                    # Check for bin folder
                    bin_folder = os.path.join(root, 'bin')
                    if os.path.exists(bin_folder):
                        print(f"     → Bin folder: {bin_folder}")
                        
                        # Check for FreeCAD libraries
                        freecad_dll = os.path.join(bin_folder, 'FreeCAD.dll')
                        if os.path.exists(freecad_dll):
                            print("     → FreeCAD.dll found - this looks like a valid installation")
    
    return found_installations

def verify_freecad_installation(freecad_path):
    """Verify that a FreeCAD installation has all required files"""
    
    print(f"\n🔍 Verifying FreeCAD installation at: {freecad_path}")
    
    # Required files for FreeCAD Python integration
    required_files = [
        'bin/FreeCAD.exe',           # Main executable
        'bin/FreeCAD.dll',           # Core DLL
        'bin/FreeCAD.pyd',           # Python extension
        'bin/FreeCADGui.pyd',        # GUI Python extension
        'bin/FreeCADBase.pyd',       # Base Python extension
        'bin/Part.pyd',              # Part workbench
        'bin/Mesh.pyd',              # Mesh workbench
    ]
    
    # Optional but recommended files
    optional_files = [
        'bin/FreeCADCmd.exe',        # Command line version
        'bin/libpack.dll',           # Library pack
    ]
    
    missing_required = []
    missing_optional = []
    found_required = []
    found_optional = []
    
    print("  Checking required files:")
    for file_path in required_files:
        full_path = os.path.join(freecad_path, file_path)
        if os.path.exists(full_path):
            print(f"    ✓ {file_path}")
            found_required.append(file_path)
        else:
            print(f"    ✗ {file_path} - MISSING")
            missing_required.append(file_path)
    
    print("  Checking optional files:")
    for file_path in optional_files:
        full_path = os.path.join(freecad_path, file_path)
        if os.path.exists(full_path):
            print(f"    ✓ {file_path}")
            found_optional.append(file_path)
        else:
            print(f"    ✗ {file_path} - MISSING")
            missing_optional.append(file_path)
    
    # Check if this installation can be imported
    bin_path = os.path.join(freecad_path, 'bin')
    if os.path.exists(bin_path):
        print(f"\n  Testing Python import from {bin_path}...")
        original_path = sys.path[:]
        try:
            sys.path.insert(0, bin_path)
            import FreeCAD
            version = FreeCAD.Version()
            print(f"    ✓ SUCCESS: FreeCAD {version} imported successfully")
            can_import = True
        except ImportError as e:
            print(f"    ✗ FAILED: {e}")
            can_import = False
        finally:
            sys.path[:] = original_path
    else:
        print(f"  ✗ Bin folder not found at {bin_path}")
        can_import = False
    
    return {
        'path': freecad_path,
        'missing_required': missing_required,
        'missing_optional': missing_optional,
        'found_required': found_required,
        'found_optional': found_optional,
        'can_import': can_import
    }

def test_step_conversion():
    """Test STEP conversion functionality"""
    
    print("Testing STEP conversion with FreeCAD...")
    
    # Check if FreeCAD is available
    freecad_python = r"C:\Program Files\FreeCAD 1.0\bin\python.exe"
    if not os.path.exists(freecad_python):
        print("❌ FreeCAD Python not found")
        return
    
    # Create a simple test STL file
    import tempfile
    import trimesh
    
    try:
        # Create a simple cube mesh for testing
        mesh = trimesh.creation.box(extents=[1, 1, 1])
        
        with tempfile.NamedTemporaryFile(suffix='.stl', delete=False) as temp_stl:
            temp_stl_path = temp_stl.name
            mesh.export(temp_stl_path)
        
        with tempfile.NamedTemporaryFile(suffix='.step', delete=False) as temp_step:
            temp_step_path = temp_step.name
        
        print(f"Created test STL: {temp_stl_path}")
        print(f"Target STEP: {temp_step_path}")
        
        # Create FreeCAD conversion script
        freecad_script = f"""
import sys
import os
sys.path.append(r'C:\\Program Files\\FreeCAD 1.0\\bin')

try:
    import FreeCAD
    import Mesh
    import Part
    
    print("FreeCAD test: Starting conversion...")
    print(f"FreeCAD version: {{FreeCAD.Version()}}")
    
    # Import STL mesh
    mesh_obj = Mesh.Mesh(r'{temp_stl_path}')
    print(f"FreeCAD test: Mesh imported - {{len(mesh_obj.Facets)}} faces")
    
    # Convert mesh to shape
    shape = Part.Shape()
    shape.makeShapeFromMesh(mesh_obj.Topology, 0.05)
    
    # Create solid from shape
    solid = Part.makeSolid(shape)
    print(f"FreeCAD test: Solid created - Volume: {{solid.Volume}}")
    
    # Export to STEP
    solid.exportStep(r'{temp_step_path}')
    
    if os.path.exists(r'{temp_step_path}'):
        print("FreeCAD test: SUCCESS - STEP file created")
    else:
        print("FreeCAD test: ERROR - STEP file was not created")
        sys.exit(1)
    
except Exception as e:
    import traceback
    print(f"FreeCAD test error: {{e}}")
    traceback.print_exc()
    sys.exit(1)
"""
        
        # Write and run the script
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as script_file:
            script_file.write(freecad_script)
            script_path = script_file.name
        
        print("Running FreeCAD conversion test...")
        import subprocess
        result = subprocess.run(
            [freecad_python, script_path],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        print(f"Return code: {result.returncode}")
        print(f"STDOUT: {result.stdout}")
        if result.stderr:
            print(f"STDERR: {result.stderr}")
        
        # Clean up
        os.unlink(script_path)
        os.unlink(temp_stl_path)
        if os.path.exists(temp_step_path):
            print(f"✓ STEP file created successfully: {temp_step_path}")
            os.unlink(temp_step_path)
        
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    try:
        print("Starting FreeCAD detection test...")
        success = test_freecad_detection()
        if success:
            print("\n🎉 FreeCAD integration should work!")
        else:
            print("\n❌ FreeCAD integration needs troubleshooting")
            
        # Also test STEP conversion if FreeCAD is available
        print("\n" + "="*60)
        print("TESTING STEP CONVERSION")
        print("="*60)
        
        test_step_conversion()
        
    except Exception as e:
        print(f"Error running test: {e}")
        import traceback
        traceback.print_exc()
    print()