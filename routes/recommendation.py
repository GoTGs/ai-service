from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError
import os
from typing import Annotated
from dotenv import load_dotenv
from models.recommendation_im import RecommendationIM
from models.recommendation import chain
from db.db import conn, curr

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
router = APIRouter()

public_key = "\n".join(os.getenv("RSAPUBLIC").split("<end>"))

@router.post("/assignment/recommend", tags=["recommendation"])
async def recommend_assignment(token: Annotated[str, Depends(oauth2_scheme)], recommendation_im: RecommendationIM):
    try:
        payload = jwt.decode(token, public_key, algorithms=["RS512"])
        id: str = payload["id"]
        
        curr.execute("""SELECT * FROM users WHERE id = %s""", (id,))
        
        result = curr.fetchone()
        
        if result is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        
        if result["role"].lower() not in ["teacher", "admin"]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to access this resource")

        response = chain.invoke({"keywords": recommendation_im.keywords})   

        # Call the recommendation service here
        return {"response": response}
    
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")