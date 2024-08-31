from fastapi import HTTPException
from ..models.YobNamesList import YobNamesList
from typing import List

def get_names_list(limit:int, offset:int, name:str ) -> List[str]:
    if name is None:
        documents = YobNamesList.objects.skip(offset).limit(limit)
        names_list = [doc.name for doc in documents]
    else:
        name_lower = name.lower()
        regex_name = f".*{name_lower}.*"
        results = YobNamesList.objects(name__regex=regex_name, name__icontains=name_lower)
        names_list = [doc.name for doc in results]
        if len(names_list) == 0:
            raise HTTPException(status_code=404, detail=str("Not found"))
    return names_list