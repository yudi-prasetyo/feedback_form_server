from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import List
from .models import engine
from .crud import create_feedback, get_feedback
from .schemas import Feedback, FeedbackCreate

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def get_db() -> AsyncSession:
    """
    Asynchronous function to establish a database session.

    This function creates a new database session using the `sessionmaker`
    function from SQLAlchemy. It uses the `engine` object to connect to the
    database, and sets `expire_on_commit=False` to prevent the session from
    expiring when a commit is performed. The `class_` parameter is set to
    `AsyncSession` to create an asynchronous session.

    Returns:
        AsyncSession: An asynchronous database session.
    """
    # Create a new database session using the sessionmaker function
    async with sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )() as session:
        # Yield the session to the caller, allowing them to use it
        yield session


@app.post("/feedback/", response_model=Feedback)
async def create_feedback_endpoint(
    feedback: FeedbackCreate, db: AsyncSession = Depends(get_db)
) -> Feedback:
    """
    Endpoint for creating a new feedback.

    This endpoint accepts a JSON payload containing the feedback details
    and creates a new feedback record in the database.

    Args:
        feedback (FeedbackCreate): The feedback details to be created.
        db (AsyncSession, optional): The database session. Defaults to Depends(get_db).

    Returns:
        Feedback: The created feedback.
    """

    # Create a new feedback record in the database using the provided details
    return await create_feedback(db=db, feedback=feedback)



@app.get("/feedback/", response_model=List[Feedback])
async def read_feedback(db: AsyncSession = Depends(get_db)):
    """
    Endpoint for reading feedback records from the database.

    This endpoint retrieves all feedback records from the database
    and returns them as a list.

    Args:
        db (AsyncSession, optional): The database session. Defaults to Depends(get_db).

    Returns:
        List[Feedback]: A list of feedback records.
    """

    # Retrieve all feedback records from the database
    # and return them as a list
    return await get_feedback(db=db)
