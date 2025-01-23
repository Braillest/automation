import os
import math
import sys
import re

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
        self.tolerance = 0.2
        self.plate_z = 1
        self.dot_radius = 0.75
        self.dot_z_size = 0.5

        # The offset of the dots
        self.dot_x_offset = 1.75
        self.dot_y_offset = 2.50

        # The spacing of the dots
        self.dot_x_spacing = 2.5
        self.dot_y_spacing = 2.5

        # Page size
        self.page_x_size = 215.9 # 8.5 in
        self.page_y_size = 279.4 # 11 in

        # Character size
        self.character_x_size = 6
        self.character_y_size = 10

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

    def generate_page_plate(self, page_path):

        if not fusion_library_is_installed:
            sys.exit("Missing fusion packages")
            return

        app = adsk.core.Application.get()
        ui = app.userInterface
        ui.messageBox('Hi')
        design = app.activeProduct

        # Get the root component of the active design
        root_component = design.rootComponent

        # Create a new sketch on the XY plane
        sketches = root_component.sketches
        xyPlane = root_component.xYConstructionPlane
        sketch = sketches.add(xyPlane)

        for line_index, line in enumerate(page):
            for character_index, character in enumerate(line):
                self.sketch_braille_character(sketch, line_index, character_index, character)

    def sketch_braille_character(self, sketch, line_index, character_index, character):

        if not fusion_library_is_installed:
            sys.exit("Missing fusion packages")
            return

        sketchLines = sketch.sketchCurves.sketchLines

        # p1 p4
        # p2 p3

        p1, p2, p3, p4 = self.calculate_character_cell_points(line_index, character_index)

        # Draw cell bounding box
        line1 = sketchLines.addByTwoPoints(p1, p2)
        line2 = sketchLines.addByTwoPoints(p2, p3)
        line3 = sketchLines.addByTwoPoints(p3, p4)
        line4 = sketchLines.addByTwoPoints(p4, p1)

        # Extrude cell
        app = adsk.core.Application.get()
        ui = app.userInterface
        ui.messageBox('Hi')
        design = app.activeProduct
        root_component = design.rootComponent
        profiles = sketch.profiles
        cell_profile = profiles.item(0)
        amount = adsk.core.ValueInput.createByReal(self.plate_z)
        cell_extrusion = root_component.features.extrudeFeatures.addSimple(cell_profile, amount, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        cell_body = cell_extrusion.bodies.item(0)
        cell_body.name = "{line_index}:{character_index}"

        # d1 d4
        # d2 d5
        # d3 d6

        d1, d2, d3, d4, d5, d6 = self.calculate_character_dot_points(line_index, character_index)

        # Conditionally draw dots
        delta = int(format(ord(self.space_character), "x")) - int(format(ord(character), "x"))
        binary = f'{delta:08b[::-1]}' # reverse to little endian
        if binary[0]:
            sketch.sketchCurves.sketchCircles.addByCenterRadius(d1, self.dot_radius)
            sketch.sketchCurves.sketchCircles.addByCenterRadius(d1, self.dot_radius + self.tolerance)
        if binary[1]:
            sketch.sketchCurves.sketchCircles.addByCenterRadius(d2, self.dot_radius)
            sketch.sketchCurves.sketchCircles.addByCenterRadius(d2, self.dot_radius + self.tolerance)
        if binary[2]:
            sketch.sketchCurves.sketchCircles.addByCenterRadius(d3, self.dot_radius)
            sketch.sketchCurves.sketchCircles.addByCenterRadius(d3, self.dot_radius + self.tolerance)
        if binary[3]:
            sketch.sketchCurves.sketchCircles.addByCenterRadius(d4, self.dot_radius)
            sketch.sketchCurves.sketchCircles.addByCenterRadius(d4, self.dot_radius + self.tolerance)
        if binary[4]:
            sketch.sketchCurves.sketchCircles.addByCenterRadius(d5, self.dot_radius)
            sketch.sketchCurves.sketchCircles.addByCenterRadius(d5, self.dot_radius + self.tolerance)
        if binary[5]:
            sketch.sketchCurves.sketchCircles.addByCenterRadius(d6, self.dot_radius)
            sketch.sketchCurves.sketchCircles.addByCenterRadius(d6, self.dot_radius + self.tolerance)

    # Utility Methods

    def calculate_character_cell_points(self, line_index, character_index):

        if not fusion_library_is_installed:
            sys.exit("Missing fusion packages")
            return

        # p1 p4
        # p2 p3

        # calculate x, y of p1
        x_offset = self.line_x_offset + (self.character_x_count - character_index) * self.character_x_size
        y_offset = self.line_y_offset + (self.character_y_count - line_index) * self.character_y_size

        p1 = adsk.core.Point3D.create(x_offset, y_offset, 0)
        p2 = adsk.core.Point3D.create(x_offset, y_offset - self.character_y_size, 0)
        p3 = adsk.core.Point3D.create(x_offset + self.character_x_size, y_offset - self.character_y_size, 0)
        p4 = adsk.core.Point3D.create(x_offset + self.character_x_size, y_offset, 0)

        return p1, p2, p3, p4

    def calculate_character_dot_points(self, line_index, character_index):

        if not fusion_library_is_installed:
            sys.exit("Missing fusion packages")
            return

        # d1 d4
        # d2 d5
        # d3 d6

        # calculate x, y of d1
        x_offset = self.line_x_offset + ((self.character_x_count - character_index) * self.character_x_size) + self.dot_x_offset
        y_offset = self.line_y_offset + ((self.character_y_count - line_index) * self.character_y_size) - self.dot_y_offset

        d1 = adsk.core.Point3D.create(x_offset, y_offset, 0)
        d2 = adsk.core.Point3D.create(x_offset, y_offset - self.dot_spacing, 0)
        d3 = adsk.core.Point3D.create(x_offset, y_offset - (self.dot_spacing * 2), 0)
        d4 = adsk.core.Point3D.create(x_offset + self.dot_spacing, y_offset, 0)
        d5 = adsk.core.Point3D.create(x_offset + self.dot_spacing, y_offset - self.dot_spacing, 0)
        d6 = adsk.core.Point3D.create(x_offset + self.dot_spacing, y_offset - (self.dot_spacing * 2), 0)

        return d1, d2, d3, d4, d5, d6

    def union_all_bodies_in_component(component):

        if not fusion_library_is_installed:
            sys.exit("Missing fusion packages")
            return

        # Validate component body count
        bodies = component.bRepBodies
        if bodies.count < 2:
            return

        # Needed vars to create feature input
        combine_features = component.features.combineFeatures
        target_body = bodies.item(0)
        tool_bodies = adsk.core.ObjectCollection.create()
        for z in range(1, bodies.count):
            tool_bodies.add(bodies.item(z))

        # Create feature input
        combine_input = combine_features.createInput(target_body, tool_bodies)
        combine_input.isKeepToolBodies = False
        combine_input.isNewComponent = False
        combine_input.operation = adsk.fusion.FeatureOperations.JoinFeatureOperation
        combine_features.add(combine_input)
