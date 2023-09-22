#!/bin/python3
# ===================================================================
# Firewall
# Autor: Alefy Gonzaga
# ===================================================================
import os

# === configuracoes ===

# default
input_default ="ACCEPT"
#forward_default="DOCKER" # DROP / ACCEPT / DOCKER
#output_default="ACCEPT"

#web
web_http_porta = "80"
web_https_porta = "443"
web_aberto_para = ["0.0.0.0/0"]

#ssh
ssh_porta = "22"
ssh_aberto_para = ["192.168.0.1","8.8.8.8","172.16.0.1","10.1.2.0/24"]

#mysql
mysql_porta ="3306"
mysql_aberto_para = ["192.168.0.1","8.8.8.8","172.19.0.0/24"]

# === Politica padrao ===

# Apticando politica padrao INPUT
if input_default == "DROP" or input_default == "ACCEPT":
    os.system("iptables -P INPUT " + input_default)

# Aplicando politica padrao FORWARD
#if forward_default == "DROP" or forward_default == "ACCEPT":

#    os.system("iptables -P FORWARD " + forward_default)

# Aplicando politica padrao OUTPUT
#if output_default == "DROP" or output_default == "ACCEPT":
#    os.system("iptables -P OUTPUT " + output_default)

# Salva vidas
os.system("iptables -F")
os.system("iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT")
os.system("iptables -A INPUT -i lo -j ACCEPT")
os.system("iptables -A OUTPUT -o lo -j ACCEPT")
os.system("iptables -A INPUT -p tcp --dport "+ssh_porta+" -j ACCEPT")

# === Regras ===

# aplicando regras ssh
for origem in ssh_aberto_para :
    os.system("iptables -A INPUT -p tcp -s "+ origem+" --dport "+ssh_porta+" -j ACCEPT")

# aplicando regras mysql
for origem in mysql_aberto_para :
    os.system("iptables -A INPUT -p tcp -s "+ origem+" --dport "+mysql_porta+" -j ACCEPT")

# aplicando regras web
for origem in web_aberto_para :
    os.system("iptables -A INPUT -p tcp -s "+ origem+" --dport "+web_http_porta+" -j ACCEPT")

for origem in web_aberto_para :
    os.system("iptables -A INPUT -p tcp -s "+ origem+" --dport "+web_https_porta+" -j ACCEPT")

# Listando regras
os.system("clear")
os.system("iptables -t filter -L -nv")
