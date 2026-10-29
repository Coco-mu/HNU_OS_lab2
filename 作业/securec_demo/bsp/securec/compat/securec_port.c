#include <stddef.h>

/*
 * 裸机上没有 libc，libboundscheck（securec）依赖的这几个函数在这里补上。
 * 全部用最简单的循环实现，不依赖任何库，也不让编译器替换成内建版本。
 */

void *memcpy(void *dst, const void *src, size_t n)
{
    unsigned char *d = (unsigned char *)dst;
    const unsigned char *s = (const unsigned char *)src;

    while (n--) {
        *d++ = *s++;
    }
    return dst;
}

void *memset(void *dst, int c, size_t n)
{
    unsigned char *d = (unsigned char *)dst;

    while (n--) {
        *d++ = (unsigned char)c;
    }
    return dst;
}

void *memmove(void *dst, const void *src, size_t n)
{
    unsigned char *d = (unsigned char *)dst;
    const unsigned char *s = (const unsigned char *)src;

    if (d == s || n == 0) {
        return dst;
    }
    if (d < s) {
        while (n--) {
            *d++ = *s++;
        }
    } else {
        d += n;
        s += n;
        while (n--) {
            *--d = *--s;
        }
    }
    return dst;
}

size_t strlen(const char *s)
{
    const char *p = s;

    while (*p != '\0') {
        p++;
    }
    return (size_t)(p - s);
}

size_t strnlen(const char *s, size_t maxlen)
{
    size_t n = 0;

    while (n < maxlen && s[n] != '\0') {
        n++;
    }
    return n;
}

/* securec 内部会读写 errno 判断参数是否非法 */
int errno = 0;
