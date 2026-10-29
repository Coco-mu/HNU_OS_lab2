#ifndef SECUREC_COMPAT_STRING_H
#define SECUREC_COMPAT_STRING_H
/*
 * 裸机没有 libc 的 string.h。这里只声明 securec 用到的那几个函数，
 * 实现放在 securec_port.c 里（手写循环，不依赖任何库）。
 */
#include <stddef.h>

void *memcpy(void *dst, const void *src, size_t n);
void *memset(void *dst, int c, size_t n);
void *memmove(void *dst, const void *src, size_t n);
size_t strlen(const char *s);
size_t strnlen(const char *s, size_t maxlen);
#endif
