def alu_model(a: int, b: int, operation: str, bit_width: int) -> int:
    """Model of an ALU that supports multiple operations with configurable bit width."""
    
    # Mask to constrain the inputs to the given bit width
    mask = (1 << bit_width) - 1
    a = a & mask
    b = b & mask

    if operation == "add":
        return (a + b) & mask  # Constrain result to bit width
    elif operation == "sub":
        return (a - b) & mask
    elif operation == "and":
        return a & b
    elif operation == "or":
        return a | b
    elif operation == "xor":
        return a ^ b
    elif operation == "gt":  # Greater than (signed)
        # Convert to signed values within bit_width
        signed_a = (a if a < (1 << (bit_width - 1)) else a - (1 << bit_width))
        signed_b = (b if b < (1 << (bit_width - 1)) else b - (1 << bit_width))
        return int(signed_a > signed_b)
    elif operation == "gtu":  # Greater than (unsigned)
        return int(a > b)  # Already masked for unsigned comparison
    elif operation == "eq":  # Equal
        return int(a == b)
    elif operation == "neq":  # Not equal
        return int(a != b)
    else:
        raise ValueError(f"Unsupported operation: {operation}")


