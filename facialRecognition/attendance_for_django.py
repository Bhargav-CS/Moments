import face_recognition
import cv2
import numpy as np
import csv
import os
from datetime import datetime


class Student:
    def __init__(self, name, photo_path):
        self.name = name
        self.photo_path = photo_path
        self.encoding = None

    def load_encoding(self):
        image = face_recognition.load_image_file(self.photo_path)
        self.encoding = face_recognition.face_encodings(image)[0]


class AttendanceSystem:
    def __init__(self, students_directory):
        self.students_directory = students_directory
        self.known_students = []
        self.face_names = []
        self.video_capture = None
        self.face_locations = []
        self.face_encodings = []
        self.current_date = None
        self.csv_file = None
        self.csv_writer = None

    def register_student(self, name, photo_path):
        student = Student(name, photo_path)
        student.load_encoding()
        self.known_students.append(student)

    def load_students_from_directory(self):
        for filename in os.listdir(self.students_directory):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                name = os.path.splitext(filename)[0]
                photo_path = os.path.join(self.students_directory, filename)
                self.register_student(name, photo_path)

    def initialize_video_capture(self):
        self.video_capture = cv2.VideoCapture(0)

    def initialize_csv_file(self):
        self.current_date = datetime.now().strftime("%Y-%m-%d")
        self.csv_file = open(f"{self.current_date}.csv", 'w+', newline='')
        self.csv_writer = csv.writer(self.csv_file)

    def process_frame(self):
        _, frame = self.video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        self.face_locations = face_recognition.face_locations(rgb_small_frame)
        self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)
        self.face_names = []

        for face_encoding in self.face_encodings:
            matches = face_recognition.compare_faces([student.encoding for student in self.known_students], face_encoding)
            name = ""
            face_distance = face_recognition.face_distance([student.encoding for student in self.known_students], face_encoding)
            best_match_index = np.argmin(face_distance)
            if matches[best_match_index]:
                name = self.known_students[best_match_index].name

            self.face_names.append(name)
            if name:
                font = cv2.FONT_HERSHEY_SIMPLEX
                bottom_left_corner_of_text = (10, 100)
                font_scale = 1.5
                font_color = (255, 0, 0)
                thickness = 3
                line_type = 2

                cv2.putText(frame, f"{name} Present",
                            bottom_left_corner_of_text,
                            font,
                            font_scale,
                            font_color,
                            thickness,
                            line_type)

                for student in self.known_students:
                    if student.name == name:
                        self.known_students.remove(student)
                        now = datetime.now()
                        current_time = now.strftime("%H-%M-%S")
                        self.csv_writer.writerow([name, current_time])
                        self.csv_file.flush()
                        break

        cv2.imshow("attendance system", frame)

    def run(self):
        self.initialize_video_capture()
        self.initialize_csv_file()
        self.load_students_from_directory()

        while True:
            self.process_frame()
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.video_capture.release()
        cv2.destroyAllWindows()
        self.csv_file.close()


if __name__ == "__main__":
    students_directory = "D:\\moments_web\\facialRecognition\\photos"
    attendance_system = AttendanceSystem(students_directory)
    attendance_system.run()
