"""Initialize Flask app."""

from pathlib import Path
from flask import Flask

# imports from SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool

import games.adapters.repository as repo
from games.adapters import memory_repository, database_repository, repository_populate
from games.adapters.orm import metadata, map_model_to_tables


def create_app(test_config=None):
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)

    # Configure the app from configuration-file settings.
    app.config.from_object('config.Config')
    data_path = Path('games') / 'adapters' / 'data'

    if test_config is not None:
        # Load test configuration, and override any configuration t.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    # Here the "magic" of our repository pattern happens. We can easily switch between in memory data and
    # persistent database data storage for our application.

    if app.config['REPOSITORY'] == 'memory':
        # Create the MemoryRepository implementation for a memory-based repository.
        repo.repo_instance = memory_repository.MemoryRepository()
        # Fill the content of the repository from the provided csv files (has to be done every time we start app!)
        database_mode = False
        repository_populate.populate(data_path, repo.repo_instance, database_mode)

    elif app.config['REPOSITORY'] == 'database':
        # Configure database.
        database_uri = app.config['SQLALCHEMY_DATABASE_URI']

        # We create a comparatively simple SQLite database, which is based on a single file (see .env for URI).
        # For example the file database could be located locally and relative to the application in covid-19.db,
        # leading to a URI of "sqlite:///covid-19.db".
        # Note that create_engine does not establish any actual DB connection directly!
        database_echo = app.config['SQLALCHEMY_ECHO']
        # Please do not change the settings for connect_args and poolclass!
        database_engine = create_engine(database_uri, connect_args={"check_same_thread": False}, poolclass=NullPool,
                                        echo=database_echo)

        # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)
        # Create the SQLAlchemy DatabaseRepository instance for a sqlite3-based repository.
        repo.repo_instance = database_repository.SqlAlchemyRepository(session_factory)

        if app.config['TESTING'] == 'True' or len(database_engine.table_names()) == 0:
            print("REPOPULATING DATABASE...")
            # For testing, or first-time use of the web application, reinitialise the database.
            clear_mappers()
            metadata.create_all(database_engine)  # Conditionally create database tables.
            with database_engine.connect() as connection:
                for table in reversed(metadata.sorted_tables):  # Remove any data from the tables.
                    connection.execute(table.delete())

            # Generate mappings that map domain model classes to the database tables.
            map_model_to_tables()

            database_mode = True
            repository_populate.populate(data_path, repo.repo_instance, database_mode)
            print("REPOPULATING DATABASE... FINISHED")

        else:
            # Solely generate mappings that map domain model classes to the database tables.
            map_model_to_tables()

    app.config.from_object('config.Config')

    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)


    with app.app_context():
        from .browse import browse
        app.register_blueprint(browse.browse_blueprint)

        from .home import home
        app.register_blueprint(home.home_blueprint)

        from .description import description
        app.register_blueprint(description.description_blueprint)

        from .searchBar import searchBar
        app.register_blueprint(searchBar.search_blueprint)

        from .user import user
        app.register_blueprint(user.user_blueprint)

        from .authentication import authentication
        app.register_blueprint(authentication.login_blueprint)
        app.register_blueprint(authentication.signup_blueprint)
        app.register_blueprint(authentication.logout_blueprint)


    
    return app