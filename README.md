DNS隐蔽传输信道

实验环境：
Windows11主机 + Ubuntu22.04.2VMware虚拟机
python3.9

运行方法：
请设置 服务器IP&端口 客户端IP&端口 服务器发送的消息command 客户端发送的消息domain
先将server.py在主机中运行，再将client.py在虚拟机中运行
亦可均在主机运行

注意：
1.VMware虚拟机中执行client.py时，需要将目标服务器IP设为VMnet8虚拟网卡的IP，而非主机IP
2.在Ubuntu中有进程systemd-r占用了53端口，可先用sudo lsof -i:53查看53端口是否被占用，若是，则需用sudo systemctl stop systemd-resolved.service
和sudo systemctl disable systemd-resolved.service关闭该服务，再次尝试
3.可使用Ubuntu防火墙ufw来对端口进行关闭/开启，需注意默认的deny/allow操作只针对in端口，而不限制out端口，故本实验中需要使用sudo ufw deny in 53和sudo ufw deny out 53来关闭53端口，再sudo ufw enable开启防火墙即可

待改进：

将正确识别的方法也放在server上
