## content-extract-routine
Local desktop Python application to extract file content into text format and upload it to Azure Blob Storage.

### Python version:
```
Python 3.9.16
pip 25.1.1
```
### Additional application dependencies:
Text OCR - Tesseract Server
Install Tesseract from
[https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki)
(is not a replacement for the Python library)


### JSON file sample payload:
```
{
	"url": "c:\\Users\\Eugene\\Downloads\\Materials\\Sources\\00_afh_full (Airplane Flying Handbook (FAA-H-8083-3C)).pdf",
	"filename": "00_afh_full (Airplane Flying Handbook (FAA-H-8083-3C)).pdf",
	"page_number": 40,
	"image_index": 2,
	"chunk_id": 1,
	"title": "00 afh full (Airplane Flying Handbook (FAA H 8083 3 C))",
	"content": "This is a sample content of a file",
	"last_updated": "20250519124828",
	"keywords": "",
	"vectors": ""
}
```

### Backlog
1. Base64 'folder name' should contain relative path
2. Add 'filepath' as a searchable field (remove slashes, word sequence); Currently used as a reference for OpenAI Chats.

