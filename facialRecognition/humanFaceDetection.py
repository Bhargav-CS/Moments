#using folders as database
import face_recognition
import cv2
import numpy as np
import os
import shutil

class Student:
    def __init__(self, name, photo_path):
        self.name = name
        self.photo_path = photo_path
        self.encoding = None

    def load_encoding(self):
        image = face_recognition.load_image_file(self.photo_path)
        encodings = face_recognition.face_encodings(image)
        if encodings:
            self.encoding = encodings[0]
        else:
            print(f"No face found in {self.photo_path}.")
            self.encoding = None

class ImageRecognitionSystem:
    def __init__(self, students_directory, input_image_path):
        self.students_directory = students_directory
        self.known_students = []
        self.input_image_path = input_image_path
        self.input_image_encoding = self.load_image_encoding(input_image_path)

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

    def load_image_encoding(self, image_path):
        image = face_recognition.load_image_file(image_path)
        return face_recognition.face_encodings(image)[0]

    def compare_images(self):
        for student in self.known_students:
            if student.encoding is not None:
                match = face_recognition.compare_faces([student.encoding], self.input_image_encoding)
                if match[0]:
                    self.save_matched_image(student.photo_path)

    def save_matched_image(self, matched_image_path):
        matched_image_name = os.path.basename(matched_image_path)
        input_image_name = os.path.splitext(os.path.basename(self.input_image_path))[0]
        matched_folder_path = os.path.join(self.students_directory, input_image_name)
        os.makedirs(matched_folder_path, exist_ok=True)
        shutil.copy(matched_image_path, os.path.join(matched_folder_path, matched_image_name))

    def run(self):
        self.load_students_from_directory()
        self.compare_images()

if __name__ == "__main__":
    students_directory = "D:\\moments_web\\facialRecognition\\photos"
    input_image_path = "D:\\moments_web\\facialRecognition\\input_for_muditaa.jpg"
    image_recognition_system = ImageRecognitionSystem(students_directory, input_image_path)
    image_recognition_system.run()