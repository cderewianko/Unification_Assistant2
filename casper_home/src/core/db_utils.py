import subprocess

# Configuration
CONTAINER_NAME = "docker-raspberry-pi-postgres-1"  # change to your container name
DB_USER = "casper"
DB_NAME = "casper_home"


SAMPLE_MESSAGES = [
    {"topic": "home/livingroom/temperature", "payload": "21.5"},
    {"topic": "home/kitchen/humidity", "payload": "45%"},
    {"topic": "home/garage/door", "payload": "closed"},
]


# Helper to run SQL inside container
def run_sql(sql):
    cmd = [
        "docker", "exec", "-i", CONTAINER_NAME,
        "psql", "-U", DB_USER, "-d", "casper_home", "-c", sql
    ]
    # This truly works, just have to make sure the container is up and running.
    cmd_line = f'docker exec -i {CONTAINER_NAME} psql -U {DB_USER} -d {DB_NAME} -c "{sql}"'
    print('cmd      : ', cmd)
    print('cmd_line : ', cmd_line)
    #result = subprocess.run(cmd, capture_output=True, text=True)
    result = subprocess.run(cmd_line, capture_output=True, text=True)
    if result.returncode != 0:
        print("Error running SQL:", result.stderr)
    else:
        print(result.stdout)


# Reset database
def reset_database():
    print(f"Dropping and recreating database {DB_NAME}...")
    run_sql(f"DROP DATABASE IF EXISTS {DB_NAME};")
    run_sql(f"CREATE DATABASE {DB_NAME};")
    print("Database reset complete.")


# Create table
def create_table():
    print("Creating mqtt_messages table...")
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS mqtt_messages (
        id SERIAL PRIMARY KEY,
        topic TEXT NOT NULL,
        payload TEXT NOT NULL,
        received_at TIMESTAMPTZ DEFAULT NOW()
    );
    """
    cmd = [
        "docker", "exec", "-i", CONTAINER_NAME,
        "psql", "-U", DB_USER, "-d", DB_NAME, "-c", create_table_sql
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("Error creating table:", result.stderr)
    else:
        print(result.stdout)


# Insert sample messages
def insert_sample_messages():
    print("Inserting sample messages...")
    for msg in SAMPLE_MESSAGES:
        sql = f"INSERT INTO mqtt_messages (topic, payload) VALUES ('{msg['topic']}', '{msg['payload']}');"
        run_sql(sql) #f"\\c {DB_NAME}; {sql}")
    print("Sample messages inserted.")


if __name__ == "__main__":
    #reset_database()
    #create_table()
    insert_sample_messages()
    print("All done! Database reset, table created, sample messages inserted.")
