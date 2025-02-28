import os
import io
import secrets
import urllib.parse
from pypdf import PdfReader, PdfWriter, PaperSize

# Define a dictionary for paper sizes (dimensions in points)
PAPER_SIZES = {
    "A0":    {"width": 2383.94, "height": 3370.39},  # 841 x 1189 mm
    "A1":    {"width": 1683.78, "height": 2383.94},  # 594 x 841 mm
    "A2":    {"width": 1190.55, "height": 1683.78},  # 420 x 594 mm
    "A3":    {"width": 841.89,  "height": 1190.55},  # 297 x 420 mm
}

def resize_process_pdf(pdf_path: str, size: str, order_number: int, file_number: int):
    # Open the PDF file from the local filesystem
    with open(pdf_path, "rb") as f:
        filestream = io.BytesIO(f.read())
    reader = PdfReader(filestream)

    # Create the output directory if it doesn't exist
    processed_dir = "processed"
    if not os.path.exists(processed_dir):
        os.makedirs(processed_dir)

    token = secrets.token_hex(8)
    pdf_page_files = []  # List to hold paths of individual page PDFs
    pdf_merger = PdfWriter()

    # Get target dimensions using PaperSize from pypdf.
    # The size parameter (e.g., "A4") must match an attribute on PaperSize.
    target_width = getattr(PaperSize, size).width
    target_height = getattr(PaperSize, size).height

    for page_index, page in enumerate(reader.pages):
        # Check orientation: if the page is portrait, rotate it
        if page.mediabox.width < page.mediabox.height:
            page = page.rotate(270)
            current_width = float(page.mediabox.height)  # after rotation, width/height swap
            current_height = float(page.mediabox.width)
        else:
            current_width = float(page.mediabox.width)
            current_height = float(page.mediabox.height)

        # Calculate scaling factors
        x_scale = target_width / current_width
        y_scale = target_height / current_height

        # Scale the page
        page.scale(x_scale, y_scale)
        pdf_merger.add_page(page)

        # Write the individual page PDF to the processed folder
        output_page_filename = f"output_{token}_{size}_{page_index}.pdf"
        output_page_path = os.path.join(processed_dir, output_page_filename)
        page_writer = PdfWriter()
        page_writer.add_page(page)
        with open(output_page_path, "wb") as f_out:
            page_writer.write(f_out)
        pdf_page_files.append(output_page_path)

    # Write the merged PDF file to the processed folder
    merged_pdf_filename = f"Order{order_number}_File{file_number}.pdf"
    merged_pdf_path = os.path.join(processed_dir, merged_pdf_filename)
    with open(merged_pdf_path, "wb") as f_out:
        pdf_merger.write(f_out)

    return merged_pdf_path, pdf_page_files

if __name__ == '__main__':
    # Ensure the input folder exists and a sample PDF is provided
    input_dir = "input"
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)
        print("Please add a PDF file to the 'input' folder and run the script again.")
        exit(1)

    input_pdf = os.path.join(input_dir, "sample.pdf")
    if not os.path.isfile(input_pdf):
        print(f"File {input_pdf} not found. Please add a PDF named 'sample.pdf' in the 'input' folder.")
        exit(1)

    size = "A2"          # Use an attribute from PaperSize (e.g., "A4", "Letter", etc.)
    order_number = 123
    file_number = 1

    merged_path, page_files = resize_process_pdf(input_pdf, size, order_number, file_number)

    print("Merged PDF saved at:", merged_path)
    print("Individual page files:")
    for file in page_files:
        print(" -", file)
