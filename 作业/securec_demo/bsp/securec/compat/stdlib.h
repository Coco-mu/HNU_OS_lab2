#ifndef SECUREC_COMPAT_STDLIB_H
#define SECUREC_COMPAT_STDLIB_H
/* 裸机上没有堆，securec 用不到 malloc，这里只放个空壳防止头文件互相引用报错 */
#include <stddef.h>
#endif
