import uuid
from fastapi import  File, UploadFile, APIRouter
from pymilvus import Collection
from .vector_db.model import document_colllection_schema
from .util.pre_process import preprocess_filename,type_of_document
from .ingestion.ingestion_handler import IngestionManager

router = APIRouter(prefix='/document')

@router.post('/upload')
async def upload_file(file: UploadFile = File(...),lanaguage:str='en'):
    filename = preprocess_filename(file.filename)
    document_type = type_of_document(filename)
    if document_type is None:
        return {"error": "Invalid file type"}

    # create collection and partition
    IngestionManager(collection_name="Test", partition_name=filename)
    
    document_id:uuid=IngestionManager.add_metadata(source_name=filename, source_type=document_type,language=lanaguage)

    # save file to partition


    return {"filename": file.filename}
