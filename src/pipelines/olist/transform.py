from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

class OlistTransformer:
    """
    Realiza a transformação dos dados do Olist.
    """
    async def create_clean_orders_enriched(self, session: AsyncSession):

        # Remover a tabela existente
        drop_query = text("DROP TABLE IF EXISTS vw_orders_enriched")
        await session.execute(drop_query)

        # Criar a nova tabela
        create_query = text(
            """
            CREATE TABLE vw_orders_enriched AS
            SELECT
                -- Colunas de categorização
                o.order_status,
                c.customer_state,

                -- Identificadores
                o.order_id,
                o.customer_id,
                c.customer_unique_id,
                oi.product_id,
                oi.product_item_id,
                oi.shipping_limit_date,

                -- Colunas Agregadas
                SUM(oi.price) AS total_price,
                SUM(oi.freight_value) AS total_freight,
                COUNT(oi.product_id) AS total_items
            FROM
                olist_orders o
                JOIN bronze_olist_order_items oi ON o.order_id = oi.order_id
                JOIN bronze_olist_order_payments op ON oi.order_id = op.order_id
                JOIN bronze_olist_customers c ON o.customer_id = c.customer_id

            GROUP BY
                o.order_status,
                c.customer_state,
                op.payment_type
            """
        )

        await session.execute(create_query)
        await session.commit()
