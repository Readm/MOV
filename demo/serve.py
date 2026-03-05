#!/usr/bin/env python3
"""
简单 HTTP 服务器，用于在本地运行 MOV demo
Web Speech API 需要 localhost 才能访问麦克风

用法：
  python serve.py

然后在 Chrome 中打开 http://localhost:8080
"""
import http.server
import socketserver
import os

PORT = 8080
os.chdir(os.path.dirname(os.path.abspath(__file__)))

Handler = http.server.SimpleHTTPRequestHandler
Handler.extensions_map.update({'.js': 'application/javascript'})

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"MOV Demo 运行中: http://localhost:{PORT}")
    print("在 Chrome 中打开上方地址（需要 Chrome 以使用语音识别）")
    print("Ctrl+C 停止服务器")
    httpd.serve_forever()
