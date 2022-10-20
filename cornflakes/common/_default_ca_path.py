import os
from typing import Tuple


def default_ca_path() -> str:
    """Find default ca-certificate of the current system.

    :return: system default ca-certificate
    """
    # Possible certificate files; stop after finding one.
    cert_paths: Tuple[str, ...] = (
        "/etc/ssl/certs/ca-certificates.crt",  # Debian/Ubuntu/Gentoo etc.
        "/etc/pki/tls/certs/ca-bundle.crt",  # Fedora/RHEL 6
        "/etc/ssl/ca-bundle.pem",  # OpenSUSE
        "/etc/pki/tls/cacert.pem",  # OpenELEC
        "/etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem",  # CentOS/RHEL 7
        "/etc/ssl/cert.pem",  # Alpine Linux
    )

    # Possible directories with certificate files; stop after successfully
    # reading at least one file from a directory.
    cert_directories: Tuple[str, ...] = (
        "/etc/ssl/certs",  # SLES10/SLES11, https://golang.org/issue/12139
        "/etc/pki/tls/certs",  # Fedora/RHEL
        "/system/etc/security/cacerts",  # Android
    )

    return next(
        (cert_path for cert_path in cert_paths if os.path.isfile(cert_path) and os.access(cert_path, os.R_OK)),
        next(
            (
                next(
                    (
                        os.path.join(cert_dir, cert_path)
                        for cert_path in os.listdir(cert_dir)
                        if os.access(os.path.join(cert_dir, cert_path), os.R_OK)
                    ),
                    "",
                )
                for cert_dir in cert_directories
                if os.path.exists(cert_dir)
            ),
            "",
        ),
    )
