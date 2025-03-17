import numpy as np
import cv2
import matplotlib.pyplot as plt

class Detection:

    def __init__(self, image):
        self.image = image
        self.height, self.width, _ = self.image.shape

    def crop_image(self, binary, gray, contours):
        """Find and extract the largest contour (assumed to be the Sudoku grid)."""
        max_area = 0
        mask = np.zeros_like(binary, np.uint8)
        output = np.zeros_like(gray)

        if contours:
            best = max(contours, key=cv2.contourArea)  # Find largest contour
            cv2.drawContours(mask, [best], 0, 255, -1)
            cv2.drawContours(mask, [best], 0, 255, 2)

        output[mask == 255] = gray[mask == 255]
        return output

    def calc_coordinates(self, rho, theta):
        """Convert (rho, theta) line representation into endpoints."""
        length = 2 * self.width
        a, b = np.cos(theta), np.sin(theta)
        x0, y0 = a * rho, b * rho
        x1, y1 = int(x0 + length * (-b)), int(y0 + length * (a))
        x2, y2 = int(x0 - length * (-b)), int(y0 - length * (a))
        return [x1, y1, x2, y2]

    def draw_houghlines(self, image, lines):
        """Draw detected Hough lines on the image."""
        out = image.copy()
        if lines is not None:
            for line in lines:
                for rho, theta in line:
                    x1, y1, x2, y2 = self.calc_coordinates(rho, theta)
                    cv2.line(out, (x1, y1), (x2, y2), (0, 255, 0), 2)
        return out

    def draw_output(self, image, lines=None, intersections=None, board=None, idx=None):
        """Overlay detected grid, intersections, and solution numbers onto the image."""
        out = np.copy(image)
        thick = self.height//200
        l = self.height//100
        if intersections is not None and len(intersections)!=0:
            box_width = box_heigth = abs(intersections[0][0] - intersections[1][0])
            intersections_arr = np.array([[x for x in intersections[i * 10:i * 10 + 10]] for i in range(10)])
            idx = [item for sublist in idx for item in sublist]

            for line in lines['horizontal']:
                (rho, theta) = line
                [x1, y1, x2, y2] = self.calc_coordinates(rho, theta)
                cv2.line(out, (x1, y1), (x2, y2), (0, 255, 255), thick)

            for line in lines['vertical']:
                (rho, theta) = line
                [x1, y1, x2, y2] = self.calc_coordinates(rho, theta)
                cv2.line(out, (x1, y1), (x2, y2), (0, 255, 0), thick)

            for coord in intersections:
                x = coord[0]
                y = coord[1]
                cv2.line(out, (x - l, y), (x + l, y), (255, 0, 255), thick)
                cv2.line(out, (x, y - l), (x, y + l), (255, 0, 255), thick)

        if len(board) != 0:
            for i in range(9):
                temp_list = list()
                for j in range(9):
                    x1 = intersections_arr[i][j][0]
                    y1 = intersections_arr[i][j][1]
                    x2 = x1 + box_width//2
                    y2 = y1 + 3*box_heigth//2
                    cx = (x1 + x2)//2
                    cy = (y1 + y2)//2
                    if (i,j) in idx:
                        cv2.putText(out, str(board[i][j]), (cx,cy), cv2.FONT_HERSHEY_SIMPLEX, int(thick/2), (0,0,255), int(l/2))
        return out

    def separate_lines(self, lines):
        """Separate horizontal and vertical lines detected using Hough Transform."""
        lines_separated = {'horizontal': [], 'vertical': []}

        for line in lines:
            theta_deg = np.rad2deg(line[0][1])
            if 0 <= theta_deg <= 5 or 175 <= theta_deg <= 185:
                lines_separated['vertical'].append(tuple(line[0]))
            elif 85 <= theta_deg <= 95:
                lines_separated['horizontal'].append(tuple(line[0]))

        for key in ['horizontal', 'vertical']:
            lines_separated[key] = sorted(lines_separated[key], key=lambda x: x[0])

        return lines_separated

    def average_lines(self, lines):
        """Merge close parallel lines to obtain a cleaner grid."""
        def merge_lines(line_set):
            """Helper function to merge nearby lines."""
            merged = []
            threshold = self.height // 70

            for rho, theta in line_set:
                close_lines = [(r, t) for r, t in line_set if abs(r - rho) <= threshold]
                median_rho, median_theta = np.median([r for r, _ in close_lines]), np.median([t for _, t in close_lines])
                merged.append((median_rho, median_theta))

            return sorted(set(merged), key=lambda x: x[0])

        return {
            'horizontal': merge_lines(lines['horizontal']),
            'vertical': merge_lines(lines['vertical'])
        }

    def calc_intersection(self, line1, line2):
        """Compute the intersection point of two lines in (rho, theta) form."""
        rho1, theta1 = line1
        rho2, theta2 = line2

        A = np.array([[np.cos(theta1), np.sin(theta1)], [np.cos(theta2), np.sin(theta2)]])
        b = np.array([[rho1], [rho2]])

        x, y = np.linalg.solve(A, b)
        return int(np.round(x)), int(np.round(y))

    def intersections(self, lines):
        """Find all intersections between horizontal and vertical lines."""
        return sorted(
            {self.calc_intersection(h, v) for h in lines['horizontal'] for v in lines['vertical']},
            key=lambda point: (point[1], point[0])
        )

    def calc_idx_printing(self, board):
        """Find indices of empty Sudoku cells (to be filled by the solver)."""
        return [[(i, j) for j, num in enumerate(row) if num == 0] for i, row in enumerate(board)]