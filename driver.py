# import sys
# import json
# import socket
# import time
# import requests
# import uuid
# import threading
# from bisect import insort
# from kafka import KafkaProducer
# from kafka import KafkaConsumer
# host_name = socket.gethostname()
# ip_address = socket.gethostbyname(host_name)
# driver_node_id = str(uuid.uuid4())
# config_data = {}

# ##############################################################################################
# def register():
#     driver = KafkaProducer(bootstrap_servers=['localhost:9092'])
#     register = {
#     "node_id": driver_node_id,
#     "node_IP": ip_address,
#     "message_type": "DRIVER_REG"
#     }
#     driver.send('register', value=json.dumps(register).encode('utf-8'))
#     driver.flush()
#     print(register)


# ###############################################################################################

# def test_config(config_data):
#     test_consume = KafkaConsumer(bootstrap_servers='localhost:9092')
#     topics_consume = ['test_config']
#     test_consume.subscribe(topics_consume)
#     for i in test_consume:
#         j=i.value.decode('utf-8')
#         print(j)
#         #global config_data
#         config_data = j
#         break

# ################################################################################################

# def trigger():
#     consumer = KafkaConsumer('trigger',
#                              bootstrap_servers='localhost:9092',
#                              value_deserializer=lambda x: json.loads(x.decode('utf-8')))
#     consumer.subscribe(['trigger'])
#     for message in consumer:
#         trigger_message = message.value
#         print(f"Received trigger message: {trigger_message}")
#         if(trigger_message['test_type']=='a' or trigger_message['test_type']=='A'):
#             #global config_data
#             avalanche1 = threading.Thread(target=avalanche, args=())
#             avalanche1.start()
#             avalanche1.join()     
        


# ##########################################################################################

# def avalanche():
#     driver = KafkaProducer(bootstrap_servers=['localhost:9092'])
#     delay = 1/5
#     response_times = []
#     mean_time = [0,0]
#     result = []

#     for i in range(int(config_data["message_count_per_driver"])):
#         start_time = time.time()
#         response = requests.get("http://127.0.0.1:8000/ping")
#         end_time = time.time()
#         time.sleep(delay)

#         response_time = end_time - start_time
#         insort(response_times, response_time)
#         mean_time[0] = mean_time[0]+response_time
#         mean_time[1] = mean_time[1]+1 

#         if i%10 == 0:
#             result = [mean_time[0]/mean_time[1], response_times[0], response_times[-1]]
#             if mean_time[1] % 2 == 1:
#                 result.append(response_times[mean_time[1] // 2])
#             else:
#                 mid1 = response_times[(mean_time[1] - 1) // 2]
#                 mid2 = response_times[mean_time[1] // 2]
#                 result.append((mid1 + mid2) / 2)
#             driver.send('metrics', value=json.dumps(result).encode('utf-8'))


# ################################################################################################

# register1 = threading.Thread(target=register, args=())
# register1.start()
# register1.join()
# print('11')
# test_config1 = threading.Thread(target=test_config, args=(config_data,))
# test_config1.start()
# test_config1.join()
# print("1")
# trigger1 = threading.Thread(target=trigger, args=())
# trigger1.start()
# trigger1.join()
# print('1111')
# avalanche1 = threading.Thread(target=avalanche, args=())
# avalanche1.start()
# avalanche1.join()
# print("avalanche ended")




import sys
import json
import socket
import time
import requests
import uuid
import threading
from bisect import insort
from kafka import KafkaProducer
from kafka import KafkaConsumer

host_name = socket.gethostname()
ip_address = socket.gethostbyname(host_name)
driver_node_id = str(uuid.uuid4())
config_data = {}
config_lock = threading.Lock()  # Added lock for thread safety

##############################################################################################

def register():
    driver = KafkaProducer(bootstrap_servers=['localhost:9092'])
    register = {
        "node_id": driver_node_id,
        "node_IP": ip_address,
        "message_type": "DRIVER_REG"
    }
    driver.send('register', value=json.dumps(register).encode('utf-8'))
    driver.flush()
    print(register)

###############################################################################################

def test_config():
    global config_data
    test_consume = KafkaConsumer(bootstrap_servers='localhost:9092')
    topics_consume = ['test_config']
    test_consume.subscribe(topics_consume)
    for i in test_consume:
        j = i.value.decode('utf-8')
        print(j)
        with config_lock:
            config_data = json.loads(j)
        break

################################################################################################

def trigger():
    global config_data
    consumer = KafkaConsumer('trigger',
                             bootstrap_servers='localhost:9092',
                             value_deserializer=lambda x: json.loads(x.decode('utf-8')))
    consumer.subscribe(['trigger'])
    for message in consumer:
        trigger_message = message.value
        print(f"Received trigger message: {trigger_message}")
        with config_lock:
            if trigger_message.get('test_id', '') in ['a', 'A']:
                avalanche1 = threading.Thread(target=avalanche, args=())
                print("inside if")
                avalanche1.start()
                avalanche1.join()

##########################################################################################

def avalanche():
    global config_data
    driver = KafkaProducer(bootstrap_servers=['localhost:9092'])
    delay = 1/5
    response_times = []
    mean_time = [0, 0]
    result = []
    print("avalanche launched")
    message_count_per_driver = int(config_data.get("message_count_per_driver", 0))
    print("starting")

    for i in range(message_count_per_driver):
        print("started")
        start_time = time.time()
        response = requests.get("http://127.0.0.1:8000/ping")
        end_time = time.time()
        time.sleep(delay)

        response_time = end_time - start_time
        insort(response_times, response_time)
        mean_time[0] += response_time
        mean_time[1] += 1
        print(response)

        if i % 10 == 0:
            result = [mean_time[0] / mean_time[1], response_times[0], response_times[-1]]
            if mean_time[1] % 2 == 1:
                result.append(response_times[mean_time[1] // 2])
            else:
                mid1 = response_times[(mean_time[1] - 1) // 2]
                mid2 = response_times[mean_time[1] // 2]
                result.append((mid1 + mid2) / 2)
            driver.send('metrics', value=json.dumps(result).encode('utf-8'))

################################################################################################

register1 = threading.Thread(target=register, args=())
register1.start()
register1.join()
print('11')
test_config1 = threading.Thread(target=test_config, args=())
test_config1.start()
test_config1.join()
print("1")
trigger1 = threading.Thread(target=trigger, args=())
trigger1.start()
trigger1.join()
print('1111')
# avalanche1 = threading.Thread(target=avalanche, args=())
# avalanche1.start()
# avalanche1.join()
# print("avalanche ended")
