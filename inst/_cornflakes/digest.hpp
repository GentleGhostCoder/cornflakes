// Copyright (c) 2022 Semjon Geist.

#ifndef INST__CORNFLAKES_DIGEST_HPP_
#define INST__CORNFLAKES_DIGEST_HPP_

#include <hash-library/crc32.h>
#include <hash-library/hmac.h>
#include <hash-library/keccak.h>
#include <hash-library/md5.h>
#include <hash-library/sha1.h>
#include <hash-library/sha256.h>
#include <hash-library/sha3.h>

#include <algorithm>
#include <string>
#include <vector>

namespace digest {  // cppcheck-suppress syntaxError

std::string hex_to_string(const std::string& hex);
template <typename HashMethod>
std::string apply_hmac(const std::vector<std::string>& data, std::string key);
std::string simple_hmac(const std::vector<std::string>& data, std::string algo);
std::string simple_sha256(const std::string& data);

}  // namespace digest

#endif  // INST__CORNFLAKES_DIGEST_HPP_
