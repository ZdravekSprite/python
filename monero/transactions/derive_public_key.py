from config import *
#var der = generate_key_derivation(pub, sec)
#var pubkey = derive_public_key(der, i, spk)
def derive_public_key(der, i, spk):
    return True

'''
this.derive_public_key = function(derivation, out_index, pub) {
    if (derivation.length !== 64 || pub.length !== 64) {
        throw "Invalid input length!";
    }
    var derivation_m = Module._malloc(KEY_SIZE);
    var derivation_b = hextobin(derivation);
    Module.HEAPU8.set(derivation_b, derivation_m);
    var base_m = Module._malloc(KEY_SIZE);
    var base_b = hextobin(pub);
    Module.HEAPU8.set(base_b, base_m);
    var point1_m = Module._malloc(STRUCT_SIZES.GE_P3);
    var point2_m = Module._malloc(STRUCT_SIZES.GE_P3);
    var point3_m = Module._malloc(STRUCT_SIZES.GE_CACHED);
    var point4_m = Module._malloc(STRUCT_SIZES.GE_P1P1);
    var point5_m = Module._malloc(STRUCT_SIZES.GE_P2);
    var derived_key_m = Module._malloc(KEY_SIZE);
    if (Module.ccall("ge_frombytes_vartime", "bool", ["number", "number"], [point1_m, base_m]) !== 0) {
        throw "ge_frombytes_vartime returned non-zero error code";
    }
    var scalar_m = Module._malloc(STRUCT_SIZES.EC_SCALAR);
    var scalar_b = hextobin(this.derivation_to_scalar(bintohex(Module.HEAPU8.subarray(derivation_m, derivation_m + STRUCT_SIZES.EC_POINT)), out_index));
    Module.HEAPU8.set(scalar_b, scalar_m);
    Module.ccall("ge_scalarmult_base", "void", ["number", "number"], [point2_m, scalar_m]);
    Module.ccall("ge_p3_to_cached", "void", ["number", "number"], [point3_m, point2_m]);
    Module.ccall("ge_add", "void", ["number", "number", "number"], [point4_m, point1_m, point3_m]);
    Module.ccall("ge_p1p1_to_p2", "void", ["number", "number"], [point5_m, point4_m]);
    Module.ccall("ge_tobytes", "void", ["number", "number"], [derived_key_m, point5_m]);
    var res = Module.HEAPU8.subarray(derived_key_m, derived_key_m + KEY_SIZE);
    Module._free(derivation_m);
    Module._free(base_m);
    Module._free(scalar_m);
    Module._free(point1_m);
    Module._free(point2_m);
    Module._free(point3_m);
    Module._free(point4_m);
    Module._free(point5_m);
    Module._free(derived_key_m);
    return bintohex(res);
};
'''
if __name__ == '__main__':
    print(__file__)
