
import os
from app import retriever

def test_db_creation(tmp_path):
    os.environ['METADATA_DB'] = str(tmp_path / 'test_metadata.db')
    retriever.init_db()
    assert os.path.exists(os.environ['METADATA_DB'])
