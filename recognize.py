import cv2
import face_recognition
import os

video_capture = cv2.VideoCapture(0)
# length = int(input_movie.get(cv2.CAP_PROP_FRAME_COUNT))


known_faces = []
known_face_names =[]

path = "./knowns"
for x in os.listdir(path):
    if x.split(".jpeg") or x.split(".jpg") or x.split(".png"):
        known_faces.append(face_recognition.face_encodings(face_recognition.load_image_file("knowns/"+x))[0])
        known_face_names.append(x)

# known_faces = [
# face_encoding,
# ]


# Initialize variables
face_locations = []
face_encodings = []
face_names = []
# frame_number = 0

while True:
    # Grab a single frame of video
    # ret, frame = input_movie.read()
    # frame_number += 1

    # Quit when the input video file ends
    # if not ret:
    #     break

    ret, frame = video_capture.read()


    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_frame = frame[:, :, ::-1]

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        match = face_recognition.compare_faces(known_faces, face_encoding, tolerance=0.50)

        name = "Unknown"
        if True in match:
                    first_match_index = match.index(True)
                    imgname = known_face_names[first_match_index]
                    uname = imgname.split(".")
                    name = uname[0]
                    tname = name.split("-")
                    name = tname[0]
                    # print(name)
                # face_names.append(name)

        face_names.append(name)

      

    # Label the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):

    	# Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        if not name:
            name = "Unknown"

        
        # # Draw a box around the face
        # cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

    # Write the resulting image to the output video file
    # print("Writing frame {} / {}".format(frame_number, length))
    # output_movie.write(frame)

    cv2.imshow('Face Camera', frame)


    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# All done!
video_capture.release()
cv2.destroyAllWindows()
