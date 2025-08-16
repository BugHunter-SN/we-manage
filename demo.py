import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# insert a new row into table
# new_row = (
#     supabase.table("demo-table")
#     .insert({"id": 3, "first_name": "Esther Doe"})
#     .execute()
# )

# updating a row in the table
updated_row = (
    supabase.table("demo-table")
    .update({"first_name": "Esther"})
    .eq("id", 3)
    .execute()
)

# delete a record
delete_row = (
    supabase.table("demo-table")
    .delete()
    .eq("id", 2)
    .execute()
)

# fetch all records
response = (
    supabase.table('demo-table')
    .select('*')
    .execute()
)
print(response)


