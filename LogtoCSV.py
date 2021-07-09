## For AoA Testing of TI Kit July 2021
## Yrina Guarisma
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import re
import sys

# Filter Time, Angle, RSSI, Antenna, and Channel Data from Log Files
def filterLog(lines):
	aoa_str = 'RTLS_CMD_AOA_RESULT_ANGLE'
	count = 0
	time_format = "%Y-%m-%d %H:%M:%S,%f"
	data_dict = []
	for line in lines:
	    if aoa_str in line:
	        #print(line + "\n")
	        count = count + 1
	        time = re.findall(r'\[([0-9- :,]*)\]', line)
	        angle_data = re.findall(r'angle\': ([0-9-]{1,5})\b', line)
	        rssi_data = re.findall(r'rssi\': ([0-9-]{1,4})\b', line)
	        antenna_data = re.findall(r'antenna\': ([0-9-]{1,4})\b', line)
	        chan_data = re.findall(r'channel\': ([0-9-]{1,4})\b', line)


	        if time and angle_data and rssi_data and antenna_data and chan_data:
	        	print(time[0])

	        	temp_dict = {"time":datetime.datetime.strptime(time[0],time_format), "angle":int(angle_data[0]), "rssi":int(rssi_data[0]), "antenna":int(antenna_data[0]), "channel":int(chan_data[0])}
	        	data_dict.append(temp_dict)
	        else:
	        	print("Data Value Omitted did not match string. Check Log File" + " - " + str(count) + "\n")
	return data_dict

# Graph Scatter Plot of Angles with respect to Time and ask User for actual angle
def graphScatter(data):
	ang = input("What is the actual angle? ")
	X = [range(0,data.shape[0])]
	plt.scatter(data["time"], data["angle"])
	plt.title("Angle Measured by TI vs. Time\nActual Angle:" + ang)
	plt.xlabel("Time")
	plt.ylabel("Angle (Degrees)")

	plt.show()

# Save Data to Useable CSV File
def saveToCSV(data):
	csv_name = "Data_" + datetime.datetime.now().strftime("%m-%d-%y_%I-%M-%S") + ".csv"
	data.to_csv(csv_name, date_format="%Y-%m-%d %H:%M:%S,%f")


## Main Function
def main(argv):
	log_file_name = sys.argv[1]
	
	file = open(log_file_name, 'r')
	lines = file.read().splitlines()


	data_dict = filterLog(lines)
	data = pd.DataFrame(data_dict)
	print(data.info())

	if data is not None:
		saveToCSV(data)
		graphScatter(data)
		print("Done")
	else:
		print("No Data Recorded")
	file.close()



if __name__ == '__main__':
    main(sys.argv)