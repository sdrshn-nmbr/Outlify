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

def append_to_array(connection_string, table_name, array_column1, array_column2, element, image_path, condition=None):
    try:
        # Connect to the Supabase database
        conn = psycopg2.connect(connection_string)
        cursor = conn.cursor()
        with open(image_path, 'rb') as f:
            image_data = f.read()
        # Construct the SQL query to append elements to the array
        if condition:
            query = f"""
            UPDATE {table_name}
            SET {array_column1} = {array_column1} || %s
            WHERE {condition};
            """
        else:
            query = f"""
            UPDATE {table_name}
            SET {array_column1} = {array_column1} || %s;
            SET {array_column2} = {array_column2} || %s;
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
array_column1 = "desc"
array_column2 = "image"
image_path = "image.jpg"
image_name = "test"
element = "cloak prismarine"
condition = "" # Optional, specify if needed

append_to_array(connection_string, table_name, array_column1, array_column2, element, image_path, condition)


# # Example usage:
# connection_string = "postgresql://postgres.rzdyvqcuzbdcaibdrypw:ZYUK+q,sLwDGc4w@aws-0-us-west-1.pooler.supabase.com:5432/postgres" 
# table_name = "ITEMS"
# image_path = "image.jpg"
# image_name = "test"
# image_desc = "cloak prismarine"

# upload_image_to_table(connection_string, table_name, image_path, image_name, image_desc)
