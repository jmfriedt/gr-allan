find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_ALLAN gnuradio-allan)

FIND_PATH(
    GR_ALLAN_INCLUDE_DIRS
    NAMES gnuradio/allan/api.h
    HINTS $ENV{ALLAN_DIR}/include
        ${PC_ALLAN_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_ALLAN_LIBRARIES
    NAMES gnuradio-allan
    HINTS $ENV{ALLAN_DIR}/lib
        ${PC_ALLAN_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-allanTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_ALLAN DEFAULT_MSG GR_ALLAN_LIBRARIES GR_ALLAN_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_ALLAN_LIBRARIES GR_ALLAN_INCLUDE_DIRS)
