import cv2
import numpy as np
from src.detection import Detection
from src.read import Read
from src.solve import Solve


def main():
    """
    Main function to read, process, solve, and display a Sudoku puzzle.
    """
    # Load and preprocess the image
    img = cv2.imread('Images/sudoku1.png')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Detect Sudoku grid
    detect = Detection(img)
    edges = cv2.Canny(blur, 50, 200, apertureSize=3)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=200)
    lines_separated = detect.separate_lines(lines)
    lines_averaged = detect.average_lines(lines_separated)
    intersections = detect.intersections(lines_averaged)

    # Read Sudoku numbers
    read = Read()
    _, binary = cv2.threshold(blur, 200, 255, cv2.THRESH_BINARY)
    board = read.collect_numbers(img, binary, intersections)
    idx = detect.calc_idx_printing(board)

    # Solve Sudoku
    solver = Solve(board)
    solution = []
    if solver.solve_sudoku():
        solution = solver.return_board()

    # Display results
    output = detect.draw_output(img, lines_averaged, intersections, solution, idx)
    cv2.imshow('Input', img)
    cv2.imshow('Output', output)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()