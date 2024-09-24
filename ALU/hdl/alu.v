module alu
#(
    parameter DATA_WIDTH = 32  // Parameterized data width with default value
)
(
    input  [DATA_WIDTH-1:0] A,    // First operand
    input  [DATA_WIDTH-1:0] B,    // Second operand
    input  [2:0] ALU_Sel,         // ALU operation selector
    output reg [DATA_WIDTH-1:0] ALU_Result, // ALU result
    output reg Zero                   // Zero flag
);

    // ALU Operation codes
    localparam ADD  = 3'b000;
    localparam SUB  = 3'b001;
    localparam AND  = 3'b010;
    localparam OR   = 3'b011;
    localparam XOR  = 3'b100;
    localparam GT   = 3'b101;   // Greater Than (signed)
    localparam GTU  = 3'b110;   // Greater Than (unsigned)
    localparam EQ   = 3'b111;   // Equal / Not Equal comparison

    always @(*) begin
        case (ALU_Sel)
            ADD:  ALU_Result = A + B;                     // Add
            SUB:  ALU_Result = A - B;                     // Subtract
            AND:  ALU_Result = A & B;                     // AND
            OR:   ALU_Result = A | B;                     // OR
            XOR:  ALU_Result = A ^ B;                     // XOR
            GT:   ALU_Result = ($signed(A) > $signed(B)); // Greater Than (signed)
            GTU:  ALU_Result = (A > B);                   // Greater Than (unsigned)
            EQ:   ALU_Result = (A == B) ? 1 : 0;          // Equal
            default: ALU_Result = {DATA_WIDTH{1'b0}};     // Default to zero
        endcase

        // Zero flag: Set if ALU_Result is zero
        Zero = (ALU_Result == {DATA_WIDTH{1'b0}});
    end

     // Dump waves
    initial begin
        $dumpfile("dump.vcd");
        $dumpvars(1, alu);
    end

endmodule
