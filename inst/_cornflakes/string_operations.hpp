// Copyright (c) 2022 Semjon Geist.

#ifndef INST__CORNFLAKES_STRING_OPERATIONS_HPP_
#define INST__CORNFLAKES_STRING_OPERATIONS_HPP_

#include <document.h>
#include <istreamwrapper.h>
#include <pybind11/eval.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <stringbuffer.h>
#include <writer.h>

#include <algorithm>
#include <chrono>
#include <iostream>
#include <map>
#include <regex>
#include <set>
#include <sstream>
#include <string>
#include <unordered_set>
#include <utility>
#include <vector>

using std::chrono::duration;
using std::chrono::duration_cast;
using std::chrono::high_resolution_clock;
using std::chrono::milliseconds;
namespace py = pybind11;

namespace string_operations {  // cppcheck-suppress syntaxError
// Constants
//    inline const char NULL_CHAR = '0';
inline const char *QUOTE_CHARS = "\"\'";
inline const char MINUS_CHAR = '-';
//    inline const char PLUS_CHAR = '+';
inline const char *HEX_CHAR = "0X";
inline const char TRUE_CHAR = 'T';
inline const char FALSE_CHAR = 'F';
inline const char *NUMBER_CHARS = "+-.0123456789";
inline const std::string LINE_SEPERATORS = "\r\n";
inline const std::string COLUM_SEPERATORS = ",;\t|\b";
inline const std::string SPECIAL_CHARS = LINE_SEPERATORS + COLUM_SEPERATORS;
inline const std::vector<std::string> NAN_STRINGS = {
    "NA", "NONE", "NULL", "UNDEFINED", "NONETYPE", "\"\""};
inline const std::regex hex_regex = std::regex("0[xX][0-9a-fA-F]+");
inline const std::regex boolen_true_regex =
    std::regex("true", std::regex::icase);
inline const std::regex boolen_false_regex =
    std::regex("false", std::regex::icase);
inline const std::regex numeric_regex =
    std::regex("(^([+-]?\\d[0-9]*)?(\\.(.*e-)?)?([0-9]*)?$)");
static const std::regex uuid_regex(
    "^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-["
    "089ab][0-9a-f]{3}-[0-9a-f]{12}$",
    std::regex_constants::icase);
static const std::regex ipv4_regex(
    R"(^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.){3}(25[0-5]|(2[0-4]|1\d|[1-9]|)\d)$)");

inline rapidjson::Document json_doc;
inline std::string ESCAPE_CHAR = "\\";
inline std::string PYTHON_ESCAPE_CHAR = "\\\\";
inline const char *JSON_CHARS = "{}";
inline const char *ARRAY_CHARS = "[]";
// static const std::regex ipv6_regex(
//     "(?!^(?:(?:.*(?:::.*::|:::).*)|::|[0:]+[01]|.*[^:]:|[0-9a-fA-F](?:.*:.*){8}"
//     "[0-9a-fA-F]|(?:[0-9a-fA-F]:){1,6}[0-9a-fA-F])$)^(?:(::|[0-9a-fA-F]{1,4}:{"
//     "1,2})([0-9a-fA-F]{1,4}:{1,2}){0,6}([0-9a-fA-F]{1,4}|::)?)$");

inline const std::array<int, 2> empty_idx{};
//    inline const std::regex datetime_regex =
//    std::regex(R"((\d{4}[-./]?(\d{2}|\w{3})[-./]?\d{2}|\d{2}[-./]?(\d{2}|\w{3})[-./]?\d{4}|(\d{2}|\w{3})
//    (\d{2}|\w{3}) (\d{2}|\w{3}))(T|
//    )?(\d{2}[:]?\d{2}[:]?\d{1,11})?(.\d{1,6}(\+\d{2}:\d{3})?)?(Z)?([+]\d{2}[:]\d{2}|[+]\d{4})?)");
//    inline std::vector<std::string> country_codes_upper =
//    {"AF","AX","AL","DZ","AS","AD","AO","AI","AQ","AG","AR","AM","AW","AU","AT","AZ","BS","BH","BD","BB","BY","BE","BZ","BJ","BM","BT","BO","BQ","BA","BW","BV","BR","IO","BN","BG","BF","BI","KH","CM","CA","CV","KY","CF","TD","CL","CN","CX","CC","CO","KM","CG","CD","CK","CR","CI","HR","CU","CW","CY","CZ","DK","DJ","DM","DO","EC","EG","SV","GQ","ER","EE","ET","FK","FO","FJ","FI","FR","GF","PF","TF","GA","GM","GE","DE","GH","GI","GR","GL","GD","GP","GU","GT","GG","GN","GW","GY","HT","HM","VA","HN","HK","HU","IS","IN","ID","IR","IQ","IE","IM","IL","IT","JM","JP","JE","JO","KZ","KE","KI","KP","KR","KW","KG","LA","LV","LB","LS","LR","LY","LI","LT","LU","MO","MK","MG","MW","MY","MV","ML","MT","MH","MQ","MR","MU","YT","MX","FM","MD","MC","MN","ME","MS","MA","MZ","MM","NA","NR","NP","NL","NC","NZ","NI","NE","NG","NU","NF","MP","NO","OM","PK","PW","PS","PA","PG","PY","PE","PH","PN","PL","PT","PR","QA","RE","RO","RU","RW","BL","SH","KN","LC","MF","PM","VC","WS","SM","ST","SA","SN","RS","SC","SL","SG","SX","SK","SI","SB","SO","ZA","GS","SS","ES","LK","SD","SR","SJ","SZ","SE","CH","SY","TW","TJ","TZ","TH","TL","TG","TK","TO","TT","TN","TR","TM","TC","TV","UG","UA","AE","GB","US","UM","UY","UZ","VU","VE","VN","VG","VI","WF","EH","YE","ZM","ZW","AFG","ALB","DZA","ASM","AND","AGO","AIA","ATA","ATG","ARG","ARM","ABW","AUS","AUT","AZE","BHS","BHR","BGD","BRB","BLR","BEL","BLZ","BEN","BMU","BTN","BOL","BIH","BWA","BVT","BRA","IOT","VGB","BRN","BGR","BFA","BDI","KHM","CMR","CAN","CPV","CYM","CAF","TCD","CHL","CHN","CXR","CCK","COL","COM","COD","COG","COK","CRI","CIV","CUB","CYP","CZE","DNK","DJI","DMA","DOM","ECU","EGY","SLV","GNQ","ERI","EST","ETH","FRO","FLK","FJI","FIN","FRA","GUF","PYF","ATF","GAB","GMB","GEO","DEU","GHA","GIB","GRC","GRL","GRD","GLP","GUM","GTM","GIN","GNB","GUY","HTI","HMD","VAT","HND","HKG","HRV","HUN","ISL","IND","IDN","IRN","IRQ","IRL","ISR","ITA","JAM","JPN","JOR","KAZ","KEN","KIR","PRK","KOR","KWT","KGZ","LAO","LVA","LBN","LSO","LBR","LBY","LIE","LTU","LUX","MAC","MKD","MDG","MWI","MYS","MDV","MLI","MLT","MHL","MTQ","MRT","MUS","MYT","MEX","FSM","MDA","MCO","MNG","MSR","MAR","MOZ","MMR","NAM","NRU","NPL","ANT","NLD","NCL","NZL","NIC","NER","NGA","NIU","NFK","MNP","NOR","OMN","PAK","PLW","PSE","PAN","PNG","PRY","PER","PHL","PCN","POL","PRT","PRI","QAT","REU","ROU","RUS","RWA","SHN","KNA","LCA","SPM","VCT","WSM","SMR","STP","SAU","SEN","SCG","SYC","SLE","SGP","SVK","SVN","SLB","SOM","ZAF","SGS","ESP","LKA","SDN","SUR","SJM","SWZ","SWE","CHE","SYR","TWN","TJK","TZA","THA","TLS","TGO","TKL","TON","TTO","TUN","TUR","TKM","TCA","TUV","VIR","UGA","UKR","ARE","GBR","UMI","USA","URY","UZB","VUT","VEN","VNM","WLF","ESH","YEM","ZMB","ZWE"};
//    inline std::vector<std::string> country_codes_lower =
//    {"af","ax","al","dz","as","ad","ao","ai","aq","ag","ar","am","aw","au","at","az","bs","bh","bd","bb","by","be","bz","bj","bm","bt","bo","bq","ba","bw","bv","br","io","bn","bg","bf","bi","kh","cm","ca","cv","ky","cf","td","cl","cn","cx","cc","co","km","cg","cd","ck","cr","ci","hr","cu","cw","cy","cz","dk","dj","dm","do","ec","eg","sv","gq","er","ee","et","fk","fo","fj","fi","fr","gf","pf","tf","ga","gm","ge","de","gh","gi","gr","gl","gd","gp","gu","gt","gg","gn","gw","gy","ht","hm","va","hn","hk","hu","is","in","id","ir","iq","ie","im","il","it","jm","jp","je","jo","kz","ke","ki","kp","kr","kw","kg","la","lv","lb","ls","lr","ly","li","lt","lu","mo","mk","mg","mw","my","mv","ml","mt","mh","mq","mr","mu","yt","mx","fm","md","mc","mn","me","ms","ma","mz","mm","na","nr","np","nl","nc","nz","ni","ne","ng","nu","nf","mp","no","om","pk","pw","ps","pa","pg","py","pe","ph","pn","pl","pt","pr","qa","re","ro","ru","rw","bl","sh","kn","lc","mf","pm","vc","ws","sm","st","sa","sn","rs","sc","sl","sg","sx","sk","si","sb","so","za","gs","ss","es","lk","sd","sr","sj","sz","se","ch","sy","tw","tj","tz","th","tl","tg","tk","to","tt","tn","tr","tm","tc","tv","ug","ua","ae","gb","us","um","uy","uz","vu","ve","vn","vg","vi","wf","eh","ye","zm","zw","afg","alb","dza","asm","and","ago","aia","ata","atg","arg","arm","abw","aus","aut","aze","bhs","bhr","bgd","brb","blr","bel","blz","ben","bmu","btn","bol","bih","bwa","bvt","bra","iot","vgb","brn","bgr","bfa","bdi","khm","cmr","can","cpv","cym","caf","tcd","chl","chn","cxr","cck","col","com","cod","cog","cok","cri","civ","cub","cyp","cze","dnk","dji","dma","dom","ecu","egy","slv","gnq","eri","est","eth","fro","flk","fji","fin","fra","guf","pyf","atf","gab","gmb","geo","deu","gha","gib","grc","grl","grd","glp","gum","gtm","gin","gnb","guy","hti","hmd","vat","hnd","hkg","hrv","hun","isl","ind","idn","irn","irq","irl","isr","ita","jam","jpn","jor","kaz","ken","kir","prk","kor","kwt","kgz","lao","lva","lbn","lso","lbr","lby","lie","ltu","lux","mac","mkd","mdg","mwi","mys","mdv","mli","mlt","mhl","mtq","mrt","mus","myt","mex","fsm","mda","mco","mng","msr","mar","moz","mmr","nam","nru","npl","ant","nld","ncl","nzl","nic","ner","nga","niu","nfk","mnp","nor","omn","pak","plw","pse","pan","png","pry","per","phl","pcn","pol","prt","pri","qat","reu","rou","rus","rwa","shn","kna","lca","spm","vct","wsm","smr","stp","sau","sen","scg","syc","sle","sgp","svk","svn","slb","som","zaf","sgs","esp","lka","sdn","sur","sjm","swz","swe","che","syr","twn","tjk","tza","tha","tls","tgo","tkl","ton","tto","tun","tur","tkm","tca","tuv","vir","uga","ukr","are","gbr","umi","usa","ury","uzb","vut","ven","vnm","wlf","esh","yem","zmb","zwe"};;

py::object eval_type(std::string value);
py::object eval_datetime(const std::string &value);
std::map<std::string, py::object> eval_csv(
    const std::string &input, const char *extra_disallowed_header_chars);
bool is_nan(std::string value);

std::map<std::string, std::vector<std::string>> convert_to_map_str(
    const py::object &dictionary);
std::map<std::string, std::vector<py::object>> convert_to_map_py(
    const py::object &dictionary);

std::array<int, 2> idx_between(std::string::const_iterator start_iter,
                               std::string::const_iterator end_iter,
                               const std::string &begin_pattern,
                               const std::string &end_pattern, int skip);
std::string trim(const std::string &str, const std::string &whitespace = " \t");

py::list extract_between(const std::string &data, std::string start, char end);
py::object apply_match(const std::vector<std::string> &vec, std::string match);

void generateAvroSchema(const rapidjson::Value &value,
                        rapidjson::StringBuffer *buffer, int depth);

py::dict generateAvroSchemaPy(const std::string &jsonChunk);

const int MAX_DEPTH = 10000;

}  // namespace string_operations
#endif  // INST__CORNFLAKES_STRING_OPERATIONS_HPP_
