cmake_minimum_required(VERSION 3.10)
project(trimesh2 VERSION 2.1.0)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include_directories(include)

if(APPLE)
    add_definitions(-DGL_SILENCE_DEPRECATION)
    add_definitions(-DDARWIN)
    set(OPENGL_LIBS "-framework OpenGL" "-framework GLUT")
    set(DONT_BUILD_FREEGLUT ON)
else()
    find_package(OpenGL REQUIRED)
    find_package(GLUT REQUIRED)
    include_directories(${OPENGL_INCLUDE_DIR} ${GLUT_INCLUDE_DIR})
    set(OPENGL_LIBS ${OPENGL_LIBRARIES} ${GLUT_LIBRARIES})
endif()

# trimesh library
set(TRIMESH_SOURCES
    libsrc/TriMesh_bounding.cc
    libsrc/TriMesh_connectivity.cc
    libsrc/TriMesh_curvature.cc
    libsrc/TriMesh_io.cc
    libsrc/TriMesh_grid.cc
    libsrc/TriMesh_normals.cc
    libsrc/TriMesh_pointareas.cc
    libsrc/TriMesh_stats.cc
    libsrc/TriMesh_tstrips.cc
    libsrc/GLCamera.cc
    libsrc/GLManager.cc
    libsrc/ICP.cc
    libsrc/KDtree.cc
    libsrc/conn_comps.cc
    libsrc/diffuse.cc
    libsrc/edgeflip.cc
    libsrc/faceflip.cc
    libsrc/filter.cc
    libsrc/make.cc
    libsrc/merge.cc
    libsrc/overlap.cc
    libsrc/remove.cc
    libsrc/reorder_verts.cc
    libsrc/subdiv.cc
    libsrc/umbrella.cc
)

add_library(trimesh STATIC ${TRIMESH_SOURCES})

# gluit library
set(GLUIT_SOURCES
    gluit/glui.cc
    gluit/glui_add_controls.cc
    gluit/glui_algebra3.cc
    gluit/glui_arcball.cc
    gluit/glui_bitmap_img_data.cc
    gluit/glui_bitmaps.cc
    gluit/glui_button.cc
    gluit/glui_checkbox.cc
    gluit/glui_column.cc
    gluit/glui_control.cc
    gluit/glui_edittext.cc
    gluit/glui_listbox.cc
    gluit/glui_mouse_iaction.cc
    gluit/glui_node.cc
    gluit/glui_panel.cc
    gluit/glui_quaternion.cc
    gluit/glui_radio.cc
    gluit/glui_rollout.cc
    gluit/glui_rotation.cc
    gluit/glui_separator.cc
    gluit/glui_slider.cc
    gluit/glui_spinner.cc
    gluit/glui_statictext.cc
    gluit/glui_translation.cc
)

if(NOT DONT_BUILD_FREEGLUT)
    # If not Apple, you might need freeglut.
    # But since we're targeted at what we need, I'll keep it simple for now.
endif()

add_library(gluit STATIC ${GLUIT_SOURCES})
target_include_directories(gluit PRIVATE include/GL)
