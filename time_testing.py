from project import QR_code_present, QR_data
import cv2

import time




test_image_filepath = "TEST PDF Scans/example_image_qr_code.png"
other_test_image = "TEST PDF Scans/high_quality_color.png"

img_path = "test images/qr page "

original_img = img_path + "(original).png"
large_img = img_path + "(large).png"
medium_img = img_path + "(medium).png"
small_img = img_path + "(small).png"




test_image = cv2.imread(medium_img)
qr_data = QR_data(test_image)
repitions = 50
tic = time.perf_counter()

for i in range(repitions):
    _ = QR_code_present(test_image, qr_data)


toc = time.perf_counter()

print(f"it took {toc - tic} seconds to run {repitions} repititions of the QR_code_present function")
print(f"An average time of {((toc - tic) / repitions):.3f} seconds per run")