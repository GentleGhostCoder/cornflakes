Examples
==========

* S3

..  code-block:: python

    from dataclasses import InitVar
    from os.path import exists
    from typing import Literal, Optional

    from cornflakes import AnyUrl, Loader, config, config_field
    from cornflakes.common import default_ca_path


    def endpoint_validation(
        endpoint_url: str,
        values: dict,
    ):
        """Method to validate the endpoint_url and add scheme if missing.

        .. highlight: python

        :code:`client = boto3.client(**Boto3ClientConfig().to_dict())`
        """
        return (
            f'{"https://" if values.get("use_https") else "http://"}' f"{endpoint_url}"
            if "http" not in endpoint_url
            else endpoint_url
        )


    def ca_path_validation(ca_path: str):
        """Method check if the ca_path exists."""
        if not exists(ca_path):
            raise Exception(f"CA-Path {ca_path} does not exists!")
        return ca_path


    @config(
        files=["~/.s3cfg", "~/.aws/credentials", "~/.aws/config", "~/.custom-rc"],  # default s3 config file paths
        is_list=True,  # read instances into a list (not a dict -> by default for each section)
        frozen=True,  # make the config immutable
        validate=True,  # activate validation and type checking
        eval_env=True,  # evaluate environment variables
        default_loader=Loader.INI_LOADER,  # use the ini loader as default
    )
    class Boto3ClientConfig:
        """Config class for the boto3 client.

        This class is used to configure the boto3 client.
        Required configs are endpoint_url, access_key and secret_key (no_default argument).
        The values for access_key and secret_key are invisible in repr methods (repr = False).
        The alias argument is used to set the alias key searched in the files.
        """

        use_https: InitVar[bool] = config_field(alias=["signurl_use_https", "use_https"], default=True)
        endpoint_url: AnyUrl = config_field(
            alias=["endpoint-url", "host_base"], validator=endpoint_validation, no_default=True
        )
        aws_access_key_id: str = config_field(alias=["access_key"], repr=False, no_default=True)
        aws_secret_access_key: str = config_field(alias=["secret_key"], repr=False, no_default=True)
        service_name: Literal["s3", "ec2"] = "s3"
        region_name: Optional[str] = config_field(default=None, alias=["bucket_location", "region", "aws_default_region"])
        verify: str = config_field(default_factory=default_ca_path, validator=ca_path_validation)


* FastAPI

..  code-block:: python

    from typing import List, Optional

    from cornflakes import AnyUrl, config, config_field


    @config(files=".env", eval_env=True, validate=True)
    class Settings:
        """Some Fastapi settings."""

        PROJECT_NAME: str = "fastapi-boilerplate"

        SENTRY_DSN: Optional[AnyUrl] = None

        API_PATH: str = "/api/v1"

        ACCESS_TOKEN_EXPIRE_MINUTES: int = 7 * 24 * 60  # 7 days

        BACKEND_CORS_ORIGINS: List[AnyUrl] = None

        # The following variables need to be defined in environment
        TEST_DATABASE_URL: Optional[AnyUrl] = None
        DATABASE_URL: AnyUrl = config_field(no_default=True)  # no default value (required)
        ASYNC_DATABASE_URL: Optional[AnyUrl] = None

        SECRET_KEY: str = ""
        #  END: required environment variables
