module or_gate(
	input wire a,
	input wire b,
	output wire y
);
assign y=a|b;

initial begin
        $dumpfile("dump.vcd");
        $dumpvars(1, or_gate);
    end
endmodule