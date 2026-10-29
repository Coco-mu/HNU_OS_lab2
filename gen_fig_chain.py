# -*- coding: utf-8 -*-
"""实验二 图 2-9：PRT_Printf 到 UARTDR 的完整调用链（基础 FIFO 版本）。
两列蛇形排布：左列 1~4，右列 5~7；箭头从左列末节点右侧绕到右列首节点。
画布 760 宽，插进 14 cm 的正文栏时正文约 6.8 pt。
"""

W, H = 760, 494
BLUE = '#1F5FA8'
DARK = '#1B1B1B'
GREY = '#5A6672'
LINE = '#D5DBE2'

NODES = [
    ('PRT_Printf(fmt, ...)', '入口：收格式串和参数', '#EAF2FB'),
    ('TryPrintf', '准备 512 字节缓冲区', '#FFF6E5'),
    ('vsnprintf_s(buf, fmt, ap)', '按 %d %s %x 拼字符串', '#EAF2FB'),
    ('TryPutc(ch)', '逐字符送出，换行补回车', '#EAF2FB'),
    ('uart_poll_send(ch)', '轮询等待，直到能发', '#FFF6E5'),
    ('uart_is_txfifo_full', '读 UARTFR，取 TXFF 位', '#E7F4EA'),
    ('写 UARTDR（0x09000000）', '字节进发送器，串口打出', '#1F5FA8'),
]

BOX_H = 60
GAP = 20
TOP = 88
COL_X = (46, 404)
BOX_W = 306
COL_N = 4            # 左列 4 个节点


def box(i, x, y, out):
    title, note, fill = NODES[i]
    last = (i == len(NODES) - 1)
    tcol = '#FFFFFF' if last else DARK
    ncol = '#D8E6F6' if last else GREY
    out.append('<rect x="%d" y="%d" width="%d" height="%d" rx="7" fill="%s" '
               'stroke="%s" stroke-width="1.4"/>'
               % (x, y, BOX_W, BOX_H, fill, BLUE))
    out.append('<text x="%d" y="%d" font-size="16" fill="%s" font-weight="600">%s</text>'
               % (x + 15, y + 25, tcol, title))
    out.append('<text x="%d" y="%d" font-size="13" fill="%s">%s</text>'
               % (x + 15, y + 46, ncol, note))


def main():
    out = []
    out.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
               'viewBox="0 0 %d %d">' % (W, H, W, H))
    out.append('<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" '
               'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
               '<path d="M 0 0 L 10 5 L 0 10 z" fill="#4A5568"/></marker></defs>')
    out.append('<g font-family="\'PingFang SC\',\'Hiragino Sans GB\','
               '\'Microsoft YaHei\',sans-serif">')
    out.append('<rect x="0" y="0" width="%d" height="%d" fill="#FFFFFF"/>' % (W, H))

    # 标题
    out.append('<rect x="20" y="22" width="4" height="17" fill="%s"/>' % BLUE)
    out.append('<text x="31" y="36" font-size="17" fill="%s" font-weight="600">'
               'PRT_Printf 到 UARTDR 的完整调用链</text>' % DARK)
    out.append('<text x="31" y="56" font-size="12.5" fill="%s">'
               '一次格式化输出，从函数调用一路走到串口寄存器</text>' % GREY)
    out.append('<line x1="20" y1="68" x2="%d" y2="68" stroke="%s" stroke-width="1"/>'
               % (W - 20, LINE))

    # 左列 1~4
    for i in range(COL_N):
        y = TOP + i * (BOX_H + GAP)
        box(i, COL_X[0], y, out)
        if i < COL_N - 1:
            cx = COL_X[0] + BOX_W // 2
            out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#4A5568" '
                       'stroke-width="1.5" marker-end="url(#ar)"/>'
                       % (cx, y + BOX_H, cx, y + BOX_H + GAP - 2))

    # 右列 5~7
    for i in range(COL_N, len(NODES)):
        y = TOP + (i - COL_N) * (BOX_H + GAP)
        box(i, COL_X[1], y, out)
        if i < len(NODES) - 1:
            cx = COL_X[1] + BOX_W // 2
            out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#4A5568" '
                       'stroke-width="1.5" marker-end="url(#ar)"/>'
                       % (cx, y + BOX_H, cx, y + BOX_H + GAP - 2))

    # 左列末节点 → 右列首节点：右侧 → 上折 → 进右列顶部
    y4 = TOP + (COL_N - 1) * (BOX_H + GAP) + BOX_H // 2
    y5 = TOP + BOX_H // 2
    mid = (COL_X[0] + BOX_W + COL_X[1]) // 2
    out.append('<polyline points="%d,%d %d,%d %d,%d %d,%d" fill="none" '
               'stroke="#4A5568" stroke-width="1.5" marker-end="url(#ar)"/>'
               % (COL_X[0] + BOX_W, y4, mid, y4, mid, y5, COL_X[1] - 2, y5))

    # 底部说明条
    by = TOP + COL_N * (BOX_H + GAP) + 4
    out.append('<rect x="20" y="%d" width="%d" height="64" rx="7" fill="#F7F9FB" '
               'stroke="%s" stroke-width="1"/>' % (by, W - 40, LINE))
    tips = [
        '基础版：开 FIFO，等 TXFF（bit5）清零再写 UARTDR。',
        '作业 1：关 FIFO，改等 TXFE（bit7）置 1 再写。两版只差这一个判据。',
    ]
    for i, t in enumerate(tips):
        out.append('<text x="38" y="%d" font-size="13" fill="#2D3748">%s</text>'
                   % (by + 26 + i * 23, t))

    out.append('</g></svg>')

    path = '实验截图/示意图_Printf到UARTDR调用链.svg'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(''.join(out))
    print('已写', path)


if __name__ == '__main__':
    main()
