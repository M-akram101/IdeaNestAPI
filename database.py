from beanie import init_beanie, Document
from motor.motor_asyncio import AsyncIOMotorClient
from models import Organization, User


async def init():
    # Create Motor client
    client = AsyncIOMotorClient(
        "mongodb://mongodb:27017", uuidRepresentation="standard")
    

    # Initialize beanie with the Sample document class and a database
    await init_beanie(database=client.ideaNestdb, document_models=[User, Organization])