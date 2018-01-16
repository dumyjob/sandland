import redis
import json

# pool = redis.ConnectionPool.from_url('redis://[:shenxfT1000]@gitlab.markbolo.com:6379/0')
r = redis.Redis(host='markbolo.com', password='shenxfT1000', port='6379')

proxy_ip_queue = 'proxy_ip_queue'
proxy_ip_len_key = 'proxy_ip_size'
ip_pool_key = 'ip_pool'


# def main():
#     proxy = {'proxy': 'http://180.118.247.179:9000'}
#
#     s = json.dumps(dict(proxy))
#     # todo: 注意事务和并发
#     r.lpush(proxy_ip_queue, s)
#
# if __name__ == '__main__':
#     main()
