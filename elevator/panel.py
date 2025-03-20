"""
16.2 ft --> 50 LEDs 
8.1 ft --> 25 LEDs

8' x 3' walls
top left corner is led[0][0]
"""
NUM_LEDS = 300
HEIGHT = 25 # 25 LEDs down 
WIDTH = 12 # 12 LEDs across 
FRAMES = 25 # change to include delay for the ceiling 

DELAY = 500 

def led_to_coords(led_idx, width, height):
    """
    Converts a sequential LED index to (row, col) coordinates in a vertical snake pattern.
    Pattern weaves down then up, moving right one column each time.
    
    Args:
        index: LED index in the sequence
        width: Width of the matrix
        height: Height of the matrix
    
    Returns:
        tuple: (row, col) coordinates in the matrix
    """
    col = led_idx // height
    is_reverse = col % 2 == 1  # True for odd-numbered columns
    
    if is_reverse:
        row = height - 1 - (led_idx % height)
    else:
        row = led_idx % height
        
    return (row, col)

def coords_to_index(row, col, width, height):
    """
    Converts (row, col) coordinates back to the LED index.
    
    Args:
        row: Row in the matrix
        col: Column in the matrix
        width: Width of the matrix
        height: Height of the matrix
    
    Returns:
        int: LED index in the sequence
    """
    if col % 2 == 0:
        return col * height + row
    else:
        return col * height + (height - 1 - row)

def play(timestamp, stay=True): 
    """
    timestamp: what timestamp the LEDs should be on right now
    stay: whether to stay or turn to black immediately 
    """
    # initialize the matrix to all black 
    leds = [['#000000' for _ in range(WIDTH)] for _ in range(HEIGHT)]

    for led in range(NUM_LEDS):
        # for each led we want to transpose the current index to the matrix index (r, c)
        row, col = led_to_coords(led, WIDTH, HEIGHT)

        # given the timestamp and the row, col coordinates
        # set the color of the LED that should be white 
        if row == (HEIGHT - 1) - (timestamp % FRAMES):
            leds[row][col] = '#FFFFFF'
    return leds


def show(led_matrix):
    """
    Displays an LED matrix in a new window using Tkinter.
    
    Args:
        led_matrix: 2D list of colors, where each color is in format '#RRGGBB'
    """
    import tkinter as tk
    from tkinter import ttk
    
    # Create window
    root = tk.Tk()
    root.title("LED Matrix Display")
    
    # Calculate cell size
    CELL_SIZE = 10  # Changed to 10x10 pixels
    
    # Create canvas
    rows, cols = len(led_matrix), len(led_matrix[0])
    canvas = tk.Canvas(
        root,
        width=cols * CELL_SIZE,
        height=rows * CELL_SIZE,
        bg='black'
    )
    canvas.pack(padx=10, pady=10)
    
    # Draw LED matrix
    for i in range(rows):
        for j in range(cols):
            x1 = j * CELL_SIZE
            y1 = i * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE
            
            # Draw rectangle with color from matrix
            canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=led_matrix[i][j],
                outline=''  # Removed outline for cleaner look at small size
            )
    
    # Start the main loop
    root.mainloop()

def show_sequence(led_matrices, delay=0.5):
    """
    Displays a sequence of LED matrices with a delay between each frame.
    Loops continuously through the sequence.
    
    Args:
        led_matrices: List of 2D lists, where each 2D list is a matrix of colors
        delay: Time in seconds between frames (default 0.5 seconds)
    """
    import tkinter as tk
    import time
    
    # Create window
    root = tk.Tk()
    root.title("LED Matrix Animation")
    
    # Calculate cell size
    CELL_SIZE = 10
    
    # Get dimensions from first matrix
    rows, cols = len(led_matrices[0]), len(led_matrices[0][0])
    
    # Create canvas
    canvas = tk.Canvas(
        root,
        width=cols * CELL_SIZE,
        height=rows * CELL_SIZE,
        bg='black'
    )
    canvas.pack(padx=10, pady=10)
    
    def update_display(matrix_index=0):
        # Clear previous display
        canvas.delete("all")
        
        # Draw current matrix
        matrix = led_matrices[matrix_index]
        for i in range(rows):
            for j in range(cols):
                x1 = j * CELL_SIZE
                y1 = i * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                
                canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=matrix[i][j],
                    outline=''
                )
        
        # Schedule next update, wrapping around to 0 when reaching the end
        next_index = (matrix_index + 1) % len(led_matrices)
        root.after(int(delay * 1000), lambda: update_display(next_index))
    
    # Start the animation
    update_display()
    
    # Start the main loop
    root.mainloop()

def main():
    # Example: Create a simple animation of a moving red dot
    size = 100
    frames = []
    
    # Create 5 frames with a red dot moving diagonally
    for i in range(5):
        matrix = [['#000000' for _ in range(size)] for _ in range(size)]
        matrix[i][i] = '#FF0000'  # Red dot
        frames.append(matrix)
    
    # Show the animation
    show_sequence(frames, delay=0.2)

def test_coords():
    leds = play(0)
    print(leds)
    # for ts in range(100):
    #     play(ts)

if __name__ == "__main__":
    # main()
    test_coords()