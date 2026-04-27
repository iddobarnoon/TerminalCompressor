import os
import dearpygui.dearpygui as dpg
from encoder import encodeFile
from decoder import decompressFile


def file_selected(_, app_data):
    selections = app_data.get("selections", {})
    if selections:
        path = list(selections.values())[0]
        dpg.set_value("file_path", path)
        set_status("")


def set_status(msg, error=False):
    dpg.set_value("status", msg)
    color = (255, 80, 80, 255) if error else (80, 220, 80, 255)
    dpg.configure_item("status", color=color)


def compress_callback():
    path = dpg.get_value("file_path")
    if not path or not os.path.exists(path):
        set_status("Please select a valid file.", error=True)
        return
    try:
        before_kb = os.path.getsize(path) / 1024
        encodeFile(path)
        after_kb = os.path.getsize(path) / 1024
        set_status(f"Compressed: {before_kb:.2f} KB  ->  {after_kb:.2f} KB  ({100 * (1 - after_kb / before_kb):.1f}% smaller)")
    except Exception as e:
        set_status(f"Error: {e}", error=True)


def decompress_callback():
    path = dpg.get_value("file_path")
    if not path or not os.path.exists(path):
        set_status("Please select a valid file.", error=True)
        return
    try:
        before_kb = os.path.getsize(path) / 1024
        decompressFile(path)
        after_kb = os.path.getsize(path) / 1024
        set_status(f"Decompressed: {before_kb:.2f} KB  ->  {after_kb:.2f} KB")
    except Exception as e:
        set_status(f"Error: {e}", error=True)


dpg.create_context()

with dpg.font_registry():
    large_font = dpg.add_font("C:/Windows/Fonts/segoeui.ttf", 24)

with dpg.file_dialog(
    directory_selector=False,
    show=False,
    callback=file_selected,
    tag="file_dialog",
    width=600,
    height=400,
):
    dpg.add_file_extension(".*")
    dpg.add_file_extension(".txt", color=(0, 255, 0, 255))

with dpg.window(tag="main"):
    dpg.add_text("Huffman File Compressor")
    dpg.add_separator()
    dpg.add_spacer(height=30)

    with dpg.group(horizontal=True):
        dpg.add_input_text(tag="file_path", hint="No file selected", width=700, readonly=True, multiline=True, height=80)
        dpg.add_spacer(width=10)
        dpg.add_button(label="Browse", callback=lambda: dpg.show_item("file_dialog"), width=120, height=80)

    dpg.add_spacer(height=40)

    with dpg.group(horizontal=True):
        dpg.add_button(label="Compress", callback=compress_callback, width=280, height=60)
        dpg.add_spacer(width=40)
        dpg.add_button(label="Decompress", callback=decompress_callback, width=280, height=60)

    dpg.add_spacer(height=30)
    dpg.add_text("", tag="status")

dpg.create_viewport(title="Terminal Compressor", width=1000, height=500)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.bind_item_font("file_path", large_font)
dpg.set_primary_window("main", True)
dpg.start_dearpygui()
dpg.destroy_context()
