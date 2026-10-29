#ifndef SECUREC_COMPAT_STDIO_H
#define SECUREC_COMPAT_STDIO_H
#include <stddef.h>
/* securec 头文件只用到 FILE 这个类型名，裸机上给个空壳 */
typedef struct _securec_stub_FILE FILE;
#endif
