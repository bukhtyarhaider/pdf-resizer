```markdown
# PDF Resizer Project

This project provides a standalone Python script that processes PDF files by resizing each page to a specified paper size using the `PaperSize` class from the `pypdf` library. It reads a PDF from the `input` folder, rotates and scales the pages as needed, and saves both individual page PDFs and a merged PDF into the `processed` folder.

## Features

- **Resize and Rotate:**  
  Adjusts each PDF page to a target paper size (e.g., A4, Letter) and rotates pages if necessary.
  
- **Individual and Merged Outputs:**  
  Saves each processed page as a separate PDF and also merges them into one final PDF.
  
- **Standalone Script:**  
  Processes local files without any external database or cloud upload dependencies.

## Prerequisites

- Python 3.6 or later
- [pypdf](https://pypi.org/project/pypdf/) library

## Installation

1. **Clone the Repository or Download the Source Code:**

   ```bash
   git clone <repository-url>
   cd pdf_processor_project
   ```

2. **Create a Virtual Environment (Recommended):**

   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment:**

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies:**

   Ensure you have a `requirements.txt` file with the following content:

   ```
   pypdf
   ```

   Then, install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

```
pdf_processor_project/
├── input/          # Place your input PDF files here.
├── processed/      # Processed PDFs will be saved here.
├── main.py         # Main Python script for PDF processing.
├── requirements.txt
└── .gitignore
```

## Usage

1. **Add a PDF:**  
   Place a PDF file (e.g., `sample.pdf`) in the `input` folder.

2. **Run the Script:**  
   With your virtual environment activated, run:

   ```bash
   python main.py
   ```

3. **Results:**  
   - The script reads the PDF from the `input` folder.
   - Processes each page by rotating (if needed) and scaling it to the target paper size.
   - Saves individual page PDFs and a merged PDF to the `processed` folder.
   - Outputs the file paths of the processed PDFs in the console.

## Customization

- **Paper Size:**  
  Modify the `size` variable in `main.py` to use different paper sizes (e.g., `"A4"`, `"Letter"`, etc.) as provided by `pypdf.PaperSize`.

- **File Naming:**  
  The script uses a unique token in the file names. Adjust the naming scheme within the script as necessary.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to open an issue or submit a pull request.

## Acknowledgements

- [pypdf](https://pypi.org/project/pypdf/) for the robust PDF processing library.
```

This README provides an overview of the project, setup instructions, usage guidelines, and customization options. You can adjust and expand it as needed for your project.