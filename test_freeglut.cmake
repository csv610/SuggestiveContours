find_package(FreeGLUT QUIET)
if(FreeGLUT_FOUND)
    message("FreeGLUT found: ${FreeGLUT_LIBRARIES}")
    message("FreeGLUT include: ${FreeGLUT_INCLUDE_DIRS}")
else()
    message("FreeGLUT NOT found")
endif()

