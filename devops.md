ACTUALIZACION 20201202

ssh -i "Datavio_Mx.pem" ubuntu@ec2-18-221-65-48.us-east-2.compute.amazonaws.com


En ubuntu@ip-172-31-9-14:~/id_check$ vim /etc/supervisor/conf.d/app.conf 

[program:app]
command=/home/id_check_admin/id_check/api/venv/bin/gunicorn app:app

bind = '127.0.0.1:8000'

workers = 2
threads = 2
timeout = 600
keepalive = 120
limit_request_line = 0
limit_request_fields = 32768
limit_request_field_size = 0

directory=/home/id_check_admin/id_check/api

user=ubuntu
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true

En ubuntu@ip-172-31-9-14:~/id_check$ vim /etc/supervisor/supervisord.conf 

; supervisor config file

[unix_http_server]
file=/var/run/supervisor.sock   ; (the path to the socket file)
chmod=0700                       ; sockef file mode (default 0700)

[supervisord]
logfile=/var/log/supervisor/supervisord.log ; (main log file;default $CWD/supervisord.log)
pidfile=/var/run/supervisord.pid ; (supervisord pidfile;default supervisord.pid)
childlogdir=/var/log/supervisor            ; ('AUTO' child log dir, default $TEMP)

; the below section must remain in the config file for RPC
; (supervisorctl/web interface) to work, additional interfaces may be
; added by defining them in separate rpcinterface: sections
[rpcinterface:supervisor]
supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface

[supervisorctl]
serverurl=unix:///var/run/supervisor.sock ; use a unix:// URL  for a unix socket

; The [include] section can just contain the "files" setting.  This
; setting can list multiple files (separated by whitespace or
; newlines).  It can also contain wildcards.  The filenames are
; interpreted as relative to this file.  Included files *cannot*
; include files themselves.

[include]
files = /etc/supervisor/conf.d/*.conf
                                     
TODO:

Scripts de creación SQL

OUTDATED

ssh -i "Datavio_Mx.pem" ubuntu@ec2-3-15-144-142.us-east-2.compute.amazonaws.com

sudo apt update

sudo apt install postgresql postgresql-contrib

`sudo apt install virtualbox`

`docker-machine create node1`
`docker-machine create node2`

`docker-machine ssh node1`
`docker-machine ssh node2`
