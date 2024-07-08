from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime
from typing import List

from .models import Feedback
from .schemas import FeedbackCreate

async def create_feedback(db: AsyncSession, feedback: FeedbackCreate):
    """
    Create a new feedback record in the database.

    Args:
        db (AsyncSession): The database session.
        feedback (FeedbackCreate): The feedback details to be created.

    Returns:
        Feedback: The created feedback.
    """

    db_feedback = Feedback(
        **feedback.dict(),
        created_at=datetime.utcnow()
    )

    db.add(db_feedback)

    await db.commit()

    await db.refresh(db_feedback)

    return db_feedback



async def get_feedback(db: AsyncSession) -> List[Feedback]:
    """
    Retrieve all feedback records from the database.

    Args:
        db (AsyncSession): The database session.

    Returns:
        List[Feedback]: A list of feedback records.
    """

    # Execute the SQLAlchemy query to retrieve all feedback records
    query = select(Feedback)
    result = await db.execute(query)

    # Retrieve the feedback records and return them as a list
    return result.scalars().all()



