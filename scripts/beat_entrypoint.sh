echo "--> Starting beats process"
celery -A tasks worker -l info --without-gossip --without-mingle --without-heartbeat