import socket,cv2, pickle,struct
from deepface import DeepFace
import time
last_time = time.time()
result = "No detection"
# create socket
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_name  = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
port = 9999
client_socket.connect((host_ip,port)) # a tuple
data = b""
payload_size = struct.calcsize("Q")

font = cv2.FONT_HERSHEY_SIMPLEX

fps = 0

while True:
	while len(data) < payload_size:
		packet = client_socket.recv(4*1024) # 4K
		if not packet: break
		data+=packet
	packed_msg_size = data[:payload_size]
	data = data[payload_size:]
	msg_size = struct.unpack("Q",packed_msg_size)[0]
	
	while len(data) < msg_size:
		data += client_socket.recv(4*1024)
	frame_data = data[:msg_size]
	data  = data[msg_size:]
	frame = pickle.loads(frame_data)
	fps += 1
	if time.time() > last_time+1:

		result = DeepFace.analyze(frame, actions = ['emotion'])
		result = result['dominant_emotion']
		last_time = time.time()
		print(f"Fps : {fps}")
		fps = 0
	
	cv2.putText(frame,
						result,
						(50,50),
						font, 3,
						(0, 0, 255),
						2,
						cv2.LINE_4)
		
	cv2.imshow("RECEIVING VIDEO",frame)
    
	key = cv2.waitKey(1) & 0xFF
	if key  == ord('q'):
		break
client_socket.close()