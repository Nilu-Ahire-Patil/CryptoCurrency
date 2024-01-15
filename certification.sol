// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.7.0 <0.9.0;

contract CertificateVerification {

    struct Certificate {

        address CertificateIssuer;
        string CertificateHashValue;
        bool isVerified;

    }

    mapping(string => Certificate) public certificates;

    function NewCertificate(string memory CertificateHashValue) external {

        require(certificates[CertificateHashValue].CertificateIssuer == address(0), "This Certificate Allredy Certified");

        certificates[CertificateHashValue] = Certificate({

            CertificateIssuer: msg.sender,

            CertificateHashValue: CertificateHashValue,

            isVerified: false

        });

    }

    function verifyCertificate(string memory CertificateHashValue) external {

        require(certificates[CertificateHashValue].CertificateIssuer != address(0), "Not found");

        require(certificates[CertificateHashValue].isVerified == false, "Already verified");

        require(msg.sender == certificates[CertificateHashValue].CertificateIssuer, "Only the Issuer can verify the certificate");

        certificates[CertificateHashValue].isVerified = true;

    }

    function isCertificateVerified(string memory CertificateHashValue) external view returns (bool) {

        return certificates[CertificateHashValue].isVerified;

    }

}
