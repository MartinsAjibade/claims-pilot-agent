"""Convert policy documents to markdown using IBM Docling (layout-aware parsing)."""

from __future__ import annotations

from pathlib import Path


def parse_document_to_markdown(source: str | Path) -> str:
    """
    Parse a PDF, DOCX, or other Docling-supported file into markdown text.

    Raises if the file is missing or conversion fails.
    """
    path = Path(source).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"Policy document not found: {path}")

    try:
        from docling.document_converter import DocumentConverter
    except ImportError as e:
        raise ImportError(
            "Docling is not installed. Add the extra: pip install 'claim-pilot-ai[docling]'"
        ) from e

    converter = DocumentConverter()
    result = converter.convert(path)
    return result.document.export_to_markdown()
