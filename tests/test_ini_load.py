import os
import unittest

import cornflakes


class TestIniLoad(unittest.TestCase):
    """Tests for ini_load."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.maxDiff = None
        os.environ["ENV_VAR1"] = "blabla"

    def test_ini_load_examples1(self):
        self.assertEqual(
            cornflakes.ini_load(
                files={
                    "s3_configs": [
                        "tests/configs/.s3cfg",
                        "tests/configs/aws_config",
                        "tests/configs/aws_credentials",
                    ]
                },
                sections=["qa", "prod", "default"],
                keys={
                    "signurl_use_https": ["signurl_use_https"],
                    "aws_access_key_id": ["access_key", "aws_access_key_id"],
                    "aws_secret_access_key": ["secret_key"],
                    "endpoint_url": ["endpoint-url", "host_base"],
                    "region_name": ["bucket_location", "region", "aws_default_region"],
                    "service_name": ["service_name"],
                    "verify": ["ca_certs", "aws_ca_bundle", "ca_bundle"],
                    "env_var1": "env_var1",
                },
                defaults={
                    # "region_name": "us-east-1",
                    "signurl_use_https": True,
                    "service_name": "s3",
                },
            ),
            {
                "s3_configs": {
                    "default": {
                        "aws_access_key_id": "XXXXXXXX",
                        "aws_secret_access_key": "XXXXXXXXXXXXXXXXXXXXXXXXXX",
                        "endpoint_url": "https://some-s3-endpoint.example",
                        "env_var1": "blabla",
                        "service_name": "s3",
                        "signurl_use_https": True,
                        "region_name": "us-east-1",
                    },
                    "prod": {
                        "env_var1": "blabla",
                        "service_name": "s3",
                        "signurl_use_https": True,
                        "aws_access_key_id": "XXXXXXXX",
                    },
                    "qa": {
                        "env_var1": "blabla",
                        "service_name": "s3",
                        "signurl_use_https": True,
                        "aws_access_key_id": "XXXXXXXX",
                    },
                }
            },
        )

    def test_ini_load_examples2(self):
        self.assertEqual(
            cornflakes.ini_load(
                files={"s3_configs": ["tests/configs/.s3cfg"]},
                sections=["qa", "prod", "default"],
                keys={
                    "signurl_use_https": ["signurl_use_https"],
                    "aws_access_key_id": ["access_key", "aws_access_key_id"],
                    "aws_secret_access_key": ["secret_key"],
                    "endpoint_url": ["endpoint-url", "host_base"],
                    "region_name": ["bucket_location", "region", "aws_default_region"],
                    "service_name": ["service_name"],
                    "verify": ["ca_certs", "aws_ca_bundle", "ca_bundle"],
                    "env_var1": "env_var1",
                },
                defaults={
                    # "region_name": "us-east-1",
                    "signurl_use_https": True,
                    "service_name": "s3",
                },
            ),
            {
                "s3_configs": {
                    "default": {
                        "aws_access_key_id": "XXXXXXXXXXXXXXXXXXXXXXXXXX",
                        "aws_secret_access_key": "XXXXXXXXXXXXXXXXXXXXXXXXXX",
                        "endpoint_url": "some-s3-endpoint.example",
                        "env_var1": "blabla",
                        "service_name": "s3",
                        "signurl_use_https": True,
                    },
                    "prod": {"env_var1": "blabla", "service_name": "s3", "signurl_use_https": True},
                    "qa": {"env_var1": "blabla", "service_name": "s3", "signurl_use_https": True},
                }
            },
        )

    def test_ini_load_examples3(self):
        self.assertEqual(
            cornflakes.ini_load(
                files={None: ["tests/configs/.s3cfg"]},
                keys={
                    "signurl_use_https": ["signurl_use_https"],
                    "aws_access_key_id": ["access_key", "aws_access_key_id"],
                    "aws_secret_access_key": ["secret_key"],
                    "endpoint_url": ["endpoint-url", "host_base"],
                    "region_name": ["bucket_location", "region", "aws_default_region"],
                    "service_name": ["service_name"],
                    "verify": ["ca_certs", "aws_ca_bundle", "ca_bundle"],
                    "env_var1": "env_var1",
                },
                defaults={
                    # "region_name": "us-east-1",
                    "signurl_use_https": True,
                    "service_name": "s3",
                },
            ),
            {
                "default": {
                    "aws_access_key_id": "XXXXXXXXXXXXXXXXXXXXXXXXXX",
                    "aws_secret_access_key": "XXXXXXXXXXXXXXXXXXXXXXXXXX",
                    "endpoint_url": "some-s3-endpoint.example",
                    "env_var1": "blabla",
                    "service_name": "s3",
                    "signurl_use_https": True,
                },
                "test1": {"env_var1": "blabla", "service_name": "s3", "signurl_use_https": True},
                "test2": {"env_var1": "blabla", "service_name": "s3", "signurl_use_https": True},
            },
        )

    def test_ini_load_examples4(self):
        self.assertEqual(
            cornflakes.ini_load(
                files={None: ["tests/configs/.s3cfg"]},
                sections={None: ["qa", "prod", "default"]},
                keys={
                    "signurl_use_https": ["signurl_use_https"],
                    "aws_access_key_id": ["access_key", "aws_access_key_id"],
                    "aws_secret_access_key": ["secret_key"],
                    "endpoint_url": ["endpoint-url", "host_base"],
                    "region_name": ["bucket_location", "region", "aws_default_region"],
                    "service_name": ["service_name"],
                    "verify": ["ca_certs", "aws_ca_bundle", "ca_bundle"],
                    "env_var1": "env_var1",
                },
                defaults={
                    # "region_name": "us-east-1",
                    "signurl_use_https": True,
                    "service_name": "s3",
                },
            ),
            {
                "aws_access_key_id": "XXXXXXXXXXXXXXXXXXXXXXXXXX",
                "aws_secret_access_key": "XXXXXXXXXXXXXXXXXXXXXXXXXX",
                "endpoint_url": "some-s3-endpoint.example",
                "env_var1": "blabla",
                "service_name": "s3",
                "signurl_use_https": True,
            },
        )

    def test_ini_load_examples5(self):
        self.assertEqual(
            cornflakes.ini_load(
                files={None: ["tests/configs/.s3cfg"]},
                sections={None: ["qa", "prod", "default"]},
                defaults={
                    # "region_name": "us-east-1",
                    "signurl_use_https": True,
                    "service_name": "s3",
                },
            ),
            {
                "access_key": "XXXXXXXXXXXXXXXXXXXXXXXXXX",
                "acl_private": True,
                "bucket_location": "us-west-1",
                "check_ssl_certificate": True,
                "check_ssl_hostname": True,
                "cloudfront_host": "some-s3-endpoint.example",
                "default_mime_type": "binary/octet-stream",
                "delay_updates": False,
                "delete_after": False,
                "delete_after_fetch": False,
                "delete_removed": False,
                "dry_run": False,
                "enable_multipart": True,
                "encoding": "UTF-8",
                "encrypt": False,
                "follow_symlinks": False,
                "force": False,
                "get_continue": False,
                "gpg_command": "/usr/bin/gpg",
                "gpg_decrypt": "%(gpg_command)s -d --verbose --no-use-agent --batch --yes --passphrase-fd %(passphrase_fd)s -o %(output_file)s %(input_file)s",
                "gpg_encrypt": "%(gpg_command)s -c --verbose --no-use-agent --batch --yes --passphrase-fd %(passphrase_fd)s -o %(output_file)s %(input_file)s",
                "guess_mime_type": True,
                "host_base": "some-s3-endpoint.example",
                "host_bucket": "some-s3-endpoint.example",
                "human_readable_sizes": False,
                "invalidate_default_index_on_cf": False,
                "invalidate_default_index_root_on_cf": True,
                "invalidate_on_cf": False,
                "limit": -1,
                "limitrate": 0,
                "list_md5": False,
                "long_listing": False,
                "max_delete": -1,
                "multipart_chunk_size_mb": 15,
                "multipart_max_chunks": 10000,
                "preserve_attrs": True,
                "progress_meter": True,
                "proxy_port": 0,
                "put_continue": False,
                "recursive": False,
                "recv_chunk": 65536,
                "reduced_redundancy": False,
                "requester_pays": False,
                "restore_days": 1,
                "restore_priority": "Standard",
                "secret_key": "XXXXXXXXXXXXXXXXXXXXXXXXXX",
                "send_chunk": 65536,
                "server_side_encryption": False,
                "signature_v2": False,
                "signurl_use_https": True,
                "simpledb_host": "sdb.amazonaws.com",
                "skip_existing": False,
                "socket_timeout": 300,
                "stats": False,
                "stop_on_error": False,
                "urlencoding_mode": "normal",
                "use_http_expect": False,
                "use_https": True,
                "use_mime_magic": True,
                "verbosity": "WARNING",
                "website_endpoint": "https://%(bucket)s.some-s3-endpoint.example/",
                "website_index": "index.html",
            },
        )

    def test_ini_load_examples6(self):
        self.assertEqual(cornflakes.ini_load({None: "tests/configs/.s3cfg"}, {None: "test1"}), {"test": "test1"})
        self.assertEqual(
            cornflakes.ini_load({None: "tests/configs/some_config"}),
            {
                "default": {
                    "test3": 12345,
                    "test": '{"bla": "blub"}',
                    "test2[BLA]": "[bla]=bla",
                    "test4": 12345,
                    "username": "testuser",
                    "user": "testuser2",
                },
                "not_default": {
                    "test3": 12345,
                    "test": '{"bla": "blub"}',
                    "test2[BLA]": "[bla]=bla",
                    "test4": 12345,
                    "username": "testuser",
                    "user": "testuser2",
                },
                "EU": {
                    "username": "blub",
                    "password": "blabla",
                    "port": 443,
                    "host1": "bla.eu.host.com",
                    "host2": "bla2.eu.host.com",
                },
                "US": {
                    "username": "blub",
                    "password": "blabla",
                    "port": 443,
                    "host1": "bla.us.host.com",
                    "host2": "bla2.us.host.com",
                },
            },
        )
        self.assertEqual(
            cornflakes.ini_load({None: "tests/configs/some_config"}, keys={"test3": "*"}),
            {
                "default": {"test3": [1234, 123456, 12345]},
                "not_default": {"test3": [1234, 123456, 12345]},
                "EU": {},
                "US": {},
            },
        )
        self.assertEqual(
            cornflakes.ini_load({None: "tests/configs/some_config"}, keys={"test": "**"}),
            {
                "default": {
                    "test": {"test3": 12345, "test": '{"bla": "blub"}', "test2[BLA]": "[bla]=bla", "test4": 12345}
                },
                "not_default": {
                    "test": {"test3": 12345, "test": '{"bla": "blub"}', "test2[BLA]": "[bla]=bla", "test4": 12345}
                },
                "EU": {},
                "US": {},
            },
        )
        self.assertEqual(
            cornflakes.ini_load(
                {None: "tests/configs/some_config"},
                keys={"user": ["username"], "password": ["password"]},
            ),
            {
                "default": {"user": "testuser"},
                "not_default": {"user": "testuser"},
                "EU": {"password": "blabla", "user": "blub"},
                "US": {"password": "blabla", "user": "blub"},
            },
        )
