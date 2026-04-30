cmake_minimum_required(VERSION 3.15)
project(rtsc CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Point to trimesh2
set(TRIMESHDIR "${CMAKE_CURRENT_SOURCE_DIR}/trimesh2")

# Modern compiler warnings
if(MSVC)
    add_compile_options(/W4 /permissive-)
    add_definitions(-D_CRT_SECURE_NO_WARNINGS)
else()
    add_compile_options(-Wall -Wextra -Wpedantic)
    add_compile_options(
        -Wno-deprecated-declarations
        -Wno-unused-parameter
        -Wno-format-pedantic
        -Wno-gnu-anonymous-struct
        -Wno-nested-anon-types
        -Wno-keyword-macro
        -Wno-c++17-attribute-extensions
        -Wno-unused-but-set-variable
    )
endif()

# Add trimesh2 as a subdirectory
add_subdirectory(${TRIMESHDIR})

# Platform specific settings
if(APPLE)
    add_definitions(-DGL_SILENCE_DEPRECATION)
    add_definitions(-DDARWIN)
    
    # Prefer native GLUT on macOS to avoid X11 dependency from Homebrew FreeGLUT
    message(STATUS "Root: Using native GLUT framework")
    set(OPENGL_LIBS "-framework OpenGL" "-framework GLUT" "-framework Cocoa")
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

# rtsc sources
set(SOURCES
    src/rtsc.cc
    src/apparentridge.cc
)

set(HEADERS
    src/apparentridge.h
)

add_executable(rtsc ${SOURCES} ${HEADERS})

# Include directories
target_include_directories(rtsc PRIVATE 
    ${TRIMESHDIR}/include
    src
    .
)

# Link libraries
# trimesh and gluit are targets from the trimesh2 subdirectory
target_link_libraries(rtsc
    PRIVATE
    trimesh
    gluit
    ${OPENGL_LIBS}
)

if(WIN32)
    add_definitions(-DWin32)
    target_link_libraries(rtsc PRIVATE -mwindows)
endif()
