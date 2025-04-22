from devbeetl import Devbeetl
from beetl.beetl import Beetl, BeetlConfig


# Only run fetch and compare, do not update any data
# Set this via env variable BEETL_DRYRUN
DRY_RUN = False


# Define the configuration
def make_config():
    secret_value = Devbeetl.secret(
        "test_secret",
        project="12345678-1234-1234-1234-1234567890",
        environment="dev",
    )
    
    return BeetlConfig(
        {
            "sources": [
                {
                    "name": "staticsrc",
                    "type": "Static",
                    "connection": {
                        "static": [
                            {"id": 1, "name": secret_value, "email": "john@test.com"},
                            {"id": 2, "name": "Jane", "email": "jane@test.com"},
                            {"id": 3, "name": "Steffen", "email": "steffen@test.com"},
                        ]
                    },
                },
                {
                    "name": "staticdst",
                    "type": "Static",
                    "connection": {
                        "static": [
                            {"id": 1, "name": secret_value, "email": "john@test.com"},
                            {"id": 4, "name": "James", "email": "jane@test.com"},
                            {"id": 3, "name": "Stephen", "email": "stephen@test.com"},
                        ]
                    },
                },
            ],
            "sync": [
                {
                    "source": "staticsrc",
                    "destination": "staticdst",
                    "sourceConfig": {},
                    "destinationConfig": {},
                    "comparisonColumns": [
                        {
                            "name": "id",
                            "type": "Int64",
                            "unique": True,
                        },
                        {
                            "name": "name",
                            "type": "Utf8",
                        },
                        {
                            "name": "email",
                            "type": "Utf8",
                        },
                    ],
                    "sourceTransformers": [],
                    "destinationTransformers": [],
                    "insertionTransformers": [],
                }
            ],
        }
    )

# Run the sync
if __name__ == "__main__":
    dryRun = Devbeetl.env("BEETL_DRYRUN", "true")
    if dryRun.lower() == "true":
        DRY_RUN = True

    beetl = Beetl(make_config())
    beetl.sync(DRY_RUN)