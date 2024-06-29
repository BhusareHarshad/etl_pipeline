import tempfile, os
import shutil, subprocess
from crawlers.base import BaseCrawler
from utils.documents import RepositoryDocument
from pymongo import MongoClient
from utils.config import settings

class Github(BaseCrawler):
    model = RepositoryDocument
    def __init__(self, ignore = (".git", ".toml", ".lock", ".png", "node_modules", ".log", ".local")):
        super().__init__()
        self._ignore = ignore
        
    def extract(self, link: str, **kwargs) -> None:
        
        #Make a temporary directory
        temp_dir = tempfile.mkdtemp()
        repo_name = link.rstrip("/").split("/")[-1]
        
        try:
            #change directory and clone repo
            os.chdir(temp_dir)
            subprocess.run(['git', 'clone', link])
            
            repo_path = os.path.join(temp_dir, os.listdir(temp_dir)[0])

            tree = {}
            for root, dirs, files in os.walk(repo_path):
                dir = root.replace(repo_name, '').lstrip("/")
                if dir.startswith(self._ignore):
                    continue
                
                for file in files:
                    if file.endswith(self._ignore):
                        continue
                    file_path = os.path.join(dir, file)
                    with open(os.path.join(root, file), 'r', errors="ignore") as f:
                        tree[file_path] = f.read().replace(" ", "")    
            
            try:
                ##save it in db  
                instance = self.model(
                    name=repo_name, link=link, content=tree, owner_id="user"
                )
                
                ##client creation and adding data
                #TODO: Add in different util and db files 
                client = MongoClient(settings.DATABASE_HOST)
                
                db = client["test1"]
                collection = db[RepositoryDocument.Settings.name]

                # Insert the document
                collection.insert_one(instance.dict(by_alias=True))

                print("Document inserted successfully!")
            except Exception as e:
                print(f"WARNING: Unable to insert in data in database: {e}")
                pass

        except Exception:
            raise
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
        
        
if __name__ == "__main__":
    g = Github()
    g.extract(r'https://github.com/BhusareHarshad/Chrome-Extension-v2.git')

