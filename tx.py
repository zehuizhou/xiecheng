#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:洪卫

import tkinter as tk  # 使用Tkinter前需要先导入

# 第1步，实例化object，建立窗口window
window = tk.Tk()

# 第2步，给窗口的可视化起名字
window.title('My Window')

# 第3步，设定窗口的大小(长 * 宽)
window.geometry('500x300')  # 这里的乘是小x

# 第4步，在图形界面上设定标签
l = tk.Label(window, text='请输入城市名称：', bg='white', font=('Arial', 12), width=30, height=2)

# 第5步，放置标签
l.pack()    # Label内容content区域放置位置，自动调节尺寸


var = tk.StringVar()

e = tk.Entry(window, show=None, font=('Arial', 14), textvariable=var)  # 显示成明文形式
e.pack()
data = var.get()

def hi():
    print('hi')
b = tk.Button(window, text='hit me', font=('Arial', 12), width=10, height=1, command=hi())
b.pack()

# 第6步，主窗口循环显示
window.mainloop()