# Real-Time Suggestive Contours (RTSC)
## User Guide

---

# Chapter 1: Introduction

## 1.1 Overview

This software implements real-time algorithms for computing various types of expressive lines on 3D meshes, including contours, suggestive contours, ridges, valleys, apparent ridges, and principal highlights. The system achieves interactive performance through GPU-accelerated rendering and efficient computational geometry techniques.

## 1.2 Mathematical Foundations

### 1.2.1 Surface Representation

Let $M$ be a triangulated surface mesh consisting of vertices $V = \{v_1, v_2, \ldots, v_n\}$ and faces $F$. Each vertex $v_i \in \mathbb{R}^3$ has associated differential geometric properties:

- **Normal vector**: $\mathbf{n}_i \in \mathbb{R}^3$, unit length
- **Principal curvatures**: $\kappa_1(v_i), \kappa_2(v_i)$ (maximum and minimum)
- **Principal directions**: $\mathbf{p}_1(v_i), \mathbf{p}_2(v_i) \in \mathbb{R}^3$
- **Curvature derivative**: $\mathbf{D}\kappa_1(v_i), \mathbf{D}\kappa_2(v_i)$

### 1.2.2 Curvature Computation

Principal curvatures $\kappa_1$ and $\kappa_2$ are computed by analyzing the tensor of the second fundamental form. For a vertex $v$, the Weingarten map $d\mathbf{N}: T_pM \to T_pM$ relates principal curvatures to principal directions through:

$$d\mathbf{N}(\mathbf{p}_1) = -\kappa_1 \mathbf{p}_1, \quad d\mathbf{N}(\mathbf{p}_2) = -\kappa_2 \mathbf{p}_2$$

The mean curvature is $H = \frac{1}{2}(\kappa_1 + \kappa_2)$, and Gaussian curvature is $K = \kappa_1 \kappa_2$.

---

# Chapter 2: Line Drawing Algorithms

## 2.1 Occluding Contours

### 2.1.1 Definition

An **occluding contour** (also called a silhouette) is defined as the set of points where the surface normal is perpendicular to the view direction:

$$\mathcal{C} = \{p \in M : \mathbf{n}(p) \cdot \mathbf{v}(p) = 0\}$$

where $\mathbf{v}(p)$ is the unit view vector from point $p$ to the camera.

### 2.1.2 Implementation

The algorithm computes $\mathbf{n} \cdot \mathbf{v}$ at each vertex and renders zero-crossings using linear or Hermite interpolation across triangle edges. The rendering pass applies front-face culling based on $\mathbf{n} \cdot \mathbf{v} > 0$.

### 2.1.3 Rendering Parameters

| Parameter | Description | Default |
|----------|------------|---------|
| `draw_c` | Enable contour rendering | on |
| `test_c` | Apply inside/outside test | on |
| Line width | In pixels | 2.5 |

## 2.2 Suggestive Contours

### 2.2.1 Definition

**Suggestive contours** are curves that are not visible in the current view but would become contours under a small change in viewpoint. They are defined as extrema (with respect to view direction) of the radial curvature $K_r$:

$$K_r = \kappa_1 \sin^2\theta_1 + \kappa_2 \sin^2\theta_2$$

where $\theta_1$ and $\theta_2$ are the angles between the view direction and the principal directions $\mathbf{p}_1, \mathbf{p}_2$.

### 2.2.2 Mathematical Derivation

The condition for a suggestive contour is $K_r = 0$. However, to ensure the curve would appear as a contour under a small view change, the algorithm tests whether the derivative of $K_r$ in the view direction has a non-zero extremum:

$$\frac{\partial K_r}{\partial w} = 0$$

This yields the **cutoff test**:

$$D_{w}K_r \cdot \sin\theta - 2K_r \cdot \frac{\partial}{\partial w}(\sin\theta)\cos\theta > \epsilon$$

For implementation efficiency, this simplifies to:

$$D_w K_r \cdot \sin\theta - 2K_r \cdot (\kappa_1 - \kappa_2) \sin\theta\cos\theta > \epsilon$$

### 2.2.3 Rendering Parameters

| Parameter | Description | Default |
|----------|------------|---------|
| `draw_sc` | Enable SC rendering | on |
| `test_sc` | Apply cutoff test | on |
| `sug_thresh` | Test threshold $\epsilon$ | 0.01 |
| `use_hermite` | Use Hermite interpolation | off |
| `draw_faded` | Fade lines by strength | on |

### 2.2.4 Threshold Adjustment

The suggestive contour threshold `sug_thresh` controls the strength of the cutoff test:

- **Increase** (press `9`): More restrictive, fewer lines
- **Decrease** (press `0`): Less restrictive, more lines

The threshold is automatically scaled by the **feature size** $\tau$, computed as $\tau = 0.01 / \kappa_{10}$, where $\kappa_{10}$ is the 10th percentile of absolute curvature values.

## 2.3 Ridges and Valleys

### 2.3.1 Definition

**Ridges** are loci of local maximum principal curvature $\kappa_1$, and **valleys** are loci of local minimum principal curvature $\kappa_2$. Formally:

- Ridge: $\{p \in M : \kappa_1(p) = \max, \nabla_T \kappa_1 = 0\}$
- Valley: $\{p \in M : \kappa_2(p) = \min, \nabla_T \kappa_2 = 0\}$

where $\nabla_T$ denotes the surface gradient (tangent to the mesh).

### 2.3.2 Detection Algorithm

The algorithm (based on Ohtake et al., 2004) identifies ridges via:

1. **Curvature sign test**: $\kappa_1 > 0$ for ridges
2. **Extremum test**: The directional derivative of $\kappa_1$ in the principal direction $\mathbf{p}_1$ changes sign across the ridge

Specifically, a ridge exists on edge $v_i v_j$ if:

$$\mathbf{t}_{max}(v_i) \cdot \mathbf{t}_{max}(v_j) < 0 \quad \text{and} \quad \mathbf{t}_{max} \cdot \mathbf{e}_{ij} \text{ has consistent direction}$$

where $\mathbf{t}_{max} = \mathbf{D}\kappa_1 \cdot \mathbf{p}_1$ (direction of maximum curvature increase) and $\mathbf{e}_{ij} = v_j - v_i$.

### 2.3.3 Rendering Parameters

| Parameter | Description | Default |
|----------|------------|---------|
| `draw_ridges` | Enable ridge rendering | off |
| `draw_valleys` | Enable valley rendering | off |
| `test_rv` | Apply extremum test | on |
| `rv_thresh` | Curvature threshold | 0.1 |

## 2.4 Apparent Ridges

### 2.4.1 Definition

**Apparent ridges** (Judd et al., 2007) are defined相对于 the viewer and address the limitation that true ridges may face away from the viewer and thus be poorly visible. They are defined as extrema of **view-dependent curvature** $q_1$:

$$q_1 = \kappa_1^{vd} = \max_{\mathbf{t}} \kappa(\mathbf{t})$$

where the maximum is taken over all directions in the tangent plane, weighted by view angle.

### 2.4.2 View-Dependent Curvature

For a view direction $\mathbf{v}$ making angle $\theta$ with the surface normal, the view-dependent curvature in direction $\mathbf{t}$ is:

$$\kappa_{vd}(\mathbf{t}) = \kappa_1 \sin^2\phi_1 + \kappa_2 sin^2\phi_2$$

where $\phi_i$ is the angle between $\mathbf{t}$ and $\mathbf{p}_i$ projected into the tangent plane.

### 2.4.3 Implementation

The algorithm computes per-vertex:
- $q_1$: maximum view-dependent curvature
- $\mathbf{t}_1$: direction in which $q_1$ attains maximum
- $D_{\mathbf{t}_1}q_1$: derivative in direction $\mathbf{t}_1$

An apparent ridge is drawn where $q_1 = 0$ with $D_{\mathbf{t}_1}q_1 > 0$.

### 2.4.4 Rendering Parameters

| Parameter | Description | Default |
|----------|------------|---------|
| `draw_apparent` | Enable apparent ridges | off |
| `test_ar` | Apply derivative test | on |
| `ar_thresh` | Curvature threshold | 0.1 |

## 2.5 Principal Highlights

### 2.5.1 Definition

**Principal highlights** are lines where the surface reflects light maximally toward the viewer—the peaks of specular reflection. They occur where the view and light directions are symmetric with respect to the surface normal, projected onto the principal directions.

### 2.5.2 Mathematical Condition

For principal highlight (ridge case):

$$\mathbf{r} \cdot \mathbf{p}_1 = 0$$

where $\mathbf{r} = \mathbf{l} - (\mathbf{l} \cdot \mathbf{n})\mathbf{n}$ is the reflected light direction projected into the tangent plane.

### 2.5.3 Rendering Parameters

| Parameter | Description | Default |
|----------|------------|---------|
| `draw_phridges` | Enable PH ridges | off |
| `draw_phvalleys` | Enable PH valleys | off |
| `test_ph` | Apply PH test | on |
| `ph_thresh` | PH threshold | 0.04 |

## 2.6 Curvature Zeros

### 2.6.1 Gaussian Curvature Zero ($K = 0$)

The parabolic set consists of points where $K = \kappa_1 \kappa_2 = 0$. These mark transitions between elliptic ($\kappa_1\kappa_2 > 0$) and hyperbolic ($\kappa_1\kappa_2 < 0$) regions.

### 2.6.2 Mean Curvature Zero ($H = 0$)

The minimal surface condition $H = \frac{1}{2}(\kappa_1 + \kappa_2) = 0$ marks points where the surface is locally minimal (saddle points have $H = 0$ if $\kappa_1 = -\kappa_2$).

### 2.6.3 Rendering Parameters

| Parameter | Description | Default |
|----------|------------|---------|
| `draw_K` | Enable $K=0$ lines | off |
| `draw_H` | Enable $H=0$ lines | off |

---

# Chapter 3: Interactive Controls

## 3.1 Mouse Controls

| Action | Control |
|--------|---------|
| Rotate | Left mouse drag |
| Pan | Middle mouse / Shift+Left |
| Zoom | Right mouse / Scroll |
| Reset view | Spacebar |
| Relight | Ctrl + drag |

## 3.2 Keyboard Commands

### 3.2.1 Line Toggle Commands

| Key | Action |
|-----|-------|
| `d` | Toggle occluding contours |
| `D` | Toggle suggestive contours |
| `r` | Toggle principal highlights (ridges) |
| `v` | Toggle principal highlights (valleys) |
| `Ctrl+r` | Toggle geometric ridges |
| `Ctrl+v` | Toggle geometric valleys |
| `A` | Toggle apparent ridges |
| `K` | Toggle $K=0$ lines |
| `H` | Toggle $H=0$ lines |
| `b` | Toggle mesh boundaries |

### 3.2.2 View Commands

| Key | Action |
|-----|-------|
| `z` | Decrease FOV (zoom in) |
| `Z` | Increase FOV (zoom out) |
| `/` | Toggle dual viewport mode |
| `x` | Save camera position |
| `i` | Save screen capture |

### 3.2.3 Style Commands

| Key | Action |
|-----|-------|
| `c` | Toggle mesh colors |
| `f` | Toggle faded lines |
| `u` | Cycle color style |
| `l` | Cycle lighting style |
| `g` | Toggle Hermite interpolation |
| `t` | Toggle texture mapping |
| `h` | Toggle hidden line rendering |

### 3.2.4 Filtering Commands

| Key | Action |
|-----|-------|
| `S` | Smooth mesh (Laplacian) |
| `s` | Diffuse normals |
| `C` | Diffuse curvatures |
| `X` | Diffuse curvature derivatives |
| `V` | Subdivide mesh (Loop) |

### 3.2.5 Adjustment Commands

| Key | Action |
|-----|-------|
| `9` | Decrease SC threshold |
| `0` | Increase SC threshold |
| `7` | Decrease RV threshold |
| `8` | Increase RV threshold |
| `+` | Increase number of isophotes |
| `-` | Decrease number of isophotes |

### 3.2.6 Quit Commands

| Key | Action |
|-----|-------|
| `q`, `Q` | Exit |
| `Esc` | Exit |

## 3.3 GUI Panel Controls

The GLUI panel provides checkboxes and sliders for all rendering options:

### 3.3.1 Lines Section
- Exterior silhouette
- Occluding contours
- Suggestive contours
- Suggestive highlights
- Principal highlights (ridges/valleys)
- Ridges / Valleys
- Apparent ridges

### 3.3.2 Line Tests Section
- Draw hidden lines
- Trim inside contours threshold
- SC threshold slider
- SH/PH/RV/AR thresholds

### 3.3.3 Line Style Section
- Texture mapping
- Fade lines
- Draw in color
- Hermite interpolation

### 3.3.4 Mesh Style Section
- Color mode: White / Gray / Curvature / Mesh colors
- Draw edges

### 3.3.5 Lighting Section
- Style: None / Lambertian / Hemisphere / Toon / Gooch
- Direction control (rotation widget)

---

# Chapter 4: Algorithm Parameters

## 4.1 Feature Size

The **feature size** $\tau$ is a scale parameter computed from mesh curvature:

$$\tau = \min\left(\frac{0.01}{\kappa_{10}}, 0.05 r_{bsphere}\right)$$

where $\kappa_{10}$ is the 10th percentile of absolute curvature and $r_{bsphere}$ is the bounding sphere radius.

Feature size normalizes all threshold values, making them dimensionless and mesh-independent.

## 4.2 Threshold Scaling

All user-adjustable thresholds are scaled by feature size:

| Parameter | Displayed | Used |
|-----------|-----------|-----|
| `sug_thresh` | 0.01 | $\epsilon / \tau^2$ |
| `sh_thresh` | 0.02 | $\epsilon / \tau^2$ |
| `ph_thresh` | 0.04 | $\epsilon / \tau^2$ |
| `rv_thresh` | 0.1 | $\epsilon / \tau$ |
| `ar_thresh` | 0.1 | $\epsilon / \tau$ |

## 4.3 Interpolation

### 4.3.1 Linear Interpolation

For an edge $v_0 \to v_1$ with scalar field values $f_0, f_1$, the zero-crossing is at parameter:

$$t = \frac{f_0}{f_0 - f_1}$$

### 4.3.2 Hermite Interpolation

Hermite interpolation uses derivative information for smoother line placement. For cubic Hermite:

$$f(t) = h_1(t)f_0 + h_2(t)f_1 + h_3(t)f'_0 + h_4(t)f'_1$$

where basis functions are:
- $h_1(t) = 2t^3 - 3t^2 + 1$
- $h_2(t) = -2t^3 + 3t^2$
- $h_3(t) = t^3 - 2t^2 + t$
- $h_4(t) = t^3 - t^2$

Derivatives are computed via automatic differentiation of the curvature field.

---

# Chapter 5: Mesh Processing

## 5.1 Laplacian Smoothing

Laplacian smoothing replaces each vertex with the average of its neighbors:

$$v_i \leftarrow \frac{1}{|N(i)|}\sum_{j \in N(i)} v_j$$

Iterative application yields exponentially decaying high-frequency geometry.

## 5.2 Normal Smoothing

Diffusing normals maintains sharp features while smoothing the field:

$$n_i \leftarrow \text{normalize}\left(\sum_{j \in N(i)} n_j\right)$$

## 5.3 Curvature Smoothing

Curvature values can be smoothed independently of geometry, allowing cleaner curvature fields while preserving mesh detail.

## 5.4 Loop Subdivision

Loop subdivision increases mesh resolution by splitting each triangle into four and computing new vertices via:

$$v_{new} = \frac{3}{8}v_0 + \frac{3}{8}v_1 + \frac{1}{8}v_2 + \frac{1}{8}v_3$$

for boundary vertices, and beta-scheme weights for interior vertices.

---

# Chapter 6: Lighting Models

## 6.1 Lambertian

$$I = \max(0, \mathbf{n} \cdot \mathbf{l})$$

## 6.2 Hemisphere Lighting

$$I = 0.5 + 0.5(\mathbf{n} \cdot \mathbf{l})$$

## 6.3 Toon Shading

Quantized shading with sharp transitions:
- Hard: 2-level quantization
- Soft: Smooth transition zones

## 6.4 Gooch Shading

Warm-to-cool color ramp:
- Warm: $(0.25, 0.25, 0.35)$ at dark
- Cool: $(0.0, 0.25, 0.55)$ at light

---

# Chapter 7: Input File Formats

## 7.1 Supported Formats

| Format | Description |
|--------|------------|
| `.ply` | Stanford PLY |
| `.obj` | Wavefront OBJ |
| `.off` | OFF |
| `.geom` | Original trimesh2 format |

## 7.2 Expected Properties

On load, the mesh is preprocessed to compute:
- Triangle strips
- Bounding sphere
- Normals
- Curvatures and principal directions
- Curvature derivatives

---

# Chapter 8: Command Line Usage

## 8.1 Syntax

```bash
rtsc [options] input_file
```

## 8.2 Options

| Option | Description |
|--------|------------|
| `-h`, `--help` | Show help message |
| `+W,H,S,P` | Window size and initial thresholds |

## 8.3 Keyboard Shortcuts via Command Line

Any string argument starting with `-` is interpreted as a sequence of keyboard commands:

```bash
rtsc -DSc model.ply  # Enable D, S, c on start
```

---

# Appendix A: Citation

This software implements algorithms from:

1. DeCarlo, Finkelstein, Rusinkiewicz, and Santella. "Suggestive Contours for Conveying Shape." SIGGRAPH 2003.

2. Rusinkiewicz, DeCarlo, and Du. "Interactive Rendering of Suggestive Contours with Temporal Coherence." NPAR 2004.

3. Judd, Durand, and Adelson. "Apparent Ridges for Line Drawing." SIGGRAPH 2007.

4. Ohtake, Belyaev, and Seidel. "Ridge-valley Lines on Meshes via Anisotropic Diffusion." 2004.

---

# Appendix B: References

- DeCarlo, F., Finkelstein, A., Rusinkiewicz, S., and Santella, A. (2003). Suggestive contours for conveying shape. *ACM Trans. Graphics*, 22(3), 848-855.

- Judd, T., Durand, F., and Adelson, E. (2007). Apparent ridges for line drawing. *ACM Trans. Graphics*, 26(3), 19.

- Ohtake, Y., Belyaev, A., and Seidel, H.-P. (2004). Ridge-valley lines on meshes via anisotropic diffusion. *Proc. SGP*, 85-90.

- Rusinkiewicz, S. (2004). *Trimesh2*: A Simple Triangle Mesh Library. Princeton University.