import os
from infisical_client import InfisicalClient, ClientSettings, AuthenticationOptions, UniversalAuthMethod, GetSecretOptions
from dotenv import load_dotenv

class Devbeetl:
    client: InfisicalClient = None
    
    addr: str = None
    client_id: str = None
    client_secret: str = None
    project_id: str = None
    environment: str = None
    
    @staticmethod
    def env(name: str, default: str = None):
        """Get env variable or default"""
        if name in os.environ:
            return os.environ[name]
        if default is not None:
            return default
        
        raise ValueError(f"Environment variable {name} not found")
    
    @staticmethod
    def check_configured():
        """Check if Devbeetl is configured already"""
        load_dotenv()
        
        if Devbeetl.client is None:
            Devbeetl.addr = Devbeetl.env("INFISICAL_ADDR")
            Devbeetl.client_id = Devbeetl.env("INFISICAL_CLIENT_ID")
            Devbeetl.client_secret = Devbeetl.env("INFISICAL_CLIENT_SECRET")
            Devbeetl.project_id = Devbeetl.env("INFISICAL_PROJECT_ID")
            Devbeetl.environment = Devbeetl.env("INFISICAL_ENVIRONMENT")
            Devbeetl.client = InfisicalClient(
            ClientSettings(
                site_url=Devbeetl.addr,
                auth=AuthenticationOptions(
                    universal_auth=UniversalAuthMethod(
                        client_id=Devbeetl.client_id,
                        client_secret=Devbeetl.client_secret,
                    )
                ),
            )
        )

    
    @staticmethod
    def secret(name: str, path: str = None, project: str = None, environment: str = None):
        """
        Returns a secret from Infisical
        """
        if Devbeetl.client is None:	
            Devbeetl.check_configured()
        
        if project is None:
            project = Devbeetl.project_id
        
        if environment is None:
            environment = Devbeetl.environment

        secret = Devbeetl.client.getSecret(
            GetSecretOptions.from_dict(
                {
                    "projectId": project,
                    "secretName": name,
                    "environment": environment,
                    "path": path,
                }
            )
        )
        if secret is None:
            raise ValueError(f"Secret {name} not found in project {project}")
        
        return secret.secret_value