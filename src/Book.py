import os
import math
import sys
import re
import time

# Conditionally import custom louis library

louis_library_is_installed = True
try:
    import louis
except:
    louis_library_is_installed = False

# Conditionally import autodesk packages

fusion_library_is_installed = True
try:
    import adsk.core, adsk.fusion, adsk.cam, traceback
except:
    fusion_library_is_installed = False

# Define fusion entrypoint method

# IMPORTANT: Right click root element in browser tree and click "Do not capture Design History" for performance
# IMPORTANT: Grid settings to Fixed, 1000 mm x 5 by preference
# IMPORTANT: Only layout grid checkbox enabled
# IMPORTANT: Control + 7 to enter wireframe render

def run(context):
    book = Book()
    book.pages_directory_path = "C:\\Users\\ramit\\AppData\\Roaming\\Autodesk\\Autodesk Fusion 360\\API\\Scripts\\braillest\\data\\revised-pages\\"
    book.generate_page_plates()

# Notes:

# Braille characters are binary in little endian
# x1 x4
# x2 x5
# x3 x6

# x1 x2 x3 x4 x5 x6

# U+2800 - "⠀", first character
# U+283F - "⠿", last character

# Fusion uses right hand cartesian coords
# Lines are generated top to bottom, left to right, where the bottom left of page is the origin

# Negative mold is +tolerance larger

class Book:

    def __init__(self):

        # Instance variables
        self.text_path = None
        self.text_lines = None
        self.braille_path = None
        self.braille_lines = None
        self.back_translation_path = None
        self.back_translation_lines = None
        self.formatted_braille_path = None
        self.formatted_braille_lines = None
        self.pages_directory_path = None
        self.translation_table = ["braille-patterns.cti", "en-us-g2.ctb"]

        # Special operator booleans
        self.remove_trailing_whitespace = True

        # Begin of assembly config
        self.tolerance = 0.2 / 10
        self.plate_z = 1 / 10
        self.dot_radius = 0.75 / 10
        self.dot_z_size = 0.5 / 10

        # The offset of the dots
        self.dot_x_offset = 1.75 / 10
        self.dot_y_offset = 2.50 / 10

        # The spacing of the dots
        self.dot_x_spacing = 2.5 / 10
        self.dot_y_spacing = 2.5 / 10

        # Page size
        self.page_x_size = 215.9 / 10 # 8.5 in
        self.page_y_size = 279.4 / 10 # 11 in

        # Character size
        self.character_x_size = 6 / 10
        self.character_y_size = 10 / 10

        # Caculate the max size character grid given constraints
        # - 2 for 1 character border
        self.character_x_count = math.floor(self.page_x_size / self.character_x_size) - 2
        self.character_y_count = math.floor(self.page_y_size / self.character_y_size) - 2

        # The offset of the lines within the page
        self.line_x_offset = (self.page_x_size - (self.character_x_count * self.character_x_size)) / 2
        self.line_y_offset = (self.page_y_size - (self.character_y_count * self.character_y_size)) / 2

        # Hardcoded space character
        self.space_character = "⠀"

    # Load Methods

    def load_text_file(self):

        if self.text_path is None:
            pass

        if not os.path.exists(self.text_path) or not os.path.isfile(self.text_path):
            pass

        with open(self.text_path, "r") as text_file:
            self.text_lines = text_file.readlines()
            if not self.text_lines:
                pass

    def load_braille_file(self):

        if self.braille_path is None:
            pass

        if not os.path.exists(self.braille_path) or not os.path.isfile(self.braille_path):
            pass

        with open(self.braille_path, "r") as braille_file:
            self.braille_lines = braille_file.readlines()
            if not self.braille_lines:
                pass

    def load_back_translation_file(self):

        if self.back_translation_path is None:
            pass

        if not os.path.exists(self.back_translation_path) or not os.path.isfile(self.back_translation_path):
            pass

        with open(self.back_translation_path, "r") as back_translation_file:
            self.back_translation_lines = back_translation_file.readlines()
            if not self.back_translation_lines:
                pass

    def load_formatted_braille_file(self):

        if self.formatted_braille_path is None:
            pass

        if not os.path.exists(self.formatted_braille_path) or not os.path.isfile(self.formatted_braille_path):
            pass

        with open(self.formatted_braille_path, "r") as formatted_braille_file:
            self.formatted_braille_lines = formatted_braille_file.readlines()
            if not self.formatted_braille_lines:
                pass

    # Write Methods

    def translate_text_file_to_braille(self):

        if not louis_library_is_installed:
            sys.exit("Missing louis library")

        self.load_text_file()

        with open(self.braille_path, "w") as braille_file:
            for line in self.text_lines:

                if self.remove_trailing_whitespace:
                    line = line.rstrip()

                braille_file.write(louis.translateString(self.translation_table, line) + "\n")

    def back_translate_braille_file_to_text(self):

        if not louis_library_is_installed:
            sys.exit("Missing louis library")

        self.load_braille_file()

        with open(self.back_translation_path, "w") as back_translation_file:
            for line in self.braille_lines:

                if self.remove_trailing_whitespace:
                    line = line.rstrip()

                back_translation_file.write(louis.backTranslateString(self.translation_table, line) + "\n")

    # Formatted Braille Methods

    def format_braille_file(self):

        # Chunk text
        pattern = r"([^\n]+(?:\n[^\n]+)*)"
        text = "".join(self.braille_lines)
        matches = re.finditer(pattern, text)
        offset = 0

        for match in matches:

            # Convert list of text to string
            match_text = match.group(0).replace("\n", self.space_character)
            match_words = match_text.split(self.space_character)

            # Paginate
            current_line = ""
            wrapped_lines = []

            # Iterate through each word
            for word in match_words:

                word_len = len(word)

                # Check if incoming word can fit
                if len(current_line) + word_len + 1 <= self.character_x_count:

                    # If it's not the first word, prepend a space
                    if current_line:
                        current_line += self.space_character

                    current_line += word

                # Incoming word cannot fit
                else:
                    # Special conditional for braille line break
                    if word_len < self.character_x_count:
                        wrapped_lines.append(current_line)

                    current_line = word

            # Add the last line if exists
            if current_line:
                wrapped_lines.append(current_line)

            wrapped_text = "\n".join(wrapped_lines)
            start = match.start() + offset
            end = match.end() + offset
            text = text[:start] + wrapped_text + text[end:]
            delta = len(wrapped_text) - len(match_text)
            offset += delta

        local_braille_lines = text.split("\n")

        with open(self.formatted_braille_path, "w") as formatted_braille_file:
            for line in local_braille_lines:
                formatted_braille_file.write(line + "\n")

    def paginate_formatted_braille_file(self):

        pages = []
        current_page = []
        current_page_size = 0

        # TODO:
        # Alter pagination to prevent dividing table of contents lines from their page number / page breaking within a line

        for line_index, line in enumerate(self.formatted_braille_lines):

            if line.strip() != '' or current_page:
                current_page_size += 1
                current_page.append(line)

            if len(current_page) >= self.character_y_count:

                # Chunk text
                pattern = r"([^\n]+(?:\n[^\n]+)*)"
                text = "".join(current_page)
                matches = list(re.finditer(pattern, text))
                last_match_text = matches[-1].group(0).replace("\n", self.space_character)
                line_break_string = "⠿" * self.character_x_count

                # Handle case that line break occurs at end of page.
                if line_break_string in last_match_text:

                    # Remove line_break_string from current page,
                    # Add current page to output
                    # Start new page with line_break_string
                    current_page = current_page[:current_page_size - 1]
                    pages.append(current_page)
                    current_page = [line]
                    current_page_size = 1
                    continue

                # Add page, reset current page
                pages.append(current_page)
                current_page = []
                current_page_size = 0

        if current_page:
            pages.append(current_page)

        # Remove pages from dir
        for filename in os.listdir(self.pages_directory_path):
            file_path = os.path.join(self.pages_directory_path, filename)
            if os.path.isfile(file_path) and not os.path.basename(file_path).startswith("."):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                print(f"Skipping directory: {file_path}")

        # Write pages to dir
        for index, page in enumerate(pages):
            with open(f"{self.pages_directory_path}{index + 1}.txt", "w") as out_file:
                for line in page:
                    out_file.write(line)

    # Entry methods

    def test(self):

        self.text_path = "/root/src/revisions/Anne of Green Gables by L. M.  Montgomery (469)"
        self.braille_path = "/root/src/braille.txt"
        self.formatted_braille_path = "/root/src/formatted_braille.txt"
        self.back_translation_path = "/root/src/back_translation.txt"

        self.load_text_file()
        self.translate_text_file_to_braille()

        self.back_translate_braille_file_to_text()
        self.load_back_translation_file()

        self.load_formatted_braille_file()
        pages = self.paginate_formatted_braille_file()

        for index, page in enumerate(pages):
            with open(f"/root/src/pages/{index}.txt", "w") as out_file:
                for line in page:
                    out_file.write(line)

    def fusion_debug(self, message):
        app = adsk.core.Application.get()
        ui = app.userInterface
        ui.messageBox(message)

    profile_index = 0
    sketch = None
    point3d = None
    cell_points = []
    dot_points = []

    def generate_page_plates(self):

        if not fusion_library_is_installed:
            sys.exit("Missing fusion packages")
            return

        app = adsk.core.Application.get()
        design = app.activeProduct
        self.point3d = adsk.core.Point3D

        # Get the root component of the active design
        root_component = design.rootComponent

        # Create a new sketch on the XY plane
        sketches = root_component.sketches
        xyPlane = root_component.xYConstructionPlane
        lines = None

        with open(self.pages_directory_path + "1.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()

        page_line = (self.character_x_count - 6) * self.space_character + "⠰⠏⠼⠚⠚⠚"
        lines.append(page_line)

        start = time.time_ns()

        for line_index, line in enumerate(lines):

            sketch = sketches.add(xyPlane)
            sketch.isVisible = False

            # Strip newline character and skip if line is now empty
            line = line.rstrip("\n")
            if line == "":
                continue

            for character_index, character in enumerate(line):

                # Cell calculations
                x_offset = self.line_x_offset + (character_index * self.character_x_size)
                y_offset = self.line_y_offset + ((self.character_y_count - line_index) * self.character_y_size)
                p1 = self.point3d.create(x_offset, y_offset, 0)
                p3 = self.point3d.create(x_offset + self.character_x_size, y_offset - self.character_y_size, 0)
                self.cell_points.append([p1, p3])

                # Dot calculations
                delta = ord(character) - ord(self.space_character)
                binary = f"{delta:06b}"[::-1] # reverse to little endian
                x_offset += self.dot_x_offset
                y_offset -= self.dot_y_offset
                if binary[0] == "1":
                    d1 = self.point3d.create(x_offset, y_offset, 0)
                    self.dot_points.append([d1, self.dot_radius])
                    self.dot_points.append([d1, self.dot_radius + self.tolerance])
                if binary[1] == "1":
                    d2 = self.point3d.create(x_offset, y_offset - self.dot_y_spacing, 0)
                    self.dot_points.append([d2, self.dot_radius])
                    self.dot_points.append([d2, self.dot_radius + self.tolerance])
                if binary[2] == "1":
                    d3 = self.point3d.create(x_offset, y_offset - (self.dot_y_spacing * 2), 0)
                    self.dot_points.append([d3, self.dot_radius])
                    self.dot_points.append([d3, self.dot_radius + self.tolerance])
                if binary[3] == "1":
                    d4 = self.point3d.create(x_offset + self.dot_x_spacing, y_offset, 0)
                    self.dot_points.append([d4, self.dot_radius])
                    self.dot_points.append([d4, self.dot_radius + self.tolerance])
                if binary[4] == "1":
                    d5 = self.point3d.create(x_offset + self.dot_x_spacing, y_offset - self.dot_y_spacing, 0)
                    self.dot_points.append([d5, self.dot_radius])
                    self.dot_points.append([d5, self.dot_radius + self.tolerance])
                if binary[5] == "1":
                    d6 = self.point3d.create(x_offset + self.dot_x_spacing, y_offset - (self.dot_y_spacing * 2), 0)
                    self.dot_points.append([d6, self.dot_radius])
                    self.dot_points.append([d6, self.dot_radius + self.tolerance])

            sketchCurves = sketch.sketchCurves

            sketchCircles = sketchCurves.sketchCircles
            for point, radius in self.dot_points:
                sketchCircles.addByCenterRadius(point, radius)

            # sketchLines = sketchCurves.sketchLines
            # for p1, p3 in self.cell_points:
            #     sketchLines.addTwoPointRectangle(p1, p3)

            x1 = self.line_x_offset
            y1 = self.line_y_offset + ((self.character_y_count - line_index) * self.character_y_size)
            x2 = x1 + (self.character_x_size * self.character_x_count)
            y2 = y1 - self.character_y_size
            p1 = self.point3d.create(x1, y1, 0)
            p3 = self.point3d.create(x2, y2, 0)
            sketchCurves.sketchLines.addTwoPointRectangle(p1, p3)

            self.dot_points = []
            self.cell_points = []

        sketch = sketches.add(xyPlane)
        sketch.isVisible = False
        p1 = self.point3d.create(0, 0, 0)
        p3 = self.point3d.create(self.page_x_size, self.page_y_size, 0)
        sketch.sketchCurves.sketchLines.addTwoPointRectangle(p1, p3)

        end = time.time_ns()
        difference = end - start
        self.fusion_debug(f"{difference / 1000000000} s")

        for sketch in root_component.sketches:
            sketch.isVisible = True
