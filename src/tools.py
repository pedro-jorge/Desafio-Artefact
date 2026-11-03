from functools import lru_cache

from langchain.tools import tool
from langchain_docling.loader import DoclingLoader, ExportType

from config import settings

@lru_cache()
def _load_pdf_text() -> str:
    loader = DoclingLoader(
        file_path=settings.PDF_PATH,
        export_type=ExportType.MARKDOWN,
    )
    docs = loader.load()
    
    return "\n\n".join(d.page_content.strip() for d in docs)

@tool
def get_document() -> str:
    return _load_pdf_text()