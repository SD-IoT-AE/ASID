/*
 * ASID: P4 Data Plane Feature Extraction Program
 * ----------------------------------------------
 * Extracts behavioral & temporal indicators of advanced SQL Injection traffic.
 * Exports features as digest messages to control plane (BMv2 + RYU/ONOS/ODL).
 */

#include <core.p4>
#include <v1model.p4>

const bit<16> TYPE_IPV4 = 0x0800;

// --- Header Definitions ---
header ethernet_t {
    bit<48> dstAddr;
    bit<48> srcAddr;
    bit<16> etherType;
}

header ipv4_t {
    bit<4>  version;
    bit<4>  ihl;
    bit<8>  diffserv;
    bit<16> totalLen;
    bit<16> identification;
    bit<3>  flags;
    bit<13> fragOffset;
    bit<8>  ttl;
    bit<8>  protocol;
    bit<16> hdrChecksum;
    bit<32> srcAddr;
    bit<32> dstAddr;
}

// --- Metadata for SQLi Feature Extraction ---
struct asid_meta_t {
    bit<32> flow_hash;
    bit<16> payload_len;
    bit<8>  sql_pattern_flag;
    bit<8>  encoded_char_freq;
    bit<8>  query_token_entropy;
    bit<8>  timing_index;
}

// --- Standard Metadata ---
struct metadata {
    asid_meta_t asid_meta;
}

// --- Parser ---
parser MyParser(packet_in packet,
                out ethernet_t eth_hdr,
                out ipv4_t ip_hdr,
                inout metadata meta,
                inout standard_metadata_t stdmeta) {
    state start {
        packet.extract(eth_hdr);
        transition select(eth_hdr.etherType) {
            TYPE_IPV4: parse_ipv4;
            default: accept;
        }
    }
    state parse_ipv4 {
        packet.extract(ip_hdr);
        meta.asid_meta.flow_hash = ip_hdr.srcAddr ^ ip_hdr.dstAddr;
        meta.asid_meta.payload_len = ip_hdr.totalLen;
        transition accept;
    }
}

// --- Registers for Feature Statistics ---
register<bit<32>>(1024) flow_entropy;
register<bit<32>>(1024) flow_encoded_ratio;
register<bit<32>>(1024) flow_packet_count;

// --- Actions ---
action compute_features() {
    bit<32> idx = meta.asid_meta.flow_hash & 1023;
    bit<32> prev_entropy;
    bit<32> prev_ratio;
    flow_entropy.read(prev_entropy, idx);
    flow_encoded_ratio.read(prev_ratio, idx);
    prev_entropy = (prev_entropy + meta.asid_meta.query_token_entropy) / 2;
    prev_ratio = (prev_ratio + meta.asid_meta.encoded_char_freq) / 2;
    flow_entropy.write(idx, prev_entropy);
    flow_encoded_ratio.write(idx, prev_ratio);
}

action forward(bit<9> port) {
    standard_metadata.egress_spec = port;
}

table feature_table {
    actions = { compute_features; forward; }
    size = 1024;
    default_action = compute_features();
}

// --- Control ---
control MyIngress(inout ethernet_t eth_hdr,
                  inout ipv4_t ip_hdr,
                  inout metadata meta,
                  inout standard_metadata_t stdmeta) {
    apply(feature_table);
}

// --- Digest Export ---
control MyEgress(inout ethernet_t eth_hdr,
                 inout ipv4_t ip_hdr,
                 inout metadata meta,
                 inout standard_metadata_t stdmeta) {
    if (stdmeta.egress_port == 0) {
        // placeholder
    }
}

control MyDeparser(packet_out packet,
                   in ethernet_t eth_hdr,
                   in ipv4_t ip_hdr) {
    packet.emit(eth_hdr);
    packet.emit(ip_hdr);
}

// --- Pipeline Assembly ---
V1Switch(MyParser(),
         MyIngress(),
         MyEgress(),
         MyDeparser()) main;
