/*
 * ASID Digest Export Logic
 * -------------------------
 * Sends periodic feature summaries (entropy, encoded ratio, etc.)
 * to the controller for ML-based classification.
 */

#include <core.p4>
#include <v1model.p4>

control FeatureExport(inout metadata meta,
                      inout standard_metadata_t stdmeta) {
    apply {
        digest_data_t d;
        d.flow_hash = meta.asid_meta.flow_hash;
        d.payload_len = meta.asid_meta.payload_len;
        d.entropy = meta.asid_meta.query_token_entropy;
        d.encoded_ratio = meta.asid_meta.encoded_char_freq;
        generate_digest(1, d);
    }
}
