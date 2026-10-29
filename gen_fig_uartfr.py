# -*- coding: utf-8 -*-
"""实验二 图 2-19：UARTFR 低 8 位与两个版本的发送判据（作业 1 用）。"""

W, H = 760, 288
BLUE = '#1F5FA8'
DARK = '#1B1B1B'
GREY = '#5A6672'
LINE = '#D5DBE2'

BITS = [
    ('bit7', 'TXFE', 'hi'),
    ('bit6', 'CTS', ''),
    ('bit5', 'TXFF', 'hi'),
    ('bit4', 'RXFE', ''),
    ('bit3', 'BUSY', ''),
    ('bit2', 'DCD', ''),
    ('bit1', 'DSR', ''),
    ('bit0', 'RI', ''),
]

BX = 40          # 左起
BW = 76          # 框宽
BG = 10          # 框间距
BY = 40          # 框顶
BH = 46


def main():
    out = []
    out.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
               'viewBox="0 0 %d %d">' % (W, H, W, H))
    out.append('<g font-family="\'PingFang SC\',\'Hiragino Sans GB\','
               '\'Microsoft YaHei\',sans-serif">')
    out.append('<rect x="0" y="0" width="%d" height="%d" fill="#FFFFFF"/>' % (W, H))

    for i, (bit, name, hl) in enumerate(BITS):
        x = BX + i * (BW + BG)
        out.append('<text x="%d" y="26" font-size="12.5" fill="%s" '
                   'text-anchor="middle">%s</text>' % (x + BW // 2, GREY, bit))
        if hl == 'hi':
            fill = '#E7F4EA' if name == 'TXFE' else '#FCE9E9'
            stroke = '#2E7D4F' if name == 'TXFE' else '#C0392B'
            sw = '2'
        else:
            fill = '#F7F9FB'
            stroke = '#9AA7B4'
            sw = '1.2'
        out.append('<rect x="%d" y="%d" width="%d" height="%d" rx="6" fill="%s" '
                   'stroke="%s" stroke-width="%s"/>'
                   % (x, BY, BW, BH, fill, stroke, sw))
        out.append('<text x="%d" y="%d" font-size="13.5" fill="%s" '
                   'font-weight="600" text-anchor="middle">%s</text>'
                   % (x + BW // 2, BY + 29, DARK, name))

    out.append('<text x="%d" y="%d" font-size="13" fill="%s" '
               'text-anchor="middle">UARTFR（0x18）低 8 位</text>'
               % (W // 2, BY + BH + 28, GREY))

    rows = [
        ('作业 1 的写法', 'return ((fr &amp; DW_UART_TXFE) == 0U);  // 非空 → 继续等',
         '#EAF2FB', BLUE),
        ('基础版的写法', 'return ((fr &amp; DW_UART_TXFF) != 0U);  // FIFO 满 → 继续等',
         '#F7F9FB', '#9AA7B4'),
    ]
    y = BY + BH + 44
    for label, code, fill, stroke in rows:
        out.append('<rect x="%d" y="%d" width="%d" height="52" rx="6" fill="%s" '
                   'stroke="%s" stroke-width="1.2"/>'
                   % (BX, y, W - 2 * BX, fill, stroke))
        out.append('<text x="%d" y="%d" font-size="12.5" fill="%s">%s</text>'
                   % (BX + 16, y + 21, GREY, label))
        out.append('<text x="%d" y="%d" font-size="13" fill="%s" '
                   'font-family="\'SF Mono\',Menlo,Consolas,monospace">%s</text>'
                   % (BX + 16, y + 42, DARK, code))
        y += 62

    out.append('<text x="%d" y="%d" font-size="12.5" fill="%s">'
               'TXFE 为 1 表示 FIFO 空、可以写；TXFF 为 1 表示 FIFO 满、要继续等。'
               '</text>' % (BX, y + 14, GREY))

    out.append('</g></svg>')

    path = '实验截图/示意图_UARTFR发送判定.svg'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(''.join(out))
    print('已写', path)


if __name__ == '__main__':
    main()
