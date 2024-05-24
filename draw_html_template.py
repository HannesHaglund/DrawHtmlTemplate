from typing import List, Tuple
import argparse
import os
import imgkit
import logging

LOGGER = logging.getLogger("DRAW_HTML_TEMPLATE")
FNAME_ZEROS = 5
HTML_FILE_PATH_START = 'file://localhost/'


def absolute_path(path):
    script_folder = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(script_folder, path)


def file_path(path):
    s = HTML_FILE_PATH_START + absolute_path(path)
    if os.sep == "\\":
        return s.replace("\\", "/")
    else:
        return s

def read_file_as_string(file_name):
    with open(file_name, 'r') as file:
        return file.read()
    assert False, "Unreachable code"


def write_string_to_file(string, file_name):
    with open(file_name, "w") as f:
        f.write(string)


def swap_double_curly_brackets_and_curly_brackets(string):
    double_curly_left_uuid = "9e6bea3f-4dae-46c7-a16e-2f0dadf805f3"
    double_curly_right_uuid = "4497e56c-8f69-4a51-8bef-934cdc57f9fd"
    s = string
    s = s.replace("{{", double_curly_left_uuid)
    s = s.replace("}}", double_curly_right_uuid)
    s = s.replace("{", "{{")
    s = s.replace("}", "}}")
    s = s.replace(double_curly_left_uuid, "{")
    s = s.replace(double_curly_right_uuid, "}")
    return s


class HtmlInfo:
    def __init__(self, file_path, x, y, width, height, out_format, output_dir):
        # Attempt to sanitize file_path, so it can use the same format as html paths
        self.file_path = file_path.lstrip(HTML_FILE_PATH_START)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.out_format = out_format
        self.output_dir = output_dir


def draw_html_template(html_info, **kwargs):
    # Function call counter
    draw_html_template.counter += 1

    # Replace args in html
    html = read_file_as_string(html_info.file_path)
    html = swap_double_curly_brackets_and_curly_brackets(html)
    html = html.format(**kwargs)

    # Get file name
    fname = str(draw_html_template.counter).zfill(FNAME_ZEROS)
    out_name_without_ext = os.path.join(html_info.output_dir, fname + '.')
    img_out_name = out_name_without_ext + html_info.out_format
    html_out_name = out_name_without_ext + 'html'

    # Check if we need to continue
    old_html = read_file_as_string(html_out_name) if os.path.isfile(html_out_name) else ""
    if old_html == html:
        LOGGER.info("{} unchanged. Skipping.".format(html_out_name))
        return

    # Write html
    write_string_to_file(html, html_out_name)
    LOGGER.info("Wrote {}".format(html_out_name))

    # Write image output file
    options= {
        'format': html_info.out_format,
        'width': html_info.width,
        'height': html_info.height,
        'crop-w': html_info.width,
        'crop-h': html_info.height,
        'crop-x': html_info.x,
        'crop-y': html_info.y,
        'quality': 30,
        'encoding': 'UTF-8',
        'enable-local-file-access': '',
        'disable-smart-width': ''
    }
    imgkit.from_file(html_out_name, img_out_name, options=options)
    LOGGER.info("Wrote {}".format(img_out_name))

# Initialize counter
draw_html_template.counter = 0
