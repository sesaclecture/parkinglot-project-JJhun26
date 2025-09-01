import cv2
import sys
import easyocr
import re

def image_ocr():
    reader = easyocr.Reader(['ko', 'en'])

    cap_dev_id = 0
    try:
        cap_dev_id = sys.argv[1]
        cap_dev_id = int(sys.argv[1])
    except IndexError:
        print(f"Info: Using default camera 0")
        cap_dev_id = 0
    except ValueError as e:
        print(f"Error: {e}")
        exit()

    cap = cv2.VideoCapture(cap_dev_id)

    if not cap.isOpened():
        print("Error: Could not open camera")
        exit()

    print("Press 'q' to quit")
    
    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Could not read frame")
            break

        result = reader.readtext(frame)

        for (bbox, text, prob) in result:
            cleaned_text = text.replace(' ', '')
            matchs = re.match(r'^[0-9]{3}[가-힣]{1}[0-9]{4}$', cleaned_text)
            if matchs:
                gr_text = matchs.group()
                return gr_text
                
        cv2.imshow('QR Code Reader', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()