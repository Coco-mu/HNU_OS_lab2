#include <stdarg.h>
#include "prt_typedef.h"

#define UART_0_REG_BASE 0x09000000 // pl011 设备寄存器地址
// 寄存器及其位定义参见：https://developer.arm.com/documentation/ddi0183/g/programmers-model/summary-of-registers
#define DW_UART_THR 0x00 // UARTDR(Data Register) 寄存器
#define DW_UART_FR 0x18  // UARTFR(Flag Register) 寄存器
#define DW_UART_LCR_HR 0x2c  // UARTLCR_H(Line Control Register) 寄存器
#define DW_XFIFO_NOT_FULL 0x020  // 发送缓冲区满置位
#define DW_FIFO_ENABLE 0x10 // 启用发送和接收FIFO

#define UART_BUSY_TIMEOUT   1000000
#define OS_MAX_SHOW_LEN 0x200


#define UART_REG_READ(addr)          (*(volatile U32 *)(((uintptr_t)addr)))  // 读设备寄存器
#define UART_REG_WRITE(value, addr)  (*(volatile U32 *)((uintptr_t)addr) = (U32)value) // 写设备寄存器

U32 PRT_UartInit(void)
{
    U32 result = 0;
    U32 reg_base = UART_0_REG_BASE;
    // LCR寄存器： https://developer.arm.com/documentation/ddi0183/g/programmers-model/register-descriptions/line-control-register--uartlcr-h?lang=en
    result = UART_REG_READ((unsigned long)(reg_base + DW_UART_LCR_HR));
    UART_REG_WRITE(result | DW_FIFO_ENABLE, (unsigned long)(reg_base + DW_UART_LCR_HR)); // 启用 FIFO

    return OS_OK;
}

// 读 reg_base + offset 寄存器的值。 uartno 参数未使用
S32 uart_reg_read(S32 uartno, U32 offset, U32 *val)
{
    U32 reg_base = UART_0_REG_BASE;
    (void)uartno;
    if (val == 0) {
        return -1;
    }
    *val = UART_REG_READ((unsigned long)(reg_base + offset));
    return OS_OK;
}

// 通过检查 FR 寄存器的 TXFF 标志确定发送 FIFO 是否已满。
S32 uart_is_txfifo_full(S32 uartno)
{
    U32 usr = 0;

    if (uart_reg_read(uartno, DW_UART_FR, &usr) != OS_OK) {
        return 1;
    }
    return (usr & DW_XFIFO_NOT_FULL) != 0;
}

// 往 reg_base + offset 寄存器中写入值 val。
void uart_reg_write(S32 uartno, U32 offset, U32 val)
{
    U32 reg_base = UART_0_REG_BASE;
    (void)uartno;
    UART_REG_WRITE(val, (unsigned long)(reg_base + offset));
    return;
}

// 通过轮询的方式发送字符到串口
void uart_poll_send(unsigned char ch)
{

    S32 timeout = 0;
    S32 max_timeout = UART_BUSY_TIMEOUT;

    // 轮询发送缓冲区是否满
    int result = uart_is_txfifo_full(0);
    while (result) {
        timeout++;
        if (timeout >= max_timeout) {
            return;
        }
        result = uart_is_txfifo_full(0);
    }

    // 如果缓冲区没满，通过往数据寄存器写入数据发送字符到串口
    uart_reg_write(0, DW_UART_THR, (U32)(U8)ch);
    return;
}

// 轮询的方式发送字符到串口，且转义换行符
void TryPutc(unsigned char ch)
{
    uart_poll_send(ch);
    if (ch == '\n') {
        uart_poll_send('\r');
    }
}

extern int  vsnprintf_s(char *buff, int buff_size, int count, char const *fmt, va_list arg);
int TryPrintf(const char *format, va_list vaList)
{
    int len;
    char buff[OS_MAX_SHOW_LEN];
    for (int i = 0; i < OS_MAX_SHOW_LEN; i++) {
        buff[i] = 0;
    }
    char *str = buff;

    len = vsnprintf_s(buff, OS_MAX_SHOW_LEN, OS_MAX_SHOW_LEN, format, vaList);
    if (len == -1) {
        return len;
    }

    while (*str != '\0') {
        TryPutc(*str);
        str++;
    }

    return (S32)len;
}

U32 PRT_Printf(const char *format, ...)
{
    va_list vaList;
    S32 count;

    va_start(vaList, format);
    count = TryPrintf(format, vaList);
    va_end(vaList);

    return count;
}
