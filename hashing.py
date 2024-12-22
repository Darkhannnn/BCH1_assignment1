import math

S = [7, 12, 17, 22] * 4 + [5, 9, 14, 20] * 4 + [4, 11, 16, 23] * 4 + [6, 10, 15, 21] * 4
K = [int(abs(2**32 * math.sin(i + 1))) & 0xFFFFFFFF for i in range(64)]

def left_rotate(x, c):
    return ((x << c) | (x >> (32 - c))) & 0xFFFFFFFF

def md5(message):
    message = bytearray(message, 'utf-8')
    original_length = (8 * len(message)) & 0xFFFFFFFFFFFFFFFF
    message.append(0x80)
    
    while len(message) % 64 != 56:
        message.append(0)
    
    message += original_length.to_bytes(8, byteorder='little')
    
    A, B, C, D = (0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476)
    
    for chunk_offset in range(0, len(message), 64):
        chunk = message[chunk_offset:chunk_offset + 64]
        M = [int.from_bytes(chunk[i:i + 4], byteorder='little') for i in range(0, 64, 4)]
        
        AA, BB, CC, DD = A, B, C, D
        
        for i in range(64):
            if 0 <= i <= 15:
                F = (B & C) | (~B & D)
                g = i
            elif 16 <= i <= 31:
                F = (D & B) | (~D & C)
                g = (5 * i + 1) % 16
            elif 32 <= i <= 47:
                F = B ^ C ^ D
                g = (3 * i + 5) % 16
            else:
                F = C ^ (B | ~D)
                g = (7 * i) % 16
            
            F = (F + A + K[i] + M[g]) & 0xFFFFFFFF
            A, D, C, B = D, C, B, (B + left_rotate(F, S[i])) & 0xFFFFFFFF
        
        A = (A + AA) & 0xFFFFFFFF
        B = (B + BB) & 0xFFFFFFFF
        C = (C + CC) & 0xFFFFFFFF
        D = (D + DD) & 0xFFFFFFFF
    
    return ''.join(f'{value:02x}' for value in A.to_bytes(4, 'little') + 
                                         B.to_bytes(4, 'little') + 
                                         C.to_bytes(4, 'little') + 
                                         D.to_bytes(4, 'little'))

def hash(text):
    return md5(text)

# print(hash("Hello, world!"))
