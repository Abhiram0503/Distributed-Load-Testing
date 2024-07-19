from kafka import KafkaConsumer
from kafka import KafkaProducer
import json
import sys
import time
import random
import threading
import uuid
count_reg=0
num_of_drivers = int(sys.argv[1])
test_ty = sys.argv[2]
test_msg_delay=sys.argv[3]
msg_count_per_delay=sys.argv[4]
flag=0

###############################################################

def register():
    global count_reg
    global num_of_drivers
    register_consume = KafkaConsumer(bootstrap_servers='localhost:9092')
    topics_consume = ['register']
    register_consume.subscribe(topics_consume)
    for i in register_consume:
     if(count_reg==num_of_drivers):
        break
     elif count_reg<num_of_drivers :
        j=i.value.decode('utf-8')
        print(j)
        count_reg+=1
        print(count_reg==num_of_drivers)
        time.sleep(2)
        test_config()
        #test_config1.join()
        with open("/home/akhilesh/Documents/version_2/hlo.json", 'a') as output_file:
            json.dump(j, output_file)
            output_file.write('\n')



########################################################################
test_id=str(uuid.uuid4())
def test_config():
    global test_ty
    global test_msg_delay
    global msg_count_per_delay
    global test_id
    global flag
    test_config_produce = KafkaProducer(bootstrap_servers='localhost:9092',value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    topic = 'test_config'
    test_message= {
        "test_id":test_id,
        "test_type": test_ty,
        "test_message_delay": test_msg_delay,
        "message_count_per_driver": msg_count_per_delay
    }
    test_config_produce.send(topic, value=test_message)
    test_config_produce.flush()
    print(f"Sent message: {test_message}")
    if(flag>0):
        time.sleep(2)
        trigger()
    flag=flag+1

################################################################




def trigger():
    global test_id
    kafka_bootstrap_servers = 'localhost:9092'  # Update with your Kafka bootstrap servers
    kafka_topic = 'trigger'
    trig = KafkaProducer(bootstrap_servers=kafka_bootstrap_servers,
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    trigger_message = {
        "test_id": test_id,
        "trigger": "YES",
    }
    trig.send(kafka_topic, value=trigger_message)
    trig.flush()
    trig.close()
    print(f"Trigger message sent: {trigger_message}")




###################################################################

def metrics():
    metrics_consume = KafkaConsumer(bootstrap_servers='localhost:9092')
    topics_consume = ['metrics']
    metrics_consume.subscribe(topics_consume)
    for i in metrics_consume:
        j=i.value.decode('utf-8')
        print(j)



################################################################################

class HeartbeatReceiver:
    def __init__(self, topic, bootstrap_servers, heartbeat_timeout=10):
        self.consumer = KafkaConsumer(topic, bootstrap_servers=bootstrap_servers)
        self.last_received_time = time.time()
        self.heartbeat_timeout = heartbeat_timeout
        self.timer_thread = threading.Thread(target=self.check_heartbeat)
        self.timer_thread.daemon = True  # Allow the program to exit even if the thread is still running

    def check_heartbeat(self):
        global num_of_drivers
        global count_reg
        while True:
            if time.time() - self.last_received_time > self.heartbeat_timeout:
                print("Heartbeat stopped!")
                count_reg=count_reg-1
                if(count_reg < num_of_drivers):
                    register()
            time.sleep(1)

    def receive_heartbeat(self):
        self.timer_thread.start()

        try:
            for message in self.consumer:
                self.last_received_time = time.time()
                print(f"Heartbeat received: {message.value}")
        except KeyboardInterrupt:
            print("Heartbeat receiver terminated.")

################################################################################



#register1 = threading.Thread(target=register, args=())
test_config1 = threading.Thread(target=test_config, args=())
trigger_A = threading.Thread(target=trigger, args=())
#trigger_T = threading.Thread(target=trigger, args=("T"))
metrics_1 = threading.Thread(target=metrics,args=())
register()
receiver = HeartbeatReceiver(topic='heartbeat', bootstrap_servers=['localhost:9092'])
#register1.start()
#register1.join()
time.sleep(2)
test_config1.start()
test_config1.join()
t=input("enter yes if trigger")
if(t=="yes"):
        trigger_A.start()
        trigger_A.join()
        metrics_1.start()
        receiver.receive_heartbeat()
        
metrics_1.join()
