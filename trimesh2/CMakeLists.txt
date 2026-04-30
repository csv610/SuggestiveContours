cmake_minimum_required(VERSION 3.10)
project(trimesh2 VERSION 2.16)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include_directories(include)

if(APPLE)
    add_definitions(-DGL_SILENCE_DEPRECATION)
    add_definitions(-DDARWIN)
    
    # Prefer native GLUT on macOS to avoid X11 dependency from Homebrew FreeGLUT
    message(STATUS "Using native GLUT framework")
    set(OPENGL_LIBS "-framework OpenGL" "-framework GLUT")
    set(DONT_BUILD_FREEGLUT ON)
else()
    find_package(FreeGLUT QUIET)
    if(FreeGLUT_FOUND)
        include_directories(${FreeGLUT_INCLUDE_DIRS})
        set(OPENGL_LIBS OpenGL::GL ${FreeGLUT_LIBRARIES})
    else()
        find_package(OpenGL REQUIRED)
        find_package(GLUT REQUIRED)
        include_directories(${OPENGL_INCLUDE_DIR} ${GLUT_INCLUDE_DIR})
        set(OPENGL_LIBS ${OPENGL_LIBRARIES} ${GLUT_LIBRARIES})
    endif()
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
    gluit/algebra3.cpp
    gluit/arcball.cpp
    gluit/glui_add_controls.cpp
    gluit/glui_bitmaps.cpp
    gluit/glui_button.cpp
    gluit/glui_checkbox.cpp
    gluit/glui_column.cpp
    gluit/glui_commandline.cpp
    gluit/glui_control.cpp
    gluit/glui_edittext.cpp
    gluit/glui_filebrowser.cpp
    gluit/glui_list.cpp
    gluit/glui_listbox.cpp
    gluit/glui_mouse_iaction.cpp
    gluit/glui_node.cpp
    gluit/glui_panel.cpp
    gluit/glui_radio.cpp
    gluit/glui_rollout.cpp
    gluit/glui_rotation.cpp
    gluit/glui_scrollbar.cpp
    gluit/glui_separator.cpp
    gluit/glui_spinner.cpp
    gluit/glui_statictext.cpp
    gluit/glui_textbox.cpp
    gluit/glui_translation.cpp
    gluit/glui_tree.cpp
    gluit/glui_treepanel.cpp
    gluit/glui_window.cpp
    gluit/glui.cpp
    gluit/quaternion.cpp
    gluit/viewmodel.cpp
    # Images
    gluit/glui_img_checkbox_0_dis.c
    gluit/glui_img_checkbox_0.c
    gluit/glui_img_checkbox_1_dis.c
    gluit/glui_img_checkbox_1.c
    gluit/glui_img_downarrow.c
    gluit/glui_img_leftarrow.c
    gluit/glui_img_listbox_down.c
    gluit/glui_img_listbox_up_dis.c
    gluit/glui_img_listbox_up.c
    gluit/glui_img_radiobutton_0_dis.c
    gluit/glui_img_radiobutton_0.c
    gluit/glui_img_radiobutton_1_dis.c
    gluit/glui_img_radiobutton_1.c
    gluit/glui_img_rightarrow.c
    gluit/glui_img_spindown_0.c
    gluit/glui_img_spindown_1.c
    gluit/glui_img_spindown_dis.c
    gluit/glui_img_spinup_0.c
    gluit/glui_img_spinup_1.c
    gluit/glui_img_spinup_dis.c
    gluit/glui_img_uparrow.c
)

if(NOT DONT_BUILD_FREEGLUT)
    # If not Apple, you might need freeglut.
    # But since we're targeted at what we need, I'll keep it simple for now.
endif()

add_library(gluit STATIC ${GLUIT_SOURCES})
target_include_directories(gluit PRIVATE include/GL)
