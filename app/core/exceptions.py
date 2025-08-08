from fastapi import HTTPException, status

OrganizationNotFound = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Организация не найдена")
ActivityNotFound = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Деятельность не найдена")
BuildingNotFound = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Здание не найдено")
NoAPIKey = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Отсутсвует API key")
WrongAPIKey = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный API key")
ParentActivityNotFound = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                       detail="Родительская деятельность не найдена")
MaxLevelReached = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Максимальная вложенность достигнута")
