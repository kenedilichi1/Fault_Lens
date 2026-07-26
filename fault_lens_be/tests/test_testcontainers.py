from testcontainers.community.postgres import PostgresContainer

def test_postgres_container():
    with PostgresContainer("postgres:17") as postgres:
        url = postgres.get_connection_url()

        print(url)

        assert url.startswith("postgresql")