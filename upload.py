import psycopg2

def upload_image_to_table(connection_string, table_name, image_path, image_name, image_desc):
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(connection_string)
        cursor = conn.cursor()

        # Read the image file
        with open(image_path, 'rb') as f:
            image_data = f.read()

        # Prepare the SQL statement to insert the image data into the table
        insert_statement = """
        INSERT INTO {} ( "user_id", "image", "desc") VALUES (%s, %s, %s)
        """.format(table_name)
        image_data = []
        image_desc = []
        # Execute the SQL statement
        cursor.execute(insert_statement, (image_name, image_data, image_desc))
        conn.commit()

        print("Image uploaded to table successfully.")

    except psycopg2.Error as e:
        print("Error uploading image to table:", e)

    finally:
        if conn is not None:
            cursor.close()
            conn.close()

import psycopg2

def append_to_array(connection_string, table_name, array_column1, array_column2, element, image_path):
    try:
        # Connect to the Supabase database
        conn = psycopg2.connect(connection_string)
        cursor = conn.cursor()
        with open(image_path, 'rb') as f:
            image_data = f.read()
        # Construct the SQL query to append elements to the array
        query = f"""
        SELECT *
        FROM your_table
        WHERE array_position('user_id', 'test') IS NOT NULL;
        SET {array_column1} = array_append(description, %s)
        SET {array_column2} = array_append(description, %s)
        """

        # Execute the SQL query for each new element
        cursor.execute(query, (element, image_data))
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
table_name = "ITEMS"
array_column1 = "description"
array_column2 = "image"
image_path = "image.jpg"
image_name = "test"
element = "cloak prismarine"

append_to_array(connection_string, table_name, array_column1, array_column2, element, image_path)


# # Example usage:
# connection_string = "postgresql://postgres.rzdyvqcuzbdcaibdrypw:ZYUK+q,sLwDGc4w@aws-0-us-west-1.pooler.supabase.com:5432/postgres" 
# table_name = "ITEMS"
# image_path = "image.jpg"
# image_name = "test"
# image_desc = "cloak prismarine"

# upload_image_to_table(connection_string, table_name, image_path, image_name, image_desc)
