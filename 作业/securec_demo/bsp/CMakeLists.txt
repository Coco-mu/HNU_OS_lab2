# 作业 2：原来的 vsnprintf_s.c 不再参与编译，格式化交给 securec
set(SRCS start.S prt_reset_vector.S print.c
         securec/src/vsnprintf_s.c securec/src/secureprintoutput_a.c
         securec/src/securecutil.c securec/compat/securec_port.c)
add_library(bsp OBJECT ${SRCS})

include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}/securec/include
    ${CMAKE_CURRENT_SOURCE_DIR}/securec/src
    ${CMAKE_CURRENT_SOURCE_DIR}/securec/compat
)
# 裸机上没有 libc：宽字符、浮点格式化、文件相关全部关掉，
# string/stdlib 头用 compat 目录下的桩，实现放在 securec_port.c
target_compile_definitions(bsp PRIVATE
    SECUREC_HAVE_STDIO_H=1
    SECUREC_HAVE_STRING_H=1
    SECUREC_HAVE_STDLIB_H=1
    SECUREC_ENABLE_VSNPRINTF=1
    SECUREC_ENABLE_SPRINTF_FLOAT=0
    SECUREC_ENABLE_SCANF_FILE=0
    SECUREC_HAVE_MBTOWC=0
    SECUREC_HAVE_WCTOMB=0
    SECUREC_HAVE_WCHART=0
    SECUREC_ENABLE_WCHAR_FUNC=0
)
