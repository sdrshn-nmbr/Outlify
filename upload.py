import psycopg2

def insert(connection_string, table_name, column_name, element_value):
    try:
        # Connect to the Supabase database
        conn = psycopg2.connect(connection_string)
        cursor = conn.cursor()
        with open(image_path, 'rb') as f:
            image_data = f.read()
        # Construct the SQL query to append elements to the array
        query = f"""
        DO $$
        BEGIN
            -- Check if the table exists
            IF NOT EXISTS (
                SELECT 1
                FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_name = '{table_name}'
            ) THEN
                -- Create the table if it doesn't exist
                CREATE TABLE {table_name} (
                    id SERIAL PRIMARY KEY,
                    image text,
                    description text
                );
            END IF;
        END $$;

        -- Insert an element into the table
        INSERT INTO {table_name} (description, image)
        VALUES ('apple', 'image.jpg');
        """

        # Execute the SQL query for each new element
        cursor.execute(query)
        conn.commit()

        print("Elements appended to the array successfully.")

    except psycopg2.Error as e:
        print("Error appending elements to the array:", e)

    finally:
        if conn is not None:
            cursor.close()
            conn.close()

# Example usage:
connection_string = "postgresql://postgres.rzdyvqcuzbdcaibdrypw:ZYUK+q,sLwDGc4w@aws-0-us-west-1.pooler.supabase.com:5432/postgres" 
table_name = "evan"
column_name = "description"
array_column2 = "image"
image_path = "image.jpg"
image_name = "test"
element = "cloak prismarine"

insert(connection_string, table_name, column_name, "")
