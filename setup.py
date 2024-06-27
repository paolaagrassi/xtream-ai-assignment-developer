import os
from setuptools import setup, Command
import shutil


class CreateEnvFile(Command):
    """Command to create a .env file from a template."""

    description = "create a .env file from a template"
    user_options = []
    
    user_env_options = {
        "POSTGRES_USER": os.environ.get("POSTGRES_USER", ""),
        "POSTGRES_PASSWORD": os.environ.get("POSTGRES_PASSWORD", ""),
        "POSTGRES_DB": os.environ.get("POSTGRES_DB", ""),
        "PGADMIN_DEFAULT_EMAIL":os.environ.get("PGADMIN_DEFAULT_EMAIL", ""),
        "PGADMIN_DEFAULT_PASSWORD":os.environ.get("PGADMIN_DEFAULT_PASSWORD", ""),
    }

    def initialize_options(self):
        """This method is called when the command is run."""
        pass

    def finalize_options(self):
        """This method is called after all the command-line options have been parsed."""
        pass

    def run(self):
        if not os.path.exists(".env"):
            shutil.copy(".env.example", ".env")

            with open(".env", "r") as file:
                env_content = file.read()
            with open(".env", "w") as file:
                file.write(env_content.format(**self.user_env_options))

            print("Created a .env file from .env.example")


setup(
    cmdclass={
        "create_env_file": CreateEnvFile,
    }
)