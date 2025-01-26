#ifndef RSA_LIBRARY_H
#define RSA_LIBRARY_H

#ifdef _WIN32
    #ifdef BUILD_DLL
        #define DLL_EXPORT __declspec(dllexport)
    #else
        #define DLL_EXPORT
    #endif
#else
    #define DLL_EXPORT
#endif

extern "C" {
    DLL_EXPORT void generate_rsa_keys(int bits, const char* public_key_file, const char* private_key_file);
    DLL_EXPORT int rsa_encrypt(const char* public_key_file, const char* input, const char* output);
    DLL_EXPORT int rsa_decrypt(const char* private_key_file, const char* input_file, const char* output_file);
}

#endif // RSA_LIBRARY_H
