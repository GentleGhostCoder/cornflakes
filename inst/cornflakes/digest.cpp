// Copyright (c) 2022 Semjon Geist.

#include <digest.hpp>

//! collection of hash functions
namespace digest {

/// This is a simple C++ function to hash multiple strings with hmac
///
/// @param data value that needs to be hashed with SHA256
/// @returns hash string
std::string simple_sha256(const std::string& data) {
  SHA256 sha256;
  return sha256(data);
}

std::string hex_to_string(const std::string& hex) {
  std::vector<char> bytes;

  for (unsigned int i = 0; i < hex.length(); i += 2) {
    std::string byteString = hex.substr(i, 2);
    char byte = static_cast<char>(strtol(byteString.c_str(), nullptr, 16));
    bytes.push_back(byte);
  }

  return {bytes.begin(), bytes.end()};
}

template <typename HashMethod>
std::string apply_hmac(const std::vector<std::string>& data, std::string key) {
  key = hmac<HashMethod>(key, data[0]);

  //         skip first and iterate over each object
  for (const std::string& item : data) {
    key = hmac<HashMethod>(key, hex_to_string(item));
  }

  return (key);
}

/// This is a simple C++ function to hash multiple strings with hmac
///
/// @param data list of values (min. 2, the first value is the `key`) that needs
/// to be included in hash
/// @param algo name of the algorithm
/// @returns hash string
/// @note supported algorithms are ["SHA256", "SHA1"] and in future [ "SHA3",
/// "CRC32", "Keccak", "MD5"]
std::string simple_hmac(const std::vector<std::string>& data,
                        std::string algo = "SHA256") {
  std::vector<std::string> algorithms = {
      "SHA256", "SHA1", "SHA3", "CRC32", "Keccak", "MD5",
  };

  std::transform(algo.begin(), algo.end(), algo.begin(), ::toupper);

  switch (std::find(algorithms.begin(), algorithms.end(), algo) -
          algorithms.begin()) {
    case 0: {
      return apply_hmac<SHA256>({data.begin() + 1, data.end()}, data.at(0));
    } break;
    case 1: {
      return apply_hmac<SHA1>({data.begin() + 1, data.end()}, data.at(0));
    } break;
      //                  case 2 : {
      //                      return apply_hmac<SHA3>({data.begin() + 1,
      //                      data.end()}, data.at(0));
      //                  } break;
      //                  case 3 : {
      //                      return apply_hmac<CRC32>({data.begin() + 1,
      //                      data.end()}, data.at(0));
      //                  } break;
      //                  case 4 : {
      //                      return apply_hmac<Keccak>({data.begin() + 1,
      //                      data.end()}, data.at(0));
      //                  } break;
    default:
      return apply_hmac<MD5>(data, data.at(0));
  }
}

}  // namespace digest
