# RTSC: Real-Time Suggestive Contour Viewer

**Note: This is a fork of the original RTSC project with modern CMake build system and Apple Silicon support. All credit for the algorithms goes to the original authors.**

Based on: DeCarlo, Finkelstein, Rusinkiewicz, and Santella. "[Suggestive Contours for Conveying Shape](https://dl.acm.org/doi/10.1145/882262.882354)." SIGGRAPH 2003.

RTSC is a high-performance interactive viewer for 3D meshes that implements real-time algorithms for suggestive contours, ridges, valleys, and other expressive line drawings.

## Features

RTSC supports a wide variety of line drawing techniques:
- **Contours and Silhouettes:** Standard occluding contours and exterior silhouettes.
- **Suggestive Contours:** Expressive lines that anticipate contours as the viewpoint changes.
- **Ridges and Valleys:** Surface features based on principal curvatures.
- **Apparent Ridges:** View-dependent ridges that better capture shape.
- **Geometric Analysis:** Visualization of Gaussian and mean curvature zeros ($K=0$, $H=0$).
- **Mesh Processing:** Real-time smoothing (geometry, normals, curvatures) and Loop subdivision.
- **Advanced Shading:** Lambertian, Gooch, Toon, and Hemisphere lighting models.

## Why Line Drawings Matter

No single line type captures shape completely. Each technique reveals different geometric features:

| Technique | What It Shows | Why It Matters |
|-----------|--------------|---------------|
| **Contours** | Where surface turns 90° from viewer | Defines silhouette - the most fundamental shape cue |
| **Suggestive Contours** | Where contours *would* appear with small view change | Reveals curvature even when contours are hidden |
| **Ridges** | Local maxima of principal curvature | Captures "crease" lines - like folded paper |
| **Valleys** | Local minima of principal curvature | The valleys/creases between ridges |
| **Apparent Ridges** | View-dependent ridges | Always visible parts that look like ridges |
| **Principal Highlights** | Max/min of reflected curvature | Shows where light reflects - critical for material appearance |
| **Asymptotic Lines** | Directions of maximum/minimum curvature | Reveals surface anisotropy |

**Key insight:** Combining multiple line types gives complete shape understanding. A technique like suggestive contours can reveal shape that contours alone miss:

```
Silhouette only:          With Suggestive Contours:
                                        
   ____                  ____
  /    \                /    \
 /      \      →       .·´    `·.
 \      /                `·.    ·´
  \____/                  \____
```

## Prerequisites

RTSC requires the following libraries:
- **trimesh2**: Bundled in `trimesh2/` (originally from Princeton)
- **OpenGL** and **GLUT**: For 3D rendering and window management.
- **GLUI**: Bundled with trimesh2

## Build Instructions

RTSC uses CMake for cross-platform builds.

```bash
git clone https://github.com/csv610/SuggestiveContours.git
cd SuggestiveContours
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
cmake --build . -j$(nproc)
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

### Keyboard Shortcuts
| Key | Action |
|-----|--------|
| `c` | Toggle mesh colors |
| `C` | Filter curvature |
| `d` | Toggle occluding contours |
| `D` | Toggle suggestive contours |
| `s` | Filter normals |
| `S` | Filter mesh (smoothing) |
| `r` | Toggle principal highlights |
| `R` | Toggle ridges/valleys test |
| `a` | Toggle asymptotic lines |
| `A` | Toggle apparent ridges |
| `n` | Toggle normals rendering |
| `f` | Toggle faded lines |
| `l` | Cycle lighting style |
| `u` | Cycle color style |
| `t` | Toggle texture |
| `+` / `-` | Increase/decrease isolines |
| `z` / `Z` | Decrease/increase FOV |
| `x` | Save camera position |
| `i` | Dump image to file |
| `/` | Toggle dual viewport mode |

Click the **Options** button in the UI to toggle different line types and adjust thresholds.

## Testing

A basic test script is provided in the `tests` directory:

```bash
python3 tests/test_basic.py
```

## CI Status

| Platform | Status |
|----------|--------|
| macOS (clang, gcc) | ✅ |
| Ubuntu (clang, gcc) | ✅ |

GitHub Actions runs on every push:
- Build verification on macOS and Ubuntu
- Code style check with clang-format
- Zero compiler warnings

## Modern Context

While RTSC (2004) is older, it remains relevant and actively cited:

- **Baseline**: New papers (Neural Contours 2019, Diff3DS 2025) compare against it
- **Educational**: Best entry point for understanding geometric line drawing
- **Lightweight**: No ML framework - runs anywhere
- **Precise**: Full control over thresholds

| Modern Work | Builds On |
|------------|----------|
| Neural Contours (2019) | Uses rtsc as geometric branch |
| Diff3DS (ICLR 2025) | Differentiable rendering from suggestions |
| Deep Sketch Vectorization (2024) | Raster → vector via neural networks |

For modern ML-based approaches, see:
- [Neural Contours](https://github.com/DifanLiu/NeuralContours) (2019)
- [Diff3DS](https://arxiv.org/abs/2501.04656) (ICLR 2025)

## Key Algorithms

The features in RTSC are based on several seminal papers in computer graphics:
- *Suggestive Contours for Conveying Shape* (SIGGRAPH 2003)
- *Interactive Rendering of Suggestive Contours with Temporal Coherence* (NPAR 2004)
- *Highlight Lines for Conveying Shape* (NPAR 2007)
- *Apparent Ridges for Line Drawing* (SIGGRAPH 2007)

## License

This software is distributed under the GNU General Public License (GPL). See the `LICENSE` file for details.

## Authors

Szymon Rusinkiewicz and Doug DeCarlo.