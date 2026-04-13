# RTSC: Real-Time Suggestive Contour Viewer

**Note: This is a clone of the original [RTSC](http://www.cs.princeton.edu/gfx/proj/sugcon/) project. The main addition in this repository is a modern CMake-based build system. All credit for the algorithms and the original codebase goes to the original authors.**

RTSC is a high-performance interactive viewer for 3D meshes that implements real-time algorithms for suggestive contours, ridges, valleys, and other expressive line drawings.

![Suggestive Contours](http://www.cs.princeton.edu/gfx/proj/sugcon/img/camel_sc.jpg)

## Features

RTSC supports a wide variety of line drawing techniques:
- **Contours and Silhouettes:** Standard occluding contours and exterior silhouettes.
- **Suggestive Contours:** Expressive lines that anticipate contours as the viewpoint changes.
- **Ridges and Valleys:** Surface features based on principal curvatures.
- **Apparent Ridges:** View-dependent ridges that better capture shape.
- **Geometric Analysis:** Visualization of Gaussian and mean curvature zeros ($K=0$, $H=0$).
- **Mesh Processing:** Real-time smoothing (geometry, normals, curvatures) and Loop subdivision.
- **Advanced Shading:** Lambertian, Gooch, Toon, and Hemisphere lighting models.

## Prerequisites

RTSC requires the following libraries:
- [trimesh2](http://www.cs.princeton.edu/gfx/proj/trimesh2/): A library for 3D triangle meshes.
- **OpenGL** and **GLUT**: For 3D rendering and window management.
- **GLUI**: For the graphical user interface (distributed with trimesh2).

## Build Instructions

RTSC uses CMake for cross-platform builds.

```bash
mkdir build
cd build
cmake ..
make
```

### Configuration
By default, the build system expects `trimesh2` to be located at `../trimesh2`. You can override this by setting the `TRIMESHDIR` cache variable:
```bash
cmake -DTRIMESHDIR=/path/to/trimesh2 ..
```

## Usage

Run RTSC by providing a 3D mesh file (PLY, OBJ, OFF, etc.):

```bash
./rtsc model.ply
```

### Interactive Controls
- **Left Mouse:** Rotate the model.
- **Middle Mouse / Left+Right:** Pan.
- **Right Mouse / Scroll:** Zoom.
- **Space Bar:** Reset view.
- **'q' / 'Esc':** Quit.

Click the **Options** button in the UI to toggle different line types and adjust thresholds.

## Testing

A basic test script is provided in the `tests` directory. To run it, ensure the project is built and then execute:

```bash
python3 tests/test_basic.py
```

This script generates a simple mesh and verifies that RTSC can load it and exit correctly.

## Key Algorithms

The features in RTSC are based on several seminal papers in computer graphics:
- *Suggestive Contours for Conveying Shape* (SIGGRAPH 2003)
- *Interactive Rendering of Suggestive Contours with Temporal Coherence* (NPAR 2004)
- *Highlight Lines for Conveying Shape* (NPAR 2007)
- *Apparent Ridges for Line Drawing* (SIGGRAPH 2007)

## License

This software is distributed under the GNU General Public License (GPL). See the `COPYING` file for details.

## Authors

Szymon Rusinkiewicz and Doug DeCarlo.
