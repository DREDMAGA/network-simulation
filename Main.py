from datetime import datetime
import time
import random


class Server:
    count = 0

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        cls.count += 1
        return instance

    def __init__(self):
        self.buffer = []
        self.ip = Server.count

    def send_data(self, data):
        Router.buffer.append(data)  # Добавление  данных в буфер роутера

    def get_data(self):
        data = self.buffer[:]
        self.buffer.clear()  # Очистка буфера после получения
        return data

    def get_ip(self):
        return self.ip


class Router:
    buffer = []
    servers = {}
    log = []

    @classmethod
    def link(cls, server):
        cls.servers[server.get_ip()] = server

    @classmethod
    def unlink(cls, server):
        del cls.servers[server.get_ip()]

    @classmethod
    def process_next(cls):
        if not cls.buffer:
            return

        data = cls.buffer.pop(0)  # Берём первое сообщение из очереди
        time.sleep(1)  # Задержка, чтобы симулировать работу роутера

        data.ttl -= 1
        time_str = data.timestamp.strftime("%H:%M:%S")

        if data.ttl <= 0:
            print(f"⛔️ Dropped (TTL=0): ", end="")
            data.info()
            cls.log.append(f"DROPPED {data.source_ip} → {data.ip} | data='{data.data}' | ttl=0 | time={time_str}")
            return

        if data.ip in cls.servers:
            cls.servers[data.ip].buffer.append(data)
            print(f"✅ Sent: ", end="")
            data.info()
            cls.log.append(f"SENT {data.source_ip} → {data.ip} | data='{data.data}' | ttl={data.ttl} | time={time_str}")

    @classmethod
    def send_data(cls):
        cls.buffer.sort(key=lambda d: -d.priority)
        while cls.buffer:
            cls.process_next()

    @classmethod
    def print_log(cls):
        print("\n Router Log:")
        for entry in cls.log:
            print(entry)


class Data:
    def __init__(self, data, dest_ip,source_ip, priority=0,):
        self.priority = priority
        self.data = data
        self.ip = dest_ip
        self.timestamp = datetime.now()
        self.ttl = 5
        self.source_ip = source_ip


    def info(self):
        time_str = self.timestamp.strftime("%H:%M:%S")
        print(f"[data='{self.data}',from={self.source_ip}, to={self.ip}, ttl={self.ttl}, time={time_str}]")

def generate_random_data(server_list):
    messages = ["Hello", "Ping", "Important", "Update", "Alert", "Test"]
    server = random.choice(server_list)
    msg = random.choice(messages)
    dest_candidates = [srv for srv in server_list if srv != server]
    dest = random.choice(dest_candidates)
    prio = random.randint(0, 10)
    packet = Data(msg, server.get_ip(),dest.get_ip(), priority=prio)
    server.send_data(packet)
    print(f"📤 Сгенерировано: '{msg}' → IP:{server.get_ip()} (prio={prio})")

if __name__ == "__main__":
    servers = [Server() for _ in range(3)]
    for srv in servers:
        Router.link(srv)

    for _ in range(10):
        generate_random_data(servers)

    Router.send_data()
    Router.print_log()
