import cv2
import numpy as np

class Output:
    def __init__(self, image):
        self.image = image
        self.height, self.width, _ = self.image.shape

        # Define color constants
        self.COLOR_HORIZONTAL = (0, 255, 255)  # Yellow for horizontal lines
        self.COLOR_VERTICAL = (0, 255, 0)     # Green for vertical lines
        self.COLOR_INTERSECTION = (255, 0, 255)  # Magenta for intersections

    def calc_coordinates(self, rho, theta):
        """
        Calculate the start and end points of a line given rho and theta.
        """
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        return [x1, y1, x2, y2]

    def draw_lines(self, image, lines, color, thick):
        """
        Draw lines on the image.
        """
        for line in lines:
            (rho, theta) = line
            [x1, y1, x2, y2] = self.calc_coordinates(rho, theta)
            cv2.line(image, (x1, y1), (x2, y2), color, thick)

    def draw_intersections(self, image, intersections, length):
        """
        Draw intersection points on the image.
        """
        for coord in intersections:
            x, y = coord
            cv2.line(image, (x - length, y), (x + length, y), self.COLOR_INTERSECTION, thickness=1)
            cv2.line(image, (x, y - length), (x, y + length), self.COLOR_INTERSECTION, thickness=1)

    def draw_output(self, image, lines, intersections):
        """
        Draw the final output with lines and intersections.
        """
        out = np.copy(image)
        thick = self.height // 200  # Adjust the thickness based on the image size
        length = self.height // 100  # Length of the intersection markers

        # Draw horizontal and vertical lines using the new helper functions
        self.draw_lines(out, lines['horizontal'], self.COLOR_HORIZONTAL, thick)
        self.draw_lines(out, lines['vertical'], self.COLOR_VERTICAL, thick)

        # Draw intersections
        self.draw_intersections(out, intersections, length)

        return out