import cv2

def datasetCreation():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    count = 1

    while True:
        ret, frame = cap.read()
        cv2.putText(frame, "Press c to Capture and s to Save", (10, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 365), 1)
        cv2.imshow("Take Images for Dataset", frame)
        if cv2.waitKey(1) & 0xFF == ord('s') or count == 1000:
            cap.release()
            cv2.destroyAllWindows()
            break
        if (cv2.waitKey(1) & 0xFF == ord('c')):
            face = cv2.resize(frame, (200, 200))
            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
            count += 1

            # Save file in specified directory with unique name
            file_name_path = 'Dataset/' + str(count) + '.jpg'
            cv2.imwrite(file_name_path, face)

            # Put count on images and display live count
            cv2.putText(face, str(count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow('Face Cropper', face)
    print("Sample collection Complete")
    print("[INFO] New Dataset has been generated.")
