import socket, threading

before_socket = socket.socket
before_thread = threading.Thread

import anvil.server                 # 这一行会触发 uplink 的 import
anvil.server.connect("server_G5LS4NKQI44CSJSY73GRKMRG-F4ZBMGWQBKSHSVYA",url = 'ws://localhost:59001/_/uplink')

after_socket = socket.socket
after_thread = threading.Thread

print("socket.socket 变了吗？", before_socket is after_socket, before_socket, "=>", after_socket)
print("threading.Thread 变了吗？", before_thread is after_thread, before_thread, "=>", after_thread)
