import os
import psycopg2

class PostgresPipeline:
    def open_spider(self,spider):
        #connect to Postgresql
        self.connection = psycopg2.connect(
            host=os.environ["PGHOST"],
            port=os.environ["PGPORT"],
            database=os.environ["PGDATABASE"],
            user=os.environ["PGUSER"],
            password=os.environ["PGPASSWORD"]
        )
        self.cursor = self.connection.cursor()
        print("Connected to Postgres sucessfully!")

    def process_item(self,item,spider):
        #Insert book details into PostgreSQL
        self.cursor.execute(
            """
            INSERT INTO books (title, price, url)
            VALUES (%s,%s,%s)
            ON CONFLICT (url) DO NOTHING
            """ ,
            (
                item["title"],
                item["price"],
                item["url"]
            )

        )
        self.connection.commit()
        return item 

    def close_spider(self,spider):
        #close database connection
        self.cursor.close()
        self.connection.close()
        print("PostgreSQL connection closed!")
    
