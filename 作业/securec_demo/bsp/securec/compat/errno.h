#ifndef SECUREC_COMPAT_ERRNO_H
#define SECUREC_COMPAT_ERRNO_H
/* 裸机上没有 libc 的 errno，这里给一个最小实现 */
extern int errno;
#define EOK 0
#define EINVAL 22
#define ERANGE 34
#define ENOMEM 12
#endif
