import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Video Feed
# For CSI Camera 
# Use Opencv version (4.1.1) for proper Functioning

# For Laptop
# Feed= cv2.VideoCapture(0) 
# For Phone
Feed =cv2.VideoCapture(0)

# Variables For Count #
counter = 0 
state = None
        ## Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while Feed.isOpened():
        ret, frame = Feed.read()
        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
            
        # Make detection
        results = pose.process(image)
            
        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        #Function
        def calculate_angle(a,b,c):
            a = np.array(a) # First
            b = np.array(b) # Mid
            c = np.array(c) # End
                    
            radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
            angle = np.abs(radians*180.0/np.pi)
                    
            if angle >180.0:
                angle = 360-angle
                        
            return angle 
        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark
            # Get coordinates
            shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                    
             # Calculate angle
            angle = calculate_angle(shoulder, elbow, wrist)
                    
            # Visualize angle
            # cv2.putText(image, str(angle), 
            #             tuple(np.multiply(elbow, [640, 480]).astype(int)), 
            #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2, cv2.LINE_AA
            #                     )

            # Curl counter logic
            if angle > 160:
                state = "Down"
            if angle < 30 and state =='Down':
                state="Up"
                counter +=1
                print(counter)     
            exercise= "Curls"
        except:
            pass
                
        cv2.rectangle(image, (0,0), (200,70), (0,0,0), -1)
        cv2.rectangle(image, (540,0), (620,20), (0,0,0), -1)
                
        # Rep data
        cv2.putText(image, 'REPS', (10,17), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA)
        cv2.putText(image, str(counter), (10,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
                
        # Stage data
        cv2.putText(image, 'STATE', (90,17), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA)
        cv2.putText(image, state, (90,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
        
        # Exercise Name
        cv2.putText(image, exercise, (550,15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA)
                
                
        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(0,0,250), thickness=2, circle_radius=2), 
                                  mp_drawing.DrawingSpec(color=(250,250,250), thickness=2, circle_radius=2) 
                                )              
            

        cv2.imshow('Feed', image)

        if cv2.waitKey(1) & 0xFF == ord('x'):
            import Leave
            break

    Feed.release()
    cv2.destroyAllWindows()
  
