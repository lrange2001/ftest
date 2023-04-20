ps -ef | grep uwsgi | grep -v grep | awk '{print $2}' | xargs kill
ps -ef | grep channel.sh | grep -v grep | awk '{print $2}' | xargs kill
ps -ef | grep daphne | grep -v grep | awk '{print $2}' | xargs kill
