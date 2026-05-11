import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sales_data(rows=100):
    data = {
        'order_id': range(1, rows + 1),
        'customer_id': np.random.randint(100, 150, size=rows),
        'product_category': np.random.choice(['Electronics', 'Home', 'Apparel'], rows),
        'amount': np.round(np.random.uniform(10.5, 500.0, size=rows), 2),
        'order_date': [(datetime.now() - timedelta(days=x)).strftime('%Y-%m-%d') for x in range(rows)],
        'status': np.random.choice(['Completed', 'Pending', 'Cancelled', None], rows)
    }
    df = pd.DataFrame(data)
    df.to_csv('sales_data.csv', index=False)

if __name__ == "__main__":
    generate_sales_data()