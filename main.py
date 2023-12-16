from find_center import findCenters

# Videos of the robot movement
files = ['vids\camera0.mp4', 'vids\camera1.mp4', 'vids\camera2.mp4', 'vids\camera3.mp4']
data_dict = {}  #  Store the center of the aruco in each video, also tells wich frame has error in reading

for i in range(len(files)):
    errors, centers = findCenters(files[i], aruco_id=0)
    data_dict[files[i]] = {'errors': errors, 'centers': centers}

for video, data in data_dict.items():
    print(f"Video: {video}")
    print(f"Errors: {data['errors']}")
    print(f"Centers: {data['centers']}")
    print("-----------\n")