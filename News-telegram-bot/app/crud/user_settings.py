from sqlalchemy import select, insert, update
from app.db.session import async_session
from app.models.user_settings import UserSettingsModel

async def get_or_create_user_settings(user_id: int):
    async with async_session() as session:
        query = select(UserSettingsModel).where(UserSettingsModel.user_id == user_id)
        result = await session.execute(query)
        settings = result.scalar_one_or_none()

        if not settings:
            stmt = insert(UserSettingsModel).values(user_id=user_id).returning(UserSettingsModel)
            result = await session.execute(stmt)
            settings = result.scalar_one()
            await session.commit()

        return settings

async def update_user_setting(user_id: int, field: str, value):

    valid_fields = {
        'digest_country', 'digest_page', 'search_country', 
        'search_page', 'sort_by', 'time_for_search'
    }
    
    if field not in valid_fields:
        raise ValueError(f"Invalid field: {field}")
    
    # Validate values based on field type
    if field in ['digest_page', 'search_page']:
        if not isinstance(value, int) or value < 1 or value > 100:
            raise ValueError(f"Page size must be between 1 and 100, got: {value}")
    
    if field == 'time_for_search':
        if not isinstance(value, int) or value < 1 or value > 168:
            raise ValueError(f"Time period must be between 1 and 168 hours, got: {value}")
    
    if field in ['digest_country', 'search_country']:
        if not isinstance(value, str) or len(value) != 2:
            raise ValueError(f"Country code must be 2 characters, got: {value}")
    
    if field == 'sort_by':
        valid_sorts = ['relevancy', 'popularity', 'publishedAt']
        if value not in valid_sorts:
            raise ValueError(f"Sort option must be one of {valid_sorts}, got: {value}")
    
    async with async_session() as session:
        stmt = (
            update(UserSettingsModel)
            .where(UserSettingsModel.user_id == user_id)
            .values({field: value})
        )
        await session.execute(stmt)
        await session.commit()
