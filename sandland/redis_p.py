import redis

# pool = redis.ConnectionPool.from_url('redis://[:shenxfT1000]@gitlab.markbolo.com:6379/0')
r = redis.Redis(host='markbolo.com', password='shenxfT1000', port='6379')

proxy_ip_key = 'proxy_ip'
proxy_ip_len_key = 'proxy_ip_size'
ip_pool_key = 'ip_pool'
