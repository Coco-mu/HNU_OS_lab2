#!/bin/sh
# 作业 2：用 libboundscheck（securec）替换手写 vsnprintf_s 后的构建脚本
set -e
rm -rf build
mkdir -p build
cd build
cmake ..
cmake --build .
