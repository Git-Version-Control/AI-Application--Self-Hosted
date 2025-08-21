from pymilvus import Collection,connections,db
from ..vector_db.model import document_colllection_schema
import uuid
import tiktoken
from typing import List

class IngestionManager():
    def __init__(self, collection_name,partition_name):
        self.collection_name = collection_name
        self.partition_name = partition_name
        self.connect()

    def connect(self):
        self.connection = connections.connect(alias="default", host='localhost', port='19530')
        self.database = db.Database("BasicRAG")
        if not self.database.has_database("BasicRAG"):
            self.database.create_database("BasicRAG")
        self.collection = Collection(name=self.collection_name, schema=document_colllection_schema)
        self.partition = (self.collection.create_partition(self.partition_name) 
                  if self.partition_name not in self.collection.list_partitions() 
                  else self.collection.get_partition(self.partition_name))
        
    # since FieldSchema(name='id', dtype=DataType.VARCHAR, max_length=200,
                #             description='Ids', is_primary=True, auto_id=False),
                # FieldSchema(name='source_name', dtype=DataType.VARCHAR,
                #             description='Document or website name', max_length=200),
                # FieldSchema(name='source_type', dtype=DataType.VARCHAR,
                #             description='Type of the Document or Source given', max_length=200) 
                # are common for any no of chunk generated for that document or website
    # generate these metadata fields for each document or website 


    def add_metadata(self, source_name, source_type,language):
        metadata = {
            'id': uuid.uuid4(),
            'source_name': source_name,
            'source_type': source_type,
            'language': language
        }
        self.collection.insert([metadata], partition_name=self.partition_name)
        return metadata['id']
    


    async def generate_chunk(self, file: str) -> List[str]:
        try:
            # Initialize tokenizer
            tokenizer = tiktoken.get_encoding("cl100k_base")
            
            # Read file content
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Tokenize content
            tokens = tokenizer.encode(content)
            
            # Initialize variables
            chunks = []
            chunk_size = 500
            current_position = 0
            
            # Split into chunks
            while current_position < len(tokens):
                # Get chunk of 500 tokens
                chunk_tokens = tokens[current_position:current_position + chunk_size]
                # Convert tokens back to text
                chunk_text = tokenizer.decode(chunk_tokens)
                # Add to chunks array
                chunks.append(chunk_text)
                # Move position
                current_position += chunk_size
                
            return chunks
            
        except Exception as e:
            print(f"Error processing file {file}: {str(e)}")
            return []
        
    def create_and_store_embeddings(self, chunks: List[str], doc_id: str) -> bool:
    try:
        # Initialize OpenAI client
        client = OpenAI()
        
        # Process chunks in batches
        batch_size = 100
        embeddings = []
        
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            
            # Generate embeddings
            response = client.embeddings.create(
                model="text-embedding-3-small",
                input=batch
            )
            
            # Extract embedding vectors
            batch_embeddings = [item.embedding for item in response.data]
            embeddings.extend(batch_embeddings)
            
        # Prepare data for storage
        documents = []
        for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            doc = {
                "id": f"{doc_id}_{idx}",
                "doc_id": doc_id,
                "chunk_index": idx,
                "content": chunk,
                "vector": embedding
            }
            documents.append(doc)
            
        # Store in vector database with partition
        self.vector_store.add_documents(
            documents,
            partition_key="doc_id",
            partition_value=doc_id
        )
        
        return True
        
    except Exception as e:
        print(f"Error creating embeddings: {str(e)}")
        return False
    