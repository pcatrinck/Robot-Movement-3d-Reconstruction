import cv2
import cv2.aruco as aruco

def findCenters(file_name, aruco_id):
    capture = cv2.VideoCapture(file_name)

    def findAruco(img, marker_size=4, total_markers=50):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)                              # Convert the input image to grayscale
        key = getattr(aruco, f'DICT_{marker_size}X{marker_size}_{total_markers}') # Construct the ArUco dictionary name dynamically based on marker size and total markers    
        arucoDict = aruco.getPredefinedDictionary(key)                            # Get the predefined ArUco dictionary based on the constructed key
        parameters = aruco.DetectorParameters()                                   # Set up parameters for the ArUco marker detection
        bbox, ids, rejectedImgPoints = aruco.detectMarkers(gray, arucoDict, parameters=parameters) # Detect ArUco markers in the grayscale image using the specified dictionary and parameters
        return bbox, ids, rejectedImgPoints                                       # Return the detected bounding boxes, IDs, and rejected image points


    

    frame_number = 0
    frame_error_list = []
    aruco_centers_list = []

    while True:
        ret, img = capture.read()      # Reads a frame from the video
        if not ret:                    # If there is not return, end
            print("End of video.")
            break

        bbox, ids, _ = findAruco(img)  # Calls function findAruco to search over the current frame

        if ids is not None and aruco_id in ids:                  # Check if ArUco markers are detected and the desired ID is present
            target_index = list(ids).index(aruco_id)             # Find the index of the desired ArUco ID
            c = bbox[target_index][0]                            # Extract the corner coordinates of the marker with the desired ID
            center = (int(c[:, 0].mean()), int(c[:, 1].mean()))  # Calculate the mean of X and Y coordinates to get the center
            aruco_centers_list.append(center)                    # Append the center coordinates to the list
            cv2.circle(img, center, 5, (0, 255, 0), -1)          # Draw a green circle at the center of the marker

        else:
            frame_error_list.append(frame_number)

        frame_number += 1

        cv2.imshow('ArUco Centers', img)  # Display the frame with ArUco centers

        if cv2.waitKey(1) == 27:          # Esc exits
            break
    
    capture.release()                     # Release the video capture object
    cv2.destroyAllWindows()               # Close all OpenCV windows

    return frame_error_list, aruco_centers_list