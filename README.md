# Image Recognition Sudoku Solver

## 📌 Goal
The goal of this project is to develop a robust Sudoku solver that can:
- Detect a Sudoku grid from an image.
- Extract and recognize digits from each cell.
- Solve the puzzle using a backtracking algorithm.
- Display the solved Sudoku with correctly placed numbers.

## 🚀 Challenges
During the development of this project, several challenges were encountered:
- **Grid Detection**: Extracting the Sudoku grid accurately despite distortions and lighting conditions.
- **Digit Recognition**: Improving OCR performance to correctly identify numbers.
- **Number Placement**: Ensuring extracted numbers align correctly with grid cells.
- **Solving Efficiency**: Optimizing the backtracking algorithm for faster solutions.

## 🔬 Methodology
The project follows a structured approach:
1. **Preprocessing**: Convert the image to grayscale and apply edge detection.
2. **Grid Detection**: Use Hough Transform to detect horizontal and vertical grid lines.
3. **Intersection Extraction**: Compute the intersections to define the grid cells.
4. **Digit Recognition**: Utilize Tesseract OCR to extract numbers from cells.
5. **Sudoku Solving**: Implement a backtracking algorithm to fill in missing numbers.
6. **Result Visualization**: Draw the solved Sudoku grid on the original image.

## 📊 Results
- Successfully detects Sudoku grids from various images.
- Extracted numbers align correctly within grid cells.
- Solves most puzzles efficiently within seconds.
- Outputs a visually clear solved Sudoku.

## 📜 Credits
The Sudoku-solving logic was inspired by solutions from various sources, including:
- [GitHub Gist - Evangelos Zafeiratos](https://gist.github.com/evangelos-zafeiratos)

---
🛠 Built with Python, OpenCV, and Tesseract OCR.
