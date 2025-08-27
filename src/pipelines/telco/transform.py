from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

class TelcoTransformer:
    async def create_clean_customer_table(self, session: AsyncSession):
        
        # Create view
        create_query = text("""
        CREATE VIEW clean_telco_customers AS
        SELECT 
            customerID,
            CASE 
                WHEN gender = 'Male' THEN 1 
                ELSE 0 
            END as is_male,
            CAST(SeniorCitizen as INTEGER) as is_senior,
            CASE 
                WHEN Churn = 'Yes' THEN 1 
                ELSE 0 
            END as churned,
            CAST(REPLACE(TotalCharges, ' ', '0') as FLOAT) as total_charges,
            CAST(MonthlyCharges as FLOAT) as monthly_charges
        FROM raw_telco_customer_churn
        WHERE customerID IS NOT NULL
        """)
    
        await session.execute(create_query)