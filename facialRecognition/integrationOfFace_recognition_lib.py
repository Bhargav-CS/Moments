import face_recognition
import os
import shutil
from tqdm import tqdm

class Student:
    def __init__(self, name, photo_path):
        self.name = name
        self.photo_path = photo_path
        self.encoding = None

class ImageRecognitionSystem:
    def __init__(self, students_directory, search_directory):
        self.students_directory = students_directory
        self.search_directory = search_directory
        self.known_students = []

    def register_student(self, name, photo_path):
        student = Student(name, photo_path)
        image = face_recognition.load_image_file(photo_path)
        encodings = face_recognition.face_encodings(image)
        if encodings:
            student.encoding = encodings[0]
            self.known_students.append(student)
        else:
            print(f"No face found in {photo_path}.")

    def load_students_from_directory(self):
        for filename in tqdm(os.listdir(self.students_directory), desc="Loading students"):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                name = os.path.splitext(filename)[0]
                photo_path = os.path.join(self.students_directory, filename)
                self.register_student(name, photo_path)

    def search_and_compare_images(self, student_name):
        for filename in tqdm(os.listdir(self.search_directory), desc="Searching and comparing"):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                image_path = os.path.join(self.search_directory, filename)
                image = face_recognition.load_image_file(image_path)
                encodings = face_recognition.face_encodings(image)
                if encodings:
                    for student in self.known_students:
                        if student.name == student_name and student.encoding is not None:
                            match = face_recognition.compare_faces([student.encoding], encodings[0])
                            if match[0]:
                                self.save_matched_image(image_path, student_name)

    def save_matched_image(self, matched_image_path, student_name):
        matched_image_name = os.path.basename(matched_image_path)
        matched_folder_path = os.path.join(self.students_directory, f"Matched{student_name}")
        os.makedirs(matched_folder_path, exist_ok=True)
        shutil.copy(matched_image_path, os.path.join(matched_folder_path, matched_image_name))

    def run(self, student_name):
        self.load_students_from_directory()
        self.search_and_compare_images(student_name)

if __name__ == "__main__":
    students_directory = "D:\\moments_web\\facialRecognition\\photos"
    search_directory = "D:\\moments_web\\facialRecognition\\testing"
    image_recognition_system = ImageRecognitionSystem(students_directory, search_directory)
    image_recognition_system.run("Bhargav")
