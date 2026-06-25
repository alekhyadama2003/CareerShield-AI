"""
CareerShield AI — resume_reader.py
Class: ResumeReader
Loads and extracts text from PDF or TXT resume files.
Tech: Python OOP
"""

import os


class ResumeReader:
    """
    Loads resume files and returns plain text.
    Supports .pdf and .txt formats.
    Falls back between pdfplumber and PyPDF2 for PDF extraction.
    """

    SUPPORTED_FORMATS = (".pdf", ".txt", ".md")

    def load(self, file_path: str) -> str:
        """Auto-detect format and return resume text."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        ext = os.path.splitext(file_path)[1].lower()
        if ext not in self.SUPPORTED_FORMATS:
            raise ValueError(
                f"Unsupported format '{ext}'. Supported: {self.SUPPORTED_FORMATS}"
            )

        if ext == ".pdf":
            return self._read_pdf(file_path)
        return self._read_text(file_path)

    def _read_pdf(self, path: str) -> str:
        # Try pdfplumber (better accuracy)
        try:
            import pdfplumber
            pages = []
            with pdfplumber.open(path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        pages.append(text)
            return "\n".join(pages)
        except ImportError:
            pass

        # Fallback: PyPDF2
        try:
            import PyPDF2
            pages = []
            with open(path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    pages.append(page.extract_text() or "")
            return "\n".join(pages)
        except ImportError:
            raise ImportError(
                "No PDF library found. Install one:\n"
                "  pip install pdfplumber\n"
                "  pip install PyPDF2"
            )

    @staticmethod
    def _read_text(path: str) -> str:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
