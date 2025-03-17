import numpy as np
import pytesseract
import cv2


class Read:

    def __init__(self):
        pass

    def read_number(self, image):
        """
        Extract the first digit found in the image using pytesseract OCR.
        """
        input_str = pytesseract.image_to_string(image, config='--psm 10 --oem 3 -c tessedit_char_whitelist=123456789')
        for char in input_str:
            if char.isdigit():
                return int(char)  # Return as integer immediately
        return None  # Return None if no number is found

    def collect_numbers(self, image, binary, intersections):
        """
        Collect numbers from the Sudoku grid based on the intersection points and binary image.
        """
        # Determine the box dimensions based on intersection points
        box_width = box_height = abs(intersections[0][0] - intersections[1][0])
        intersections_arr = np.array([[x for x in intersections[i*10:i*10+10]] for i in range(10)])
        numbers = []

        # Loop over each grid cell to collect numbers
        for i in range(9):
            temp_list = []
            for j in range(9):
                # Create a mask for each Sudoku cell
                x1, y1 = intersections_arr[i][j]
                x2, y2 = x1 + box_width, y1 + box_height
                mask = np.zeros_like(binary, dtype=np.uint8)
                mask[y1:y2, x1:x2] = 255

                # Apply the mask to the binary image
                output = np.bitwise_and(mask, binary)

                # Read the number from the image
                number = self.read_number(output)
                temp_list.append(number if number is not None else 0)  # Use 0 if no number is detected

            numbers.append(temp_list)

        return numbers