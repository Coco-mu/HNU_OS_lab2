cmake_minimum_required(VERSION 3.12)

set(CMAKE_SYSTEM_NAME "Generic")
set(CMAKE_SYSTEM_PROCESSOR "aarch64")
set(CMAKE_TRY_COMPILE_TARGET_TYPE STATIC_LIBRARY)

find_program(TOOLCHAIN_CC NAMES aarch64-none-elf-gcc aarch64-elf-gcc)
if(NOT TOOLCHAIN_CC)
    message(FATAL_ERROR "AArch64 bare-metal GCC was not found on PATH")
endif()
get_filename_component(TOOLCHAIN_BIN "${TOOLCHAIN_CC}" DIRECTORY)
find_program(TOOLCHAIN_CXX NAMES aarch64-none-elf-g++ aarch64-elf-g++ HINTS "${TOOLCHAIN_BIN}")
find_program(TOOLCHAIN_LD NAMES aarch64-none-elf-ld aarch64-elf-ld HINTS "${TOOLCHAIN_BIN}")
set(CMAKE_C_COMPILER "${TOOLCHAIN_CC}")
set(CMAKE_CXX_COMPILER "${TOOLCHAIN_CXX}")
set(CMAKE_ASM_COMPILER "${TOOLCHAIN_CC}")
set(CMAKE_LINKER "${TOOLCHAIN_LD}")

set(CC_OPTION "-Os -Wformat-signedness -Wl,--build-id=none -fno-PIE -fno-PIE -fno-builtin -fno-dwarf2-cfi-asm -fomit-frame-pointer -fzero-initialized-in-bss -fdollars-in-identifiers -ffunction-sections -fdata-sections -fno-aggressive-loop-optimizations -fno-optimize-strlen -fno-schedule-insns -fno-inline-small-functions -fno-inline-functions-called-once -fno-strict-aliasing -finline-limit=20 -mlittle-endian -nostartfiles -funwind-tables")
set(AS_OPTION "${CC_OPTION}")
set(LD_OPTION "")
set(CMAKE_C_FLAGS "${CC_OPTION}")
set(CMAKE_ASM_FLAGS "${AS_OPTION}")
set(CMAKE_LINK_FLAGS "${LD_OPTION} -T ${CMAKE_CURRENT_SOURCE_DIR}/aarch64-qemu.ld")
set(CMAKE_EXE_LINKER_FLAGS "${LD_OPTION} -T ${CMAKE_CURRENT_SOURCE_DIR}/aarch64-qemu.ld -nostdlib")
set(CMAKE_C_LINK_FLAGS "")
set(CMAKE_CXX_LINK_FLAGS "")

set(HOME_PATH ${CMAKE_CURRENT_SOURCE_DIR})
set(APP "miniEuler")
project(${APP} LANGUAGES C ASM)
set(CMAKE_BUILD_TYPE Debug)

include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}/include
    ${CMAKE_CURRENT_SOURCE_DIR}/bsp
)

add_subdirectory(bsp)
list(APPEND OBJS $<TARGET_OBJECTS:bsp>)
add_executable(${APP} main.c ${OBJS})
